// SPDX-License-Identifier: MIT
// SIMD floating point is executed one lane at a time by the scalar hardware.
module wasmetal_simd_fp_decode (
    input logic [31:0] op,
    output logic supported, source_wide, result_wide,
    output logic [31:0] scalar_op,
    output logic [2:0] lanes, arity, mode
);
    always_comb begin
        supported=op[31:16]=='hfd; source_wide=0; result_wide=0;
        scalar_op=0; lanes=0; arity=0; mode=0;
        case(op[15:0])
            'h41: begin scalar_op='h5b; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd2; mode=3'd1; end
            'h47: begin scalar_op='h61; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd2; mode=3'd1; end
            'h42: begin scalar_op='h5c; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd2; mode=3'd1; end
            'h48: begin scalar_op='h62; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd2; mode=3'd1; end
            'h43: begin scalar_op='h5d; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd2; mode=3'd1; end
            'h49: begin scalar_op='h63; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd2; mode=3'd1; end
            'h44: begin scalar_op='h5e; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd2; mode=3'd1; end
            'h4a: begin scalar_op='h64; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd2; mode=3'd1; end
            'h45: begin scalar_op='h5f; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd2; mode=3'd1; end
            'h4b: begin scalar_op='h65; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd2; mode=3'd1; end
            'h46: begin scalar_op='h60; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd2; mode=3'd1; end
            'h4c: begin scalar_op='h66; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd2; mode=3'd1; end
            'h67: begin scalar_op='h8d; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd1; mode=3'd0; end
            'h68: begin scalar_op='h8e; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd1; mode=3'd0; end
            'h69: begin scalar_op='h8f; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd1; mode=3'd0; end
            'h6a: begin scalar_op='h90; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd1; mode=3'd0; end
            'h74: begin scalar_op='h9b; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd1; mode=3'd0; end
            'h75: begin scalar_op='h9c; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd1; mode=3'd0; end
            'h7a: begin scalar_op='h9d; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd1; mode=3'd0; end
            'h94: begin scalar_op='h9e; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd1; mode=3'd0; end
            'he0: begin scalar_op='h8b; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd1; mode=3'd0; end
            'he1: begin scalar_op='h8c; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd1; mode=3'd0; end
            'he3: begin scalar_op='h91; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd1; mode=3'd0; end
            'he4: begin scalar_op='h92; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd2; mode=3'd0; end
            'he5: begin scalar_op='h93; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd2; mode=3'd0; end
            'he6: begin scalar_op='h94; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd2; mode=3'd0; end
            'he7: begin scalar_op='h95; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd2; mode=3'd0; end
            'he8: begin scalar_op='h96; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd2; mode=3'd0; end
            'he9: begin scalar_op='h97; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd2; mode=3'd0; end
            'hec: begin scalar_op='h99; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd1; mode=3'd0; end
            'hed: begin scalar_op='h9a; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd1; mode=3'd0; end
            'hef: begin scalar_op='h9f; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd1; mode=3'd0; end
            'hf0: begin scalar_op='ha0; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd2; mode=3'd0; end
            'hf1: begin scalar_op='ha1; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd2; mode=3'd0; end
            'hf2: begin scalar_op='ha2; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd2; mode=3'd0; end
            'hf3: begin scalar_op='ha3; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd2; mode=3'd0; end
            'hf4: begin scalar_op='ha4; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd2; mode=3'd0; end
            'hf5: begin scalar_op='ha5; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd2; mode=3'd0; end
            'hea: begin scalar_op='h5e; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd2; mode=3'd2; end
            'heb: begin scalar_op='h5d; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd2; mode=3'd3; end
            'hf6: begin scalar_op='h64; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd2; mode=3'd2; end
            'hf7: begin scalar_op='h63; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd2; mode=3'd3; end
            'h5e: begin scalar_op='hb6; source_wide=1; result_wide=0; lanes=3'd2; arity=3'd1; mode=3'd0; end
            'h5f: begin scalar_op='hbb; source_wide=0; result_wide=1; lanes=3'd2; arity=3'd1; mode=3'd0; end
            'hf8: begin scalar_op='hfc0000; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd1; mode=3'd0; end
            'hf9: begin scalar_op='hfc0001; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd1; mode=3'd0; end
            'hfa: begin scalar_op='hb2; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd1; mode=3'd0; end
            'hfb: begin scalar_op='hb3; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd1; mode=3'd0; end
            'hfc: begin scalar_op='hfc0002; source_wide=1; result_wide=0; lanes=3'd2; arity=3'd1; mode=3'd0; end
            'hfd: begin scalar_op='hfc0003; source_wide=1; result_wide=0; lanes=3'd2; arity=3'd1; mode=3'd0; end
            'hfe: begin scalar_op='hb7; source_wide=0; result_wide=1; lanes=3'd2; arity=3'd1; mode=3'd0; end
            'hff: begin scalar_op='hb8; source_wide=0; result_wide=1; lanes=3'd2; arity=3'd1; mode=3'd0; end
            'h101: begin scalar_op='hfc0000; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd1; mode=3'd0; end
            'h102: begin scalar_op='hfc0001; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd1; mode=3'd0; end
            'h103: begin scalar_op='hfc0002; source_wide=1; result_wide=0; lanes=3'd2; arity=3'd1; mode=3'd0; end
            'h104: begin scalar_op='hfc0003; source_wide=1; result_wide=0; lanes=3'd2; arity=3'd1; mode=3'd0; end
            'h105: begin scalar_op='h94; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd3; mode=3'd4; end
            'h106: begin scalar_op='h94; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd3; mode=3'd5; end
            'h107: begin scalar_op='ha2; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd3; mode=3'd4; end
            'h108: begin scalar_op='ha2; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd3; mode=3'd5; end
            'h10d: begin scalar_op='h96; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd2; mode=3'd0; end
            'h10e: begin scalar_op='h97; source_wide=0; result_wide=0; lanes=3'd4; arity=3'd2; mode=3'd0; end
            'h10f: begin scalar_op='ha4; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd2; mode=3'd0; end
            'h110: begin scalar_op='ha5; source_wide=1; result_wide=1; lanes=3'd2; arity=3'd2; mode=3'd0; end
            default: supported=0;
        endcase
        if(op[31:16]!='hfd) supported=0;
    end
endmodule
