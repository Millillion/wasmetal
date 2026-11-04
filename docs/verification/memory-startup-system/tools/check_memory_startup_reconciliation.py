#!/usr/bin/env python3
"""Compare complete-CPU startup execution with a fresh SRAM-only baseline."""
import argparse
from copy import deepcopy
import json
from pathlib import Path

from loadable_ci import GROUPS, RECOVERY, check_plan
from prepare_standalone import ROOT, digest
from standalone_support import verify_simulator


NO_COMMIT = frozenset({'profile-rejection', 'crc-rejection', 'partial-reset',
                       'receive-timeout', 'break-abort'})


def require(condition, message):
    if not condition:
        raise ValueError(message)


def after_startup(case, allowance):
    """Predict the entire observation, including clocks, from the old run."""
    expected = deepcopy(case)
    if case['name'] in NO_COMMIT:
        return expected
    traces = [expected['uart']] if 'uart' in expected else [
        expected['interrupted'], expected['recovered']]
    if 'offset_after_commit' in expected:
        expected['offset_after_commit'] += allowance
    for trace in traces:
        trace['clocks'] += allowance
        if trace['first_result_clock']:
            trace['first_result_clock'] += allowance
    return expected


def compare(reference, startup, identity, latency):
    require(reference['status'] == startup['status'] == 'passed', 'passed receipts required')
    require(all(r['physical_hardware_tested'] is False and r['foundry_macro_tested'] is False
                for r in (reference, startup)), 'incorrect physical-validation claim')
    require(reference['read_latency'] == startup['read_latency'] == latency, 'latency mismatch')
    require(not startup['corrupt_read_negative_control_rejected'], 'positive execution required')
    old, new = reference['model'], startup['model']
    require(new == identity == startup['observations']['model'], 'executable identity mismatch')
    require(old == reference['observations']['model'], 'reference executable identity mismatch')
    require(reference['observations']['inputs'] == startup['observations']['inputs'],
            'integration checker inputs changed')
    require(new['backend'] == f'memory-startup-system-{latency}-rtl', 'wrong startup backend')
    require(old['backend'] == f'asic-sram-system-{latency}-rtl', 'wrong baseline backend')
    require(new['profile'] == old['profile'], 'CPU capacity/profile changed')
    for field, value in [('uart_ticks', 4), ('clock_scale', 1), ('upload_timeout', 4096)]:
        require(new[field] == old[field] == value, 'changed UART or upload timing: ' + field)
    require(new['profile_tag'] == old['profile_tag'], 'image profile tag changed')
    memory = new['backing_memory']
    require(memory['read_latency'] == latency and memory['startup_test_bytes'] == new['profile']['ram_bytes'],
            'startup does not test the complete backing capacity')
    require(memory['bridge_held_in_reset_until_test_passes'] is True and
            memory['nonzero_power_on_contents'] is True and memory['reset_clears_array'] is False and
            memory['deliberately_corrupt_read_data'] is False and memory['foundry_macro'] is False,
            'unexpected startup memory binding')
    allowance = 1 + new['profile']['ram_bytes'] // 16 * (320 + 40 * latency)
    require(new['startup_clock_allowance'] == allowance, 'wrong startup clock allowance')
    adjustment = new['harness_deadline_adjustment']
    original = 'const uint64_t deadline=clocks+12000000ULL*CLOCK_SCALE;'
    replacement = f'const uint64_t deadline=clocks+(12000000ULL+{allowance}ULL)*CLOCK_SCALE;'
    require(adjustment == {'original': original, 'replacement': replacement,
            'cpu_watchdog_unchanged': True, 'source_sha256': old['inputs']['tests/standalone/loadable.cpp']},
            'unexpected harness deadline change')
    removed = {'soc/wasmetal_local_memory.sv', 'tools/check_sram_system.py'}
    added = {f'build/memory-startup-system-{latency}/loadable.cpp',
             'soc/asic/wasmetal_memory_bist.sv', 'soc/asic/wasmetal_memory_startup.sv',
             'tests/asic/startup/wasmetal_local_memory.sv',
             'tools/check_memory_startup_system.py', 'tools/run_xc7_system.py'}
    require(set(old['inputs']) - set(new['inputs']) == removed and
            set(new['inputs']) - set(old['inputs']) == added, 'unexpected source inventory difference')
    shared = sorted(set(old['inputs']) & set(new['inputs']))
    require(any(name.startswith('rtl/') for name in shared), 'no shared CPU RTL evidence')
    for name in shared:
        require(old['inputs'][name] == new['inputs'][name], 'changed shared source: ' + name)
    expected_names = {name for group in GROUPS for name in group} | set(RECOVERY)
    for receipt in (reference, startup):
        observation = receipt['observations']
        require(observation['clock_scale'] == 1 and observation['uart_ticks'] == 4 and
                observation['physical_hardware_tested'] is False, 'incorrect observation timing/scope')
        cases = observation['cases']
        require(observation['status'] == 'passed' and receipt['case_count'] == len(expected_names),
                'complete passed case count required')
        require(len(cases) == len(expected_names) and {c['name'] for c in cases} == expected_names,
                'missing, repeated or extra integration case')
    baseline = {c['name']: c for c in reference['observations']['cases']}
    for case in startup['observations']['cases']:
        require(case == after_startup(baseline[case['name']], allowance),
                'startup result, UART bytes, CPU cycles or exact wall clocks differ: ' + case['name'])
    return {'read_latency': latency, 'case_count': len(expected_names),
            'startup_clocks_per_committed_image': allowance, 'unchanged_shared_inputs': shared,
            'source_inventory_difference': {'removed': sorted(removed), 'added': sorted(added)},
            'same_cpu_cycles_and_uart_bytes': True, 'exact_wall_clock_prediction': True}


