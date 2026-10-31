#!/usr/bin/env python3
"""Independent Python bit_count oracle; exhaustive 16-bit and wide edge cases."""
from pathlib import Path
import random
import subprocess

ROOT=Path(__file__).resolve().parent.parent


def main():
    directory=ROOT/"build/unit";directory.mkdir(parents=True,exist_ok=True)
    values=list(range(1<<16));full=(1<<64)-1
    for bit in range(64):
        values.extend([1<<bit,full^(1<<bit)])
        for other in range(bit):
            pair=(1<<bit)|(1<<other);values.extend([pair,full^pair])
    rng=random.Random(0x574d2026)
    values.extend(rng.getrandbits(64) for _ in range(8192))
    with (directory/"popcount.hex").open("w") as output:
        for value in values:
            packed=value
            for index,width in enumerate((8,16,32,64)):
                packed|=(value&((1<<width)-1)).bit_count()<<(64+8*index)
            output.write(f"{packed:024x}\n")
    prefix=ROOT/".cache/tools/usr"
    subprocess.run([str(prefix/"bin/iverilog"),"-B"+str(prefix/"lib/x86_64-linux-gnu/ivl"),"-g2012",
                    "-s","popcount_tb","-o",str(directory/"popcount.vvp"),"rtl/wasmetal_popcount.sv","tests/rtl/popcount_tb.sv"],cwd=ROOT,check=True)
    subprocess.run([str(prefix/"bin/vvp"),str(directory/"popcount.vvp"),"+COUNT="+str(len(values))],cwd=ROOT,check=True,timeout=60)


if __name__=="__main__":
    main()
