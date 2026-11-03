#!/usr/bin/env python3
"""The host reader accepts independently encoded frames and rejects corruption."""
import binascii
import os
from pathlib import Path
import sys
import termios
import threading
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from read_standalone import read_frame,receive
from check_standalone import decode


class SerialTests(unittest.TestCase):
    def packet(self):
        payload=bytes([1,0,0,1])+(123).to_bytes(4,'little')+(42).to_bytes(16,'little')
        return b'WM'+payload+binascii.crc_hqx(payload,0xffff).to_bytes(2,'little')

    def test_noise_corruption_and_truncated_previous_frame(self):
        packet=self.packet();bad=bytearray(packet);bad[10]^=1
        read,write=os.pipe()
        try:
            os.write(write,b'noiseWM\x01\0\0\xff'+bad+b'other bytes'+packet)
            frame=read_frame(read,1)
            self.assertEqual(frame['values'],[42]);self.assertEqual(frame['cycles'],123)
        finally:os.close(read);os.close(write)

    def test_bad_packet_and_timeout(self):
        for data in (b'',self.packet()[:-1],self.packet()+b'junk'):
            with self.assertRaises(ValueError):decode(data.hex())
        read,write=os.pipe()
        try:
            with self.assertRaises(TimeoutError):read_frame(read,0.01)
        finally:os.close(read);os.close(write)

    def test_memory_startup_failure(self):
        for status in (5,6):
            payload=bytes([1,status,0,0])+bytes(4)
            packet=b'WM'+payload+binascii.crc_hqx(payload,0xffff).to_bytes(2,'little')
            if status==5:
                self.assertEqual(decode(packet.hex()),{'status':5,'trap':0,'cycles':0,'values':[]})
            else:
                with self.assertRaises(ValueError):decode(packet.hex())

    def test_terminal_configuration_and_restoration(self):
        master,slave=os.openpty();ready=threading.Event()
        original=termios.tcgetattr(slave);configure=termios.tcsetattr
        def configured(fd,when,attrs):
            configure(fd,when,attrs);ready.set()
        def send():
            if ready.wait(2):os.write(master,self.packet())
        writer=threading.Thread(target=send);writer.start()
        try:
            with patch('read_standalone.termios.tcsetattr',side_effect=configured):
                self.assertEqual(receive(os.ttyname(slave),2)['values'],[42])
            self.assertEqual(termios.tcgetattr(slave),original)
        finally:writer.join();os.close(master);os.close(slave)


if __name__=='__main__':unittest.main()
