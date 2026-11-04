// SPDX-License-Identifier: MIT
// One aligned 128-bit request becomes a complete eight-word x16 SDR burst.
// Pin commands are sampled on clk's rising edge. Read data from that edge is
// captured on the following rising edge, allowing a full cycle for tAC/board IO.
// A board wrapper must provide the forwarded clock, IO registers and constraints.
// reset is COLD reset: use only with power/clock initialization. bus_reset is a
// warm interface reset: finish accepted pin operations, discard their response,
// keep refreshing, and accept a new request only after the old bank is closed.
module wasmetal_sdram_memory #(
    parameter integer RAM_BYTES=33554432,
    parameter integer ROW_BITS=13, COLUMN_BITS=9,
    parameter integer POWERUP_CYCLES=5000, REFRESH_CYCLES=195,
    parameter integer CAS_LATENCY=2,
    parameter integer T_RCD=1, T_RP=1, T_RFC=2,
    parameter integer T_RAS=2, T_WR=2, T_RC=2, T_MRD=2
) (
    input wire clk, reset, bus_reset, valid, write,
    input wire [31:0] address,
    input wire [15:0] mask,
    input wire [127:0] wdata,
    output wire initialized, ready,
    output logic fault,
    output logic [127:0] rdata,
    output logic sdram_cke, sdram_cs_n, sdram_ras_n, sdram_cas_n, sdram_we_n,
    output logic [12:0] sdram_address,
    output logic [1:0] sdram_bank, sdram_dqm,
    output logic [15:0] sdram_dq_out,
    output logic sdram_dq_oe,
    input wire [15:0] sdram_dq_in
);
    // Reserve enough time to finish even the slowest permitted transaction,
    // return to the idle scheduler and issue refresh before its deadline.
    localparam integer TRANSACTION_BOUND=T_RCD+CAS_LATENCY+8+T_WR+T_RAS+T_RP+T_RC+16;
    localparam integer REFRESH_TRIGGER=REFRESH_CYCLES-TRANSACTION_BOUND-2;
    localparam logic [12:0] MODE_WORD=13'(CAS_LATENCY*16+3); // sequential BL8, burst writes
    function automatic integer maximum(input integer a,b);
        maximum=a>b ? a : b;
    endfunction
    localparam integer WAIT_MAX=maximum(POWERUP_CYCLES,maximum(T_RCD,
        maximum(T_RP,maximum(T_RFC,maximum(T_WR,maximum(T_MRD,CAS_LATENCY))))));
    localparam integer WAIT_WIDTH=$clog2(WAIT_MAX+1),
        REFRESH_WIDTH=$clog2(REFRESH_CYCLES+1), ROW_AGE_WIDTH=$clog2(T_RAS+T_RC+2);
    typedef enum logic [4:0] {
        POWER_WAIT,INIT_PRECHARGE,INIT_RP,INIT_REFRESH,INIT_RFC,INIT_MODE,INIT_MRD,
        IDLE,ACTIVATE,WAIT_RCD,COMMAND,WRITE_BURST,READ_WAIT,READ_BURST,
        RECOVER,PRECHARGE,WAIT_RP,RESPONSE,REFRESH,WAIT_RFC,FAILED
    } state_t;
    state_t state;
    logic [WAIT_WIDTH-1:0] remaining;
    logic [REFRESH_WIDTH-1:0] refresh_age;
    logic [ROW_AGE_WIDTH-1:0] row_age;
    logic [31:0] operation_age;
    logic [12:0] row_q;
    logic [COLUMN_BITS-1:0] column_q;
    logic [1:0] bank_q;
    logic [2:0] beat;
    logic [15:0] mask_q;
    logic [127:0] data_q;
    logic write_q, booted, second_refresh, outstanding, aborted, wait_release;
    wire legal=address[3:0]==0 && mask!=0 && {1'b0,address}+33'd16<=33'(RAM_BYTES);
    // The case comparisons prevent optimistic pin writes in four-state simulation.
    // They are not a detector for analog metastability or electrical data errors.
    // Compare with binary alternatives: explicit X constants can be treated as
    // synthesis don't-cares and must never participate in hardware permission.
    wire known_mask=(^mask===1'b0) || (^mask===1'b1);
    wire known_address=(^address===1'b0) || (^address===1'b1);
    wire known_data=(^wdata===1'b0) || (^wdata===1'b1);
    wire known_request=(legal===1'b1) && known_mask && known_address &&
        ((write===1'b0) || (write===1'b1)) && ((write===1'b0) || known_data);
    wire warm_reset=bus_reset!==1'b0;
    assign initialized=booted && state!=FAILED && !reset;
    assign ready=state==RESPONSE && !aborted && !warm_reset && !reset && valid;

    always_comb begin
        sdram_cke=!reset; sdram_cs_n=0;
        sdram_ras_n=1; sdram_cas_n=1; sdram_we_n=1;
        sdram_address=0; sdram_bank=bank_q;
        sdram_dqm=2'b11; sdram_dq_out=0; sdram_dq_oe=0;
        if(!reset) case(state)
            INIT_PRECHARGE: begin
                sdram_ras_n=0; sdram_we_n=0; sdram_address[10]=1;
            end
            INIT_REFRESH,REFRESH: begin sdram_ras_n=0; sdram_cas_n=0; end
            INIT_MODE: begin
                sdram_ras_n=0; sdram_cas_n=0; sdram_we_n=0;
                sdram_bank=0; sdram_address=MODE_WORD;
            end
            ACTIVATE: begin sdram_ras_n=0; sdram_address=row_q; end
            COMMAND: begin
                sdram_cas_n=0; sdram_we_n=!write_q;
                sdram_address=13'(column_q); // A10=0: close the bank explicitly
                sdram_dqm=write_q ? ~mask_q[1:0] : 2'b00;
                sdram_dq_oe=write_q; sdram_dq_out=data_q[15:0];
            end
            WRITE_BURST: begin
                sdram_dqm=~mask_q[{beat,1'b0}+:2];
                sdram_dq_out=data_q[{beat,4'b0}+:16]; sdram_dq_oe=1;
            end
            READ_WAIT,READ_BURST: sdram_dqm=0;
            PRECHARGE: begin sdram_ras_n=0; sdram_we_n=0; end
            default: begin end
        endcase
    end

    always_ff @(posedge clk) begin
        if(reset) begin
            state<=POWER_WAIT; remaining<=WAIT_WIDTH'(POWERUP_CYCLES-1);
            refresh_age<=0; row_age<=0; operation_age<=0;
            row_q<=0; column_q<=0; bank_q<=0; beat<=0; mask_q<=0; data_q<=0;
            write_q<=0; booted<=0; second_refresh<=0; outstanding<=0;
            aborted<=0; wait_release<=0; fault<=0; rdata<=0;
        end else begin
            if(refresh_age<REFRESH_WIDTH'(REFRESH_CYCLES)) refresh_age<=refresh_age+1'b1;
            if(outstanding) begin
                if(row_age<ROW_AGE_WIDTH'(T_RAS+T_RC+1)) row_age<=row_age+1'b1;
                operation_age<=operation_age+1'b1;
                if(warm_reset || !valid) aborted<=1;
            end
            if(warm_reset || !valid) wait_release<=0;
            case(state)
                POWER_WAIT: if(remaining==0) state<=INIT_PRECHARGE;
                    else remaining<=remaining-1'b1;
                INIT_PRECHARGE: begin remaining<=WAIT_WIDTH'(T_RP-1);state<=INIT_RP;end
                INIT_RP: if(remaining==0) state<=INIT_REFRESH;
                    else remaining<=remaining-1'b1;
                INIT_REFRESH: begin remaining<=WAIT_WIDTH'(T_RFC-1);state<=INIT_RFC;refresh_age<=0;end
                INIT_RFC: if(remaining==0) begin
                    if(second_refresh) state<=INIT_MODE;
                    else begin second_refresh<=1;state<=INIT_REFRESH;end
                end else remaining<=remaining-1'b1;
                INIT_MODE: begin remaining<=WAIT_WIDTH'(T_MRD-1);state<=INIT_MRD;end
                INIT_MRD: if(remaining==0) begin booted<=1;state<=IDLE;end
                    else remaining<=remaining-1'b1;
                IDLE: begin
                    if(refresh_age>=REFRESH_WIDTH'(REFRESH_TRIGGER)) state<=REFRESH;
                    else if(valid && !warm_reset && !wait_release) begin
                        write_q<=write;mask_q<=mask;data_q<=wdata;
                        bank_q<=address[COLUMN_BITS+1+:2];
                        row_q<=13'(ROW_BITS'(address >> (COLUMN_BITS+3)));
                        column_q<=address[1+:COLUMN_BITS];
                        rdata<=0;fault<=!known_request;beat<=0;
                        outstanding<=1;aborted<=0;operation_age<=0;row_age<=0;
                        state<=known_request ? ACTIVATE : RESPONSE;
                    end
                end
                ACTIVATE: begin row_age<=0;remaining<=WAIT_WIDTH'(T_RCD-1);state<=WAIT_RCD;end
                WAIT_RCD: if(remaining==0) state<=COMMAND;
                    else remaining<=remaining-1'b1;
                COMMAND: if(write_q) begin beat<=1;state<=WRITE_BURST;end
                    else begin remaining<=WAIT_WIDTH'(CAS_LATENCY);state<=READ_WAIT;end
                WRITE_BURST: if(beat==7) begin remaining<=WAIT_WIDTH'(T_WR-1);state<=RECOVER;end
                    else beat<=beat+1'b1;
                READ_WAIT: if(remaining==0) begin
                    rdata[15:0]<=sdram_dq_in;beat<=1;state<=READ_BURST;
                end else remaining<=remaining-1'b1;
                READ_BURST: begin
                    rdata[{beat,4'b0}+:16]<=sdram_dq_in;
                    if(beat==7) begin remaining<=0;state<=RECOVER;end
                    else beat<=beat+1'b1;
                end
                RECOVER: if(remaining!=0) remaining<=remaining-1'b1;
                    else if(row_age>=ROW_AGE_WIDTH'(T_RAS)) state<=PRECHARGE;
                PRECHARGE: begin remaining<=WAIT_WIDTH'(T_RP-1);state<=WAIT_RP;end
                WAIT_RP: if(remaining==0 && row_age>=ROW_AGE_WIDTH'(T_RC)) state<=RESPONSE;
                    else if(remaining!=0) remaining<=remaining-1'b1;
                RESPONSE: begin
                    outstanding<=0;
                    wait_release<=valid && !warm_reset && !aborted;
                    state<=IDLE;
                end
                REFRESH: begin refresh_age<=0;remaining<=WAIT_WIDTH'(T_RFC-1);state<=WAIT_RFC;end
                WAIT_RFC: if(remaining==0) state<=IDLE;
                    else remaining<=remaining-1'b1;
                FAILED: begin end
                default: begin state<=FAILED;booted<=0;fault<=1;end
            endcase
        end
    end

`ifdef WASMETAL_ASSERTIONS
    initial begin
        assert(ROW_BITS>=1 && ROW_BITS<=13 && COLUMN_BITS>=3 && COLUMN_BITS<=10);
        assert(RAM_BYTES>=16 && RAM_BYTES%16==0 && 64'(RAM_BYTES)<=(64'd1 << (ROW_BITS+COLUMN_BITS+3)));
        assert(POWERUP_CYCLES>=2 && REFRESH_TRIGGER>T_RFC+T_MRD+8);
        assert(CAS_LATENCY==2 || CAS_LATENCY==3);
        assert(T_RCD>=1 && T_RP>=1 && T_RFC>=1 && T_RAS>=1 && T_WR>=2 && T_RC>=1 && T_MRD>=2);
    end
    always_ff @(posedge clk) if(!reset) begin
        assert(state!=FAILED && state<=FAILED);
        if(booted) assert(refresh_age<REFRESH_WIDTH'(REFRESH_CYCLES));
        if(outstanding) assert(operation_age<32'(TRANSACTION_BOUND));
        if(sdram_dq_oe) assert(outstanding && write_q && (state==COMMAND || state==WRITE_BURST));
        if(ready) assert(outstanding && !aborted && !warm_reset);
        if(state==ACTIVATE || state==COMMAND || state==PRECHARGE) assert(outstanding && booted);
        if(state==REFRESH) assert(!outstanding && booted);
    end
`endif
endmodule
