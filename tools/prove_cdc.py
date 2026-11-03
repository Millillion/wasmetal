#!/usr/bin/env python3
"""Prove CDC register initialization and payload stability with arbitrary clocks."""
import json
from pathlib import Path
import subprocess
from prepare_standalone import ROOT,digest

HARNESS='''
    reg formal_started=0;
    always @($global_clock) begin
        if(!formal_started) assume(reset);
        formal_started<=1;
    end
    // These reachable-state lemmas are proved alongside the clocked assertions,
    // not assumed. They allow induction without a bound on either clock period.
    always @* begin
        assert(!source_held || source_state==SOURCE_WAIT || source_state==SOURCE_RESPONSE);
        assert(!source_held || request_payload==prior_source);
        assert(!destination_held || (m_valid && destination_request==prior_destination));
        assert((^{source_release,destination_release,source_state,destination_state,
            request_toggle,response_toggle,destination_up,request_payload,destination_request,
            response_payload,request_sync,response_sync,destination_up_sync,s_fault,s_rdata,
            source_held,destination_held,prior_source,prior_destination})!==1'bx);
    end
'''


def main():
    directory=ROOT/'build/formal-cdc';directory.mkdir(parents=True,exist_ok=True)
    original=ROOT/'soc/external/wasmetal_memory_cdc.sv'
    source=directory/'cdc.sv';text=original.read_text();assert text.count('endmodule')==1
    source.write_text(text.replace('endmodule',HARNESS+'\nendmodule'))
    inputs=[original,Path(__file__).resolve(),source]
    hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs}
    def execute(path,name,induction):
        script=directory/f'{name}.ys';logfile=directory/f'{name}.log'
        proof='-seq 1 -tempinduct -maxsteps 16' if induction else '-seq 18'
        script.write_text(f'''read_verilog -formal -sv -DWASMETAL_ASSERTIONS {path}
prep -top wasmetal_memory_cdc -flatten
clk2fflogic
opt_clean
sat {proof} -set-assumes -set-def-inputs -set-init-undef -enable_undef -prove-asserts -verify
''')
        with logfile.open('w') as log:
            result=subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-Q','-T','-s',str(script)],
                cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=180)
        return result,logfile.read_text()
    result,log=execute(source,'safety',True);result.check_returncode()
    if 'Induction step proven: SUCCESS!' not in log:raise ValueError('missing unbounded proof')
    rejected=[]
    for name in ('missing-payload-reset','payload-changes-while-pending'):
        text=source.read_text()
        if name=='missing-payload-reset':
            old='request_toggle<=0;request_payload<=0;';assert text.count(old)==1
            text=text.replace(old,'request_toggle<=0;')
        else:
            old='SOURCE_WAIT: if(response_sync[1]==request_toggle) begin';assert text.count(old)==1
            text=text.replace(old,'SOURCE_WAIT: begin request_payload<={s_write,s_address,s_mask,s_wdata};\n if(response_sync[1]==request_toggle) begin')
            text=text.replace('            SOURCE_RESPONSE:','            end\n            SOURCE_RESPONSE:',1)
        negative=directory/f'{name}.sv';negative.write_text(text)
        result,log=execute(negative,name,False)
        if result.returncode==0 or 'proof did fail' not in log:raise ValueError('bad negative control: '+name)
        rejected.append(name)
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise RuntimeError('proof inputs changed')
    report={'status':'passed','scope':'unbounded register initialization and stall safety; not complete transfer equivalence, liveness or analog CDC signoff',
        'properties':['source payload stable while waiting for response','destination valid and payload held through stalls',
            'all RTL registers remain defined after reset'],
        'environment':'initial common reset; arbitrary binary inputs, independent clocks and later common resets; clocks may stop',
        'clock_model':'Yosys clk2fflogic converts both clocks to edge detection on the formal global time step',
        'reachable_state_lemmas':'proven jointly with the original RTL assertions; no payload or clock fairness assumptions',
        'negative_controls_rejected':rejected,'inputs':hashes,'physical_hardware_tested':False}
    (ROOT/'reports/cdc-proof.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS CDC unbounded initialization/stall safety with arbitrary clocks and reset; both mutations rejected')


if __name__=='__main__':main()
