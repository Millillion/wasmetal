"""Exercise timing-audit rejection using the reference board's clock domains."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import check_timing


class TimingAudit(unittest.TestCase):
    def setUp(self):
        self.report={
            'fmax':{
                'clk_25mhz$TRELLIS_IO_IN':{'constraint':25,'achieved':894.45},
                'bridge_clock':{'constraint':12.5,'achieved':33.49},
                'core_clock':{'constraint':1,'achieved':3.24}},
            'critical_paths':[
                {'from':'negedge core_clock','to':'posedge core_clock','path':[{'delay':154.268}]},
                {'from':'posedge bridge_clock','to':'posedge core_clock','path':[{'delay':163.042}]},
                {'from':'posedge core_clock','to':'posedge bridge_clock','path':[{'delay':34.867}]}],
            'utilization':{}}

    def audit(self,report):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'timing.json';path.write_text(json.dumps(report))
            return check_timing.audit(path)

    def test_reference_domains(self):
        result=self.audit(self.report)
        self.assertEqual(result['reported_core_paths']['negedge->posedge']['budget_ns'],500)
        self.assertFalse(result['physical_hardware_tested'])

    def test_bad_clock_constraints(self):
        for name,field,value in [('core_clock','constraint',0.5),('bridge_clock','achieved',12),
                                 ('core_clock','achieved',float('nan'))]:
            with self.subTest(name=name,field=field):
                report=copy.deepcopy(self.report);report['fmax'][name][field]=value
                with self.assertRaises(ValueError):self.audit(report)

    def test_missing_domains_and_paths(self):
        report=copy.deepcopy(self.report);del report['fmax']['core_clock']
        with self.assertRaises(ValueError):self.audit(report)
        for index in range(3):
            with self.subTest(path=index):
                report=copy.deepcopy(self.report);del report['critical_paths'][index]
                with self.assertRaises(ValueError):self.audit(report)

    def test_edge_and_crossing_budgets(self):
        for index,delay in [(0,500.001),(1,1000.001),(2,float('inf'))]:
            with self.subTest(path=index):
                report=copy.deepcopy(self.report);report['critical_paths'][index]['path'][0]['delay']=delay
                with self.assertRaises(ValueError):self.audit(report)

    def test_full_cycle_path(self):
        report=copy.deepcopy(self.report)
        report['fmax']['core_clock']['achieved']=1.1
        report['critical_paths'][0].update({'from':'posedge core_clock','path':[{'delay':900}]})
        self.assertEqual(self.audit(report)['reported_core_paths']['posedge->posedge']['budget_ns'],1000)
        report['critical_paths'][0]['path'][0]['delay']=1000.001
        with self.assertRaises(ValueError):self.audit(report)


if __name__=='__main__':unittest.main()
