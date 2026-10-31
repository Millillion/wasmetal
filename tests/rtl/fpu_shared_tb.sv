// SPDX-License-Identifier: MIT
module fpu_shared_tb (
    input logic clk, reset, start,
    input logic [31:0] op,
    input logic [63:0] a,b,
    output wire [63:0] actual, expected,
    output wire [7:0] actual_trap,expected_trap,
    output wire actual_done,expected_done,
    output wire actual_supported,expected_supported,actual_unary,expected_unary
);
    wasmetal_fpu implementation(
        .clk(clk),.reset(reset),.start(start),.op(op),.a(a),.b(b),
        .supported(actual_supported),.unary_op(actual_unary),.done(actual_done),
        .result(actual),.trap(actual_trap));
    wasmetal_fpu_reference reference_unit(
        .clk(clk),.reset(reset),.start(start),.op(op),.a(a),.b(b),
        .supported(expected_supported),.unary_op(expected_unary),.done(expected_done),
        .result(expected),.trap(expected_trap));
endmodule
