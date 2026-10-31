// SPDX-License-Identifier: MIT
// One raw binary64 datapath serves both precisions. Binary32 operands are
// widened exactly by the caller. Each result is rounded directly to its final
// format from the raw significand and sticky bit; no intermediate rounding.
module wasmetal_fp_arithmetic (
    input logic clk, reset, start,
    input logic [5:0] operation,
    input logic [64:0] a, b,
    output wire [31:0] result32,
    output wire [63:0] result64,
    output wire div_done
);
    // Conditions: invalid, NaN, infinity, zero, sign.
    wire [4:0] add_condition, mul_condition, div_condition;
    wire signed [12:0] add_exponent, mul_exponent, div_exponent;
    wire [55:0] add_significand, mul_significand, div_significand;
    wire div_infinite, div_ready, unused_sqrt;
    wire [2:0] unused_rounding;
    addRecFNToRaw #(11,53) add_unit(
        1'b1,operation==8,a,b,3'b000,
        add_condition[4],add_condition[3],add_condition[2],add_condition[1],add_condition[0],
        add_exponent,add_significand);
    mulRecFNToRaw #(11,53) multiply_unit(
        1'b1,a,b,
        mul_condition[4],mul_condition[3],mul_condition[2],mul_condition[1],mul_condition[0],
        mul_exponent,mul_significand);
    divSqrtRecFNToRaw_small #(11,53,0) divide_unit(
        .nReset(!reset),.clock(clk),.control(1'b1),.inReady(div_ready),
        .inValid(start && (operation==6 || operation==10)),.sqrtOp(operation==6),
        .a(a),.b(b),.roundingMode(3'b000),.outValid(div_done),
        .sqrtOpOut(unused_sqrt),.roundingModeOut(unused_rounding),
        .invalidExc(div_condition[4]),.infiniteExc(div_infinite),
        .out_isNaN(div_condition[3]),.out_isInf(div_condition[2]),
        .out_isZero(div_condition[1]),.out_sign(div_condition[0]),
        .out_sExp(div_exponent),.out_sig(div_significand));
    wire select_div = div_done || operation==6 || operation==10;
    wire select_mul = operation==9;
    wire [4:0] condition = select_div ? div_condition : select_mul ? mul_condition : add_condition;
    wire signed [12:0] exponent = select_div ? div_exponent : select_mul ? mul_exponent : add_exponent;
    wire [55:0] significand = select_div ? div_significand : select_mul ? mul_significand : add_significand;
    wire [32:0] rec32;
    wire [64:0] rec64;
    wire [4:0] unused_flags32, unused_flags64;
    roundAnyRawFNToRecFN #(11,55,8,24,0) round32(
        1'b1,condition[4],select_div && div_infinite,
        condition[3],condition[2],condition[1],condition[0],exponent,significand,
        3'b000,rec32,unused_flags32);
    roundAnyRawFNToRecFN #(11,55,11,53,0) round64(
        1'b1,condition[4],select_div && div_infinite,
        condition[3],condition[2],condition[1],condition[0],exponent,significand,
        3'b000,rec64,unused_flags64);
    recFNToFN #(8,24) encode32(rec32,result32);
    recFNToFN #(11,53) encode64(rec64,result64);
`ifdef WASMETAL_ASSERTIONS
    always_ff @(posedge clk)
        if(!reset && start && (operation==6 || operation==10)) assert(div_ready);
`endif
endmodule
