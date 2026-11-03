// SPDX-License-Identifier: MIT
// Bounded Wasm regions backed by masked, 128-bit local block RAM.
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
    wasmetal_memory_bridge #(.RAM_BYTES(RAM_BYTES),.REGIONS_PER_KIND(REGIONS_PER_KIND)) bridge(
        .clk(clk),.reset(reset),.initialized(initialized),.initialization_failed(initialization_failed),
        .valid(valid),.write(write),.initialize(initialize),.kind(kind),.index(index),
        .address(address),.bytes(bytes),.wdata(wdata),.region(region),
        .ready(ready),.fault(fault),.rdata(rdata),
        .bus_valid(bus_valid),.bus_write(bus_write),.bus_address(bus_address),
        .bus_mask(bus_mask),.bus_wdata(bus_wdata),.bus_ready(bus_ready),
        .bus_fault(bus_fault),.bus_rdata(bus_rdata));
    wasmetal_bram #(.RAM_BYTES(RAM_BYTES)) ram_backend(
        .clk(clk),.reset(reset),.valid(bus_valid),.write(bus_write),
        .address(bus_address),.mask(bus_mask),.wdata(bus_wdata),
        .ready(bus_ready),.fault(bus_fault),.rdata(bus_rdata));
endmodule
