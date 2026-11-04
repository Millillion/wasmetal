// SPDX-License-Identifier: MIT
module wasmetal_simd_decode (
    input logic [31:0] op,
    output logic supported,
    output logic [2:0] arity,
    output logic [1:0] width_code,
    output logic [5:0] operation,
    output logic lane_operation
);
    wire [15:0] subop=op[15:0];
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
endmodule
