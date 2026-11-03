#!/usr/bin/env python3
"""Admission failures must not become truncated, executable FPGA images."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from prepare_standalone import load_profile, pack_trace, MAGIC


class ImageTests(unittest.TestCase):
    def setUp(self):
        self.profile = load_profile()
        self.code = ['Y 0 0', 'F 0 0 0 0 1 0', 'I 0 65 0 0 0 0 2a', 'I 1 11 0 0 0 0 0']

    def pack(self, setup=(), end=('Z 0 0',), profile=None):
        return pack_trace(self.code + list(setup) + list(end), profile or self.profile)

    def test_header_and_instruction_identity(self):
        rom, summary = self.pack()
        self.assertEqual(rom['code'][0], 65 | 42 << 160)
        self.assertEqual(rom['types'][0], 1)
        self.assertEqual(rom['boot'][0] & 0xffffffff, MAGIC)
        self.assertEqual(summary['counts']['boot'], 3)
        self.assertEqual(rom['boot'][2], 0)
        self.assertEqual(len(rom['code']), self.profile['instruction_depth'])

    def test_all_memory_kinds_and_little_endian_initialization(self):
        rom, summary = self.pack(['M 0 1 1 0', 'T 0 1 2 0', 'G 0 1234',
                                  'D 0 4 01020304', 'L 0 1 1 12345678',
                                  'B 0 65534 aabb', 'E 0 1 deadbeef'])
        self.assertEqual({r['kind'] for r in summary['regions']}, set(range(6)))
        writes = [w for w in rom['boot'] if w >> 228 == 2]
        self.assertIn(0x04030201, [w & ((1 << 128) - 1) for w in writes])
        self.assertIn(0xbbaa, [w & ((1 << 128) - 1) for w in writes])

    def test_regions_reject_overruns_before_emitting(self):
        for setup in (['M 0 1 1 0', 'B 0 65535 aabb'], ['G 16 0'],
                      ['T 0 1 1 0', 'E 0 1 2'], ['B 0 0 aa'],
                      ['D 0 2 00'], ['L 0 1 2 0'], ['G 0 0', 'G 0 0']):
            with self.subTest(setup=setup), self.assertRaises(ValueError):
                self.pack(setup)

    def test_declared_growth_and_ram_capacity_are_bounded(self):
        for setup in (['M 0 1 2 0'], ['M 0 2 1 0'], ['T 0 1 129 0']):
            with self.subTest(setup=setup), self.assertRaises(ValueError):
                self.pack(setup)
        large = deepcopy(self.profile); large['memory_pages'] = 2
        with self.assertRaisesRegex(ValueError, 'RAM capacity'):
            self.pack(['M 0 2 2 0'], profile=large)

    def test_invocation_and_termination(self):
        for end in ([], ['Z 1 0'], ['Z 0 1'], ['Z 0 0', 'Z 0 0'], ['X']):
            with self.subTest(end=end), self.assertRaises(ValueError):
                self.pack(end=end)

    def test_rom_and_field_limits(self):
        for setup in (['I 0 65 0 0 0 0 0'], ['I 1024 0 0 0 0 0 0'],
                      ['Y 64 0'], ['F 128 0 0 0 0 0'],
                      ['I 2 65 0 0 0 0 ' + '1' + '0' * 32],
                      ['F 1 3 0 0 0 0'], ['A 8192 1'],
                      ['A 0 1'] * 512):
            with self.subTest(setup=setup[:1]), self.assertRaises(ValueError):
                self.pack(setup)


if __name__ == '__main__':
    unittest.main()
