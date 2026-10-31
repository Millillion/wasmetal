// SPDX-License-Identifier: MIT
module descriptors_tb;
    localparam integer COUNT=13,WIDTH=129;
    reg clk=0,reset=1,pending_write=0;
    reg [31:0] write_index=0,read_index_a=0,read_index_b=0;
    reg [WIDTH-1:0] write_data=0;
    wire [WIDTH-1:0] read_data_a,read_data_b;
    reg [WIDTH-1:0] reference_words[0:COUNT-1];
    reg [COUNT-1:0] reference_valid=0;
    integer step,index,checks=0,seed=32'h574d2031;
    wasmetal_descriptors #(COUNT,WIDTH) dut(clk,reset,pending_write,write_index,read_index_a,read_index_b,write_data,read_data_a,read_data_b);
    always #5 clk=~clk;
    initial begin
        for(step=0;step<20000;step=step+1) begin
            @(posedge clk);
            if(reset) reference_valid=0;
            else if(pending_write && write_index<COUNT) begin
                reference_words[write_index]=write_data;
                reference_valid[write_index]=1;
            end
            // Match the core's registered pending-write interface, including
            // reset cancellation and replacement by a different pending write.
            #1;
            reset=(step%127)==0;
            pending_write=!reset && ($random(seed)&3)!=0;
            write_index=$unsigned($random(seed))%(COUNT+2);
            write_data={$random(seed),$random(seed),$random(seed),$random(seed),1'b1};
            read_index_a=(step%3)==0 ? write_index:$unsigned($random(seed))%(COUNT+2);
            read_index_b=(step%5)==0 ? write_index:$unsigned($random(seed))%(COUNT+2);
            #1;
            @(negedge clk); #1;
            for(index=0;index<2;index=index+1) begin : check_read
                reg [31:0] selected;
                reg [WIDTH-1:0] expected;
                selected=index==0 ? read_index_a:read_index_b;
                expected=0;
                if(selected<COUNT) begin
                    if(pending_write && selected==write_index) expected=write_data;
                    else if(reference_valid[selected]) expected=reference_words[selected];
                end
                if((index==0 ? read_data_a:read_data_b)!==expected)
                    $fatal(1,"descriptor mismatch step=%0d port=%0d index=%0d",step,index,selected);
                checks=checks+1;
            end
        end
        $display("PASS %0d descriptor validity, bounds, reset and forwarding checks",checks);
        $finish;
    end
endmodule
