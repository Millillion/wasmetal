#!/usr/bin/env python3
"""Prove AXI request stability, handshake dependencies and error isolation."""
import json
from pathlib import Path
import subprocess
from prepare_standalone import ROOT,digest

HARNESS='''
    reg formal_started=0;
    always @(posedge clk) begin
        if(!formal_started) assume(reset);
        formal_started<=1;
        if(formal_started && !reset)
            assert((^{state,address_q,mask_q,data_q,aw_sent,w_sent,ar_sent,
                poisoned,fault,rdata,held_aw,held_w,held_ar,prior_address,prior_write})!==1'bx);
    end
'''


def main():
    directory=ROOT/'build/formal-axi';directory.mkdir(parents=True,exist_ok=True)
    original=ROOT/'soc/external/wasmetal_axi_memory.sv'
    source=directory/'axi.sv';text=original.read_text();assert text.count('endmodule')==1
    source.write_text(text.replace('endmodule',HARNESS+'\nendmodule'))
    inputs=[original,Path(__file__).resolve(),source]
    hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs};results=[]
    def execute(path,name,base,induction):
        script=directory/f'{name}.ys';logfile=directory/f'{name}.log'
        proof='-seq 1 -tempinduct -maxsteps 12' if induction else '-seq 7'
        script.write_text(f'''read_verilog -formal -sv -DWASMETAL_ASSERTIONS {path}
chparam -set BASE_ADDRESS {base} wasmetal_axi_memory
prep -top wasmetal_axi_memory -flatten
sat {proof} -set-assumes -set-def-inputs -set-init-undef -enable_undef -prove-asserts -verify
''')
        with logfile.open('w') as log:
            result=subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-Q','-T','-s',str(script)],
                cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=180)
        return result,logfile.read_text()
    for base in (0,4096,0xfffff000):
        result,log=execute(source,f'base-{base}',base,True)
        result.check_returncode()
        if 'Induction step proven: SUCCESS!' not in log: raise ValueError('missing unbounded proof')
        results.append({'base_address':base,'id_width':4,'status':'proven'})
        print('PASS AXI safety induction BASE_ADDRESS='+hex(base),flush=True)
    rejected=[]
    for name,old,new in [
        ('valid-depends-on-ready','assign awvalid=state==WRITE && !aw_sent && !reset;',
         'assign awvalid=state==WRITE && !aw_sent && !reset && awready;'),
        ('early-write-response','assign bready=state==WRITE && aw_sent && w_sent && !reset;',
         'assign bready=state==WRITE && aw_sent && !reset;'),
        ('missing-data-reset','address_q<=0;mask_q<=0;data_q<=0;', 'address_q<=0;mask_q<=0;'),
    ]:
        assert source.read_text().count(old)==1
        negative=directory/f'{name}.sv';negative.write_text(source.read_text().replace(old,new))
        result,log=execute(negative,name,0,False)
        if result.returncode==0 or 'proof did fail' not in log:raise ValueError('bad negative control: '+name)
        rejected.append(name)
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise RuntimeError('proof inputs changed')
    report={'status':'passed','scope':'unbounded protocol safety induction, not liveness or complete data equivalence',
        'configurations':results,'properties':['address/data stability through stalls','VALID independent of READY',
            'write response only after address and data','read response only after address',
            'aligned requests and nonzero write strobes','no new transactions after a response error'],
        'environment':'initial reset, then arbitrary binary local requests, channel handshakes, responses and resets',
        'negative_controls_rejected':rejected,'inputs':hashes,'physical_hardware_tested':False}
    (ROOT/'reports/axi-proof.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
