// SPDX-License-Identifier: MIT
// Scalar integer operations. Integer division is handled by wasmetal_divider.
module wasmetal_alu (
    input  logic [31:0] op,
    input  logic [63:0] a, b,
    output logic [63:0] result,
    output logic unary_op,
    output logic supported
);
    logic [31:0] a32, b32, r32;
    logic [63:0] r64;
    wire [5:0] population32;
    wire [6:0] population64;
    wasmetal_popcount #(32) pop32(a[31:0],population32);
    wasmetal_popcount #(64) pop64(a,population64);
    integer i;
    always_comb begin
        i = 0;
        a32 = a[31:0]; b32 = b[31:0];
        r32 = 0; r64 = 0; result = 0;
        unary_op = 0; supported = 1;
        case (op)
            'h45: begin result = {63'b0, a32 == 0}; unary_op = 1; end
            'h46: result = {63'b0, a32 == b32};
            'h47: result = {63'b0, a32 != b32};
            'h48: result = {63'b0, $signed(a32) < $signed(b32)};
            'h49: result = {63'b0, a32 < b32};
            'h4a: result = {63'b0, $signed(a32) > $signed(b32)};
            'h4b: result = {63'b0, a32 > b32};
            'h4c: result = {63'b0, $signed(a32) <= $signed(b32)};
            'h4d: result = {63'b0, a32 <= b32};
            'h4e: result = {63'b0, $signed(a32) >= $signed(b32)};
            'h4f: result = {63'b0, a32 >= b32};
            'h50: begin result = {63'b0, a == 0}; unary_op = 1; end
            'h51: result = {63'b0, a == b};
            'h52: result = {63'b0, a != b};
            'h53: result = {63'b0, $signed(a) < $signed(b)};
            'h54: result = {63'b0, a < b};
            'h55: result = {63'b0, $signed(a) > $signed(b)};
            'h56: result = {63'b0, a > b};
            'h57: result = {63'b0, $signed(a) <= $signed(b)};
            'h58: result = {63'b0, a <= b};
            'h59: result = {63'b0, $signed(a) >= $signed(b)};
            'h5a: result = {63'b0, a >= b};
            'h67: begin
                r32 = 32;
                for (i=0; i<32; i=i+1) if (a32[i]) r32 = 32'(31-i);
                result = {32'b0, r32}; unary_op = 1;
            end
            'h68: begin
                r32 = 32;
                for (i=31; i>=0; i=i-1) if (a32[i]) r32 = 32'(i);
                result = {32'b0, r32}; unary_op = 1;
            end
            'h69: begin
                result = {58'b0,population32}; unary_op = 1;
            end
            'h6a: begin r32 = a32+b32; result = {32'b0,r32}; end
            'h6b: begin r32 = a32-b32; result = {32'b0,r32}; end
            'h6c: begin r32 = a32*b32; result = {32'b0,r32}; end
            'h71: result = {32'b0, a32 & b32};
            'h72: result = {32'b0, a32 | b32};
            'h73: result = {32'b0, a32 ^ b32};
            'h74: begin r32 = a32 << b32[4:0]; result = {32'b0,r32}; end
            'h75: begin r32 = $signed(a32) >>> b32[4:0]; result = {32'b0,r32}; end
            'h76: begin r32 = a32 >> b32[4:0]; result = {32'b0,r32}; end
            'h77: begin r32 = (a32 << b32[4:0]) | (a32 >> (32-{27'b0,b32[4:0]})); result = {32'b0,r32}; end
            'h78: begin r32 = (a32 >> b32[4:0]) | (a32 << (32-{27'b0,b32[4:0]})); result = {32'b0,r32}; end
            'h79: begin
                r64 = 64;
                for (i=0; i<64; i=i+1) if (a[i]) r64 = {32'b0,32'(63-i)};
                result = r64; unary_op = 1;
            end
            'h7a: begin
                r64 = 64;
                for (i=63; i>=0; i=i-1) if (a[i]) r64 = 64'(i);
                result = r64; unary_op = 1;
            end
            'h7b: begin
                result = {57'b0,population64}; unary_op = 1;
            end
            'h7c: result = a+b;
            'h7d: result = a-b;
            'h7e: result = a*b;
            'h83: result = a & b;
            'h84: result = a | b;
            'h85: result = a ^ b;
            'h86: result = a << b[5:0];
            'h87: result = $signed(a) >>> b[5:0];
            'h88: result = a >> b[5:0];
            'h89: result = (a << b[5:0]) | (a >> (64-{26'b0,b[5:0]}));
            'h8a: result = (a >> b[5:0]) | (a << (64-{26'b0,b[5:0]}));
            'ha7: begin result = {32'b0,a32}; unary_op = 1; end
            'hac: begin result = {{32{a32[31]}},a32}; unary_op = 1; end
            'had: begin result = {32'b0,a32}; unary_op = 1; end
            'hbc, 'hbe: begin result = {32'b0,a32}; unary_op = 1; end
            'hbd, 'hbf: begin result = a; unary_op = 1; end
            'hc0: begin result = {32'b0,{24{a[7]}},a[7:0]}; unary_op = 1; end
            'hc1: begin result = {32'b0,{16{a[15]}},a[15:0]}; unary_op = 1; end
            'hc2: begin result = {{56{a[7]}},a[7:0]}; unary_op = 1; end
            'hc3: begin result = {{48{a[15]}},a[15:0]}; unary_op = 1; end
            'hc4: begin result = {{32{a[31]}},a[31:0]}; unary_op = 1; end
            default: supported = 0;
        endcase
    end
endmodule
