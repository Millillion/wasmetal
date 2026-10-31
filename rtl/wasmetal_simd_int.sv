// SPDX-License-Identifier: MIT
module wasmetal_simd_int (
    input logic [31:0] op,
    input logic [31:0] lane,
    input logic [127:0] immediate, a, b, c,
    output logic supported,
    output logic [2:0] arity,
    output logic [127:0] result
);
    logic [1:0] width_code;
    logic [5:0] operation;
    logic lane_operation;
    wire [127:0] r8,r16,r32,r64;
    wire all8,all16,all32,all64;
    wire [15:0] mask8,mask16,mask32,mask64;
    wire [15:0] subop=op[15:0];
    wasmetal_simd_lanes #(8) lanes8(operation,a,b,b[5:0],r8,all8,mask8);
    wasmetal_simd_lanes #(16) lanes16(operation,a,b,b[5:0],r16,all16,mask16);
    wasmetal_simd_lanes #(32) lanes32(operation,a,b,b[5:0],r32,all32,mask32);
    wasmetal_simd_lanes #(64) lanes64(operation,a,b,b[5:0],r64,all64,mask64);
    function automatic [63:0] narrow(input logic signed [63:0] v,input integer width,input logic unsigned_out);
        logic signed [63:0] lower_bound, upper_bound;
        begin
            lower_bound=unsigned_out ? 0 : -(64'sd1 << (width-1));
            upper_bound=(64'sd1 << (unsigned_out ? width : width-1))-1;
            if(v<lower_bound) narrow=lower_bound;
            else if(v>upper_bound) narrow=upper_bound;
            else narrow=v;
        end
    endfunction
    always_comb begin
        supported=op[31:16]=='hfd; arity=2; width_code=0; operation=0; lane_operation=0;
        case(subop)
            'h60: begin width_code=2'd0; operation=6'd0; arity=3'd1; lane_operation=1; end
            'h61: begin width_code=2'd0; operation=6'd1; arity=3'd1; lane_operation=1; end
            'h62: begin width_code=2'd0; operation=6'd2; arity=3'd1; lane_operation=1; end
            'h6b: begin width_code=2'd0; operation=6'd15; arity=3'd2; lane_operation=1; end
            'h6c: begin width_code=2'd0; operation=6'd16; arity=3'd2; lane_operation=1; end
            'h6d: begin width_code=2'd0; operation=6'd17; arity=3'd2; lane_operation=1; end
            'h6e: begin width_code=2'd0; operation=6'd3; arity=3'd2; lane_operation=1; end
            'h71: begin width_code=2'd0; operation=6'd4; arity=3'd2; lane_operation=1; end
            'h6f: begin width_code=2'd0; operation=6'd11; arity=3'd2; lane_operation=1; end
            'h70: begin width_code=2'd0; operation=6'd12; arity=3'd2; lane_operation=1; end
            'h72: begin width_code=2'd0; operation=6'd13; arity=3'd2; lane_operation=1; end
            'h73: begin width_code=2'd0; operation=6'd14; arity=3'd2; lane_operation=1; end
            'h7b: begin width_code=2'd0; operation=6'd10; arity=3'd2; lane_operation=1; end
            'h76: begin width_code=2'd0; operation=6'd6; arity=3'd2; lane_operation=1; end
            'h77: begin width_code=2'd0; operation=6'd7; arity=3'd2; lane_operation=1; end
            'h78: begin width_code=2'd0; operation=6'd8; arity=3'd2; lane_operation=1; end
            'h79: begin width_code=2'd0; operation=6'd9; arity=3'd2; lane_operation=1; end
            'h80: begin width_code=2'd1; operation=6'd0; arity=3'd1; lane_operation=1; end
            'h81: begin width_code=2'd1; operation=6'd1; arity=3'd1; lane_operation=1; end
            'h8b: begin width_code=2'd1; operation=6'd15; arity=3'd2; lane_operation=1; end
            'h8c: begin width_code=2'd1; operation=6'd16; arity=3'd2; lane_operation=1; end
            'h8d: begin width_code=2'd1; operation=6'd17; arity=3'd2; lane_operation=1; end
            'h8e: begin width_code=2'd1; operation=6'd3; arity=3'd2; lane_operation=1; end
            'h91: begin width_code=2'd1; operation=6'd4; arity=3'd2; lane_operation=1; end
            'h95: begin width_code=2'd1; operation=6'd5; arity=3'd2; lane_operation=1; end
            'h8f: begin width_code=2'd1; operation=6'd11; arity=3'd2; lane_operation=1; end
            'h90: begin width_code=2'd1; operation=6'd12; arity=3'd2; lane_operation=1; end
            'h92: begin width_code=2'd1; operation=6'd13; arity=3'd2; lane_operation=1; end
            'h93: begin width_code=2'd1; operation=6'd14; arity=3'd2; lane_operation=1; end
            'h9b: begin width_code=2'd1; operation=6'd10; arity=3'd2; lane_operation=1; end
            'h96: begin width_code=2'd1; operation=6'd6; arity=3'd2; lane_operation=1; end
            'h97: begin width_code=2'd1; operation=6'd7; arity=3'd2; lane_operation=1; end
            'h98: begin width_code=2'd1; operation=6'd8; arity=3'd2; lane_operation=1; end
            'h99: begin width_code=2'd1; operation=6'd9; arity=3'd2; lane_operation=1; end
            'ha0: begin width_code=2'd2; operation=6'd0; arity=3'd1; lane_operation=1; end
            'ha1: begin width_code=2'd2; operation=6'd1; arity=3'd1; lane_operation=1; end
            'hab: begin width_code=2'd2; operation=6'd15; arity=3'd2; lane_operation=1; end
            'hac: begin width_code=2'd2; operation=6'd16; arity=3'd2; lane_operation=1; end
            'had: begin width_code=2'd2; operation=6'd17; arity=3'd2; lane_operation=1; end
            'hae: begin width_code=2'd2; operation=6'd3; arity=3'd2; lane_operation=1; end
            'hb1: begin width_code=2'd2; operation=6'd4; arity=3'd2; lane_operation=1; end
            'hb5: begin width_code=2'd2; operation=6'd5; arity=3'd2; lane_operation=1; end
            'hb6: begin width_code=2'd2; operation=6'd6; arity=3'd2; lane_operation=1; end
            'hb7: begin width_code=2'd2; operation=6'd7; arity=3'd2; lane_operation=1; end
            'hb8: begin width_code=2'd2; operation=6'd8; arity=3'd2; lane_operation=1; end
            'hb9: begin width_code=2'd2; operation=6'd9; arity=3'd2; lane_operation=1; end
            'hc0: begin width_code=2'd3; operation=6'd0; arity=3'd1; lane_operation=1; end
            'hc1: begin width_code=2'd3; operation=6'd1; arity=3'd1; lane_operation=1; end
            'hcb: begin width_code=2'd3; operation=6'd15; arity=3'd2; lane_operation=1; end
            'hcc: begin width_code=2'd3; operation=6'd16; arity=3'd2; lane_operation=1; end
            'hcd: begin width_code=2'd3; operation=6'd17; arity=3'd2; lane_operation=1; end
            'hce: begin width_code=2'd3; operation=6'd3; arity=3'd2; lane_operation=1; end
            'hd1: begin width_code=2'd3; operation=6'd4; arity=3'd2; lane_operation=1; end
            'hd5: begin width_code=2'd3; operation=6'd5; arity=3'd2; lane_operation=1; end
            'h23: begin width_code=2'd0; operation=6'd18; arity=3'd2; lane_operation=1; end
            'h24: begin width_code=2'd0; operation=6'd19; arity=3'd2; lane_operation=1; end
            'h25: begin width_code=2'd0; operation=6'd20; arity=3'd2; lane_operation=1; end
            'h26: begin width_code=2'd0; operation=6'd21; arity=3'd2; lane_operation=1; end
            'h27: begin width_code=2'd0; operation=6'd22; arity=3'd2; lane_operation=1; end
            'h28: begin width_code=2'd0; operation=6'd23; arity=3'd2; lane_operation=1; end
            'h29: begin width_code=2'd0; operation=6'd24; arity=3'd2; lane_operation=1; end
            'h2a: begin width_code=2'd0; operation=6'd25; arity=3'd2; lane_operation=1; end
            'h2b: begin width_code=2'd0; operation=6'd26; arity=3'd2; lane_operation=1; end
            'h2c: begin width_code=2'd0; operation=6'd27; arity=3'd2; lane_operation=1; end
            'h2d: begin width_code=2'd1; operation=6'd18; arity=3'd2; lane_operation=1; end
            'h2e: begin width_code=2'd1; operation=6'd19; arity=3'd2; lane_operation=1; end
            'h2f: begin width_code=2'd1; operation=6'd20; arity=3'd2; lane_operation=1; end
            'h30: begin width_code=2'd1; operation=6'd21; arity=3'd2; lane_operation=1; end
            'h31: begin width_code=2'd1; operation=6'd22; arity=3'd2; lane_operation=1; end
            'h32: begin width_code=2'd1; operation=6'd23; arity=3'd2; lane_operation=1; end
            'h33: begin width_code=2'd1; operation=6'd24; arity=3'd2; lane_operation=1; end
            'h34: begin width_code=2'd1; operation=6'd25; arity=3'd2; lane_operation=1; end
            'h35: begin width_code=2'd1; operation=6'd26; arity=3'd2; lane_operation=1; end
            'h36: begin width_code=2'd1; operation=6'd27; arity=3'd2; lane_operation=1; end
            'h37: begin width_code=2'd2; operation=6'd18; arity=3'd2; lane_operation=1; end
            'h38: begin width_code=2'd2; operation=6'd19; arity=3'd2; lane_operation=1; end
            'h39: begin width_code=2'd2; operation=6'd20; arity=3'd2; lane_operation=1; end
            'h3a: begin width_code=2'd2; operation=6'd21; arity=3'd2; lane_operation=1; end
            'h3b: begin width_code=2'd2; operation=6'd22; arity=3'd2; lane_operation=1; end
            'h3c: begin width_code=2'd2; operation=6'd23; arity=3'd2; lane_operation=1; end
            'h3d: begin width_code=2'd2; operation=6'd24; arity=3'd2; lane_operation=1; end
            'h3e: begin width_code=2'd2; operation=6'd25; arity=3'd2; lane_operation=1; end
            'h3f: begin width_code=2'd2; operation=6'd26; arity=3'd2; lane_operation=1; end
            'h40: begin width_code=2'd2; operation=6'd27; arity=3'd2; lane_operation=1; end
            'hd6: begin width_code=2'd3; operation=6'd18; arity=3'd2; lane_operation=1; end
            'hd7: begin width_code=2'd3; operation=6'd19; arity=3'd2; lane_operation=1; end
            'hd8: begin width_code=2'd3; operation=6'd20; arity=3'd2; lane_operation=1; end
            'hd9: begin width_code=2'd3; operation=6'd22; arity=3'd2; lane_operation=1; end
            'hda: begin width_code=2'd3; operation=6'd24; arity=3'd2; lane_operation=1; end
            'hdb: begin width_code=2'd3; operation=6'd26; arity=3'd2; lane_operation=1; end
            'h82: begin width_code=2'd1; operation=6'd28; arity=3'd2; lane_operation=1; end
            'h111: begin width_code=2'd1; operation=6'd28; arity=3'd2; lane_operation=1; end
            'h0f,'h10,'h11,'h12,'h13,'h14,
            'h15,'h16,'h18,'h19,'h1b,'h1d,'h1f,'h21,
            'h4d,'h53,'h63,'h64,'h83,'h84,'ha3,'ha4,'hc3,'hc4,
            'h7c,'h7d,'h7e,'h7f,
            'h87,'h88,'h89,'h8a,'ha7,'ha8,'ha9,'haa,'hc7,'hc8,'hc9,'hca: arity=1;
            'h52,'h109,'h10a,'h10b,'h10c,'h113: arity=3;
            'h0d,'h0e,'h100,'h17,'h1a,'h1c,'h1e,'h20,'h22,'h4e,'h4f,'h50,'h51,
            'h65,'h66,'h85,'h86,'h9c,'h9d,'h9e,'h9f,'hbc,'hbd,'hbe,'hbf,
            'hdc,'hdd,'hde,'hdf,'hba,'h112: arity=2;
            default: supported=0;
        endcase
        if(op[31:16]!='hfd) supported=0;
    end
    integer j, index_a, index_b;
    logic [255:0] joined;
    logic [127:0] shifted;
    always_comb begin
        result=0; joined={b,a}; shifted=0; index_a=0; index_b=0; j=0;
        if(lane_operation) begin
            case(width_code)
                0: result=r8; 1: result=r16; 2: result=r32; 3: result=r64;
            endcase
        end else case(subop)
            'h0d: for(j=0;j<16;j=j+1) result[j*8+:8]=joined[immediate[j*8+:8]*8+:8];
            'h0e,'h100: for(j=0;j<16;j=j+1) result[j*8+:8]=b[j*8+:8]<16 ? a[b[j*8+:8]*8+:8] : 8'b0;
            'h0f: result={16{a[7:0]}};
            'h10: result={8{a[15:0]}};
            'h11,'h13: result={4{a[31:0]}};
            'h12,'h14: result={2{a[63:0]}};
            'h15: begin shifted=a>>(lane*8); result={96'b0,{24{shifted[7]}},shifted[7:0]}; end
            'h16: begin shifted=a>>(lane*8); result={120'b0,shifted[7:0]}; end
            'h18: begin shifted=a>>(lane*16); result={96'b0,{16{shifted[15]}},shifted[15:0]}; end
            'h19: begin shifted=a>>(lane*16); result={112'b0,shifted[15:0]}; end
            'h1b,'h1f: begin shifted=a>>(lane*32); result={96'b0,shifted[31:0]}; end
            'h1d,'h21: begin shifted=a>>(lane*64); result={64'b0,shifted[63:0]}; end
            'h17: begin result=a; result[lane*8+:8]=b[7:0]; end
            'h1a: begin result=a; result[lane*16+:16]=b[15:0]; end
            'h1c,'h20: begin result=a; result[lane*32+:32]=b[31:0]; end
            'h1e,'h22: begin result=a; result[lane*64+:64]=b[63:0]; end
            'h4d: result=~a;
            'h4e: result=a&b;
            'h4f: result=a&~b;
            'h50: result=a|b;
            'h51: result=a^b;
            'h52,'h109,'h10a,'h10b,'h10c: result=(a&c)|(b&~c);
            'h53: result={127'b0,|a};
            'h63: result={127'b0,all8};
            'h83: result={127'b0,all16};
            'ha3: result={127'b0,all32};
            'hc3: result={127'b0,all64};
            'h64: result={112'b0,mask8};
            'h84: result={112'b0,mask16};
            'ha4: result={112'b0,mask32};
            'hc4: result={112'b0,mask64};
            'h65,'h66: for(j=0;j<8;j=j+1) begin
                result[j*8+:8]=8'(narrow({{48{a[j*16+15]}},a[j*16+:16]},8,subop=='h66));
                result[(j+8)*8+:8]=8'(narrow({{48{b[j*16+15]}},b[j*16+:16]},8,subop=='h66));
            end
            'h85,'h86: for(j=0;j<4;j=j+1) begin
                result[j*16+:16]=16'(narrow({{32{a[j*32+31]}},a[j*32+:32]},16,subop=='h86));
                result[(j+4)*16+:16]=16'(narrow({{32{b[j*32+31]}},b[j*32+:32]},16,subop=='h86));
            end
            'h7c,'h7d: for(j=0;j<8;j=j+1) begin
                if(subop=='h7c) result[j*16+:16]=$signed({{8{a[j*16+7]}},a[j*16+:8]})+$signed({{8{a[j*16+15]}},a[j*16+8+:8]});
                else result[j*16+:16]={8'b0,a[j*16+:8]}+{8'b0,a[j*16+8+:8]};
            end
            'h7e,'h7f: for(j=0;j<4;j=j+1) begin
                if(subop=='h7e) result[j*32+:32]=$signed({{16{a[j*32+15]}},a[j*32+:16]})+$signed({{16{a[j*32+31]}},a[j*32+16+:16]});
                else result[j*32+:32]={16'b0,a[j*32+:16]}+{16'b0,a[j*32+16+:16]};
            end
            'h87,'h88,'h89,'h8a: for(j=0;j<8;j=j+1) begin
                index_a=j+(subop=='h88 || subop=='h8a ? 8 : 0);
                result[j*16+:16]={{8{(subop=='h87 || subop=='h88) && a[index_a*8+7]}},a[index_a*8+:8]};
            end
            'ha7,'ha8,'ha9,'haa: for(j=0;j<4;j=j+1) begin
                index_a=j+(subop=='ha8 || subop=='haa ? 4 : 0);
                result[j*32+:32]={{16{(subop=='ha7 || subop=='ha8) && a[index_a*16+15]}},a[index_a*16+:16]};
            end
            'hc7,'hc8,'hc9,'hca: for(j=0;j<2;j=j+1) begin
                index_a=j+(subop=='hc8 || subop=='hca ? 2 : 0);
                result[j*64+:64]={{32{(subop=='hc7 || subop=='hc8) && a[index_a*32+31]}},a[index_a*32+:32]};
            end
            'h9c,'h9d,'h9e,'h9f: for(j=0;j<8;j=j+1) begin
                index_a=j+(subop[0] ? 8 : 0);
                if(!subop[1]) result[j*16+:16]=$signed(a[index_a*8+:8])*$signed(b[index_a*8+:8]);
                else result[j*16+:16]=a[index_a*8+:8]*b[index_a*8+:8];
            end
            'hbc,'hbd,'hbe,'hbf: for(j=0;j<4;j=j+1) begin
                index_a=j+(subop[0] ? 4 : 0);
                if(!subop[1]) result[j*32+:32]=$signed(a[index_a*16+:16])*$signed(b[index_a*16+:16]);
                else result[j*32+:32]=a[index_a*16+:16]*b[index_a*16+:16];
            end
            'hdc,'hdd,'hde,'hdf: for(j=0;j<2;j=j+1) begin
                index_a=j+(subop[0] ? 2 : 0);
                if(!subop[1]) result[j*64+:64]=$signed(a[index_a*32+:32])*$signed(b[index_a*32+:32]);
                else result[j*64+:64]=a[index_a*32+:32]*b[index_a*32+:32];
            end
            'hba: for(j=0;j<4;j=j+1) result[j*32+:32]=
                $signed(a[j*32+:16])*$signed(b[j*32+:16])+
                $signed(a[j*32+16+:16])*$signed(b[j*32+16+:16]);
            'h112: for(j=0;j<8;j=j+1) result[j*16+:16]=
                $signed(a[j*16+:8])*$signed(b[j*16+:8])+
                $signed(a[j*16+8+:8])*$signed(b[j*16+8+:8]);
            'h113: for(j=0;j<4;j=j+1) result[j*32+:32]=c[j*32+:32]+
                $signed(a[j*32+:8])*$signed(b[j*32+:8])+
                $signed(a[j*32+8+:8])*$signed(b[j*32+8+:8])+
                $signed(a[j*32+16+:8])*$signed(b[j*32+16+:8])+
                $signed(a[j*32+24+:8])*$signed(b[j*32+24+:8]);
            default: result=0;
        endcase
    end
endmodule
