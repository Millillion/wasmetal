#!/usr/bin/env python3
"""Execute compiled C through the SDRAM-backed CPU with independent CRC results."""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import time
import zlib
from check_c_workload import LENGTHS,tool
from check_loadable import parse_frames
from check_standalone import check_expected
from prepare_standalone import ROOT,prepare,digest
from program_upload import encode
from standalone_support import verify_simulator


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--timing',choices=('25mhz','100mhz'),required=True)
    parser.add_argument('--startup-cycles',type=int)
    args=parser.parse_args();started=time.monotonic()
    if args.startup_cycles is not None and args.startup_cycles<1:
        parser.error('--startup-cycles must be positive')
    label='sdram-c-'+args.timing+(f'-{args.startup_cycles}' if args.startup_cycles else '')
    directory=ROOT/'build'/label;directory.mkdir(parents=True,exist_ok=True)
    report_path=ROOT/'reports'/(label+'.json');report_path.unlink(missing_ok=True)
    # Reuse the reviewed system builder byte for byte except for its output
    # directory prefix. Separate binaries preserve the system campaign's fixed
    # coverage output. Neither an existing circuit nor its evidence is changed.
    parent=ROOT/'tools/check_sdram_system.py';text=parent.read_text()
    before="label=f'sdram-system-{timing}-";after="label=f'sdram-c-system-{timing}-"
    if text.count(before)!=1:raise ValueError('review SDRAM C builder isolation')
    copied=directory/'builder.py';copied.write_text(text.replace(before,after))
    spec=importlib.util.spec_from_file_location('wasmetal_sdram_c_builder',copied)
    builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
    source=ROOT/'examples/c/crc32.c'
    inputs={str(p.relative_to(ROOT)):digest(p) for p in [source,parent,copied,Path(__file__).resolve(),
        ROOT/'tools/check_c_workload.py',ROOT/'tools/check_loadable.py',ROOT/'tools/check_standalone.py',
        ROOT/'tools/prepare_standalone.py',ROOT/'tools/program_upload.py',ROOT/'tools/standalone_support.py']}
    binary,model_directory,device=builder.build(args.timing,args.startup_cycles,None)
    identity=verify_simulator(binary);coverage=model_directory/'coverage.jsonl';coverage.unlink(missing_ok=True)
    compiler=tool('clang-18');linker=tool('wasm-ld-18');obj=directory/'crc32.o';wasm=directory/'crc32.wasm'
    commands={'compile':[compiler['path'],'--target=wasm32','-std=c11','-O2','-Wall','-Wextra','-Werror',
        '-ffreestanding','-fno-builtin','-c',str(source),'-o',str(obj)],
        'link':[linker['path'],'--no-entry','--export=checksum','--stack-first','-z','stack-size=16384',
            '--initial-memory=65536','--max-memory=65536',str(obj),'-o',str(wasm)]}
    for stage,command in commands.items():
        run=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
        (directory/(stage+'.log')).write_text(run.stdout+run.stderr)
        run.check_returncode()
    wasm_hash=digest(wasm);results=[];artifacts={}
    for length in LENGTHS:
        image=directory/f'image-{length}';manifest=prepare(wasm,image,export='checksum',arguments=[length])
        packet=directory/f'crc32-{length}.wmu';packet.write_bytes(encode(image,0x574d430000000000+length).bytes())
        artifacts[packet]=digest(packet);artifacts[image/'manifest.json']=digest(image/'manifest.json')
        if digest(binary)!=identity['binary_sha256']:
            raise ValueError('SDRAM C simulator changed before execution')
        run=subprocess.run([str(binary),'--upload',str(packet)],cwd=ROOT,
            capture_output=True,text=True,timeout=1800)
        (directory/f'execution-{length}.log').write_text(run.stdout+run.stderr);run.check_returncode()
        uart=json.loads(run.stdout);replies,frames=parse_frames(uart['uart'])
        if [r['status'] for r in replies]!=['ready','committed'] or len(frames)!=1:
            raise ValueError('compiled SDRAM workload did not finish its upload and execution')
        expected=zlib.crc32(bytes(n%256 for n in range(length))) if length<=1024 else 0xffffffff
        check_expected(frames[0],[expected])
        try:check_expected(dict(frames[0],values=[expected^1]),[expected])
        except AssertionError:pass
        else:raise ValueError('SDRAM C result checker accepted a wrong value')
        results.append({'length':length,'expected_crc32':expected,'uart':uart,'result':frames[0],
            'wrong_result_rejected':True,'packet_sha256':artifacts[packet],
            'image_manifest_sha256':artifacts[image/'manifest.json'],'counts':manifest['counts']})
        print(f'PASS SDRAM {args.timing} compiled C length {length}: {frames[0]["cycles"]} invocation cycles',flush=True)
    samples=[json.loads(line) for line in coverage.read_text().splitlines()]
    if len(samples)!=len(LENGTHS) or any(s['maximum_refresh_gap']>device['REFRESH_CYCLES'] for s in samples):
        raise ValueError('incomplete or invalid SDRAM C device coverage')
    if sum(s['reads'] for s in samples)==0 or sum(s['writes'] for s in samples)==0:
        raise ValueError('compiled C did not exercise SDRAM reads and writes')
    if verify_simulator(binary)!=identity:raise ValueError('SDRAM C simulator changed')
    if any(digest(ROOT/n)!=h for n,h in inputs.items()) or digest(wasm)!=wasm_hash:
        raise ValueError('SDRAM C verification inputs changed')
    if any(digest(p)!=h for p,h in artifacts.items()):
        raise ValueError('SDRAM C upload packet or image manifest changed')
    for t in (compiler,linker):
        if digest(Path(t['path']))!=t['sha256']:raise ValueError('C compiler/linker changed')
    report={'status':'passed','scope':'compiled C through complete CPU and behavioral SDRAM pins; RTL only',
        'device_parameters':device,'model':identity,'compiler':compiler,'linker':linker,'commands':commands,
        'wasm_sha256':wasm_hash,'inputs':inputs,'cases':results,'device_coverage':samples,
        'coverage_sha256':digest(coverage),'elapsed_seconds':time.monotonic()-started,'physical_hardware_tested':False}
    report_path.parent.mkdir(exist_ok=True);report_path.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
