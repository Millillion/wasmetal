#!/usr/bin/env python3
"""Encode checked prepared images for the two-phase WasMetal upload protocol."""
import argparse
import binascii
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import secrets
import struct
import zlib

from standalone_support import verify_image

MAGIC=b'WMLD'
REPLY_MAGIC=b'WMLR'
HEADER_SIZE=33
REPLY_SIZE=20
STATUS=('ready','committed','version','profile','length','checksum','timeout','abort')


def profile_tag(profile):
    canonical=json.dumps(profile,sort_keys=True,separators=(',',':')).encode('ascii')
    return hashlib.sha256(b'WasMetal prepared image upload v1\0'+canonical).digest()[:16]


def sections(profile):
    return [('code.hex',profile['instruction_depth'],288),
            ('functions.hex',profile['function_depth'],160),
            ('types.hex',profile['type_depth'],profile['type_depth']),
            ('regions.hex',6*profile['regions_per_kind'],64),
            ('boot.hex',profile['boot_depth'],232)]


@dataclass(frozen=True)
class Upload:
    nonce:int
    tag:bytes
    header:bytes
    payload:bytes
    checksum:int

    def bytes(self):
        return self.header+self.payload+struct.pack('<I',self.checksum)


def encode(directory,nonce=None,compact=False):
    """Version 1 sends every row; compact version 2 omits trailing zero rows,
    which the loader clears itself after verifying the checksum."""
    directory=Path(directory);manifest=verify_image(directory);profile=manifest['profile']
    rows_by_section=[]
    for name,rows,width in sections(profile):
        lines=(directory/name).read_text().splitlines()
        if len(lines)!=rows:raise ValueError('wrong image row count: '+name)
        values=[]
        for line in lines:
            if not re.fullmatch(r'[0-9a-fA-F]+',line):raise ValueError('invalid image word: '+name)
            value=int(line,16)
            if value>=1<<width:raise ValueError('image word exceeds hardware width: '+name)
            values.append(value)
        if compact:
            while values and values[-1]==0:values.pop()
        rows_by_section.append((values,width))
    payload=bytearray(struct.pack('<5I',*(len(v) for v,_ in rows_by_section)) if compact else b'')
    for values,width in rows_by_section:
        for value in values:payload.extend(value.to_bytes((width+7)//8,'little'))
    if len(payload)>0xffffffff:raise ValueError('upload is too large')
    nonce=secrets.randbits(64) if nonce is None else nonce
    tag=profile_tag(profile)
    body=struct.pack('<BQ16sI',2 if compact else 1,nonce,tag,len(payload))
    return Upload(nonce,tag,MAGIC+body,bytes(payload),zlib.crc32(body+payload))


def decode_reply(data):
    if len(data)!=REPLY_SIZE or data[:4]!=REPLY_MAGIC:raise ValueError('bad upload reply framing')
    version,status,nonce,checksum,crc=struct.unpack('<BBQIH',data[4:])
    if version!=1 or status>=len(STATUS):raise ValueError('unknown upload reply')
    if binascii.crc_hqx(data[4:18],0xffff)!=crc:raise ValueError('upload reply CRC mismatch')
    if status not in (1,5) and checksum:raise ValueError('unexpected upload reply checksum')
    return {'status':STATUS[status],'status_code':status,'nonce':nonce,'checksum':checksum}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image',type=Path);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();upload=encode(args.image)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(upload.bytes())
    print(json.dumps({'file':str(args.output),'payload_bytes':len(upload.payload),'nonce':upload.nonce,
        'profile_tag':upload.tag.hex(),'checksum':upload.checksum,
        'transport':'send the 33-byte header, wait for ready, then send payload and CRC; do not stream this whole file without the handshake'},indent=2))


if __name__=='__main__':main()
