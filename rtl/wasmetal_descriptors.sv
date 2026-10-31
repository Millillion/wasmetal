// SPDX-License-Identifier: MIT
// Small descriptor RAM with two read ports and an architecturally visible
// pending write. Reset clears validity instead of resetting every stored bit.
module wasmetal_descriptors #(
    parameter integer COUNT=256,
    parameter integer WIDTH=64
) (
    input logic clk,reset,pending_write,
    input logic [31:0] write_index,read_index_a,read_index_b,
    input logic [WIDTH-1:0] write_data,
    output wire [WIDTH-1:0] read_data_a,read_data_b
);
    localparam integer ADDRESS_BITS=COUNT>1 ? $clog2(COUNT):1;
    logic [WIDTH-1:0] words[0:COUNT-1];
    logic [COUNT-1:0] valid;
    assign read_data_a=read_index_a>=COUNT ? {WIDTH{1'b0}} :
        pending_write && write_index==read_index_a ? write_data :
        valid[ADDRESS_BITS'(read_index_a)] ? words[ADDRESS_BITS'(read_index_a)] : {WIDTH{1'b0}};
    assign read_data_b=read_index_b>=COUNT ? {WIDTH{1'b0}} :
        pending_write && write_index==read_index_b ? write_data :
        valid[ADDRESS_BITS'(read_index_b)] ? words[ADDRESS_BITS'(read_index_b)] : {WIDTH{1'b0}};
    always_ff @(posedge clk) begin
        if(reset) valid<='0;
        else if(pending_write && write_index<COUNT) begin
            words[ADDRESS_BITS'(write_index)]<=write_data;
            valid[ADDRESS_BITS'(write_index)]<=1;
        end
    end
endmodule
