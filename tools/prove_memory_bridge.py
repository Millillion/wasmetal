#!/usr/bin/env python3
"""Inductively prove the bridge's address, hold and poisoned-state invariants."""
import json
from pathlib import Path
import subprocess
from prepare_standalone import ROOT,digest

HARNESS='''
    reg formal_started=0;
    always @(posedge clk) begin
        if(!formal_started) assume(reset);
        formal_started<=1;
        // Reachability lemma, proved rather than assumed: a reset followed by
        // binary inputs leaves no uninitialized protocol state. This prevents
        // induction from starting inside an impossible X-filled stalled beat.
        if(formal_started && !reset)
            assert((^{state,location,clear_address,wait_cycles,
                initialization_failed,poisoned,position,length,offset,saved_kind,
                saved_write,saved_initialize,valid_region,payload,fault,rdata,
                prior_valid,prior_ready,prior_timeout,prior_request})!==1'bx);
    end
'''

def main():
    directory=ROOT/'build/formal-memory-bridge';directory.mkdir(parents=True,exist_ok=True)
    original=ROOT/'soc/memory/wasmetal_memory_bridge.sv';lanes=ROOT/'soc/memory/wasmetal_memory_lanes.sv'
    source=directory/'bridge.sv';text=original.read_text();assert text.count('endmodule')==1
    source.write_text(text.replace('endmodule',HARNESS+'\nendmodule'))
    inputs=[original,lanes,Path(__file__).resolve(),source];hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs}
    results=[]
    for size,regions,timeout in [(256,2,4),(131072,16,1024)]:
        script=directory/f'ram-{size}.ys';logfile=directory/f'ram-{size}.log'
        script.write_text(f'''read_verilog -formal -sv -DWASMETAL_ASSERTIONS {lanes} {source}
chparam -set RAM_BYTES {size} -set REGIONS_PER_KIND {regions} -set TIMEOUT_CYCLES {timeout} wasmetal_memory_bridge
prep -top wasmetal_memory_bridge -flatten
opt_clean
sat -seq 1 -tempinduct -maxsteps 12 -set-assumes -set-def-inputs -set-init-undef -enable_undef -prove-asserts -verify
''')
        with logfile.open('w') as log:
            subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-Q','-T','-s',str(script)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=180)
        if 'Induction step proven: SUCCESS!' not in logfile.read_text():raise RuntimeError('no unbounded induction result')
        results.append({'ram_bytes':size,'regions_per_kind':regions,'timeout_cycles':timeout,'status':'proven'})
        print('PASS bridge safety induction RAM_BYTES='+str(size),flush=True)
    rejected=[]
    for name,old,new in [
        ('misaligned-address','clearing ? clear_address :',"clearing ? (clear_address ^ 32'd1) :"),
        ('uninitialized-payload','valid_region<=0; payload<=0; fault<=0;', 'valid_region<=0; fault<=0;'),
    ]:
        negative=directory/f'{name}.sv';assert source.read_text().count(old)==1
        negative.write_text(source.read_text().replace(old,new))
        script=directory/f'{name}.ys';script.write_text(f'''read_verilog -formal -sv -DWASMETAL_ASSERTIONS {lanes} {negative}
chparam -set RAM_BYTES 256 -set REGIONS_PER_KIND 2 -set TIMEOUT_CYCLES 4 wasmetal_memory_bridge
prep -top wasmetal_memory_bridge -flatten
sat -seq 4 -set-assumes -set-def-inputs -set-init-undef -enable_undef -prove-asserts -verify
''')
        logfile=directory/f'{name}.log'
        with logfile.open('w') as log:
            result=subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-Q','-T','-s',str(script)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=180)
        if result.returncode==0 or 'proof did fail' not in logfile.read_text():raise RuntimeError('bad negative control: '+name)
        rejected.append(name)
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise RuntimeError('proof inputs changed')
    report={'status':'passed','scope':'unbounded safety induction, not complete memory data equivalence or liveness',
        'configurations':results,'properties':['aligned in-range physical requests','stable request through stalls',
            'nonzero byte mask','no physical requests when poisoned','valid beat geometry'],
        'environment':'one initial reset; arbitrary binary later resets, requests, regions, data and backend responses',
        'negative_controls_rejected':rejected,'inputs':hashes,'physical_hardware_tested':False}
    (ROOT/'reports').mkdir(exist_ok=True)
    (ROOT/'reports/memory-bridge-proof.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
