"""Check reconciliation output protection; fixture executables are never run."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import build_identity
from check_spec_reconciliation import protect_outputs
from spec_shards import sha256


class OutputProtection(unittest.TestCase):
    def test_distinct_artifacts_are_allowed(self):
        protect_outputs([ROOT/'reports/input.json'],[ROOT/'reports/output.json',ROOT/'build/aggregate.json'])

    def test_aliases_and_source_destinations_are_rejected(self):
        source=ROOT/'reports/input.json'
        for outputs in ([source],[ROOT/'reports/a.json',ROOT/'reports/a.json'],[ROOT/'tools/new.py']):
            with self.subTest(outputs=outputs),self.assertRaises(ValueError):
                protect_outputs([source],outputs)

    def run_cli_control(self,mode):
        (ROOT/'build').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='reconciliation-output-',dir=ROOT/'build') as name:
            directory=Path(name);reference=directory/'reference.json';plan=directory/'plan.json'
            canary=directory/'transitive-input.json';output=directory/'output.json'
            aggregate=directory/'aggregate.json';binary=directory/'fixture-model'
            for path in (reference,plan,canary,output,aggregate):path.write_text('{"preserve": true}\n')
            binary.write_bytes(b'Nonexecutable identity fixture; never run.\n')
            build_identity.begin(binary,'native')
            snapshot_path=Path(str(binary)+'.inputs.json')
            snapshot=json.loads(snapshot_path.read_text())
            snapshot['extra_inputs']={str(canary.relative_to(ROOT)):sha256(canary)}
            snapshot_path.write_text(json.dumps(snapshot)+'\n')
            build_identity.finish(binary)
            if mode=='direct':output=reference
            elif mode=='transitive':output=canary
            elif mode=='overlap':aggregate=output
            before={p:p.read_bytes() for p in (reference,plan,canary,output,aggregate,binary)}
            run=subprocess.run([sys.executable,str(ROOT/'tools/check_spec_reconciliation.py'),
                '--reference',str(reference),'--plan',str(plan),'--reports',str(directory),
                '--native-simulator',str(binary),'--mapped-simulator',str(binary),
                '--mapped-backend','mapped-xc7-functional','--output',str(output),'--aggregate',str(aggregate)],
                cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=30)
            self.assertEqual(run.returncode,2,run.stdout)
            self.assertIn('reconciliation outputs overlap' if mode=='overlap' else
                          'reconciliation output would overwrite an input',run.stdout)
            for path,content in before.items():self.assertEqual(path.read_bytes(),content)

    def test_cli_preserves_direct_input(self):self.run_cli_control('direct')

    def test_cli_preserves_transitive_model_input(self):self.run_cli_control('transitive')

    def test_cli_preserves_overlapping_outputs(self):self.run_cli_control('overlap')


if __name__=='__main__':unittest.main()
