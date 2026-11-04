"""Process lifecycle and metadata checks; these fixtures do not execute a CPU."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import time
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from run_xc7_system import check_destinations, check_shard, require_artifact_path, run_workers
import xc7_system_test as comparison_fixture


class CampaignTests(unittest.TestCase):
    def test_worker_concurrency_and_complete_callbacks(self):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw);script=root/'worker.py'
            script.write_text('''import json,sys,time
from pathlib import Path
p=Path(sys.argv[1]);start=time.monotonic();time.sleep(0.2)
p.write_text(json.dumps([start,time.monotonic()]))
print('worker finished')
''')
            commands=[[sys.executable,str(script),str(root/f'{i}.json')] for i in range(4)]
            callbacks=[];done=run_workers(commands,range(4),root/'logs',2,callbacks.append)
            self.assertEqual(set(done),set(range(4)));self.assertEqual(callbacks,done)
            events=[]
            for i in range(4):
                start,end=json.loads((root/f'{i}.json').read_text());events.extend([(start,1),(end,-1)])
            active=maximum=0
            for _,change in sorted(events):active+=change;maximum=max(maximum,active)
            self.assertEqual(maximum,2)

    def fail_with_child(self, callback_failure):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw);script=root/'worker.py'
            script.write_text('''import subprocess,sys,time
from pathlib import Path
root=Path(sys.argv[1]);index=int(sys.argv[2])
if index==1:
 child=subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)'])
 (root/'child.pid').write_text(str(child.pid))
 time.sleep(60)
else:
 deadline=time.monotonic()+5
 while not (root/'child.pid').exists():
  if time.monotonic()>deadline:raise RuntimeError('child did not start')
  time.sleep(0.01)
 sys.exit(int(sys.argv[3]))
''')
            commands=[[sys.executable,str(script),str(root),str(i),'0' if callback_failure else '7'] for i in range(2)]
            started=time.monotonic()
            def completed(index):
                if callback_failure:raise ValueError('injected receipt failure')
            with self.assertRaisesRegex(ValueError,'injected receipt failure' if callback_failure else 'exited 7'):
                run_workers(commands,range(2),root/'logs',2,completed)
            self.assertLess(time.monotonic()-started,10)
            child=int((root/'child.pid').read_text());stat=Path('/proc')/str(child)/'stat'
            deadline=time.monotonic()+2
            while stat.exists() and stat.read_text().split(') ',1)[1][0]!='Z' and time.monotonic()<deadline:
                time.sleep(0.02)
            self.assertTrue(not stat.exists() or stat.read_text().split(') ',1)[1][0]=='Z','simulator descendant survived failed campaign')

    def test_nonzero_worker_stops_other_checkers_and_descendants(self):
        self.fail_with_child(False)

    def test_invalid_receipt_stops_other_checkers_and_descendants(self):
        self.fail_with_child(True)

    def test_resume_checks_full_case_content_and_identity(self):
        fixture=comparison_fixture.XilinxSystemComparison();fixture.setUp()
        for i,report in enumerate(fixture.reports):check_shard(report,i,fixture.reference,fixture.mapped)
        mutations=[lambda r:r.update(status='running'),lambda r:r['cases'].pop(),
                   lambda r:r['cases'].reverse(),lambda r:r['model'].update(binary_sha256='0'*64),
                   lambda r:r['inputs'].update({'different':'0'*64}),
                   lambda r:r['cases'][0]['uart'].update(clocks=101),
                   lambda r:r['cases'][0]['result'].update(values=[41])]
        for mutation in mutations:
            report=deepcopy(fixture.reports[0]);mutation(report)
            with self.assertRaises(ValueError):check_shard(report,0,fixture.reference,fixture.mapped)

    def test_output_aliases_and_input_overwrites_are_rejected(self):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw);source=root/'source';source.write_text('input')
            alias=root/'alias';alias.symlink_to(source)
            check_destinations([source],[root/'out1',root/'out2'])
            with self.assertRaisesRegex(ValueError,'verification input'):check_destinations([source],[alias])
            with self.assertRaisesRegex(ValueError,'overlap'):check_destinations([], [source,alias])
            for path in (root/'build/run/plan.json',root/'reports/partitions'):
                require_artifact_path(path,root)
            for path in (root/'rtl/core.sv',root/'README.md',root/'build/../../escaped'):
                with self.assertRaisesRegex(ValueError,'within build/ or reports/'):require_artifact_path(path,root)
            (root/'build').mkdir();(root/'build/linked').symlink_to(root)
            with self.assertRaisesRegex(ValueError,'within build/ or reports/'):
                require_artifact_path(root/'build/linked/README.md',root)


if __name__=='__main__':unittest.main()
