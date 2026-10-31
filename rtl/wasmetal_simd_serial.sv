// SPDX-License-Identifier: MIT
// One output byte per cycle. A shared lane datapath implements every integer
// SIMD instruction; the parallel implementation is retained as a test oracle.
// Inputs remain stable from start until done, as required by the core's wait state.
module wasmetal_simd_serial (
    input logic clk, reset, start,
    input logic [31:0] op, lane,
    input logic [127:0] immediate, a, b, c,
    output logic supported,
    output logic [2:0] arity,
    output logic done,
    output logic [127:0] result
);
    logic [1:0] width_code;
    logic [5:0] operation;
    logic lane_operation, running;
    logic [3:0] byte_index;
    logic [127:0] accumulated;
    logic [7:0] byte_value;
    wire [15:0] subop=op[15:0];
    wasmetal_simd_decode decode(op,supported,arity,width_code,operation,lane_operation);

    function automatic [63:0] lane_mask(input [1:0] width);
        case(width)
            0: lane_mask=64'hff;
            1: lane_mask=64'hffff;
            2: lane_mask=64'hffffffff;
            3: lane_mask=64'hffffffffffffffff;
        endcase
    endfunction
    function automatic signed [63:0] sign_extend(input [63:0] value,input [1:0] width);
        case(width)
            0: sign_extend={{56{value[7]}},value[7:0]};
            1: sign_extend={{48{value[15]}},value[15:0]};
            2: sign_extend={{32{value[31]}},value[31:0]};
            3: sign_extend=value;
        endcase
    endfunction
    function automatic [63:0] slice(input [127:0] value,input integer position);
        slice=64'(value>>position);
    endfunction
    function automatic [63:0] narrow(input logic signed [63:0] value,input logic wide,input logic unsigned_out);
        logic signed [63:0] lower_bound,upper_bound;
        begin
            lower_bound=unsigned_out ? 0 : wide ? -64'sd32768 : -64'sd128;
            upper_bound=unsigned_out ? (wide ? 64'sd65535 : 64'sd255) : (wide ? 64'sd32767 : 64'sd127);
            narrow=value<lower_bound ? lower_bound : value>upper_bound ? upper_bound : value;
        end
    endfunction

    wire [15:0] nonzero8,mask8;
    wire [7:0] nonzero16,mask16;
    wire [3:0] nonzero32,mask32;
    wire [1:0] nonzero64,mask64;
    genvar g;
    generate
        for(g=0;g<16;g=g+1) begin : reductions8
            assign nonzero8[g]=|a[g*8+:8]; assign mask8[g]=a[g*8+7];
        end
        for(g=0;g<8;g=g+1) begin : reductions16
            assign nonzero16[g]=|a[g*16+:16]; assign mask16[g]=a[g*16+15];
        end
        for(g=0;g<4;g=g+1) begin : reductions32
            assign nonzero32[g]=|a[g*32+:32]; assign mask32[g]=a[g*32+31];
        end
        for(g=0;g<2;g=g+1) begin : reductions64
            assign nonzero64[g]=|a[g*64+:64]; assign mask64[g]=a[g*64+63];
        end
    endgenerate

    integer j,base,source_position,d;
    logic [63:0] mask,x,y,source_a,source_b;
    logic signed [63:0] sx,sy,multiply_a,multiply_b;
    wire signed [63:0] product=multiply_a*multiply_b;
    logic signed [16:0] dot_a[0:3],dot_b[0:3];
    wire signed [33:0] dot_product[0:3];
    logic signed [63:0] dot_accumulator;
    wire signed [63:0] dot_sum=64'(dot_product[0])+64'(dot_product[1])+64'(dot_product[2])+64'(dot_product[3])+dot_accumulator;
    generate for(g=0;g<4;g=g+1) begin : dot_multiply
        assign dot_product[g]=dot_a[g]*dot_b[g];
    end endgenerate
    wire [6:0] population;
    wasmetal_popcount #(64) pop(x,population);
    logic [5:0] shift_count;
    logic signed [64:0] sum_signed,difference_signed;
    logic [64:0] sum_unsigned;
    logic signed [63:0] upper_bound,lower_bound;
    // Explicit combinational sensitivity also works in Icarus 12, whose
    // always_comb scheduling loops on the unpacked dot-product arrays.
    always @* begin
        j=32'(byte_index); base=j&~((1<<width_code)-1); mask=lane_mask(width_code);
        x=slice(a,base*8)&mask; y=slice(b,base*8)&mask;
        sx=sign_extend(x,width_code); sy=sign_extend(y,width_code);
        multiply_a=sx; multiply_b=sy; source_a=0; source_b=0; source_position=0;
        if(subop>='h9c && subop<='h9f) begin
            source_position=(j/2+(subop[0] ? 8:0))*8;
            source_a=slice(a,source_position)&64'hff; source_b=slice(b,source_position)&64'hff;
            multiply_a=subop[1] ? $signed(source_a) : sign_extend(source_a,0);
            multiply_b=subop[1] ? $signed(source_b) : sign_extend(source_b,0);
        end else if(subop>='hbc && subop<='hbf) begin
            source_position=(j/4+(subop[0] ? 4:0))*16;
            source_a=slice(a,source_position)&64'hffff; source_b=slice(b,source_position)&64'hffff;
            multiply_a=subop[1] ? $signed(source_a) : sign_extend(source_a,1);
            multiply_b=subop[1] ? $signed(source_b) : sign_extend(source_b,1);
        end else if(subop>='hdc && subop<='hdf) begin
            source_position=(j/8+(subop[0] ? 2:0))*32;
            source_a=slice(a,source_position)&64'hffffffff; source_b=slice(b,source_position)&64'hffffffff;
            multiply_a=subop[1] ? $signed(source_a) : sign_extend(source_a,2);
            multiply_b=subop[1] ? $signed(source_b) : sign_extend(source_b,2);
        end
        dot_accumulator=0;
        for(d=0;d<4;d=d+1) begin
            dot_a[d]=0; dot_b[d]=0;
            if(subop=='hba && d<2) begin
                dot_a[d]=17'(sign_extend(slice(a,(j/4)*32+d*16),1));
                dot_b[d]=17'(sign_extend(slice(b,(j/4)*32+d*16),1));
            end else if(subop=='h112 && d<2) begin
                dot_a[d]=17'(sign_extend(slice(a,(j/2)*16+d*8),0));
                dot_b[d]=17'(sign_extend(slice(b,(j/2)*16+d*8),0));
            end else if(subop=='h113) begin
                dot_a[d]=17'(sign_extend(slice(a,(j/4)*32+d*8),0));
                dot_b[d]=17'(sign_extend(slice(b,(j/4)*32+d*8),0));
            end
        end
        if(subop=='h113) dot_accumulator=sign_extend(slice(c,(j/4)*32),2);
        shift_count=b[5:0] & (6'd7 << width_code | ((6'd1 << width_code)-1'b1));
        sum_signed={sx[63],sx}+{sy[63],sy}; difference_signed={sx[63],sx}-{sy[63],sy};
        sum_unsigned={1'b0,x}+{1'b0,y};
        upper_bound=$signed(mask>>1); lower_bound=~upper_bound;
    end

    logic [63:0] lane_result,temporary;
    logic [255:0] joined;
    integer selected,offset;
    always @* begin
        lane_result=0; temporary=0; joined={b,a}; selected=0; offset=0; byte_value=0;
        if(lane_operation) begin
            case(operation)
                0: lane_result=sx[63] ? -x:x;
                1: lane_result=-x;
                2: lane_result={57'b0,population};
                3: lane_result=x+y;
                4: lane_result=x-y;
                5: lane_result=product;
                6: lane_result=sx<sy ? x:y;
                7: lane_result=x<y ? x:y;
                8: lane_result=sx>sy ? x:y;
                9: lane_result=x>y ? x:y;
                10: lane_result=64'((sum_unsigned+1'b1)>>1);
                11: lane_result=sum_signed>$signed({upper_bound[63],upper_bound}) ? upper_bound :
                                sum_signed<$signed({lower_bound[63],lower_bound}) ? lower_bound : sum_signed[63:0];
                12: lane_result=sum_unsigned>{1'b0,mask} ? mask:sum_unsigned[63:0];
                13: lane_result=difference_signed>$signed({upper_bound[63],upper_bound}) ? upper_bound :
                                difference_signed<$signed({lower_bound[63],lower_bound}) ? lower_bound : difference_signed[63:0];
                14: lane_result=x<y ? 64'b0:x-y;
                15: lane_result=x<<shift_count;
                16: lane_result=sx>>>shift_count;
                17: lane_result=x>>shift_count;
                18: lane_result={64{x==y}};
                19: lane_result={64{x!=y}};
                20: lane_result={64{sx<sy}};
                21: lane_result={64{x<y}};
                22: lane_result={64{sx>sy}};
                23: lane_result={64{x>y}};
                24: lane_result={64{sx<=sy}};
                25: lane_result={64{x<=y}};
                26: lane_result={64{sx>=sy}};
                27: lane_result={64{x>=y}};
                28: lane_result=x==64'h8000 && y==64'h8000 ? 64'h7fff : 64'((product+64'sd16384)>>>15);
                default: lane_result=0;
            endcase
            byte_value=8'(lane_result>>((j-base)*8));
        end else case(subop)
            'h0d: byte_value=joined[immediate[j*8+:8]*8+:8];
            'h0e,'h100: byte_value=b[j*8+:8]<16 ? a[b[j*8+:8]*8+:8] : 8'b0;
            'h0f: byte_value=a[7:0];
            'h10: byte_value=a[(j&1)*8+:8];
            'h11,'h13: byte_value=a[(j&3)*8+:8];
            'h12,'h14: byte_value=a[(j&7)*8+:8];
            'h15: begin temporary={32'b0,32'(sign_extend(slice(a,32'(lane)*8),0))}; byte_value=8'(temporary>>(j*8)); end
            'h16: begin temporary=slice(a,32'(lane)*8)&64'hff; byte_value=8'(temporary>>(j*8)); end
            'h18: begin temporary={32'b0,32'(sign_extend(slice(a,32'(lane)*16),1))}; byte_value=8'(temporary>>(j*8)); end
            'h19: begin temporary=slice(a,32'(lane)*16)&64'hffff; byte_value=8'(temporary>>(j*8)); end
            'h1b,'h1f: begin temporary=slice(a,32'(lane)*32)&64'hffffffff; byte_value=8'(temporary>>(j*8)); end
            'h1d,'h21: begin temporary=slice(a,32'(lane)*64); byte_value=8'(temporary>>(j*8)); end
            'h17,'h1a,'h1c,'h1e,'h20,'h22: begin
                selected=(subop=='h17) ? 1:(subop=='h1a) ? 2:(subop=='h1c || subop=='h20) ? 4:8;
                offset=32'(lane)*selected;
                byte_value=j>=offset && j<offset+selected ? b[(j-offset)*8+:8] : a[j*8+:8];
            end
            'h4d: byte_value=~a[j*8+:8];
            'h4e: byte_value=a[j*8+:8]&b[j*8+:8];
            'h4f: byte_value=a[j*8+:8]&~b[j*8+:8];
            'h50: byte_value=a[j*8+:8]|b[j*8+:8];
            'h51: byte_value=a[j*8+:8]^b[j*8+:8];
            'h52,'h109,'h10a,'h10b,'h10c: byte_value=(a[j*8+:8]&c[j*8+:8])|(b[j*8+:8]&~c[j*8+:8]);
            'h53: byte_value=j==0 ? {7'b0,|a}:8'b0;
            'h63: byte_value=j==0 ? {7'b0,&nonzero8}:8'b0;
            'h83: byte_value=j==0 ? {7'b0,&nonzero16}:8'b0;
            'ha3: byte_value=j==0 ? {7'b0,&nonzero32}:8'b0;
            'hc3: byte_value=j==0 ? {7'b0,&nonzero64}:8'b0;
            'h64: byte_value=8'({48'b0,mask8}>>(j*8));
            'h84: byte_value=j==0 ? mask16:8'b0;
            'ha4: byte_value=j==0 ? {4'b0,mask32}:8'b0;
            'hc4: byte_value=j==0 ? {6'b0,mask64}:8'b0;
            'h65,'h66: begin
                temporary=narrow(sign_extend(slice(j<8 ? a:b,(j&7)*16),1),0,subop=='h66);
                byte_value=temporary[7:0];
            end
            'h85,'h86: begin
                temporary=narrow(sign_extend(slice(j<8 ? a:b,((j&7)/2)*32),2),1,subop=='h86);
                byte_value=8'(temporary>>((j&1)*8));
            end
            'h7c,'h7d: begin
                temporary=subop=='h7c ? sign_extend(slice(a,(j/2)*16),0)+sign_extend(slice(a,(j/2)*16+8),0) :
                    (slice(a,(j/2)*16)&64'hff)+(slice(a,(j/2)*16+8)&64'hff);
                byte_value=8'(temporary>>((j&1)*8));
            end
            'h7e,'h7f: begin
                temporary=subop=='h7e ? sign_extend(slice(a,(j/4)*32),1)+sign_extend(slice(a,(j/4)*32+16),1) :
                    (slice(a,(j/4)*32)&64'hffff)+(slice(a,(j/4)*32+16)&64'hffff);
                byte_value=8'(temporary>>((j&3)*8));
            end
            'h87,'h88,'h89,'h8a: begin
                selected=(j/2+(subop=='h88 || subop=='h8a ? 8:0))*8;
                temporary=(subop=='h87 || subop=='h88) ? sign_extend(slice(a,selected),0):slice(a,selected)&64'hff;
                byte_value=8'(temporary>>((j&1)*8));
            end
            'ha7,'ha8,'ha9,'haa: begin
                selected=(j/4+(subop=='ha8 || subop=='haa ? 4:0))*16;
                temporary=(subop=='ha7 || subop=='ha8) ? sign_extend(slice(a,selected),1):slice(a,selected)&64'hffff;
                byte_value=8'(temporary>>((j&3)*8));
            end
            'hc7,'hc8,'hc9,'hca: begin
                selected=(j/8+(subop=='hc8 || subop=='hca ? 2:0))*32;
                temporary=(subop=='hc7 || subop=='hc8) ? sign_extend(slice(a,selected),2):slice(a,selected)&64'hffffffff;
                byte_value=8'(temporary>>((j&7)*8));
            end
            'h9c,'h9d,'h9e,'h9f: byte_value=8'(product>>((j&1)*8));
            'hbc,'hbd,'hbe,'hbf: byte_value=8'(product>>((j&3)*8));
            'hdc,'hdd,'hde,'hdf: byte_value=8'(product>>((j&7)*8));
            'hba,'h113: byte_value=8'(dot_sum>>((j&3)*8));
            'h112: byte_value=8'(dot_sum>>((j&1)*8));
            default: byte_value=0;
        endcase
    end
    always_ff @(posedge clk) begin
        if(reset) begin running<=0; done<=0; byte_index<=0; accumulated<=0; result<=0; end
        else begin
            done<=0;
            if(start && !running) begin running<=1; byte_index<=0; accumulated<=0; end
            else if(running) begin
                accumulated[byte_index*8+:8]<=byte_value;
                if(byte_index==15) begin result<={byte_value,accumulated[119:0]}; done<=1; running<=0; end
                else byte_index<=byte_index+1'b1;
            end
        end
    end
`ifdef WASMETAL_ASSERTIONS
    logic [575:0] held_inputs;
    always_ff @(posedge clk) begin
        if(reset) held_inputs<=0;
        else if(start && !running) held_inputs<={op,lane,immediate,a,b,c};
        else if(running) assert({op,lane,immediate,a,b,c}==held_inputs);
        if(!reset && done) assert(!running);
    end
`endif
endmodule
