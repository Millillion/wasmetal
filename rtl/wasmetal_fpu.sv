// SPDX-License-Identifier: MIT
module wasmetal_fpu (
    input logic clk, reset, start,
    input logic [31:0] op,
    input logic [63:0] a, b,
    output logic supported, unary_op, done,
    output logic [63:0] result,
    output logic [7:0] trap
);
    logic [5:0] operation;
    logic wide, int_wide, result_signed, integer_signed, is_sat;
    logic [63:0] integer_input, calculated, converted;
    logic [7:0] calculated_trap;
    logic [2:0] conversion_flags;
    wire [31:0] f32_result, f32_div, f32_integer, f32_i32;
    wire [63:0] f64_result, f64_div, f64_integer, f32_i64, f64_i64;
    wire [31:0] f64_i32, demoted;
    wire [63:0] promoted;
    wire [32:0] f32_rec, f32_rec_b, rec_demoted;
    wire [64:0] f64_rec, f64_rec_b, rec_promoted, rec_promoted_b;
    wire [2:0] f32_i32_flags, f32_i64_flags, f64_i32_flags, f64_i64_flags;
    wire f32_done, f64_done, f32_nan, f64_nan;
    wire [4:0] unused_promote_flags, unused_promote_b_flags, unused_demote_flags;
    wire [31:0] arithmetic32;
    wire [63:0] arithmetic64;
    wire arithmetic_done;
    logic divide_wide;
    wasmetal_fp_format #(8,24) fp32(
        .arithmetic_result(arithmetic32),.arithmetic_done(arithmetic_done && !divide_wide),.operation(operation),.a(a[31:0]),.b(b[31:0]),
        .integer_signed(integer_signed),.result_signed(result_signed),.integer_input(integer_input),
        .result(f32_result),.div_result(f32_div),.integer_float(f32_integer),.div_done(f32_done),
        .int32_result(f32_i32),.int64_result(f32_i64),.int32_flags(f32_i32_flags),.int64_flags(f32_i64_flags),
        .rec_a(f32_rec),.rec_b(f32_rec_b),.is_nan(f32_nan));
    wasmetal_fp_format #(11,53) fp64(
        .arithmetic_result(arithmetic64),.arithmetic_done(arithmetic_done && divide_wide),.operation(operation),.a(a),.b(b),
        .integer_signed(integer_signed),.result_signed(result_signed),.integer_input(integer_input),
        .result(f64_result),.div_result(f64_div),.integer_float(f64_integer),.div_done(f64_done),
        .int32_result(f64_i32),.int64_result(f64_i64),.int32_flags(f64_i32_flags),.int64_flags(f64_i64_flags),
        .rec_a(f64_rec),.rec_b(f64_rec_b),.is_nan(f64_nan));
    recFNToRecFN #(8,24,11,53) promote(1'b1,f32_rec,3'b000,rec_promoted,unused_promote_flags);
    recFNToRecFN #(8,24,11,53) promote_b(1'b1,f32_rec_b,3'b000,rec_promoted_b,unused_promote_b_flags);
    wasmetal_fp_arithmetic arithmetic(
        .clk(clk),.reset(reset),.start(start),.operation(operation),
        .a(wide ? f64_rec : rec_promoted),.b(wide ? f64_rec_b : rec_promoted_b),
        .result32(arithmetic32),.result64(arithmetic64),.div_done(arithmetic_done));
    always_ff @(posedge clk) begin
        if(reset) divide_wide<=0;
        else if(start && (operation==6 || operation==10)) divide_wide<=wide;
    end
    recFNToFN #(11,53) encode_promote(rec_promoted,promoted);
    recFNToRecFN #(11,53,8,24) demote(1'b1,f64_rec,3'b000,rec_demoted,unused_demote_flags);
    recFNToFN #(8,24) encode_demote(rec_demoted,demoted);
    assign supported = (op >= 'h5b && op <= 'h66) || (op >= 'h8b && op <= 'ha6) ||
            (op >= 'ha8 && op <= 'hab) || (op >= 'hae && op <= 'hbb) ||
            (op >= 'hfc0000 && op <= 'hfc0007);
    assign unary_op = (op >= 'h8b && op <= 'h91) || (op >= 'h99 && op <= 'h9f) || op >= 'ha8;
    always_comb begin
        operation = 0; wide = 0; int_wide = 0; result_signed = 0;
        integer_signed = op == 'hb2 || op == 'hb4 || op == 'hb7 || op == 'hb9;
        integer_input = a;
        if (op == 'hb2 || op == 'hb7) integer_input = {{32{a[31]}},a[31:0]};
        else if (op == 'hb3 || op == 'hb8) integer_input = {32'b0,a[31:0]};
        is_sat = op >= 'hfc0000 && op <= 'hfc0007;
        if (op >= 'h8b && op <= 'h98) operation = 6'(op-'h8b);
        else if (op >= 'h99 && op <= 'ha6) begin operation = 6'(op-'h99); wide = 1; end
        else if (op >= 'h5b && op <= 'h60) operation = 6'(op-'h5b+14);
        else if (op >= 'h61 && op <= 'h66) begin operation = 6'(op-'h61+14); wide = 1; end
        if (op == 'haa || op == 'hab || op == 'hb0 || op == 'hb1 || (op >= 'hb7 && op <= 'hba)) wide = 1;
        if (op >= 'hae && op <= 'hb1) int_wide = 1;
        if (op == 'ha8 || op == 'haa || op == 'hae || op == 'hb0) result_signed = 1;
        if (is_sat) begin wide = op[1]; int_wide = op[2]; result_signed = !op[0]; end
    end
    always_comb begin
        calculated = wide ? f64_result : {32'b0,f32_result}; calculated_trap = 0;
        converted = int_wide ? (wide ? f64_i64 : f32_i64) : {32'b0,(wide ? f64_i32 : f32_i32)};
        conversion_flags = int_wide ? (wide ? f64_i64_flags : f32_i64_flags) : (wide ? f64_i32_flags : f32_i32_flags);
        if ((op >= 'ha8 && op <= 'hab) || (op >= 'hae && op <= 'hb1) || is_sat) begin
            calculated = converted;
            if (wide ? f64_nan : f32_nan) begin
                calculated = 0;
                if (!is_sat) calculated_trap = 8;
            end else if (!is_sat && (conversion_flags[2] || conversion_flags[1])) calculated_trap = 3;
        end else if ((op >= 'hb2 && op <= 'hb5) || (op >= 'hb7 && op <= 'hba))
            calculated = wide ? f64_integer : {32'b0,f32_integer};
        else if (op == 'hb6) calculated = {32'b0,demoted};
        else if (op == 'hbb) calculated = promoted;
    end
    always_ff @(posedge clk) begin
        if (reset) begin done <= 0; result <= 0; trap <= 0; end
        else begin
            done <= 0;
            if (start && operation != 6 && operation != 10) begin
                done <= 1; result <= calculated; trap <= calculated_trap;
            end else if (f32_done || f64_done) begin
                done <= 1; result <= f64_done ? f64_div : {32'b0,f32_div}; trap <= 0;
            end
        end
    end
endmodule
