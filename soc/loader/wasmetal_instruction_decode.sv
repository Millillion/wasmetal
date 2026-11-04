// SPDX-License-Identifier: MIT
module wasmetal_instruction_decode (
    input wire [193:0] compact,
    output wire [287:0] expanded
);
    wire [287:0] form_a={96'b0,compact[191:0]};
    wire [287:0] form_b={compact[191:64],96'b0,compact[63:0]};
    wire [287:0] form_c={32'b0,compact[191:96],64'b0,compact[95:0]};
    wire [287:0] form_d={64'b0,compact[191:128],32'b0,compact[127:0]};
    // Conditional operators preserve the bits common to possible layouts when
    // a selector is unknown in four-state simulation.
    assign expanded=compact[193] ? (compact[192] ? form_d : form_c) :
                                   (compact[192] ? form_b : form_a);
endmodule
