#!/usr/bin/env python3
"""Exercise CPU startup and execution without two-state initialization assumptions."""
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parent.parent


def main():
    directory=ROOT/'build/core-four-state';directory.mkdir(parents=True,exist_ok=True)
    tools=ROOT/'.cache/tools/usr';vendor=ROOT/'third_party/hardfloat/source'
    sources=sorted((ROOT/'rtl').glob('*.sv'))+sorted(vendor.glob('*.v'))
    sources += [vendor/'RISCV/HardFloat_specialize.v',ROOT/'tests/rtl/core_tb.sv']
    with (directory/'compile.log').open('w') as stream:
        subprocess.run([str(tools/'bin/iverilog'),'-B'+str(tools/'lib/x86_64-linux-gnu/ivl'),
                        '-g2012','-DWASMETAL_ASSERTIONS','-I'+str(vendor),'-I'+str(vendor/'RISCV'),
                        '-s','core_tb','-o',str(directory/'test.vvp')]+list(map(str,sources)),
                       cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,check=True)
    result=subprocess.run([str(tools/'bin/vvp'),str(directory/'test.vvp')],
                          capture_output=True,text=True,timeout=90,check=True)
    output=result.stdout+result.stderr
    (directory/'test.log').write_text(output)
    # Icarus reports a failed immediate assertion without necessarily exiting
    # nonzero. Reject those diagnostics as well as an absent success marker.
    if 'ERROR:' in output or 'FATAL:' in output or 'PASS four-state CPU execution: 8 checks' not in output:
        raise RuntimeError(output)
    print(output,end='')


if __name__=='__main__': main()
