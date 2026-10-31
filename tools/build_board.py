#!/usr/bin/env python3
"""Integrate a mapped WasMetal core, route ULX3S 85F, and produce a bitstream."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess

import cad

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
    args=parser.parse_args()
    directory=ROOT/"build/ulx3s";directory.mkdir(parents=True,exist_ok=True)
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
              "--json",str(directory/"design.json"),"--lpf",str(ROOT/"fpga/ulx3s.lpf"),
              "--textcfg",str(directory/"design.config"),"--report",str(directory/"timing.json"),"--freq","25"]
    with (directory/"nextpnr.log").open("w") as output:
        subprocess.run(cad.command("nextpnr-ecp5")+args_pnr,cwd=ROOT,env=cad.environment(),
                       stdout=output,stderr=subprocess.STDOUT,check=True)
    with (directory/"ecppack.log").open("w") as output:
        subprocess.run(cad.command("ecppack")+[str(directory/"design.config"),str(directory/"wasmetal.bit"),"--compress"],
                       cwd=ROOT,env=cad.environment(),stdout=output,stderr=subprocess.STDOUT,check=True)
    inputs=[args.core_netlist.resolve(),ROOT/"fpga/wasmetal_uart.sv",ROOT/"fpga/wasmetal_ulx3s.sv",ROOT/"fpga/core_ports.svh",ROOT/"fpga/profile.json",ROOT/"fpga/ulx3s.lpf"]
    manifest={"board":"ULX3S 85F CABGA381 speed 6","parameters":parameters,"seed":args.seed,
              "inputs":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
              "bitstream_sha256":hashlib.sha256((directory/"wasmetal.bit").read_bytes()).hexdigest(),
              "physical_hardware_tested":False}
    (directory/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print("Built",directory/"wasmetal.bit")


if __name__=="__main__":
    main()
