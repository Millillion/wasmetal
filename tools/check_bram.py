#!/usr/bin/env python3
"""Compare the production masked RAM RTL and mapped circuit with byte storage."""
import argparse
import json
import os
from pathlib import Path
import subprocess
from build_board import yosys
from build_standalone_gate_sim import build
from prepare_standalone import ROOT,digest


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--mapped',action='store_true');args=parser.parse_args()
    directory=ROOT/'build/masked-bram';directory.mkdir(parents=True,exist_ok=True)
    source=ROOT/'soc/memory/wasmetal_bram.sv';harness=ROOT/'tests/memory/bram.cpp'
    inputs=[source,harness,Path(__file__).resolve()];hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs}
    native=directory/'native';native.mkdir(exist_ok=True)
    command=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL','--assert',
        '--top-module','wasmetal_bram','--cc','--exe','--build','-j','4','--Mdir',str(native),
        '-CFLAGS','-std=c++17 -O2 -Wall -Wextra -Werror',str(source),str(harness)]
    with (directory/'native.log').open('w') as log:
        result=subprocess.run(command,cwd=ROOT,env=dict(os.environ,
            VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),stdout=log,stderr=subprocess.STDOUT)
    if result.returncode:print((directory/'native.log').read_text()[-9000:]);result.check_returncode()
    binaries={'rtl':native/'Vwasmetal_bram'}
    if args.mapped:
        netlist=directory/'memory.json'
        yosys(f'read_verilog -sv {source}\nsynth_ecp5 -top wasmetal_bram -json {netlist}\ncheck -assert\n','synthesis',directory)
        netlist.with_suffix('.manifest.json').write_text(json.dumps({'inputs':hashes,'netlist_sha256':digest(netlist)},indent=2)+'\n')
        binaries['mapped']=build(netlist,directory/'mapped',top='wasmetal_bram',harness=harness,cflags='')
    results={}
    for backend,binary in binaries.items():
        result=subprocess.run([str(binary)],cwd=ROOT,capture_output=True,text=True,timeout=180)
        if result.returncode:raise RuntimeError(result.stdout+result.stderr)
        results[backend]=dict(json.loads(result.stdout),binary_sha256=digest(binary))
    if args.mapped:
        for key in ('transactions','cycles'):assert results['rtl'][key]==results['mapped'][key],key
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise RuntimeError('BRAM test inputs changed')
    report={'status':'passed','ram_bytes':131072,'tests':results,'inputs':hashes,'physical_hardware_tested':False}
    if args.mapped:report['mapped_build']=json.loads(Path(str(binaries['mapped'])+'.build.json').read_text())
    (ROOT/'reports').mkdir(exist_ok=True)
    (ROOT/'reports'/('masked-bram-mapped.json' if args.mapped else 'masked-bram.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__':main()
