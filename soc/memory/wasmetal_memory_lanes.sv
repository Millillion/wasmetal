// SPDX-License-Identifier: MIT
// Align a <=16-byte logical transfer to one 16-byte physical beat.
module wasmetal_memory_lanes (
    input wire [4:0] position, length,
    input wire [3:0] offset,
    input wire [127:0] payload, memory_data,
    output wire [4:0] count,
    output wire [15:0] mask,
    output logic [127:0] write_data,
    output wire [127:0] read_data
);
    wire [4:0] available=5'd16-{1'b0,offset};
    assign count=(length-position)<available ? length-position : available;
    wire [127:0] shifted=(payload >> {position,3'b0}) << {offset,3'b0};
    wire [127:0] read_mask={128{1'b1}} >> {(5'd16-count),3'b0};
    assign mask=(16'hffff >> (5'd16-count)) << offset;
    assign read_data=((memory_data >> {offset,3'b0}) & read_mask) << {position,3'b0};
    always_comb begin
        write_data=0;
        for(integer lane=0;lane<16;lane=lane+1)
            if(mask[lane]) write_data[lane*8+:8]=shifted[lane*8+:8];
    end
endmodule
