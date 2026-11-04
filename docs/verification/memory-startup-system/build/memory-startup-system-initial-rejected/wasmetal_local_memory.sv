// SPDX-License-Identifier: MIT
// Simulation-only complete-CPU binding with destructive startup testing.
// Hold the bridge reset until the test grants access, preserving its ordinary
// transaction timeout. The backend binding supplies the actual SRAM adapter.
module wasmetal_local_memory #(
    parameter integer RAM_BYTES=131072,
    parameter integer REGIONS_PER_KIND=16,
    parameter integer LOADABLE=0,
    parameter IMAGE_DIR="build/standalone-image"
) (
    input logic clk, reset,
    output wire initialized, initialization_failed,
    input logic valid, write, initialize,
    input logic [2:0] kind,
    input logic [31:0] index,
    input logic [63:0] address,
    input logic [4:0] bytes,
    input logic [127:0] wdata,
    output wire ready, fault,
    output wire [127:0] rdata,
    input wire image_write_valid,
    input wire [31:0] image_index,
    input wire [63:0] image_region
);
    (* rom_style="block" *) logic [63:0] regions [0:6*REGIONS_PER_KIND-1];
    generate if(LOADABLE==0) begin: read_only_image
    initial $readmemh({IMAGE_DIR,"/regions.hex"},regions);
    end else begin: writable_image
        always_ff @(posedge clk)
            if(reset && image_write_valid && image_index<6*REGIONS_PER_KIND) regions[image_index]<=image_region;
    end endgenerate
    logic [63:0] region;
    always_ff @(posedge clk)
        if(LOADABLE==0 || !reset)
            region<=regions[(kind<6 && index<REGIONS_PER_KIND) ?
                            (32'(kind)*REGIONS_PER_KIND+index) : 0];

    wire bus_valid, bus_write, bus_ready, bus_fault;
    wire [31:0] bus_address;
    wire [15:0] bus_mask;
    wire [127:0] bus_wdata, bus_rdata;
    wire cpu_enabled,test_busy,test_done,test_failed,bridge_initialized,bridge_failed;
    wire [1:0] test_error_code;
    wire [31:0] test_error_address;
    wire [127:0] test_expected,test_observed;
    wire [63:0] test_count;
    wire memory_valid,memory_write,memory_ready,memory_fault;
    wire [31:0] memory_address;
    wire [15:0] memory_mask;
    wire [127:0] memory_wdata,memory_rdata;
    assign initialized=cpu_enabled && bridge_initialized;
    assign initialization_failed=test_failed || bridge_failed;
    wasmetal_memory_startup #(.RAM_BYTES(RAM_BYTES)) startup(
        .clk(clk),.reset(reset),.cpu_valid(bus_valid),.cpu_write(bus_write),
        .cpu_address(bus_address),.cpu_mask(bus_mask),.cpu_wdata(bus_wdata),
        .cpu_ready(bus_ready),.cpu_fault(bus_fault),.cpu_rdata(bus_rdata),
        .cpu_enabled(cpu_enabled),.test_busy(test_busy),.test_done(test_done),.test_failed(test_failed),
        .error_code(test_error_code),.error_address(test_error_address),
        .expected_data(test_expected),.observed_data(test_observed),.completed_operations(test_count),
        .memory_valid(memory_valid),.memory_write(memory_write),.memory_address(memory_address),
        .memory_mask(memory_mask),.memory_wdata(memory_wdata),
        .memory_ready(memory_ready),.memory_fault(memory_fault),.memory_rdata(memory_rdata));
    always_ff @(posedge clk) begin
        if(!reset && cpu_enabled) begin
            assert(test_done && !test_busy && !test_failed && test_count==80*64'(RAM_BYTES/16));
        end
        if(!reset && !cpu_enabled) begin assert(!bus_valid && !initialized);end
    end
    wasmetal_memory_bridge #(.RAM_BYTES(RAM_BYTES),.REGIONS_PER_KIND(REGIONS_PER_KIND)) bridge(
        .clk(clk),.reset(reset || !cpu_enabled),.initialized(bridge_initialized),.initialization_failed(bridge_failed),
        .valid(valid),.write(write),.initialize(initialize),.kind(kind),.index(index),
        .address(address),.bytes(bytes),.wdata(wdata),.region(region),
        .ready(ready),.fault(fault),.rdata(rdata),
        .bus_valid(bus_valid),.bus_write(bus_write),.bus_address(bus_address),
        .bus_mask(bus_mask),.bus_wdata(bus_wdata),.bus_ready(bus_ready),
        .bus_fault(bus_fault),.bus_rdata(bus_rdata));
    wasmetal_bram #(.RAM_BYTES(RAM_BYTES)) ram_backend(
        .clk(clk),.reset(reset),.valid(memory_valid),.write(memory_write),
        .address(memory_address),.mask(memory_mask),.wdata(memory_wdata),
        .ready(memory_ready),.fault(memory_fault),.rdata(memory_rdata));
endmodule
