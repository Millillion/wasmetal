#!/usr/bin/env python3
"""Verify the destructive memory-test master with independent memory faults."""
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import subprocess
import time

from build_board import yosys
from build_standalone_gate_sim import build as build_mapped
from prepare_standalone import ROOT, digest

CONFIGURATIONS=((80,32),(16,16),(131072,1024))


def native(source,directory,size,timeout):
    directory.mkdir(parents=True,exist_ok=True)
    command=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL','--assert',
        '-DWASMETAL_ASSERTIONS',f'-GRAM_BYTES={size}',f'-GRESPONSE_TIMEOUT={timeout}',
        '--top-module','wasmetal_memory_bist','--cc','--exe','--build','-j','2',
        '--Mdir',str(directory/'obj'),'-CFLAGS',
        f'-std=c++17 -O2 -Wall -Wextra -Werror -DTEST_BYTES={size} -DTEST_TIMEOUT={timeout}',
        str(source),str(ROOT/'tests/memory/bist.cpp')]
    with (directory/'build.log').open('w') as stream:
        subprocess.run(command,cwd=ROOT,env=dict(os.environ,VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),
                       stdout=stream,stderr=subprocess.STDOUT,check=True,timeout=300)
    return directory/'obj/Vwasmetal_memory_bist'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mapped',action='store_true')
    args=parser.parse_args()
    started=time.monotonic();directory=ROOT/'build/memory-bist'
    directory.mkdir(parents=True,exist_ok=True)
    output=ROOT/'reports'/('memory-bist-mapped.json' if args.mapped else 'memory-bist.json')
    output.parent.mkdir(exist_ok=True);output.unlink(missing_ok=True)
    source=ROOT/'soc/asic/wasmetal_memory_bist.sv'
    paths=[source,ROOT/'tests/memory/bist.cpp',Path(__file__).resolve(),ROOT/'tools/build_standalone_gate_sim.py',
           ROOT/'tools/build_board.py',ROOT/'tools/prepare_standalone.py',ROOT/'tools/upstream.lock.json',
           ROOT/'.cache/tools/usr/bin/verilator_bin',ROOT/'.cache/tools/usr/bin/yosys']
    inputs={str(p.relative_to(ROOT)):digest(p) for p in paths}
    checks=[]
    for size,timeout in CONFIGURATIONS:
        target=directory/f'{size}-{timeout}';target.mkdir(exist_ok=True)
        binaries={'rtl':native(source,target/'native',size,timeout)}
        counts={};mapping=None
        if args.mapped:
            netlist=target/'mapped.json'
            yosys(f'read_verilog -sv {source}\nchparam -set RAM_BYTES {size} -set RESPONSE_TIMEOUT {timeout} wasmetal_memory_bist\n'
                  f'synth_ecp5 -top wasmetal_memory_bist -json {netlist}\ncheck -assert\n','synthesis',target)
            counts=dict(Counter(c['type'] for c in json.loads(netlist.read_text())['modules']['wasmetal_memory_bist']['cells'].values()))
            netlist.with_suffix('.manifest.json').write_text(json.dumps({'inputs':inputs,'netlist_sha256':digest(netlist)},indent=2)+'\n')
            binaries['mapped']=build_mapped(netlist,target/'mapped-model',top='wasmetal_memory_bist',
                harness=ROOT/'tests/memory/bist.cpp',cflags=f' -DTEST_BYTES={size} -DTEST_TIMEOUT={timeout}')
            mapping=json.loads(Path(str(binaries['mapped'])+'.build.json').read_text())
        results={}
        for backend,binary in binaries.items():
            log=target/(backend+'-observations.log')
            with log.open('w') as stream:
                subprocess.run([str(binary)],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,check=True,timeout=600)
            results[backend]={'binary_sha256':digest(binary),'observations':json.loads(log.read_text()),
                              'log_sha256':digest(log)}
            print('PASS',size,timeout,backend,results[backend]['observations'],flush=True)
        if args.mapped and results['rtl']['observations']!=results['mapped']['observations']:
            raise ValueError('RTL and mapped memory-test traces differ')
        checks.append({'ram_bytes':size,'response_timeout':timeout,'tests':results,
                       'mapped_primitives':counts,'mapped_identity':mapping})
    mutations=[
        ('wrong-background','assign wdata=(phase==1 || phase==3) ? ~background : background;',
         "assign wdata=((phase==1 || phase==3) ? ~background : background) ^ 128'h1;"),
        ('missing-read-check','if(failed || fault || (!write && mismatch))','if(failed || fault)'),
        ('wrong-descent','wire descending=phase==3 || phase==4;',"wire descending=1'b0;"),
        ('timeout-withdraws-request','assign valid=state==REQUEST && !reset;','assign valid=state==REQUEST && !reset && !failed;'),
        ('wrong-observed-data','observed_data<=rdata;',"observed_data<=rdata ^ 128'h1;"),
        ('missing-diagnostic-reset','error_address<=0;expected_data<=0;observed_data<=0;completed_operations<=0;',
         'error_address<=0;observed_data<=0;completed_operations<=0;')]
    controls=[];original=source.read_text()
    for name,old,new in mutations:
        if original.count(old)!=(2 if name=='missing-diagnostic-reset' else 1):
            raise ValueError('ambiguous fault mutation: '+name)
        target=directory/'negative'/name;target.mkdir(parents=True,exist_ok=True)
        mutant=target/'wasmetal_memory_bist.sv';mutant.write_text(original.replace(old,new,1))
        binary=native(mutant,target/'native',80,32)
        run=subprocess.run([str(binary)],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        log=target/'rejection.log';log.write_bytes(run.stdout)
        if run.returncode==0 or b'BIST ' not in run.stdout:raise ValueError('independent checker did not reject '+name)
        controls.append({'name':name,'source_sha256':digest(mutant),'binary_sha256':digest(binary),
                         'exit_code':run.returncode,'log_sha256':digest(log),'reason':run.stdout.decode().strip()})
        print('REJECTED',name,flush=True)
    for name,value in inputs.items():
        if digest(ROOT/name)!=value:raise ValueError('memory-test verification input changed: '+name)
    result={'status':'passed','scope':'independent March-sequence and memory-fault simulations; no manufacturing qualification',
            'inputs':inputs,'checks':checks,'negative_controls':controls,'negative_controls_rejected':len(controls),
            'physical_hardware_tested':False,'default_cpu_integration':False,'elapsed_seconds':time.monotonic()-started,
            'limitations':['Destructive exclusive-access component; caller must arbitrate and stop the CPU.',
                'Binary fault models do not establish coverage of every physical, retention, linked or analog fault.',
                'A permanent timeout retains the outstanding request; reset the test master and controller together.',
                'Functional ECP5 mapping is not an ASIC standard-cell implementation.']}
    output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS memory self-test campaign and six deliberately broken implementations',flush=True)


if __name__=='__main__':main()
