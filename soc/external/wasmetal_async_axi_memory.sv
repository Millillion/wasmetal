// SPDX-License-Identifier: MIT
// Complete transport from a CPU-domain physical request to a separate AXI clock.
// The external AXI interface must share axi_reset. Online describes this link's
// reset sequencing; controller calibration must be handled by its integration.
module wasmetal_async_axi_memory #(
    parameter logic [31:0] BASE_ADDRESS=0,
    parameter integer ID_WIDTH=4
) (
    input wire clk, axi_clk, reset, valid, write,
    input wire [31:0] address,
    input wire [15:0] mask,
    input wire [127:0] wdata,
    output wire ready, fault, online, source_reset,
    // This reset asserts asynchronously and releases after two AXI clock edges.
    // CDC state uses async reset; the adapter samples that same stretched reset.
    /* verilator lint_off SYNCASYNCNET */
    output wire axi_reset,
    /* verilator lint_on SYNCASYNCNET */
    output wire [127:0] rdata,
    output wire awvalid, wvalid, arvalid, bready, rready,
    input wire awready, wready, arready, bvalid, rvalid,
    output wire [31:0] awaddr, araddr,
    output wire [ID_WIDTH-1:0] awid, arid,
    input wire [ID_WIDTH-1:0] bid, rid,
    output wire [7:0] awlen, arlen,
    output wire [2:0] awsize, arsize, awprot, arprot,
    output wire [1:0] awburst, arburst,
    output wire awlock, arlock,
    output wire [3:0] awcache, arcache, awqos, arqos,
    output wire [127:0] write_data,
    output wire [15:0] wstrb,
    output wire wlast,
    input wire [127:0] read_data,
    input wire [1:0] bresp, rresp,
    input wire rlast
);
    wire bus_valid,bus_write,bus_ready,bus_fault;
    wire [31:0] bus_address;
    wire [15:0] bus_mask;
    wire [127:0] bus_wdata,bus_rdata;
    wasmetal_memory_cdc crossing(
        .s_clk(clk),.m_clk(axi_clk),.reset(reset),.source_online(online),
        .s_reset(source_reset),.m_reset(axi_reset),
        .s_valid(valid),.s_write(write),.s_address(address),.s_mask(mask),.s_wdata(wdata),
        .s_ready(ready),.s_fault(fault),.s_rdata(rdata),
        .m_valid(bus_valid),.m_write(bus_write),.m_address(bus_address),.m_mask(bus_mask),.m_wdata(bus_wdata),
        .m_ready(bus_ready),.m_fault(bus_fault),.m_rdata(bus_rdata));
    wasmetal_axi_memory #(.BASE_ADDRESS(BASE_ADDRESS),.ID_WIDTH(ID_WIDTH)) adapter(
        .clk(axi_clk),.reset(axi_reset),.valid(bus_valid),.write(bus_write),.address(bus_address),
        .mask(bus_mask),.wdata(bus_wdata),.ready(bus_ready),.fault(bus_fault),.rdata(bus_rdata),.*);
endmodule
