#!/usr/bin/env python3
"""Require reset isolation and preserve unknown SRAM read data in four states."""
import json
from pathlib import Path
import subprocess
from prepare_standalone import ROOT,digest


def main():
    directory=ROOT/'build/sram-four-state';directory.mkdir(parents=True,exist_ok=True)
    source=ROOT/'soc/asic/wasmetal_sram_memory.sv';bench=ROOT/'tests/memory/sram_four_state.sv'
    paths=[source,bench,Path(__file__).resolve(),ROOT/'tools/upstream.lock.json']
    inputs={str(path.relative_to(ROOT)):digest(path) for path in paths}
    def execute(path,name):
        executable=directory/(name+'.vvp');log=directory/(name+'.log')
        command=[str(ROOT/'.cache/tools/usr/bin/iverilog'),'-B'+str(ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl'),
            '-g2012','-s','sram_four_state_tb','-o',str(executable),str(path),str(bench)]
        subprocess.run(command,cwd=ROOT,check=True,capture_output=True,text=True,timeout=30)
        run=subprocess.run([str(ROOT/'.cache/tools/usr/bin/vvp'),str(executable)],cwd=ROOT,capture_output=True,text=True,timeout=30)
        log.write_text(run.stdout+run.stderr);return run,log
    run,log=execute(source,'positive');run.check_returncode()
    if 'PASS SRAM four-state' not in run.stdout:raise ValueError('missing SRAM four-state completion')
    rejected=[]
    for name,old,new,message in [
        ('unknown-coerced-to-zero','rdata<=sram_rdata;',"rdata<=(^sram_rdata===1'bx) ? 128'b0 : sram_rdata;",'unknown SRAM data was coerced'),
        ('missing-reset-isolation','assign sram_enable=state==ISSUE && !reset;','assign sram_enable=state==ISSUE;',
         'reset did not block unknown-state macro strobes')]:
        text=source.read_text();assert text.count(old)==1
        mutant=directory/(name+'.sv');mutant.write_text(text.replace(old,new))
        negative,_=execute(mutant,name)
        if negative.returncode==0 or message not in negative.stdout+negative.stderr:
            raise ValueError('four-state SRAM negative control failed: '+name)
        rejected.append(name)
    if any(digest(ROOT/name)!=value for name,value in inputs.items()):raise ValueError('SRAM four-state inputs changed')
    report={'status':'passed','scope':'controller reset and four-state data behavior; no foundry macro or physical timing model',
        'ram_bytes':80,'read_latency':2,'negative_controls_rejected':rejected,
        'positive_log_sha256':digest(log),'inputs':inputs,'physical_hardware_tested':False}
    (ROOT/'reports/sram-four-state.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS SRAM four-state checks and two negative controls')


if __name__=='__main__':main()
