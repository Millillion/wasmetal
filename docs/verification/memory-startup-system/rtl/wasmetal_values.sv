// SPDX-License-Identifier: MIT
// Four interleaved banks supply the four newest stack words concurrently.
// An auxiliary read reuses those ports for locals, copies, results and the fifth
// array.copy operand. The registered pending write is architecturally visible
// immediately through forwarding, then commits on the next rising edge.
// Read addresses and data are captured on falling edges for block-RAM mapping.
module wasmetal_values #(parameter integer DEPTH=16384) (
    input logic clk,
    input logic pending_write,
    input logic [31:0] write_index,
    input logic [127:0] write_data,
    input logic auxiliary,
    input logic [31:0] auxiliary_index,window_top,
    output wire [511:0] bank_words
);
    localparam integer ROWS=(DEPTH+3)/4;
    localparam integer ROW_BITS=ROWS>1 ? $clog2(ROWS):1;
    genvar bank;
    generate for(bank=0;bank<4;bank=bank+1) begin : banks
        localparam [1:0] BANK=2'(bank);
        (* ram_style="block" *) logic [127:0] words[0:ROWS-1];
        logic [127:0] read_word;
        logic [29:0] read_row;
        wire previous_row;
        if(bank==0) begin : first_bank
            assign previous_row=0;
        end else begin : following_bank
            assign previous_row=BANK>window_top[1:0];
        end
        wire [29:0] row=auxiliary ? auxiliary_index[31:2] :
            window_top[31:2]-(previous_row ? 30'd1:30'd0);
        always_ff @(negedge clk) begin
            read_word<=words[ROW_BITS'(row)];
            read_row<=row;
        end
        wire forward=pending_write && write_index<DEPTH && write_index[1:0]==BANK && write_index[31:2]==read_row;
        assign bank_words[bank*128+:128]=forward ? write_data:read_row<30'(ROWS) ? read_word:128'b0;
        always_ff @(posedge clk)
            if(pending_write && write_index<DEPTH && write_index[1:0]==BANK)
                words[ROW_BITS'(write_index[31:2])]<=write_data;
    end endgenerate
endmodule
