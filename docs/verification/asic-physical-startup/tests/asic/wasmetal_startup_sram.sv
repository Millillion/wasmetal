// SPDX-License-Identifier: MIT
// Verification binding for startup ownership and the real SRAM adapter.
module wasmetal_startup_sram #(
    parameter integer RAM_BYTES=131072,
    parameter integer READ_LATENCY=1,
    parameter integer RESPONSE_TIMEOUT=1024,
    parameter integer ADDRESS_WIDTH=(RAM_BYTES/16)>1 ? $clog2(RAM_BYTES/16) : 1
) (
    input wire clk, reset, cpu_valid, cpu_write,
    input wire [31:0] cpu_address,
    input wire [15:0] cpu_mask,
    input wire [127:0] cpu_wdata,
    output wire cpu_ready, cpu_fault,
    output wire [127:0] cpu_rdata,
    output wire cpu_enabled, test_busy, test_done, test_failed,
    output wire [1:0] error_code,
    output wire [31:0] error_address,
    output wire [127:0] expected_data, observed_data,
    output wire [63:0] completed_operations,
    output wire sram_enable, sram_write,
    output wire [ADDRESS_WIDTH-1:0] sram_address,
    output wire [15:0] sram_byte_enable,
    output wire [127:0] sram_wdata,
    input wire [127:0] sram_rdata
);
    wire memory_valid, memory_write, memory_ready, memory_fault;
    wire [31:0] memory_address;
    wire [15:0] memory_mask;
    wire [127:0] memory_wdata, memory_rdata;
    wasmetal_memory_startup #(.RAM_BYTES(RAM_BYTES),.RESPONSE_TIMEOUT(RESPONSE_TIMEOUT)) startup(
        .clk(clk),.reset(reset),.cpu_valid(cpu_valid),.cpu_write(cpu_write),
        .cpu_address(cpu_address),.cpu_mask(cpu_mask),.cpu_wdata(cpu_wdata),
        .cpu_ready(cpu_ready),.cpu_fault(cpu_fault),.cpu_rdata(cpu_rdata),
        .cpu_enabled(cpu_enabled),.test_busy(test_busy),.test_done(test_done),.test_failed(test_failed),
        .error_code(error_code),.error_address(error_address),.expected_data(expected_data),
        .observed_data(observed_data),.completed_operations(completed_operations),
        .memory_valid(memory_valid),.memory_write(memory_write),.memory_address(memory_address),
        .memory_mask(memory_mask),.memory_wdata(memory_wdata),
        .memory_ready(memory_ready),.memory_fault(memory_fault),.memory_rdata(memory_rdata));
    wasmetal_sram_memory #(.RAM_BYTES(RAM_BYTES),.READ_LATENCY(READ_LATENCY),
        .ADDRESS_WIDTH(ADDRESS_WIDTH)) adapter(
        .clk(clk),.reset(reset),.valid(memory_valid),.write(memory_write),
        .address(memory_address),.mask(memory_mask),.wdata(memory_wdata),
        .ready(memory_ready),.fault(memory_fault),.rdata(memory_rdata),
        .sram_enable(sram_enable),.sram_write(sram_write),.sram_address(sram_address),
        .sram_byte_enable(sram_byte_enable),.sram_wdata(sram_wdata),.sram_rdata(sram_rdata));
endmodule
