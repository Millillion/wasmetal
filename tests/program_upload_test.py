#!/usr/bin/env python3
"""Verify image encoding, bounds, fingerprints and independent reply checksums."""
import binascii
import hashlib
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import zlib

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from prepare_standalone import load_profile
from program_upload import encode,decode_reply,profile_tag,sections


def fixture(directory):
    """Transport-only image; its arbitrary words are not an executable program."""
    profile=load_profile();directory.mkdir(parents=True,exist_ok=True)
    for name,rows,width in sections(profile):
        words=[((index+1)*0x102030405060708090a0b0c0d0e0f)&((1<<width)-1) for index in range(rows)]
        (directory/name).write_text(''.join(f'{word:0{(width+3)//4}x}\n' for word in words))
    (directory/'program.wasm').write_bytes(b'\0asm\1\0\0\0')
    (directory/'initialization.txt').write_bytes(b'')
    manifest={'format':'wasmetal-standalone-v1','profile':profile,'preparation_inputs':{},
              'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in directory.iterdir() if p.name!='manifest.json'}}
    (directory/'manifest.json').write_text(json.dumps(manifest))
    return manifest


class CodecTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.directory=Path(self.temp.name);self.manifest=fixture(self.directory)

    def rehash(self,name):
        self.manifest['files'][name]=hashlib.sha256((self.directory/name).read_bytes()).hexdigest()
        (self.directory/'manifest.json').write_text(json.dumps(self.manifest))

    def test_packet_layout_and_crc(self):
        packet=encode(self.directory,0x0123456789abcdef)
        version,nonce,tag,length=struct.unpack('<BQ16sI',packet.header[4:])
        self.assertEqual(packet.header[:4],b'WMLD');self.assertEqual(version,1)
        self.assertEqual(nonce,packet.nonce);self.assertEqual(tag,profile_tag(self.manifest['profile']))
        expected=b''.join(int(word,16).to_bytes((width+7)//8,'little')
            for name,_,width in sections(self.manifest['profile']) for word in (self.directory/name).read_text().splitlines())
        self.assertEqual(packet.payload,expected);self.assertEqual(length,len(expected))
        self.assertEqual(packet.checksum,zlib.crc32(packet.header[4:]+expected))
        self.assertEqual(packet.bytes()[-4:],struct.pack('<I',packet.checksum))

    def test_profile_canonicalization_and_configuration_change(self):
        profile=self.manifest['profile']
        self.assertEqual(profile_tag(profile),profile_tag(dict(reversed(list(profile.items())))))
        changed=dict(profile);changed['ram_bytes']*=2
        self.assertNotEqual(profile_tag(profile),profile_tag(changed))

    def test_changed_image_and_profile_rejected(self):
        path=self.directory/'code.hex';path.write_text(path.read_text()+'\n')
        with self.assertRaisesRegex(ValueError,'hash mismatch'):encode(self.directory)
        self.manifest['profile']['ram_bytes']*=2;self.rehash('code.hex')
        with self.assertRaisesRegex(ValueError,'hardware profile'):encode(self.directory)

    def test_valid_hash_does_not_excuse_bad_words(self):
        for content,message in [('0\n','row count'),('not-hex\n','invalid image word'),
                (f'{1<<self.manifest["profile"]["type_depth"]:x}\n','hardware width')]:
            rows=self.manifest['profile']['type_depth']
            (self.directory/'types.hex').write_text(content if message=='row count' else content*rows)
            self.rehash('types.hex')
            with self.assertRaisesRegex(ValueError,message):encode(self.directory)

    def test_reply_and_every_single_bit_corruption(self):
        body=struct.pack('<BBQI',1,1,987654321,0x12345678)
        packet=b'WMLR'+body+struct.pack('<H',binascii.crc_hqx(body,0xffff))
        self.assertEqual(decode_reply(packet),{'status':'committed','status_code':1,'nonce':987654321,'checksum':0x12345678})
        for bit in range(len(packet)*8):
            corrupt=bytearray(packet);corrupt[bit//8]^=1<<(bit%8)
            with self.assertRaises(ValueError):decode_reply(corrupt)
        for invalid in (packet[:-1],packet+b'\0'):
            with self.assertRaises(ValueError):decode_reply(invalid)
        for version,status,checksum in ((2,1,0),(1,8,0),(1,0,1)):
            body=struct.pack('<BBQI',version,status,0,checksum)
            with self.assertRaises(ValueError):decode_reply(b'WMLR'+body+struct.pack('<H',binascii.crc_hqx(body,0xffff)))


if __name__=='__main__':unittest.main()
