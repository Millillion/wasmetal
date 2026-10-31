// SPDX-License-Identifier: MIT
// Independent four-state simulation against SystemVerilog division semantics.
module divider_tb;
    logic clk=0, reset=1, start=0, wide=0, signed_op=0, remainder_op=0;
    logic [63:0] a=0, b=0;
    wire done;
    wire [63:0] result;
    wire [7:0] trap;
    integer checks=0;
    logic [31:0] rng=32'h5a17c039;
    wasmetal_divider dut(.*);

    function automatic [31:0] random_word();
        rng=rng^(rng<<13); rng=rng^(rng>>17); rng=rng^(rng<<5);
        random_word=rng;
    endfunction

    task automatic tick();
        clk=0; #5; clk=1; #5;
    endtask

    task automatic check(input logic w, s, r, input logic [63:0] x, y);
        logic [63:0] nx, ny, expected;
        logic signed [63:0] sx, sy;
        logic [7:0] expected_trap;
        integer cycles;
        nx=w?x:{32'b0,x[31:0]}; ny=w?y:{32'b0,y[31:0]};
        sx=w?$signed(x):$signed({{32{x[31]}},x[31:0]});
        sy=w?$signed(y):$signed({{32{y[31]}},y[31:0]});
        expected=0; expected_trap=0;
        if(ny==0) expected_trap=2;
        else if(s && sy==-1 && sx==(w ? 64'sh8000000000000000 : -64'sd2147483648)) begin
            if(!r) expected_trap=3;
        end else if(s) expected=r ? sx%sy : sx/sy;
        else expected=r ? nx%ny : nx/ny;
        if(!w) expected[63:32]=0;
        a=x; b=y; wide=w; signed_op=s; remainder_op=r; start=1;
        tick(); start=0;
        // Operand/control changes while busy must not change the latched operation.
        a=~x; b=~y; wide=~w; signed_op=~s; remainder_op=~r;
        cycles=0;
        while(!done && cycles<66) begin tick(); cycles=cycles+1; end
        if(done!==1'b1 || trap!==expected_trap || (expected_trap==0 && result!==expected))
            $fatal(1,"divide mismatch w=%b s=%b r=%b a=%h b=%h got=%h trap=%d expected=%h trap=%d",w,s,r,x,y,result,trap,expected,expected_trap);
        checks=checks+1;
    endtask

    integer w,s,r,n;
    initial begin
        tick(); reset=0;
        for(w=0;w<2;w=w+1) for(s=0;s<2;s=s+1) for(r=0;r<2;r=r+1) begin
            check(w[0],s[0],r[0],0,0);
            check(w[0],s[0],r[0],64'h8000000000000000,64'hffffffffffffffff);
            check(w[0],s[0],r[0],64'h80000000,64'hffffffff);
            check(w[0],s[0],r[0],64'hffffffffffffffff,1);
            check(w[0],s[0],r[0],1,64'hffffffffffffffff);
            for(n=0;n<500;n=n+1)
                check(w[0],s[0],r[0],{random_word(),random_word()},{random_word(),random_word()});
        end
        a=64'h8765432101234567; b=3; wide=1; start=1; tick(); start=0;
        repeat(7) tick(); reset=1; tick(); reset=0;
        repeat(70) begin tick(); if(done!==0) $fatal(1,"completion leaked across reset"); end
        check(1,0,0,99,3);
        $display("PASS %0d divider cases, operand latching and reset cancellation",checks);
        $finish;
    end
endmodule
