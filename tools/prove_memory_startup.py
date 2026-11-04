#!/usr/bin/env python3
"""Prove startup ownership, request stability and isolation for arbitrary responses."""
import json
from pathlib import Path
import subprocess
import time
from prepare_standalone import ROOT,digest
from prove_memory_bist import HARNESS as BIST_INVARIANTS

HARNESS=r'''
    reg formal_started=0;
    reg previous_enabled,previous_valid,waiting_memory,waiting_cpu;
    reg [176:0] previous_memory_payload,previous_cpu_payload;
    reg [63:0] previous_count;
    always @(posedge clk) begin
        if(!formal_started) assume(reset);
        formal_started<=1;
        if(reset) begin
            assert(!cpu_enabled && !memory_valid && !memory_write && !cpu_ready && !cpu_fault);
            previous_enabled<=0;previous_valid<=0;waiting_memory<=0;waiting_cpu<=0;
            previous_memory_payload<=0;previous_cpu_payload<=0;previous_count<=0;
        end else begin
            if(formal_started) begin
                if(waiting_cpu) begin
                    assume(cpu_valid);
                    assume({cpu_write,cpu_address,cpu_mask,cpu_wdata}==previous_cpu_payload);
                end
                assert((^{launched,test_busy,test_done,test_failed,completed_operations})!==1'bx);
                if(test_done || test_busy) assert(launched);
                if(previous_enabled) begin
                    assert(cpu_enabled);
                    assert(completed_operations==previous_count);
                end
                if(cpu_enabled) begin
                    assert(test_done && !test_busy && !test_failed);
                    assert(completed_operations==64'(RAM_BYTES/16)*64'd80);
                    assert(memory_valid==cpu_valid);
                    assert(memory_write==(cpu_valid && cpu_write));
                    assert({memory_address,memory_mask,memory_wdata}=={cpu_address,cpu_mask,cpu_wdata});
                    assert(cpu_ready==(cpu_valid && memory_ready));
                    assert(cpu_fault==(cpu_valid && memory_ready && memory_fault));
                    assert(cpu_rdata==memory_rdata);
                    if(!previous_enabled) assert(!previous_valid);
                end else begin
                    assert(!cpu_ready && !cpu_fault && cpu_rdata==0);
                    assert(memory_valid==test_valid);
                    assert(memory_write==(test_valid && test_write));
                    assert({memory_address,memory_mask,memory_wdata}=={test_address,test_mask,test_wdata});
                end
                if(test_failed) assert(!cpu_enabled);
                if(waiting_memory) begin
                    assert(memory_valid);
                    assert({memory_write,memory_address,memory_mask,memory_wdata}==previous_memory_payload);
                end
            end
            previous_enabled<=cpu_enabled;previous_valid<=memory_valid;
            waiting_memory<=memory_valid && !memory_ready;
            waiting_cpu<=cpu_valid && !cpu_ready;
            previous_memory_payload<={memory_write,memory_address,memory_mask,memory_wdata};
            previous_cpu_payload<={cpu_write,cpu_address,cpu_mask,cpu_wdata};
            previous_count<=completed_operations;
        end
    end
'''


