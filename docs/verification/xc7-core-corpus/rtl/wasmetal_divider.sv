// SPDX-License-Identifier: MIT
// One quotient bit per clock. No combinational / or % hardware.
module wasmetal_divider (
    input logic clk, reset, start, wide, signed_op, remainder_op,
    input logic [63:0] a, b,
    output logic done,
    output logic [63:0] result,
    output logic [7:0] trap
);
    logic busy, neg_q, neg_r, is_rem, is_wide;
    logic [6:0] remaining;
    logic [63:0] dividend, divisor, quotient, rem_value;
    logic [64:0] trial, next_rem;
    logic [63:0] next_q, abs_a, abs_b, norm_a, norm_b;
    logic sign_a, sign_b;
    always_comb begin
        norm_a = wide ? a : {32'b0,a[31:0]};
        norm_b = wide ? b : {32'b0,b[31:0]};
        sign_a = signed_op && (wide ? a[63] : a[31]);
        sign_b = signed_op && (wide ? b[63] : b[31]);
        abs_a = sign_a ? -norm_a : norm_a;
        abs_b = sign_b ? -norm_b : norm_b;
        if (!wide) begin abs_a[63:32] = 0; abs_b[63:32] = 0; end
        trial = {rem_value,dividend[63]};
        next_rem = trial >= {1'b0,divisor} ? trial-{1'b0,divisor} : trial;
        next_q = {quotient[62:0],trial >= {1'b0,divisor}};
    end
    always_ff @(posedge clk) begin
        if (reset) begin
            busy <= 0; done <= 0; result <= 0; trap <= 0;
            neg_q <= 0; neg_r <= 0; is_rem <= 0; is_wide <= 0;
            remaining <= 0; dividend <= 0; divisor <= 0; quotient <= 0; rem_value <= 0;
        end else begin
            done <= 0;
            if (start && !busy) begin
                trap <= 0;
                if (norm_b == 0) begin done <= 1; trap <= 2; result <= 0; end
                else if (signed_op && !remainder_op &&
                    ((wide && a == 64'h8000000000000000 && b == 64'hffffffffffffffff) ||
                     (!wide && a[31:0] == 32'h80000000 && b[31:0] == 32'hffffffff))) begin
                    done <= 1; trap <= 3; result <= 0;
                end else begin
                    busy <= 1; remaining <= wide ? 7'd64 : 7'd32;
                    dividend <= wide ? abs_a : {abs_a[31:0],32'b0};
                    divisor <= abs_b; quotient <= 0; rem_value <= 0;
                    neg_q <= sign_a ^ sign_b; neg_r <= sign_a;
                    is_rem <= remainder_op; is_wide <= wide;
                end
            end else if (busy) begin
                dividend <= {dividend[62:0],1'b0};
                quotient <= next_q; rem_value <= next_rem[63:0];
                remaining <= remaining-1'b1;
                if (remaining == 1) begin
                    busy <= 0; done <= 1;
                    if (is_rem) result <= neg_r ? -next_rem[63:0] : next_rem[63:0];
                    else result <= neg_q ? -next_q : next_q;
                    if (!is_wide) result[63:32] <= 0;
                end
            end
        end
    end
endmodule
