#!/usr/bin/env python3
"""Reuse the verified synthesis recipe with faster UART parameters for regression."""
import collections
import datetime
import json
from pathlib import Path
import re
import time

from build_board import yosys
from prepare_standalone import ROOT,digest
from xc7_memory_mapping import audit_address_pins,prepare


def main():
    started=time.monotonic()
    baseline_path=ROOT/'reports/xc7-system-estimate.json'
    baseline=json.loads(baseline_path.read_text())
    source_directory=ROOT/'build/xc7-system'
    source_script=source_directory/'synthesis.ys'
    if baseline['status']!='synthesized_and_structurally_checked' or digest(source_script)!=baseline['script_sha256']:
        raise ValueError('need the complete checked baseline synthesis recipe')
    for name,value in baseline['inputs'].items():
        if digest(ROOT/name)!=value:raise ValueError('baseline synthesis input changed: '+name)
    expected={'UART_TICKS':81,'UPLOAD_TIMEOUT_CYCLES':2000000}
    replacement={'UART_TICKS':4,'UPLOAD_TIMEOUT_CYCLES':4096}
    if any(baseline['parameters'][name]!=value for name,value in expected.items()):
        raise ValueError('unrecognized baseline serial parameters')
    directory=ROOT/'build/xc7-accelerated';directory.mkdir(parents=True,exist_ok=True)
    report_path=ROOT/'reports/xc7-accelerated-estimate.json';report_path.unlink(missing_ok=True)
    _,mapping=prepare(directory/'mapping-overlay')
    script=source_script.read_text()
    for name,value in replacement.items():
        original=f'-set {name} {expected[name]} '
        if script.count(original)!=1:raise ValueError('ambiguous parameter override: '+name)
        script=script.replace(original,f'-set {name} {value} ')
    script=script.replace(str(source_directory),str(directory))
    restored=script.replace(str(directory),str(source_directory))
    for name,value in replacement.items():
        restored=restored.replace(f'-set {name} {value} ',f'-set {name} {expected[name]} ')
    if restored!=source_script.read_text():raise ValueError('unexpected synthesis recipe change')
    dependencies=[Path(__file__).resolve(),baseline_path,source_script,*[ROOT/name for name in mapping['outputs']]]
    inputs={**baseline['inputs'],**{str(p.relative_to(ROOT)):digest(p) for p in dependencies}}
    yosys(script,'synthesis',directory)
    top=baseline['top']
    generic=json.loads((directory/'generic.json').read_text())['modules'][top]
    design=json.loads((directory/'mapped.json').read_text())['modules'][top]
    memories=[c for c in generic['cells'].values() if c['type']=='$mem_v2']
    memory_bits=sum(int(c['parameters']['WIDTH'],2)*int(c['parameters']['SIZE'],2) for c in memories)
    if len(memories)!=baseline['generic_memory_count'] or memory_bits!=baseline['generic_memory_bits']:
        raise ValueError('accelerated serial parameters changed storage capacity')
    counts=collections.Counter(c['type'] for c in design['cells'].values())
    if set(counts)-set(baseline['cell_counts']):raise ValueError('new primitive type needs review')
    if design['ports']!=json.loads((source_directory/'mapped.json').read_text())['modules'][top]['ports']:
        raise ValueError('accelerated variant changed the external interface')
    for name,value in inputs.items():
        if digest(ROOT/name)!=value:raise ValueError('accelerated synthesis input changed: '+name)
    result=dict(baseline)
    result.update(captured_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        variant='accelerated-uart',scope='Complete programmable core-clock simulation profile with accelerated UART and upload timeout',
        parameters={**baseline['parameters'],**replacement},inputs=inputs,
        recipe_changes_verified={'parameter_overrides':replacement,'other_commands_unchanged':True,
            'baseline_report_sha256':digest(baseline_path)},memory_mapping=mapping,
        ram_address_pin_audit=audit_address_pins(design),
        script_sha256=digest(directory/'synthesis.ys'),log_sha256=digest(directory/'synthesis.log'),
        generic_netlist_sha256=digest(directory/'generic.json'),netlist_sha256=digest(directory/'mapped.json'),
        generic_memory_count=len(memories),generic_memory_bits=memory_bits,cell_counts=dict(sorted(counts.items())),
        logic_lut_primitives=sum(counts['LUT'+str(n)] for n in range(1,7)),
        flip_flops=sum(value for kind,value in counts.items() if kind.startswith('FD')),
        ram36_equivalent=counts['RAMB36E1']+counts['RAMB18E1']/2,
        distributed_ram_primitives={k:v for k,v in sorted(counts.items()) if k.startswith('RAM') and not k.startswith('RAMB')},
        warnings=sorted(set(re.findall(r'^Warning: (.*)$',(directory/'synthesis.log').read_text(),re.M))),
        elapsed_seconds=time.monotonic()-started)
    report_path.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS accelerated UART synthesis; original recipe and storage capacity preserved')


if __name__=='__main__':main()
