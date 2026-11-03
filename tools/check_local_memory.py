#!/usr/bin/env python3
"""Build and check the actual local-memory RTL with a separate byte-array oracle."""
import json
import os
from pathlib import Path
import subprocess
from prepare_standalone import ROOT, digest


def main():
    directory=ROOT/'build/standalone-memory'; directory.mkdir(parents=True,exist_ok=True)
    fixture=ROOT/'build/standalone-memory-fixture'; fixture.mkdir(parents=True,exist_ok=True)
    entries=[(0,64),(64,16),(80,16),(0,0),(96,32),(0,0),
             (128,16),(0,0),(144,16),(0,0),(160,96),(0,0)]
    (fixture/'regions.hex').write_text(''.join(f'{base | size<<32:016x}\n' for base,size in entries))
    sources=[ROOT/'soc/wasmetal_local_memory.sv']+sorted((ROOT/'soc/memory').glob('*.sv'))
    inputs=sources+[ROOT/'tests/standalone/memory.cpp',
            Path(__file__).resolve(),fixture/'regions.hex']
    hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs}
    args=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL',
          '--assert','-DWASMETAL_ASSERTIONS','--top-module','wasmetal_local_memory',
          '-GRAM_BYTES=256','-GREGIONS_PER_KIND=2',
          '-GIMAGE_DIR="build/standalone-memory-fixture"',
          '--cc','--exe','--build','-j','4','--Mdir',str(directory),
          '-CFLAGS','-std=c++17 -O2 -Wall -Wextra -Werror']+list(map(str,sources+[ROOT/'tests/standalone/memory.cpp']))
    with (directory/'build.log').open('w') as log:
        result=subprocess.run(args,cwd=ROOT,env=dict(os.environ,
            VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),stdout=log,stderr=subprocess.STDOUT)
    if result.returncode:
        print((directory/'build.log').read_text()[-8000:]); result.check_returncode()
    binary=directory/'Vwasmetal_local_memory'
    result=subprocess.run([str(binary)],cwd=ROOT,capture_output=True,text=True,check=True)
    report=json.loads(result.stdout)
    report.update(inputs=hashes,binary_sha256=digest(binary),physical_hardware_tested=False)
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):
        raise RuntimeError('memory test inputs changed during execution')
    (ROOT/'reports').mkdir(exist_ok=True)
    (ROOT/'reports/standalone-memory.json').write_text(json.dumps(report,indent=2)+'\n')
    print(result.stdout,end='')


if __name__=='__main__': main()
