#!/usr/bin/env python3
"""Reject incomplete or altered upstream standard-cell source inventories."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'tools'))
import check_asic_cell_models as models


class CellSources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lock = json.loads(models.LOCK.read_text())
        if not all((models.CACHE / r['path']).exists() for r in cls.lock['files']):
            raise ValueError('Run tools/check_asic_cell_models.py to populate the verified source cache first')

    def validate(self, data):
        with tempfile.TemporaryDirectory(prefix='wasmetal-asic-cell-lock-') as directory:
            path = Path(directory) / 'lock.json'
            path.write_text(json.dumps(data))
            with mock.patch.object(models, 'LOCK', path), mock.patch.object(
                    models.urllib.request, 'urlopen', side_effect=AssertionError('unexpected network request')):
                return models.upstream()

    def test_complete_inventory(self):
        self.assertEqual(self.validate(self.lock), self.lock)

    def test_missing_cell_source(self):
        data = deepcopy(self.lock)
        data['files'] = [r for r in data['files'] if r['path'] != next(
            r['path'] for r in self.lock['files'] if r['path'].startswith('cells/'))]
        with self.assertRaisesRegex(ValueError, 'source/license inventory'):
            self.validate(data)

    def test_unbound_cell_type(self):
        data = deepcopy(self.lock)
        data['cell_types'] = sorted(data['cell_types'] + ['sky130_fd_sc_hd__dfxtp_2'])
        with self.assertRaisesRegex(ValueError, 'source/license inventory'):
            self.validate(data)

    def test_duplicate_source(self):
        data = deepcopy(self.lock)
        data['files'].append(deepcopy(data['files'][0]))
        with self.assertRaisesRegex(ValueError, 'duplicate upstream model file'):
            self.validate(data)

    def test_missing_transitive_primitive(self):
        data = deepcopy(self.lock)
        data['files'] = [r for r in data['files'] if r['path'] !=
                         'models/udp_mux_2to1/sky130_fd_sc_hd__udp_mux_2to1.v']
        with self.assertRaisesRegex(ValueError, 'unbound transitive model include'):
            self.validate(data)

    def test_changed_source_digest(self):
        data = deepcopy(self.lock)
        data['files'][0]['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'SHA256 mismatch'):
            self.validate(data)

    def test_moving_upstream_revision(self):
        data = deepcopy(self.lock)
        data['revision'] = 'master'
        with self.assertRaisesRegex(ValueError, 'unpinned upstream cell models'):
            self.validate(data)


if __name__ == '__main__':
    unittest.main()
