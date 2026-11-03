#!/usr/bin/env python3
"""Timing acceptance must fail for missing clocks, crossings or late paths."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from build_standalone_board import audit


class TimingTests(unittest.TestCase):
    def setUp(self):
        self.report={'fmax':{'clk_25mhz':{'constraint':25,'achieved':100},
                             'core_clock':{'constraint':0.78125,'achieved':3}},
            'critical_paths':[{'from':'negedge core_clock','to':'posedge core_clock',
                               'path':[{'delay':200}]}],
            'utilization':{'DP16KD':{'used':171,'available':208}}}

    def check(self,report):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'timing.json';path.write_text(json.dumps(report))
            return audit(path)

    def test_known_clock_budget(self):
        self.assertEqual(self.check(self.report)['paths']['core:negedge->posedge']['budget_ns'],640)

    def test_missing_or_weak_clock_constraints(self):
        bad=deepcopy(self.report);del bad['fmax']['core_clock']
        with self.assertRaises(ValueError):self.check(bad)
        for field,value in [('constraint',0),('constraint',4),('achieved',0.5),('achieved',float('nan'))]:
            bad=deepcopy(self.report);bad['fmax']['core_clock'][field]=value
            with self.subTest(field=field,value=value),self.assertRaises(ValueError):self.check(bad)

    def test_half_cycle_overrun_crossing_and_capacity(self):
        bad=deepcopy(self.report);bad['critical_paths'][0]['path'][0]['delay']=641
        with self.assertRaises(ValueError):self.check(bad)
        bad=deepcopy(self.report);bad['critical_paths'][0]['from']='posedge clk_25mhz'
        with self.assertRaises(ValueError):self.check(bad)
        bad=deepcopy(self.report);bad['utilization']['DP16KD']['used']=209
        with self.assertRaises(ValueError):self.check(bad)
        bad=deepcopy(self.report);bad['critical_paths']=[]
        with self.assertRaises(ValueError):self.check(bad)


if __name__=='__main__':unittest.main()
