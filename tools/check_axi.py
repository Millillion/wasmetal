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
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--mapped',action='store_true')
    parser.add_argument('--async',dest='asynchronous',action='store_true');args=parser.parse_args()
    prefix='async-axi' if args.asynchronous else 'axi'
    top='wasmetal_async_axi_memory' if args.asynchronous else 'wasmetal_axi_memory'
    directory=ROOT/('build/'+prefix+'-memory');directory.mkdir(parents=True,exist_ok=True)
    sources=[ROOT/'soc/external/wasmetal_axi_memory.sv'];harness=ROOT/'tests/memory/axi.cpp'
    if args.asynchronous:sources += [ROOT/'soc/external/wasmetal_memory_cdc.sv',ROOT/'soc/external/wasmetal_async_axi_memory.sv']
    cflags=' -DWASMETAL_ASYNC_AXI' if args.asynchronous else ''
    inputs=[*sources,harness,Path(__file__).resolve(),ROOT/'tools/upstream.lock.json']
    hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs}
    native=directory/'native';native.mkdir(exist_ok=True)
    command=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL','--assert',
        '-DWASMETAL_ASSERTIONS','-GBASE_ADDRESS=4096','--top-module',top,
        '--cc','--exe','--build','-j','4','--Mdir',str(native),
        '-CFLAGS','-std=c++17 -O2 -Wall -Wextra -Werror '+cflags,*map(str,sources),str(harness)]
    with (directory/'native.log').open('w') as log:
        result=subprocess.run(command,cwd=ROOT,env=dict(os.environ,
            VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),stdout=log,stderr=subprocess.STDOUT)
    if result.returncode:print((directory/'native.log').read_text()[-9000:]);result.check_returncode()
    binaries={'rtl':native/('V'+top)}
    if args.mapped:
        netlist=directory/'axi.json'
        yosys(f'read_verilog -sv {" ".join(map(str,sources))}\nchparam -set BASE_ADDRESS 4096 {top}\n'
              f'synth_ecp5 -top {top} -json {netlist}\ncheck -assert\n','synthesis',directory)
        netlist.with_suffix('.manifest.json').write_text(json.dumps({'inputs':hashes,'netlist_sha256':digest(netlist)},indent=2)+'\n')
        binaries['mapped']=build(netlist,directory/'mapped',top=top,harness=harness,cflags=cflags)
    results={}
    configurations={'axi_faster':[],'axi_slower':['--slow-axi']} if args.asynchronous else {'same_clock':[]}
    for backend,binary in binaries.items():
        tests={}
        for name,arguments in configurations.items():
            result=subprocess.run([str(binary),*arguments],cwd=ROOT,capture_output=True,text=True,timeout=180)
            if result.returncode:raise RuntimeError(result.stdout+result.stderr)
            negative=subprocess.run([str(binary),*arguments,'--corrupt-read'],cwd=ROOT,capture_output=True,text=True,timeout=30)
            if negative.returncode==0 or 'read data differs from independent byte oracle' not in negative.stderr:
                raise RuntimeError('AXI data oracle negative control did not fail correctly')
            tests[name]=dict(json.loads(result.stdout),binary_sha256=digest(binary),negative_control_rejected=True)
        results[backend]=tests if args.asynchronous else tests['same_clock']
    if args.mapped:
        for name in configurations:
            rtl=results['rtl'][name] if args.asynchronous else results['rtl']
            mapped=results['mapped'][name] if args.asynchronous else results['mapped']
            for key in ('transactions','cycles','aw_before_w','w_before_aw','aw_with_w'):
                if rtl[key]!=mapped[key]:raise ValueError('RTL/mapped AXI behavior differs: '+name+'/'+key)
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise RuntimeError('AXI test inputs changed')
    scope='one outstanding 128-bit AXI4 beat; behavioral subordinate, no DDR PHY'
    scope+='; independent clocks and common reset' if args.asynchronous else '; no clock crossing'
    report={'status':'passed','scope':scope,
        'base_address':4096,'tests':results,'inputs':hashes,'physical_hardware_tested':False}
    if args.mapped:report['mapped_build']=json.loads(Path(str(binaries['mapped'])+'.build.json').read_text())
    if args.asynchronous:report['clocks']={'axi_faster':{'source_half':7,'axi_half':3,'phase':1},'axi_slower':{'source_half':3,'axi_half':7,'phase':2}}
    (ROOT/'reports'/(prefix+('-mapped.json' if args.mapped else '.json'))).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__=='__main__':main()
