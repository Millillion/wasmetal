// SPDX-License-Identifier: MIT
module fp_shared_tb (
    input logic clk, reset, start, wide,
    input logic [5:0] operation,
    input logic [63:0] a,b,
    output wire [63:0] actual, expected,
    output wire actual_done, expected_done
);
    wire [32:0] rec32a, rec32b;
    wire [64:0] rec64a, rec64b, extended_a, extended_b;
    wire [31:0] result32, ref32, div32;
    wire [63:0] result64, ref64, div64;
    wire done32, done64;
    wire [4:0] unused_flags_a,unused_flags_b;
    wasmetal_fp_format_reference #(8,24) reference32(
        .clk(clk),.reset(reset),.start(start && !wide),.operation(operation),
        .a(a[31:0]),.b(b[31:0]),.integer_signed(1'b0),.result_signed(1'b0),.integer_input(64'b0),
        .result(ref32),.div_result(div32),.integer_float(),.div_done(done32),
        .int32_result(),.int64_result(),.int32_flags(),.int64_flags(),.rec_a(rec32a),.is_nan());
    wasmetal_fp_format_reference #(11,53) reference64(
        .clk(clk),.reset(reset),.start(start && wide),.operation(operation),
        .a(a),.b(b),.integer_signed(1'b0),.result_signed(1'b0),.integer_input(64'b0),
        .result(ref64),.div_result(div64),.integer_float(),.div_done(done64),
        .int32_result(),.int64_result(),.int32_flags(),.int64_flags(),.rec_a(rec64a),.is_nan());
    fNToRecFN #(8,24) decode32b(b[31:0],rec32b);
    fNToRecFN #(11,53) decode64b(b,rec64b);
    recFNToRecFN #(8,24,11,53) extend_a(1'b1,rec32a,3'b000,extended_a,unused_flags_a);
    recFNToRecFN #(8,24,11,53) extend_b(1'b1,rec32b,3'b000,extended_b,unused_flags_b);
    wasmetal_fp_arithmetic shared_unit(
        .clk(clk),.reset(reset),.start(start),.operation(operation),
        .a(wide ? rec64a : extended_a),.b(wide ? rec64b : extended_b),
        .result32(result32),.result64(result64),.div_done(actual_done));
    assign actual=wide ? result64 : {32'b0,result32};
    wire is_div=operation==6 || operation==10;
    assign expected=wide ? (is_div ? div64 : ref64) : {32'b0,(is_div ? div32 : ref32)};
    assign expected_done=wide ? done64 : done32;
endmodule
