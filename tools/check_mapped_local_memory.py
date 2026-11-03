#!/usr/bin/env python3
"""Compare the production-sized memory controller with an independent oracle."""
import json
import os
from pathlib import Path
import subprocess

from build_board import yosys
from build_standalone_gate_sim import build
from prepare_standalone import ROOT,digest


def main():
    directory=ROOT/'build/standalone-memory-production';directory.mkdir(parents=True,exist_ok=True)
    entries=[(16380,64),(65530,16),(131056,16),(131064,16),(70000,32),(0,0),
             (128,16),(0,0),(144,16),(0,0),(160,96),(0,0)]
    (directory/'regions.hex').write_text(''.join(f'{base|size<<32:016x}\n' for base,size in entries))
    rtl=ROOT/'soc/wasmetal_local_memory.sv';harness=ROOT/'tests/standalone/memory.cpp'
    inputs=[rtl,harness,Path(__file__).resolve(),directory/'regions.hex']
    hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs}
    image=str(directory.relative_to(ROOT))
    script=f'''read_verilog -sv {rtl}
chparam -set RAM_BYTES 131072 -set REGIONS_PER_KIND 2 -set IMAGE_DIR "{image}" wasmetal_local_memory
synth_ecp5 -top wasmetal_local_memory -json {directory}/memory.json
check -assert
'''
    yosys(script,'synthesis',directory)
    netlist=directory/'memory.json'
    manifest={'inputs':hashes,'netlist_sha256':digest(netlist)}
    netlist.with_suffix('.manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    native=directory/'native'; native.mkdir(exist_ok=True)
    args=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL','--assert',
          '-DWASMETAL_ASSERTIONS','--top-module','wasmetal_local_memory',
          '-GRAM_BYTES=131072','-GREGIONS_PER_KIND=2',f'-GIMAGE_DIR="{image}"',
          '--cc','--exe','--build','-j','4','--Mdir',str(native),'-CFLAGS',
          '-std=c++17 -O2 -Wall -Wextra -Werror -DPHYSICAL_RAM_BYTES=131072',str(rtl),str(harness)]
    with (directory/'native.log').open('w') as log:
        result=subprocess.run(args,cwd=ROOT,env=dict(os.environ,
            VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),stdout=log,stderr=subprocess.STDOUT)
        if result.returncode: log.flush();print((directory/'native.log').read_text()[-8000:]);result.check_returncode()
    mapped=build(netlist,directory/'mapped',top='wasmetal_local_memory',harness=harness,
                 cflags=' -DPHYSICAL_RAM_BYTES=131072')
    results={}
    binaries={'rtl':native/'Vwasmetal_local_memory','mapped':mapped}
    for backend,binary in binaries.items():
        result=subprocess.run([str(binary)],cwd=ROOT,capture_output=True,text=True,timeout=300)
        if result.returncode: raise RuntimeError(result.stdout+result.stderr)
        results[backend]=dict(json.loads(result.stdout),binary_sha256=digest(binary))
    if results['rtl']['transactions']!=results['mapped']['transactions']:
        raise ValueError('memory controller coverage differs between models')
    if any(digest(ROOT/name)!=value for name,value in hashes.items()): raise ValueError('memory inputs changed during tests')
    report={'status':'passed','ram_bytes':131072,'tests':results,'inputs':hashes,
            'netlist_sha256':digest(netlist),'mapped_build':json.loads(Path(str(mapped)+'.build.json').read_text()),
            'physical_hardware_tested':False}
    (ROOT/'reports/standalone-memory-mapped.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__=='__main__': main()
