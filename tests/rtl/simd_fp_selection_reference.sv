// Behavioral reference retained from the original CPU lane-selection block.
// This includes result assembly and out-of-range lanes, not only valid Wasm lanes.
module simd_fp_selection_reference(
    input wire [127:0] top,below,third,simd_accum,
    input wire [63:0] fp_result,
    input wire [2:0] simd_lane,simd_arity,simd_mode,
    input wire simd_source_wide,simd_result_wide,
    output logic [63:0] simd_a_lane,simd_b_lane,simd_c_lane,simd_result_lane,
    output logic [127:0] simd_assembled
);
    logic [127:0] simd_a,simd_b;
    always_comb begin
        simd_a = simd_arity == 1 ? top : simd_arity == 2 ? below : third;
        simd_b = simd_arity == 3 ? below : top;
        simd_a_lane = 64'(simd_a >> (simd_lane*(simd_source_wide ? 64 : 32)));
        simd_b_lane = 64'(simd_b >> (simd_lane*(simd_source_wide ? 64 : 32)));
        simd_c_lane = 64'(top >> (simd_lane*(simd_source_wide ? 64 : 32)));
        if (!simd_source_wide) begin simd_a_lane[63:32]=0; simd_b_lane[63:32]=0; simd_c_lane[63:32]=0; end
        simd_result_lane = fp_result;
        if (simd_mode == 1) simd_result_lane = {64{fp_result[0]}};
        else if (simd_mode == 2 || simd_mode == 3) simd_result_lane = fp_result[0] ? simd_b_lane : simd_a_lane;
        simd_assembled = simd_accum;
        if (simd_result_wide) simd_assembled[simd_lane*64+:64] = simd_result_lane;
        else simd_assembled[simd_lane*32+:32] = simd_result_lane[31:0];
    end
endmodule
