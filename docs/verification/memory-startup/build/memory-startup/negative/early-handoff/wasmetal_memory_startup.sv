// SPDX-License-Identifier: MIT
// Destructive startup test followed by exclusive CPU ownership. Reset this
// controller and its memory backend together. Every reset starts a new test.
module wasmetal_memory_startup #(
    parameter integer RAM_BYTES=131072,
    parameter integer RESPONSE_TIMEOUT=1024
) (
    input wire clk, reset,
    input wire cpu_valid, cpu_write,
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
    output wire memory_valid, memory_write,
    output wire [31:0] memory_address,
    output wire [15:0] memory_mask,
    output wire [127:0] memory_wdata,
    input wire memory_ready, memory_fault,
    input wire [127:0] memory_rdata
);
    logic launched;
    wire test_valid, test_write;
    wire [31:0] test_address;
    wire [15:0] test_mask;
    wire [127:0] test_wdata;
    always_ff @(posedge clk) begin
        if(reset) launched<=0;
        else launched<=1;
    end

    // done follows a complete low-valid release cycle. Failed tests retain
    // ownership, including a timed-out request waiting for its late response.
    assign cpu_enabled=launched && !test_failed && !reset;
    assign memory_valid=!reset && (cpu_enabled ? cpu_valid : test_valid);
    assign memory_write=memory_valid && (cpu_enabled ? cpu_write : test_write);
    assign memory_address=cpu_enabled ? cpu_address : test_address;
    assign memory_mask=cpu_enabled ? cpu_mask : test_mask;
    assign memory_wdata=cpu_enabled ? cpu_wdata : test_wdata;
    assign cpu_ready=cpu_enabled && cpu_valid && memory_ready;
    assign cpu_fault=cpu_ready && memory_fault;
    assign cpu_rdata=cpu_enabled ? memory_rdata : 128'b0;

    wasmetal_memory_bist #(.RAM_BYTES(RAM_BYTES),.RESPONSE_TIMEOUT(RESPONSE_TIMEOUT)) test_master(
        .clk(clk),.reset(reset),.start(!launched),
        .busy(test_busy),.done(test_done),.failed(test_failed),
        .error_code(error_code),.error_address(error_address),
        .expected_data(expected_data),.observed_data(observed_data),
        .completed_operations(completed_operations),
        .valid(test_valid),.write(test_write),.address(test_address),
        .mask(test_mask),.wdata(test_wdata),
        .ready(!cpu_enabled && memory_ready),.fault(memory_fault),.rdata(memory_rdata));
endmodule
