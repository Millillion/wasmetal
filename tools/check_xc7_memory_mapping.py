#!/usr/bin/env python3
"""Check real 7-series memory mapping against independent traces and vendor RAM models."""
import collections
import copy
import fcntl
import hashlib
import json
from pathlib import Path
import random
import re
import subprocess
import time

from prepare_standalone import ROOT, digest
from xc7_memory_mapping import LIBRARY, audit_address_pins, prepare

BUILD = ROOT / 'build/xc7-memory-mapping'
VENDOR = ROOT / 'third_party/xilinx-unisim'
TOOLS = ROOT / '.cache/tools/usr'
BENCH = ROOT / 'tests/memory/xc7_mapping.sv'
CASES = [(9, 2048, 'RAMB18E1', 'TDP'), (18, 2048, 'RAMB36E1', 'TDP'),
         (36, 1024, 'RAMB36E1', 'TDP'), (36, 512, 'RAMB18E1', 'SDP'),
         (72, 512, 'RAMB36E1', 'SDP'), (9, 4096, 'RAMB36E1', 'TDP')]


def run(command, log, timeout=180):
    with log.open('w') as out:
        result = subprocess.run(list(map(str, command)), cwd=ROOT, stdout=out,
                                stderr=subprocess.STDOUT, timeout=timeout)
    return result.returncode, log.read_text()


def identities(paths):
    return {str(p.relative_to(ROOT)): digest(p) for p in paths}


def verify_vendor():
    pins = json.loads((VENDOR / 'UPSTREAM.json').read_text())
    for item in pins['files']:
        path = VENDOR / item['local_path']
        data = path.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if digest(path) != item['sha256'] or blob != item['git_blob_sha']:
            raise ValueError('unmodified vendor source identity mismatch: ' + path.name)
    return pins


