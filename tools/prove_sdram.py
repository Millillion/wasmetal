#!/usr/bin/env python3
"""Prove SDRAM request isolation, pin payload, refresh deadlines and read capture."""
import argparse
import json
from pathlib import Path
import re
import subprocess
from check_sdram import PROFILES
from prepare_standalone import ROOT,digest


HARNESS=r'''
    reg formal_started=0;
    reg observed_refresh=0, waiting_hold=0, collecting_read=0;
    reg [REFRESH_WIDTH-1:0] pin_refresh_age=0;
    reg [4:0] read_age=0;
    reg [127:0] expected_read=0, expected_data=0;
    reg [31:0] expected_address=0;
    reg [15:0] expected_mask=0;
    reg expected_legal=0, expected_write=0;
    wire pin_refresh={sdram_cs_n,sdram_ras_n,sdram_cas_n,sdram_we_n}==4'b0001;
    wire pin_activate={sdram_cs_n,sdram_ras_n,sdram_cas_n,sdram_we_n}==4'b0011;
    wire pin_read={sdram_cs_n,sdram_ras_n,sdram_cas_n,sdram_we_n}==4'b0101;
    wire pin_write={sdram_cs_n,sdram_ras_n,sdram_cas_n,sdram_we_n}==4'b0100;
    wire [31:0] decoded_address=32'({row_q[ROW_BITS-1:0],bank_q,column_q,1'b0});
    always @(posedge clk) begin
        if(!formal_started) assume(reset);
        else assume(!reset); // subsequent application resets use bus_reset
        formal_started<=1;
        if(reset) begin
            observed_refresh<=0;pin_refresh_age<=0;waiting_hold<=0;
            collecting_read<=0;read_age<=0;expected_read<=0;
            expected_data<=0;expected_address<=0;expected_mask<=0;
            expected_legal<=0;expected_write<=0;
        end else begin
            assert((^{state,remaining,refresh_age,row_age,operation_age,row_q,column_q,
                bank_q,beat,mask_q,data_q,write_q,booted,second_refresh,outstanding,
                aborted,wait_release,fault,rdata})!==1'bx);
            // Strengthening invariants tie each timer to its legal phase.
            assert(booted==(state>=IDLE && state<=WAIT_RFC));
            assert(outstanding==(state>=ACTIVATE && state<=RESPONSE));
            assert(refresh_age<=REFRESH_WIDTH'(REFRESH_CYCLES));
            assert(row_age<=ROW_AGE_WIDTH'(T_RAS+T_RC+1));
            if(wait_release)assert(!outstanding);
            if(state==POWER_WAIT)assert(remaining<POWERUP_CYCLES);
            if(state==INIT_RP || state==WAIT_RP)assert(remaining<T_RP);
            if(state==INIT_RFC || state==WAIT_RFC)assert(remaining<T_RFC);
            if(state==INIT_MRD)assert(remaining<T_MRD);
            if(state==WAIT_RCD)assert(remaining<T_RCD);
            if(state==READ_WAIT)assert(remaining<=CAS_LATENCY);
            if(state==RECOVER)assert(remaining<T_WR);
            if(state==WRITE_BURST || state==READ_BURST)assert(beat>=1 && beat<=7);
            assert(known_request==legal);
            if(pin_refresh)begin observed_refresh<=1;pin_refresh_age<=0;end
            else if(observed_refresh && pin_refresh_age<REFRESH_WIDTH'(REFRESH_CYCLES))
                pin_refresh_age<=pin_refresh_age+1'b1;
            if(observed_refresh)assert(pin_refresh_age==refresh_age);
            if(booted)begin assert(observed_refresh);assert(pin_refresh_age<REFRESH_CYCLES);end
            // Capture bus values while idle, independently of the permission
            // calculation. Any subsequent pin command must use that request.
            if(state==IDLE)begin
                expected_address<=address;expected_mask<=mask;expected_data<=wdata;
                expected_write<=write;
                expected_legal<=address%16==0 && mask!=0 && {1'b0,address}+33'd16<=33'(RAM_BYTES);
            end
            if(pin_activate || pin_read || pin_write)begin
                assert(expected_legal && outstanding && booted);
                assert(decoded_address==expected_address && decoded_address%16==0);
            end
            if(pin_write)assert(expected_write);
            if(pin_read)assert(!expected_write);
            if(sdram_dq_oe)begin
                assert(expected_legal && expected_write);
                if(pin_write)begin
                    assert(sdram_dq_out==expected_data[15:0]);
                    assert(sdram_dqm==~expected_mask[1:0]);
                end else begin
                    assert(sdram_dq_out==16'(expected_data>>(16*beat)));
                    assert(sdram_dqm==2'((~expected_mask)>>(2*beat)));
                end
            end
            if(pin_read)begin collecting_read<=1;read_age<=0;expected_read<=0;end
            else if(collecting_read)begin
                if(read_age>=CAS_LATENCY)expected_read<={sdram_dq_in,expected_read[127:16]};
                if(read_age==CAS_LATENCY+7)collecting_read<=0;
                else read_age<=read_age+1'b1;
            end
            if(waiting_hold)assert(!pin_activate && !pin_read && !pin_write && !ready);
            if(bus_reset || !valid)waiting_hold<=0;
            else if(ready)waiting_hold<=1;
            if(ready)begin
                assert(fault==!expected_legal);
                if(expected_legal && !expected_write)assert(rdata==expected_read);
                else assert(rdata==0);
            end
        end
    end
'''


