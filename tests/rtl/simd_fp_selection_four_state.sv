`timescale 1ns/1ps
module simd_fp_selection_four_state;
    reg [127:0] top=0,below=0,third=0,simd_accum=0;
    reg [63:0] fp_result=0;
    reg [2:0] simd_lane=0,simd_arity=1,simd_mode=0;
    reg simd_source_wide=0,simd_result_wide=0;
    wire [63:0] simd_a_lane,simd_b_lane,simd_c_lane,simd_result_lane;
    wire [127:0] simd_assembled;
    reg [3:0] controls;
    reg [127:0] operands [0:2];
    reg [63:0] observed [0:2];
    reg [63:0] possible_ones [0:2];
    reg [63:0] possible_zeros [0:2];
    reg [63:0] binary_value;
    integer seed=1234567,compatible,choices,checks=0;
    simd_fp_selection_candidate dut(.*);
    initial begin
        for(integer sample=0;sample<16;sample=sample+1) begin
            if(sample==0)begin top=0;below=~128'b0;third=128'h123456789abcdef0;end
            else if(sample==1)begin top=~128'b0;below=0;third=~128'h123456789abcdef0;end
            else if(sample==2)begin top='x;below='x;third='x;end
            else if(sample==3)begin top='z;below='z;third='z;end
            else if(sample==4)begin
                top={32'bx,32'h12345678,32'bz,32'h87654321};
                below={32'hfedcba98,32'bz,32'h76543210,32'bx};
                third={32'bz,32'bx,32'h01234567,32'h89abcdef};
            end
            else for(integer word=0;word<4;word=word+1)begin
                top[word*32+:32]=$urandom(seed);
                below[word*32+:32]=$urandom(seed);
                third[word*32+:32]=$urandom(seed);
            end
            for(integer arity=1;arity<=3;arity=arity+1)begin
                simd_arity=3'(arity);
                operands[0]=arity==1 ? top : arity==2 ? below : third;
                operands[1]=arity==3 ? below : top;
                operands[2]=top;
                for(integer pattern=0;pattern<256;pattern=pattern+1)begin
                    for(integer b=0;b<4;b=b+1)begin
                        case((pattern>>(b*2))&3)
                            0:controls[b]=0;
                            1:controls[b]=1;
                            2:controls[b]=1'bx;
                            3:controls[b]=1'bz;
                        endcase
                    end
                    simd_source_wide=controls[3];simd_lane=controls[2:0];#1;
                    observed[0]=simd_a_lane;observed[1]=simd_b_lane;observed[2]=simd_c_lane;
                    for(integer operand=0;operand<3;operand=operand+1)begin
                        possible_ones[operand]=0;possible_zeros[operand]=0;
                    end
                    choices=0;
                    // Every compatible binary assignment is an independent oracle.
                    for(integer selector=0;selector<16;selector=selector+1)begin
                        compatible=1;
                        for(integer b=0;b<4;b=b+1)
                            if((controls[b]===1'b0 || controls[b]===1'b1) && controls[b]!==((selector>>b)&1))
                                compatible=0;
                        if(compatible!=0)begin
                            choices=choices+1;
                            for(integer operand=0;operand<3;operand=operand+1)begin
                                binary_value=64'(operands[operand] >> ((selector&7)*((selector&8)!=0 ? 64 : 32)));
                                if((selector&8)==0)binary_value[63:32]=0;
                                // X/Z source bits admit both binary values.
                                for(integer b=0;b<64;b=b+1)begin
                                    if(binary_value[b]!==1'b0)possible_ones[operand][b]=1;
                                    if(binary_value[b]!==1'b1)possible_zeros[operand][b]=1;
                                end
                            end
                        end
                    end
                    if(choices==0)$fatal(1,"missing compatible binary selector");
                    for(integer operand=0;operand<3;operand=operand+1)
                        for(integer b=0;b<64;b=b+1)
                            if((observed[operand][b]===1'b0 && possible_ones[operand][b]) ||
                               (observed[operand][b]===1'b1 && possible_zeros[operand][b]))
                                $fatal(1,"selector asserted an unjustified known bit: controls=%b operand=%0d bit=%0d",controls,operand,b);
                    checks=checks+1;
                end
            end
        end
        $display("PASS %0d four-state selector patterns",checks);$finish;
    end
endmodule
