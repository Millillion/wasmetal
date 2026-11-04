// SPDX-License-Identifier: MIT
module codec_proof (
    input wire [287:0] original,
    input wire [193:0] arbitrary_stored,
    output wire ok
);
    wire [193:0] stored,repacked;
    wire [287:0] restored,decoded,decoded_again;
    wire valid,decoded_valid;
    wasmetal_instruction_encode e(original,stored,valid);
    wasmetal_instruction_decode d(stored,restored);
    wasmetal_instruction_decode d2(arbitrary_stored,decoded);
    wasmetal_instruction_encode e2(decoded,repacked,decoded_valid);
    wasmetal_instruction_decode d3(repacked,decoded_again);
    assign ok=(valid==(restored==original)) && stored[31:0]==original[31:0] &&
              decoded_valid && decoded_again==decoded;
endmodule