NEGATIVES={
    'request-disabled':('wire known_request=',"wire known_request=1'b0 && "),
    'refresh-suppressed':('INIT_REFRESH,REFRESH: begin sdram_ras_n=0; sdram_cas_n=0; end',
        'INIT_REFRESH,REFRESH: begin end'),
    'write-mask-inverted':("sdram_dqm=write_q ? ~mask_q[1:0] : 2'b00;",
        "sdram_dqm=write_q ? mask_q[1:0] : 2'b00;"),
    'read-early':("remaining<=WAIT_WIDTH'(CAS_LATENCY);state<=READ_WAIT;",
        "remaining<=WAIT_WIDTH'(CAS_LATENCY-1);state<=READ_WAIT;"),
    'uninitialized-data':('mask_q<=0; data_q<=0;','mask_q<=0;'),
    'repeated-held-request':('wait_release<=valid && !warm_reset && !aborted;',
        'wait_release<=0;'),
    'bank-misdirected':('bank_q<=address[COLUMN_BITS+1+:2];',
        "bank_q<=address[COLUMN_BITS+1+:2]^2'b01;"),
}


def prove(source,directory,name,profile,timeout,negative=False):
    parameters=' '.join(f'-set {key} {value}' for key,value in profile.items())
    script=directory/(name+'.ys');logfile=directory/(name+'.log')
    mode='-seq 40' if negative else '-seq 1 -tempinduct -maxsteps 96'
    script.write_text(f'''read_verilog -formal -sv -DWASMETAL_ASSERTIONS {source}
chparam {parameters} wasmetal_sdram_memory
prep -top wasmetal_sdram_memory -flatten
opt -full
wreduce
opt -full
sat {mode} -set-assumes -set-def-inputs -set-init-undef -enable_undef -prove-asserts -verify
''')
    with logfile.open('w') as log:
        result=subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-Q','-T','-s',str(script)],
            cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=timeout)
    output=logfile.read_text()
    if negative:
        if result.returncode==0 or 'Called with -verify and proof did fail' not in output:
            raise RuntimeError('SDRAM proof did not reject negative control: '+name)
    elif result.returncode or 'Induction step proven: SUCCESS!' not in output:
        raise RuntimeError('SDRAM induction did not pass: '+name)
    depths=re.findall(r'\[induction step (\d+)\]',output)
    return {'profile':name,'parameters':profile,'log_sha256':digest(logfile),
        'script_sha256':digest(script),'source_sha256':digest(source),
        'induction_depth':int(depths[-1]) if depths else None,
        'status':'counterexample-found' if negative else 'proven'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile',action='append',choices=PROFILES)
    parser.add_argument('--report',type=Path,default=ROOT/'reports/sdram-proof.json')
    parser.add_argument('--timeout-seconds',type=int,default=1200)
    args=parser.parse_args();args.report.unlink(missing_ok=True)
    directory=ROOT/'build/formal-sdram';directory.mkdir(parents=True,exist_ok=True)
    original=ROOT/'soc/sdram/wasmetal_sdram_memory.sv'
    source=directory/'controller.sv';text=original.read_text()
    if text.count('endmodule')!=1:raise ValueError('review SDRAM proof injection')
    source.write_text(text.replace('endmodule',HARNESS+'\nendmodule'))
    paths=[original,source,Path(__file__).resolve(),ROOT/'tools/check_sdram.py',ROOT/'tools/upstream.lock.json']
    inputs={str(p.relative_to(ROOT)):digest(p) for p in paths}
    negatives=[]
    for name,(old,new) in NEGATIVES.items():
        if text.count(old)!=1:raise ValueError('review SDRAM negative mutation: '+name)
        mutation=directory/('negative-'+name+'.sv')
        mutation.write_text(text.replace(old,new).replace('endmodule',HARNESS+'\nendmodule'))
        negatives.append(prove(mutation,directory,'negative-'+name,
            PROFILES['synthetic-minimum'],args.timeout_seconds,negative=True))
        print('PASS rejected SDRAM protocol mutation '+name,flush=True)
    results=[]
    for name in args.profile or PROFILES:
        results.append(prove(source,directory,name,PROFILES[name],args.timeout_seconds))
        print('PASS SDRAM protocol induction '+name,flush=True)
    if any(digest(ROOT/name)!=value for name,value in inputs.items()):raise ValueError('SDRAM proof inputs changed')
    report={'status':'passed','scope':'unbounded controller protocol safety; no DRAM storage, analog or physical timing proof',
        'environment':'initial cold reset, then arbitrary binary requests, read input and warm resets',
        'configurations':results,'negative_controls':negatives,'inputs':inputs,'physical_hardware_tested':False}
    args.report.parent.mkdir(exist_ok=True);args.report.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
