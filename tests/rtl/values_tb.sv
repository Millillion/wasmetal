// SPDX-License-Identifier: MIT
module values_tb;
    localparam integer DEPTH=129; // Also exercise a partially populated last bank.
    reg clk=0,pending_write=0,auxiliary=0;
    reg [31:0] write_index=0,auxiliary_index=0,window_top=0;
    reg [127:0] write_data=0;
    wire [511:0] bank_words;
    reg [127:0] reference_words[0:DEPTH-1];
    integer step,index,offset,checks=0,seed=32'h574d2030;
    wasmetal_values #(DEPTH) dut(clk,pending_write,write_index,write_data,auxiliary,auxiliary_index,window_top,bank_words);
    always #5 clk=~clk;
    initial begin
        // The core registers a pending write on an edge; forwarding exposes it
        // before the RAM commits it on the following edge.
        for(step=0;step<DEPTH+10000;step=step+1) begin
            @(posedge clk);
            pending_write<=step<DEPTH || ($random(seed)&3)!=0;
            write_index<=step<DEPTH ? step : $unsigned($random(seed))%DEPTH;
            write_data<={$random(seed),$random(seed),$random(seed),$random(seed)};
            auxiliary<=($random(seed)&1)!=0;
            auxiliary_index<=$unsigned($random(seed))%DEPTH;
            window_top<=$unsigned($random(seed))%DEPTH;
            #1;
            if(pending_write) reference_words[write_index]=write_data;
            if(step>=DEPTH) begin
                if(auxiliary) begin
                    if(bank_words[auxiliary_index[1:0]*128+:128]!==reference_words[auxiliary_index])
                        $fatal(1,"auxiliary forwarding mismatch");
                    checks=checks+1;
                end else for(offset=0;offset<4;offset=offset+1) begin
                    index=32'(window_top)-offset;
                    if(index>=0) begin
                        if(bank_words[(index%4)*128+:128]!==reference_words[index])
                            $fatal(1,"window mismatch at %0d",index);
                        checks=checks+1;
                    end
                end
            end
        end
        $display("PASS %0d banked value-store and write-forwarding checks",checks);
        $finish;
    end
endmodule
