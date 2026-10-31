#!/usr/bin/env python3
"""Adversarial checks of resource boundaries and the conformance oracle."""
from pathlib import Path
import subprocess

from run_spec import ROOT, RTL, WASM_TOOLS, Module, Trap, ExecutionError, matches, trap_matches


def load(rtl, text):
    binary = subprocess.run([str(WASM_TOOLS), "parse"], input=text.encode(), capture_output=True, check=True).stdout
    return rtl.instantiate(Module(binary))


def main():
    rtl = RTL(wait_states=5)
    try:
        module = load(rtl, '''(module
          (func (export "add") (param i32 i32) (result i32) (i32.add (local.get 0) (local.get 1)))
          (func (export "trap") unreachable))''')
        result = rtl.invoke(module.exports["add"][1], [6,7])
        assert result == [13]
        assert matches(result[0], {"type":"i32", "value":"13"})
        assert not matches(result[0], {"type":"i32", "value":"14"}), "wrong expected value was accepted"
        try:
            rtl.invoke(module.exports["trap"][1], [])
            raise AssertionError("unreachable returned")
        except Trap as error:
            assert error.code == 1
            assert trap_matches(error.code, "unreachable")
            assert not trap_matches(error.code, "integer divide by zero")
        assert not trap_matches(255, "unsupported instruction")
        assert not trap_matches(254, "invalid load image")
        assert not matches(0, {"type":"f32", "value":"2147483648"}), "signed zeros were collapsed"
        assert not matches(0x7fc00001, {"type":"f32", "value":"nan:canonical"})
        assert matches(0x7fc00001, {"type":"f32", "value":"nan:arithmetic"})
        assert not matches(4 << 96, {"type":"structref"})

        # A full stack can execute a non-pushing instruction and return.
        locals_full = "(local " + "i32 "*16384 + ")"
        module = load(rtl, "(module (func (export \"full\") " + locals_full + " nop))")
        assert rtl.invoke(module.exports["full"][1], []) == []
        module = load(rtl, "(module (func (export \"overflow\") " + locals_full + " i32.const 1 drop))")
        try:
            rtl.invoke(module.exports["overflow"][1], [])
            raise AssertionError("stack overflow returned")
        except Trap as error:
            assert error.code == 9

        # Tail calls reuse the old frame even when both frames cannot coexist.
        module = load(rtl, '''(module
          (global (export "observed") (mut i32) (i32.const 0))
          (func $callee (param i32 i32) (local ''' + "i32 "*16381 + ''')
            local.get 0 global.set 0)
          (func (export "tail") (local ''' + "i32 "*16382 + ''')
            i32.const 42 i32.const 7 return_call $callee))''')
        assert rtl.invoke(module.exports["tail"][1], []) == []
        assert rtl.global_value(module.exports["observed"][1]) == 42
    finally:
        rtl.close()

    rtl = RTL(wait_states=5, max_cycles=5000)
    try:
        module = load(rtl, '''(module
          (type $array (array (mut i32)))
          (func (export "copy") (result i32)
            (local $source (ref null $array)) (local $dest (ref null $array))
            i32.const 42 i32.const 3 array.new $array local.set $source
            i32.const 0 i32.const 3 array.new $array local.set $dest
            local.get $dest i32.const 1 local.get $source i32.const 0 i32.const 1
            array.copy $array $array
            local.get $dest i32.const 1 array.get $array))''')
        assert rtl.invoke(module.exports["copy"][1], []) == [42]
    finally:
        rtl.close()

    rtl = RTL(max_cycles=40)
    try:
        module = load(rtl, '(module (func (export "spin") (loop $l br $l)))')
        try:
            rtl.invoke(module.exports["spin"][1], [])
            raise AssertionError("infinite loop returned")
        except ExecutionError as error:
            assert str(error).startswith("TIMEOUT"), "timeout became a Wasm trap"
    finally:
        rtl.close()
    print("PASS oracle negative controls, exact stack capacity, tail-frame reuse, five-operand array copying, and timeout classification")


if __name__ == "__main__":
    main()
