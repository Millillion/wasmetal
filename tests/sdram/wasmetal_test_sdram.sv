// SPDX-License-Identifier: MIT
// Behavioral x16 SDRAM: only public device pins and application-boundary
// monitors are visible. No controller hierarchy or state is inspected.
`include "sdram_test_parameters.svh"
/* verilator lint_off BLKSEQ */
module wasmetal_test_sdram #(parameter integer RAM_BYTES=131072) (
    input wire clk,cke,cs_n,ras_n,cas_n,we_n,dq_oe,
    input wire [12:0] address,
    input wire [1:0] bank,dqm,
    input wire [15:0] dq_out,
    output logic [15:0] dq_in,
    input wire application_reset,initialized,request_valid
);
    logic [15:0] memory [0:RAM_BYTES/2-1];
    bit bank_open [0:3];
    integer bank_row [0:3];
    longint activated [0:3],precharged [0:3],written [0:3];
    longint cycle=0,first_clock=-1,last_refresh=-1,recovery_until=0,last_activate=-1000000;
    bit had_precharge=0,mode_set=0,reading=0,writing=0;
    integer initial_refreshes=0,write_index=0,burst_word=0,burst_bank=0;
    longint read_start=0;
    logic [1:0] older_mask=3,previous_mask=3,drive_mask=0;
    longint reads=0,writes=0,refreshes=0,read_beats=0,write_beats=0,max_refresh_gap=0;
    longint warm_resets=0,reset_refreshes=0,startup_stalls=0;
    bit prior_reset=0;
    initial begin
        dq_in=16'hb57e;
        for(integer n=0;n<RAM_BYTES/2;n=n+1) memory[n]=16'ha93c^16'(n*73);
        for(integer b=0;b<4;b=b+1) begin
            bank_open[b]=0;bank_row[b]=0;
            activated[b]=-1000000;precharged[b]=-1000000;written[b]=-1000000;
        end
    end
    always @(posedge clk) begin: device_edge
        integer command,word_index;
        logic [1:0] delayed_mask;
        logic [15:0] value;
        bit continuation;
        cycle=cycle+1;
        command=cs_n ? 7 : integer'({ras_n,cas_n,we_n});
        delayed_mask=older_mask;older_mask=previous_mask;previous_mask=dqm;
        assert(!(dq_oe && drive_mask!=0)) else $fatal(1,"SDRAM data bus contention");
        drive_mask=0;dq_in<=16'hb57e^16'(cycle);
        if(application_reset && !prior_reset && mode_set) warm_resets=warm_resets+1;
        prior_reset=application_reset;
        if(!application_reset && !initialized) startup_stalls=startup_stalls+1;
        if(request_valid) assert(initialized)
            else $fatal(1,"memory request issued before SDRAM startup finished");
        if(!cke) begin
            assert(!mode_set && command==7 && !dq_oe)
                else $fatal(1,"unexpected SDRAM clock suspension");
        end else begin
            if(first_clock<0) first_clock=cycle;
            if(command!=7) begin
                assert(cycle-first_clock>=`SDRAM_POWERUP_CYCLES) else $fatal(1,"SDRAM startup wait violated");
                assert(cycle>=recovery_until) else $fatal(1,"SDRAM command before timing recovery");
            end
            if(mode_set) begin
                assert(last_refresh>=0 && cycle-last_refresh<=`SDRAM_REFRESH_CYCLES)
                    else $fatal(1,"SDRAM refresh deadline missed");
                if(cycle-last_refresh>max_refresh_gap) max_refresh_gap=cycle-last_refresh;
            end
            for(integer b=0;b<4;b=b+1)
                if(bank_open[b]) assert(cycle-activated[b]<3000) else $fatal(1,"SDRAM row held open");
            continuation=writing;
            if(writing) assert(command==7) else $fatal(1,"SDRAM write burst interrupted");
            case(command)
                2: begin
                    assert(!writing && !reading) else $fatal(1,"SDRAM precharge interrupted burst");
                    assert(address[10] || bank_open[bank]) else $fatal(1,"SDRAM precharge of idle bank");
                    for(integer b=0;b<4;b=b+1) if(address[10] || b==integer'(bank)) begin
                        assert(!bank_open[b] || cycle-activated[b]>=`SDRAM_T_RAS) else $fatal(1,"SDRAM tRAS");
                        assert(cycle-written[b]>=`SDRAM_T_WR) else $fatal(1,"SDRAM tWR");
                        bank_open[b]=0;precharged[b]=cycle;
                    end
                    had_precharge=1;
                end
                1: begin
                    assert(had_precharge && !reading && !writing) else $fatal(1,"invalid SDRAM refresh");
                    for(integer b=0;b<4;b=b+1) begin
                        assert(!bank_open[b] && cycle-precharged[b]>=`SDRAM_T_RP) else $fatal(1,"SDRAM refresh before tRP");
                    end
                    recovery_until=cycle+`SDRAM_T_RFC;last_refresh=cycle;refreshes=refreshes+1;
                    if(application_reset && mode_set) reset_refreshes=reset_refreshes+1;
                    if(!mode_set) initial_refreshes=initial_refreshes+1;
                end
                0: begin
                    assert(!mode_set && initial_refreshes==2 && bank==0 &&
                        address==13'(`SDRAM_CAS_LATENCY*16+3)) else $fatal(1,"SDRAM mode programming");
                    for(integer b=0;b<4;b=b+1) assert(!bank_open[b]);
                    mode_set=1;recovery_until=cycle+`SDRAM_T_MRD;
                end
                3: begin
                    assert(mode_set && !bank_open[bank] && !reading && !writing) else $fatal(1,"invalid SDRAM activate");
                    assert(cycle-precharged[bank]>=`SDRAM_T_RP) else $fatal(1,"SDRAM activate before tRP");
                    assert(cycle-activated[bank]>=`SDRAM_T_RC && cycle-last_activate>=`SDRAM_T_RC)
                        else $fatal(1,"SDRAM tRC");
                    bank_open[bank]=1;bank_row[bank]=integer'(address);
                    activated[bank]=cycle;last_activate=cycle;
                end
                4,5: begin
                    assert(mode_set && bank_open[bank] && cycle-activated[bank]>=`SDRAM_T_RCD)
                        else $fatal(1,"SDRAM access before tRCD");
                    assert(!reading && !writing && address<512 && address[2:0]==0)
                        else $fatal(1,"SDRAM burst geometry");
                    burst_word=((bank_row[bank]*4+integer'(bank))*512)+integer'(address);
                    burst_bank=integer'(bank);
                    assert(burst_word>=0 && burst_word+8<=RAM_BYTES/2) else $fatal(1,"SDRAM physical address out of bounds");
                    if(command==4) begin writing=1;write_index=0;writes=writes+1;end
                    else begin reading=1;read_start=cycle+`SDRAM_CAS_LATENCY;reads=reads+1;end
                end
                7: begin end
                default: $fatal(1,"unsupported SDRAM device command");
            endcase
            if(writing) begin
                assert(dq_oe && write_index<8) else $fatal(1,"missing SDRAM write data");
                word_index=burst_word+write_index;
                if(!dqm[0]) memory[word_index][7:0]=dq_out[7:0];
                if(!dqm[1]) memory[word_index][15:8]=dq_out[15:8];
                written[burst_bank]=cycle;write_index=write_index+1;write_beats=write_beats+1;
                if(write_index==8) writing=0;
            end else if(!continuation) assert(!dq_oe) else $fatal(1,"SDRAM DQ driven outside write");
            if(reading && cycle>=read_start) begin
                if(cycle-read_start==8) reading=0;
                else begin
                    assert(cycle-read_start<8);
                    value=memory[burst_word+integer'(cycle-read_start)];
`ifdef WASMETAL_TEST_CORRUPT_SDRAM
                    value=value^16'h0001;
`endif
                    drive_mask=~delayed_mask;
                    if(delayed_mask[0]) value[7:0]=8'h7e^8'(cycle);
                    if(delayed_mask[1]) value[15:8]=8'hb5^8'(cycle>>8);
                    dq_in<=value;read_beats=read_beats+1;
                end
            end
        end
    end
    final begin
        integer file;
        file=$fopen(`WASMETAL_TEST_SDRAM_COVERAGE,"a");
        if(file==0) $fatal(1,"could not write SDRAM system coverage");
        $fdisplay(file,"{\"reads\":%0d,\"writes\":%0d,\"refreshes\":%0d,\"read_beats\":%0d,\"write_beats\":%0d,\"maximum_refresh_gap\":%0d,\"warm_resets\":%0d,\"refreshes_during_reset\":%0d,\"startup_stalls\":%0d}",
            reads,writes,refreshes,read_beats,write_beats,max_refresh_gap,warm_resets,reset_refreshes,startup_stalls);
        $fclose(file);
    end
endmodule
