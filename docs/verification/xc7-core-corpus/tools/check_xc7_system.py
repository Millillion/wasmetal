#!/usr/bin/env python3
"""Reconcile all 35 programmable Xilinx cases with an unchanged RTL reference."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import time

from loadable_ci import GROUPS, RECOVERY, check_plan
from prepare_standalone import ROOT, digest
from program_upload import profile_tag
from standalone_support import parameters, verify_simulator

# The legacy native builder parses every soc/*.sv file. These nine modules
# are not instantiated by the default core-clock loadable top; alternate
# memory backends, instruction-codec checks and board wrappers use them.
NATIVE_PARSE_ONLY = frozenset({
    'soc/asic/wasmetal_sram_memory.sv',
    'soc/external/wasmetal_async_axi_memory.sv',
    'soc/external/wasmetal_axi_memory.sv',
    'soc/external/wasmetal_memory_cdc.sv',
    'soc/loader/wasmetal_instruction_decode.sv',
    'soc/loader/wasmetal_instruction_encode.sv',
    'soc/loader/wasmetal_loadable_ulx3s.sv',
    'soc/sdram/wasmetal_sdram_memory.sv',
    'soc/wasmetal_standalone_ulx3s.sv',
})


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_models(reference, native, mapped):
    check_plan()
    require(reference['status'] == 'passed' and reference['model'] == native,
            'passed native reference and exact executable identity required')
    require(native['backend'] in ('loadable-rtl', 'loadable-xc7-rtl') and native['clock_scale'] == 1,
            'core-clock RTL reference required')
    require(mapped['backend'] == 'loadable-mapped-xc7-functional' and mapped['top'] == 'wasmetal_loadable',
            'complete 7-series mapped system required')
    for key in ('profile', 'profile_tag', 'uart_ticks', 'clock_scale', 'upload_timeout'):
        require(mapped[key] == native[key], 'different circuit configuration: '+key)
    require(native['profile_tag'] == profile_tag(native['profile']).hex(), 'profile tag differs from capacities')
    expected_params = parameters(native['profile'])
    expected_params.update(PROFILE_TAG=f"128'h{int.from_bytes(profile_tag(native['profile']),'little'):032x}",
                           UART_TICKS=native['uart_ticks'], UPLOAD_TIMEOUT_CYCLES=native['upload_timeout'])
    require(mapped['parameters'] == expected_params, 'mapped elaboration parameters differ from RTL')
    if 'parameters' in native:
        require(native['parameters'] == expected_params, 'native elaboration parameters differ')
    shared = {}
    for name, value in native['inputs'].items():
        if name.startswith(('rtl/', 'soc/')) and Path(name).suffix in ('.sv','.svh','.v','.vi','.json'):
            require(mapped['inputs'].get(name) == value or name in NATIVE_PARSE_ONLY and name not in mapped['inputs'],
                    'different RTL or system source: '+name)
        if name in mapped['inputs']:
            require(mapped['inputs'][name] == value, 'different shared model input: '+name)
            shared[name] = value
    for name, value in mapped['inputs'].items():
        if name.startswith(('rtl/', 'soc/')) and Path(name).suffix in ('.sv','.svh','.v','.vi','.json'):
            require(native['inputs'].get(name) == value, 'mapped RTL source absent from native model: '+name)
    require(any(k.startswith('build/') and k.endswith('/mapped.json') and v == mapped['netlist_sha256']
                for k,v in mapped['inputs'].items()), 'missing exact synthesized circuit identity')
    return shared


def compare(reference, reports, native, mapped):
    shared = validate_models(reference, native, mapped)
    expected = {c['name']: c for c in reference['cases']}
    names = {name for group in GROUPS for name in group} | set(RECOVERY)
    require(len(reference['cases']) == len(names) and set(expected) == names, 'incomplete native case coverage')
    require(len(reports) == len(GROUPS), 'missing or extra mapped partitions')
    groups = set(); observed = {}
    for report in reports:
        require(report['status'] == 'passed' and report['model'] == mapped, 'mapped partition status or identity differs')
        require(report['inputs'] == reference['inputs'], 'different integration checker inputs')
        actual = [case['name'] for case in report['cases']]
        choices = [n for n,group in enumerate(GROUPS) if actual == group+(RECOVERY if n == 0 else [])]
        require(len(choices) == 1 and choices[0] not in groups, 'missing, duplicate or reordered partition cases')
        groups.add(choices[0])
        for case in report['cases']:
            name = case['name']
            require(name not in observed and case == expected[name], 'UART bytes, cycles, image or result differs: '+name)
            observed[name] = case
    require(groups == set(range(len(GROUPS))) and set(observed) == names, 'incomplete mapped case coverage')
    return [observed[name] for name in sorted(observed)], shared


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference', type=Path, default=ROOT/'reports/loadable-rtl.json')
    parser.add_argument('--reports', type=Path, default=ROOT/'reports/xc7-system-shards')
    parser.add_argument('--native-simulator', type=Path, default=ROOT/'build/loadable-sim/Vwasmetal_loadable')
    parser.add_argument('--mapped-simulator', type=Path, default=ROOT/'build/xc7-accelerated-gate-fast/obj/Vwasmetal_loadable')
    parser.add_argument('--output', type=Path, default=ROOT/'reports/xc7-system-complete.json')
    args = parser.parse_args(); started = time.monotonic()
    paths = sorted(args.reports.glob('loadable-mapped-*.json'))
    consumed = [args.reference, *paths, Path(__file__).resolve(), ROOT/'tools/loadable_ci.py',
                ROOT/'tools/standalone_support.py', ROOT/'tools/program_upload.py', ROOT/'tools/prepare_standalone.py']
    protected = [*consumed, args.native_simulator, args.mapped_simulator,
                 Path(str(args.native_simulator)+'.build.json'), Path(str(args.mapped_simulator)+'.build.json')]
    if args.output.resolve() in {p.resolve() for p in protected}:
        parser.error('output must not overwrite a verification input')
    args.output.unlink(missing_ok=True)
    inputs = {str(p.resolve().relative_to(ROOT)): digest(p) for p in consumed}
    reference = json.loads(args.reference.read_text()); reports = [json.loads(p.read_text()) for p in paths]
    native = verify_simulator(args.native_simulator); mapped = verify_simulator(args.mapped_simulator)
    cases, shared = compare(reference, reports, native, mapped)
    for name, value in reference['inputs'].items():
        path = Path(name)
        require(not path.is_absolute() and '..' not in path.parts and digest(ROOT/path) == value,
                'integration checker input changed: '+name)
        require(name not in inputs or inputs[name] == value, 'conflicting checker identity: '+name)
        inputs[name] = value
    controls = []

    def reject(name, mutation):
        ref, rows = deepcopy((reference, reports)); mutation(ref, rows)
        try:
            compare(ref, rows, native, mapped)
        except ValueError as error:
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
        else:
            raise ValueError('comparison accepted deliberate defect: '+name)

    reject('missing-partition', lambda r,s: s.pop())
    reject('duplicate-partition', lambda r,s: s.__setitem__(-1, deepcopy(s[0])))
    reject('incomplete-partition', lambda r,s: s[0].update(status='running'))
    reject('missing-case', lambda r,s: s[0]['cases'].pop())
    reject('reordered-cases', lambda r,s: s[0]['cases'].reverse())
    reject('native-substitution', lambda r,s: s[0].update(model=deepcopy(native)))
    reject('wrong-result', lambda r,s: s[0]['cases'][0]['result']['values'].__setitem__(0,s[0]['cases'][0]['result']['values'][0]^1))
    reject('wrong-clock', lambda r,s: s[0]['cases'][0]['uart'].update(clocks=s[0]['cases'][0]['uart']['clocks']+1))
    reject('wrong-packet', lambda r,s: s[0]['cases'][0].update(packet_sha256='0'*64))
    def flip_uart(reference, rows):
        uart = rows[0]['cases'][0]['uart']
        uart['uart'] = f"{int(uart['uart'][:2],16)^1:02x}"+uart['uart'][2:]
    reject('wrong-uart', flip_uart)
    reject('wrong-netlist', lambda r,s: s[0]['model'].update(netlist_sha256='0'*64))
    reject('wrong-simulator', lambda r,s: s[0]['model'].update(binary_sha256='0'*64))
    reject('wrong-parameters', lambda r,s: s[0]['model']['parameters'].update(UART_TICKS=s[0]['model']['parameters']['UART_TICKS']+1))
    reject('wrong-source', lambda r,s: s[0]['model']['inputs'].update({'rtl/wasmetal_core.sv':'0'*64}))
    reject('wrong-checker', lambda r,s: s[0]['inputs'].update({'tools/check_loadable.py':'0'*64}))
    require(verify_simulator(args.native_simulator) == native and verify_simulator(args.mapped_simulator) == mapped,
            'simulator identity changed during aggregation')
    for name, value in inputs.items():
        require(digest(ROOT/name) == value, 'aggregation input changed: '+name)
    result = {'status': 'passed', 'scope': 'all 35 bounded programmable integration cases; not the official host-backed corpus',
              'inputs': inputs, 'models': {'rtl': native, 'mapped': mapped}, 'checker_inputs': reference['inputs'],
              'shared_model_inputs': shared, 'parameters': mapped['parameters'],
              'native_parse_only_sources': {k:v for k,v in native['inputs'].items() if k in NATIVE_PARSE_ONLY and k not in mapped['inputs']},
              'case_count': len(cases), 'cases': cases, 'uart_and_cycles_identical': True,
              'netlist_sha256': mapped['netlist_sha256'], 'negative_controls_rejected': len(controls),
              'negative_controls': controls, 'elapsed_seconds': time.monotonic()-started,
              'physical_hardware_tested': False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print('PASS', len(cases), 'complete Xilinx system cases and', len(controls), 'comparison faults')


if __name__ == '__main__':
    main()
