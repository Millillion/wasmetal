#!/usr/bin/env python3
"""Upload a trusted prepared image at 9600 baud and read its execution result."""
import argparse
import json
import math
import os
from pathlib import Path
import select
import termios
import time

from program_upload import encode,decode_reply,REPLY_MAGIC,REPLY_SIZE
from read_standalone import read_frame


def remaining(deadline):
    value=deadline-time.monotonic()
    if value<=0:raise TimeoutError('WasMetal upload deadline exceeded')
    return value


def write_all(fd,data,deadline):
    pending=memoryview(data)
    while pending:
        if not select.select([],[fd],[],remaining(deadline))[1]:raise TimeoutError('Serial output stalled')
        try:written=os.write(fd,pending[:4096])
        except BlockingIOError:continue
        if written<=0:raise EOFError('Serial output closed during upload')
        pending=pending[written:]


def read_reply(fd,buffer,nonce,deadline):
    while True:
        start=0
        while True:
            start=buffer.find(REPLY_MAGIC,start)
            if start<0:break
            if len(buffer)-start>=REPLY_SIZE:
                try:reply=decode_reply(buffer[start:start+REPLY_SIZE])
                except ValueError:reply=None
                if reply is not None and reply['nonce']==nonce:
                    del buffer[:start+REPLY_SIZE]
                    return reply
            start+=1
        if len(buffer)>8192:del buffer[:-4096]
        if not select.select([fd],[],[],remaining(deadline))[0]:raise TimeoutError('No upload acknowledgment')
        try:chunk=os.read(fd,4096)
        except BlockingIOError:continue
        if not chunk:raise EOFError('Serial input closed during upload')
        buffer.extend(chunk)


def transfer(upload,device,timeout=120):
    if not math.isfinite(timeout) or timeout<=0:raise ValueError('timeout must be finite and positive')
    deadline=time.monotonic()+timeout;buffer=bytearray();original=None
    fd=os.open(device,os.O_RDWR|os.O_NOCTTY|os.O_NONBLOCK)
    try:
        original=termios.tcgetattr(fd);raw=termios.tcgetattr(fd)
        raw[0]=0;raw[1]=0;raw[3]=0
        raw[2]=(raw[2]&~(termios.CSIZE|termios.PARENB|termios.CSTOPB|termios.CRTSCTS))|termios.CS8|termios.CREAD|termios.CLOCAL
        raw[4]=termios.B9600;raw[5]=termios.B9600;raw[6][termios.VMIN]=0;raw[6][termios.VTIME]=0
        termios.tcsetattr(fd,termios.TCSANOW,raw)
        write_all(fd,upload.header,deadline)
        ready=read_reply(fd,buffer,upload.nonce,deadline)
        if ready['status']!='ready':raise ValueError('FPGA rejected upload header: '+ready['status'])
        write_all(fd,upload.payload+upload.checksum.to_bytes(4,'little'),deadline)
        committed=read_reply(fd,buffer,upload.nonce,deadline)
        if committed['status']!='committed':raise ValueError('FPGA rejected upload: '+committed['status'])
        if committed['checksum']!=upload.checksum:raise ValueError('FPGA committed a different image checksum')
        result=read_frame(fd,remaining(deadline),buffer)
        return {'nonce':upload.nonce,'image_checksum':upload.checksum,'profile_tag':upload.tag.hex(),
                'payload_bytes':len(upload.payload),'result':result}
    finally:
        try:
            if original is not None:termios.tcsetattr(fd,termios.TCSANOW,original)
        finally:
            os.close(fd)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image',type=Path);parser.add_argument('--device',required=True)
    parser.add_argument('--timeout',type=float,default=120)
    args=parser.parse_args()
    if not math.isfinite(args.timeout) or args.timeout<=0:parser.error('timeout must be finite and positive')
    print(json.dumps(transfer(encode(args.image),args.device,args.timeout),indent=2))


if __name__=='__main__':main()
