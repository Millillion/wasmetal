// SPDX-License-Identifier: MIT
module wasmetal_simd_lanes #(parameter integer W=8) (
    input logic [5:0] operation,
    input logic [127:0] a,b,
    input logic [5:0] shift,
    output logic [127:0] result,
    output logic all_true,
    output logic [15:0] bitmask
);
    logic [128/W-1:0] nonzero;
    genvar g;
    generate for (g=0; g<128/W; g=g+1) begin : lanes
        wire [W-1:0] x=a[g*W+:W], y=b[g*W+:W];
        logic [W-1:0] r;
        logic signed [W:0] sx, sy, sum_s, diff_s;
        logic [W:0] sum_u;
        logic signed [2*W-1:0] product;
        integer k;
        always_comb begin
            k=0;
            sx=$signed({x[W-1],x}); sy=$signed({y[W-1],y});
            sum_s=sx+sy; diff_s=sx-sy; sum_u={1'b0,x}+{1'b0,y};
            product=$signed(x)*$signed(y); r=0;
            case(operation)
                0: r=x[W-1] ? -x : x;
                1: r=-x;
                2: for(k=0;k<W;k=k+1) r=r+{{(W-1){1'b0}},x[k]};
                3: r=x+y;
                4: r=x-y;
                5: r=x*y;
                6: r=$signed(x)<$signed(y) ? x:y;
                7: r=x<y ? x:y;
                8: r=$signed(x)>$signed(y) ? x:y;
                9: r=x>y ? x:y;
                10: r=W'((sum_u+1'b1)>>1);
                11: begin
                    if(sum_s>$signed({2'b00,{(W-1){1'b1}}})) r={1'b0,{(W-1){1'b1}}};
                    else if(sum_s<$signed({2'b11,{(W-1){1'b0}}})) r={1'b1,{(W-1){1'b0}}};
                    else r=sum_s[W-1:0];
                end
                12: r=sum_u[W] ? {W{1'b1}} : sum_u[W-1:0];
                13: begin
                    if(diff_s>$signed({2'b00,{(W-1){1'b1}}})) r={1'b0,{(W-1){1'b1}}};
                    else if(diff_s<$signed({2'b11,{(W-1){1'b0}}})) r={1'b1,{(W-1){1'b0}}};
                    else r=diff_s[W-1:0];
                end
                14: r=x<y ? {W{1'b0}} : x-y;
                15: r=x << (shift & 6'(W-1));
                16: r=$signed(x) >>> (shift & 6'(W-1));
                17: r=x >> (shift & 6'(W-1));
                18: r={W{x==y}};
                19: r={W{x!=y}};
                20: r={W{$signed(x)<$signed(y)}};
                21: r={W{x<y}};
                22: r={W{$signed(x)>$signed(y)}};
                23: r={W{x>y}};
                24: r={W{$signed(x)<=$signed(y)}};
                25: r={W{x<=y}};
                26: r={W{$signed(x)>=$signed(y)}};
                27: r={W{x>=y}};
                28: if(W==16) r=(x==W'(16'h8000) && y==W'(16'h8000)) ? W'(16'h7fff) : W'((product+(2*W)'(16384))>>>15);
                default: r=0;
            endcase
        end
        assign result[g*W+:W]=r;
        assign nonzero[g]=|x;
    end endgenerate
    integer j;
    always_comb begin
        all_true=&nonzero; bitmask=0;
        for(j=0;j<128/W;j=j+1) bitmask[j]=a[j*W+W-1];
    end
endmodule
