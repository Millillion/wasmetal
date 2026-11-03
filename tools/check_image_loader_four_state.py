#!/usr/bin/env python3
"""Check unknown startup and payload rejection using actual four-state RTL."""
import json
from pathlib import Path
import struct
import subprocess
import zlib
from prepare_standalone import ROOT,digest


def main():
    directory=ROOT/'build/image-loader/four-state';directory.mkdir(parents=True,exist_ok=True)
    original=ROOT/'soc/loader/wasmetal_image_loader.sv';bench=ROOT/'tests/memory/image_loader_four_state.sv'
    inputs=[original,bench,Path(__file__).resolve()];hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs}
    body=struct.pack('<BQ16sI',1,0x0123456789abcdef,bytes(range(16)),404)+bytes((n*17+42)%256 for n in range(404))
    packet=b'WMLD'+body+struct.pack('<I',zlib.crc32(body))
    (directory/'packet.hex').write_text(''.join(f'{byte:02x}\n' for byte in packet))
    def run(source,name):
        binary=directory/(name+'.vvp')
        with (directory/(name+'-compile.log')).open('w') as log:
            subprocess.run([str(ROOT/'.cache/tools/usr/bin/iverilog'),
                '-B'+str(ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl'),'-g2012','-s','image_loader_tb',
                '-o',str(binary),str(source),str(bench)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=60)
        result=subprocess.run([str(ROOT/'.cache/tools/usr/bin/vvp'),str(binary)],cwd=ROOT,capture_output=True,text=True,timeout=30)
        (directory/(name+'.log')).write_text(result.stdout+result.stderr)
        return result
    positive=run(original,'positive');positive.check_returncode()
    if 'PASS loader four-state' not in positive.stdout:raise ValueError('missing four-state pass')
    rejected=[]
    for name,old,new,message in [
        ('missing-permission-reset','image_valid<=0;word_section<=0;','word_section<=0;','loader reset retained unknown state'),
        ('missing-checksum-gate','checksum_next==~crc && words_sent==TOTAL_WORDS','words_sent==TOTAL_WORDS','unknown payload became executable'),
    ]:
        text=original.read_text();assert text.count(old)==1
        path=directory/(name+'.sv');path.write_text(text.replace(old,new))
        result=run(path,name)
        if result.returncode==0 or message not in result.stdout+result.stderr:raise ValueError('bad four-state negative control: '+name)
        rejected.append(name)
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise RuntimeError('four-state loader inputs changed')
    report={'status':'passed','scope':'four-state reset and unknown-data fail-closed image authorization',
        'payload_bytes':404,'packet_sha256':digest(directory/'packet.hex'),
        'negative_controls_rejected':rejected,'inputs':hashes,'physical_hardware_tested':False}
    (ROOT/'reports/image-loader-four-state.json').write_text(json.dumps(report,indent=2)+'\n')
    print(positive.stdout.strip())


if __name__=='__main__':main()
