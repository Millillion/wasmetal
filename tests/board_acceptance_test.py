#!/usr/bin/env python3
"""Check host acceptance accounting and rejection with a software serial peer."""
import binascii
import concurrent.futures
import copy
import json
import os
from pathlib import Path
import shutil
import struct
import sys
import tempfile
import termios
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import board_acceptance as acceptance
from prepare_standalone import ROOT,digest,load_profile
from program_upload import encode,profile_tag
from upload_transport_test import read_exact,reply


class AcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template=tempfile.TemporaryDirectory(prefix='acceptance-template-',dir=ROOT/'build')
        cls.addClassCleanup(cls.template.cleanup)
        cls.template_path=acceptance.prepare_plan(Path(cls.template.name),ROOT/'reports/loadable-rtl.json')

    def setUp(self):
        temporary=tempfile.TemporaryDirectory(prefix='acceptance-test-',dir=ROOT/'build');self.addCleanup(temporary.cleanup)
        self.directory=Path(temporary.name);shutil.copytree(self.template_path.parent,self.directory/'plan')
        self.path=self.directory/'plan/plan.json';self.plan=json.loads(self.path.read_text())
        self.report=self.directory/'run.json'

    def save_plan(self):self.path.write_text(json.dumps(self.plan,indent=2)+'\n')

    def run_plan(self,**options):
        return acceptance.run_plan(self.path,'test-serial-device',self.report,repetitions=1,**options)

    def fake_transfer(self,bad=None):
        self.calls=[]
        def transfer(upload,device,timeout):
            item=self.plan['cases'][len(self.calls)%len(self.plan['cases'])];self.calls.append(item['name'])
            frame=copy.deepcopy(item['expected'])
            if len(self.calls)==2:
                if bad=='cycles':frame['cycles']+=1
                elif bad=='value':frame['values'][0]^=1
                elif bad=='link':raise TimeoutError('disconnected test peer')
            return {'nonce':upload.nonce,'image_checksum':upload.checksum,'profile_tag':upload.tag.hex(),
                    'payload_bytes':len(upload.payload),'result':frame}
        return transfer

    def test_repeated_campaign_over_real_pseudoterminal(self):
        master,slave=os.openpty();self.addCleanup(os.close,master);self.addCleanup(os.close,slave)
        original=termios.tcgetattr(slave);nonces=[]
        def peer():
            for _ in range(2):
                for item in self.plan['cases']:
                    header=read_exact(master,33);nonce=int.from_bytes(header[5:13],'little');nonces.append(nonce)
                    upload=encode(self.path.parent/item['image'],nonce)
                    self.assertEqual(header,upload.header);os.write(master,reply(0,nonce))
                    self.assertEqual(read_exact(master,len(upload.payload)+4),upload.payload+struct.pack('<I',upload.checksum))
                    expected=item['expected'];body=bytes([1,expected['status'],expected['trap'],len(expected['values'])])
                    body+=expected['cycles'].to_bytes(4,'little')
                    body+=b''.join(value.to_bytes(16,'little') for value in expected['values'])
                    frame=b'WM'+body+struct.pack('<H',binascii.crc_hqx(body,0xffff))
                    os.write(master,reply(1,nonce,upload.checksum)+frame)
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future=pool.submit(peer)
            report=acceptance.run_plan(self.path,os.ttyname(slave),self.report,repetitions=2,timeout=10)
            future.result()
        self.assertEqual(report['status'],'passed');self.assertEqual(len(report['cases']),50)
        self.assertFalse(report['physical_hardware_tested']);self.assertFalse(report['hardware_asserted_by_operator'])
        self.assertTrue(all(case['matches_reference'] for case in report['cases']))
        self.assertEqual(len(set(nonces)),50);self.assertEqual(termios.tcgetattr(slave),original)

    def test_wrong_result_preserves_observation_and_stops(self):
        with patch('board_acceptance.transfer',side_effect=self.fake_transfer('value')):
            with self.assertRaises(AssertionError):self.run_plan()
        report=json.loads(self.report.read_text());self.assertEqual(report['status'],'failed')
        self.assertEqual(len(self.calls),2);self.assertEqual(len(report['cases']),2)
        self.assertTrue(report['cases'][0]['matches_reference']);self.assertFalse(report['cases'][1]['matches_reference'])

    def test_wrong_cycle_count_is_not_a_pass(self):
        with patch('board_acceptance.transfer',side_effect=self.fake_transfer('cycles')):
            with self.assertRaisesRegex(ValueError,'cycle count'):self.run_plan()
        self.assertEqual(json.loads(self.report.read_text())['status'],'failed');self.assertEqual(len(self.calls),2)

    def test_disconnect_preserves_partial_progress(self):
        with patch('board_acceptance.transfer',side_effect=self.fake_transfer('link')):
            with self.assertRaises(TimeoutError):self.run_plan()
        report=json.loads(self.report.read_text());self.assertEqual(report['status'],'failed')
        self.assertEqual(len(report['cases']),1);self.assertEqual(report['active_case']['name'],'selftest')

    def test_missing_coverage_and_changed_expectations_rejected_before_io(self):
        original=copy.deepcopy(self.plan)
        for mutation in ('missing','duplicate','reorder','result','tools'):
            self.plan=copy.deepcopy(original)
            if mutation=='missing':self.plan['cases'].pop()
            elif mutation=='duplicate':self.plan['cases'].append(self.plan['cases'][0])
            elif mutation=='reorder':self.plan['cases'].reverse()
            elif mutation=='result':self.plan['cases'][0]['expected']['cycles']+=1
            else:self.plan['inputs']['tools/program_upload.py']='0'*64
            self.save_plan()
            with patch('board_acceptance.transfer') as transport:
                with self.assertRaises(ValueError):self.run_plan()
                transport.assert_not_called()

    def test_rehashed_different_program_is_rejected(self):
        item=self.plan['cases'][0];image=self.path.parent/item['image'];code=image/'code.hex'
        words=code.read_text().splitlines();words[0]=f'{int(words[0],16)^1:072x}';code.write_text('\n'.join(words)+'\n')
        manifest=json.loads((image/'manifest.json').read_text());manifest['files']['code.hex']=digest(code)
        (image/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        item['manifest_sha256']=digest(image/'manifest.json');self.save_plan()
        with patch('board_acceptance.transfer') as transport:
            with self.assertRaisesRegex(ValueError,'differs from native execution'):self.run_plan()
            transport.assert_not_called()

    def test_non_native_reference_is_rejected(self):
        path=self.path.parent/'native-reference.json';reference=json.loads(path.read_text())
        reference['model']['backend']='loadable-mapped-ecp5-functional';path.write_text(json.dumps(reference))
        self.plan['reference_sha256']=digest(path);self.save_plan()
        with patch('board_acceptance.transfer') as transport:
            with self.assertRaisesRegex(ValueError,'native programmable reference'):self.run_plan()
            transport.assert_not_called()

    def test_bitstream_integrity_and_hardware_label(self):
        directory=self.directory/'bitstream';directory.mkdir();bit=directory/'wasmetal.bit';bit.write_bytes(b'test fixture, not an FPGA bitstream')
        path=directory/'manifest.json';profile=load_profile()
        manifest={'top':'wasmetal_loadable_ulx3s','profile':profile,'profile_tag':profile_tag(profile).hex(),
            'board':'test fixture','bitstream_round_trip_passed':True,
            'inputs':{name:digest(ROOT/name) for name in ('tools/upstream.lock.json','soc/profile.json',
                'soc/loader/ulx3s.lpf','soc/loader/wasmetal_loadable.sv','soc/loader/wasmetal_loadable_ulx3s.sv')},
            'artifacts':{'wasmetal.bit':digest(bit)}}
        path.write_text(json.dumps(manifest));actual=acceptance.verify_bitstream(path,profile)
        self.assertFalse(actual['read_back_from_device']);bit.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'changed board bitstream'):acceptance.verify_bitstream(path,profile)
        with self.assertRaisesRegex(ValueError,'hardware runs require'):
            acceptance.run_plan(self.path,'/dev/pts/123',self.report,hardware=True,label='test',bitstream_manifest=path)

    def test_progress_cannot_overwrite_the_prepared_plan(self):
        with patch('board_acceptance.transfer') as transport:
            with self.assertRaisesRegex(ValueError,'outside the prepared plan'):
                acceptance.run_plan(self.path,'test',self.path,repetitions=1)
            transport.assert_not_called()


if __name__=='__main__':unittest.main()
