"""Comparison-metadata fixtures; these tests do not execute a CPU model."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
from check_xc7_system import NATIVE_PARSE_ONLY, compare
from loadable_ci import GROUPS, RECOVERY
from prepare_standalone import load_profile
from program_upload import profile_tag
from standalone_support import parameters


class XilinxSystemComparison(unittest.TestCase):
    def setUp(self):
        profile = load_profile(); tag = profile_tag(profile)
        self.native = {'backend': 'loadable-rtl', 'profile': profile, 'profile_tag': tag.hex(),
                       'uart_ticks': 4, 'clock_scale': 1, 'upload_timeout': 4096,
                       'binary_sha256': '1'*64,
                       'inputs': {'rtl/core.sv': '2'*64, 'soc/profile.json': '3'*64}}
        params = parameters(profile)
        params.update(UART_TICKS=4, UPLOAD_TIMEOUT_CYCLES=4096, PROFILE_TAG=f"128'h{int.from_bytes(tag,'little'):032x}")
        self.mapped = deepcopy(self.native)
        self.mapped.update(backend='loadable-mapped-xc7-functional', top='wasmetal_loadable',
                           parameters=params, binary_sha256='4'*64, netlist_sha256='5'*64)
        self.mapped['inputs']['build/xc7/mapped.json'] = '5'*64
        cases = {name: {'name': name, 'packet_sha256': '6'*64,
                        'uart': {'clocks': 100, 'uart': '1234'}, 'result': {'values': [42]}}
                 for name in [*[n for group in GROUPS for n in group], *RECOVERY]}
        checker = {'tools/check_loadable.py': '7'*64}
        self.reference = {'status': 'passed', 'model': deepcopy(self.native),
                          'inputs': checker, 'cases': list(cases.values())}
        self.reports = [{'status': 'passed', 'model': deepcopy(self.mapped), 'inputs': checker,
                         'cases': [deepcopy(cases[n]) for n in group+(RECOVERY if i==0 else [])]}
                        for i,group in enumerate(GROUPS)]

    def test_complete_comparison_preserves_every_case(self):
        cases, shared = compare(self.reference, self.reports, self.native, self.mapped)
        self.assertEqual(len(cases), 35)
        self.assertEqual({c['name'] for c in cases}, {c['name'] for c in self.reference['cases']})
        self.assertEqual(shared, self.native['inputs'])

    def test_coverage_results_and_identity_faults_are_rejected(self):
        mutations = {
            'missing-shard': lambda r,s: s.pop(),
            'duplicate-shard': lambda r,s: s.__setitem__(-1,deepcopy(s[0])),
            'missing-case': lambda r,s: s[0]['cases'].pop(),
            'reordered-case': lambda r,s: s[0]['cases'].reverse(),
            'running': lambda r,s: s[0].update(status='running'),
            'wrong-clock': lambda r,s: s[0]['cases'][0]['uart'].update(clocks=101),
            'wrong-uart': lambda r,s: s[0]['cases'][0]['uart'].update(uart='1235'),
            'wrong-value': lambda r,s: s[0]['cases'][0]['result'].update(values=[41]),
            'wrong-packet': lambda r,s: s[0]['cases'][0].update(packet_sha256='8'*64),
            'wrong-model': lambda r,s: s[0].update(model=deepcopy(self.native)),
            'wrong-binary': lambda r,s: s[0]['model'].update(binary_sha256='8'*64),
            'wrong-checker': lambda r,s: s[0].update(inputs={'different':'8'*64}),
            'incomplete-reference': lambda r,s: r['cases'].pop(),
            'failed-reference': lambda r,s: r.update(status='failed'),
        }
        for name, mutation in mutations.items():
            reference, reports = deepcopy((self.reference,self.reports)); mutation(reference,reports)
            with self.subTest(name=name), self.assertRaises(ValueError):
                compare(reference,reports,self.native,self.mapped)

    def test_consistent_model_metadata_cannot_hide_wrong_parameters_or_source(self):
        for field in ('UART_TICKS','UPLOAD_TIMEOUT_CYCLES','VALUE_DEPTH'):
            mapped = deepcopy(self.mapped); mapped['parameters'][field] += 1
            reports = deepcopy(self.reports)
            for report in reports: report['model'] = deepcopy(mapped)
            with self.subTest(field=field), self.assertRaisesRegex(ValueError,'elaboration parameters'):
                compare(self.reference,reports,self.native,mapped)
        mapped = deepcopy(self.mapped); mapped['inputs']['rtl/core.sv'] = '8'*64
        reports = deepcopy(self.reports)
        for report in reports: report['model'] = deepcopy(mapped)
        with self.assertRaisesRegex(ValueError,'different RTL'):
            compare(self.reference,reports,self.native,mapped)

    def test_circuit_binding_cannot_be_omitted(self):
        mapped = deepcopy(self.mapped); mapped['inputs'].pop('build/xc7/mapped.json')
        reports = deepcopy(self.reports)
        for report in reports: report['model'] = deepcopy(mapped)
        with self.assertRaisesRegex(ValueError,'synthesized circuit identity'):
            compare(self.reference,reports,self.native,mapped)

    def test_only_known_unused_native_modules_may_be_absent(self):
        native, reference = deepcopy((self.native,self.reference))
        for name in NATIVE_PARSE_ONLY: native['inputs'][name] = '9'*64
        reference['model'] = deepcopy(native)
        cases, shared = compare(reference,self.reports,native,self.mapped)
        self.assertEqual(len(cases),35)
        self.assertTrue(set(shared).isdisjoint(NATIVE_PARSE_ONLY))
        native['inputs']['soc/new_runtime.sv'] = '9'*64
        reference['model'] = deepcopy(native)
        with self.assertRaisesRegex(ValueError,'different RTL'):
            compare(reference,self.reports,native,self.mapped)

    def test_extra_mapped_source_requires_native_identity(self):
        mapped, reports = deepcopy((self.mapped,self.reports))
        mapped['inputs']['soc/new_runtime.sv'] = '9'*64
        for report in reports:report['model'] = deepcopy(mapped)
        with self.assertRaisesRegex(ValueError,'absent from native'):
            compare(self.reference,reports,self.native,mapped)


if __name__ == '__main__':
    unittest.main()
