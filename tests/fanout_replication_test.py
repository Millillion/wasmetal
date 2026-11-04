"""Independent small-circuit checks for chained physical LUT substitutions."""
from pathlib import Path
import copy
import itertools
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import replicate_fanout as fanout


def lut(a,b,c,d,z,truth):
    return {'hide_name':0,'type':'LUT4','parameters':{'INIT':format(truth,'016b')},'attributes':{},
            'port_directions':{'A':'input','B':'input','C':'input','D':'input','Z':'output'},
            'connections':{'A':[a],'B':[b],'C':[c],'D':[d],'Z':[z]}}


def fixture():
    cells={'a':lut(3,4,'0','0',10,0x6666),'b':lut(10,5,'0','0',11,0x8888)}
    for index in range(8):cells['sink'+str(index)]=lut(10 if index<4 else 11,'0','0','0',20+index,0xaaaa)
    cells['state']={'hide_name':0,'type':'TRELLIS_FF','parameters':{'REGSET':'RESET'},'attributes':{},
        'port_directions':{'CLK':'input','DI':'input','LSR':'input','Q':'output'},
        'connections':{'CLK':[2],'DI':[10],'LSR':[6],'Q':[30]}}
    module={'attributes':{},'parameter_default_values':{},'ports':{
        'clk':{'direction':'input','bits':[2]},'x':{'direction':'input','bits':[3]},
        'y':{'direction':'input','bits':[4]},'z':{'direction':'input','bits':[5]},
        'reset':{'direction':'input','bits':[6]},'result':{'direction':'output','bits':list(range(20,28))}},
        'cells':cells,'netnames':{'a':{'hide_name':0,'bits':[10],'attributes':{}},
            'b':{'hide_name':0,'bits':[11],'attributes':{}},
            'data':{'hide_name':0,'bits':[10,11],'attributes':{}}}}
    design={'creator':'test fixture','modules':{'top':module,'unrelated':{'attributes':{'opaque':'keep'}}}}
    locations={name:(index%3,index//3) for index,name in enumerate(cells)}
    return design,locations


def observe(design,values):
    """Evaluate truth tables directly, without using the substitution checker."""
    nets={'0':0,'1':1,2:0,3:values[0],4:values[1],5:values[2],6:0,30:0}
    remaining={name:cell for name,cell in design['modules']['top']['cells'].items() if cell['type']=='LUT4'}
    while remaining:
        progress=[]
        for name,cell in remaining.items():
            inputs=[cell['connections'][port][0] for port in 'ABCD']
            if not all(bit in nets for bit in inputs):continue
            address=sum(nets[bit]<<index for index,bit in enumerate(inputs))
            nets[cell['connections']['Z'][0]]=(int(cell['parameters']['INIT'],2)>>address)&1
            progress.append(name)
        if not progress:raise ValueError('combinational cycle or missing driver')
        for name in progress:del remaining[name]
    return [nets[bit] for bit in design['modules']['top']['ports']['result']['bits']]


class FanoutTests(unittest.TestCase):
    def candidate(self):
        reference,locations=fixture()
        first,a=fanout.add_stage(reference,'top',{'net':'data','bit':0},locations,2,'copy_a')
        result,b=fanout.add_stage(first,'top',{'net':'data','bit':1},locations,2,'copy_b')
        return reference,result,[a,b]

    def test_dependent_stages_preserve_every_binary_input(self):
        reference,candidate,stages=self.candidate()
        proof=fanout.verify_chain(reference,candidate,'top',stages)
        self.assertEqual(proof['stages'],2)
        self.assertGreater(proof['added_luts'],1)
        for values in itertools.product((0,1),repeat=3):
            self.assertEqual(observe(reference,values),observe(candidate,values))
        # Also check the algorithm against the intended function independently.
        for x,y,z in itertools.product((0,1),repeat=3):
            self.assertEqual(observe(candidate,(x,y,z)),[x^y]*4+[((x^y)&z)]*4)

    def test_unlocated_sinks_and_clock_pins_keep_original_driver(self):
        reference,locations=fixture()
        reference['modules']['top']['cells']['state']['connections']['CLK']=[10]
        del locations['sink0']
        candidate,stage=fanout.add_stage(reference,'top',{'net':'a','bit':0},locations,2,'copy')
        fanout.verify_chain(reference,candidate,'top',[stage])
        self.assertEqual(candidate['modules']['top']['cells']['sink0']['connections']['A'],[10])
        self.assertEqual(candidate['modules']['top']['cells']['state']['connections']['CLK'],[10])
        self.assertEqual(stage['unlocated_or_clock_sink_pins_retained'],2)

    def test_original_function_change_cannot_hide_in_matching_copies(self):
        reference,candidate,stages=self.candidate()
        for name in ['a',*[g['driver'] for g in stages[0]['groups'][1:]]]:
            candidate['modules']['top']['cells'][name]['parameters']['INIT']=format(0x9999,'016b')
        with self.assertRaisesRegex(ValueError,'collapsed circuit differs'):
            fanout.verify_chain(reference,candidate,'top',stages)

    def test_partial_stage_list_is_not_a_complete_proof(self):
        reference,candidate,stages=self.candidate()
        with self.assertRaises(ValueError):fanout.verify_chain(reference,candidate,'top',stages[1:])

    def test_unrelated_module_and_output_changes_are_rejected(self):
        reference,candidate,stages=self.candidate()
        changed=copy.deepcopy(candidate);changed['modules']['unrelated']['attributes']['opaque']='changed'
        with self.assertRaisesRegex(ValueError,'collapsed circuit differs'):
            fanout.verify_chain(reference,changed,'top',stages)
        changed=copy.deepcopy(candidate);changed['modules']['top']['ports']['result']['bits'][0]=3
        with self.assertRaisesRegex(ValueError,'collapsed circuit differs'):
            fanout.verify_chain(reference,changed,'top',stages)

    def test_out_of_range_and_constant_selections_fail(self):
        reference,locations=fixture()
        with self.assertRaisesRegex(ValueError,'selected bit is absent or constant'):
            fanout.add_stage(reference,'top',{'net':'data','bit':2},locations,2,'copy')
        reference['modules']['top']['netnames']['constant']={'bits':['0']}
        with self.assertRaisesRegex(ValueError,'selected bit is absent or constant'):
            fanout.add_stage(reference,'top',{'net':'constant','bit':0},locations,2,'copy')


if __name__=='__main__':unittest.main()
