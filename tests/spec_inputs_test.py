"""Exercise actual pinned conversions and deliberate pre/post execution mutations."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
import run_spec
import spec_inputs


class FreshInputs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix='spec-input-fixture-', dir=run_spec.ROOT/'build')
        cls.root = Path(cls.temporary.name)
        cls.addClassCleanup(cls.temporary.cleanup)
        for name in ('.cache/upstream/spec.tar.gz', '.cache/packages/wasm-tools.tar.gz'):
            target = cls.root/name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(run_spec.ROOT/name)
        cls.source_dir = cls.root/'.cache/upstream'/('spec-'+run_spec.LOCK['spec']['revision'])/'test/core'
        shutil.copytree(run_spec.SPEC/'test/core', cls.source_dir)

    def setUp(self):
        self.session = spec_inputs.ConversionSession(self.root, run_spec.LOCK, run_spec.WASM_TOOLS)
        self.source = self.source_dir/'i32.wast'
        self.target = self.session.convert(self.source)

    def module(self):
        record = self.session.verify(self.source)
        return self.target.parent/next(iter(record['identity']['payloads']))

    def test_fresh_conversions_ignore_stale_shared_cache(self):
        cached = self.root/'build/spec/i32/test.json'
        cached.parent.mkdir(parents=True, exist_ok=True)
        cached.write_text('{"commands": []}')
        other = spec_inputs.ConversionSession(self.root, run_spec.LOCK, run_spec.WASM_TOOLS)
        target = other.convert(self.source)
        self.assertNotEqual(target, self.target)
        self.assertNotEqual(target, cached)
        self.assertGreater(len(json.loads(target.read_text())['commands']), 1)
        self.assertEqual(other.verify(self.source)['identity'], self.session.verify(self.source)['identity'])
        self.assertEqual(cached.read_text(), '{"commands": []}')
        other.verify_all()

    def test_expected_value_change_is_rejected(self):
        document = json.loads(self.target.read_text())
        command = next(c for c in document['commands'] if c['type'] == 'assert_return' and c.get('expected'))
        command['expected'][0]['value'] = 'wrong'
        self.target.write_text(json.dumps(document))
        with self.assertRaisesRegex(ValueError, 'JSON changed'):
            self.session.verify(self.source)

    def test_module_change_is_rejected(self):
        module = self.module()
        module.write_bytes(module.read_bytes()+b'wrong')
        with self.assertRaisesRegex(ValueError, 'module changed'):
            self.session.verify(self.source)

    def test_invalid_module_binary_representation_is_bound(self):
        source = self.source_dir/'address.wast'
        target = self.session.convert(source)
        name = next(c['binary_filename'] for c in json.loads(target.read_text())['commands'] if 'binary_filename' in c)
        path = target.parent/name
        path.write_bytes(path.read_bytes()+b'wrong')
        with self.assertRaisesRegex(ValueError, 'module changed'):
            self.session.verify(source)

    def test_missing_payload_is_rejected(self):
        self.module().unlink()
        with self.assertRaisesRegex(ValueError, 'missing or indirect converted payload'):
            self.session.verify(self.source)

    def test_symlink_payload_is_rejected_even_with_matching_bytes(self):
        module = self.module()
        copy = self.session.directory/'copy.wasm'
        copy.write_bytes(module.read_bytes())
        module.unlink()
        module.symlink_to(copy)
        with self.assertRaisesRegex(ValueError, 'missing or indirect converted payload'):
            self.session.verify(self.source)

    def test_conversion_log_change_is_rejected(self):
        entry = self.session.verify(self.source)
        (self.root/entry['conversion_log']).write_text('wrong command')
        with self.assertRaisesRegex(ValueError, 'command receipt changed'):
            self.session.verify(self.source)

    def test_another_script_cannot_be_substituted(self):
        with self.assertRaisesRegex(ValueError, 'substituted another'):
            self.session.verify(self.source, self.session.directory/'other.json')

    def test_changed_source_is_rejected(self):
        original = self.source.read_bytes()
        self.addCleanup(self.source.write_bytes, original)
        self.source.write_bytes(original+b'\n;; changed after conversion\n')
        with self.assertRaisesRegex(ValueError, 'source differs from pinned archive'):
            self.session.verify(self.source)

    def test_changed_converter_is_rejected(self):
        path = self.session.directory/'wrong-converter'
        path.write_bytes(b'not the pinned executable')
        self.session.executable = path
        with self.assertRaisesRegex(ValueError, 'installed converter differs'):
            self.session.verify_all()

    def test_changed_converter_archive_is_rejected(self):
        path = self.session.directory/'wrong-release.tar.gz'
        path.write_bytes(b'not the pinned archive')
        self.session.archive = path
        with self.assertRaisesRegex(ValueError, 'archive checksum mismatch'):
            self.session.verify_all()

    def test_bad_input_is_rejected_before_execution(self):
        self.module().write_bytes(b'changed')
        with patch.object(run_spec, 'conversion_session', return_value=self.session), patch.object(run_spec, 'run_file') as execute:
            with self.assertRaisesRegex(ValueError, 'module changed'):
                run_spec.run_with_verified_inputs(self.source, self.target, None)
            execute.assert_not_called()

    def test_input_changed_during_execution_cannot_pass(self):
        module = self.module()
        def execute(*unused):
            module.write_bytes(module.read_bytes()+b'changed during execution')
            return {'failures': []}
        with patch.object(run_spec, 'conversion_session', return_value=self.session), patch.object(run_spec, 'run_file', side_effect=execute):
            with self.assertRaisesRegex(ValueError, 'module changed'):
                run_spec.run_with_verified_inputs(self.source, self.target, None)

    def test_execution_receipt_contains_both_checks(self):
        with patch.object(run_spec, 'conversion_session', return_value=self.session), patch.object(run_spec, 'run_file', return_value={'failures': []}):
            result = run_spec.run_with_verified_inputs(self.source, self.target, None)
        expected = self.session.verify(self.source)['identity']
        spec_inputs.checked_evidence(result, expected)
        for flag in ('verified_before_execution', 'verified_after_execution'):
            for value in (False, None, 'true', 1):
                altered = deepcopy(result)
                altered['test_inputs'][flag] = value
                with self.subTest(flag=flag, value=value), self.assertRaisesRegex(ValueError, 'verified around execution'):
                    spec_inputs.checked_evidence(altered, expected)

    def test_spectest_cache_must_match_fresh_conversion(self):
        root = self.session.directory/'spectest-root'
        (root/'build').mkdir(parents=True)
        (root/'build/spectest.wasm').write_bytes(b'corrupted fixture')
        (root/'.cache/packages').mkdir(parents=True)
        (root/'.cache/packages/wasm-tools.tar.gz').symlink_to(run_spec.ROOT/'.cache/packages/wasm-tools.tar.gz')
        with patch.object(run_spec, 'ROOT', root), patch.object(run_spec, '_spectest_bytes', None):
            with self.assertRaisesRegex(run_spec.ExecutionError, 'differs from trusted conversion'):
                run_spec.prepare_spectest()


if __name__ == '__main__':
    unittest.main()
