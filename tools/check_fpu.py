#!/usr/bin/env python3
"""Compare shared floating-point RTL with the previous separate-precision design."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parent.parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    start = time.monotonic()
    vendor = sorted((ROOT / 'third_party/hardfloat/source').glob('*.v'))
    vendor.append(ROOT / 'third_party/hardfloat/source/RISCV/HardFloat_specialize.v')
    include_files = sorted((ROOT / 'third_party/hardfloat/source').rglob('*.vi'))
    arithmetic = ROOT / 'rtl/wasmetal_fp_arithmetic.sv'
    reference_format = ROOT / 'tests/rtl/wasmetal_fp_format_reference.sv'
    benches = {
        'fp_shared': [arithmetic, reference_format],
        'fpu_shared': [arithmetic, ROOT / 'rtl/wasmetal_fp_format.sv', ROOT / 'rtl/wasmetal_fpu.sv',
                       reference_format, ROOT / 'tests/rtl/wasmetal_fpu_reference.sv'],
    }
    paths = set(vendor + include_files + [ROOT / 'rtl/vendor.vlt', Path(__file__).resolve(), ROOT / 'tools/upstream.lock.json'])
    for name, sources in benches.items():
        paths.update(sources + [ROOT / f'tests/rtl/{name}_tb.sv', ROOT / f'tests/rtl/{name}.cpp'])
    inputs = {str(p.relative_to(ROOT)): digest(p) for p in sorted(paths)}
    env = dict(os.environ, VERILATOR_ROOT=str(ROOT / '.cache/tools/usr/share/verilator'))
    results = []
    for name, sources in benches.items():
        directory = ROOT / 'build' / name
        directory.mkdir(parents=True, exist_ok=True)
        config = directory / 'test.vlt'
        config.write_text('`verilator_config\n' +
                          (f'lint_off -rule PINCONNECTEMPTY -file "*tests/rtl/{name}_tb.sv"\n' if name == 'fp_shared' else ''))
        command = [str(ROOT / '.cache/tools/usr/bin/verilator'), '-Wall', '-Wno-UNUSEDSIGNAL',
                   '--assert', '-DWASMETAL_ASSERTIONS', '--top-module', name + '_tb',
                   '-Ithird_party/hardfloat/source', '-Ithird_party/hardfloat/source/RISCV',
                   '--cc', '--exe', '--build', '-j', '4', '--Mdir', str(directory / 'obj'),
                   '-MAKEFLAGS', 'OPT_FAST=-O3', '-CFLAGS', '-std=c++17 -O3 -Wall -Wextra -Werror',
                   str(ROOT / 'rtl/vendor.vlt'), str(config), *map(str, sources),
                   str(ROOT / f'tests/rtl/{name}_tb.sv'), *map(str, vendor),
                   str(ROOT / f'tests/rtl/{name}.cpp')]
        with (directory / 'build.log').open('w') as output:
            subprocess.run(command, cwd=ROOT, env=env, stdout=output, stderr=subprocess.STDOUT, check=True)
        binary = directory / 'obj' / ('V' + name + '_tb')
        result = subprocess.run([str(binary)], cwd=ROOT, capture_output=True, text=True, check=True)
        message = result.stdout.strip()
        if not message.startswith('PASS ') or len(message.splitlines()) != 1:
            raise RuntimeError('unexpected floating-point test result: ' + result.stdout + result.stderr)
        negative_controls = 0
        if name == 'fpu_shared':
            for flag in ['--negative-value', '--negative-trap']:
                rejected = subprocess.run([str(binary), flag], cwd=ROOT, capture_output=True, text=True)
                if rejected.returncode == 0 or 'FPU mismatch' not in rejected.stderr:
                    raise RuntimeError('floating-point negative control was not rejected: ' + flag)
                negative_controls += 1
        print(message, flush=True)
        results.append({'bench': name, 'comparisons': int(message.split()[1]),
                        'negative_controls': negative_controls, 'binary_sha256': digest(binary)})
    for name, sha in inputs.items():
        if digest(ROOT / name) != sha:
            raise RuntimeError('floating-point test source changed during verification: ' + name)
    report = {'inputs': inputs, 'results': results, 'elapsed_seconds': time.monotonic() - start,
              'reference': 'Separate precision RTL from f926690; both designs use pinned HardFloat.',
              'scope': 'Deterministic edge and random differential checks, including reset interruption; not a formal arithmetic proof.'}
    target = ROOT / 'reports/floating-point.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
