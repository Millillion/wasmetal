#!/usr/bin/env python3
"""Verify destructive startup testing and CPU handoff at actual SRAM adapter pins."""
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

CONFIGURATIONS=((16,1,9),(80,3,11),(272,7,10),(131072,3,11),(80,3,5),(80,3,2))
TOP='wasmetal_startup_sram'
BINDING=ROOT/'tests/asic/wasmetal_startup_sram.sv'
HARNESS=ROOT/'tests/asic/startup_sram.cpp'
SOURCE=ROOT/'soc/asic/wasmetal_memory_startup.sv'
DEPENDENCIES=[ROOT/'soc/asic/wasmetal_memory_bist.sv',ROOT/'soc/asic/wasmetal_sram_memory.sv']

def native(source,directory,size,latency,timeout):
    directory.mkdir(parents=True,exist_ok=True)
    flags=f' -DTEST_BYTES={size} -DTEST_LATENCY={latency} -DTEST_TIMEOUT={timeout}'
    command=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL','--assert',
        '-DWASMETAL_ASSERTIONS',f'-GRAM_BYTES={size}',f'-GREAD_LATENCY={latency}',f'-GRESPONSE_TIMEOUT={timeout}',
        '--top-module',TOP,'--cc','--exe','--build','-j','2','--Mdir',str(directory/'obj'),
        '-CFLAGS','-std=c++17 -O2 -Wall -Wextra -Werror'+flags,*map(str,DEPENDENCIES),str(source),str(BINDING),str(HARNESS)]
    with (directory/'build.log').open('w') as log:
        subprocess.run(command,cwd=ROOT,env=dict(os.environ,VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),
                       stdout=log,stderr=subprocess.STDOUT,check=True,timeout=300)
    return directory/('obj/V'+TOP)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--mapped',action='store_true')
    args=parser.parse_args();started=time.monotonic();directory=ROOT/'build/memory-startup';directory.mkdir(parents=True,exist_ok=True)
    output=ROOT/'reports'/('memory-startup-mapped.json' if args.mapped else 'memory-startup.json')
    output.parent.mkdir(exist_ok=True);output.unlink(missing_ok=True)
    mutations=[
        ('early-handoff','cpu_enabled=test_done && !test_failed && !reset;',
         'cpu_enabled=launched && !test_failed && !reset;','startup enabled CPU before full test'),
        ('failed-test-grants-cpu','cpu_enabled=test_done && !test_failed && !reset;',
         'cpu_enabled=test_done && !reset;','startup enabled CPU before full test'),
        ('restarted-test','else launched<=1;','else launched<=test_busy;',
         'startup revoked successful ownership without reset'),
        ('test-response-leak','cpu_ready=cpu_enabled && cpu_valid && memory_ready;',
         'cpu_ready=cpu_valid && memory_ready;','startup exposed CPU response before handoff'),
        ('wrong-cpu-mask','memory_mask=cpu_enabled ? cpu_mask : test_mask;',
         "memory_mask=cpu_enabled ? cpu_mask & 16'hfffe : test_mask;",'startup CPU macro byte mask mismatch'),
        ('reset-grant-retained','cpu_enabled=test_done && !test_failed && !reset;',
         'cpu_enabled=test_done && !test_failed;','startup reset did not isolate access'),
        ('wrong-cpu-read','cpu_rdata=cpu_enabled ? memory_rdata : 128\'b0;',
         "cpu_rdata=cpu_enabled ? memory_rdata ^ 128'h1 : 128'b0;",'startup CPU response data differs from SRAM oracle')]
    for name,old,_,_ in mutations:
        if SOURCE.read_text().count(old)!=1:raise ValueError('ambiguous startup fault: '+name)
    paths=[SOURCE,BINDING,HARNESS,*DEPENDENCIES,Path(__file__).resolve(),ROOT/'tools/build_standalone_gate_sim.py',
        ROOT/'tools/build_board.py',ROOT/'tools/prepare_standalone.py',ROOT/'tools/upstream.lock.json',
        ROOT/'.cache/tools/usr/bin/verilator_bin',ROOT/'.cache/tools/usr/bin/yosys']
    inputs={str(p.relative_to(ROOT)):digest(p) for p in paths};checks=[]
    for size,latency,timeout in CONFIGURATIONS:
        target=directory/f'{size}-{latency}-{timeout}';target.mkdir(exist_ok=True)
        binaries={'rtl':native(SOURCE,target/'native',size,latency,timeout)};counts={};mapping=None
        if args.mapped:
            netlist=target/'mapped.json'
            script='read_verilog -sv '+' '.join(map(str,[*DEPENDENCIES,SOURCE,BINDING]))+'\n'
            script+=f'chparam -set RAM_BYTES {size} -set READ_LATENCY {latency} -set RESPONSE_TIMEOUT {timeout} {TOP}\n'
            script+=f'synth_ecp5 -top {TOP} -json {netlist}\ncheck -assert\n';yosys(script,'synthesis',target)
            counts=dict(Counter(c['type'] for c in json.loads(netlist.read_text())['modules'][TOP]['cells'].values()))
            netlist.with_suffix('.manifest.json').write_text(json.dumps({'inputs':inputs,'netlist_sha256':digest(netlist)},indent=2)+'\n')
            binaries['mapped']=build_mapped(netlist,target/'mapped-model',top=TOP,harness=HARNESS,
                cflags=f' -DTEST_BYTES={size} -DTEST_LATENCY={latency} -DTEST_TIMEOUT={timeout}')
            mapping=json.loads(Path(str(binaries['mapped'])+'.build.json').read_text())
        results={}
        for backend,binary in binaries.items():
            log=target/(backend+'-observations.log')
            with log.open('w') as stream:
                subprocess.run([str(binary)],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,check=True,timeout=900)
            results[backend]={'binary_sha256':digest(binary),'log_sha256':digest(log),'observations':json.loads(log.read_text())}
            print('PASS',size,latency,timeout,backend,results[backend]['observations'],flush=True)
        if args.mapped and results['rtl']['observations']!=results['mapped']['observations']:
            raise ValueError('startup RTL and mapped observations differ')
        checks.append({'ram_bytes':size,'read_latency':latency,'response_timeout':timeout,
                       'tests':results,'mapped_primitives':counts,'mapped_identity':mapping})
    controls=[]
    for name,old,new,message in mutations:
        target=directory/'negative'/name;target.mkdir(parents=True,exist_ok=True)
        mutant=target/'wasmetal_memory_startup.sv';mutant.write_text(SOURCE.read_text().replace(old,new))
        binary=native(mutant,target/'native',80,3,11)
        run=subprocess.run([str(binary)],cwd=ROOT,capture_output=True,text=True,timeout=180)
        log=target/'rejection.log';log.write_text(run.stdout+run.stderr)
        if run.returncode==0 or message not in log.read_text():raise ValueError('startup fault not rejected: '+name)
        controls.append({'name':name,'source_sha256':digest(mutant),'binary_sha256':digest(binary),
                         'log_sha256':digest(log),'reason':log.read_text().strip(),'exit_code':run.returncode})
        print('REJECTED',name,flush=True)
    binary=directory/('80-3-11/native/obj/V'+TOP)
    run=subprocess.run([str(binary),'--corrupt-read'],cwd=ROOT,capture_output=True,text=True,timeout=180)
    log=directory/'corrupt-read.log';log.write_text(run.stdout+run.stderr)
    if run.returncode==0 or 'startup healthy memory did not grant CPU' not in log.read_text():
        raise ValueError('corrupted startup SRAM model was accepted')
    controls.append({'name':'corrupt-read','binary_sha256':digest(binary),'log_sha256':digest(log),
                     'reason':log.read_text().strip(),'exit_code':run.returncode})
    for name,sha in inputs.items():
        if digest(ROOT/name)!=sha:raise ValueError('startup input changed: '+name)
    report={'status':'passed','scope':'startup test, CPU ownership and real SRAM adapter checked at independent macro pins',
        'inputs':inputs,'checks':checks,'negative_controls':controls,'negative_controls_rejected':len(controls),
        'physical_hardware_tested':False,'default_cpu_integration':False,'elapsed_seconds':time.monotonic()-started,
        'limitations':['CPU requests are driven by an independent transaction generator, not the complete CPU.',
            'Every shared reset restarts the destructive test; warm-reset retention is not implemented.',
            'The SRAM is a functional model, not a foundry macro or physical timing model.',
            'RTL and ECP5 functional mapping do not establish ASIC standard-cell or physical-board correctness.']}
    output.write_text(json.dumps(report,indent=2)+'\n');print('PASS memory startup and eight fault controls',flush=True)


if __name__=='__main__':main()
