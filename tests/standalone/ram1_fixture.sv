// SPDX-License-Identifier: MIT
// Keep the previously used one-bit EBR mode under test after the wide-memory
// replacement. This fixture is synthesized by the pinned tool, not hand-mapped.
module wasmetal_ram1_fixture (
    input wire clk, write, data,
    input wire [13:0] address,
    output logic result
);
    (* ram_style="block" *) logic storage [0:16383];
    initial for(integer i=0;i<16384;i=i+1) storage[i]=0;
    always_ff @(posedge clk) begin
        result<=storage[address];
        if(write) storage[address]<=data;
    end
endmodule
