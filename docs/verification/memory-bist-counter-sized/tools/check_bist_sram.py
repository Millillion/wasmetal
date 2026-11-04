#!/usr/bin/env python3
"""Verify the memory self-test and SRAM adapter together at the macro pins."""
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import subprocess
import time

from build_board import yosys
from build_standalone_gate_sim import build as build_mapped
from prepare_standalone import ROOT,digest

# Include non-power-of-two capacities, the largest configured array, a tight
# successful read deadline, and deadlines that expire on reads and on writes.
CONFIGURATIONS=((16,1,9),(80,3,11),(272,7,10),(131072,3,11),(80,3,5),(80,3,2))


def native(source,directory,size,latency,timeout):
    directory.mkdir(parents=True,exist_ok=True)
    flags=f' -DTEST_BYTES={size} -DTEST_LATENCY={latency} -DTEST_TIMEOUT={timeout}'
    command=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL','--assert',
        '-DWASMETAL_ASSERTIONS',f'-GRAM_BYTES={size}',f'-GREAD_LATENCY={latency}',f'-GRESPONSE_TIMEOUT={timeout}',
        '--top-module','wasmetal_bist_sram','--cc','--exe','--build','-j','2',
        '--Mdir',str(directory/'obj'),'-CFLAGS','-std=c++17 -O2 -Wall -Wextra -Werror'+flags,
        str(ROOT/'soc/asic/wasmetal_memory_bist.sv'),str(ROOT/'soc/asic/wasmetal_sram_memory.sv'),
        str(source),str(ROOT/'tests/asic/bist_sram.cpp')]
    with (directory/'build.log').open('w') as log:
        subprocess.run(command,cwd=ROOT,env=dict(os.environ,VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),
                       stdout=log,stderr=subprocess.STDOUT,check=True,timeout=300)
    return directory/'obj/Vwasmetal_bist_sram'


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--mapped',action='store_true')
    args=parser.parse_args();started=time.monotonic();directory=ROOT/'build/bist-sram';directory.mkdir(parents=True,exist_ok=True)
    output=ROOT/'reports'/('bist-sram-mapped.json' if args.mapped else 'bist-sram.json')
    output.parent.mkdir(exist_ok=True);output.unlink(missing_ok=True)
    source=ROOT/'tests/asic/wasmetal_bist_sram.sv'
    mutations=[
        ('wrong-read-latency','.READ_LATENCY(READ_LATENCY)', '.READ_LATENCY(READ_LATENCY+1)',
         'BIST SRAM unexpected failure'),
        ('reset-not-shared','.clk(clk),.reset(reset),.valid(request_valid)',
         ".clk(clk),.reset(1'b0),.valid(request_valid)",'BIST SRAM reset did not isolate macro strobes'),
        ('wrong-byte-enables','.address(request_address),.mask(request_mask),.wdata(request_data)',
         ".address(request_address),.mask(request_mask & 16'hfffe),.wdata(request_data)",
         'BIST SRAM incomplete macro byte enables')]
    for name,old,_,_ in mutations:
        if source.read_text().count(old)!=1:raise ValueError('ambiguous SRAM integration fault: '+name)
    paths=[source,ROOT/'soc/asic/wasmetal_memory_bist.sv',ROOT/'soc/asic/wasmetal_sram_memory.sv',
           ROOT/'tests/asic/bist_sram.cpp',Path(__file__).resolve(),ROOT/'tools/build_standalone_gate_sim.py',
           ROOT/'tools/build_board.py',ROOT/'tools/prepare_standalone.py',ROOT/'tools/upstream.lock.json',
           ROOT/'.cache/tools/usr/bin/verilator_bin',ROOT/'.cache/tools/usr/bin/yosys']
    inputs={str(path.relative_to(ROOT)):digest(path) for path in paths};checks=[]
    for size,latency,timeout in CONFIGURATIONS:
        target=directory/f'{size}-{latency}-{timeout}';target.mkdir(exist_ok=True)
        binaries={'rtl':native(source,target/'native',size,latency,timeout)};counts={};mapping=None
        if args.mapped:
            netlist=target/'mapped.json'
            script='read_verilog -sv '+str(ROOT/'soc/asic/wasmetal_memory_bist.sv')+' '+str(ROOT/'soc/asic/wasmetal_sram_memory.sv')+' '+str(source)+'\n'
            script+=f'chparam -set RAM_BYTES {size} -set READ_LATENCY {latency} -set RESPONSE_TIMEOUT {timeout} wasmetal_bist_sram\n'
            script+=f'synth_ecp5 -top wasmetal_bist_sram -json {netlist}\ncheck -assert\n'
            yosys(script,'synthesis',target)
            counts=dict(Counter(cell['type'] for cell in json.loads(netlist.read_text())['modules']['wasmetal_bist_sram']['cells'].values()))
            netlist.with_suffix('.manifest.json').write_text(json.dumps({'inputs':inputs,'netlist_sha256':digest(netlist)},indent=2)+'\n')
            binaries['mapped']=build_mapped(netlist,target/'mapped-model',top='wasmetal_bist_sram',
                harness=ROOT/'tests/asic/bist_sram.cpp',cflags=f' -DTEST_BYTES={size} -DTEST_LATENCY={latency} -DTEST_TIMEOUT={timeout}')
            mapping=json.loads(Path(str(binaries['mapped'])+'.build.json').read_text())
        results={}
        for backend,binary in binaries.items():
            log=target/(backend+'-observations.log')
            with log.open('w') as stream:
                subprocess.run([str(binary)],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,check=True,timeout=900)
            results[backend]={'binary_sha256':digest(binary),'log_sha256':digest(log),'observations':json.loads(log.read_text())}
            print('PASS',size,latency,timeout,backend,results[backend]['observations'],flush=True)
        if args.mapped and results['rtl']['observations']!=results['mapped']['observations']:
            raise ValueError('SRAM integration RTL and mapped observations differ')
        checks.append({'ram_bytes':size,'read_latency':latency,'response_timeout':timeout,
                       'tests':results,'mapped_primitives':counts,'mapped_identity':mapping})
    controls=[]
    for name,old,new,message in mutations:
        text=source.read_text()
        if text.count(old)!=1:raise ValueError('ambiguous SRAM integration fault: '+name)
        target=directory/'negative'/name;target.mkdir(parents=True,exist_ok=True)
        mutant=target/'wasmetal_bist_sram.sv';mutant.write_text(text.replace(old,new))
        binary=native(mutant,target/'native',80,3,11)
        run=subprocess.run([str(binary)],cwd=ROOT,capture_output=True,text=True,timeout=180)
        log=target/'rejection.log';log.write_text(run.stdout+run.stderr)
        if run.returncode==0 or message not in log.read_text():raise ValueError('integration fault was not rejected: '+name)
        controls.append({'name':name,'source_sha256':digest(mutant),'binary_sha256':digest(binary),
                         'log_sha256':digest(log),'reason':log.read_text().strip(),'exit_code':run.returncode})
        print('REJECTED',name,flush=True)
    binary=directory/'80-3-11/native/obj/Vwasmetal_bist_sram'
    run=subprocess.run([str(binary),'--corrupt-read'],cwd=ROOT,capture_output=True,text=True,timeout=180)
    log=directory/'corrupt-read.log';log.write_text(run.stdout+run.stderr)
    if run.returncode==0 or 'BIST SRAM unexpected failure' not in log.read_text():raise ValueError('corrupted SRAM oracle was accepted')
    controls.append({'name':'corrupt-read','binary_sha256':digest(binary),'log_sha256':digest(log),
                     'reason':log.read_text().strip(),'exit_code':run.returncode})
    for name,value in inputs.items():
        if digest(ROOT/name)!=value:raise ValueError('SRAM integration input changed: '+name)
    report={'status':'passed','scope':'self-test master plus SRAM adapter checked at independent macro pins',
            'inputs':inputs,'checks':checks,'negative_controls':controls,'negative_controls_rejected':len(controls),
            'physical_hardware_tested':False,'default_cpu_integration':False,'elapsed_seconds':time.monotonic()-started,
            'limitations':['The independent SRAM is a functional model, not a foundry macro or physical timing model.',
                'This exclusive-access verification binding does not supply CPU arbitration or boot sequencing.',
                'RTL and ECP5 functional mapping establish simulated behavior; no ASIC standard-cell result is claimed.']}
    output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS memory self-test SRAM integration and four fault controls',flush=True)


if __name__=='__main__':main()
