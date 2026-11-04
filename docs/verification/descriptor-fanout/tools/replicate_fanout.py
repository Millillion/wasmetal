#!/usr/bin/env python3
"""Try equivalent local LUT copies for selected high-fanout data/control bits."""
import argparse
import copy
import gc
import json
from pathlib import Path
import re
import subprocess
import time

import cad
from prepare_standalone import ROOT,digest
from replicate_reset import all_bits,partition,verify

CLOCK_PORTS=frozenset({'CLK','CLKA','CLKB','CLKI','WCK','CLK0','CLK1','CLK2','CLK3','ECLKI'})


def check_inputs(inputs):
    for name,sha in inputs.items():
        if digest(ROOT/name)!=sha:raise ValueError('fanout experiment input changed: '+name)


def verify_chain(reference,candidate,top,stages):
    """Reverse each exact substitution and require the original complete circuit."""
    for name,cell in reference['modules'][top]['cells'].items():
        for port,bits in cell['connections'].items():
            if port in CLOCK_PORTS and cell['port_directions'][port]=='input':
                if candidate['modules'][top]['cells'][name]['connections'][port]!=bits:
                    raise ValueError('original clock connection changed: '+name+'.'+port)
    current=candidate
    for stage in reversed(stages):
        restored=copy.deepcopy(current);module=restored['modules'][top]
        substitutions={int(k):v for k,v in stage['proof']['added_net_substitutions'].items()}
        for group in stage['groups'][1:]:
            del module['cells'][group['driver']]
            del module['netnames'][group['driver']+'_out']
        for cell in module['cells'].values():
            for port,bits in cell['connections'].items():
                if cell['port_directions'][port]=='input':
                    cell['connections'][port]=[substitutions.get(bit,bit) for bit in bits]
        proof=verify(restored,current,top,stage['driver'])
        if proof!=stage['proof']:raise ValueError('stage proof changed during reverse substitution')
        current=restored
    if current!=reference:raise ValueError('collapsed circuit differs from original baseline')
    return {'method':'reverse exact LUT substitutions followed by complete baseline equality',
            'stages':len(stages),'added_luts':sum(stage['proof']['added_luts'] for stage in stages),
            'changed_state_primitives':0,'added_clock_cycles':0,'original_clock_inputs_unchanged':True}


