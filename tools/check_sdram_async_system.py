#!/usr/bin/env python3
"""Exercise the complete CPU through CDC and SDRAM on separate test clocks."""
import argparse
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time

from build_standalone_sim import sources
from check_sdram import PROFILES
from check_sdram_system import replace_once
from loadable_ci import GROUPS, RECOVERY, check_plan
from prepare_standalone import ROOT, digest, load_profile, prepare
from program_upload import profile_tag, encode
from standalone_support import generate_parameters, parameters, verify_simulator, verify_image

CLOCKS = {'faster': {'cpu_half_period': 11, 'memory_half_period': 3, 'memory_phase': 2},
          'slower': {'cpu_half_period': 7, 'memory_half_period': 11, 'memory_phase': 5}}


def build(timing, clock_name, startup, negative):
    profile = load_profile(); generated = generate_parameters(); tag = profile_tag(profile)
    device = dict(PROFILES[timing+'-full']); device['RAM_BYTES'] = profile['ram_bytes']
    if startup is not None:
        if startup < device['POWERUP_CYCLES']:
            raise ValueError('startup override cannot shorten device initialization')
        device['POWERUP_CYCLES'] = startup
    label = f'sdram-async-{clock_name}-{timing}-{device["POWERUP_CYCLES"]}'+('-'+negative if negative else '')
    directory = ROOT/'build'/label; directory.mkdir(parents=True, exist_ok=True)
    binary = directory/'obj/Vwasmetal_loadable'
    if binary.exists() and Path(str(binary)+'.build.json').exists():
        try:
            identity = verify_simulator(binary)
            if identity['backend'] == label+'-rtl':
                return binary, directory, device
        except ValueError:
            pass
    header = directory/'sdram_test_parameters.svh'
    header.write_text(''.join(f'`define SDRAM_{key} {value}\n' for key, value in device.items()))
    clock = CLOCKS[clock_name]
    clock_header = directory/'clock_parameters.hpp'
    clock_header.write_text('#pragma once\n#include <cstdint>\n'+
        f'constexpr uint64_t CPU_HALF_PERIOD={clock["cpu_half_period"]};\n'+
        f'constexpr uint64_t MEMORY_HALF_PERIOD={clock["memory_half_period"]};\n'+
        f'constexpr uint64_t MEMORY_PHASE={clock["memory_phase"]};\n'+
        'constexpr const char* CLOCK_COVERAGE='+json.dumps(str(directory/'clock-coverage.jsonl'))+';\n')
    original = ROOT/'soc/wasmetal_local_memory.sv'; original_top = ROOT/'soc/loader/wasmetal_loadable.sv'
    text = replace_once(original.read_text(), 'wire bus_valid, bus_write, bus_ready, bus_fault;',
        'wire bus_valid, bus_write, bus_ready, bus_fault;\n    wire backend_initialized;')
    text = replace_once(text, '.reset(reset),.initialized(initialized)',
        '.reset(reset || !backend_initialized),.initialized(initialized)')
    text = replace_once(text, '.ready(bus_ready),.fault(bus_fault),.rdata(bus_rdata));',
        '.ready(bus_ready),.fault(bus_fault),.rdata(bus_rdata),.initialized(backend_initialized));')
    local = directory/'wasmetal_local_memory.sv'; local.write_text(text)
    top = directory/'wasmetal_loadable.sv'
    top.write_text(replace_once(original_top.read_text(), 'input wire clk, reset, rx,',
        'input wire clk, memory_clk, reset, rx,'))
    backing = ROOT/'soc/memory/wasmetal_bram.sv'; binding = ROOT/'tests/sdram_async/wasmetal_bram.sv'
    model = ROOT/'tests/sdram/wasmetal_test_sdram.sv'; harness = ROOT/'tests/sdram_async/loadable.cpp'
    replacements = {original: local, original_top: top, backing: binding}; source = sources()
    if any(source.count(path) != 1 for path in replacements):
        raise ValueError('ambiguous asynchronous SDRAM system binding')
    source = [replacements.get(path, path) for path in source]+[model]
    vendor = ROOT/'third_party/hardfloat/source'
    paths = [*source, *sorted(vendor.rglob('*.vi')), harness, original, original_top, header, clock_header,
        Path(__file__).resolve(), generated, ROOT/'tests/standalone/loadable.cpp',
        ROOT/'tools/build_standalone_sim.py', ROOT/'tools/check_sdram_system.py', ROOT/'tools/check_sdram.py',
        ROOT/'tools/prepare_standalone.py', ROOT/'tools/standalone_support.py', ROOT/'tools/program_upload.py',
        ROOT/'tools/loadable_ci.py', ROOT/'soc/profile.json', ROOT/'tools/upstream.lock.json']
    hashes = {str(path.relative_to(ROOT)): digest(path) for path in paths}
    params = {**parameters(profile), 'UART_TICKS': 4, 'UPLOAD_TIMEOUT_CYCLES': 4096,
        'PROFILE_TAG': f"128'h{int.from_bytes(tag, 'little'):032x}"}
    command = [str(ROOT/'.cache/tools/usr/bin/verilator'), '-Wall', '-Wno-UNUSEDSIGNAL',
        '--unroll-count', '512', '--assert', '-DWASMETAL_ASSERTIONS',
        f'-DWASMETAL_TEST_SDRAM_COVERAGE="{directory}/coverage.jsonl"',
        f'-DWASMETAL_ASYNC_SDRAM_COVERAGE="{directory}/source-coverage.jsonl"',
        '--top-module', 'wasmetal_loadable', '-I'+str(vendor), '-I'+str(vendor/'RISCV'),
        '-I'+str(directory), '-I'+str(ROOT/'build'), *[f'-G{name}={value}' for name, value in params.items()],
        '--cc', '--exe', '--build', '-j', '1', '--Mdir', str(directory/'obj'),
        '-CFLAGS', '-std=c++17 -O3 -Wall -Wextra -Werror -DBIT_TICKS=4 -DCLOCK_SCALE=1 -DUPLOAD_TIMEOUT=4096 -I'+str(directory)]
    if negative:
        command.append('-D'+{'read-corruption': 'WASMETAL_TEST_CORRUPT_SDRAM',
            'startup-bypass': 'WASMETAL_ASYNC_SDRAM_BYPASS_STARTUP',
            'wrong-clock': 'WASMETAL_ASYNC_SDRAM_WRONG_CLOCK'}[negative])
    command += [*map(str, source), str(harness)]
    with (directory/'build.log').open('w') as log:
        run = subprocess.run(command, cwd=ROOT, env=dict(os.environ,
            VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')), stdout=log, stderr=subprocess.STDOUT)
    if run.returncode:
        raise RuntimeError((directory/'build.log').read_text()[-10000:])
    for name, value in hashes.items():
        if digest(ROOT/name) != value:
            raise ValueError('asynchronous SDRAM build input changed: '+name)
    identity = {'backend': label+'-rtl', 'inputs': hashes, 'profile': profile, 'profile_tag': tag.hex(),
        'uart_ticks': 4, 'clock_scale': 1, 'upload_timeout': 4096, 'binary_sha256': digest(binary),
        'clock_schedule': clock, 'clock_ticks_are_physical_time': False,
        'backing_memory': {'implementation': 'production CDC and SDR controller with behavioral pin model',
            'device_parameters': device, 'nonzero_power_on_contents': True, 'reset_clears_array': False,
            'negative_control': negative, 'physical_device': False}, 'command': command}
    Path(str(binary)+'.build.json').write_text(json.dumps(identity, indent=2)+'\n')
    return binary, directory, device


def check_clocks(sample, clock):
    elapsed = sample['elapsed_ticks']; cpu = clock['cpu_half_period']; memory = clock['memory_half_period']
    phase = clock['memory_phase']
    if elapsed % (2*cpu) or sample['cpu_rising_edges'] != elapsed//(2*cpu):
        raise ValueError('CPU clock schedule or edge count differs')
    expected_memory = 0 if elapsed < phase else (elapsed-phase)//(2*memory)+1
    if sample['memory_rising_edges'] != expected_memory:
        raise ValueError('memory clock schedule or edge count differs')
    first = next((i*cpu for i in range(1, memory+1) if i*cpu >= phase and (i*cpu-phase)%memory == 0), None)
    expected_coincident = 0 if first is None or elapsed < first else (elapsed-first)//math.lcm(cpu, memory)+1
    if sample['coincident_edges'] != expected_coincident or expected_coincident == 0:
        raise ValueError('coincident clock edges were omitted or miscounted')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--timing', choices=('25mhz', '100mhz'), required=True)
    parser.add_argument('--clocks', choices=CLOCKS, required=True)
    parser.add_argument('--startup-cycles', type=int)
    parser.add_argument('--negative-control', choices=('read-corruption', 'startup-bypass', 'wrong-clock'))
    parser.add_argument('--case', help='one integration case for an initial smoke check')
    args = parser.parse_args(); started = time.monotonic(); check_plan()
    startup = args.startup_cycles or PROFILES[args.timing+'-full']['POWERUP_CYCLES']
    label = f'sdram-async-{args.clocks}-{args.timing}-{startup}'+('-'+args.negative_control if args.negative_control else '')
    if args.case:
        label += '-case-'+args.case
    report = ROOT/'reports'/(label+'.json'); observations = ROOT/'reports'/(label+'-observations.json')
    report.parent.mkdir(exist_ok=True)
    for path in (report, observations):
        path.unlink(missing_ok=True)
    binary, directory, device = build(args.timing, args.clocks, args.startup_cycles, args.negative_control)
    coverage = [directory/name for name in ('coverage.jsonl', 'source-coverage.jsonl', 'clock-coverage.jsonl')]
    for path in coverage:
        path.unlink(missing_ok=True)
    log_path = directory/(label+'-execution.log')
    if args.negative_control in ('startup-bypass', 'wrong-clock'):
        wat = directory/'probe.wat'; wat.write_text('(module (func (export "main") (result i32) i32.const 42))\n')
        image = directory/'probe-image'; prepare(wat, image); verify_image(image)
        packet = directory/'probe.wmu'; packet.write_bytes(encode(image, 0x574d4153594e4300).bytes())
        command = [str(binary), '--upload', str(packet)]
        with log_path.open('w') as log:
            run = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, timeout=1800)
        marker = ('memory request issued before SDRAM startup finished' if args.negative_control == 'startup-bypass'
            else 'SDRAM command before timing recovery')
        if run.returncode == 0 or marker not in log_path.read_text():
            raise ValueError('asynchronous SDRAM mutation did not trigger the expected independent assertion')
        receipt = {'status': 'passed', 'scope': 'complete CPU asynchronous SDRAM negative control, RTL only',
            'negative_control_rejected': args.negative_control, 'expected_diagnostic': marker,
            'command': command, 'packet_sha256': digest(packet), 'exit_code': run.returncode,
            'model': verify_simulator(binary), 'log_sha256': digest(log_path),
            'elapsed_seconds': time.monotonic()-started, 'physical_hardware_tested': False}
    else:
        command = [sys.executable, str(ROOT/'tools/check_loadable.py'), '--binary', str(binary), '--report', str(observations)]
        if args.case or args.negative_control:
            command += ['--case', args.case or 'selftest', '--no-recovery']
        with log_path.open('w') as log:
            run = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, timeout=7200)
        result = json.loads(observations.read_text())
        if args.negative_control:
            if run.returncode == 0 or result['status'] != 'failed' or 'AssertionError: UART result differs from independent expectation:' not in log_path.read_text():
                raise ValueError('corrupted asynchronous read escaped the program-result oracle')
        else:
            run.check_returncode()
            expected = {args.case} if args.case else {name for group in GROUPS for name in group}|set(RECOVERY)
            actual = [case['name'] for case in result['cases']]
            if result['status'] != 'passed' or len(actual) != len(expected) or set(actual) != expected:
                raise ValueError('incomplete asynchronous SDRAM execution coverage')
        identity = verify_simulator(binary)
        if identity != result['model']:
            raise ValueError('asynchronous SDRAM simulator changed')
        samples = [[json.loads(line) for line in path.read_text().splitlines()] if path.exists() else [] for path in coverage]
        totals = {key: sum(sample[key] for sample in samples[0]) for key in
            ('reads', 'writes', 'refreshes', 'read_beats', 'write_beats', 'warm_resets', 'refreshes_during_reset', 'startup_stalls')}
        if not args.negative_control:
            if not samples[0] or len({len(s) for s in samples}) != 1:
                raise ValueError('missing device, CDC or clock observations')
            if any(totals[key] == 0 for key in ('reads', 'writes', 'refreshes', 'read_beats', 'write_beats', 'refreshes_during_reset')):
                raise ValueError('missing asynchronous SDRAM traffic coverage')
            if any(sample['maximum_refresh_gap'] > device['REFRESH_CYCLES'] for sample in samples[0]):
                raise ValueError('SDRAM refresh deadline exceeded')
            if args.startup_cycles and totals['startup_stalls'] == 0:
                raise ValueError('delayed startup was hidden by the upload')
            for sample in samples[2]:
                check_clocks(sample, CLOCKS[args.clocks])
        receipt = {'status': 'passed', 'scope': 'complete CPU through CDC and SDRAM with separately scheduled clocks; RTL and behavioral device, no PHY',
            'case_count': len(result['cases']), 'complete_integration_corpus': not args.case and not args.negative_control,
            'negative_control_rejected': args.negative_control, 'device_parameters': device, 'device_coverage': totals,
            'source_coverage': samples[1], 'clock_coverage': samples[2], 'observations': result,
            'observation_report_sha256': digest(observations), 'model': identity,
            'artifacts': {str(path.relative_to(ROOT)): digest(path) for path in coverage if path.exists()},
            'elapsed_seconds': time.monotonic()-started, 'physical_hardware_tested': False,
            'metastability_or_electrical_timing_simulated': False}
    report.write_text(json.dumps(receipt, indent=2)+'\n')
    print('PASS '+label)


if __name__ == '__main__':
    main()
