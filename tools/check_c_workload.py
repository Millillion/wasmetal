#!/usr/bin/env python3
"""Compile freestanding C to Wasm and execute its prepared image through UART."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import time
import zlib
from check_loadable import parse_frames
from check_standalone import check_expected
from prepare_standalone import ROOT,prepare,digest
from program_upload import encode
from standalone_support import verify_simulator


LENGTHS=(0,1,256,1024,1025)


def tool(name):
    found=shutil.which(name)
    if found is None:raise RuntimeError(f'{name} is required; install clang-18 and lld-18')
    # lld selects its linker flavor from argv[0]; retain the wasm-ld symlink.
    path=Path(found).absolute()
    version=subprocess.run([str(path),'--version'],capture_output=True,text=True,check=True).stdout.strip()
    return {'path':str(path),'sha256':digest(path),'version':version}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--mapped',action='store_true')
    args=parser.parse_args();directory=ROOT/'build/c-workload';directory.mkdir(parents=True,exist_ok=True)
    source=ROOT/'examples/c/crc32.c';wasm=directory/'crc32.wasm';obj=directory/'crc32.o'
    compiler=tool('clang-18');linker=tool('wasm-ld-18')
    paths=[source,Path(__file__).resolve(),ROOT/'tools/check_loadable.py',ROOT/'tools/check_standalone.py',
        ROOT/'tools/prepare_standalone.py',ROOT/'tools/program_upload.py',ROOT/'tools/standalone_support.py']
    inputs={str(path.relative_to(ROOT)):digest(path) for path in paths}
    commands={'compile':[compiler['path'],'--target=wasm32','-std=c11','-O2','-Wall','-Wextra','-Werror',
        '-ffreestanding','-fno-builtin','-c',str(source),'-o',str(obj)],
        'link':[linker['path'],'--no-entry','--export=checksum','--stack-first','-z','stack-size=16384',
            '--initial-memory=65536','--max-memory=65536',str(obj),'-o',str(wasm)]}
    for stage,command in commands.items():
        result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
        (directory/(stage+'.log')).write_text(result.stdout+result.stderr)
        if result.returncode:raise RuntimeError('C workload '+stage+' failed: '+result.stdout+result.stderr)
    wasm_hash=digest(wasm);packets={};prepared={}
    for length in LENGTHS:
        image=directory/f'image-{length}';manifest=prepare(wasm,image,export='checksum',arguments=[length])
        packet=encode(image,0x574d430000000000+length);path=directory/f'crc32-{length}.wmu';path.write_bytes(packet.bytes())
        packets[length]=path;prepared[length]={'counts':manifest['counts'],'allocated_ram_bytes':manifest['allocated_ram_bytes'],
            'image_manifest_sha256':digest(image/'manifest.json'),'packet_sha256':digest(path)}
    binaries={'rtl':ROOT/'build/loadable-sim/Vwasmetal_loadable'}
    if args.mapped:binaries['mapped']=ROOT/'build/loadable-gate-sim/obj/Vwasmetal_loadable'
    identities={backend:verify_simulator(binary) for backend,binary in binaries.items()}
    if identities['rtl']['backend']!='loadable-rtl':raise ValueError('native programmable model required')
    if args.mapped:
        mapped=identities['mapped']
        if mapped['backend']!='loadable-mapped-ecp5-functional':raise ValueError('mapped programmable model required')
        for key in ('profile','profile_tag','uart_ticks','clock_scale','upload_timeout'):
            if mapped[key]!=identities['rtl'][key]:raise ValueError('C workload model configuration differs: '+key)
    report_path=ROOT/'reports'/('c-workload-mapped.json' if args.mapped else 'c-workload-rtl.json')
    started=time.monotonic();observations={};report={'status':'running','source_sha256':digest(source),
        'wasm_sha256':wasm_hash,'compiler':compiler,'linker':linker,'commands':commands,'inputs':inputs,
        'models':identities,'cases':observations,'physical_hardware_tested':False,
        'scope':'compiler-generated C workload through programmable UART; software preparation and bounded local memory'}
    def save(status):
        report['status']=status;report['elapsed_seconds']=time.monotonic()-started
        report_path.parent.mkdir(parents=True,exist_ok=True);report_path.write_text(json.dumps(report,indent=2)+'\n')
    save('running')
    try:
        for backend,binary in binaries.items():
            observations[backend]=[]
            for length in LENGTHS:
                if digest(binary)!=identities[backend]['binary_sha256']:raise ValueError('C workload simulator changed')
                run=subprocess.run([str(binary),'--upload',str(packets[length])],cwd=ROOT,
                    capture_output=True,text=True,check=True,timeout=7200)
                uart=json.loads(run.stdout);replies,frames=parse_frames(uart['uart'])
                if [reply['status'] for reply in replies]!=['ready','committed'] or len(frames)!=1:
                    raise ValueError('compiled workload did not complete upload and execution')
                expected=zlib.crc32(bytes(index%256 for index in range(length))) if length<=1024 else 0xffffffff
                check_expected(frames[0],[expected])
                # Confirm the result checker rejects a deliberately wrong answer.
                wrong=dict(frames[0],values=[expected^1])
                try:check_expected(wrong,[expected])
                except AssertionError:pass
                else:raise ValueError('compiled-workload oracle accepted a wrong value')
                item={'length':length,'expected_crc32':expected,'prepared':prepared[length],
                    'uart':uart,'result':frames[0],'wrong_result_rejected':True}
                if backend=='mapped' and item!=observations['rtl'][len(observations[backend])]:
                    raise ValueError('compiler workload RTL and mapped UART/results/cycles differ')
                observations[backend].append(item);save('running')
                print(f'PASS {backend} compiled C CRC-32 length {length}, {frames[0]["cycles"]} invocation cycles',flush=True)
            if verify_simulator(binary)!=identities[backend]:raise ValueError('compiled-workload model identity changed')
        if digest(wasm)!=wasm_hash or any(digest(ROOT/name)!=value for name,value in inputs.items()):
            raise ValueError('C workload inputs changed')
        for identity in (compiler,linker):
            if digest(Path(identity['path']))!=identity['sha256']:raise ValueError('C toolchain changed during verification')
        for length,path in packets.items():
            if digest(path)!=prepared[length]['packet_sha256']:raise ValueError('compiled upload packet changed')
        save('passed')
    except BaseException as error:
        report['error']=f'{type(error).__name__}: {error}';save('failed');raise


if __name__=='__main__':main()
