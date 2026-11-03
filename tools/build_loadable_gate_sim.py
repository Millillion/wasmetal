#!/usr/bin/env python3
"""Build the complete programmable mapped CPU with checked primitive models."""
import json
from pathlib import Path
from build_standalone_gate_sim import build
from prepare_standalone import ROOT,digest


def main():
    netlist=ROOT/'build/loadable-mapped/design.json'
    manifest=json.loads(netlist.with_suffix('.manifest.json').read_text())
    if manifest['top']!='wasmetal_loadable' or manifest['parameters']['UART_TICKS']!=4 or manifest['parameters']['UPLOAD_TIMEOUT_CYCLES']!=4096:
        raise ValueError('wrong mapped upload test configuration')
    binary=build(netlist,ROOT/'build/loadable-gate-sim',top='wasmetal_loadable',
        harness=ROOT/'tests/standalone/loadable.cpp',cflags=' -DBIT_TICKS=4 -DCLOCK_SCALE=1 -DUPLOAD_TIMEOUT=4096')
    path=Path(str(binary)+'.build.json');identity=json.loads(path.read_text())
    identity.update(backend='loadable-mapped-ecp5-functional',profile=manifest['profile'],
        profile_tag=manifest['profile_tag'],uart_ticks=4,clock_scale=1,upload_timeout=4096)
    identity['inputs'][str(Path(__file__).resolve().relative_to(ROOT))]=digest(Path(__file__).resolve())
    path.write_text(json.dumps(identity,indent=2)+'\n')


if __name__=='__main__':main()
