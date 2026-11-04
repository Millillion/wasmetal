"""Missing tests, mutable state and mismatched models must never yield a CI pass."""
from collections import Counter
from copy import deepcopy
from contextlib import redirect_stderr
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import run_spec
import spec_ci
import spec_shards
import build_identity
from wasm_image import Module


class PartitionSafety(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.fixture_path = run_spec.prepare_spectest()
        self.fixture = Module(self.fixture_path.read_bytes())

    def module(self, wat):
        path = self.directory/'module.wasm'
        subprocess.run([str(run_spec.WASM_TOOLS),'parse','-o',str(path)],input=wat,text=True,check=True,capture_output=True)
        return Module(path.read_bytes())

    def test_immutable_state_is_allowed(self):
        for wat in ['(module (func (param i32) (result i32) local.get 0))',
                    '(module (global i32 (i32.const 4)) (func (result i32) global.get 0))',
                    '(module (table 2 funcref) (func (result funcref) i32.const 0 table.get))',
                    '(module (import "spectest" "print_i32_f32" (func (param i32 f32))))']:
            with self.subTest(wat=wat):
                spec_shards.independent_module(self.module(wat),self.fixture)

    def test_state_and_unknown_imports_are_rejected(self):
        for wat in ['(module (global (mut i32) (i32.const 0)))',
                    '(module (memory 1))',
                    '(module (func $start) (start $start))',
                    '(module (import "env" "random" (func (result i32))))',
                    '(module (table 2 funcref) (func i32.const 0 ref.null func table.set))',
                    '(module (type $a (array i32)) (func (result (ref $a)) i32.const 1 array.new_default $a))']:
            with self.subTest(wat=wat), self.assertRaises(ValueError):
                spec_shards.independent_module(self.module(wat),self.fixture)

    def test_nonlocal_and_stateful_script_commands_are_rejected(self):
        for command in [{'type':'register','as':'foo'},
                        {'type':'assert_return','action':{'type':'get','field':'g','args':[]}},
                        {'type':'assert_return','action':{'type':'invoke','module':'earlier','args':[]}},
                        {'type':'assert_return','action':{'type':'invoke','args':[{'type':'externref','value':'0'}]}}]:
            with self.subTest(command=command), self.assertRaises(ValueError):
                spec_shards.independent_script('return_call.wast',self.directory/'test.json',[command],self.fixture_path)


class CompleteCoverage(PartitionSafety):
    def setUp(self):
        super().setUp()
        self.module('(module (func (export "f") (result i32) i32.const 7))')
        module = {'type':'module','filename':'module.wasm'}
        assertion = {'type':'assert_return','action':{'type':'invoke','field':'f','args':[]}}
        self.entries = {'return_call.wast':(self.directory/'test.json',[module,assertion,module,assertion]),
                        'i32.wast':(self.directory/'test.json',[module,assertion])}
        self.per_command = {'return_call.wast':[{'modules_instantiated':1},{'rtl_assertions_passed':1},
                                               {'modules_instantiated':1},{'rtl_assertions_passed':1}],
                            'i32.wast':[{'modules_instantiated':1},{'rtl_assertions_passed':1}]}
        suites = []
        totals = Counter()
        for name,cycles in [('return_call.wast',[50,100,3,200]),('i32.wast',[50,22])]:
            counts = Counter({'script_commands':len(cycles),'rtl_cycles':sum(cycles)})
            for c in self.per_command[name]:
                counts.update(c)
            totals.update(counts)
            suites.append({'suite':name,'counts':dict(counts),'command_count':len(cycles),'command_cycles':cycles,
                           'executed_commands':list(range(len(cycles))),'replayed_setup_commands':[],
                           'fixture_cycles':48,'replayed_setup_cycles':0,'total_simulated_cycles':sum(cycles),'failures':[]})
        self.reference = {'spec':run_spec.LOCK['spec'],'official_sources_sha256':'sources','runner_inputs':{'runner':'hash'},
                          'rtl_build_id':'rtl','capacities':{'value':8192},'memory_wait_states':3,
                          'max_cycles_per_invocation':300000000,'source_sha256':'tree','identity_error':None,
                          'simulator_sha256':'native','build_manifest':{'inputs':{'rtl':'hash'},'binary_sha256':'native'},
                          'full_core_suite_selected':True,'full_core_suite_passed':True,'suite_files':2,
                          'totals':dict(totals),'suites':suites,'response_timeout_seconds':3600}
        self.plan = spec_ci.create_plan(self.reference,'reference','sources',self.entries,2)
        self.reports = []
        native = {s['suite']:s for s in suites}
        for shard in self.plan['shards']:
            report = deepcopy(self.reference)
            report.update(shard_id=shard['id'],shard_plan_sha256='plan',full_core_suite_selected=False,
                          full_core_suite_passed=False,simulator_sha256='mapped',suites=[])
            report['build_manifest'].update(backend='mapped-ecp5-functional',binary_sha256='mapped')
            totals = Counter()
            for entry in shard['entries']:
                name = entry['suite']
                suite = deepcopy(native[name])
                selected = entry['commands'] if entry['commands'] is not None else list(range(suite['command_count']))
                suite['executed_commands'] = selected
                suite['command_cycles'] = [c if i in selected else None for i,c in enumerate(suite['command_cycles'])]
                counts = Counter({'script_commands':len(selected),'rtl_cycles':sum(c for c in suite['command_cycles'] if c is not None)})
                for index in selected:
                    counts.update(self.per_command[name][index])
                suite['counts'] = dict(counts)
                replayed = [i for i,c in enumerate(self.entries[name][1]) if i not in selected and c['type']=='module']
                suite['replayed_setup_commands'] = replayed
                suite['replayed_setup_cycles'] = sum(native[name]['command_cycles'][i]-(48 if i==0 else 0) for i in replayed)+(48 if 0 not in selected else 0)
                suite['total_simulated_cycles'] = counts['rtl_cycles'] + suite['replayed_setup_cycles']
                report['suites'].append(suite)
                totals.update(counts)
            report.update(suite_files=len(report['suites']),totals=dict(totals))
            self.reports.append(report)

    def merge(self, reports=None, plan=None):
        return spec_ci.merge_reports(plan or self.plan,'plan',self.reference,'reference',
                                     self.reports if reports is None else reports,'sources',self.entries)

    def test_complete_partition_matches_native_counts_and_cycles(self):
        result = self.merge()
        self.assertTrue(result['full_core_suite_passed'])
        self.assertEqual(result['totals'],self.reference['totals'])
        self.assertEqual(result['suite_files'],2)

    def test_xilinx_requires_explicit_family_and_rejects_mixed_models(self):
        reports = deepcopy(self.reports)
        for report in reports:report['build_manifest']['backend'] = 'mapped-xc7-functional'
        with self.assertRaisesRegex(ValueError,'selected mapped CPU'):self.merge(reports)
        result = spec_ci.merge_reports(self.plan,'plan',self.reference,'reference',reports,
                                      'sources',self.entries,expected_backend='mapped-xc7-functional')
        self.assertTrue(result['full_core_suite_passed'])
        self.assertEqual(result['totals'],self.reference['totals'])
        reports[-1]['build_manifest']['backend'] = 'mapped-ecp5-functional'
        with self.assertRaisesRegex(ValueError,'selected mapped CPU'):
            spec_ci.merge_reports(self.plan,'plan',self.reference,'reference',reports,
                                  'sources',self.entries,expected_backend='mapped-xc7-functional')
        with self.assertRaisesRegex(ValueError,'unreviewed mapped backend'):
            spec_ci.merge_reports(self.plan,'plan',self.reference,'reference',reports,
                                  'sources',self.entries,expected_backend='native')

    def test_missing_and_duplicate_shards_fail(self):
        for reports in [[],self.reports[:1],[self.reports[0],self.reports[0]]]:
            with self.subTest(count=len(reports)), self.assertRaises(ValueError):
                self.merge(reports)

    def test_plan_cannot_omit_duplicate_or_reorder_commands(self):
        for mutation in ['omit','duplicate','reorder','sources','unreviewed']:
            plan = deepcopy(self.plan)
            entry = next(e for s in plan['shards'] for e in s['entries'] if e['commands'] is not None and len(e['commands'])>1)
            if mutation=='omit': entry['commands'].pop()
            elif mutation=='duplicate': entry['commands'].append(entry['commands'][0])
            elif mutation=='reorder': entry['commands'].reverse()
            elif mutation=='sources': plan['official_sources_sha256']='different'
            else:
                next(e for s in plan['shards'] for e in s['entries'] if e['suite']=='i32.wast')['commands']=[0,1]
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.merge(plan=plan)

    def test_false_success_evidence_is_rejected(self):
        def mismatch(key,value):
            return lambda r:r[0].__setitem__(key,value)
        changes = {
            'plan':mismatch('shard_plan_sha256','wrong'),
            'identity':mismatch('identity_error','stale executable'),
            'source':mismatch('official_sources_sha256','wrong'),
            'runner':mismatch('runner_inputs',{}),
            'binary':mismatch('simulator_sha256','wrong'),
            'partial':mismatch('full_core_suite_passed',True),
            'backend':lambda r:r[0]['build_manifest'].pop('backend'),
            'counts':lambda r:r[0]['totals'].__setitem__('rtl_assertions_passed',999),
            'errors':lambda r:r[0]['totals'].__setitem__('runner_errors',1),
            'omitted-command':lambda r:r[0]['suites'][0]['executed_commands'].pop(),
            'setup':lambda r:r[0]['suites'][0].__setitem__('replayed_setup_cycles',999),
            'cycle':lambda r:r[0]['suites'][0]['command_cycles'].__setitem__(0,999),
        }
        for label,change in changes.items():
            reports = deepcopy(self.reports)
            change(reports)
            with self.subTest(label=label), self.assertRaises(ValueError):
                self.merge(reports)


class WorkspaceReconciliation(unittest.TestCase):
    """Use real files and identity verification; only the workspace is isolated."""
    def setUp(self):
        fixture = CompleteCoverage('test_complete_partition_matches_native_counts_and_cycles')
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.fixture = fixture
        self.root = fixture.directory/'identity-fixture'
        names = ['Makefile', 'tools/upstream.lock.json', 'tools/generate_fpga_ports.py',
                 'tools/build_identity.py', 'tools/spec_ci.py', 'rtl/tiny.sv', 'sim/tiny.cpp',
                 'tools/run_spec.py', 'tools/wasm_image.py', 'tools/spec_shards.py',
                 'build/spectest.wasm', 'build/circuit.v', 'build/native', 'build/mapped']
        for name in names:
            path = self.root/name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('identity-check fixture: '+name+'\n')
        for module in (spec_ci, build_identity):
            change = patch.object(module, 'ROOT', self.root)
            change.start()
            self.addCleanup(change.stop)
        self.models = {name: self.root/'build'/name for name in ('native', 'mapped')}
        manifests = {}
        for name, binary in self.models.items():
            build_identity.begin(binary, 'native')
            snapshot = Path(str(binary)+'.inputs.json')
            value = json.loads(snapshot.read_text())
            if name == 'mapped':
                value.update(backend='mapped-ecp5-functional',
                             extra_inputs={'build/circuit.v': spec_shards.sha256(self.root/'build/circuit.v')})
                snapshot.write_text(json.dumps(value))
            build_identity.finish(binary)
            manifests[name] = build_identity.verify(binary)
        fixture.reference.update(build_manifest=manifests['native'],
            simulator_sha256=manifests['native']['binary_sha256'], source_sha256='1'*64,
            runner_inputs={name: spec_shards.sha256(self.root/name) for name in
                ('tools/run_spec.py', 'tools/wasm_image.py', 'tools/spec_shards.py', 'build/spectest.wasm')})
        for row in fixture.reports:
            row.update(build_manifest=deepcopy(manifests['mapped']),
                       simulator_sha256=manifests['mapped']['binary_sha256'],
                       runner_inputs=deepcopy(fixture.reference['runner_inputs']), source_sha256='2'*64)

    def merge(self):
        f = self.fixture
        return spec_ci.merge_reports(f.plan, 'plan', f.reference, 'reference', f.reports,
                                     'sources', f.entries, execution_models=self.models)

    def test_unrelated_tools_do_not_change_execution_identity(self):
        with self.assertRaisesRegex(ValueError, 'source_sha256'):
            self.fixture.merge()
        first = self.merge()
        (self.root/'tools/unrelated.py').write_text('unrelated tool added during simulation\n')
        self.assertEqual(first, self.merge())
        self.assertIsNone(first['source_sha256'])
        snapshots = first['workspace_reconciliation']['reported_workspace_sha256']
        self.assertEqual(snapshots['native'], '1'*64)
        self.assertEqual(set(snapshots['mapped_shards'].values()), {'2'*64})

    def test_changed_dependency_or_executable_is_rejected(self):
        for name in ['rtl/tiny.sv', 'sim/tiny.cpp', 'tools/run_spec.py', 'tools/wasm_image.py',
                     'build/spectest.wasm', 'build/circuit.v', 'build/native', 'build/mapped']:
            path = self.root/name
            original = path.read_bytes()
            try:
                path.write_bytes(original+b'deliberate corruption\n')
                with self.subTest(name=name), self.assertRaises((ValueError, RuntimeError)):
                    self.merge()
            finally:
                path.write_bytes(original)
        self.assertTrue(self.merge()['full_core_suite_passed'])

    def test_new_rtl_source_is_rejected(self):
        (self.root/'rtl/new.sv').write_text('new RTL input\n')
        with self.assertRaisesRegex(RuntimeError, 'stale'):
            self.merge()

    def test_substituted_executable_is_rejected(self):
        self.models['native'] = self.models['mapped']
        with self.assertRaisesRegex(ValueError, 'native executable differs'):
            self.merge()

    def test_missing_runner_dependency_is_rejected(self):
        self.fixture.reference['runner_inputs'].pop('tools/wasm_image.py')
        with self.assertRaisesRegex(ValueError, 'runner input inventory'):
            self.merge()

    def test_failed_cli_merge_removes_previous_success(self):
        output = self.root/'previous.json'
        output.write_text('{"full_core_suite_passed": true}\n')
        argv = ['spec_ci.py', 'merge', '--reference', str(self.root/'reference.json'),
                '--plan', str(self.root/'plan.json'), '--reports', str(self.root/'reports'),
                '--output', str(output)]
        with patch.object(sys, 'argv', argv), patch.object(spec_ci, 'catalog', side_effect=ValueError('catalog failed')):
            with self.assertRaisesRegex(ValueError, 'catalog failed'):
                spec_ci.main()
        self.assertFalse(output.exists())

    def test_cli_refuses_to_overwrite_input(self):
        reference = self.root/'reference.json'
        reference.write_text('verification input must survive\n')
        argv = ['spec_ci.py', 'merge', '--reference', str(reference),
                '--plan', str(self.root/'plan.json'), '--reports', str(self.root/'reports'),
                '--output', str(reference)]
        with patch.object(sys, 'argv', argv), redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                spec_ci.main()
        self.assertEqual(reference.read_text(), 'verification input must survive\n')


if __name__ == '__main__':
    unittest.main()
