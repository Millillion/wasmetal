#!/usr/bin/env python3
"""Check startup isolation and failed X/Z reads in four-state simulation."""
import json
from pathlib import Path
import subprocess
from prepare_standalone import ROOT,digest


def main():
    directory=ROOT/'build/memory-startup-four-state';directory.mkdir(parents=True,exist_ok=True)
    startup=ROOT/'soc/asic/wasmetal_memory_startup.sv';bist=ROOT/'soc/asic/wasmetal_memory_bist.sv'
    bench=ROOT/'tests/memory/startup_four_state.sv';output=ROOT/'reports/memory-startup-four-state.json';output.unlink(missing_ok=True)
    inputs={str(p.relative_to(ROOT)):digest(p) for p in [startup,bist,bench,Path(__file__).resolve(),
        ROOT/'tools/prepare_standalone.py',ROOT/'tools/upstream.lock.json',ROOT/'.cache/tools/usr/bin/iverilog',ROOT/'.cache/tools/usr/bin/vvp']}
    def execute(controller,master,name):
        binary=directory/(name+'.vvp');log=directory/(name+'.log');compiler=directory/(name+'-compile.log')
        command=[str(ROOT/'.cache/tools/usr/bin/iverilog'),'-B'+str(ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl'),
                 '-g2012','-s','startup_four_state_tb','-o',str(binary),str(master),str(controller),str(bench)]
        with compiler.open('w') as stream:
            subprocess.run(command,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,check=True,timeout=30)
        run=subprocess.run([str(ROOT/'.cache/tools/usr/bin/vvp'),str(binary)],cwd=ROOT,capture_output=True,text=True,timeout=30)
        log.write_text(run.stdout+run.stderr);return run,log
    run,log=execute(startup,bist,'positive');run.check_returncode()
    if 'PASS startup four-state' not in run.stdout:raise ValueError('four-state startup did not finish')
    controls=[]
    for name,source,old,new,message in [
        ('test-data-leak',startup,"cpu_rdata=cpu_enabled ? memory_rdata : 128'b0;",'cpu_rdata=memory_rdata;',
         'startup leaked test response to CPU'),
        ('unknown-not-diagnosed',bist,'wire mismatch=rdata!==expected_read;','wire mismatch=rdata!=expected_read;',
         'startup unknown memory granted CPU'),
        ('reset-retains-grant',startup,'cpu_enabled=test_done && !test_failed && !reset;','cpu_enabled=test_done && !test_failed;',
         'startup reset retained CPU ownership')]:
        text=source.read_text()
        if text.count(old)!=1:raise ValueError('ambiguous startup four-state fault: '+name)
        mutant=directory/(name+'.sv');mutant.write_text(text.replace(old,new))
        negative,faultlog=execute(mutant if source==startup else startup,mutant if source==bist else bist,name)
        if negative.returncode==0 or message not in faultlog.read_text():raise ValueError('startup four-state fault not rejected: '+name)
        controls.append({'name':name,'source_sha256':digest(mutant),'log_sha256':digest(faultlog)})
    for name,sha in inputs.items():
        if digest(ROOT/name)!=sha:raise ValueError('startup four-state input changed: '+name)
    report={'status':'passed','scope':'RTL four-state startup isolation, X/Z memory diagnostics and queued CPU handoff',
        'inputs':inputs,'positive_log_sha256':digest(log),'negative_controls':controls,'negative_controls_rejected':len(controls),
        'physical_hardware_tested':False,'limitations':['X/Z simulation diagnostics are not an electrical metastability detector.',
            'Binary RTL/mapped SRAM integration and unbounded protocol proofs are separate checks.']}
    output.parent.mkdir(exist_ok=True);output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS startup four-state checks and three fault controls')


if __name__=='__main__':main()