def negative_controls(reference, startup, identity, latency):
    controls = []

    def reject(name, change):
        candidate = deepcopy(startup)
        change(candidate)
        try:
            compare(reference, candidate, identity, latency)
        except ValueError as error:
            controls.append({'name': name, 'diagnostic': str(error)})
        else:
            raise ValueError('comparison accepted deliberate fault: ' + name)

    def case(receipt, name):
        return next(c for c in receipt['observations']['cases'] if c['name'] == name)

    reject('failed-receipt', lambda r: r.update(status='failed'))
    reject('incomplete-case-list', lambda r: r['observations']['cases'].pop())
    reject('duplicate-case', lambda r: r['observations']['cases'].__setitem__(1, deepcopy(r['observations']['cases'][0])))
    reject('wrong-result', lambda r: case(r, 'answer')['result']['values'].__setitem__(0, 43))
    reject('changed-cpu-cycle-count', lambda r: case(r, 'answer')['result'].update(cycles=0))
    reject('wrong-uart-bytes', lambda r: case(r, 'answer')['uart'].update(uart='00'))
    reject('changed-commit-clock', lambda r: case(r, 'answer')['uart'].update(commit_clock=0))
    reject('missing-boot-delay', lambda r: case(r, 'answer')['uart'].update(
        clocks=next(c for c in reference['observations']['cases'] if c['name'] == 'answer')['uart']['clocks']))
    reject('shifted-first-result', lambda r: case(r, 'answer')['uart'].update(first_result_clock=0))
    reject('delayed-rejected-upload', lambda r: case(r, 'crc-rejection')['uart'].update(clocks=0))
    reject('wrong-interruption-offset', lambda r: case(r, 'reset-during-result').update(offset_after_commit=0))
    reject('wrong-recovery-result', lambda r: case(r, 'reset-during-execution')['recovered'].update(uart='00'))
    reject('different-executable', lambda r: r['model'].update(binary_sha256='0' * 64))
    reject('weakened-watchdog-claim', lambda r: r['model']['harness_deadline_adjustment'].update(cpu_watchdog_unchanged=False))
    reject('different-checker-inputs', lambda r: r['observations']['inputs'].update(
        {next(iter(r['observations']['inputs'])): '0' * 64}))
    reject('wrong-observation-clock-scale', lambda r: r['observations'].update(clock_scale=2))
    return controls


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--latency', type=int, choices=(1, 3), required=True)
    args = parser.parse_args()
    check_plan()
    latency = args.latency
    reference_path = ROOT / f'reports/asic-sram-system-{latency}.json'
    startup_path = ROOT / f'reports/memory-startup-system-{latency}.json'
    output = ROOT / f'reports/memory-startup-system-{latency}-reconciliation.json'
    output.unlink(missing_ok=True)
    reference, startup = [json.loads(p.read_text()) for p in (reference_path, startup_path)]
    for path, receipt in ((reference_path, reference), (startup_path, startup)):
        observations = path.with_name(path.stem + '-observations.json')
        require(digest(observations) == receipt['observation_report_sha256'] and
                json.loads(observations.read_text()) == receipt['observations'], 'raw observation receipt differs')
    binary = ROOT / f'build/memory-startup-system-{latency}/Vwasmetal_loadable'
    identity = verify_simulator(binary)
    require(reference['model'] == verify_simulator(ROOT / f'build/asic-sram-system-{latency}/Vwasmetal_loadable'),
            'fresh baseline executable identity mismatch')
    harness = ROOT / f'build/memory-startup-system-{latency}/loadable.cpp'
    original = ROOT / 'tests/standalone/loadable.cpp'
    adjustment = identity['harness_deadline_adjustment']
    require(original.read_text().count(adjustment['original']) == 1 and
            harness.read_text() == original.read_text().replace(adjustment['original'], adjustment['replacement']),
            'generated harness differs beyond the single overall-deadline allowance')
    check = compare(reference, startup, identity, latency)
    controls = negative_controls(reference, startup, identity, latency)
    paths = [reference_path, startup_path, original, harness, Path(__file__).resolve(),
             ROOT / 'tools/loadable_ci.py', ROOT / 'tools/standalone_support.py', ROOT / 'tools/prepare_standalone.py']
    result = {'status': 'passed', 'scope': 'all bounded programmable CPU integration cases after destructive startup',
              'check': check, 'negative_controls': controls, 'negative_controls_rejected': len(controls),
              'inputs': {str(p.relative_to(ROOT)): digest(p) for p in paths},
              'startup_binary_sha256': digest(binary), 'physical_hardware_tested': False,
              'foundry_macro_tested': False,
              'limitations': ['The complete CPU uses RTL simulation and a behavioral SRAM macro.',
                  'The FPGA images do not yet instantiate this optional startup binding.',
                  'The component-level mapped and formal proofs have separate evidence.']}
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(f'PASS startup reconciliation latency {latency}: {check["case_count"]} cases, {len(controls)} rejected faults')


if __name__ == '__main__':
    main()
