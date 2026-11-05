// SPDX-License-Identifier: MIT
// Experimental bank wrapper for the named OpenRAM macro, not a physical signoff.
// Four 512x32 macros form one 8 KiB bank of 128-bit words.
// Connect through wasmetal_sram_memory: only one transaction may be outstanding.
module wasmetal_sky130_sram #(
    parameter integer RAM_BYTES = 131072,
    parameter integer ADDRESS_WIDTH = $clog2(RAM_BYTES / 16),
    // Used only when WASMETAL_SKY130_SRAM_MODEL selects the upstream model.
    parameter integer MODEL_DELAY = 3,
    parameter integer MODEL_HOLD = 1
) (
    input wire clk, reset, enable, write,
    input wire [ADDRESS_WIDTH-1:0] address,
    input wire [15:0] byte_enable,
    input wire [127:0] wdata,
    output wire [127:0] rdata
);
    localparam integer BANKS = RAM_BYTES / 8192;
    localparam integer BANK_BITS = BANKS > 1 ? $clog2(BANKS) : 1;
    wire [127:0] bank_data [0:BANKS-1];
    logic pending;
    logic [BANK_BITS-1:0] selected;
    logic [127:0] held;
    wire [127:0] sampled = bank_data[selected];

    initial begin
        if (RAM_BYTES < 8192 || RAM_BYTES % 8192 != 0)
            $fatal(1, "SKY130 wrapper requires whole 8 KiB banks");
        if (ADDRESS_WIDTH != $clog2(RAM_BYTES / 16))
            $fatal(1, "SKY130 wrapper address width mismatch");
    end

    // The upstream macro latches commands at the rising edge and completes
    // reads after the falling edge. At the next rising edge the consumer may
    // sample directly. Save that value before subsequent idle edges invalidate
    // the model's output, so an adapter with a longer latency sees the same data.
    assign rdata = pending ? sampled : held;
    always_ff @(posedge clk) begin
        if (reset) begin
            pending <= 0;
            selected <= 0;
            held <= 0;
        end else begin
            if (pending) held <= sampled;
            pending <= enable && !write;
            if (enable && !write) selected <= BANK_BITS'(32'(address) >> 9);
        end
    end

    for (genvar bank = 0; bank < BANKS; bank++) begin: banks
        for (genvar lane = 0; lane < 4; lane++) begin: lanes
            wire active = enable && !reset && (32'(address) >> 9) == bank &&
                          (!write || byte_enable[lane*4+:4] != 0);
            sky130_sram_2kbyte_1rw1r_32x512_8
`ifdef WASMETAL_SKY130_SRAM_MODEL
            #(.VERBOSE(0), .DELAY(MODEL_DELAY), .T_HOLD(MODEL_HOLD))
`endif
            memory (
                .clk0(clk), .csb0(!active), .web0(!write),
                .wmask0(byte_enable[lane*4+:4]), .addr0(9'(address)),
                .din0(wdata[lane*32+:32]), .dout0(bank_data[bank][lane*32+:32]),
                .clk1(1'b0), .csb1(1'b1), .addr1(9'b0), .dout1()
            );
        end
    end
endmodule