def main():
    started=time.monotonic();directory=ROOT/'build/formal-memory-startup';directory.mkdir(parents=True,exist_ok=True)
    output=ROOT/'reports/memory-startup-proof.json';output.unlink(missing_ok=True)
    original=ROOT/'soc/asic/wasmetal_memory_startup.sv';bist_original=ROOT/'soc/asic/wasmetal_memory_bist.sv'
    source=directory/'wasmetal_memory_startup.sv';bist=directory/'wasmetal_memory_bist.sv'
    for path,extra,target in [(original,HARNESS,source),(bist_original,BIST_INVARIANTS,bist)]:
        text=path.read_text()
        if text.count('endmodule')!=1:raise ValueError('ambiguous proof insertion')
        target.write_text(text.replace('endmodule',extra+'\nendmodule'))
    paths=[original,bist_original,source,bist,Path(__file__).resolve(),ROOT/'tools/prove_memory_bist.py',
        ROOT/'tools/check_memory_bist.py',ROOT/'tools/prepare_standalone.py',ROOT/'tools/upstream.lock.json',ROOT/'.cache/tools/usr/bin/yosys']
    inputs={str(p.relative_to(ROOT)):digest(p) for p in paths}
    def execute(path,label,size,timeout,induction):
        script=directory/(label+'.ys');logfile=directory/(label+'.log')
        bound='-seq 1 -tempinduct -maxsteps 24' if induction else '-seq 12'
        script.write_text(f'read_verilog -formal -sv -DWASMETAL_ASSERTIONS {bist} {path}\n'+
            f'chparam -set RAM_BYTES {size} -set RESPONSE_TIMEOUT {timeout} wasmetal_memory_startup\n'+
            'prep -top wasmetal_memory_startup -flatten\nmemory_map\nopt_clean\n'+
            f'sat {bound} -set-assumes -set-def-inputs -set-init-undef -enable_undef -prove-asserts -verify\n')
        with logfile.open('w') as log:
            run=subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-Q','-T','-s',str(script)],cwd=ROOT,
                               stdout=log,stderr=subprocess.STDOUT,timeout=240)
        return run,script,logfile
    checks=[]
    for size,timeout in [(16,9),(80,11),(131072,1024),(16,1)]:
        run,script,log=execute(source,f'{size}-{timeout}',size,timeout,True);run.check_returncode()
        if 'Induction step proven: SUCCESS!' not in log.read_text():raise ValueError('missing startup induction proof')
        checks.append({'ram_bytes':size,'response_timeout':timeout,'status':'proven','script_sha256':digest(script),'log_sha256':digest(log)})
        print('PASS unbounded startup safety',size,timeout,flush=True)
    controls=[]
    for name,old,new in [
        ('early-handoff','cpu_enabled=test_done && !test_failed && !reset;','cpu_enabled=launched && !test_failed && !reset;'),
        ('failure-grants-cpu','cpu_enabled=test_done && !test_failed && !reset;','cpu_enabled=test_done && !reset;'),
        ('test-response-leak','cpu_ready=cpu_enabled && cpu_valid && memory_ready;','cpu_ready=cpu_valid && memory_ready;'),
        ('timeout-withdraws-request','memory_valid=!reset && (cpu_enabled ? cpu_valid : test_valid);',
         'memory_valid=!reset && (cpu_enabled ? cpu_valid : test_valid && !test_failed);')]:
        text=source.read_text()
        if text.count(old)!=1:raise ValueError('ambiguous startup proof fault: '+name)
        mutant=directory/(name+'.sv');mutant.write_text(text.replace(old,new))
        run,script,log=execute(mutant,name,32,2,False)
        if run.returncode==0 or 'proof did fail' not in log.read_text():raise ValueError('startup proof fault not rejected: '+name)
        controls.append({'name':name,'source_sha256':digest(mutant),'script_sha256':digest(script),'log_sha256':digest(log)})
        print('REJECTED',name,flush=True)
    for name,sha in inputs.items():
        if digest(ROOT/name)!=sha:raise ValueError('startup proof input changed: '+name)
    report={'status':'passed','scope':'unbounded startup ownership, full-test accounting, stable requests and CPU isolation',
        'environment':'initial shared reset; arbitrary binary memory responses and resets; CPU keeps each valid request stable until acknowledgement or reset',
        'inputs':inputs,'checks':checks,'negative_controls':controls,'negative_controls_rejected':len(controls),
        'limitations':['No fairness assumption or eventual completion proof for an unresponsive memory.',
            'The SRAM storage and physical timing are not modeled by these protocol proofs.',
            'The CPU transaction source is abstract; the complete CPU is not part of this proof.'],
        'physical_hardware_tested':False,'elapsed_seconds':time.monotonic()-started}
    output.parent.mkdir(exist_ok=True);output.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
