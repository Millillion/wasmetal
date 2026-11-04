// SPDX-License-Identifier: MIT
// Verification binding: destructive self-test master and real SRAM adapter.
// The independent harness supplies only the external macro pins.
module wasmetal_bist_sram #(
    parameter integer RAM_BYTES=131072,
    parameter integer READ_LATENCY=1,
    parameter integer RESPONSE_TIMEOUT=1024,
    parameter integer ADDRESS_WIDTH=(RAM_BYTES/16)>1 ? $clog2(RAM_BYTES/16) : 1
) (
    input wire clk, reset, start,
    output wire busy, done, failed,
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
    wire request_valid, request_write, response_ready, response_fault;
    wire [31:0] request_address;
    wire [15:0] request_mask;
    wire [127:0] request_data, response_data;
    wasmetal_memory_bist #(.RAM_BYTES(RAM_BYTES),.RESPONSE_TIMEOUT(RESPONSE_TIMEOUT)) master(
        .clk(clk),.reset(reset),.start(start),.busy(busy),.done(done),.failed(failed),
        .error_code(error_code),.error_address(error_address),.expected_data(expected_data),
        .observed_data(observed_data),.completed_operations(completed_operations),
        .valid(request_valid),.write(request_write),.address(request_address),
        .mask(request_mask),.wdata(request_data),.ready(response_ready),
        .fault(response_fault),.rdata(response_data));
    wasmetal_sram_memory #(.RAM_BYTES(RAM_BYTES),.READ_LATENCY(READ_LATENCY),
        .ADDRESS_WIDTH(ADDRESS_WIDTH)) adapter(
        .clk(clk),.reset(reset),.valid(request_valid),.write(request_write),
        .address(request_address),.mask(request_mask & 16'hfffe),.wdata(request_data),
        .ready(response_ready),.fault(response_fault),.rdata(response_data),
        .sram_enable(sram_enable),.sram_write(sram_write),.sram_address(sram_address),
        .sram_byte_enable(sram_byte_enable),.sram_wdata(sram_wdata),.sram_rdata(sram_rdata));
endmodule
