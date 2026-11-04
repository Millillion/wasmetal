// SPDX-License-Identifier: MIT
// Balanced, minimally sized sums. W must be a power of two.
module wasmetal_popcount #(parameter integer W=64) (
    input logic [W-1:0] bits_in,
    output wire [$clog2(W):0] count
);
    genvar level, item;
    generate for(level=0;level<=$clog2(W);level=level+1) begin : levels
        wire [level:0] sums [0:(W>>level)-1];
        for(item=0;item<(W>>level);item=item+1) begin : items
            if(level==0) begin : leaf
                assign sums[item]=bits_in[item];
            end else begin : branch
                assign sums[item]={1'b0,levels[level-1].sums[item*2]}+
                                   {1'b0,levels[level-1].sums[item*2+1]};
            end
        end
    end endgenerate
    assign count=levels[$clog2(W)].sums[0];
endmodule
