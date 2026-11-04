// SPDX-License-Identifier: MIT
// Wasm floating-point semantics around synthesizable Berkeley HardFloat units.
module wasmetal_fp_round_reference #(
    parameter integer EXP=8,
    parameter integer SIG=24,
    parameter integer N=EXP+SIG
) (
    input logic [5:0] operation,
    input logic [N-1:0] a, b,
    input logic integer_signed, result_signed,
    input logic [63:0] integer_input,
    input logic [N-1:0] arithmetic_result,
    input logic arithmetic_done,
    output logic [N-1:0] result, div_result, integer_float,
    output logic div_done,
    output logic [31:0] int32_result,
    output logic [63:0] int64_result,
    output logic [2:0] int32_flags, int64_flags,
    output logic [N:0] rec_a, rec_b,
    output logic is_nan
);
    localparam logic [N-1:0] QNAN={1'b0,{EXP{1'b1}},1'b1,{(SIG-2){1'b0}}};
    localparam integer ROUND_THRESHOLD=(1 << (EXP-1))-1+SIG-1;
    wire [N:0] rec_integer, rec_round;
    wire [N-1:0] round_result;
    wire [63:0] round_integer;
    wire [4:0] unused_compare_flags, unused_integer_flags, unused_round_flags;
    wire [2:0] unused_round_integer_flags;
    wire lt, eq, gt, unused_unordered;
    logic [2:0] round_mode;
    wire b_nan = (&b[N-2:SIG-1]) && (|b[SIG-2:0]);
    assign is_nan = (&a[N-2:SIG-1]) && (|a[SIG-2:0]);
    fNToRecFN #(EXP,SIG) decode_a(a,rec_a);
    fNToRecFN #(EXP,SIG) decode_b(b,rec_b);
    compareRecFN #(EXP,SIG) compare_unit(rec_a,rec_b,1'b0,lt,eq,gt,unused_unordered,unused_compare_flags);
    assign div_result = arithmetic_result;
    assign div_done = arithmetic_done;
    recFNToIN #(EXP,SIG,32) convert_i32(1'b1,rec_a,3'b001,result_signed,int32_result,int32_flags);
    recFNToIN #(EXP,SIG,64) convert_i64(1'b1,rec_a,3'b001,result_signed,int64_result,int64_flags);
    iNToRecFN #(64,EXP,SIG) convert_integer(1'b1,integer_signed,integer_input,3'b000,rec_integer,unused_integer_flags);
    recFNToFN #(EXP,SIG) encode_integer(rec_integer,integer_float);
    recFNToIN #(EXP,SIG,64) round_to_integer(1'b1,rec_a,round_mode,1'b1,round_integer,unused_round_integer_flags);
    iNToRecFN #(64,EXP,SIG) round_to_float(1'b1,1'b1,round_integer,3'b000,rec_round,unused_round_flags);
    recFNToFN #(EXP,SIG) encode_round(rec_round,round_result);
    always_comb begin
        case (operation)
            2: round_mode = 3'b011; // ceil, toward +infinity
            3: round_mode = 3'b010; // floor, toward -infinity
            4: round_mode = 3'b001; // truncate, toward zero
            default: round_mode = 3'b000; // nearest, ties even
        endcase
    end
    always_comb begin
        result = 0;
        case (operation)
            0: result = {1'b0,a[N-2:0]};
            1: result = {!a[N-1],a[N-2:0]};
            2,3,4,5: begin
                if (is_nan) result = QNAN;
                else if (a[N-2:SIG-1] >= EXP'(ROUND_THRESHOLD)) result = a;
                else if (round_result[N-2:0] == 0) result = {a[N-1],{(N-1){1'b0}}};
                else result = round_result;
            end
            7,8,9: result = arithmetic_result;
            11: begin
                if (is_nan || b_nan) result = QNAN;
                else if (eq) result = a | b;
                else result = lt ? a : b;
            end
            12: begin
                if (is_nan || b_nan) result = QNAN;
                else if (eq) result = a & b;
                else result = gt ? a : b;
            end
            13: result = {b[N-1],a[N-2:0]};
            14: result = {{(N-1){1'b0}},eq};
            15: result = {{(N-1){1'b0}},!eq};
            16: result = {{(N-1){1'b0}},lt};
            17: result = {{(N-1){1'b0}},gt};
            18: result = {{(N-1){1'b0}},lt || eq};
            19: result = {{(N-1){1'b0}},gt || eq};
            default: result = 0;
        endcase
    end
endmodule
