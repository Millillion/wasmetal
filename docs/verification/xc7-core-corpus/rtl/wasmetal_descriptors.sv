// SPDX-License-Identifier: MIT
// Small descriptor RAM with two read ports and an architecturally visible
// pending write. Reset clears validity instead of resetting every stored bit.
// Both reads capture their address, data and validity on the falling edge.
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
    wire [95:0] checked_indices={read_index_b,read_index_a,write_index};
    wire [2:0] in_range;
    genvar port_index;
    generate for(port_index=0;port_index<3;port_index=port_index+1) begin: bounds
        wire [31:0] index=checked_indices[port_index*32+:32];
        if(COUNT==(1<<ADDRESS_BITS)) begin: power_of_two
            assign in_range[port_index]=!(|index[31:ADDRESS_BITS]);
        end else begin: other_capacity
            assign in_range[port_index]=!(|index[31:ADDRESS_BITS]) && index[ADDRESS_BITS-1:0]<ADDRESS_BITS'(COUNT);
        end
    end endgenerate
    wire write_accepted=pending_write && in_range[0];
    (* ram_style="block" *) logic [WIDTH-1:0] words[0:COUNT-1];
    logic [COUNT-1:0] valid;
    logic [31:0] index_a,index_b;
    logic [WIDTH-1:0] word_a,word_b;
    logic valid_a,valid_b;
    always_ff @(negedge clk) begin
        word_a<=words[ADDRESS_BITS'(read_index_a)];
        word_b<=words[ADDRESS_BITS'(read_index_b)];
        index_a<=read_index_a; index_b<=read_index_b;
        valid_a<=in_range[1] && valid[ADDRESS_BITS'(read_index_a)];
        valid_b<=in_range[2] && valid[ADDRESS_BITS'(read_index_b)];
    end
    assign read_data_a=write_accepted && write_index==index_a ? write_data : valid_a ? word_a : {WIDTH{1'b0}};
    assign read_data_b=write_accepted && write_index==index_b ? write_data : valid_b ? word_b : {WIDTH{1'b0}};
    genvar row;
    generate for(row=0;row<COUNT;row=row+1) begin: validity
        always_ff @(posedge clk) begin
            if(reset) valid[row]<=0;
            else if(write_accepted && write_index[ADDRESS_BITS-1:0]==ADDRESS_BITS'(row)) valid[row]<=1;
        end
    end endgenerate
    always_ff @(posedge clk)
        if(!reset && write_accepted) words[ADDRESS_BITS'(write_index)]<=write_data;
endmodule
