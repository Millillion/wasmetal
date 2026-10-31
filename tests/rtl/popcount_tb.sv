// SPDX-License-Identifier: MIT
module popcount_tb;
    reg [63:0] value;
    wire [3:0] count8;
    wire [4:0] count16;
    wire [5:0] count32;
    wire [6:0] count64;
    reg [95:0] cases[0:99999];
    integer count,n;
    wasmetal_popcount #(8) p8(value[7:0],count8);
    wasmetal_popcount #(16) p16(value[15:0],count16);
    wasmetal_popcount #(32) p32(value[31:0],count32);
    wasmetal_popcount #(64) p64(value,count64);
    initial begin
        if(!$value$plusargs("COUNT=%d",count) || count>100000) $fatal(1,"invalid vector count");
        $readmemh("build/unit/popcount.hex",cases,0,count-1);
        for(n=0;n<count;n=n+1) begin
            value=cases[n][63:0];#1;
            if({8'(count64),8'(count32),8'(count16),8'(count8)}!==cases[n][95:64])
                $fatal(1,"popcount mismatch at input %h",value);
        end
        $display("PASS %0d population-count vectors at four widths",count);
        $finish;
    end
endmodule
