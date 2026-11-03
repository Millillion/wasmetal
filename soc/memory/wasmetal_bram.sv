// SPDX-License-Identifier: MIT
// Masked 128-bit storage. This backend is replaceable by a checked external
// memory controller or SRAM adapter; clearing belongs to the bridge.
module wasmetal_bram #(
    parameter integer RAM_BYTES=131072
) (
    input wire clk, reset, valid, write,
    input wire [31:0] address,
    input wire [15:0] mask,
    input wire [127:0] wdata,
    output wire ready,
    output logic fault,
    output logic [127:0] rdata
);
    // Explicit 2048-word banks retain the already checked ECP5 9-bit RAM mode.
    localparam integer WORDS=RAM_BYTES/16, AW=WORDS>1 ? $clog2(WORDS) : 1,
        BANK_WORDS=WORDS<2048 ? WORDS : 2048, BANKS=WORDS/BANK_WORDS;
    typedef enum logic [1:0] {IDLE,DELAY,RESPONSE,RELEASE} state_t;
    state_t state;
    logic [AW-1:0] saved_address;
    wire [127:0] bank_value [0:BANKS-1];
    wire [127:0] read_value=bank_value[32'(saved_address)/BANK_WORDS];
    wire legal=address[3:0]==0 && {1'b0,address}+33'd16<=33'(RAM_BYTES) && mask!=0;
    wire accepting=state==IDLE && valid && !reset && legal;
    assign ready=state==RESPONSE;
    for(genvar bank=0;bank<BANKS;bank=bank+1) begin: banks
        for(genvar lane=0;lane<16;lane=lane+1) begin: lanes
            (* ram_style="block" *) logic [7:0] storage [0:BANK_WORDS-1];
            logic [7:0] value;
            always_ff @(posedge clk) if(accepting && write && mask[lane] &&
                                         32'(address[AW+3:4])/BANK_WORDS==bank)
                storage[32'(address[AW+3:4])%BANK_WORDS]<=wdata[lane*8+:8];
            always_ff @(negedge clk) value<=storage[32'(saved_address)%BANK_WORDS];
            assign bank_value[bank][lane*8+:8]=value;
        end
    end
    always_ff @(posedge clk) begin
        if(reset) begin state<=IDLE; saved_address<=0; fault<=0; rdata<=0; end
        else case(state)
            IDLE: if(valid) begin
                fault<=!legal; saved_address<=address[AW+3:4]; state<=DELAY;
            end
            DELAY: begin rdata<=fault ? 128'b0 : read_value; state<=RESPONSE; end
            RESPONSE: state<=RELEASE;
            RELEASE: if(!valid) state<=IDLE;
            default: state<=IDLE;
        endcase
    end
endmodule
