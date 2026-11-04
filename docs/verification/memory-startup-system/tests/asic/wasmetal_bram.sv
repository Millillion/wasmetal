// SPDX-License-Identifier: MIT
// Simulation-only binding of the existing backend port to the ASIC adapter.
// The integration builder excludes soc/memory/wasmetal_bram.sv and includes
// this file explicitly. Normal FPGA builds never read this replacement.
module wasmetal_bram #(
    parameter integer RAM_BYTES=131072
) (
    input wire clk, reset, valid, write,
    input wire [31:0] address,
    input wire [15:0] mask,
    input wire [127:0] wdata,
    output wire ready, fault,
    output wire [127:0] rdata
);
    localparam integer LATENCY=`WASMETAL_TEST_SRAM_LATENCY,
        WORDS=RAM_BYTES/16, AW=WORDS>1 ? $clog2(WORDS) : 1;
    wire enable,macro_write;
    wire [AW-1:0] macro_address;
    wire [15:0] byte_enable;
    wire [127:0] write_data;
    logic [127:0] memory [0:WORDS-1];
    logic [127:0] pipeline [0:LATENCY-1];
    logic [LATENCY-1:0] pipeline_valid;
    logic [127:0] output_data;
`ifdef WASMETAL_TEST_CORRUPT_SRAM
    wire [127:0] read_data=output_data^128'h1;
`else
    wire [127:0] read_data=output_data;
`endif
    wasmetal_sram_memory #(.RAM_BYTES(RAM_BYTES),.READ_LATENCY(LATENCY)) adapter(
        .clk(clk),.reset(reset),.valid(valid),.write(write),.address(address),
        .mask(mask),.wdata(wdata),.ready(ready),.fault(fault),.rdata(rdata),
        .sram_enable(enable),.sram_write(macro_write),.sram_address(macro_address),
        .sram_byte_enable(byte_enable),.sram_wdata(write_data),.sram_rdata(read_data));

    // Nonzero power-on contents expose missing boot initialization. Reset is
    // intentionally absent from the memory and its outstanding read pipeline.
    initial begin
        for(integer word=0;word<WORDS;word=word+1)
            memory[word]=128'hd1b54a32d192ed039e3779b97f4a7c15^128'(word);
        pipeline_valid=0;
        output_data=128'hffffffffffffffffffffffffffffffff;
    end
    generate if(LATENCY==1) begin: immediate_read
        always_ff @(posedge clk) begin
            if(enable && !macro_write) output_data<=memory[macro_address];
        end
    end else begin: delayed_read
        always_ff @(posedge clk) begin
            pipeline_valid[0]<=enable && !macro_write;
            if(enable && !macro_write) pipeline[0]<=memory[macro_address];
            for(integer stage=1;stage<LATENCY-1;stage=stage+1) begin
                pipeline_valid[stage]<=pipeline_valid[stage-1];
                if(pipeline_valid[stage-1]) pipeline[stage]<=pipeline[stage-1];
            end
            if(pipeline_valid[LATENCY-2]) output_data<=pipeline[LATENCY-2];
        end
    end endgenerate
    always_ff @(posedge clk) begin
        if(enable) begin
            assert(32'(macro_address)<WORDS);
            if(macro_write)
                for(integer lane=0;lane<16;lane=lane+1)
                    if(byte_enable[lane]) memory[macro_address][lane*8+:8]<=write_data[lane*8+:8];
        end
    end
endmodule
