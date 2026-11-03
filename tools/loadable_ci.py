#!/usr/bin/env python3
"""Share the programmable circuit and require every integration case to match RTL."""
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys
import tarfile

from check_standalone import cases
from check_loadable import extra_cases
from prepare_standalone import ROOT,digest
from standalone_support import verify_simulator


GROUPS=[
    ['answer','selftest'],
    ['arguments','memory64','unaligned-simd','subtype-cast','tail-reference'],
    ['branches','sixteen-results','no-results','unreachable','divide-zero'],
    ['memory-oob','memory64-wrap','table-oob','null-call','bad-cast'],
    ['uncaught','heap-exhaustion','watchdog'],
    ['program-address-boundaries','type-address-boundaries','type-boundary-rejection',
     'boot-address-boundaries','segment-address-boundaries']]
RECOVERY=['profile-rejection','crc-rejection','partial-reset','receive-timeout','break-abort',
          'recovery-upload','serial-period-980','serial-period-1020','reset-during-execution','reset-during-result']


def check_plan():
    expected=[c['name'] for c in cases() if not any(k in c for k in ('reset_at','reset_phase','corrupt'))]
    expected += [c['name'] for c in extra_cases()]
    assigned=[name for group in GROUPS for name in group]
    if len(assigned)!=len(set(assigned)) or set(assigned)!=set(expected):
        raise ValueError('programmable integration ownership is incomplete or duplicated')


def compare(reference,shards):
    check_plan()
    if reference['status']!='passed' or reference['model']['backend']!='loadable-rtl':
        raise ValueError('complete native programmable reference required')
    expected={case['name']:case for case in reference['cases']}
    names={name for group in GROUPS for name in group}|set(RECOVERY)
    if len(reference['cases'])!=len(names) or set(expected)!=names:
        raise ValueError('native reference has incomplete integration coverage')
    observed={};netlist=None;groups=set()
    for report in shards:
        if report['status']!='passed' or report['model']['backend']!='loadable-mapped-ecp5-functional':
            raise ValueError('passed mapped circuit report required')
        identity=report['model']
        for field in ('profile','profile_tag','uart_ticks','clock_scale','upload_timeout'):
            if identity[field]!=reference['model'][field]:raise ValueError('different circuit configuration: '+field)
        if report['inputs']!=reference['inputs']:raise ValueError('different integration checker inputs')
        if not identity.get('netlist_sha256'):raise ValueError('missing circuit identity')
        if netlist is not None and netlist!=identity['netlist_sha256']:raise ValueError('different mapped circuits')
        netlist=identity['netlist_sha256']
        actual=[case['name'] for case in report['cases']]
        candidates=[n for n,group in enumerate(GROUPS) if actual==group+(RECOVERY if n==0 else [])]
        if len(candidates)!=1 or candidates[0] in groups:raise ValueError('missing, duplicate or reordered shard cases')
        groups.add(candidates[0])
        for case in report['cases']:
            name=case['name']
            if name in observed:raise ValueError('duplicate integration case')
            if case!=expected[name]:raise ValueError('UART bytes, cycles or results differ: '+name)
            observed[name]=case
    if groups!=set(range(len(GROUPS))) or set(observed)!=names:
        raise ValueError('incomplete mapped integration coverage')
    return netlist,observed


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='action',required=True)
    sub.add_parser('plan')
    pack=sub.add_parser('pack');pack.add_argument('--output',type=Path,default=ROOT/'reports/loadable-simulator.tar.gz')
    run=sub.add_parser('run');run.add_argument('--shard',type=int,choices=range(len(GROUPS)),required=True)
    merge=sub.add_parser('merge');merge.add_argument('--reference',type=Path,default=ROOT/'reports/loadable-rtl.json')
    merge.add_argument('--reports',type=Path,default=ROOT/'reports');merge.add_argument('--output',type=Path,default=ROOT/'reports/loadable-mapped.json')
    args=parser.parse_args();check_plan()
    binary=ROOT/'build/loadable-gate-sim/obj/Vwasmetal_loadable'
    if args.action=='plan':print(json.dumps({'shard':list(range(len(GROUPS)))}));return
    if args.action=='run':
        command=[sys.executable,str(ROOT/'tools/check_loadable.py'),'--binary',str(binary),
                 '--report',str(ROOT/f'reports/loadable-mapped-{args.shard}.json')]
        for name in GROUPS[args.shard]:command+=['--case',name]
        if args.shard:command+=['--no-recovery']
        subprocess.run(command,cwd=ROOT,check=True);return
    if args.action=='pack':
        identity=verify_simulator(binary)
        if identity['backend']!='loadable-mapped-ecp5-functional' or not identity['compilation']['portable']:
            raise ValueError('portable programmable circuit required')
        paths={binary,Path(str(binary)+'.build.json')}
        paths.update(ROOT/name for name in identity['inputs'] if name.startswith('build/'))
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with tarfile.open(args.output,'w:gz') as archive:
            for path in sorted(paths):archive.add(path,arcname=str(path.resolve().relative_to(ROOT)),recursive=False)
        verify_simulator(binary);print(args.output);return
    reference=json.loads(args.reference.read_text())
    paths=sorted(args.reports.rglob('loadable-mapped-[0-9].json'))
    reports=[json.loads(path.read_text()) for path in paths]
    netlist,observed=compare(reference,reports)
    for report in [reference,*reports]:
        for name,value in report['inputs'].items():
            if digest(ROOT/name)!=value:raise ValueError('stale integration checker: '+name)
        # Workers check generated artifacts and executable identities before
        # and after execution. Recheck source/tool inputs in the merge job too.
        for name,value in report['model']['inputs'].items():
            path=Path(name)
            if path.is_absolute() or '..' in path.parts:raise ValueError('unsafe model input path')
            if not name.startswith('build/') and digest(ROOT/path)!=value:
                raise ValueError('stale programmable model source: '+name)
    rejected=[]
    for name in ('missing-shard','duplicate-shard','native-substitution','wrong-result','wrong-clock','wrong-netlist'):
        broken=copy.deepcopy(reports)
        if name=='missing-shard':broken.pop()
        elif name=='duplicate-shard':broken.append(copy.deepcopy(broken[0]))
        elif name=='native-substitution':broken[0]['model']['backend']='loadable-rtl'
        elif name=='wrong-result':broken[0]['cases'][0]['result']['values'][0]^=1
        elif name=='wrong-clock':broken[0]['cases'][0]['uart']['clocks']+=1
        else:broken[0]['model']['netlist_sha256']='0'*64
        try:compare(reference,broken)
        except ValueError:rejected.append(name)
        else:raise ValueError('integration merge accepted '+name)
    output={'status':'passed','scope':'all programmable integration cases; not the official host-backed corpus',
        'netlist_sha256':netlist,'case_count':len(observed),'uart_and_cycles_identical':True,
        'cases':[observed[name] for name in sorted(observed)],'negative_controls_rejected':rejected,
        'reports':{str(path.resolve().relative_to(ROOT)):digest(path) for path in [args.reference,*paths]},
        'inputs':{str(Path(__file__).resolve().relative_to(ROOT)):digest(Path(__file__).resolve())},
        'physical_hardware_tested':False}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(output,indent=2)+'\n');print(args.output)


if __name__=='__main__':main()
