#!/usr/bin/env python3
"""Run unmodified official Wasm tests against the clocked SystemVerilog core.

Unsupported cases and tool failures make the command fail. Validation assertions
are reported separately from RTL assertions. No expected value is sent to RTL.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from wasm_image import Module, Unsupported, ImageError, Instruction, relocated

ROOT = Path(__file__).resolve().parent.parent
LOCK = json.loads((ROOT / "tools/upstream.lock.json").read_text())
SPEC = ROOT / ".cache/upstream" / ("spec-" + LOCK["spec"]["revision"])
WASM_TOOLS = Path(os.environ.get("WASM_TOOLS", str(ROOT / ".cache/tools/wasm-tools-1.263.0-x86_64-linux/wasm-tools")))
TRAPS = {1: "unreachable", 2: "integer divide by zero", 3: "integer overflow",
         4: "out of bounds memory access", 5: "out of bounds table access",
         6: "null reference", 7: "indirect call type mismatch", 8: "invalid conversion to integer",
         9: "call stack exhausted", 254: "invalid load image", 255: "unsupported instruction"}


class ExecutionError(Exception):
    pass


class LinkError(ImageError):
    pass


class Trap(Exception):
    def __init__(self, code, detail):
        self.code, self.detail = code, detail
        super().__init__(f"{TRAPS.get(code, code)} ({detail})")


def raw_value(value):
    ty, v = value["type"], value["value"]
    if ty in ("i32", "f32"):
        return int(v) & 0xffffffff
    if ty in ("i64", "f64"):
        return int(v) & 0xffffffffffffffff
    if ty == "v128":
        width = {"i8": 8, "i16": 16, "i32": 32, "i64": 64, "f32": 32, "f64": 64}[value["lane_type"]]
        return sum((int(x) & ((1 << width)-1)) << (n*width) for n, x in enumerate(v))
    if v == "null":
        return 0
    if ty in ("externref", "ref.extern"):
        return (2 << 64) | (int(v)+1)
    raise Unsupported(f"test argument {value}")


def matches(actual, expected):
    if expected["type"] == "either":
        return any(matches(actual, option) for option in expected["values"])
    if expected["type"] == "refnull":
        return actual == 0
    if "value" not in expected and expected["type"] in ("funcref", "externref", "anyref", "eqref", "structref", "arrayref", "i31ref"):
        return actual != 0
    ty, value = expected["type"], expected["value"]
    if ty == "v128":
        lane_type = expected["lane_type"]
        width = {"i8": 8, "i16": 16, "i32": 32, "i64": 64, "f32": 32, "f64": 64}[lane_type]
        for n, lane in enumerate(value):
            bits = (actual >> (n*width)) & ((1 << width)-1)
            if lane_type in ("f32", "f64"):
                if not matches(bits, {"type": lane_type, "value": lane}):
                    return False
            elif bits != int(lane) & ((1 << width)-1):
                return False
        return actual >> 128 == 0
    if ty in ("f32", "f64") and isinstance(value, str) and value.startswith("nan:"):
        bits, frac = (32, 23) if ty == "f32" else (64, 52)
        magnitude = actual & ((1 << (bits-1))-1)
        exponent = ((1 << (bits-frac-1))-1) << frac
        if value == "nan:canonical":
            return magnitude == exponent | (1 << (frac-1))
        return magnitude & exponent == exponent and bool(magnitude & (1 << (frac-1)))
    return actual == raw_value(expected)


@dataclass
class Instance:
    module: Module
    functions: list
    globals: list
    memories: list
    tables: list
    types: list
    data: list
    elements: list
    exports: dict


class RTL:
    def __init__(self, wait_states=0, max_cycles=2000000):
        self.proc = subprocess.Popen([str(ROOT / "build/obj/Vwasmetal_core")],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
        self.instructions = 0
        self.functions = 0
        self.globals = 0
        self.memories = 0
        self.tables = 0
        self.data = 0
        self.elements = 0
        self.function_types = {}
        self.global_types = {}
        self.memory_types = {}
        self.table_types = {}
        self.types = {}
        self.registered = {}
        self.max_cycles = max_cycles
        self.send(f"W {wait_states}")

    def install_spectest(self):
        path = ROOT / "build/spectest.wasm"
        if not path.exists():
            wat = '''(module
              (func (export "print"))
              (func (export "print_i32") (param i32))
              (func (export "print_i64") (param i64))
              (func (export "print_f32") (param f32))
              (func (export "print_f64") (param f64))
              (func (export "print_i32_f32") (param i32 f32))
              (func (export "print_f64_f64") (param f64 f64))
              (global (export "global_i32") i32 (i32.const 666))
              (global (export "global_i64") i64 (i64.const 666))
              (global (export "global_f32") f32 (f32.const 666.6))
              (global (export "global_f64") f64 (f64.const 666.6))
              (table (export "table") 10 20 funcref)
              (table (export "table64") i64 10 20 funcref)
              (memory (export "memory") 1 2))'''
            subprocess.run([str(WASM_TOOLS), "parse", "-o", str(path)], input=wat, text=True, check=True)
        self.registered["spectest"] = self.instantiate(Module(path.read_bytes()))

    def close(self):
        if self.proc.poll() is None:
            self.send("Q")
            self.proc.stdin.flush()
        self.proc.communicate(timeout=10)
        if self.proc.returncode:
            raise ExecutionError(f"simulator exited {self.proc.returncode}")

    def send(self, command):
        self.proc.stdin.write(command + "\n")

    def receive(self):
        self.proc.stdin.flush()
        line = self.proc.stdout.readline().strip()
        if not line:
            raise ExecutionError(f"simulator terminated: {self.proc.poll()}")
        return line.split()

    def invoke(self, function, arguments):
        for n, value in enumerate(arguments):
            self.send(f"A {n} {value:x}")
        self.send(f"R {function} {len(arguments)} {self.max_cycles}")
        result = self.receive()
        if result[0] == "TRAP":
            raise Trap(int(result[1]), f"pc={result[2]}, cycles={result[3]}")
        if result[0] != "OK":
            raise ExecutionError(" ".join(result))
        count = int(result[1])
        if len(result) != count+3:
            raise ExecutionError("malformed result")
        return [int(x, 16) for x in result[2:2+count]]

    def global_value(self, index):
        self.send(f"H {index}")
        result = self.receive()
        if result[0] != "GLOBAL":
            raise ExecutionError("malformed global response")
        return int(result[1], 16)

    def size(self, kind, index):
        self.send(f"S {kind} {index}")
        response = self.receive()
        if response[0] != "SIZE":
            raise ExecutionError("malformed size response")
        return int(response[1], 16)

    def type_id(self, ty):
        key = repr(ty)
        if key not in self.types:
            self.types[key] = len(self.types)
        return self.types[key]

    def emit(self, code, params, locals_, results, type_id, instance):
        fid = self.functions
        self.functions += 1
        self.emit_at(fid, code, params, locals_, results, type_id, instance)
        return fid

    def emit_at(self, fid, code, params, locals_, results, type_id, instance):
        base = self.instructions
        code = relocated(code, base, instance.functions, instance.globals, instance.memories, instance.tables, instance.types, instance.data, instance.elements)
        # br_table label depths live in read-only metadata after the function.
        for i in list(code):
            if i.targets:
                i.x = base + len(code)
                code.extend(Instruction(0xffff, x=t) for t in i.targets)
        self.send(f"F {fid} {base} {params} {locals_} {results} {type_id}")
        for n, i in enumerate(code):
            self.send(f"I {base+n} {i.op} {i.x} {i.y} {i.z} {i.w} {i.imm:x}")
        self.instructions += len(code)

    def init_expr(self, code, instance):
        fid = self.emit(code, 0, 0, 1, 0, instance)
        values = self.invoke(fid, [])
        if len(values) != 1:
            raise ImageError("initializer result arity")
        return values[0]

    def instantiate(self, module):
        functions, globals_, memories, tables = [], [], [], []
        for mod, name, kind, desc in module.imports:
            if mod not in self.registered or name not in self.registered[mod].exports:
                raise LinkError(f"unknown import {mod}.{name}")
            actual_kind, index = self.registered[mod].exports[name]
            if actual_kind != kind:
                raise LinkError("incompatible import kind")
            if kind == 0:
                if self.type_id(module.types[desc]) != self.function_types[index]:
                    raise LinkError("incompatible function import")
                functions.append(index)
            elif kind == 2:
                self.check_limits(desc, self.memory_types[index], self.size(0, index))
                memories.append(index)
            elif kind == 3:
                if desc != self.global_types[index]:
                    raise LinkError("incompatible global import")
                globals_.append(index)
            elif kind == 1:
                actual = self.table_types[index]
                if desc[0] != actual[0]:
                    raise LinkError("incompatible table element type")
                self.check_limits(desc[1], actual[1], self.size(1, index))
                tables.append(index)
            else:
                raise Unsupported(f"import kind {kind}")
        imported_functions = len(functions)
        for n, _ in enumerate(module.bodies):
            functions.append(self.functions)
            self.function_types[self.functions] = self.type_id(module.types[module.function_types[n]])
            self.functions += 1
        for ty, mutable, _ in module.globals:
            globals_.append(self.globals)
            self.global_types[self.globals] = (ty, mutable)
            self.globals += 1
        for minimum, maximum, wide in module.memories:
            if self.memories >= 256:
                raise Unsupported("physical memory descriptor capacity")
            memories.append(self.memories)
            if minimum > 65536:
                raise Unsupported("physical backing capacity exceeded")
            self.memory_types[self.memories] = (minimum, maximum, wide)
            self.send(f"M {self.memories} {minimum} {min(maximum if maximum is not None else 65536, 65536)} {int(wide)}")
            self.memories += 1
        for ty, (minimum, maximum, wide), _ in module.tables:
            if self.tables >= 256:
                raise Unsupported("physical table descriptor capacity")
            tables.append(self.tables)
            if minimum > 65536:
                raise Unsupported("physical table capacity exceeded")
            self.table_types[self.tables] = (ty, (minimum, maximum, wide))
            self.send(f"T {self.tables} {minimum} {min(maximum if maximum is not None else 65536, 65536)} {int(wide)}")
            self.tables += 1
        data_ids = list(range(self.data, self.data+len(module.data)))
        element_ids = list(range(self.elements, self.elements+len(module.elements)))
        self.data += len(module.data)
        self.elements += len(module.elements)
        if self.data > 256 or self.elements > 256:
            raise Unsupported("segment descriptor capacity")
        instance = Instance(module, functions, globals_, memories, tables, [self.type_id(t) for t in module.types], data_ids, element_ids, {})
        for n, (locals_, code) in enumerate(module.bodies):
            ty = module.types[module.function_types[n]]
            self.emit_at(functions[imported_functions+n], code, len(ty[0]), locals_, len(ty[1]), self.type_id(ty), instance)
        imported_globals = len(globals_) - len(module.globals)
        for n, (_, _, code) in enumerate(module.globals):
            value = self.init_expr(code, instance)
            self.send(f"G {globals_[imported_globals+n]} {value:x}")
        imported_tables = len(tables)-len(module.tables)
        for n, (_, (minimum, _, _), init) in enumerate(module.tables):
            if init is not None:
                value = self.init_expr(init, instance)
                if value:
                    for address in range(minimum):
                        self.send(f"E {tables[imported_tables+n]} {address} {value:x}")
        for n, (flags, memory, offset, data) in enumerate(module.data):
            self.send(f"D {data_ids[n]} {len(data) if flags == 1 else 0} {data.hex() or '-'}")
            if flags == 1:
                continue
            address = self.init_expr(offset, instance)
            # Admission/instantiation is host work, with runtime accesses checked in RTL.
            if memory >= len(memories) or address + len(data) > self.size(0, memories[memory])*65536:
                raise Trap(4, "data segment instantiation")
            if data:
                self.send(f"B {memories[memory]} {address} {data.hex()}")
        for n, (flags, table, offset, elements) in enumerate(module.elements):
            values = [self.init_expr(code, instance) for code in elements]
            self.send(f"L {element_ids[n]} {len(values) if flags in (1,5) else 0} {len(values)}" + ''.join(f" {v:x}" for v in values))
            if flags in (1, 3, 5, 7):
                continue
            address = self.init_expr(offset, instance)
            if table >= len(tables) or address+len(elements) > self.size(1, tables[table]):
                raise Trap(5, "element segment instantiation")
            for position, value in enumerate(values):
                self.send(f"E {tables[table]} {address+position} {value:x}")
        spaces = {0: functions, 1: tables, 2: memories, 3: globals_}
        for name, (kind, index) in module.exports.items():
            if kind not in spaces:
                raise Unsupported(f"export kind {kind}")
            instance.exports[name] = kind, spaces[kind][index]
        if module.start is not None:
            self.invoke(functions[module.start], [])
        return instance

    @staticmethod
    def check_limits(expected, actual, current_size):
        minimum, maximum, wide = expected
        _, actual_maximum, actual_wide = actual
        if wide != actual_wide or current_size < minimum or (maximum is not None and (actual_maximum is None or actual_maximum > maximum)):
            raise LinkError("incompatible import limits")


def validate(path):
    return subprocess.run([str(WASM_TOOLS), "validate", str(path)], capture_output=True, text=True)


def convert(source):
    relative = source.relative_to(SPEC / "test/core").with_suffix("")
    directory = ROOT / "build/spec" / relative
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / "test.json"
    stamp = directory / "source.sha256"
    digest = hashlib.sha256(source.read_bytes()).hexdigest() + ":" + LOCK["wasm_tools"]["version"]
    if not target.exists() or not stamp.exists() or stamp.read_text() != digest:
        proc = subprocess.run([str(WASM_TOOLS), "json-from-wast", str(source),
            "--wasm-dir", str(directory), "-o", str(target)], capture_output=True, text=True)
        if proc.returncode:
            return source, None, proc.stderr
        stamp.write_text(digest)
    return source, target, None


def run_file(source, target, args):
    counts = Counter()
    failures = []
    rtl = RTL(args.wait_states, args.max_cycles)
    rtl.install_spectest()
    current, named = None, {}
    definitions = {}
    last_definition = None
    commands = json.loads(target.read_text())["commands"]
    try:
        for command_number, command in enumerate(commands):
            kind = command["type"]
            location = f"{source.relative_to(SPEC / 'test/core')}:{command['line']}"
            try:
                if kind in ("assert_invalid", "assert_malformed"):
                    path = target.parent / command["filename"]
                    if path.suffix == ".wat":
                        parsed = subprocess.run([str(WASM_TOOLS), "parse", str(path), "-o", str(path.with_suffix('.parsed.wasm'))], capture_output=True)
                        rejected = parsed.returncode != 0
                        if not rejected:
                            rejected = validate(path.with_suffix('.parsed.wasm')).returncode != 0
                    else:
                        rejected = validate(path).returncode != 0
                    if not rejected:
                        raise ExecutionError("validator accepted expected-invalid module")
                    counts["loader_assertions_passed"] += 1
                elif kind in ("module", "module_definition"):
                    current = None
                    if "name" in command:
                        named[command["name"]] = None
                    path = target.parent / command.get("binary_filename", command["filename"])
                    checked = validate(path)
                    if checked.returncode:
                        raise ExecutionError("valid module rejected: " + checked.stderr[:250])
                    module = Module(path.read_bytes())
                    if kind == "module_definition":
                        last_definition = module
                        if "name" in command:
                            definitions[command["name"]] = module
                        counts["module_definitions"] += 1
                        continue
                    current = rtl.instantiate(module)
                    if "name" in command:
                        named[command["name"]] = current
                    counts["modules_instantiated"] += 1
                elif kind == "module_instance":
                    definition = definitions[command["module"]] if "module" in command else last_definition
                    current = rtl.instantiate(definition)
                    if "instance" in command:
                        named[command["instance"]] = current
                    counts["modules_instantiated"] += 1
                elif kind in ("assert_unlinkable", "assert_uninstantiable"):
                    path = target.parent / command.get("binary_filename", command["filename"])
                    checked = validate(path)
                    if checked.returncode:
                        raise ExecutionError("instantiation test rejected during validation")
                    try:
                        rtl.instantiate(Module(path.read_bytes()))
                    except LinkError:
                        if kind != "assert_unlinkable":
                            raise
                        counts["embedding_assertions_passed"] += 1
                    except Trap as e:
                        aliases = {5: ("undefined element",), 6: ("uninitialized element",)}
                        if kind != "assert_uninstantiable" or not (TRAPS.get(e.code) == command["text"] or command["text"] in aliases.get(e.code, ())):
                            raise
                        counts["embedding_assertions_passed"] += 1
                    else:
                        raise ExecutionError("expected linking/instantiation failure")
                elif kind == "register":
                    instance = named.get(command.get("name"), current)
                    if instance is None:
                        raise Unsupported("registration depends on failed module")
                    rtl.registered[command["as"]] = instance
                    counts["registrations"] += 1
                elif kind in ("assert_return", "assert_trap", "assert_exhaustion", "action"):
                    action = command["action"]
                    instance = named.get(action.get("module"), current)
                    if instance is None:
                        raise Unsupported("action depends on failed module")
                    export_kind, index = instance.exports[action["field"]]
                    try:
                        if action["type"] == "invoke" and export_kind == 0:
                            actual = rtl.invoke(index, [raw_value(v) for v in action["args"]])
                        elif action["type"] == "get" and export_kind == 3:
                            actual = [rtl.global_value(index)]
                        else:
                            raise Unsupported(f"action {action['type']}")
                    except Trap as e:
                        if kind == "assert_exhaustion" and e.code == 9:
                            counts["rtl_assertions_passed"] += 1
                            continue
                        expected = command.get("text", "")
                        aliases = {5: ("undefined element",), 6: ("uninitialized element", "null function reference")}
                        if kind == "assert_trap" and (TRAPS.get(e.code) == expected or expected in aliases.get(e.code, ())):
                            counts["rtl_assertions_passed"] += 1
                            continue
                        raise
                    if kind in ("assert_trap", "assert_exhaustion"):
                        raise ExecutionError("expected trap, execution returned")
                    if kind == "assert_return":
                        expected = command["expected"]
                        if len(actual) != len(expected) or not all(matches(a, e) for a, e in zip(actual, expected)):
                            raise ExecutionError(f"actual {[hex(x) for x in actual]}, expected {expected}")
                        counts["rtl_assertions_passed"] += 1
                    else:
                        counts["rtl_actions_completed"] += 1
                else:
                    raise Unsupported(f"script command {kind}")
            except Unsupported as e:
                counts["unsupported"] += 1
                failures.append({"location": location, "kind": "unsupported", "reason": str(e)})
            except (ExecutionError, ImageError, Trap, KeyError, IndexError, ValueError) as e:
                counts["failed"] += 1
                failures.append({"location": location, "kind": "failed", "reason": str(e)})
                if isinstance(e, ExecutionError) and ("TIMEOUT" in str(e) or "terminated" in str(e)):
                    counts["blocked"] += len(commands)-command_number-1
                    failures.append({"location": location, "kind": "blocked", "reason": "Remaining script commands cannot run after simulator timeout/failure"})
                    break
    finally:
        rtl.close()
    return {"suite": str(source.relative_to(SPEC / "test/core")), "counts": dict(counts), "failures": failures}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", action="append", help="exact relative suite path without .wast; repeatable")
    parser.add_argument("--wait-states", type=int, default=0)
    parser.add_argument("--max-cycles", type=int, default=2000000)
    parser.add_argument("--report", type=Path, default=ROOT / "reports/spec.json")
    args = parser.parse_args()
    sources = sorted((SPEC / "test/core").rglob("*.wast"))
    if args.suite:
        requested = set(args.suite)
        sources = [s for s in sources if str(s.relative_to(SPEC / "test/core").with_suffix("")) in requested]
        if len(sources) != len(requested):
            parser.error("unknown suite")
    if not sources:
        parser.error("official test sources are missing")
    started = time.time()
    reports = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        converted = list(pool.map(convert, sources))
    for source, target, error in converted:
        if error:
            report = {"suite": str(source.relative_to(SPEC / "test/core")), "counts": {"conversion_errors": 1},
                      "failures": [{"kind": "conversion", "reason": error}]}
        else:
            report = run_file(source, target, args)
        reports.append(report)
        print(report["suite"], json.dumps(report["counts"], sort_keys=True), flush=True)
        for failure in report["failures"][:3]:
            print(" ", failure.get("location", ""), failure["reason"], flush=True)
    totals = Counter()
    for report in reports:
        totals.update(report["counts"])
    complete = not args.suite and not any(totals[k] for k in ("failed", "unsupported", "conversion_errors", "blocked"))
    result = {"spec": LOCK["spec"], "wasm_tools": LOCK["wasm_tools"]["version"],
              "full_core_suite_selected": not bool(args.suite), "full_core_suite_passed": complete,
              "elapsed_seconds": time.time()-started, "totals": dict(totals), "suites": reports}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2)+"\n")
    print("TOTAL", json.dumps(dict(totals), sort_keys=True))
    return 1 if any(totals[k] for k in ("failed", "unsupported", "conversion_errors", "blocked")) else 0


if __name__ == "__main__":
    sys.exit(main())
