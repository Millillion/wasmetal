#!/usr/bin/env python3
"""Verify the AXI adapter against independently scheduled channels and byte RAM."""
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
    directory=ROOT/'build/axi-memory';directory.mkdir(parents=True,exist_ok=True)
    source=ROOT/'soc/external/wasmetal_axi_memory.sv';harness=ROOT/'tests/memory/axi.cpp'
    inputs=[source,harness,Path(__file__).resolve(),ROOT/'tools/upstream.lock.json']
    hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs}
    native=directory/'native';native.mkdir(exist_ok=True)
    command=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL','--assert',
        '-DWASMETAL_ASSERTIONS','-GBASE_ADDRESS=4096','--top-module','wasmetal_axi_memory',
        '--cc','--exe','--build','-j','4','--Mdir',str(native),
        '-CFLAGS','-std=c++17 -O2 -Wall -Wextra -Werror',str(source),str(harness)]
    with (directory/'native.log').open('w') as log:
        result=subprocess.run(command,cwd=ROOT,env=dict(os.environ,
            VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),stdout=log,stderr=subprocess.STDOUT)
    if result.returncode:print((directory/'native.log').read_text()[-9000:]);result.check_returncode()
    binaries={'rtl':native/'Vwasmetal_axi_memory'}
    if args.mapped:
        netlist=directory/'axi.json'
        yosys(f'read_verilog -sv {source}\nchparam -set BASE_ADDRESS 4096 wasmetal_axi_memory\n'
              f'synth_ecp5 -top wasmetal_axi_memory -json {netlist}\ncheck -assert\n','synthesis',directory)
        netlist.with_suffix('.manifest.json').write_text(json.dumps({'inputs':hashes,'netlist_sha256':digest(netlist)},indent=2)+'\n')
        binaries['mapped']=build(netlist,directory/'mapped',top='wasmetal_axi_memory',harness=harness,cflags='')
    results={}
    for backend,binary in binaries.items():
        result=subprocess.run([str(binary)],cwd=ROOT,capture_output=True,text=True,timeout=180)
        if result.returncode:raise RuntimeError(result.stdout+result.stderr)
        negative=subprocess.run([str(binary),'--corrupt-read'],cwd=ROOT,capture_output=True,text=True,timeout=30)
        if negative.returncode==0 or 'read data differs from independent byte oracle' not in negative.stderr:
            raise RuntimeError('AXI data oracle negative control did not fail correctly')
        results[backend]=dict(json.loads(result.stdout),binary_sha256=digest(binary),negative_control_rejected=True)
    if args.mapped:
        for key in ('transactions','cycles','aw_before_w','w_before_aw','aw_with_w'):
            if results['rtl'][key]!=results['mapped'][key]:raise ValueError('RTL/mapped AXI behavior differs: '+key)
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise RuntimeError('AXI test inputs changed')
    report={'status':'passed','scope':'one outstanding 128-bit AXI4 beat; behavioral subordinate, no DDR PHY or clock crossing',
        'base_address':4096,'tests':results,'inputs':hashes,'physical_hardware_tested':False}
    if args.mapped:report['mapped_build']=json.loads(Path(str(binaries['mapped'])+'.build.json').read_text())
    (ROOT/'reports'/('axi-mapped.json' if args.mapped else 'axi.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__=='__main__':main()
