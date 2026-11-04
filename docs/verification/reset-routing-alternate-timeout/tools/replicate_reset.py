#!/usr/bin/env python3
"""Isolate a placement experiment with equivalent local reset-LUT copies.

Every added cell must duplicate the original LUT's complete combinational
function and inputs. Substituting its output with the original output must
recover every original cell connection, port and module. State, clocks and
latency are unchanged. Physical routing improvement is a separate experiment.
"""
import argparse
from collections import Counter
import copy
import gc
import json
from pathlib import Path
import re
import subprocess

import cad
from prepare_standalone import ROOT,digest


def all_bits(module):
    values={b for p in module['ports'].values() for b in p['bits'] if isinstance(b,int)}
    values.update(b for n in module['netnames'].values() for b in n['bits'] if isinstance(b,int))
    values.update(b for c in module['cells'].values() for bits in c['connections'].values() for b in bits if isinstance(b,int))
    return values


def verify(reference,candidate,top,driver):
    if reference.keys()!=candidate.keys() or reference['modules'].keys()!=candidate['modules'].keys():
        raise ValueError('document/module set changed')
    for key,value in reference.items():
        if key!='modules' and candidate[key]!=value:raise ValueError('document metadata changed')
    for name,module in reference['modules'].items():
        if name!=top and candidate['modules'][name]!=module:raise ValueError('another module changed')
    before=reference['modules'][top];after=candidate['modules'][top];original=before['cells'][driver]
    expected={'A':'input','B':'input','C':'input','D':'input','Z':'output'}
    if original['type']!='LUT4' or original['port_directions']!=expected or set(original['parameters'])!={'INIT'}:
        raise ValueError('expected one ordinary combinational LUT4')
    init=original['parameters']['INIT']
    if len(init)!=16 or set(init)-{'0','1'} or any(len(b)!=1 for b in original['connections'].values()):
        raise ValueError('invalid LUT truth table or interface')
    output=original['connections']['Z'][0]
    if not isinstance(output,int) or any(output in original['connections'][p] for p in 'ABCD'):
        raise ValueError('invalid or self-dependent LUT output')
    if after['cells'].get(driver)!=original:raise ValueError('original reset driver changed')
    additions=set(after['cells'])-set(before['cells'])
    if not additions or set(before['cells'])-set(after['cells']):raise ValueError('missing original cells or reset copies')
    existing=all_bits(before);substitutions={};extra_nets=set(after['netnames'])-set(before['netnames'])
    expected_nets=set()
    for name in sorted(additions):
        cell=after['cells'][name]
        if cell['type']!=original['type'] or cell['parameters']!=original['parameters'] or cell['port_directions']!=expected:
            raise ValueError('copy primitive/truth table differs: '+name)
        if set(cell['connections'])!=set(expected) or any(cell['connections'][p]!=original['connections'][p] for p in 'ABCD'):
            raise ValueError('copy inputs differ: '+name)
        bits=cell['connections']['Z']
        if len(bits)!=1 or not isinstance(bits[0],int) or bits[0] in existing or bits[0] in substitutions:
            raise ValueError('copy output is not a fresh unique net')
        substitutions[bits[0]]=output
        net_name=name+'_out';expected_nets.add(net_name)
        if after['netnames'].get(net_name)!={'hide_name':0,'bits':bits,'attributes':{'noglobal':'1'}}:
            raise ValueError('unexpected copy net metadata')
        attributes={**original['attributes'],'keep':'1','wasmetal_replica_of':driver}
        if cell['attributes']!=attributes or set(cell)!=set(original):raise ValueError('unexpected copy cell metadata')
    if extra_nets!=expected_nets:raise ValueError('unexpected added net')
    for name,net in before['netnames'].items():
        if after['netnames'].get(name)!=net:raise ValueError('original net metadata changed')
    usage=Counter();original_uses=0
    for name,old in before['cells'].items():
        new=after['cells'][name]
        if old.keys()!=new.keys():raise ValueError('original cell shape changed')
        for key,value in old.items():
            if key!='connections' and new[key]!=value:raise ValueError('original cell configuration changed: '+name)
        if old['connections'].keys()!=new['connections'].keys():raise ValueError('original cell ports changed')
        for port,bits in old['connections'].items():
            observed=new['connections'][port]
            if old['port_directions'][port]=='input':
                original_uses+=bits.count(output)
                usage.update(b for b in observed if b in substitutions or b==output)
                observed=[substitutions.get(b,b) for b in observed]
            if observed!=bits:raise ValueError('original cell connection changed beyond substitution: '+name+'.'+port)
    if any(usage[b]==0 for b in substitutions) or sum(usage.values())!=original_uses:
        raise ValueError('reset sink coverage changed or a copy is unused')
    for key,value in before.items():
        if key not in ('cells','netnames') and after.get(key)!=value:raise ValueError('top interface or configuration changed')
    if before.keys()!=after.keys():raise ValueError('top shape changed')
    return {'method':'exact structural substitution of identical combinational LUT4 functions',
        'added_luts':len(additions),'original_sink_pins':original_uses,
        'distributed_sink_pins':sum(usage.values()),'maximum_resulting_fanout':max(usage.values()),
        'changed_state_primitives':0,'added_clock_cycles':0,
        'added_net_substitutions':{str(k):v for k,v in substitutions.items()}}


