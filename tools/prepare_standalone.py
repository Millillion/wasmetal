#!/usr/bin/env python3
"""Validate Wasm and prepare bounded ROMs; execution stays in the existing RTL.

The preparation simulator evaluates instantiation, not the requested export.
Its initialization commands are replayed by the hardware boot sequencer.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

import build_identity
from run_spec import RTL, validate, WASM_TOOLS
from wasm_image import Module

ROOT = Path(__file__).resolve().parent.parent
MAGIC = 0x574d5301
ROM_WIDTHS = {"code": 288, "functions": 160, "types": None,
              "regions": 64, "boot": 232}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def profile_path():
    """The selected capacity profile; WASMETAL_PROFILE overrides the default."""
    selected = os.environ.get('WASMETAL_PROFILE')
    return (ROOT / selected).resolve() if selected else ROOT / "soc/profile.json"


def load_profile(path=None):
    p = json.loads((path or profile_path()).read_text())
    expected = {"core", "instruction_depth", "function_depth", "type_depth",
                "boot_depth", "regions_per_kind", "ram_bytes", "memory_pages",
                "table_slots", "max_results", "watchdog_cycles"}
    if set(p) != expected or any(type(v) is not int or v < 1 or v >= 1 << 30
                                for k, v in p.items() if k != "core"):
        raise ValueError("invalid standalone profile")
    if set(p['core']) != {'VALUE_DEPTH', 'CONTROL_DEPTH', 'CALL_DEPTH', 'MEMORY_COUNT', 'HEAP_SLOTS'} or any(
            type(v) is not int or not 1 <= v < 1 << 30 for v in p['core'].values()):
        raise ValueError("invalid standalone core profile")
    if p['regions_per_kind'] > p['core']['MEMORY_COUNT']:
        raise ValueError("local regions exceed core descriptor capacity")
    if p['max_results'] > 255 or p['type_depth'] > 256:
        raise ValueError("result/type profile exceeds image protocol")
    for name in ('ram_bytes', 'instruction_depth', 'function_depth', 'type_depth',
                 'boot_depth', 'regions_per_kind'):
        if p[name] & (p[name] - 1):
            raise ValueError(f"{name} must be a power of two")
    return p


def record(mode, kind=0, index=0, data=0, aux=0):
    fields = ((mode, 4), (kind, 4), (index, 32), (data, 128), (aux, 64))
    if any(type(v) is not int or not 0 <= v < 1 << bits for v, bits in fields):
        raise ValueError("boot record field out of range")
    return data | aux << 128 | index << 192 | kind << 224 | mode << 228


class Recorder(RTL):
    def __init__(self, profile, **kwargs):
        self.profile = profile
        self.trace = []
        super().__init__(**kwargs)

    def send(self, command):
        fields = command.split()
        if fields[0] in ('M', 'T'):
            maximum = self.profile['memory_pages' if fields[0] == 'M' else 'table_slots']
            if int(fields[2]) > maximum:
                raise ValueError(f"{fields[0]} initial size exceeds standalone capacity")
            fields[3] = str(min(int(fields[3]), maximum))
            command = ' '.join(fields)
        self.trace.append(command)
        super().send(command)


def pack_trace(trace, profile, session=False):
    """Pack actual loader commands, with explicit physical regions and no pruning.

    A session image reports every execution and global/size query, in order.
    It then also returns, for each reporting boot record, its trace line.
    """
    p = profile
    code, functions, relations, regions = {}, {}, set(), {}
    cursor = 0

    def allocate(kind, index, size):
        nonlocal cursor
        if not 0 <= index < p['regions_per_kind'] or size < 0 or size >= 1 << 32:
            raise ValueError("local memory region index/size exceeds profile")
        if (kind, index) in regions:
            raise ValueError("duplicate region initialization")
        cursor = (cursor + 15) & ~15
        regions[kind, index] = (cursor, size)
        cursor += size
        if cursor > p['ram_bytes']:
            raise ValueError("prepared module exceeds local RAM capacity")

    allocate(5, 0, p['core']['HEAP_SLOTS'] * 16)
    lines = [line.split() for line in trace]
    for f in lines:
        op = f[0]
        if op in ('M', 'T'):
            minimum, maximum = map(int, f[2:4])
            limit = p['memory_pages' if op == 'M' else 'table_slots']
            if not 0 <= minimum <= maximum <= limit:
                raise ValueError("descriptor size exceeds physical capacity")
            allocate(0 if op == 'M' else 2, int(f[1]), maximum * (65536 if op == 'M' else 16))
        elif op == 'G':
            allocate(1, int(f[1]), 16)
        elif op == 'D':
            data = b'' if f[3] == '-' else bytes.fromhex(f[3])
            if int(f[2]) not in (0, len(data)):
                raise ValueError("data descriptor differs from segment")
            allocate(3, int(f[1]), len(data))
        elif op == 'L':
            count = int(f[3])
            if count != len(f[4:]) or int(f[2]) not in (0, count):
                raise ValueError("element descriptor differs from segment")
            allocate(4, int(f[1]), count * 16)

    boot = [0]  # Header is filled after the exact command count is known.

    def initialize(kind, index, offset, data):
        if (kind, index) not in regions:
            raise ValueError("initializer refers to an absent memory region")
        base, size = regions[kind, index]
        if offset < 0 or offset > size or len(data) > size - offset:
            raise ValueError("initializer exceeds local region")
        for start in range(0, len(data), 16):
            chunk = data[start:start + 16]
            boot.append(record(2, index=base + offset + start,
                               data=int.from_bytes(chunk, 'little'), aux=len(chunk)))

    final_seen = False
    reports = []
    for line_number, f in enumerate(lines):
        op = f[0]
        if final_seen:
            raise ValueError("commands after exported invocation")
        if op == 'I':
            index = int(f[1])
            values = [int(x) for x in f[2:7]]
            if any(not -(1 << 31) <= x < 1 << 32 for x in values):
                raise ValueError("instruction field out of range")
            if index in code or not 0 <= index < p['instruction_depth']:
                raise ValueError("instruction image exceeds profile or repeats an address")
            immediate = int(f[7], 16)
            if not 0 <= immediate < 1 << 128:
                raise ValueError("immediate exceeds 128 bits")
            code[index] = sum((x & 0xffffffff) << (32 * n) for n, x in enumerate(values)) | immediate << 160
        elif op == 'F':
            index = int(f[1]); values = list(map(int, f[2:7]))
            if index in functions or not 0 <= index < p['function_depth']:
                raise ValueError("function image exceeds profile or repeats an index")
            if any(not 0 <= v < 1 << 32 for v in values) or values[4] >= p['type_depth']:
                raise ValueError("function metadata exceeds profile")
            if values[1] + values[2] > p['core']['VALUE_DEPTH'] or values[3] > p['max_results']:
                raise ValueError("function values/results exceed profile")
            functions[index] = sum(x << (32 * n) for n, x in enumerate(values))
        elif op == 'Y':
            pair = tuple(map(int, f[1:3]))
            if any(not 0 <= x < p['type_depth'] for x in pair):
                raise ValueError("type metadata exceeds profile")
            relations.add(pair)
        elif op in ('M', 'T'):
            boot.append(record(1, 2 if op == 'M' else 3, int(f[1]),
                               int(f[2]) | int(f[3]) << 64, int(f[4])))
        elif op == 'A':
            if not 0 <= int(f[1]) < p['core']['VALUE_DEPTH']:
                raise ValueError("argument exceeds value capacity")
            boot.append(record(1, 1, int(f[1]), int(f[2], 16)))
        elif op in ('R', 'Z') and session:
            if op == 'Z':
                raise ValueError("session images report every execution")
            reports.append((len(boot), line_number))
            boot.append(record(4, index=int(f[1]), aux=int(f[2])))
        elif op in ('H', 'S') and session:
            if op == 'H' and not 0 <= int(f[1]) < p['regions_per_kind']:
                raise ValueError("global query exceeds profile")
            reports.append((len(boot), line_number))
            boot.append(record(5, 8 if op == 'H' else 6 + int(f[1]), int(f[-1])))
        elif op in ('R', 'Z'):
            boot.append(record(3 if op == 'Z' else 1, index=int(f[1]), aux=int(f[2])))
            final_seen = op == 'Z'
        elif op == 'G':
            initialize(1, int(f[1]), 0, int(f[2], 16).to_bytes(16, 'little'))
        elif op == 'E':
            initialize(2, int(f[1]), int(f[2]) * 16, int(f[3], 16).to_bytes(16, 'little'))
        elif op == 'B':
            initialize(0, int(f[1]), int(f[2]), bytes.fromhex(f[3]))
        elif op == 'D':
            initialize(3, int(f[1]), 0, b'' if f[3] == '-' else bytes.fromhex(f[3]))
            boot.append(record(1, 4, int(f[1]), int(f[2])))
        elif op == 'L':
            initialize(4, int(f[1]), 0, b''.join(int(x, 16).to_bytes(16, 'little') for x in f[4:]))
            boot.append(record(1, 5, int(f[1]), int(f[2])))
        elif op not in ('V', 'W', 'S', 'H', 'Q'):
            raise ValueError(f"unsupported image command: {op}")
    if (final_seen == session) or not code or not functions or (session and not reports):
        raise ValueError("image needs code, functions and one exported invocation or reported session")
    if set(code) != set(range(len(code))) or set(functions) != set(range(len(functions))):
        raise ValueError("image contains holes")
    for value in functions.values():
        if (value & 0xffffffff) >= len(code):
            raise ValueError("function entry lies outside instruction image")
    for value in boot:
        mode, kind = value >> 228, (value >> 224) & 15
        if mode in (1, 3, 4) and kind == 0:
            index, argc = (value >> 192) & 0xffffffff, (value >> 128) & ((1 << 64) - 1)
            if index not in functions or argc != ((functions[index] >> 32) & 0xffffffff):
                raise ValueError("invocation has invalid function or argument count")
    boot.append(record(0))
    if len(boot) > p['boot_depth']:
        raise ValueError("boot image exceeds profile")
    boot[0] = record(15, data=MAGIC | len(code) << 32 | len(functions) << 64 | len(boot) << 96)
    types = [sum(1 << expected for actual, expected in relations if actual == row)
             for row in range(p['type_depth'])]
    region_words = [0] * (6 * p['regions_per_kind'])
    for (kind, index), (base, size) in regions.items():
        region_words[kind * p['regions_per_kind'] + index] = base | size << 32
    roms = {'code': [code[n] for n in range(len(code))], 'functions': [functions[n] for n in range(len(functions))],
            'types': types, 'regions': region_words, 'boot': boot}
    counts = {name: len(values) for name, values in roms.items()}
    depths = {'code': p['instruction_depth'], 'functions': p['function_depth'],
              'types': p['type_depth'], 'regions': 6 * p['regions_per_kind'], 'boot': p['boot_depth']}
    roms = {name: values + [0] * (depths[name] - len(values)) for name, values in roms.items()}
    summary = {'counts': counts, 'allocated_ram_bytes': cursor,
               'regions': [{'kind': k, 'index': i, 'base': b, 'bytes': s}
                           for (k, i), (b, s) in sorted(regions.items())]}
    if session:
        summary['reports'] = [{'boot_record': b, 'trace_line': n} for b, n in reports]
    return roms, summary


def prepare(source, output, export='main', arguments=(), profile=None, simulator=None):
    p = profile or load_profile()
    output.mkdir(parents=True, exist_ok=True)
    (output / 'manifest.json').unlink(missing_ok=True)
    binary = simulator or ROOT / 'build/obj/Vwasmetal_core'
    identity = build_identity.verify(binary)
    wasm = output / 'program.wasm'
    if source.suffix == '.wat':
        subprocess.run([str(WASM_TOOLS), 'parse', str(source), '-o', str(wasm)], check=True)
    else:
        wasm.write_bytes(source.read_bytes())
    if validate(wasm).returncode != 0:
        raise ValueError("Wasm module failed validation")
    module = Module(wasm.read_bytes())
    if module.imports:
        raise ValueError("standalone image requires a module without imports")
    rtl = Recorder(p, simulator=binary)
    try:
        instance = rtl.instantiate(module)
        kind, fid = instance.exports[export]
        if kind != 0:
            raise ValueError("requested export is not a function")
        params = rtl.type_info[rtl.function_types[fid]].params
        widths = {0x7f: 32, 0x7e: 64, 0x7d: 32, 0x7c: 64, 0x7b: 128}
        if len(params) != len(arguments):
            raise ValueError("wrong number of exported function arguments")
        for ty, value in zip(params, arguments):
            if ty not in widths or not 0 <= value < 1 << widths[ty]:
                raise ValueError("arguments must be numeric/SIMD raw bits of the correct width")
        trace = rtl.trace.copy()
        trace.extend(f'A {n} {v:x}' for n, v in enumerate(arguments))
        trace.append(f'Z {fid} {len(arguments)}')
        roms, summary = pack_trace(trace, p)
    finally:
        rtl.close()
    files = {}
    for name, values in roms.items():
        width = ROM_WIDTHS[name] or p['type_depth']
        path = output / (name + '.hex')
        path.write_text(''.join(f'{v:0{(width+3)//4}x}\n' for v in values))
        files[path.name] = digest(path)
    (output / 'initialization.txt').write_text('\n'.join(trace) + '\n')
    files['initialization.txt'] = digest(output / 'initialization.txt')
    files['program.wasm'] = digest(wasm)
    manifest = {'format': 'wasmetal-standalone-v1', 'profile': p, 'export': export,
                'arguments': list(arguments), **summary, 'files': files,
                'source_sha256': digest(source), 'preparation_simulator_sha256': identity['binary_sha256'],
                'preparation_build_id': rtl.build_id, 'physical_hardware_tested': False,
                'preparation_inputs': {name: digest(ROOT/name) for name in
                    ('tools/prepare_standalone.py', 'tools/wasm_image.py', 'tools/run_spec.py', 'tools/upstream.lock.json')}}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, default=ROOT / 'build/standalone-image')
    parser.add_argument('--export', default='main')
    parser.add_argument('--arg', type=lambda x: int(x, 0), action='append', default=[])
    args = parser.parse_args()
    result = prepare(args.source, args.output, args.export, args.arg)
    print(json.dumps({'image': str(args.output), 'counts': result['counts'],
                      'allocated_ram_bytes': result['allocated_ram_bytes']}, indent=2))


if __name__ == '__main__':
    main()
