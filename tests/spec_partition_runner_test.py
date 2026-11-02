"""Exercise command ownership and setup replay on an actual RTL simulator."""
from collections import Counter
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import run_spec


class RunnerPartition(unittest.TestCase):
    def test_real_execution_matches_an_intact_script(self):
        simulator = Path(os.environ.get('WASMETAL_TEST_SIMULATOR',str(run_spec.ROOT/'build/obj/Vwasmetal_core'))).resolve()
        run_spec.prepare_spectest()
        with tempfile.TemporaryDirectory() as directory:
            spec = Path(directory)
            source = spec/'test/core/return_call.wast'
            source.parent.mkdir(parents=True)
            # Synthetic fixture, separate from the checksum-pinned official tree.
            source.write_text('''
                (module
                  (global $g i32 (i32.const 7))
                  (func (export "f") (param i32) (result i32)
                    local.get 0 global.get $g i32.add))
                (assert_return (invoke "f" (i32.const 1)) (i32.const 8))
                (assert_return (invoke "f" (i32.const 2)) (i32.const 9))
                (module
                  (table 1 funcref)
                  (func $g (result i32) i32.const 42)
                  (elem (i32.const 0) func $g)
                  (func (export "g") (result i32)
                    i32.const 0 call_indirect (result i32))
                  (func (export "trap") unreachable))
                (assert_return (invoke "g") (i32.const 42))
                (assert_trap (invoke "trap") "unreachable")
            ''')
            target = spec/'test.json'
            subprocess.run([str(run_spec.WASM_TOOLS),'json-from-wast',str(source),
                            '--wasm-dir',str(spec),'-o',str(target)],check=True,capture_output=True)
            self.assertEqual(len(json.loads(target.read_text())['commands']),6)
            reports = []
            for selected in [None,[0,2,5],[1,3,4]]:
                args = SimpleNamespace(wait_states=3,max_cycles=300000000,simulator=simulator,
                                       response_timeout=60,verbose=False,
                                       command_partitions={} if selected is None else {'return_call.wast':selected})
                with patch.object(run_spec,'SPEC',spec):
                    report = run_spec.run_file(source,target,args)
                self.assertEqual(report['failures'],[])
                self.assertEqual(report['executed_commands'],list(range(6)) if selected is None else selected)
                reports.append(report)
            whole,first,second = reports
            combined = Counter(first['counts']);combined.update(second['counts'])
            self.assertEqual(dict(combined),whole['counts'])
            self.assertEqual(whole['counts']['rtl_assertions_passed'],4)
            self.assertEqual(whole['counts']['modules_instantiated'],2)
            self.assertEqual(first['replayed_setup_commands'],[3])
            self.assertEqual(second['replayed_setup_commands'],[0])
            self.assertGreater(second['replayed_setup_cycles'],second['fixture_cycles'])
            trace = [None]*6
            for part in [first,second]:
                self.assertEqual(part['total_simulated_cycles'],part['counts']['rtl_cycles']+part['replayed_setup_cycles'])
                for i in part['executed_commands']:
                    self.assertIsNone(trace[i])
                    trace[i] = part['command_cycles'][i]
            self.assertEqual(trace,whole['command_cycles'])


if __name__ == '__main__':
    unittest.main()
