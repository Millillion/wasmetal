#!/usr/bin/env python3
"""Integrate a mapped WasMetal core, route ULX3S 85F, and produce a bitstream."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess

import cad
import check_timing

ROOT=Path(__file__).resolve().parent.parent
YOSYS=ROOT/".cache/tools/usr/bin/yosys"


def yosys(script,name,directory):
    path=directory/(name+".ys");path.write_text(script)
    with (directory/(name+".log")).open("w") as output:
        subprocess.run([str(YOSYS),"-Q","-T","-s",str(path)],cwd=ROOT,stdout=output,stderr=subprocess.STDOUT,check=True)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--core-netlist",type=Path,default=ROOT/"build/core-ecp5.json")
    parser.add_argument("--seed",type=int,default=1)
    parser.add_argument("--router",choices=["router1","router2"],default="router2")
    parser.add_argument("--placer",choices=["static","heap","sa"],default="static")
    args=parser.parse_args()
    directory=ROOT/"build/ulx3s";directory.mkdir(parents=True,exist_ok=True)
    for name in ['wasmetal.bit','manifest.json']:
        (directory/name).unlink(missing_ok=True)
    source=json.loads(args.core_netlist.read_text())
    core_manifest=json.loads(args.core_netlist.with_suffix(".manifest.json").read_text())
    if hashlib.sha256(args.core_netlist.read_bytes()).hexdigest()!=core_manifest["netlist_sha256"]:
        raise ValueError("mapped core does not match its synthesis manifest")
    for name,digest in core_manifest["inputs"].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:
            raise ValueError(f"mapped core is stale: {name}")
    core=source["modules"]["wasmetal_core"]
    parameters={k:int(v,2) for k,v in core["parameter_default_values"].items()}
    for name,value in json.loads((ROOT/"fpga/profile.json").read_text()).items():
        if parameters[name]!=value:
            raise ValueError(f"mapped core {name} does not match the board profile")
    if any(cell["type"].startswith("$") for cell in core["cells"].values()):
        raise ValueError("core is not fully mapped to FPGA cells")
    subprocess.run(["python3",str(ROOT/"tools/generate_fpga_ports.py")],check=True)
    input_paths=[args.core_netlist.resolve(),args.core_netlist.with_suffix('.manifest.json').resolve(),
                 ROOT/'tools/build_board.py',ROOT/'tools/check_timing.py',ROOT/'tools/cad.py',
                 ROOT/'tools/generate_fpga_ports.py',ROOT/'tools/upstream.lock.json']+sorted((ROOT/'fpga').glob('*'))
    input_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in input_paths if p.is_file()}
    fingerprint='sha256:'+hashlib.sha256(json.dumps(input_hashes,sort_keys=True).encode()).hexdigest()
    (directory/'build-inputs.json').write_text(json.dumps({'inputs':input_hashes,'fingerprint':fingerprint},indent=2)+'\n')
    # Reuse the mapped arithmetic core. Synthesize only the transport around an
    # opaque copy, then restore and flatten the exact original mapped module.
    script=f'''read_json {args.core_netlist.resolve()}
blackbox wasmetal_core
read_verilog -sv -Ifpga -DWASMETAL_MAPPED_CORE fpga/wasmetal_uart.sv fpga/wasmetal_ulx3s.sv
synth_ecp5 -top wasmetal_ulx3s -json build/ulx3s/wrapper.json
check -assert
'''
    yosys(script,"wrapper",directory)
    wrapper=json.loads((directory/"wrapper.json").read_text())
    wrapper['modules']['wasmetal_ulx3s']['attributes']['wasmetal_input_sha256']=fingerprint
    restored=copy.deepcopy(core);restored["attributes"].pop("top",None)
    wrapper["modules"]["wasmetal_core"]=restored
    for name,module in source["modules"].items():
        if name not in wrapper["modules"]:
            wrapper["modules"][name]=module
    (directory/"combined.json").write_text(json.dumps(wrapper))
    yosys('''read_json build/ulx3s/combined.json
read_verilog -lib -overwrite +/ecp5/cells_sim.v
hierarchy -check -top wasmetal_ulx3s
flatten
blackbox =A:whitebox
check -assert
write_json build/ulx3s/design.json
''',"flatten",directory)
    args_pnr=["--85k","--package","CABGA381","--speed","6","--seed",str(args.seed),
              "--router",args.router,
              "--json",str(directory/"design.json"),"--lpf",str(ROOT/"fpga/ulx3s.lpf"),
              "--textcfg",str(directory/"design.config"),"--report",str(directory/"timing.json"),
              "--write",str(directory/'routed.json'),"--freq","25"]
    # Save placement before routing. Each stage starts from the recorded seed,
    # and the placed checkpoint makes a failed route independently reproducible.
    args_place=args_pnr.copy()
    for option in ["--textcfg","--report"]:
        index=args_place.index(option);del args_place[index:index+2]
    args_place[args_place.index("--write")+1]=str(directory/'placed.json')
    args_place += ["--no-route","--placer",args.placer]
    with (directory/"placement.log").open("w") as output:
        subprocess.run(cad.command("nextpnr-ecp5")+args_place,cwd=ROOT,env=cad.environment(),
                       stdout=output,stderr=subprocess.STDOUT,check=True)
    args_pnr[args_pnr.index("--json")+1]=str(directory/'placed.json')
    args_pnr += ["--no-pack","--no-place"]
    commands={"placement":args_place,"routing":args_pnr}
    (directory/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
    with (directory/"nextpnr.log").open("w") as output:
        subprocess.run(cad.command("nextpnr-ecp5")+args_pnr,cwd=ROOT,env=cad.environment(),
                       stdout=output,stderr=subprocess.STDOUT,check=True)
    timing=check_timing.audit(directory/'timing.json')
    (directory/'timing-audit.json').write_text(json.dumps(timing,indent=2)+'\n')
    routed=json.loads((directory/'routed.json').read_text())
    if not any(m.get('attributes',{}).get('wasmetal_input_sha256')==fingerprint for m in routed['modules'].values()):
        raise ValueError('routed design lost its source fingerprint')
    for name,digest in input_hashes.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest: raise ValueError('board input changed during build: '+name)
    with (directory/"ecppack.log").open("w") as output:
        pending=directory/'wasmetal.pending.bit'
        subprocess.run(cad.command("ecppack")+[str(directory/"design.config"),str(pending),"--compress"],
                       cwd=ROOT,env=cad.environment(),stdout=output,stderr=subprocess.STDOUT,check=True)
        subprocess.run(cad.command("ecpunpack")+[str(pending),str(directory/'unpacked.config')],
                       cwd=ROOT,env=cad.environment(),stdout=output,stderr=subprocess.STDOUT,check=True)
        subprocess.run(cad.command("ecppack")+[str(directory/'unpacked.config'),str(directory/'repacked.bit'),"--compress"],
                       cwd=ROOT,env=cad.environment(),stdout=output,stderr=subprocess.STDOUT,check=True)
    if pending.read_bytes()!=(directory/'repacked.bit').read_bytes():
        raise ValueError('bitstream did not survive unpack/repack verification')
    pending.replace(directory/'wasmetal.bit')
    versions={name:subprocess.run(command+['--version'],env=cad.environment(),capture_output=True,text=True,check=True)
              for name,command in [('yosys',[str(YOSYS)]),('nextpnr-ecp5',cad.command('nextpnr-ecp5')),('ecppack',cad.command('ecppack'))]}
    manifest={"board":"ULX3S 85F CABGA381 speed 6","parameters":parameters,"seed":args.seed,"router":args.router,
              "placer":args.placer,"commands":commands,
              "inputs":input_hashes,"fingerprint":fingerprint,'timing':timing,
              'tool_versions':{name:(result.stdout+result.stderr).strip() for name,result in versions.items()},
              'artifacts':{name:hashlib.sha256((directory/name).read_bytes()).hexdigest() for name in ['design.json','placed.json','routed.json','design.config','timing.json']},
              "bitstream_sha256":hashlib.sha256((directory/"wasmetal.bit").read_bytes()).hexdigest(),
              "bitstream_round_trip_passed":True,"physical_hardware_tested":False}
    (directory/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print("Built",directory/"wasmetal.bit")


if __name__=="__main__":
    main()
