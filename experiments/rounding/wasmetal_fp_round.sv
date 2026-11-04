// SPDX-License-Identifier: MIT
// Integral rounding directly in the IEEE encoding. Experimental until integrated.
module wasmetal_fp_round #(parameter integer EXP=8,SIG=24,N=EXP+SIG) (
    input wire [N-1:0] a,
    input wire [1:0] mode, // ceil, floor, trunc, nearest-even
    output wire [N-1:0] result
);
    initial begin
        if (!((EXP==8 && SIG==24 && N==32) || (EXP==11 && SIG==53 && N==64)))
            $fatal(1,"integral rounding supports only binary32 and binary64");
    end
    localparam integer CW=$clog2(N);
    localparam logic [EXP-1:0] BIAS=EXP'((1<<(EXP-1))-1),
        THRESHOLD=EXP'((1<<(EXP-1))-1+SIG-1);
    localparam logic [N-2:0] ONE={BIAS,{(SIG-1){1'b0}}};
    localparam logic [N-1:0] QNAN={1'b0,{EXP{1'b1}},1'b1,{(SIG-2){1'b0}}};
    wire sign=a[N-1];
    wire [EXP-1:0] exponent=a[N-2:SIG-1];
    wire [N-2:0] magnitude=a[N-2:0];
    wire nan=(&exponent) && (|a[SIG-2:0]);
    // In the ordinary branch, the count is between 1 and SIG-1; its low
    // CW bits are sufficient. Other exponents select a different result.
    wire [EXP-1:0] fractional_bits=THRESHOLD-exponent;
    wire [N-2:0] unit_bit={{(N-2){1'b0}},1'b1} << fractional_bits[CW-1:0];
    wire [N-2:0] fraction_mask=unit_bit-1'b1;
    wire [N-2:0] down=magnitude & ~fraction_mask;
    wire [N-2:0] lost=magnitude & fraction_mask;
    wire [N-2:0] half_bit=unit_bit>>1;
    // For magnitudes [1,2), the integer's low bit is the implicit leading 1.
    // Above that range, it is the encoded significand bit at the rounding unit.
    wire odd=(exponent==BIAS) || (|(magnitude & unit_bit));
    wire nearest_up=(|(lost & half_bit)) && ((|(lost & (half_bit-1'b1))) || odd);
    wire up=mode==0 ? (!sign && (|lost)) : mode==1 ? (sign && (|lost)) :
        mode==2 ? 1'b0 : nearest_up;
    // Below one, nearest-even rounds exactly one half to signed zero.
    wire small_up=mode==0 ? (!sign && (|magnitude)) : mode==1 ? (sign && (|magnitude)) :
        mode==2 ? 1'b0 : ((exponent==BIAS-1'b1) && (|a[SIG-2:0]));
    wire [N-1:0] small_result={sign,small_up ? ONE : {(N-1){1'b0}}};
    wire [N-1:0] ordinary_result={sign,up ? down+unit_bit : down};
    // Ternaries merge possibilities when a control is X/Z; they do not
    // silently select a known branch for an unknown condition.
    assign result=nan ? QNAN : exponent>=THRESHOLD ? a : exponent<BIAS ? small_result : ordinary_result;
endmodule
