#!/usr/bin/env python3
"""Test complete memory transfers under independent clocks and common reset."""
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
    directory=ROOT/'build/memory-cdc';directory.mkdir(parents=True,exist_ok=True)
    source=ROOT/'soc/external/wasmetal_memory_cdc.sv';harness=ROOT/'tests/memory/cdc.cpp'
    inputs=[source,harness,Path(__file__).resolve(),ROOT/'tools/upstream.lock.json']
    hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs}
    native=directory/'native';native.mkdir(exist_ok=True)
    command=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL','--assert',
        '-DWASMETAL_ASSERTIONS','--top-module','wasmetal_memory_cdc','--cc','--exe','--build','-j','4','--Mdir',str(native),
        '-CFLAGS','-std=c++17 -O2 -Wall -Wextra -Werror',str(source),str(harness)]
    with (directory/'native.log').open('w') as log:
        result=subprocess.run(command,cwd=ROOT,env=dict(os.environ,
            VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),stdout=log,stderr=subprocess.STDOUT)
    if result.returncode:print((directory/'native.log').read_text()[-9000:]);result.check_returncode()
    binaries={'rtl':native/'Vwasmetal_memory_cdc'}
    if args.mapped:
        netlist=directory/'cdc.json'
        yosys(f'read_verilog -sv {source}\nsynth_ecp5 -top wasmetal_memory_cdc -json {netlist}\ncheck -assert\n','synthesis',directory)
        netlist.with_suffix('.manifest.json').write_text(json.dumps({'inputs':hashes,'netlist_sha256':digest(netlist)},indent=2)+'\n')
        binaries['mapped']=build(netlist,directory/'mapped',top='wasmetal_memory_cdc',harness=harness,cflags='')
    results={}
    for backend,binary in binaries.items():
        result=subprocess.run([str(binary)],cwd=ROOT,capture_output=True,text=True,timeout=180)
        if result.returncode:raise RuntimeError(result.stdout+result.stderr)
        negative=subprocess.run([str(binary),'--corrupt-response'],cwd=ROOT,capture_output=True,text=True,timeout=30)
        if negative.returncode==0 or 'CDC response payload differs' not in negative.stderr:
            raise RuntimeError('CDC oracle negative control did not fail correctly')
        results[backend]=dict(json.loads(result.stdout),binary_sha256=digest(binary),negative_control_rejected=True)
    if args.mapped:
        for key in ('transfers','time_steps','clock_configurations','resets','paused_transfers','reset_phase_coverage'):
            if results['rtl'][key]!=results['mapped'][key]:raise ValueError('RTL/mapped CDC behavior differs: '+key)
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise RuntimeError('CDC test inputs changed')
    report={'status':'passed','scope':'digital transaction integrity under independently scheduled clocks, not metastability or physical timing signoff',
        'clock_half_periods_and_phases':[[2,3,0],[3,2,1],[5,7,3],[4,4,2],[32,1,0],[1,32,17],[1,1,0]],
        'reset_phases':['before destination capture','backend pending','response crossing','source completed'],
        'tests':results,'inputs':hashes,'physical_hardware_tested':False,'physical_cdc_constraints_verified':False}
    if args.mapped:report['mapped_build']=json.loads(Path(str(binaries['mapped'])+'.build.json').read_text())
    (ROOT/'reports'/('cdc-mapped.json' if args.mapped else 'cdc.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__=='__main__':main()
