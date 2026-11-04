#!/usr/bin/env python3
"""Compare two original-library 7-series CPU smoke cases with the verified RTL."""
import argparse
from copy import deepcopy
import json
from pathlib import Path

from check_xc7_system import NATIVE_PARSE_ONLY, require, validate_models
from prepare_standalone import ROOT, digest
from standalone_support import verify_simulator


def compare(reference, report, native, mapped):
    shared = validate_models(reference, native, mapped)
    require(report['status'] == 'passed' and report['model'] == mapped, 'mapped smoke identity or status differs')
    require(report['inputs'] == reference['inputs'], 'smoke checker inputs differ')
    names = ['answer', 'program-address-boundaries']
    require([case['name'] for case in report['cases']] == names, 'incomplete or reordered smoke cases')
    expected = {case['name']: case for case in reference['cases']}
    require(len(expected) == len(reference['cases']), 'duplicate native case')
    for case in report['cases']:
        require(case == expected.get(case['name']), 'different smoke UART bytes, clocks, packet or result')
    return shared


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'reports/xc7-smoke-comparison.json')
    args = parser.parse_args()
    native_binary = ROOT/'build/loadable-sim/Vwasmetal_loadable'
    mapped_binary = ROOT/'build/xc7-accelerated-gate-sim/obj/Vwasmetal_loadable'
    reference_path = ROOT/'reports/loadable-rtl.json'
    mapped_path = ROOT/'reports/xc7-accelerated-mapped-smoke.json'
    consumed = [reference_path, mapped_path, Path(__file__).resolve(), ROOT/'tools/check_xc7_system.py',
                ROOT/'tools/loadable_ci.py', ROOT/'tools/standalone_support.py',
                ROOT/'tools/prepare_standalone.py', ROOT/'tools/program_upload.py']
    protected = [*consumed, native_binary, mapped_binary,
                 Path(str(native_binary)+'.build.json'), Path(str(mapped_binary)+'.build.json')]
    if args.output.resolve() in {path.resolve() for path in protected}:
        parser.error('output must not overwrite a verification input')
    args.output.unlink(missing_ok=True)
    inputs = {str(p.relative_to(ROOT)): digest(p) for p in consumed}
    native = verify_simulator(native_binary); mapped = verify_simulator(mapped_binary)
    require(not mapped.get('model_options', {}).get('fast_luts'), 'smoke receipt must cover original LUT models')
    reference = json.loads(reference_path.read_text()); report = json.loads(mapped_path.read_text())
    shared = compare(reference, report, native, mapped)
    for name, value in reference['inputs'].items():
        path = Path(name)
        require(not path.is_absolute() and '..' not in path.parts and digest(ROOT/path) == value,
                'checker input changed: '+name)
        require(name not in inputs or inputs[name] == value, 'conflicting checker identity')
        inputs[name] = value
    controls = []

    def reject(name, change):
        wrong = deepcopy(report); change(wrong)
        try:
            compare(reference, wrong, native, mapped)
        except ValueError as error:
            controls.append({'name':name, 'rejected':True, 'reason':str(error)})
        else:
            raise ValueError('accepted smoke comparison fault: '+name)

    reject('missing-case', lambda r: r['cases'].pop())
    reject('reordered-cases', lambda r: r['cases'].reverse())
    reject('unfinished-run', lambda r: r.update(status='running'))
    reject('wrong-binary', lambda r: r['model'].update(binary_sha256='0'*64))
    reject('wrong-clock', lambda r: r['cases'][0]['uart'].update(clocks=r['cases'][0]['uart']['clocks']+1))
    reject('wrong-packet', lambda r: r['cases'][0].update(packet_sha256='0'*64))
    reject('wrong-result', lambda r: r['cases'][0]['result']['values'].__setitem__(0,41))
    reject('wrong-checker', lambda r: r['inputs'].update({'tools/check_loadable.py':'0'*64}))
    require(verify_simulator(native_binary) == native and verify_simulator(mapped_binary) == mapped,
            'simulator changed during comparison')
    for name, value in inputs.items():
        require(digest(ROOT/name) == value, 'comparison input changed: '+name)
    result = {'status':'passed', 'scope':'two complete programmable CPU smoke cases with original LUT library models',
              'models':{'rtl':native,'mapped':mapped}, 'inputs':inputs, 'shared_model_inputs':shared,
              'native_parse_only_sources':{k:v for k,v in native['inputs'].items() if k in NATIVE_PARSE_ONLY and k not in mapped['inputs']},
              'case_count':len(report['cases']), 'cases':report['cases'], 'uart_and_cycles_identical':True,
              'negative_controls_rejected':len(controls), 'negative_controls':controls,
              'full_35_case_regression_passed':False, 'physical_hardware_tested':False}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS two original-library CPU smoke cases and eight comparison faults')


if __name__ == '__main__':
    main()