def vectors(width, depth, directory):
    """Software byte-lane oracle; never reads the generated or mapped HDL."""
    rng = random.Random(0x58374337 + width * depth)
    lanes = width // 9
    full_mask = (1 << lanes) - 1
    reset_value = int('a5' * 9, 16) & ((1 << width) - 1)
    memory = [rng.getrandbits(width) for _ in range(depth)]
    initial = directory / 'initial.hex'
    initial.write_text(''.join(f'{word:x}\n' for word in memory))
    rows = []
    output = None
    coverage = collections.Counter()

    def emit(op, wa=0, ra=0, wd=0, mask=0):
        nonlocal output
        if op == 1:
            for lane in range(lanes):
                if mask & (1 << lane):
                    bits = 511 << (9 * lane)
                    memory[wa] = (memory[wa] & ~bits) | (wd & bits)
        elif op == 0:
            output = memory[ra]
        elif op == 4:
            output = reset_value
        if output is None:
            raise ValueError('trace must start with an enabled read')
        rows.append(f'{op:x} {wa:x} {ra:x} {wd:x} {mask:x} {output:x}\n')
        coverage[op] += 1

    # Read every INIT/INITP bit through the public port before modifying storage.
    for addr in range(depth):
        emit(0, ra=addr)
    # Walking bits distinguish data, parity, byte lanes and complements.
    for bit in range(width):
        addr = (bit * 31 + 7) % depth
        for word in [1 << bit, ((1 << width) - 1) ^ (1 << bit)]:
            emit(1, wa=addr, wd=word, mask=full_mask)
            emit(0, ra=addr)
    # Exercise every combination of independent nine-bit write lanes.
    for mask in range(full_mask + 1):
        addr = (mask * 13 + depth - 1) % depth
        emit(1, wa=addr, wd=rng.getrandbits(width), mask=mask)
        emit(0, ra=addr)
    for addr in range(depth):
        emit(1, wa=addr, wd=rng.getrandbits(width), mask=full_mask)
    for addr in reversed(range(depth)):
        emit(0, ra=addr)
    for addr in [0, 1, depth // 2 - 1, depth // 2, depth - 2, depth - 1]:
        emit(3, wa=addr, wd=rng.getrandbits(width), mask=full_mask)  # disabled write
        emit(0, ra=addr)
        emit(2, ra=(addr + 1) % depth)  # disabled read must hold the last word
        emit(5, ra=(addr + 1) % depth)  # reset with read enable low also holds
        emit(4, ra=addr)  # synchronous output reset must not clear stored data
        emit(0, ra=addr)
    # Final whole-memory check catches address aliases and writes to other words.
    for addr in range(depth):
        emit(0, ra=addr)
    path = directory / 'vectors.txt'
    path.write_text(''.join(rows))
    return path, len(rows), dict(coverage), reset_value, initial


def fixture(width, depth, reset_value, initial):
    addr = (depth - 1).bit_length()
    return f'''module ram_fixture(
input wclk,rclk,wen,ren,rst,
input [{addr-1}:0] wa,ra,
input [{width-1}:0] wd,
input [{width//9-1}:0] wmask,
output reg [{width-1}:0] rd);
reg [{width-1}:0] memory [0:{depth-1}];
initial $readmemh({json.dumps(str(initial))},memory);
genvar lane;
generate for(lane=0;lane<{width//9};lane=lane+1) begin
always @(posedge wclk) if(wen && wmask[lane]) memory[wa][lane*9+:9]<=wd[lane*9+:9];
end endgenerate
always @(posedge rclk) if(ren) begin
if(rst) rd<={width}'h{reset_value:x}; else rd<=memory[ra];
end
endmodule
'''


def synthesize(directory, source, corrected):
    prefix = 'fixed' if corrected else 'stock'
    base = 'synth_xilinx -family xc7 -top ram_fixture -noiopad -noclkbuf'
    script = 'read_verilog -sv ' + json.dumps(str(source)) + '\n'
    if corrected:
        commands, overlay = prepare(directory / 'overlay')
        script += base + ' -run begin:map_memory\n' + commands + base + ' -run map_ffram:check\n'
    else:
        overlay = None
        script += base + '\n'
    netlist = directory / (prefix + '.v')
    design = directory / (prefix + '.json')
    script += 'check -assert\nwrite_verilog -noattr ' + json.dumps(str(netlist)) + '\n'
    script += 'write_json ' + json.dumps(str(design)) + '\n'
    path = directory / (prefix + '.ys')
    path.write_text(script)
    log = directory / (prefix + '-synthesis.log')
    code, _ = run([TOOLS / 'bin/yosys', '-Q', '-T', '-s', path], log)
    if code:
        raise RuntimeError('memory synthesis failed: ' + str(log))
    cells = json.loads(design.read_text())['modules']['ram_fixture']['cells']
    counts = collections.Counter(c['type'] for c in cells.values())
    brams = [c for c in cells.values() if c['type'] in ('RAMB18E1', 'RAMB36E1')]
    if len(brams) != 1:
        raise ValueError('fixture must map to exactly one physical block RAM: ' + str(counts))
    pin_audit = audit_address_pins({'cells': cells}) if corrected else None
    pin_negatives = []
    if corrected and brams[0]['type'] == 'RAMB36E1':
        for label in ['low-A15', 'low-unused-A0', 'short-address', 'long-address',
                      'unsupported-width', 'unsupported-cascade']:
            bad = copy.deepcopy(cells)
            ram = next(c for c in bad.values() if c['type'] == 'RAMB36E1')
            address = ram['connections']['ADDRARDADDR']
            if label == 'low-A15':
                address[15] = '0'
            elif label == 'low-unused-A0':
                address[0] = '0'
            elif label == 'short-address':
                address.pop()
            elif label == 'long-address':
                address.append('1')
            elif label == 'unsupported-width':
                ram['parameters']['READ_WIDTH_A'] = f'{3:032b}'
            else:
                ram['parameters']['RAM_EXTENSION_A'] = 'LOWER'
            try:
                audit_address_pins({'cells': bad})
            except ValueError as error:
                pin_negatives.append({'mutation': label, 'rejection': str(error),
                    'mutant_cells_sha256': hashlib.sha256(json.dumps(bad, sort_keys=True).encode()).hexdigest()})
            else:
                raise ValueError('RAM address-pin mutation escaped: ' + label)
    # Use the pinned tool's actual logic cells, but its empty RAM shells are
    # deliberately excluded. All block-RAM behavior comes from original Unisim.
    library = (LIBRARY / 'cells_sim.v').read_text()
    bodies = []
    for kind in sorted(set(counts) - {'RAMB18E1', 'RAMB36E1'}):
        if kind not in {'INV', *['LUT' + str(i) for i in range(1, 7)]}:
            raise ValueError('review unexpected fixture logic cell: ' + kind)
        matches = re.findall(r'^module\s+' + re.escape(kind) + r'\s*\(.*?^endmodule', library, re.M | re.S)
        if len(matches) != 1:
            raise ValueError('ambiguous logic primitive extraction: ' + kind)
        bodies.extend(matches)
    logic = directory / (prefix + '-logic.v')
    logic.write_text('\n'.join(bodies) + '\n')
    return netlist, logic, {'cell_counts': dict(counts), 'ram_parameters': brams[0]['parameters'],
        'ram_type': brams[0]['type'], 'overlay': overlay, 'address_pin_audit': pin_audit,
        'address_pin_negative_controls': pin_negatives,
        'artifacts': identities([source, path, log, netlist, design, logic])}


def simulate(directory, label, sources, vector_file, count, width, depth, expected_failure=None):
    binary = directory / (label + '.vvp')
    compile_log = directory / (label + '-compile.log')
    command = [TOOLS / 'bin/iverilog', '-B' + str(TOOLS / 'lib/x86_64-linux-gnu/ivl'),
        '-g2012', '-s', 'xc7_mapping', '-s', 'glbl', '-I' + str(directory), '-o', binary,
        *sources, VENDOR / 'glbl.v', BENCH]
    code, _ = run(command, compile_log)
    if code:
        raise RuntimeError('memory simulator compilation failed: ' + str(compile_log))
    log = directory / (label + '.log')
    code, text = run([TOOLS / 'bin/vvp', binary, '+VECTORS=' + str(vector_file), '+COUNT=' + str(count)], log)
    marker = f'PASS XC7_MEMORY vectors={count} width={width} depth={depth}'
    if expected_failure is None:
        extra = [line for line in text.splitlines() if line and line != marker and
                 not re.fullmatch(r'.*:\d+: \$finish called at \d+ \(1ps\)', line)]
        if code != 0 or text.splitlines().count(marker) != 1 or extra:
            raise ValueError('memory simulation failed or emitted unexpected diagnostics: ' + str(log))
    elif code == 0 or expected_failure not in text or marker in text:
        raise ValueError('memory negative control was not rejected: ' + str(log))
    return {'label': label, 'returncode': code, 'expected_failure': expected_failure,
        'observations': text.splitlines(), 'command': list(map(str, command)),
        'artifacts': identities([*sources, binary, compile_log, log, vector_file,
                                 directory / 'fixture_parameters.svh'])}


def main():
    started = time.monotonic()
    BUILD.mkdir(parents=True, exist_ok=True)
    report = ROOT / 'reports/xc7-memory-mapping.json'
    report.parent.mkdir(exist_ok=True)
    report.unlink(missing_ok=True)
    pins = verify_vendor()
    inputs = [Path(__file__).resolve(), ROOT / 'tools/xc7_memory_mapping.py',
        ROOT / 'tools/prepare_standalone.py', BENCH, *sorted(p for p in VENDOR.iterdir() if p.is_file()),
        *[p for p in sorted(LIBRARY.rglob('*')) if p.is_file()],
        *[p for p in sorted(LIBRARY.parent.glob('*.v')) if p.is_file()],
        *[TOOLS / 'bin' / n for n in ['yosys', 'yosys-abc', 'iverilog', 'vvp']],
        *[p for p in sorted((TOOLS / 'lib/x86_64-linux-gnu/ivl').glob('*')) if p.is_file()]]
    hashes = identities(inputs)
    checks = []
    for width, depth, ram_type, mode in CASES:
        directory = BUILD / f'w{width}-d{depth}'
        directory.mkdir(exist_ok=True)
        vector_file, count, coverage, reset_value, initial = vectors(width, depth, directory)
        constants = directory / 'fixture_parameters.svh'
        constants.write_text(f'`define WIDTH {width}\n`define DEPTH {depth}\n'
            f'`define ADDR_WIDTH {(depth-1).bit_length()}\n`define LANES {width//9}\n')
        source = directory / 'fixture.sv'
        body = fixture(width, depth, reset_value, initial)
        source.write_text(body)
        generated_inputs = identities([initial, vector_file, constants, source])
        native = simulate(directory, 'native', [source], vector_file, count, width, depth)
        netlist, logic, mapping = synthesize(directory, source, corrected=True)
        if mapping['ram_type'] != ram_type or mapping['ram_parameters']['RAM_MODE'].strip() != mode:
            raise ValueError('unexpected mapped RAM configuration: ' + str(mapping['ram_parameters']))
        mapped = simulate(directory, 'fixed', [netlist, logic, VENDOR / 'RAMB18E1.v', VENDOR / 'RAMB36E1.v'],
                          vector_file, count, width, depth)
        negatives = []
        if width == 72:
            bad, bad_logic, stock = synthesize(directory, source, corrected=False)
            negatives.append(simulate(directory, 'stock', [bad, bad_logic, VENDOR / 'RAMB18E1.v', VENDOR / 'RAMB36E1.v'],
                vector_file, count, width, depth, 'READ_DATA_MISMATCH'))
            mutations = {
                'ignored-write-enable': ('wen && wmask[lane]', 'wmask[lane]'),
                'ignored-lane-mask': ('wen && wmask[lane]', 'wen'),
                'ignored-read-enable': ('if(ren)', "if(1'b1)"),
                'ignored-output-reset': ('if(rst)', "if(1'b0)"),
                'aliased-read-address': ('memory[ra]', f'memory[ra & {depth//2-1}]'),
            }
            for label, (before, after) in mutations.items():
                if body.count(before) != 1:
                    raise ValueError('review memory oracle mutation anchor: ' + label)
                mutant = directory / (label + '.sv')
                mutant.write_text(body.replace(before, after))
                negatives.append(simulate(directory, label, [mutant], vector_file, count, width, depth,
                                          'READ_DATA_MISMATCH'))
            mapping['stock_negative_mapping'] = stock
        if identities([ROOT / name for name in generated_inputs]) != generated_inputs:
            raise ValueError('generated memory-verification inputs changed')
        checks.append({'width': width, 'depth': depth, 'vectors_per_model': count,
            'operation_counts': coverage, 'generated_inputs': generated_inputs,
            'mapping': mapping, 'native': native, 'vendor_mapped': mapped, 'negative_controls': negatives})
        print(f'PASS {width}x{depth}: {count} vectors/model; {ram_type} {mode}; {len(negatives)} negative controls', flush=True)
    if identities(inputs) != hashes:
        raise ValueError('memory verification inputs changed during execution')
    verify_vendor()
    report.write_text(json.dumps({'status': 'passed',
        'scope': 'Five initialized RAM geometries: exact public-port traces in native RTL and physically mapped primitives using unmodified vendor four-state models; read/write clock edges are separated by at least 10 ns',
        'inputs': hashes, 'vendor_source': pins, 'checks': checks,
        'total_vectors_per_model': sum(c['vectors_per_model'] for c in checks),
        'negative_controls_rejected': sum(len(c['negative_controls']) for c in checks),
        'address_pin_negative_controls_rejected': sum(len(c['mapping']['address_pin_negative_controls']) for c in checks),
        'whole_cpu_mapping_verified': False, 'physical_hardware_tested': False,
        'limitations': ['No collision, asynchronous-clock aperture, metastability or electrical timing claim.',
                        'No DSP, complete CPU, place-and-route or board verification is implied.'],
        'elapsed_seconds': time.monotonic()-started}, indent=2) + '\n')


if __name__ == '__main__':
    BUILD.mkdir(parents=True, exist_ok=True)
    with (BUILD / '.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        main()
