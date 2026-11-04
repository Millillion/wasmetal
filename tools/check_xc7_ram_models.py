#!/usr/bin/env python3
"""Compare experimental fast RAM models with preserved vendor-model evidence."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import random
import re
import resource
import shutil
import subprocess
import time

from check_xc7_memory_mapping import CASES, VENDOR, TOOLS, identities, simulate, verify_vendor
from prepare_standalone import ROOT, digest

BUILD = ROOT / 'build/xc7-ram-models'
MODEL = ROOT / 'tests/xc7/ram_primitives.sv'
BENCH = ROOT / 'tests/xc7/ram_four_state.sv'
KNOWN_BENCH = ROOT / 'tests/memory/xc7_mapping.sv'


def run(command, log, timeout=300):
    def no_core_dump():
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    with log.open('w') as out:
        result = subprocess.run(list(map(str, command)), cwd=ROOT, stdout=out,
            stderr=subprocess.STDOUT, timeout=timeout, preexec_fn=no_core_dump,
            env=dict(os.environ, VERILATOR_ROOT=str(TOOLS / 'share/verilator')))
    return result.returncode, log.read_text()


def outcome(code, text, marker, failure=None, verilator=False):
    if failure:
        if code == 0 or failure not in text or 'PASS XC7_' in text:
            raise ValueError('negative control was not rejected: ' + failure)
        return
    allowed = [r'.*:\d+: \$finish called at \d+ \(1ps\)',
               r'- .*:\d+: Verilog \$finish', r'- S i m u l a t i o n.*',
               r'- Verilator:.*', r'- Walltime.*'] if verilator else [r'.*:\d+: \$finish called at \d+ \(1ps\)']
    extra = [line for line in text.splitlines() if line and line != marker and
             not any(re.fullmatch(p, line) for p in allowed)]
    if code or text.splitlines().count(marker) != 1 or extra:
        raise ValueError('simulation failed or emitted unexpected diagnostics: ' + text[-2000:])


def four_state_vectors(width, depth, initial, unknown, directory):
    rng = random.Random(0x7CA4 + width * depth)
    bits = lambda value: list(f'{value:0{width}b}'[::-1])
    memory = [list('x' * width) if unknown else bits(int(word, 16))
              for word in initial.read_text().splitlines()]
    assert len(memory) == depth
    rows = []
    previous = None
    counts = {'x_write_bits': 0, 'z_write_bits': 0}
    full = (1 << (width // 9)) - 1

    def emit(op, wa=0, ra=0, wd=None, mask=0):
        nonlocal previous
        wd = bits(0) if wd is None else list(wd)
        if op == 1:
            for bit in range(width):
                if mask & (1 << (bit // 9)):
                    if wd[bit] in ('x', 'z'):
                        counts[wd[bit] + '_write_bits'] += 1
                    memory[wa][bit] = wd[bit]
        elif op == 0:
            previous = memory[ra].copy()
        elif op == 4:
            previous = bits(int('a5' * 9, 16) & ((1 << width) - 1))
        if previous is None:
            raise ValueError('four-state trace must start with a read')
        rows.append(f'{op:x} {wa:x} {ra:x} {"".join(reversed(wd))} {mask:x} {"".join(reversed(previous))}\n')

    for addr in range(depth):
        emit(0, ra=addr)
    for lane in range(width // 9):
        addr = (lane * 41 + depth // 2) % depth
        for word in ['x' * width, 'z' * width, ''.join(rng.choice('01xz') for _ in range(width))]:
            emit(1, wa=addr, wd=word, mask=1 << lane)
            emit(0, ra=addr)
            emit(2, ra=(addr+1) % depth)
            emit(3, wa=addr, wd=bits(0), mask=full)
            emit(0, ra=addr)
            emit(4, ra=addr)
            emit(0, ra=addr)
    for word in [('x' if bit % 9 == 8 else '0' for bit in range(width)),
                 ('1' if bit % 9 == 8 else 'x' for bit in range(width))]:
        emit(1, wa=depth-1, wd=list(word), mask=full)
        emit(0, ra=depth-1)
    for addr in range(depth):
        emit(0, ra=addr)
    path = directory / ('unknown-init.txt' if unknown else 'known-init.txt')
    path.write_text(''.join(rows))
    return path, len(rows), counts


def simulate_four(directory, label, netlist, logic, models, vector_file, count, width, depth, failure=None):
    sources = [netlist, logic, *models, VENDOR / 'glbl.v', BENCH]
    inputs = identities([*sources, vector_file, directory / 'fixture_parameters.svh'])
    binary = directory / (label + '.vvp')
    compile_log = directory / (label + '-compile.log')
    command = [TOOLS / 'bin/iverilog', '-B' + str(TOOLS / 'lib/x86_64-linux-gnu/ivl'),
        '-g2012', '-s', 'xc7_ram_four_state', '-s', 'glbl', '-I' + str(directory), '-o', binary, *sources]
    code, _ = run(command, compile_log)
    if code:
        raise RuntimeError('four-state compilation failed: ' + str(compile_log))
    log = directory / (label + '.log')
    code, text = run([TOOLS / 'bin/vvp', binary, '+VECTORS=' + str(vector_file), '+COUNT=' + str(count)], log)
    outcome(code, text, f'PASS XC7_FOUR_STATE vectors={count} width={width} depth={depth}', failure)
    if identities([ROOT / n for n in inputs]) != inputs:
        raise ValueError('four-state model inputs changed')
    return {'label': label, 'inputs': inputs, 'returncode': code, 'expected_failure': failure,
        'command': list(map(str, command)), 'observations': text.splitlines(),
        'artifacts': identities([binary, compile_log, log])}


def verilate(directory, netlist, logic, vector_file, count, width, depth):
    obj = directory / 'obj'
    sources = [netlist, logic, MODEL, KNOWN_BENCH]
    inputs = identities([*sources, vector_file, directory / 'fixture_parameters.svh'])
    command = [TOOLS / 'bin/verilator', '--binary', '--timing', '--assert', '-j', '2',
        '-Wno-fatal', '--top-module', 'xc7_mapping', '-I' + str(directory), '--Mdir', obj, *sources]
    compile_log = directory / 'verilator-build.log'
    code, _ = run(command, compile_log, timeout=600)
    if code:
        raise RuntimeError('Verilator compilation failed: ' + str(compile_log))
    binary = obj / 'Vxc7_mapping'
    log = directory / 'verilator.log'
    code, text = run([binary, '+VECTORS=' + str(vector_file), '+COUNT=' + str(count)], log)
    outcome(code, text, f'PASS XC7_MEMORY vectors={count} width={width} depth={depth}', verilator=True)
    if identities([ROOT / n for n in inputs]) != inputs:
        raise ValueError('Verilator model inputs changed')
    return binary, {'inputs': inputs, 'command': list(map(str, command)), 'observations': text.splitlines(),
        'artifacts': identities([binary, compile_log, log])}


def main():
    started = time.monotonic()
    report = ROOT / 'reports/xc7-ram-models.json'
    report.unlink(missing_ok=True)
    reference_path = ROOT / 'reports/xc7-memory-mapping.json'
    reference = json.loads(reference_path.read_text())
    if reference['status'] != 'passed' or reference['negative_controls_rejected'] != 6:
        raise ValueError('run the complete vendor mapping regression first')
    if [(c['width'], c['depth'], c['mapping']['ram_type'], c['mapping']['ram_parameters']['RAM_MODE'].strip())
            for c in reference['checks']] != CASES:
        raise ValueError('vendor reference must cover every expected geometry exactly once')
    for name, value in reference['inputs'].items():
        if digest(ROOT / name) != value:
            raise ValueError('stale vendor reference input: ' + name)
    verify_vendor()
    tools = [TOOLS / 'bin/verilator', TOOLS / 'bin/verilator_bin', Path(shutil.which('g++')).resolve()]
    tool_identities = {str(p): digest(p) for p in tools}
    inputs = identities([Path(__file__).resolve(), MODEL, BENCH, KNOWN_BENCH,
        ROOT / 'tools/check_xc7_memory_mapping.py', ROOT / 'tools/prepare_standalone.py', reference_path])
    checks = []
    negatives = []
    for case in reference['checks']:
        width, depth = case['width'], case['depth']
        source = ROOT / 'build/xc7-memory-mapping' / f'w{width}-d{depth}'
        directory = BUILD / source.name
        directory.mkdir(parents=True, exist_ok=True)
        for group in [case['generated_inputs'], case['mapping']['artifacts'], case['vendor_mapped']['artifacts']]:
            for name, value in group.items():
                if digest(ROOT / name) != value:
                    raise ValueError('stale vendor reference artifact: ' + name)
        shutil.copyfile(source / 'fixture_parameters.svh', directory / 'fixture_parameters.svh')
        netlist, logic = source / 'fixed.v', source / 'fixed-logic.v'
        known = source / 'vectors.txt'
        fast = simulate(directory, 'fast', [netlist, logic, MODEL], known,
                        case['vectors_per_model'], width, depth)
        binary, compiled = verilate(directory, netlist, logic, known, case['vectors_per_model'], width, depth)
        unknown_cases = []
        for unknown in [False, True]:
            vector_file, count, counts = four_state_vectors(width, depth, source / 'initial.hex', unknown, directory)
            variant = netlist
            if unknown:
                body, replacements = re.subn(r"(\.INITP?_[0-9A-F]{2}\()256'h[0-9a-fA-FxXzZ]+(\))",
                    lambda m: m.group(1) + "256'h" + 'x' * 64 + m.group(2), netlist.read_text())
                if replacements != (72 if case['mapping']['ram_type'] == 'RAMB18E1' else 144):
                    raise ValueError('unexpected initialization parameter count')
                variant = directory / 'unknown-init.v'
                variant.write_text(body)
            label = 'unknown-init' if unknown else 'known-init'
            native_source = source / 'fixture.sv'
            if unknown:
                native_body, removed = re.subn(r'^initial \$readmemh[^\n]*\n', '',
                    native_source.read_text(), flags=re.M)
                if removed != 1:
                    raise ValueError('native unknown-initialization anchor missing')
                native_source = directory / 'native-unknown-init.sv'
                native_source.write_text(native_body)
            native = simulate_four(directory, label + '-native', native_source, logic,
                [], vector_file, count, width, depth)
            vendor = simulate_four(directory, label + '-vendor', variant, logic,
                [VENDOR / 'RAMB18E1.v', VENDOR / 'RAMB36E1.v'], vector_file, count, width, depth)
            proposed = simulate_four(directory, label + '-fast', variant, logic, [MODEL],
                vector_file, count, width, depth)
            unknown_cases.append({'unknown_initial_storage': unknown, 'vectors_per_model': count,
                'write_bit_counts': counts, 'native': native, 'vendor': vendor, 'fast': proposed})
        if width == 72:
            negatives.append(simulate(directory, 'stock-fast', [source / 'stock.v', source / 'stock-logic.v', MODEL],
                known, case['vectors_per_model'], width, depth, 'READ_DATA_MISMATCH'))
            for name, value in [('DOA_REG', '1'), ('DOB_REG', '1'), ('READ_WIDTH_A', '36'),
                    ('RAM_MODE', '"TDP"'), ('IS_CLKARDCLK_INVERTED', "1'b1"),
                    ('EN_ECC_READ', '"TRUE"'), ('RAM_EXTENSION_A', '"LOWER"')]:
                body = netlist.read_text()
                pattern = r'(\.' + name + r'\()[^)]*(\))'
                if re.search(pattern, body):
                    body, replacements = re.subn(pattern, lambda m: m.group(1)+value+m.group(2), body)
                    if replacements != 1:
                        raise ValueError('ambiguous configuration mutation')
                else:
                    if body.count('RAMB36E1 #(') != 1:
                        raise ValueError('configuration insertion anchor missing')
                    body = body.replace('RAMB36E1 #(', f'RAMB36E1 #(\n    .{name}({value}),')
                mutant = directory / (name + '.v')
                mutant.write_text(body)
                negatives.append(simulate_four(directory, name, mutant, logic, [MODEL],
                    directory / 'known-init.txt', unknown_cases[0]['vectors_per_model'], width, depth,
                    'UNSUPPORTED_XC7_RAM_CONFIGURATION'))
            for label, pattern, replacement, init_kind in [
                ('zero-unknown-init', r'words\[word_index\]\[lane\*9\+:9\]=\{.*?\};',
                 "words[word_index][lane*9+:9]=9'b0;", 'unknown'),
                ('zero-unknown-write', r'words\[write_index\]\[lane\*9\+:9\]<=\{.*?\};',
                 "words[write_index][lane*9+:9]<=9'b0;", 'known')]:
                body, replacements = re.subn(pattern, replacement, MODEL.read_text(), flags=re.S)
                if replacements != 1:
                    raise ValueError('review unknown-state mutation anchor')
                mutant = directory / (label + '.sv'); mutant.write_text(body)
                selected = directory / 'unknown-init.v' if init_kind == 'unknown' else netlist
                entry = unknown_cases[1 if init_kind == 'unknown' else 0]
                negatives.append(simulate_four(directory, label, selected, logic, [mutant],
                    directory / (init_kind + '-init.txt'), entry['vectors_per_model'], width, depth,
                    'READ_DATA_MISMATCH'))
            first = int((source / 'initial.hex').read_text().splitlines()[0], 16)
            collision = directory / 'collision.txt'
            collision.write_text(f'0 0 0 {0:072b} 0 {first:072b}\n6 0 0 {0:072b} ff {first:072b}\n')
            negatives.append(simulate_four(directory, 'collision', netlist, logic, [MODEL],
                collision, 2, width, depth, 'UNSUPPORTED_XC7_RAM_COLLISION'))
            # Execute the real compiled parser with truncated, extra and malformed data.
            for label, data, declared, error in [
                ('missing-vector', ''.join(known.read_text().splitlines(keepends=True)[:-1]), case['vectors_per_model'], 'INCOMPLETE_VECTORS'),
                ('extra-vector', known.read_text(), case['vectors_per_model']-1, 'MALFORMED_VECTORS'),
                ('malformed-vector', known.read_text()+'not-a-vector\n', case['vectors_per_model'], 'MALFORMED_VECTORS')]:
                path = directory / (label + '.txt'); path.write_text(data)
                log = directory / (label + '.log')
                code, text = run([binary, '+VECTORS=' + str(path), '+COUNT=' + str(declared)], log)
                outcome(code, text, '', error, verilator=True)
                negatives.append({'label': label, 'expected_failure': error, 'returncode': code,
                    'observations': text.splitlines(), 'artifacts': identities([path, binary, log])})
        checks.append({'width': width, 'depth': depth, 'known_vectors': case['vectors_per_model'],
            'fast_icarus': fast, 'fast_verilator': compiled, 'four_state': unknown_cases})
        print(f'PASS fast RAM {width}x{depth}: both simulators, vendor reference and X/Z data', flush=True)
    if identities([ROOT / n for n in inputs]) != inputs or any(digest(Path(p)) != h for p, h in tool_identities.items()):
        raise ValueError('fast RAM verification inputs changed')
    verify_vendor()
    if len(negatives) != 14:
        raise ValueError('missing fast RAM negative controls')
    report.write_text(json.dumps({'status': 'passed', 'inputs': inputs, 'tools': tool_identities,
        'scope': 'Experimental untimed models for five RAM configurations; known vectors in Icarus and Verilator plus native/vendor/fast four-state data and initialization checks',
        'reference_report_sha256': digest(reference_path), 'checks': checks, 'negative_controls': negatives,
        'negative_controls_rejected': len(negatives),
        'known_vectors_per_model': sum(c['known_vectors'] for c in checks),
        'four_state_vectors_per_model': sum(s['vectors_per_model'] for c in checks for s in c['four_state']),
        'whole_cpu_mapping_verified': False, 'physical_hardware_tested': False,
        'limitations': ['Only the five explicitly accepted configurations are supported.',
            'No aperture, metastability, electrical timing or general collision semantics are modeled.',
            'Unknown control/address signals are outside this regression. WRITE_FIRST collisions fail closed.'],
        'elapsed_seconds': time.monotonic()-started}, indent=2)+'\n')


if __name__ == '__main__':
    BUILD.mkdir(parents=True, exist_ok=True)
    with (BUILD / '.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        main()
