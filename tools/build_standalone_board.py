#!/usr/bin/env python3
"""Map and route standalone WasMetal while retaining the complete mapped CPU."""
import argparse
import copy
import json
import math
from pathlib import Path
import subprocess

import cad
from build_board import yosys
from check_timing import clock_kind
from prepare_standalone import ROOT, digest, load_profile
from standalone_support import generate_parameters, verify_image

TOP='wasmetal_standalone_ulx3s'


def audit(path):
    report=json.loads(path.read_text())
    required={'oscillator':25.0,'core':0.78125}
    clocks={}
    for name,values in report['fmax'].items():
        kind=clock_kind(name)
        if kind not in required or kind in clocks: raise ValueError('unexpected/duplicate standalone clock')
        achieved=float(values['achieved']);constraint=float(values['constraint'])
        if not math.isfinite(achieved) or not math.isfinite(constraint) or constraint<required[kind] or achieved<constraint:
            raise ValueError(f'standalone clock failed timing: {name}')
        clocks[kind]={'net':name,'required_mhz':constraint,'achieved_mhz':achieved}
    if set(clocks)!=set(required): raise ValueError('standalone clock is unconstrained')
    paths={}
    for entry in report['critical_paths']:
        source=clock_kind(entry['from']);destination=clock_kind(entry['to'])
        if source is None or destination is None: continue
        if source!=destination: raise ValueError('unexpected standalone data clock crossing')
        edges=[entry[key].split(' ',1)[0] for key in ('from','to')]
        if any(edge not in ('posedge','negedge') for edge in edges): raise ValueError('missing timing edge')
        budget=(1000.0 if edges[0]==edges[1] else 500.0)/clocks[source]['required_mhz']
        delay=sum(float(segment['delay']) for segment in entry['path'])
        if not math.isfinite(delay) or delay<0 or delay>budget:
            raise ValueError('standalone path exceeds its full/half-cycle timing budget')
        paths[source+':'+ '->'.join(edges)]={'delay_ns':delay,'budget_ns':budget}
    if not any(name.startswith('core:') for name in paths): raise ValueError('missing core timing paths')
    for name,values in report['utilization'].items():
        if values['used']>values['available']: raise ValueError('FPGA resource overrun: '+name)
    return {'report_sha256':digest(path),'clocks':clocks,'paths':paths,
            'utilization':report['utilization'],'physical_hardware_tested':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--core-netlist',type=Path,default=ROOT/'build/standalone-core-ecp5.json')
    parser.add_argument('--wrapper-only',action='store_true',help='inspect wrapper mapping before CPU synthesis finishes')
    parser.add_argument('--map-only',action='store_true')
    parser.add_argument('--seed',type=int,default=1)
    args=parser.parse_args()
    p=load_profile(); generated=generate_parameters()
    image=ROOT/'build/standalone-image'; image_manifest=verify_image(image)
    directory=ROOT/'build'/('standalone-wrapper-check' if args.wrapper_only else 'standalone-ulx3s')
    directory.mkdir(parents=True,exist_ok=True)
    for name in ('wasmetal.bit','manifest.json','design.manifest.json'):
        (directory/name).unlink(missing_ok=True)
    layout=json.loads((ROOT/'fpga/ports.json').read_text())
    expected={'clk':('input',1)}
    expected.update({port['name']:(direction,port['width']) for direction,ports in layout.items() for port in ports})
    stub='(* blackbox *) module wasmetal_core('+','.join(
        f'{direction} wire [{width-1}:0] {name}' for name,(direction,width) in expected.items())+'); endmodule\n'
    (directory/'core_stub.v').write_text(stub)
    paths=[Path(__file__).resolve(),ROOT/'tools/build_board.py',ROOT/'tools/check_timing.py',
           ROOT/'tools/cad.py',ROOT/'tools/standalone_support.py',ROOT/'tools/prepare_standalone.py',
           ROOT/'tools/upstream.lock.json',ROOT/'fpga/ports.json',ROOT/'fpga/wasmetal_uart.sv',generated]
    paths+=sorted((ROOT/'soc').rglob('*'))+sorted(image.glob('*'))+[directory/'core_stub.v']
    source=core=None
    if not args.wrapper_only:
        netlist=args.core_netlist.resolve()
        manifest_path=netlist.with_suffix('.manifest.json')
        manifest=json.loads(manifest_path.read_text())
        if digest(netlist)!=manifest['netlist_sha256']: raise ValueError('mapped CPU hash mismatch')
        for name,value in manifest['inputs'].items():
            if digest(ROOT/name)!=value: raise ValueError('stale mapped CPU: '+name)
        source=json.loads(netlist.read_text()); core=source['modules']['wasmetal_core']
        actual={name:(port['direction'],len(port['bits'])) for name,port in core['ports'].items()}
        if actual!=expected: raise ValueError('mapped CPU ports differ from wrapper contract')
        params={name:int(value,2) for name,value in core['parameter_default_values'].items()}
        if params!=p['core']: raise ValueError('mapped CPU has wrong standalone capacities')
        if any(cell['type'].startswith('$') for cell in core['cells'].values()): raise ValueError('CPU is not mapped')
        paths+=[netlist,manifest_path]
    hashes={str(path.relative_to(ROOT)):digest(path) for path in paths if path.is_file()}
    script=f'''read_verilog {directory}/core_stub.v
read_verilog -sv -Ibuild -DWASMETAL_MAPPED_CORE fpga/wasmetal_uart.sv soc/memory/*.sv soc/wasmetal_local_memory.sv soc/wasmetal_standalone.sv soc/wasmetal_standalone_ulx3s.sv
synth_ecp5 -top {TOP} -json {directory}/wrapper.json
check -assert
'''
    yosys(script,'wrapper',directory)
    wrapper=json.loads((directory/'wrapper.json').read_text())
    if args.wrapper_only:
        print(directory/'wrapper.json'); return
    restored=copy.deepcopy(core);restored['attributes'].pop('top',None)
    wrapper['modules']['wasmetal_core']=restored
    for name,module in source['modules'].items():
        if name not in wrapper['modules']: wrapper['modules'][name]=module
    (directory/'combined.json').write_text(json.dumps(wrapper))
    yosys(f'''read_json {directory}/combined.json
read_verilog -lib -overwrite +/ecp5/cells_sim.v
hierarchy -check -top {TOP}
flatten
blackbox =A:whitebox
check -assert
write_json {directory}/design.json
''','flatten',directory)
    for name,value in hashes.items():
        if digest(ROOT/name)!=value: raise ValueError('standalone mapping input changed: '+name)
    mapped={'top':TOP,'inputs':hashes,'profile':p,'image':image_manifest,
            'core_netlist_sha256':digest(args.core_netlist),'netlist_sha256':digest(directory/'design.json')}
    (directory/'design.manifest.json').write_text(json.dumps(mapped,indent=2)+'\n')
    if args.map_only:
        print(directory/'design.json'); return
    common=['--85k','--package','CABGA381','--speed','6','--seed',str(args.seed),
            '--router','router2','--lpf',str(ROOT/'soc/ulx3s.lpf'),'--freq','25']
    place=common+['--json',str(directory/'design.json'),'--write',str(directory/'placed.json'),
                  '--no-route','--placer','static']
    route=common+['--json',str(directory/'placed.json'),'--write',str(directory/'routed.json'),
                  '--no-pack','--no-place','--textcfg',str(directory/'design.config'),
                  '--report',str(directory/'timing.json')]
    for name,command in [('placement',place),('routing',route)]:
        with (directory/(name+'.log')).open('w') as log:
            subprocess.run(cad.command('nextpnr-ecp5')+command,cwd=ROOT,env=cad.environment(),
                           stdout=log,stderr=subprocess.STDOUT,check=True)
    timing=audit(directory/'timing.json')
    (directory/'timing-audit.json').write_text(json.dumps(timing,indent=2)+'\n')
    for name,value in hashes.items():
        if digest(ROOT/name)!=value: raise ValueError('standalone build input changed: '+name)
    pending=directory/'wasmetal.pending.bit'
    with (directory/'packing.log').open('w') as log:
        for tool,command in [('ecppack',[str(directory/'design.config'),str(pending),'--compress']),
                             ('ecpunpack',[str(pending),str(directory/'unpacked.config')]),
                             ('ecppack',[str(directory/'unpacked.config'),str(directory/'repacked.bit'),'--compress'])]:
            subprocess.run(cad.command(tool)+command,cwd=ROOT,env=cad.environment(),
                           stdout=log,stderr=subprocess.STDOUT,check=True)
    if pending.read_bytes()!=(directory/'repacked.bit').read_bytes(): raise ValueError('bitstream round trip failed')
    pending.replace(directory/'wasmetal.bit')
    receipt={**mapped,'board':'ULX3S 85F CABGA381 speed 6','seed':args.seed,
             'commands':{'placement':place,'routing':route},'timing':timing,
             'artifacts':{name:digest(directory/name) for name in
                 ('design.json','placed.json','routed.json','design.config','timing.json','wasmetal.bit')},
             'bitstream_round_trip_passed':True,'physical_hardware_tested':False}
    (directory/'manifest.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(directory/'wasmetal.bit')


if __name__=='__main__': main()
