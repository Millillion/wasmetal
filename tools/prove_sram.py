#!/usr/bin/env python3
"""Prove SRAM command bounds, payload, fixed latency and reset/release behavior."""
import json
from pathlib import Path
import subprocess
from check_sram import CONFIGURATIONS
from prepare_standalone import ROOT,digest


HARNESS='''
    reg formal_started=0;
    always @(posedge clk) begin
        if(!formal_started) assume(reset);
        formal_started<=1;
        if(formal_started && !reset)
            assert((^{state,write_q,address_q,mask_q,data_q,remaining,fault,rdata,
                tracked,waiting_release,expected_legal,expected_write,expected_address,
                age,expected_mask,expected_data,prior_read_data})!==1'bx);
    end
'''


def main():
    directory=ROOT/'build/formal-sram';directory.mkdir(parents=True,exist_ok=True)
    original=ROOT/'soc/asic/wasmetal_sram_memory.sv';source=directory/'sram.sv'
    text=original.read_text();assert text.count('endmodule')==1;source.write_text(text.replace('endmodule',HARNESS+'\nendmodule'))
    paths=[original,source,Path(__file__).resolve(),ROOT/'tools/check_sram.py',ROOT/'tools/upstream.lock.json']
    inputs={str(path.relative_to(ROOT)):digest(path) for path in paths};results=[]
    def execute(path,name,size,latency,induction):
        script=directory/f'{name}.ys';logfile=directory/f'{name}.log'
        proof='-seq 1 -tempinduct -maxsteps 24' if induction else '-seq 9'
        script.write_text(f'''read_verilog -formal -sv -DWASMETAL_ASSERTIONS {path}
chparam -set RAM_BYTES {size} -set READ_LATENCY {latency} wasmetal_sram_memory
prep -top wasmetal_sram_memory -flatten
sat {proof} -set-assumes -set-def-inputs -set-init-undef -enable_undef -prove-asserts -verify
''')
        with logfile.open('w') as log:
            result=subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-Q','-T','-s',str(script)],
                cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=180)
        return result,logfile.read_text()
    for size,latency in CONFIGURATIONS:
        result,log=execute(source,f'memory-{size}-latency-{latency}',size,latency,True);result.check_returncode()
        if 'Induction step proven: SUCCESS!' not in log:raise ValueError('missing unbounded SRAM safety proof')
        results.append({'ram_bytes':size,'read_latency':latency,'status':'proven'})
        print(f'PASS SRAM safety induction {size} bytes, latency {latency}',flush=True)
    rejected=[]
    for name,old,new in [
        ('wrong-byte-enable','assign sram_byte_enable=mask_q;','assign sram_byte_enable=mask_q ^ 16\'h1;'),
        ('early-read-capture',"remaining<=COUNT_WIDTH'(READ_LATENCY);","remaining<=COUNT_WIDTH'(READ_LATENCY-1);"),
        ('duplicate-held-command','RELEASE: if(!valid) state<=IDLE;','RELEASE: state<=IDLE;'),
        ('missing-data-reset','mask_q<=0;data_q<=0;','mask_q<=0;')]:
        assert source.read_text().count(old)==1
        negative=directory/f'{name}.sv';negative.write_text(source.read_text().replace(old,new))
        result,log=execute(negative,name,80,2,False)
        if result.returncode==0 or 'proof did fail' not in log:raise ValueError('bad SRAM negative control: '+name)
        rejected.append(name)
    if any(digest(ROOT/name)!=value for name,value in inputs.items()):raise ValueError('SRAM proof inputs changed')
    report={'status':'passed','scope':'unbounded adapter protocol and response safety, not SRAM stored-data equivalence or physical timing',
        'environment':'initial reset, then arbitrary binary requests, read data and resets; fixed latency is an adapter contract',
        'configurations':results,'properties':['one in-bounds macro command per legal request','exact address/data/byte enables',
            'no command on invalid request','exact fixed-latency completion','read captures previous edge input',
            'no repetition while valid stays asserted','reset establishes defined controller state'],
        'negative_controls_rejected':rejected,'inputs':inputs,'physical_hardware_tested':False}
    (ROOT/'reports/sram-proof.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
