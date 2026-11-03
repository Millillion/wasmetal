#!/usr/bin/env python3
"""Check image upload against independent byte/word and reply oracles."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from build_board import yosys
from build_standalone_gate_sim import build
from prepare_standalone import ROOT,digest,load_profile
from program_upload import encode,profile_tag
sys.path.insert(0,str(ROOT/'tests'))
from program_upload_test import fixture


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--mapped',action='store_true');args=parser.parse_args()
    source=ROOT/'soc/loader/wasmetal_image_loader.sv';harness=ROOT/'tests/memory/image_loader.cpp'
    inputs=[source,harness,Path(__file__).resolve(),ROOT/'tools/program_upload.py',ROOT/'tools/standalone_support.py',
        ROOT/'tests/program_upload_test.py',ROOT/'tools/prepare_standalone.py',ROOT/'soc/profile.json',ROOT/'tools/upstream.lock.json']
    hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs};results={}
    profile=load_profile()
    for name,capacities in [('small',(4,2,8,4,2)),('production',tuple(profile[key] for key in
            ('instruction_depth','function_depth','type_depth','boot_depth','regions_per_kind')))]:
        directory=ROOT/'build/image-loader'/name;directory.mkdir(parents=True,exist_ok=True)
        params=dict(zip(('INSTRUCTION_DEPTH','FUNCTION_DEPTH','TYPE_DEPTH','BOOT_DEPTH','REGIONS_PER_KIND'),capacities))
        tag=profile_tag(profile) if name=='production' else bytes(range(16))
        params.update(TIMEOUT_CYCLES=64,PROFILE_TAG=f"128'h{int.from_bytes(tag,'little'):032x}")
        cflags=' '+' '.join(f'-D{key}={value}' for key,value in zip(('INSTRUCTIONS','FUNCTIONS','TYPES','BOOT','REGIONS'),capacities))
        cflags+=f" -DTAG_LOW=0x{int.from_bytes(tag[:8],'little'):016x}ULL -DTAG_HIGH=0x{int.from_bytes(tag[8:],'little'):016x}ULL"
        if name=='production':
            image=directory/'image';fixture(image);packet=directory/'image.wmu'
            packet.write_bytes(encode(image,0x0123456789abcdef).bytes())
        native=directory/'native';native.mkdir(exist_ok=True)
        command=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL','--assert',
            '-DWASMETAL_ASSERTIONS','--top-module','wasmetal_image_loader',
            *[f'-G{key}={value}' for key,value in params.items()],
            '--cc','--exe','--build','-j','4','--Mdir',str(native),
            '-CFLAGS','-std=c++17 -O2 -Wall -Wextra -Werror'+cflags,str(source),str(harness)]
        with (directory/'native.log').open('w') as log:
            result=subprocess.run(command,cwd=ROOT,env=dict(os.environ,
                VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),stdout=log,stderr=subprocess.STDOUT)
        if result.returncode:print((directory/'native.log').read_text()[-9000:]);result.check_returncode()
        binaries={'rtl':native/'Vwasmetal_image_loader'}
        if args.mapped:
            netlist=directory/'loader.json'
            yosys(f'read_verilog -sv {source}\nchparam '+
                ' '.join(f'-set {key} {value}' for key,value in params.items())+
                f' wasmetal_image_loader\nsynth_ecp5 -top wasmetal_image_loader -json {netlist}\ncheck -assert\n','synthesis',directory)
            netlist.with_suffix('.manifest.json').write_text(json.dumps({'inputs':hashes,'netlist_sha256':digest(netlist)},indent=2)+'\n')
            binaries['mapped']=build(netlist,directory/'mapped',top='wasmetal_image_loader',harness=harness,cflags=cflags)
        tests={}
        for backend,binary in binaries.items():
            result=subprocess.run([str(binary)],cwd=ROOT,capture_output=True,text=True,timeout=180)
            if result.returncode:raise RuntimeError(result.stdout+result.stderr)
            for flag,message in [('--corrupt-reply','loader reply differs from independent oracle'),
                                 ('--corrupt-word','image write differs from independent byte oracle')]:
                negative=subprocess.run([str(binary),flag],cwd=ROOT,capture_output=True,text=True,timeout=30)
                if negative.returncode==0 or message not in negative.stderr:
                    raise RuntimeError('loader negative control did not fail correctly: '+flag)
            tests[backend]=dict(json.loads(result.stdout),binary_sha256=digest(binary),negative_controls_rejected=['reply','store word'])
            if name=='production':
                encoded=subprocess.run([str(binary),'--packet',str(packet)],cwd=ROOT,capture_output=True,text=True,timeout=60)
                if encoded.returncode:raise RuntimeError(encoded.stdout+encoded.stderr)
                tests[backend]['python_encoded_image']=json.loads(encoded.stdout)
        if args.mapped:
            for key in ('cycles','words','replies','commits','resets','payload_bytes'):
                if tests['rtl'][key]!=tests['mapped'][key]:raise ValueError('RTL/mapped loader behavior differs: '+key)
            if name=='production' and tests['rtl']['python_encoded_image']!=tests['mapped']['python_encoded_image']:
                raise ValueError('RTL/mapped encoded image differs')
        results[name]={'parameters':params,'tests':tests}
        if args.mapped:results[name]['mapped_build']=json.loads(Path(str(binaries['mapped'])+'.build.json').read_text())
        print(name+': '+json.dumps(tests),flush=True)
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise RuntimeError('loader test inputs changed')
    report={'status':'passed','scope':'prepared-image byte transport and store write interface; no CPU or UART integration',
        'configurations':results,'inputs':hashes,'physical_hardware_tested':False}
    (ROOT/'reports'/('image-loader-mapped.json' if args.mapped else 'image-loader.json')).write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
