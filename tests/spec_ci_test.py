"""Missing tests, mutable state and mismatched models must never yield a CI pass."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import run_spec
import spec_ci
import spec_shards
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


if __name__ == '__main__':
    unittest.main()
