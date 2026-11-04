// SPDX-License-Identifier: MIT
// Private integration binding: production CDC and SDRAM controller, independent
// test clocks, synchronized startup permission and a behavioral SDRAM device.
// This is not a board PHY and is never read by a normal FPGA build.
`include "sdram_test_parameters.svh"
module wasmetal_bram #(parameter integer RAM_BYTES=131072) (
    input wire clk, reset, valid, write,
    input wire [31:0] address,
    input wire [15:0] mask,
    input wire [127:0] wdata,
    output wire ready, fault, initialized,
    output wire [127:0] rdata
);
    // The only cross-hierarchy reference is the private test top's public
    // memory-clock input. No CPU or controller state is driven by the test.
    wire memory_clk=wasmetal_loadable.memory_clk;
    logic power_on=1;
    always_ff @(posedge memory_clk) power_on<=0;
    (* ASYNC_REG="TRUE", async_reg="true" *) logic [1:0] cold_release;
    always_ff @(posedge memory_clk or posedge power_on)
        if(power_on) cold_release<=0;
        else cold_release<={cold_release[0],1'b1};
    wire cold_reset=!cold_release[1];
    wire common_reset=reset || power_on;
    wire source_online,source_reset;
    // The CDC asserts this reset asynchronously and releases it on memory_clk.
    // The SDR controller and its pin monitor sample it on that same clock.
    /* verilator lint_off SYNCASYNCNET */
    wire memory_reset;
    /* verilator lint_on SYNCASYNCNET */
    wire memory_valid,memory_write,memory_ready,memory_fault,memory_initialized;
    wire [31:0] memory_address;
    wire [15:0] memory_mask;
    wire [127:0] memory_wdata,memory_rdata;
    (* ASYNC_REG="TRUE", async_reg="true" *) logic [1:0] startup_sync;
    always_ff @(posedge clk or posedge common_reset)
        if(common_reset) startup_sync<=0;
        else startup_sync<={startup_sync[0],memory_initialized};
`ifdef WASMETAL_ASYNC_SDRAM_BYPASS_STARTUP
    assign initialized=1'b1;
`else
    assign initialized=source_online && !source_reset && startup_sync[1];
`endif
    wasmetal_memory_cdc crossing(
        .s_clk(clk),.m_clk(memory_clk),.reset(common_reset),
        .source_online(source_online),.s_reset(source_reset),.m_reset(memory_reset),
        .s_valid(valid && initialized),.s_write(write),.s_address(address),
        .s_mask(mask),.s_wdata(wdata),.s_ready(ready),.s_fault(fault),.s_rdata(rdata),
        .m_valid(memory_valid),.m_write(memory_write),.m_address(memory_address),
        .m_mask(memory_mask),.m_wdata(memory_wdata),.m_ready(memory_ready),
        .m_fault(memory_fault),.m_rdata(memory_rdata));
    wire cke,cs_n,ras_n,cas_n,we_n,dq_oe;
    wire [12:0] pin_address;
    wire [1:0] bank,dqm;
    wire [15:0] dq_out,dq_in;
`ifdef WASMETAL_ASYNC_SDRAM_WRONG_CLOCK
    wire controller_clk=clk;
`else
    wire controller_clk=memory_clk;
`endif
    wasmetal_sdram_memory #(.RAM_BYTES(RAM_BYTES),.ROW_BITS(13),.COLUMN_BITS(9),
        .POWERUP_CYCLES(`SDRAM_POWERUP_CYCLES),.REFRESH_CYCLES(`SDRAM_REFRESH_CYCLES),
        .CAS_LATENCY(`SDRAM_CAS_LATENCY),.T_RCD(`SDRAM_T_RCD),.T_RP(`SDRAM_T_RP),
        .T_RFC(`SDRAM_T_RFC),.T_RAS(`SDRAM_T_RAS),.T_WR(`SDRAM_T_WR),
        .T_RC(`SDRAM_T_RC),.T_MRD(`SDRAM_T_MRD)) controller(
        .clk(controller_clk),.reset(cold_reset),.bus_reset(memory_reset),
        .valid(memory_valid),.write(memory_write),.address(memory_address),
        .mask(memory_mask),.wdata(memory_wdata),.ready(memory_ready),
        .fault(memory_fault),.rdata(memory_rdata),.initialized(memory_initialized),
        .sdram_cke(cke),.sdram_cs_n(cs_n),.sdram_ras_n(ras_n),.sdram_cas_n(cas_n),
        .sdram_we_n(we_n),.sdram_address(pin_address),.sdram_bank(bank),
        .sdram_dqm(dqm),.sdram_dq_out(dq_out),.sdram_dq_oe(dq_oe),.sdram_dq_in(dq_in));
    wasmetal_test_sdram #(.RAM_BYTES(RAM_BYTES)) device(
        .clk(memory_clk),.cke(cke),.cs_n(cs_n),.ras_n(ras_n),.cas_n(cas_n),.we_n(we_n),
        .address(pin_address),.bank(bank),.dqm(dqm),.dq_out(dq_out),.dq_oe(dq_oe),.dq_in(dq_in),
        .application_reset(memory_reset),.initialized(memory_initialized),.request_valid(memory_valid));

    longint unsigned source_stalls=0,completed=0;
    always @(posedge clk) begin
        if(!reset && !initialized) source_stalls<=source_stalls+1;
        if(!reset && ready) begin
            assert(valid && initialized) else $fatal(1,"asynchronous SDRAM response outside live request");
            completed<=completed+1;
        end
    end
    final begin
        integer file;
        file=$fopen(`WASMETAL_ASYNC_SDRAM_COVERAGE,"a");
        if(file==0) $fatal(1,"could not write asynchronous SDRAM coverage");
        $fdisplay(file,"{\"source_startup_stalls\":%0d,\"completed_requests\":%0d}",source_stalls,completed);
        $fclose(file);
    end
endmodule
