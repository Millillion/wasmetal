#!/usr/bin/env python3
"""Build the serial-upload CPU; the simulator contains no prepared program ROM."""
import argparse
import json
import os
from pathlib import Path
import subprocess
from build_standalone_sim import sources
from prepare_standalone import ROOT,digest,load_profile
from program_upload import profile_tag
from standalone_support import generate_parameters,parameters


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--board',action='store_true')
    parser.add_argument('--lint',action='store_true');args=parser.parse_args()
    profile=load_profile();generated=generate_parameters();tag=profile_tag(profile)
    top='wasmetal_loadable_ulx3s' if args.board else 'wasmetal_loadable'
    directory=ROOT/'build'/('loadable-board-sim' if args.board else 'loadable-sim');directory.mkdir(parents=True,exist_ok=True)
    uart_ticks=81 if args.board else 4;timeout=2000000 if args.board else 4096;scale=32 if args.board else 1
    params={'PROFILE_TAG':f"128'h{int.from_bytes(tag,'little'):032x}"}
    if not args.board:params.update(parameters(profile),UART_TICKS=uart_ticks,UPLOAD_TIMEOUT_CYCLES=timeout)
    vendor=ROOT/'third_party/hardfloat/source';source=sources();harness=ROOT/'tests/standalone/loadable.cpp'
    inputs=[*source,*sorted(vendor.rglob('*.vi')),harness,Path(__file__).resolve(),generated,
        ROOT/'tools/build_standalone_sim.py',ROOT/'tools/prepare_standalone.py',ROOT/'tools/standalone_support.py',
        ROOT/'tools/program_upload.py',ROOT/'soc/profile.json',ROOT/'tools/upstream.lock.json']
    hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs}
    command=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL',
        '--unroll-count','512','--assert','-DWASMETAL_ASSERTIONS','--top-module',top,
        '-I'+str(vendor),'-I'+str(vendor/'RISCV'),'-I'+str(ROOT/'build'),
        *[f'-G{key}={value}' for key,value in params.items()]]
    cflags=f' -DBIT_TICKS={uart_ticks*scale} -DCLOCK_SCALE={scale} -DUPLOAD_TIMEOUT={timeout*scale}'
    if args.board:cflags+=' -DWASMETAL_BOARD'
    if args.lint:command+=['--lint-only']
    else:command+=['--cc','--exe','--build','-j','4','--Mdir',str(directory),
        '-CFLAGS','-std=c++17 -O3 -Wall -Wextra -Werror'+cflags]
    command+=list(map(str,source))
    if not args.lint:command.append(str(harness))
    with (directory/'build.log').open('w') as log:
        result=subprocess.run(command,cwd=ROOT,env=dict(os.environ,
            VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),stdout=log,stderr=subprocess.STDOUT)
    if result.returncode:print((directory/'build.log').read_text()[-10000:]);result.check_returncode()
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise RuntimeError('loadable build inputs changed')
    if not args.lint:
        binary=directory/('V'+top)
        report={'backend':'loadable-board-rtl' if args.board else 'loadable-rtl','inputs':hashes,
            'profile':profile,'profile_tag':tag.hex(),'uart_ticks':uart_ticks,'clock_scale':scale,
            'upload_timeout':timeout,'binary_sha256':digest(binary)}
        Path(str(binary)+'.build.json').write_text(json.dumps(report,indent=2)+'\n');print(binary)


if __name__=='__main__':main()
