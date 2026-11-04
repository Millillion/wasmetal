#!/usr/bin/env python3
"""Interrupt CDC/SDRAM transactions at independently observed burst phases."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time

from build_board import yosys
from build_sdram_gate_sim import build
from check_sdram import MACROS, PROFILES
from prepare_standalone import ROOT, digest

CONFIGURATIONS = [[2,3,0],[3,2,1],[5,7,3],[4,4,2],[32,1,0],[1,32,17],[1,1,0]]
STAGES = ['destination request', 'activate', 'burst command',
    *[f'after beat {n}' for n in range(8)], 'precharge', 'destination ready',
    'response crossing', 'source completed']
STYLES = ['one-tick reset', 'held reset with continued refresh', 'source clock paused after reset']
NEGATIVES = {'--corrupt-read': 'CDC SDRAM read differs from independent byte oracle',
    '--ignore-masks': 'CDC SDRAM bytes differ from independent byte oracle',
    '--omit-refresh': 'refresh deadline missed'}


def execute(command, log, timeout):
    with log.open('w') as stream:
        run = subprocess.run(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, timeout=timeout)
    return run, log.read_text()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mapped', action='store_true')
    parser.add_argument('--profile', action='append', choices=('25mhz-full', '100mhz-full'))
    args = parser.parse_args(); started = time.monotonic()
    report = ROOT/'reports'/('cdc-sdram-mapped.json' if args.mapped else 'cdc-sdram-rtl.json')
    report.parent.mkdir(exist_ok=True); report.unlink(missing_ok=True)
    top = 'wasmetal_cdc_sdram'
    source = [ROOT/'soc/external/wasmetal_memory_cdc.sv', ROOT/'soc/sdram/wasmetal_sdram_memory.sv',
        ROOT/'tests/memory/wasmetal_cdc_sdram.sv']
    harness = ROOT/'tests/memory/cdc_sdram.cpp'
    inputs = [*source, harness, ROOT/'tests/memory/sdram_device.hpp', Path(__file__).resolve(),
        ROOT/'tools/check_sdram.py', ROOT/'tools/build_board.py', ROOT/'tools/build_sdram_gate_sim.py',
        ROOT/'tools/build_standalone_gate_sim.py', ROOT/'tools/build_gate_sim.py',
        ROOT/'tools/prepare_standalone.py', ROOT/'tools/upstream.lock.json']
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in inputs}
    results = []
    for name in args.profile or ('25mhz-full', '100mhz-full'):
        profile = PROFILES[name]
        directory = ROOT/'build'/('cdc-sdram-'+name); directory.mkdir(exist_ok=True, parents=True)
        header = directory/'sdram_test_parameters.svh'
        header.write_text(''.join(f'`define SDRAM_{key} {value}\n' for key, value in profile.items()))
        profile_hashes = {**hashes, str(header.relative_to(ROOT)): digest(header)}
        flags = ' '.join(f'-DTEST_{MACROS[key]}={value}' for key, value in profile.items())
        command = [str(ROOT/'.cache/tools/usr/bin/verilator'), '-Wall', '-Wno-UNUSEDSIGNAL',
            '--assert', '-DWASMETAL_ASSERTIONS', '-I'+str(directory), '--top-module', top,
            '--cc', '--exe', '--build', '-j', '1', '-CFLAGS',
            '-std=c++17 -O2 -Wall -Wextra -Werror '+flags, *map(str, source), str(harness)]
        native = directory/'native'; mutant = directory/'cold-reset-mutant'
        env = dict(os.environ, VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator'))
        builds = []
        for target, extra in ((native, []), (mutant, ['-DWASMETAL_TEST_COLD_WARM_RESET'])):
            invocation = [*command, '--Mdir', str(target), *extra]; builds.append(invocation)
            with (directory/(target.name+'-build.log')).open('w') as log:
                run = subprocess.run(invocation, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
            if run.returncode:
                raise RuntimeError((directory/(target.name+'-build.log')).read_text()[-12000:])
        binaries = {'rtl': native/('V'+top)}
        mapped_identity = None
        if args.mapped:
            netlist = directory/'design.json'
            yosys('read_verilog -sv -I'+str(directory)+' '+' '.join(map(str, source))+'\n'+
                f'synth_ecp5 -top {top} -json {netlist}\ncheck -assert\n', 'synthesis', directory)
            netlist.with_suffix('.manifest.json').write_text(json.dumps(
                {'inputs': profile_hashes, 'netlist_sha256': digest(netlist)}, indent=2)+'\n')
            binaries['mapped'] = build(netlist, directory/'mapped', harness, flags, top=top)
            mapped_identity = json.loads(Path(str(binaries['mapped'])+'.build.json').read_text())
        observations = {}
        for backend, binary in binaries.items():
            run, text = execute([str(binary)], directory/(backend+'-execution.log'), 1800)
            if run.returncode:
                raise RuntimeError(text[-12000:])
            observed = json.loads(text)
            rows = observed.get('configurations', [])
            if observed.get('status') != 'passed' or len(rows) != len(CONFIGURATIONS):
                raise ValueError('missing CDC/SDRAM clock configurations')
            for row, clock in zip(rows, CONFIGURATIONS):
                actual = [row[key] for key in ('source_half_period', 'memory_half_period', 'memory_phase')]
                if actual != clock or row['warm_resets'] != 90 or row['cancelled_requests'] != 84 or \
                    row['coverage'] != [[[1]*3 for _ in STAGES] for _ in range(2)] or \
                    row['refreshes_during_reset'] <= 0 or row['largest_refresh_gap'] > profile['REFRESH_CYCLES']:
                    raise ValueError('CDC/SDRAM reset, timing or clock coverage is incomplete')
            negatives = []
            for mutation, marker in NEGATIVES.items():
                run, text = execute([str(binary), mutation], directory/(backend+mutation+'.log'), 90)
                if run.returncode == 0 or marker not in text:
                    raise ValueError('CDC/SDRAM oracle failed to reject '+mutation+': '+text[-2000:])
                negatives.append({'mutation': mutation, 'diagnostic': marker, 'exit_code': run.returncode})
            observations[backend] = {'results': observed, 'binary_sha256': digest(binary),
                'negative_controls': negatives}
        if args.mapped and observations['rtl']['results'] != observations['mapped']['results']:
            raise ValueError('native/mapped CDC/SDRAM stimuli, pins, clocks or coverage differ')
        run, text = execute([str(mutant/('V'+top))], directory/'cold-reset-mutation.log', 90)
        if run.returncode == 0 or 'unexpected clock suspension' not in text:
            raise ValueError('warm-to-cold reset wiring mutation escaped the independent pin model')
        for path, value in profile_hashes.items():
            if digest(ROOT/path) != value:
                raise ValueError('CDC/SDRAM source changed: '+path)
        results.append({'name': name, 'parameters': profile, 'build_commands': builds,
            'tests': observations, 'mapped_build': mapped_identity,
            'cold_reset_mutation': {'rejected': True, 'diagnostic': 'unexpected clock suspension',
                'exit_code': run.returncode, 'binary_sha256': digest(mutant/('V'+top))},
            'artifacts': {str(p.relative_to(ROOT)): digest(p) for p in directory.glob('*.log')}})
        print('PASS CDC and SDRAM '+name+': 630 reset interruptions per model', flush=True)
    for path, value in hashes.items():
        if digest(ROOT/path) != value:
            raise ValueError('CDC/SDRAM source changed: '+path)
    report.write_text(json.dumps({'status': 'passed', 'scope': 'production CDC plus SDRAM controller; independent pin model and byte oracle',
        'profiles': results, 'clock_configurations': CONFIGURATIONS, 'reset_phases': STAGES,
        'reset_styles': STYLES, 'directions': ['read', 'write'], 'inputs': hashes,
        'elapsed_seconds': time.monotonic()-started, 'physical_hardware_tested': False,
        'metastability_or_electrical_timing_simulated': False}, indent=2)+'\n')


if __name__ == '__main__':
    main()