def add_stage(reference,top,selection,locations,limit,prefix):
    module=reference['modules'][top];name=selection['net'];index=selection['bit']
    if not isinstance(name,str) or type(index) is not int or index<0:raise ValueError('invalid net/bit selection')
    bits=module['netnames'][name]['bits']
    if index>=len(bits) or not isinstance(bits[index],int):raise ValueError('selected bit is absent or constant')
    bit=bits[index]
    drivers=[n for n,c in module['cells'].items() for p,b in c['connections'].items()
             if c['port_directions'][p]=='output' and bit in b]
    if len(drivers)!=1 or module['cells'][drivers[0]]['type']!='LUT4':raise ValueError('selected bit needs one ordinary LUT4 driver')
    driver=drivers[0];located=[];fixed=[]
    for cell_name,cell in module['cells'].items():
        pins=[];fixed_pins=[]
        for port,values in cell['connections'].items():
            if cell['port_directions'][port]!='input':continue
            for offset,value in enumerate(values):
                if value!=bit:continue
                (fixed_pins if port in CLOCK_PORTS or cell_name not in locations else pins).append((port,offset))
        if pins:located.append({'cell':cell_name,'pins':pins,'location':locations[cell_name]})
        if fixed_pins:fixed.append({'cell':cell_name,'pins':fixed_pins})
    if not located:raise ValueError('no located non-clock sinks to distribute')
    groups=([fixed] if fixed else [])+partition(located,limit)
    if len(groups)<2:raise ValueError('selected bit does not need replication')
    candidate=copy.deepcopy(reference);new=candidate['modules'][top];next_bit=max(all_bits(module))+1;assignment=[]
    for i,group in enumerate(groups):
        copy_name=driver if i==0 else f'{prefix}_{i:03}'
        target=bit
        bbox=None
        if all('location' in sink for sink in group):
            bbox=[min(s['location'][0] for s in group),min(s['location'][1] for s in group),
                  max(s['location'][0] for s in group),max(s['location'][1] for s in group)]
        if i:
            if copy_name in new['cells'] or copy_name+'_out' in new['netnames']:raise ValueError('replica name collision')
            target=next_bit;next_bit+=1;cell=copy.deepcopy(module['cells'][driver]);cell['connections']['Z']=[target]
            cell['attributes'].update(keep='1',wasmetal_replica_of=driver)
            new['cells'][copy_name]=cell;new['netnames'][copy_name+'_out']={'hide_name':0,'bits':[target],'attributes':{'noglobal':'1'}}
            # A prior-stage copy has no physical placement yet. Its group's
            # center is only a later grouping hint, never a fixed BEL.
            locations[copy_name]=((bbox[0]+bbox[2])//2,(bbox[1]+bbox[3])//2)
        for sink in group:
            for port,offset in sink['pins']:new['cells'][sink['cell']]['connections'][port][offset]=target
        assignment.append({'driver':copy_name,'output_bit':target,'sink_pins':sum(len(s['pins']) for s in group),
                           'baseline_sink_bbox':bbox})
    proof=verify(reference,candidate,top,driver)
    return candidate,{'selection':selection,'driver':driver,'original_output_bit':bit,
        'unlocated_or_clock_sink_pins_retained':sum(len(s['pins']) for s in fixed),'groups':assignment,'proof':proof}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline',type=Path,default=ROOT/'build/reset-replication')
    parser.add_argument('--directory',type=Path,default=ROOT/'build/descriptor-fanout')
    parser.add_argument('--selection',type=Path,required=True)
    parser.add_argument('--maximum-fanout',type=int,default=128)
    parser.add_argument('--place',action='store_true');args=parser.parse_args()
    if not 2<=args.maximum_fanout<=1024:parser.error('invalid grouping fanout bound')
    baseline=args.baseline.resolve();directory=args.directory.resolve();selection_path=args.selection.resolve()
    if directory==baseline:parser.error('experiment must not overwrite its baseline')
    directory.mkdir(parents=True,exist_ok=True);output=directory/'experiment.json';output.unlink(missing_ok=True)
    source=baseline/'design.json';placement=baseline/'placed.json';manifest_path=baseline/'design.manifest.json'
    manifest=json.loads(manifest_path.read_text());top=manifest['top']
    if top!='wasmetal_loadable_ulx3s' or digest(source)!=manifest['netlist_sha256']:raise ValueError('unidentified programmable baseline')
    paths=[source,placement,manifest_path,selection_path,Path(__file__).resolve(),ROOT/'tools/replicate_reset.py',
           ROOT/'tools/cad.py',ROOT/'tools/prepare_standalone.py',ROOT/'soc/loader/ulx3s.lpf',
           cad.SUITE/'libexec/nextpnr-ecp5',ROOT/'.cache/tools/usr/share/yosys/ecp5/cells_sim.v']
    inputs=dict(manifest['inputs'])
    for path in paths:
        name=str(path.relative_to(ROOT));sha=digest(path)
        if name in inputs and inputs[name]!=sha:raise ValueError('conflicting baseline input: '+name)
        inputs[name]=sha
    check_inputs(inputs);selections=json.loads(selection_path.read_text())
    if not isinstance(selections,list) or not selections:raise ValueError('nonempty selection list required')
    if any(not isinstance(s,dict) or set(s)!={'net','bit'} for s in selections):raise ValueError('selection must contain only net and bit')
    if len({(s['net'],s['bit']) for s in selections})!=len(selections):raise ValueError('duplicate selected bit')
    started=time.monotonic();reference=json.loads(source.read_text());placed=json.loads(placement.read_text())['modules']['top']
    locations={}
    for name,cell in placed['cells'].items():
        match=re.match(r'X(\d+)/Y(\d+)/',cell.get('attributes',{}).get('NEXTPNR_BEL',''))
        if match:locations[name]=tuple(map(int,match.groups()))
    del placed;candidate=reference;stages=[]
    for index,selection in enumerate(selections):
        candidate,stage=add_stage(candidate,top,selection,locations,args.maximum_fanout,f'wasmetal_fanout_replica_{index:02}')
        stages.append(stage)
        print('PASS substitution',selection,stage['proof']['original_sink_pins'],'sinks;',stage['proof']['added_luts'],'copies',flush=True)
    proof=verify_chain(reference,candidate,top,stages);controls=[];module=candidate['modules'][top]
    last=stages[-1];clone=module['cells'][last['groups'][1]['driver']]
    def reject(name,change,restore,marker=None):
        change()
        try:
            try:verify_chain(reference,candidate,top,stages)
            except ValueError as error:
                if marker and marker not in str(error):raise
                controls.append({'name':name,'reason':str(error)});print('REJECTED',name,flush=True)
            else:raise ValueError('structural proof accepted '+name)
        finally:restore()
    old=clone['parameters']['INIT']
    reject('wrong-truth-table',lambda:clone['parameters'].__setitem__('INIT',old[:-1]+str(1-int(old[-1]))),
           lambda:clone['parameters'].__setitem__('INIT',old),'copy primitive/truth table differs')
    old=clone['connections']['C'];replacement=['1'] if old!=['1'] else ['0']
    reject('wrong-copy-input',lambda:clone['connections'].__setitem__('C',replacement),
           lambda:clone['connections'].__setitem__('C',old),'copy inputs differ')
    old=clone['connections']['Z']
    reject('aliased-copy-output',lambda:clone['connections'].__setitem__('Z',[last['original_output_bit']]),
           lambda:clone['connections'].__setitem__('Z',old),'fresh unique net')
    copied_bit=old[0]
    sink=next((cell,port,i) for cell in module['cells'].values() for port,bits in cell['connections'].items()
              if cell['port_directions'][port]=='input' for i,bit in enumerate(bits) if bit==copied_bit)
    cell,port,index=sink
    reject('disconnected-sink',lambda:cell['connections'][port].__setitem__(index,'0'),
           lambda:cell['connections'][port].__setitem__(index,copied_bit),'stage proof changed')
    register=next(c for c in module['cells'].values() if c['type']=='TRELLIS_FF');old=register['parameters']['REGSET']
    reject('changed-register-reset',lambda:register['parameters'].__setitem__('REGSET','SET' if old!='SET' else 'RESET'),
           lambda:register['parameters'].__setitem__('REGSET',old),'collapsed circuit differs')
    clock_cell,clock_port=next((c,p) for c in module['cells'].values() for p in c['connections']
                              if p in CLOCK_PORTS and c['port_directions'][p]=='input')
    old=clock_cell['connections'][clock_port]
    reject('changed-clock',lambda:clock_cell['connections'].__setitem__(clock_port,[copied_bit]),
           lambda:clock_cell['connections'].__setitem__(clock_port,old),'original clock connection changed')
    saved=stages[0]
    reject('omitted-substitution-stage',lambda:stages.pop(0),lambda:stages.insert(0,saved))
    if verify_chain(reference,candidate,top,stages)!=proof:raise ValueError('fault controls did not restore the candidate')
    netlist=directory/'design.json';netlist.write_text(json.dumps(candidate))
    report={'status':'structurally_verified','scope':__doc__,'inputs':inputs,'baseline_sha256':digest(source),
            'candidate_sha256':digest(netlist),'proof':proof,'stages':stages,'negative_controls':controls,
            'negative_controls_rejected':len(controls),'requested_group_fanout':args.maximum_fanout,
            'placement_completed':False,'routing_completed':False,'timing_passed':False,
            'physical_hardware_tested':False,'default_board_build_changed':False,
            'baseline_coordinates_only_guide_grouping':True,
            'limitations':['Exact substitution preserves logical functions and clock connections, not physical delays.',
                'Unlocated sinks and clocks remain on the original driver.',
                'Later-stage copies may add loads to earlier-stage drivers; recorded per-stage fanout is not a global timing guarantee.']}
    output.write_text(json.dumps(report,indent=2)+'\n');del reference,candidate,module;gc.collect()
    try:
        if args.place:
            command=['--85k','--package','CABGA381','--speed','6','--seed','1','--router','router2',
                '--lpf',str(ROOT/'soc/loader/ulx3s.lpf'),'--freq','25','--json',str(netlist),
                '--write',str(directory/'placed.json'),'--no-route','--placer','static']
            report['placement_command']=command;output.write_text(json.dumps(report,indent=2)+'\n')
            with (directory/'placement.log').open('w') as log:
                subprocess.run(cad.command('nextpnr-ecp5')+command,cwd=ROOT,env=cad.environment(),
                               stdout=log,stderr=subprocess.STDOUT,check=True,timeout=1800)
            report['placement_completed']=True;report['placement_sha256']=digest(directory/'placed.json')
    except BaseException as error:
        report['error']=repr(error);report['status']='placement_incomplete';raise
    finally:
        check_inputs(inputs)
        if digest(netlist)!=report['candidate_sha256']:raise ValueError('fanout candidate changed')
        report['final_input_checks_passed']=True;report['elapsed_seconds']=time.monotonic()-started
        output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS fanout substitution and',len(controls),'fault controls; placement',report['placement_completed'],flush=True)


if __name__=='__main__':main()
