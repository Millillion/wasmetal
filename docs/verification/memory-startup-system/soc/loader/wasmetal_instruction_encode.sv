// SPDX-License-Identifier: MIT
// Lossless storage for expanded instructions whose operand fields fit one of
// four layouts. Preserve the full opcode and all retained operand bits. The
// loader must reject an image if any instruction has encodable != 1.
module wasmetal_instruction_encode (
    input wire [287:0] expanded,
    output wire [193:0] compact,
    output wire encodable
);
    wire form_a=expanded[287:192]==0;
    wire form_b=expanded[159:64]==0;
    wire form_c=expanded[159:96]==0 && expanded[287:256]==0;
    wire form_d=expanded[159:128]==0 && expanded[287:224]==0;
    assign encodable=form_a || form_b || form_c || form_d;
    assign compact=form_a ? {2'b00,expanded[191:0]} :
                   form_b ? {2'b01,expanded[287:160],expanded[63:0]} :
                   form_c ? {2'b10,expanded[255:160],expanded[95:0]} :
                            {2'b11,expanded[223:160],expanded[127:0]};
endmodule

