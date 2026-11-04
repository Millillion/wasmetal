#!/usr/bin/env python3
"""Compile the standalone RTL with a clock/reset/UART-only test driver."""
import argparse
import json
import os
from pathlib import Path
import subprocess

from prepare_standalone import ROOT, digest, load_profile
from standalone_support import generate_parameters, parameters


def sources():
    vendor = ROOT / 'third_party/hardfloat/source'
    return [ROOT/'rtl/vendor.vlt'] + sorted((ROOT/'rtl').glob('*.sv')) + sorted(vendor.glob('*.v')) + [
        vendor/'RISCV/HardFloat_specialize.v', ROOT/'fpga/wasmetal_uart.sv'] + [
            path for path in sorted((ROOT/'soc').rglob('*.sv'))
            # Startup self-test components have their own verification targets
            # and are not instantiated by any default CPU/board top.
            if path not in {ROOT/'soc/asic/wasmetal_memory_bist.sv',
                            ROOT/'soc/asic/wasmetal_memory_startup.sv'}]


def build(board=False, lint=False):
    p = load_profile()
    generated = generate_parameters()
    top = 'wasmetal_standalone_ulx3s' if board else 'wasmetal_standalone'
    directory = ROOT / 'build' / ('standalone-board-sim' if board else 'standalone-sim')
    directory.mkdir(parents=True, exist_ok=True)
    vendor = ROOT/'third_party/hardfloat/source'
    source = sources()
    inputs = source + sorted(vendor.rglob('*.vi')) + [ROOT/'tests/standalone/system.cpp',
        Path(__file__).resolve(), ROOT/'soc/profile.json', ROOT/'tools/prepare_standalone.py',
        ROOT/'tools/standalone_support.py', generated]
    hashes = {str(path.relative_to(ROOT)): digest(path) for path in inputs}
    args = [str(ROOT/'.cache/tools/usr/bin/verilator'), '-Wall', '-Wno-UNUSEDSIGNAL',
            '--unroll-count', '512', '--assert', '-DWASMETAL_ASSERTIONS', '--top-module', top,
            '-I'+str(vendor), '-I'+str(vendor/'RISCV'), '-I'+str(ROOT/'build')]
    if not board:
        params = parameters(p)
        params['UART_TICKS'] = 4
        args += [f'-G{k}={v}' for k, v in params.items()]
    if lint:
        args += ['--lint-only']
    else:
        args += ['--cc', '--exe', '--build', '-j', '4', '--Mdir', str(directory),
                 '-CFLAGS', '-std=c++17 -O3 -Wall -Wextra -Werror' + (' -DWASMETAL_BOARD' if board else '')]
    args += list(map(str, source))
    if not lint:
        args.append(str(ROOT/'tests/standalone/system.cpp'))
    with (directory/'build.log').open('w') as log:
        result = subprocess.run(args, cwd=ROOT,
            env=dict(os.environ, VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),
            stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        print((directory/'build.log').read_text()[-12000:])
        raise RuntimeError(f'standalone compilation failed: {directory}/build.log')
    if any(digest(ROOT/name) != value for name, value in hashes.items()):
        raise RuntimeError('standalone build inputs changed during compilation')
    if not lint:
        binary = directory/('V'+top)
        receipt = {'backend': 'standalone-board-rtl' if board else 'standalone-rtl',
                   'inputs': hashes, 'profile': p, 'uart_ticks': 81 if board else 4,
                   'binary_sha256': digest(binary)}
        Path(str(binary)+'.build.json').write_text(json.dumps(receipt, indent=2)+'\n')
        print(binary)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--board', action='store_true')
    parser.add_argument('--lint', action='store_true')
    args = parser.parse_args()
    build(args.board, args.lint)
