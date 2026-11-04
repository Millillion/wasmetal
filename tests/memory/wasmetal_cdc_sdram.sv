// SPDX-License-Identifier: MIT
// Test composition of production modules. All observation ports are module
// interfaces or SDRAM pins; no implementation state is exposed or driven.
`include "sdram_test_parameters.svh"
module wasmetal_cdc_sdram (
    input wire s_clk,m_clk,reset,cold_reset,
    input wire s_valid,s_write,
    input wire [31:0] s_address,
    input wire [15:0] s_mask,
    input wire [127:0] s_wdata,
    output wire s_ready,s_fault,source_online,s_reset,available,
    output wire [127:0] s_rdata,
    output wire initialized,m_valid,m_ready,
    // Asynchronous assertion and synchronous release in the crossing; sampled
    // on that same destination clock by the SDR controller.
    /* verilator lint_off SYNCASYNCNET */
    output wire m_reset,
    /* verilator lint_on SYNCASYNCNET */
    output wire sdram_cke,sdram_cs_n,sdram_ras_n,sdram_cas_n,sdram_we_n,sdram_dq_oe,
    output wire [12:0] sdram_address,
    output wire [1:0] sdram_bank,sdram_dqm,
    output wire [15:0] sdram_dq_out,
    input wire [15:0] sdram_dq_in
);
    wire m_write,m_fault;
    wire [31:0] m_address;
    wire [15:0] m_mask;
    wire [127:0] m_wdata,m_rdata;
    (* ASYNC_REG="TRUE", async_reg="true" *) logic [1:0] startup_sync;
    always_ff @(posedge s_clk or posedge reset)
        if(reset) startup_sync<=0;
        else startup_sync<={startup_sync[0],initialized};
    assign available=source_online && !s_reset && startup_sync[1];
    wasmetal_memory_cdc crossing(
        .s_clk(s_clk),.m_clk(m_clk),.reset(reset),.source_online(source_online),
        .s_reset(s_reset),.m_reset(m_reset),.s_valid(s_valid && available),
        .s_write(s_write),.s_address(s_address),.s_mask(s_mask),.s_wdata(s_wdata),
        .s_ready(s_ready),.s_fault(s_fault),.s_rdata(s_rdata),
        .m_valid(m_valid),.m_write(m_write),.m_address(m_address),.m_mask(m_mask),
        .m_wdata(m_wdata),.m_ready(m_ready),.m_fault(m_fault),.m_rdata(m_rdata));
`ifdef WASMETAL_TEST_COLD_WARM_RESET
    wire controller_reset=cold_reset || m_reset;
`else
    wire controller_reset=cold_reset;
`endif
    wasmetal_sdram_memory #(
        .RAM_BYTES(`SDRAM_RAM_BYTES),.ROW_BITS(`SDRAM_ROW_BITS),.COLUMN_BITS(`SDRAM_COLUMN_BITS),
        .POWERUP_CYCLES(`SDRAM_POWERUP_CYCLES),.REFRESH_CYCLES(`SDRAM_REFRESH_CYCLES),
        .CAS_LATENCY(`SDRAM_CAS_LATENCY),.T_RCD(`SDRAM_T_RCD),.T_RP(`SDRAM_T_RP),
        .T_RFC(`SDRAM_T_RFC),.T_RAS(`SDRAM_T_RAS),.T_WR(`SDRAM_T_WR),
        .T_RC(`SDRAM_T_RC),.T_MRD(`SDRAM_T_MRD)) controller(
        .clk(m_clk),.reset(controller_reset),.bus_reset(m_reset),
        .valid(m_valid),.write(m_write),.address(m_address),.mask(m_mask),.wdata(m_wdata),
        .initialized(initialized),.ready(m_ready),.fault(m_fault),.rdata(m_rdata),
        .sdram_cke(sdram_cke),.sdram_cs_n(sdram_cs_n),.sdram_ras_n(sdram_ras_n),
        .sdram_cas_n(sdram_cas_n),.sdram_we_n(sdram_we_n),.sdram_address(sdram_address),
        .sdram_bank(sdram_bank),.sdram_dqm(sdram_dqm),.sdram_dq_out(sdram_dq_out),
        .sdram_dq_oe(sdram_dq_oe),.sdram_dq_in(sdram_dq_in));
endmodule
