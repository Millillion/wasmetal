#!/usr/bin/env python3
"""Exercise the memory bridge with an independent, randomly stalled backend."""
import json
import os
from pathlib import Path
import subprocess
from prepare_standalone import ROOT,digest


def main():
    directory=ROOT/'build/memory-bridge';directory.mkdir(parents=True,exist_ok=True)
    source=ROOT/'soc/memory/wasmetal_memory_bridge.sv';harness=ROOT/'tests/memory/bridge.cpp'
    lanes=ROOT/'soc/memory/wasmetal_memory_lanes.sv'
    inputs=[source,lanes,harness,Path(__file__).resolve()]
    hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs}
    args=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL','--assert',
        '-DWASMETAL_ASSERTIONS','--top-module','wasmetal_memory_bridge','-GRAM_BYTES=256',
        '-GREGIONS_PER_KIND=2','-GTIMEOUT_CYCLES=32','--cc','--exe','--build','-j','4',
        '--Mdir',str(directory),'-CFLAGS','-std=c++17 -O2 -Wall -Wextra -Werror',str(source),str(lanes),str(harness)]
    with (directory/'build.log').open('w') as log:
        result=subprocess.run(args,cwd=ROOT,env=dict(os.environ,
            VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),stdout=log,stderr=subprocess.STDOUT)
    if result.returncode:print((directory/'build.log').read_text()[-9000:]);result.check_returncode()
    binary=directory/'Vwasmetal_memory_bridge'
    result=subprocess.run([str(binary)],cwd=ROOT,capture_output=True,text=True,timeout=120)
    if result.returncode:raise RuntimeError(result.stdout+result.stderr)
    report=json.loads(result.stdout)
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise RuntimeError('bridge inputs changed')
    report.update(inputs=hashes,binary_sha256=digest(binary),physical_hardware_tested=False,
        coverage=['all six logical spaces','every byte width and alignment','bounds and 64-bit overflow',
                  'read-only segments','0-7 backend wait cycles','request stability',
                  'backend errors on first and second beat','startup failure','timeout poisoning','reset recovery'])
    (ROOT/'reports').mkdir(exist_ok=True)
    (ROOT/'reports/memory-bridge.json').write_text(json.dumps(report,indent=2)+'\n')
    print(result.stdout,end='')


if __name__=='__main__':main()
