#!/usr/bin/env python3
"""Read a standalone result at 9600 baud, or decode a captured hexadecimal frame."""
import argparse
import json
import math
import os
import select
import termios
import time

from check_standalone import decode


def read_frame(fd, timeout):
    deadline=time.monotonic()+timeout
    data=bytearray()
    while time.monotonic()<deadline:
        if not select.select([fd],[],[],max(0,deadline-time.monotonic()))[0]: break
        chunk=os.read(fd,4096)
        if not chunk: raise EOFError('Serial stream closed before a valid result frame arrived.')
        data.extend(chunk)
        # Search every candidate so a truncated old frame cannot hide a fresh
        # boot result. Length and checksum must both validate before returning.
        start=0
        while True:
            start=data.find(b'WM\x01',start)
            if start<0: break
            if len(data)-start>=6:
                length=12+16*data[start+5]
                if len(data)-start>=length:
                    try: return decode(data[start:start+length].hex())
                    except ValueError: pass
            start+=1
        if len(data)>8192: del data[:-4096]
    raise TimeoutError('No valid WasMetal frame received; start the reader, then reset the board.')


def receive(device,timeout):
    fd=os.open(device,os.O_RDONLY|os.O_NOCTTY|os.O_NONBLOCK)
    original=None
    try:
        original=termios.tcgetattr(fd)
        raw=termios.tcgetattr(fd)
        raw[0]=0;raw[1]=0;raw[3]=0
        raw[2]=(raw[2]&~(termios.CSIZE|termios.PARENB|termios.CSTOPB|termios.CRTSCTS))|termios.CS8|termios.CREAD|termios.CLOCAL
        raw[4]=termios.B9600;raw[5]=termios.B9600
        raw[6][termios.VMIN]=0;raw[6][termios.VTIME]=0
        termios.tcsetattr(fd,termios.TCSANOW,raw)
        return read_frame(fd,timeout)
    finally:
        if original is not None: termios.tcsetattr(fd,termios.TCSANOW,original)
        os.close(fd)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    source=parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--device')
    source.add_argument('--hex')
    parser.add_argument('--timeout',type=float,default=30)
    args=parser.parse_args()
    if not math.isfinite(args.timeout) or args.timeout<=0: parser.error('timeout must be finite and positive')
    frame=decode(args.hex) if args.hex is not None else receive(args.device,args.timeout)
    frame['raw_hex']=[f'{value:032x}' for value in frame['values']]
    print(json.dumps(frame,indent=2))
