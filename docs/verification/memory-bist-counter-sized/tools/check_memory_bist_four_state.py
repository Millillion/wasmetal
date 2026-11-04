#!/usr/bin/env python3
"""Check simulation unknown-data diagnostics and reset isolation of the test master."""
import json
from pathlib import Path
import subprocess
from prepare_standalone import ROOT,digest


def main():
    directory=ROOT/'build/memory-bist-four-state';directory.mkdir(parents=True,exist_ok=True)
    source=ROOT/'soc/asic/wasmetal_memory_bist.sv';bench=ROOT/'tests/memory/bist_four_state.sv'
    output=ROOT/'reports/memory-bist-four-state.json';output.unlink(missing_ok=True)
    inputs={str(p.relative_to(ROOT)):digest(p) for p in
        [source,bench,Path(__file__).resolve(),ROOT/'tools/upstream.lock.json',ROOT/'.cache/tools/usr/bin/iverilog',ROOT/'.cache/tools/usr/bin/vvp']}
    def execute(path,name):
        binary=directory/(name+'.vvp');log=directory/(name+'.log');compiler=directory/(name+'-compile.log')
        command=[str(ROOT/'.cache/tools/usr/bin/iverilog'),'-B'+str(ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl'),
            '-g2012','-s','bist_four_state_tb','-o',str(binary),str(path),str(bench)]
        with compiler.open('w') as stream:
            subprocess.run(command,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,check=True,timeout=30)
        run=subprocess.run([str(ROOT/'.cache/tools/usr/bin/vvp'),str(binary)],cwd=ROOT,capture_output=True,text=True,timeout=30)
        log.write_text(run.stdout+run.stderr);return run,log
    run,log=execute(source,'positive');run.check_returncode()
    if 'PASS BIST four-state' not in run.stdout:raise ValueError('four-state checks did not finish')
    controls=[]
    for name,old,new,message in [
        ('unknown-not-diagnosed','wire mismatch=rdata!==expected_read;','wire mismatch=rdata!=expected_read;',
         'BIST unknown read was not diagnosed'),
        ('reset-not-isolated','assign valid=state==REQUEST && !reset;','assign valid=state==REQUEST;',
         'BIST reset did not isolate pending request')]:
        text=source.read_text()
        if text.count(old)!=1:raise ValueError('ambiguous four-state mutation')
        path=directory/(name+'.sv');path.write_text(text.replace(old,new))
        negative,faultlog=execute(path,name)
        if negative.returncode==0 or message not in negative.stdout+negative.stderr:
            raise ValueError('four-state check did not reject '+name)
        controls.append({'name':name,'log_sha256':digest(faultlog),'source_sha256':digest(path)})
    for name,value in inputs.items():
        if digest(ROOT/name)!=value:raise ValueError('four-state input changed: '+name)
    report={'status':'passed','scope':'RTL simulation X/Z diagnostics, unknown initial memory and reset isolation',
        'inputs':inputs,'positive_log_sha256':digest(log),'negative_controls':controls,
        'negative_controls_rejected':len(controls),'physical_hardware_tested':False,
        'limitations':['Simulation X/Z diagnosis is not an electrical metastability detector.',
                       'The mapped binary-input campaign has a separate report.']}
    output.parent.mkdir(exist_ok=True);output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS BIST four-state campaign and two deliberately broken implementations')


if __name__=='__main__':main()
