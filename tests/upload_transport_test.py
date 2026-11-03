#!/usr/bin/env python3
"""Exercise real file descriptors, backpressure, stale replies and terminal cleanup."""
import binascii
import concurrent.futures
import os
from pathlib import Path
import select
import struct
import sys
import tempfile
import termios
import time
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from program_upload import encode
from program_upload_test import fixture
from upload_program import transfer


def reply(status,nonce,checksum=0):
    body=struct.pack('<BBQI',1,status,nonce,checksum)
    return b'WMLR'+body+struct.pack('<H',binascii.crc_hqx(body,0xffff))


def result():
    body=bytes([1,0,0,1])+(53).to_bytes(4,'little')+(42).to_bytes(16,'little')
    return b'WM'+body+struct.pack('<H',binascii.crc_hqx(body,0xffff))


def read_exact(fd,size):
    data=bytearray();deadline=time.monotonic()+3
    while len(data)<size:
        if not select.select([fd],[],[],max(0,deadline-time.monotonic()))[0]:raise TimeoutError('test peer did not receive data')
        data.extend(os.read(fd,size-len(data)))
    return bytes(data)


class TransportTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        path=Path(temp.name);fixture(path);self.upload=encode(path,0x0123456789abcdef)
        self.master,self.slave=os.openpty();self.addCleanup(os.close,self.master);self.addCleanup(os.close,self.slave)
        self.original=termios.tcgetattr(self.slave)

    def test_stale_and_fragmented_replies_combined_with_result(self):
        def server():
            self.assertEqual(read_exact(self.master,33),self.upload.header)
            corrupt=bytearray(reply(0,self.upload.nonce));corrupt[-1]^=1
            stream=b'noiseWMLR\x01'+reply(0,self.upload.nonce+1)+corrupt+reply(0,self.upload.nonce)
            for at in range(0,len(stream),3):os.write(self.master,stream[at:at+3])
            self.assertEqual(read_exact(self.master,len(self.upload.payload)+4),self.upload.payload+struct.pack('<I',self.upload.checksum))
            # A single read can include both commit acknowledgment and result.
            os.write(self.master,reply(1,self.upload.nonce,self.upload.checksum)+result())
        with concurrent.futures.ThreadPoolExecutor() as pool:
            peer=pool.submit(server);actual=transfer(self.upload,os.ttyname(self.slave),3);peer.result()
        self.assertEqual(actual['result'],{'status':0,'trap':0,'cycles':53,'values':[42]})
        self.assertEqual(termios.tcgetattr(self.slave),self.original)

    def test_rejection_prevents_payload_and_restores_terminal(self):
        def server():
            read_exact(self.master,33);os.write(self.master,reply(3,self.upload.nonce))
        with concurrent.futures.ThreadPoolExecutor() as pool:
            peer=pool.submit(server)
            with self.assertRaisesRegex(ValueError,'header: profile'):transfer(self.upload,os.ttyname(self.slave),3)
            peer.result()
        self.assertFalse(select.select([self.master],[],[],0.02)[0])
        self.assertEqual(termios.tcgetattr(self.slave),self.original)

    def test_wrong_commit_checksum_and_timeout(self):
        def server():
            read_exact(self.master,33);os.write(self.master,reply(0,self.upload.nonce))
            read_exact(self.master,len(self.upload.payload)+4)
            os.write(self.master,reply(1,self.upload.nonce,self.upload.checksum^1))
        with concurrent.futures.ThreadPoolExecutor() as pool:
            peer=pool.submit(server)
            with self.assertRaisesRegex(ValueError,'different image checksum'):transfer(self.upload,os.ttyname(self.slave),3)
            peer.result()
        self.assertEqual(termios.tcgetattr(self.slave),self.original)

        with self.assertRaises(TimeoutError):transfer(self.upload,os.ttyname(self.slave),0.02)
        self.assertEqual(termios.tcgetattr(self.slave),self.original)

    def test_device_closes_even_when_restoring_terminal_fails(self):
        real_setattr=termios.tcsetattr;real_close=os.close;closed=[]
        def configure(fd,when,settings):
            if settings==self.original:raise OSError('simulated disconnected terminal')
            real_setattr(fd,when,settings)
        def close(fd):closed.append(fd);real_close(fd)
        def server():
            read_exact(self.master,33);os.write(self.master,reply(3,self.upload.nonce))
        with concurrent.futures.ThreadPoolExecutor() as pool:
            peer=pool.submit(server)
            with patch('upload_program.termios.tcsetattr',side_effect=configure),patch('upload_program.os.close',side_effect=close):
                with self.assertRaisesRegex(OSError,'disconnected terminal'):
                    transfer(self.upload,os.ttyname(self.slave),3)
            peer.result()
        self.assertEqual(len(closed),1)
        with self.assertRaises(OSError):os.fstat(closed[0])


if __name__=='__main__':unittest.main()
