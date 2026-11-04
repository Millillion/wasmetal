#!/usr/bin/env python3
"""Audit every official instruction row through RTL and compare full CPU execution."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from build_identity import verify
from prepare_standalone import ROOT,digest


def compare(report,reference,records):
    for data in [report,reference]:
        if not data['full_core_suite_selected'] or not data['full_core_suite_passed'] or data['identity_error']:
            raise ValueError('complete passing official corpus required')
        if len(data['suites'])!=data['suite_files'] or any(s['failures'] for s in data['suites']):
            raise ValueError('incomplete or failed suites')
    for key in ['official_sources_sha256','suite_files','memory_wait_states','capacities','totals']:
        if report[key]!=reference[key]:raise ValueError('different corpus result: '+key)
    expected={s['suite']:s for s in reference['suites']}
    actual={s['suite']:s for s in report['suites']}
    if len(actual)!=report['suite_files'] or set(actual)!=set(expected):
        raise ValueError('duplicate or missing official suite')
    for name,suite in actual.items():
        for key in ['counts','command_count','command_cycles','executed_commands']:
            if suite[key]!=expected[name][key]:raise ValueError('instruction codec changed '+name+': '+key)
    if len(records)!=report['suite_files']+1:
        raise ValueError('missing per-process coverage, including capability-negotiation fixture')
    layouts=[0]*4;opcodes=set();rows=0
    for record in records:
        if len(record['layouts'])!=4 or any(type(n)!=int or n<0 for n in record['layouts']):
            raise ValueError('invalid layout counters')
        if type(record['rows_checked'])!=int or sum(record['layouts'])!=record['rows_checked']:
            raise ValueError('inconsistent loaded-row counters')
        if any(type(n)!=int or not 0<=n<1<<32 for n in record['opcodes']):
            raise ValueError('invalid observed opcode')
        if record['opcodes']!=sorted(set(record['opcodes'])):raise ValueError('duplicate opcode observations')
        rows+=record['rows_checked'];opcodes.update(record['opcodes'])
        layouts=[a+b for a,b in zip(layouts,record['layouts'])]
    if not rows or not opcodes:raise ValueError('no instructions were audited')
    return {'processes':len(records),'rows_checked':rows,'layouts':layouts,
            'distinct_opcode_values':len(opcodes),'opcodes':sorted(opcodes)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference',type=Path,required=True)
    parser.add_argument('--jobs',type=int,default=4)
    args=parser.parse_args()
    if args.jobs<1:parser.error('jobs must be positive')
    binary=ROOT/'build/instruction-codec-sim/obj/Vwasmetal_core';identity=verify(binary)
    reference=json.loads(args.reference.read_text());reference_hash=digest(args.reference)
    source_hash=digest(Path(__file__).resolve())
    parent=ROOT/'build/instruction-codec-sim/coverage';parent.mkdir(parents=True,exist_ok=True)
    directory=Path(tempfile.mkdtemp(prefix='run-',dir=parent))
    report_path=ROOT/'reports/instruction-codec-core.json'
    subprocess.run([sys.executable,str(ROOT/'tools/run_spec.py'),'--simulator',str(binary),
        '--wait-states',str(reference['memory_wait_states']),'--jobs',str(args.jobs),
        '--schedule-from',str(args.reference),'--report',str(report_path),
        '--progress-report',str(ROOT/'reports/instruction-codec-progress.json')],cwd=ROOT,
        env=dict(os.environ,WASMETAL_CODEC_COVERAGE=str(directory)),check=True)
    report=json.loads(report_path.read_text());paths=sorted(directory.glob('*.jsonl'))
    records=[json.loads(line) for p in paths for line in p.read_text().splitlines()]
    coverage=compare(report,reference,records)
    if verify(binary)!=identity or report['build_manifest']!=identity:
        raise ValueError('codec simulator identity changed')
    if digest(args.reference)!=reference_hash or digest(Path(__file__).resolve())!=source_hash:
        raise ValueError('corpus verification inputs changed')
    result={'status':'passed','scope':'complete host-backed CPU with RTL codec on instruction inputs and every loaded row audited; not local memory or routing',
        'coverage':coverage,'all_native_counts_and_command_cycles_identical':True,
        'corpus_report':str(report_path.relative_to(ROOT)),'corpus_report_sha256':digest(report_path),
        'reference_sha256':reference_hash,'model':identity,
        'coverage_files':{str(p.relative_to(ROOT)):digest(p) for p in paths},
        'inputs':{str(Path(__file__).resolve().relative_to(ROOT)):source_hash},
        'physical_hardware_tested':False}
    (ROOT/'reports/instruction-codec-corpus.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS complete instruction-codec corpus:',coverage['rows_checked'],'rows,',coverage['distinct_opcode_values'],'opcode values')


if __name__=='__main__':main()