def partition(groups,limit):
    if sum(len(g['pins']) for g in groups)<=limit:return [groups]
    if len(groups)<2:raise ValueError('one cell exceeds the fanout limit')
    spans=[max(g['location'][axis] for g in groups)-min(g['location'][axis] for g in groups) for axis in (0,1)]
    axis=int(spans[1]>spans[0]);ordered=sorted(groups,key=lambda g:(g['location'][axis],g['location'][1-axis],g['cell']))
    middle=len(ordered)//2
    return partition(ordered[:middle],limit)+partition(ordered[middle:],limit)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory',type=Path,default=ROOT/'build/reset-replication')
    parser.add_argument('--baseline',type=Path,default=ROOT/'build/loadable-ulx3s')
    parser.add_argument('--net',default='system.execution.core_reset');parser.add_argument('--maximum-fanout',type=int,default=256)
    parser.add_argument('--place',action='store_true');parser.add_argument('--route',action='store_true')
    args=parser.parse_args()
    if not 2<=args.maximum_fanout<=1024:parser.error('invalid fanout bound')
    directory=args.directory.resolve();baseline=args.baseline.resolve()
    if directory==baseline:parser.error('experiment must not overwrite its baseline')
    directory.mkdir(parents=True,exist_ok=True);report_path=directory/'experiment.json';report_path.unlink(missing_ok=True)
    source=baseline/'design.json';placement=baseline/'placed.json';manifest_path=baseline/'design.manifest.json'
    manifest=json.loads(manifest_path.read_text());top=manifest['top']
    if top!='wasmetal_loadable_ulx3s' or digest(source)!=manifest['netlist_sha256']:raise ValueError('expected identified programmable board mapping')
    dependencies=[source,placement,manifest_path,Path(__file__).resolve(),ROOT/'tools/cad.py',ROOT/'tools/prepare_standalone.py',
        ROOT/'.cache/tools/usr/share/yosys/ecp5/cells_sim.v',cad.SUITE/'libexec/nextpnr-ecp5']
    inputs={str(p.relative_to(ROOT)):digest(p) for p in dependencies};inputs.update(manifest['inputs'])
    for name,value in inputs.items():
        if digest(ROOT/name)!=value:raise ValueError('stale experiment input: '+name)
    reference=json.loads(source.read_text());module=reference['modules'][top]
    bits=module['netnames'][args.net]['bits']
    if len(bits)!=1 or not isinstance(bits[0],int):raise ValueError('expected a scalar reset net')
    bit=bits[0];drivers=[n for n,c in module['cells'].items() for p,b in c['connections'].items() if c['port_directions'][p]=='output' and bit in b]
    if len(drivers)!=1:raise ValueError('reset must have one driver')
    driver=drivers[0];placed=json.loads(placement.read_text())['modules']['top'];sink_cells=[]
    for name,cell in module['cells'].items():
        pins=[(port,i) for port,values in cell['connections'].items() if cell['port_directions'][port]=='input'
            for i,value in enumerate(values) if value==bit]
        if not pins:continue
        match=re.match(r'X(\d+)/Y(\d+)/',placed['cells'][name]['attributes']['NEXTPNR_BEL'])
        if not match:raise ValueError('reset sink lacks an identified baseline location')
        sink_cells.append({'cell':name,'pins':pins,'location':tuple(map(int,match.groups()))})
    groups=partition(sink_cells,args.maximum_fanout)
    if len(groups)<2:raise ValueError('reset does not need replication at this fanout bound')
    candidate=copy.deepcopy(reference);new=candidate['modules'][top];next_bit=max(all_bits(module))+1;assignment=[]
    for i,group in enumerate(groups):
        name=driver if i==0 else f'wasmetal_reset_replica_{i:03}'
        target=bit
        if i:
            if name in new['cells'] or name+'_out' in new['netnames']:raise ValueError('replica name collision')
            target=next_bit;next_bit+=1;replica=copy.deepcopy(module['cells'][driver])
            replica['connections']['Z']=[target];replica['attributes'].update(keep='1',wasmetal_replica_of=driver)
            new['cells'][name]=replica;new['netnames'][name+'_out']={'hide_name':0,'bits':[target],'attributes':{'noglobal':'1'}}
        for sink in group:
            for port,index in sink['pins']:new['cells'][sink['cell']]['connections'][port][index]=target
        assignment.append({'driver':name,'output_bit':target,'sink_pins':sum(len(g['pins']) for g in group),
            'baseline_sink_bbox':[min(g['location'][0] for g in group),min(g['location'][1] for g in group),
                max(g['location'][0] for g in group),max(g['location'][1] for g in group)]})
    proof=verify(reference,candidate,top,driver);negative=[]
    copy_name=assignment[1]['driver'];copy_cell=new['cells'][copy_name]
    # Deliberate defects are checked in memory, then restored before writing the
    # candidate. Each must fail for its own specific reason.
    def reject(name,change,restore,marker):
        change()
        try:
            try:verify(reference,candidate,top,driver)
            except ValueError as error:
                if marker not in str(error):raise
                negative.append({'name':name,'rejected':True,'reason':str(error)})
            else:raise RuntimeError('structural checker accepted '+name)
        finally:restore()
    old=copy_cell['parameters']['INIT']
    reject('wrong truth table',lambda:copy_cell['parameters'].__setitem__('INIT',old[:-1]+str(1-int(old[-1]))),
        lambda:copy_cell['parameters'].__setitem__('INIT',old),'copy primitive/truth table differs')
    old_input=copy_cell['connections']['C']
    replacement=['1'] if old_input!=['1'] else ['0']
    reject('wrong LUT input',lambda:copy_cell['connections'].__setitem__('C',replacement),
        lambda:copy_cell['connections'].__setitem__('C',old_input),'copy inputs differ')
    old_output=copy_cell['connections']['Z']
    reject('aliased copy output',lambda:copy_cell['connections'].__setitem__('Z',[bit]),
        lambda:copy_cell['connections'].__setitem__('Z',old_output),'fresh unique net')
    sink=groups[1][0];port,index=sink['pins'][0];connections=new['cells'][sink['cell']]['connections'][port];saved=connections[index]
    reject('disabled sink reset',lambda:connections.__setitem__(index,'0'),lambda:connections.__setitem__(index,saved),
        'original cell connection changed beyond substitution')
    state=next(c for c in new['cells'].values() if c['type']=='TRELLIS_FF');saved=state['parameters']['REGSET']
    reject('changed register reset value',lambda:state['parameters'].__setitem__('REGSET','SET' if saved!='SET' else 'RESET'),
        lambda:state['parameters'].__setitem__('REGSET',saved),'original cell configuration changed')
    if verify(reference,candidate,top,driver)!=proof:raise ValueError('negative control did not restore the candidate')
    output=directory/'design.json';output.write_text(json.dumps(candidate))
    report={'status':'structurally_verified','scope':__doc__,'inputs':inputs,'original_net':args.net,
        'proof':proof,'negative_controls':negative,'groups':assignment,'candidate_sha256':digest(output),
        'placement_completed':False,'routing_completed':False,'physical_hardware_tested':False,
        'baseline_coordinates_only_guide_grouping':True}
    report_path.write_text(json.dumps(report,indent=2)+'\n')
    print(f'PASS reset replication by exact substitution: {proof["added_luts"]} added LUTs, '
        f'{proof["original_sink_pins"]} sinks, fanout at most {proof["maximum_resulting_fanout"]}; five rejected mutations',flush=True)
    del reference,candidate,module,new,placed;gc.collect()
    common=['--85k','--package','CABGA381','--speed','6','--seed','1','--router','router2',
        '--lpf',str(ROOT/'soc/loader/ulx3s.lpf'),'--freq','25']
    commands=[]
    if args.place or args.route:
        commands.append(('placement',common+['--json',str(output),'--write',str(directory/'placed.json'),'--no-route','--placer','static']))
    if args.route:
        commands.append(('routing',common+['--json',str(directory/'placed.json'),'--write',str(directory/'routed.json'),
            '--no-pack','--no-place','--textcfg',str(directory/'design.config'),'--report',str(directory/'timing.json'),
            '--router2-heatmap',str(directory/'congestion')]))
    for label,arguments in commands:
        with (directory/(label+'.log')).open('w') as log:
            subprocess.run(cad.command('nextpnr-ecp5')+arguments,cwd=ROOT,env=cad.environment(),stdout=log,stderr=subprocess.STDOUT,check=True)
        report[label+'_completed']=True;report.setdefault('commands',{})[label]=arguments
        report.setdefault('artifacts',{})[label]=digest(directory/('placed.json' if label=='placement' else 'routed.json'))
        report_path.write_text(json.dumps(report,indent=2)+'\n')
    for name,value in inputs.items():
        if digest(ROOT/name)!=value:raise ValueError('experiment input changed: '+name)
    if digest(output)!=report['candidate_sha256']:raise ValueError('candidate circuit changed')
    report['final_input_checks_passed']=True;report_path.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
