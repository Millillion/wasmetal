#!/usr/bin/env python3
"""Check unknown SDRAM requests and read data with real four-state simulation."""
import json
from pathlib import Path
import subprocess
from prepare_standalone import ROOT,digest


def main():
    source=ROOT/'soc/sdram/wasmetal_sdram_memory.sv';bench=ROOT/'tests/memory/sdram_four_state.sv'
    report=ROOT/'reports/sdram-four-state.json';report.unlink(missing_ok=True)
    directory=ROOT/'build/sdram-four-state';directory.mkdir(parents=True,exist_ok=True)
    paths=[source,bench,Path(__file__).resolve(),ROOT/'tools/prepare_standalone.py',ROOT/'tools/upstream.lock.json']
    hashes={str(p.relative_to(ROOT)):digest(p) for p in paths}
    cases=[('positive',None,None,'PASS 366 SDRAM four-state checks'),
        ('unknown-mask',' && known_mask','', 'unknown SDRAM pin control'),
        ('unknown-reset',"wire warm_reset=bus_reset!==1'b0;","wire warm_reset=bus_reset===1'b1;",'unknown warm reset accepted a request'),
        ('hidden-unknown-read','<=sdram_dq_in;',"<=((^sdram_dq_in===1'bx) ? 16'b0 : sdram_dq_in);",'read did not preserve four-state data')]
    results={}
    for name,before,after,marker in cases:
        candidate=source
        if before is not None:
            text=source.read_text();expected=2 if name=='hidden-unknown-read' else 1
            if text.count(before)!=expected:raise ValueError('mutation site changed: '+name)
            candidate=directory/(name+'.sv');candidate.write_text(text.replace(before,after))
        binary=directory/(name+'.vvp');compile_log=directory/(name+'-compile.log')
        with compile_log.open('w') as log:
            subprocess.run([str(ROOT/'.cache/tools/usr/bin/iverilog'),
                '-B'+str(ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl'),'-g2012','-s','sdram_four_state',
                '-o',str(binary),str(candidate),str(bench)],stdout=log,stderr=subprocess.STDOUT,check=True,timeout=60)
        run=subprocess.run([str(ROOT/'.cache/tools/usr/bin/vvp'),str(binary)],capture_output=True,text=True,timeout=120)
        log=directory/(name+'.log');log.write_text(run.stdout+run.stderr)
        if bool(run.returncode)!=(before is not None) or marker not in log.read_text():
            raise ValueError('unexpected four-state outcome: '+name+'\n'+log.read_text())
        results[name]={'outcome':'passed' if before is None else 'rejected','log_sha256':digest(log),
            'binary_sha256':digest(binary)}
    for name,value in hashes.items():
        if digest(ROOT/name)!=value:raise ValueError('four-state inputs changed: '+name)
    output={'status':'passed','scope':'four-state request controls and data; not analog or board timing validation',
        'cases':366,'checks':results,'inputs':hashes,'physical_hardware_tested':False}
    report.parent.mkdir(exist_ok=True);report.write_text(json.dumps(output,indent=2)+'\n')
    print('PASS 366 SDRAM four-state checks and three negative controls')


if __name__=='__main__':main()
