#!/usr/bin/env python3
"""Map the programmable system with the complete CPU; optionally route ULX3S."""
import argparse
import copy
import json
from pathlib import Path
import subprocess
import cad
from build_board import yosys
from build_standalone_board import audit
from prepare_standalone import ROOT,digest,load_profile
from program_upload import profile_tag
from standalone_support import generate_parameters,parameters


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--core-netlist',type=Path,default=ROOT/'build/standalone-core-ecp5.json')
    parser.add_argument('--simulation',action='store_true',help='map the core-clock top with accelerated UART/receive timeout')
    parser.add_argument('--map-only',action='store_true');parser.add_argument('--seed',type=int,default=1)
    args=parser.parse_args();profile=load_profile();generated=generate_parameters();tag=profile_tag(profile)
    top='wasmetal_loadable' if args.simulation else 'wasmetal_loadable_ulx3s'
    directory=ROOT/'build'/('loadable-mapped' if args.simulation else 'loadable-ulx3s');directory.mkdir(parents=True,exist_ok=True)
    for name in ('wasmetal.bit','manifest.json','design.manifest.json'):(directory/name).unlink(missing_ok=True)
    netlist=args.core_netlist.resolve();core_manifest_path=netlist.with_suffix('.manifest.json')
    core_manifest=json.loads(core_manifest_path.read_text())
    if digest(netlist)!=core_manifest['netlist_sha256']:raise ValueError('mapped CPU hash mismatch')
    for name,value in core_manifest['inputs'].items():
        if digest(ROOT/name)!=value:raise ValueError('stale mapped CPU: '+name)
    source=json.loads(netlist.read_text());core=source['modules']['wasmetal_core']
    layout=json.loads((ROOT/'fpga/ports.json').read_text());expected={'clk':('input',1)}
    expected.update({p['name']:(direction,p['width']) for direction,ports in layout.items() for p in ports})
    actual={name:(p['direction'],len(p['bits'])) for name,p in core['ports'].items()}
    if actual!=expected:raise ValueError('CPU ports differ from wrapper contract')
    if {name:int(value,2) for name,value in core['parameter_default_values'].items()}!=profile['core']:
        raise ValueError('mapped CPU has wrong capacities')
    if any(c['type'].startswith('$') for c in core['cells'].values()):raise ValueError('CPU is not mapped')
    stub=directory/'core_stub.v';stub.write_text('(* blackbox *) module wasmetal_core('+','.join(
        f'{direction} wire [{width-1}:0] {name}' for name,(direction,width) in expected.items())+'); endmodule\n')
    rtl=[ROOT/'fpga/wasmetal_uart.sv',ROOT/'soc/wasmetal_local_memory.sv',ROOT/'soc/wasmetal_standalone.sv',
        *sorted((ROOT/'soc/memory').glob('*.sv')),*sorted((ROOT/'soc/loader').glob('*.sv'))]
    paths=[Path(__file__).resolve(),ROOT/'tools/build_board.py',ROOT/'tools/build_standalone_board.py',
        ROOT/'tools/check_timing.py',ROOT/'tools/cad.py',ROOT/'tools/standalone_support.py',ROOT/'tools/prepare_standalone.py',
        ROOT/'tools/program_upload.py',ROOT/'tools/upstream.lock.json',ROOT/'fpga/ports.json',ROOT/'soc/profile.json',
        ROOT/'soc/loader/ulx3s.lpf',generated,stub,netlist,core_manifest_path,*rtl]
    hashes={str(p.relative_to(ROOT)):digest(p) for p in paths}
    params={'PROFILE_TAG':f"128'h{int.from_bytes(tag,'little'):032x}"}
    if args.simulation:params.update(parameters(profile),UART_TICKS=16,UPLOAD_TIMEOUT_CYCLES=4096)
    # Deferring elaboration avoids reading the legacy ROM files: this top has
    # writable, uninitialized stores and does not depend on a prepared program.
    yosys(f'read_verilog {stub}\nread_verilog -sv -defer -Ibuild -DWASMETAL_MAPPED_CORE '+
        ' '.join(map(str,rtl))+'\nchparam '+' '.join(f'-set {key} {value}' for key,value in params.items())+
        f' {top}\nsynth_ecp5 -top {top} -json {directory}/wrapper.json\ncheck -assert\n','wrapper',directory)
    wrapper=json.loads((directory/'wrapper.json').read_text());restored=copy.deepcopy(core);restored['attributes'].pop('top',None)
    wrapper['modules']['wasmetal_core']=restored
    for name,module in source['modules'].items():
        if name not in wrapper['modules']:wrapper['modules'][name]=module
    (directory/'combined.json').write_text(json.dumps(wrapper))
    yosys(f'''read_json {directory}/combined.json
read_verilog -lib -overwrite +/ecp5/cells_sim.v
hierarchy -check -top {top}
flatten
blackbox =A:whitebox
check -assert
write_json {directory}/design.json
''','flatten',directory)
    for name,value in hashes.items():
        if digest(ROOT/name)!=value:raise ValueError('mapping input changed: '+name)
    mapped={'top':top,'inputs':hashes,'profile':profile,'profile_tag':tag.hex(),
        'parameters':params,'prepared_program_embedded':False,'core_netlist_sha256':digest(netlist),
        'netlist_sha256':digest(directory/'design.json'),'physical_hardware_tested':False}
    (directory/'design.manifest.json').write_text(json.dumps(mapped,indent=2)+'\n')
    if args.simulation or args.map_only:print(directory/'design.json');return
    common=['--85k','--package','CABGA381','--speed','6','--seed',str(args.seed),'--router','router2',
        '--lpf',str(ROOT/'soc/loader/ulx3s.lpf'),'--freq','25']
    place=common+['--json',str(directory/'design.json'),'--write',str(directory/'placed.json'),'--no-route','--placer','static']
    route=common+['--json',str(directory/'placed.json'),'--write',str(directory/'routed.json'),'--no-pack','--no-place',
        '--textcfg',str(directory/'design.config'),'--report',str(directory/'timing.json')]
    for name,command in [('placement',place),('routing',route)]:
        with (directory/(name+'.log')).open('w') as log:
            subprocess.run(cad.command('nextpnr-ecp5')+command,cwd=ROOT,env=cad.environment(),stdout=log,stderr=subprocess.STDOUT,check=True)
    timing=audit(directory/'timing.json');(directory/'timing-audit.json').write_text(json.dumps(timing,indent=2)+'\n')
    pending=directory/'wasmetal.pending.bit'
    with (directory/'packing.log').open('w') as log:
        for tool,command in [('ecppack',[str(directory/'design.config'),str(pending),'--compress']),
            ('ecpunpack',[str(pending),str(directory/'unpacked.config')]),
            ('ecppack',[str(directory/'unpacked.config'),str(directory/'repacked.bit'),'--compress'])]:
            subprocess.run(cad.command(tool)+command,cwd=ROOT,env=cad.environment(),stdout=log,stderr=subprocess.STDOUT,check=True)
    if pending.read_bytes()!=(directory/'repacked.bit').read_bytes():raise ValueError('bitstream round trip failed')
    for name,value in hashes.items():
        if digest(ROOT/name)!=value:raise ValueError('build input changed: '+name)
    pending.replace(directory/'wasmetal.bit')
    receipt={**mapped,'board':'ULX3S 85F CABGA381 speed 6','seed':args.seed,
        'commands':{'placement':place,'routing':route},'timing':timing,
        'artifacts':{name:digest(directory/name) for name in
            ('design.json','placed.json','routed.json','design.config','timing.json','wasmetal.bit')},'bitstream_round_trip_passed':True}
    (directory/'manifest.json').write_text(json.dumps(receipt,indent=2)+'\n');print(directory/'wasmetal.bit')


if __name__=='__main__':main()
