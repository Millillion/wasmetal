// SPDX-License-Identifier: MIT
// Compare the shared sequential datapath with the independently structured
// parallel implementation, including sign, saturation, lane and shuffle edges.
module simd_serial_tb;
    reg clk=0,reset=1,start=0;
    reg [31:0] op=0,lane=0;
    reg [127:0] immediate=0,a=0,b=0,c=0;
    wire supported,reference_supported,done;
    wire [2:0] arity,reference_arity;
    wire [127:0] result,reference_result;
    wasmetal_simd_serial dut(clk,reset,start,op,lane,immediate,a,b,c,supported,arity,done,result);
    wasmetal_simd_int reference_unit(op,lane,immediate,a,b,c,reference_supported,reference_arity,reference_result);
    always #5 clk=~clk;
    integer opcode,sample,n,cycles,checks=0,seed=32'h574d2026;
    task automatic execute_case;
        reg [127:0] expected;
        begin
            #1; expected=reference_result;
            if(supported!==reference_supported || arity!==reference_arity) $fatal(1,"decode mismatch");
            @(negedge clk);start=1;@(negedge clk);start=0;
            cycles=0;
            while(!done && cycles<20) begin @(negedge clk);cycles=cycles+1;end
            if(!done || result!==expected)
                $fatal(1,"SIMD op=%h lane=%d a=%h b=%h c=%h result=%h expected=%h",op,lane,a,b,c,result,expected);
            checks=checks+1;
            @(negedge clk);if(done) $fatal(1,"done did not pulse");
        end
    endtask
    initial begin
        repeat(2) @(negedge clk);reset=0;
        for(opcode=0;opcode<'h114;opcode=opcode+1) begin
            op='hfd0000+opcode;#1;
            if(reference_supported) begin
                for(sample=0;sample<40;sample=sample+1) begin
                    a={$random(seed),$random(seed),$random(seed),$random(seed)};
                    b={$random(seed),$random(seed),$random(seed),$random(seed)};
                    c={$random(seed),$random(seed),$random(seed),$random(seed)};
                    if(sample==0) begin a=0;b=0;c=0;end
                    if(sample==1) begin a='1;b='1;c='1;end
                    if(sample==2) begin a={8{16'h8000}};b=a;c=a;end
                    if(sample==3) begin a={4{32'h7fffffff}};b={4{32'h80000000}};end
                    if(sample==4) begin a={16{8'h80}};b={16{8'h7f}};end
                    if(sample==5) begin a={2{64'h8000000000000000}};b={2{64'hffffffffffffffff}};end
                    lane=sample%16;
                    if(opcode=='h18 || opcode=='h19 || opcode=='h1a) lane=sample%8;
                    if(opcode=='h1b || opcode=='h1c || opcode=='h1f || opcode=='h20) lane=sample%4;
                    if(opcode=='h1d || opcode=='h1e || opcode=='h21 || opcode=='h22) lane=sample%2;
                    for(n=0;n<16;n=n+1) immediate[n*8+:8]=8'($random(seed)&31);
                    execute_case();
                end
            end
        end
        op='hfd00d5;a='1;b=7;
        @(negedge clk);start=1;@(negedge clk);start=0;
        repeat(3) @(negedge clk);reset=1;
        @(negedge clk);reset=0;
        repeat(20) begin @(negedge clk);if(done) $fatal(1,"reset did not cancel");end
        execute_case();
        $display("PASS %0d SIMD differential cases and reset cancellation",checks);
        $finish;
    end
endmodule
