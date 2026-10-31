#!/usr/bin/env python3
"""Exercise the board's UART framing and real core through the host adapter."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import time

import build_identity
from run_spec import ROOT, RTL, WASM_TOOLS, Module, Trap


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--simulator",type=Path,default=ROOT/"build/uart-model/Vwasmetal_ulx3s")
    parser.add_argument("--report",type=Path,default=ROOT/"reports/fpga-smoke.json")
    args=parser.parse_args()
    manifest=build_identity.verify(args.simulator)
    runner_inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in [Path(__file__).resolve(),ROOT/'tools/run_spec.py',ROOT/'tools/wasm_image.py']}
    checks=[]
    wat='''(module
      (type $box (struct (field i32)))
      (type $array (array (mut i32)))
      (tag $tag (param i32))
      (memory 1 2)
      (func (export "add") (param i32 i32) (result i32) local.get 0 local.get 1 i32.add)
      (func (export "memory") (param i32 i32) (result i32)
        local.get 0 local.get 1 i32.store local.get 0 i32.load)
      (func (export "vector") (param v128 v128) (result v128) local.get 0 local.get 1 i32x4.add)
      (func (export "divide") (param f64 f64) (result f64) local.get 0 local.get 1 f64.div)
      (func (export "object") (result i32) i32.const 42 struct.new $box struct.get $box 0)
      (func (export "arraycopy") (result i32) (local $source (ref null $array)) (local $dest (ref null $array))
        i32.const 7 i32.const 2 array.new $array local.set $source
        i32.const 0 i32.const 2 array.new $array local.set $dest
        local.get $dest i32.const 0 local.get $source i32.const 0 i32.const 2 array.copy $array $array
        local.get $dest i32.const 1 array.get $array)
      (func (export "grow") (result i32) i32.const 1 memory.grow)
      (func (export "load") (param i32) (result i32) local.get 0 i32.load)
      (func (export "exception") (result i32)
        (block (result i32) (try_table (catch $tag 0) i32.const 42 throw $tag) unreachable)))'''
    binary=subprocess.run([str(WASM_TOOLS),'parse'],input=wat.encode(),capture_output=True,check=True).stdout
    rtl=RTL(wait_states=2,simulator=args.simulator)
    started=time.monotonic()
    try:
        instance=rtl.instantiate(Module(binary))
        def run(name,arguments,expected):
            actual=rtl.invoke(instance.exports[name][1],arguments)
            assert actual==[expected],(name,actual,expected)
            checks.append(name)
            print('PASS',name,flush=True)
        run('add',[6,7],13)
        run('memory',[3,0x12345678],0x12345678)
        pack=lambda lanes:sum(x<<(32*i) for i,x in enumerate(lanes))
        run('vector',[pack([1,2,3,4]),pack([10,20,30,40])],pack([11,22,33,44]))
        bits=lambda f:struct.unpack('<Q',struct.pack('<d',f))[0]
        run('divide',[bits(6.0),bits(2.0)],bits(3.0))
        run('object',[],42)
        run('arraycopy',[],7)
        run('exception',[],42)
        try:
            rtl.invoke(instance.exports['memory'][1],[65535,7])
            raise AssertionError('out-of-bounds store returned')
        except Trap as error:
            assert error.code==4
            checks.append('bounds_trap')
        run('grow',[],1)
        run('load',[65536],0)
        rtl.send('K'); assert rtl.receive()==['CHECKSUM_OK']
        checks.extend(['corrupt_frame_no_execution','invalid_flags_no_execution','capabilities_no_execution','incomplete_frame_recovery'])
        print('PASS bounds trap, invalid/corrupt/incomplete frames, and capability queries without execution',flush=True)
    finally:
        rtl.close()
    if build_identity.verify(args.simulator)!=manifest: raise RuntimeError('simulator identity changed during test')
    for name,digest in runner_inputs.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest: raise RuntimeError('test runner changed: '+name)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps({'passed':True,'checks':checks,'elapsed_seconds':time.monotonic()-started,
                                      'build_manifest':manifest,'runner_inputs':runner_inputs},indent=2)+'\n')
    print('Board interface smoke tests passed in',round(time.monotonic()-started,2),'seconds')


if __name__=='__main__':
    main()
