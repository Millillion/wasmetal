#!/usr/bin/env python3
"""Prove memory-test progress accounting and protocol safety for arbitrary responses."""
import json
from pathlib import Path
import subprocess
import time

from check_memory_bist import CONFIGURATIONS
from prepare_standalone import ROOT, digest

HARNESS=r'''
    reg formal_started=0;
    reg keep_error;
    reg [290:0] saved_error;
    wire [127:0] mathematical_background;
    for(genvar formal_bit=0;formal_bit<128;formal_bit=formal_bit+1) begin: formal_background
        assign mathematical_background[formal_bit]=background_index==7 ? 1'b0 :
            1'((formal_bit>>background_index)&1);
    end
    reg [63:0] position_in_pass;
    always_comb case(phase)
        0:position_in_pass=64'(word_index);
        1:position_in_pass=64'(WORDS)+2*64'(word_index)+64'(write_half);
        2:position_in_pass=3*64'(WORDS)+2*64'(word_index)+64'(write_half);
        3:position_in_pass=5*64'(WORDS)+2*(64'(WORDS-1)-64'(word_index))+64'(write_half);
        4:position_in_pass=7*64'(WORDS)+2*(64'(WORDS-1)-64'(word_index))+64'(write_half);
        default:position_in_pass=9*64'(WORDS)+64'(word_index);
    endcase
    always @(posedge clk) begin
        if(!formal_started) assume(reset);
        formal_started<=1;
        if(reset) begin keep_error<=0;saved_error<=0;end
        else begin
            if(formal_started) begin
                assert((^{state,word_index,waiting,phase,background_index,write_half,
                    stop_after_release,done,failed,error_code,error_address,expected_data,
                    observed_data,completed_operations,was_waiting,pending_payload})!==1'bx);
                assert(background==mathematical_background);
                assert(completed_operations==64'(background_index)*10*64'(WORDS)+
                    position_in_pass+64'(stop_after_release));
                assert(32'(waiting)<RESPONSE_TIMEOUT);
                assert(!write_half || (phase>=1 && phase<=4));
                assert(state!=REQUEST || !stop_after_release);
                assert(!stop_after_release || state==RELEASE || state==FINISH || state==IDLE);
                assert(failed==(error_code!=0));
                if(done && !failed) assert(completed_operations==80*64'(WORDS));
                if(keep_error) assert({failed,error_code,error_address,expected_data,observed_data}==saved_error);
            end
            keep_error<=failed && !(state==IDLE && start);
            saved_error<={failed,error_code,error_address,expected_data,observed_data};
        end
    end
'''


def main():
    started=time.monotonic();directory=ROOT/'build/formal-memory-bist';directory.mkdir(parents=True,exist_ok=True)
    output=ROOT/'reports/memory-bist-proof.json';output.unlink(missing_ok=True)
    original=ROOT/'soc/asic/wasmetal_memory_bist.sv';text=original.read_text()
    if text.count('endmodule')!=1:raise ValueError('ambiguous formal insertion')
    source=directory/'memory_bist.sv';source.write_text(text.replace('endmodule',HARNESS+'\nendmodule'))
    paths=[original,source,Path(__file__).resolve(),ROOT/'tools/check_memory_bist.py',
           ROOT/'tools/upstream.lock.json',ROOT/'.cache/tools/usr/bin/yosys']
    inputs={str(p.relative_to(ROOT)):digest(p) for p in paths};checks=[]
    def execute(path,label,size,timeout,induction):
        script=directory/(label+'.ys');logfile=directory/(label+'.log')
        bounds='-seq 1 -tempinduct -maxsteps 24' if induction else '-seq 12'
        script.write_text(f'read_verilog -formal -sv -DWASMETAL_ASSERTIONS {path}\n'+
            f'chparam -set RAM_BYTES {size} -set RESPONSE_TIMEOUT {timeout} wasmetal_memory_bist\n'+
            'prep -top wasmetal_memory_bist -flatten\nmemory_map\nopt_clean\n'+
            f'sat {bounds} -set-assumes -set-def-inputs -set-init-undef -enable_undef -prove-asserts -verify\n')
        with logfile.open('w') as log:
            run=subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-Q','-T','-s',str(script)],
                               cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=180)
        return run,logfile
    for size,timeout in [*CONFIGURATIONS,(16,1)]:
        run,log=execute(source,f'{size}-{timeout}',size,timeout,True);run.check_returncode()
        if 'Induction step proven: SUCCESS!' not in log.read_text():raise ValueError('missing unbounded induction proof')
        checks.append({'ram_bytes':size,'response_timeout':timeout,'status':'proven','log_sha256':digest(log)})
        print('PASS unbounded BIST safety',size,timeout,flush=True)
    controls=[]
    for name,old,new in [
        ('wrong-background',"0:background=128'haaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa;","0:background=128'h0;"),
        ('extra-count','completed_operations<=completed_operations+1\'b1;',"completed_operations<=completed_operations+2'd2;"),
        ('timeout-withdraws-request','assign valid=state==REQUEST && !reset;','assign valid=state==REQUEST && !reset && !failed;'),
        ('wrong-descent','wire descending=phase==3 || phase==4;',"wire descending=1'b0;")]:
        if source.read_text().count(old)!=1:raise ValueError('ambiguous proof fault: '+name)
        mutant=directory/(name+'.sv');mutant.write_text(source.read_text().replace(old,new))
        run,log=execute(mutant,name,32,2,False)
        if run.returncode==0 or 'proof did fail' not in log.read_text():raise ValueError('proof did not reject '+name)
        controls.append({'name':name,'source_sha256':digest(mutant),'log_sha256':digest(log)})
        print('REJECTED',name,flush=True)
    for name,value in inputs.items():
        if digest(ROOT/name)!=value:raise ValueError('BIST proof input changed: '+name)
    report={'status':'passed','scope':'unbounded protocol, complete sequence accounting and first-error retention; no stored-data or physical proof',
        'environment':'initial reset, then arbitrary binary starts, responses, data and resets; no response fairness assumption',
        'checks':checks,'negative_controls':controls,'negative_controls_rejected':len(controls),'inputs':inputs,
        'physical_hardware_tested':False,'elapsed_seconds':time.monotonic()-started}
    output.parent.mkdir(exist_ok=True);output.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
