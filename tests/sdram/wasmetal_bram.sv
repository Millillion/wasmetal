// SPDX-License-Identifier: MIT
// Simulation-only backend binding. Normal FPGA builds never read this file.
`include "sdram_test_parameters.svh"
module wasmetal_bram #(parameter integer RAM_BYTES=131072) (
    input wire clk,reset,valid,write,
    input wire [31:0] address,
    input wire [15:0] mask,
    input wire [127:0] wdata,
    output wire ready,fault,initialized,
    output wire [127:0] rdata
);
    // Model creation is power-on. Application resets must not restart SDRAM.
    logic cold_reset=1;
    always_ff @(posedge clk) cold_reset<=0;
    wire cke,cs_n,ras_n,cas_n,we_n,dq_oe;
    wire [12:0] pin_address;
    wire [1:0] bank,dqm;
    wire [15:0] dq_out,dq_in;
    wasmetal_sdram_memory #(.RAM_BYTES(RAM_BYTES),
        .ROW_BITS(13),.COLUMN_BITS(9),
        .POWERUP_CYCLES(`SDRAM_POWERUP_CYCLES),.REFRESH_CYCLES(`SDRAM_REFRESH_CYCLES),
        .CAS_LATENCY(`SDRAM_CAS_LATENCY),.T_RCD(`SDRAM_T_RCD),.T_RP(`SDRAM_T_RP),
        .T_RFC(`SDRAM_T_RFC),.T_RAS(`SDRAM_T_RAS),.T_WR(`SDRAM_T_WR),
        .T_RC(`SDRAM_T_RC),.T_MRD(`SDRAM_T_MRD)) controller(
        .clk(clk),.reset(cold_reset),.bus_reset(reset),.valid(valid),.write(write),
        .address(address),.mask(mask),.wdata(wdata),.ready(ready),.fault(fault),.rdata(rdata),
        .initialized(initialized),.sdram_cke(cke),.sdram_cs_n(cs_n),.sdram_ras_n(ras_n),
        .sdram_cas_n(cas_n),.sdram_we_n(we_n),.sdram_address(pin_address),.sdram_bank(bank),
        .sdram_dqm(dqm),.sdram_dq_out(dq_out),.sdram_dq_oe(dq_oe),.sdram_dq_in(dq_in));
    wasmetal_test_sdram #(.RAM_BYTES(RAM_BYTES)) device(
        .clk(clk),.cke(cke),.cs_n(cs_n),.ras_n(ras_n),.cas_n(cas_n),.we_n(we_n),
        .address(pin_address),.bank(bank),.dqm(dqm),.dq_out(dq_out),.dq_oe(dq_oe),.dq_in(dq_in),
        .application_reset(reset),.initialized(initialized),.request_valid(valid));
endmodule
