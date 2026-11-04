// SPDX-License-Identifier: MIT
// Adapter to a synchronous, single-port, 128-bit SRAM with byte write enables.
// The macro samples enable/address/write/data on clk's rising edge. A read
// issued at edge N must be stable before edge N+READ_LATENCY. Neither reset nor
// this adapter clears SRAM contents; the upstream bridge owns initialization.
module wasmetal_sram_memory #(
    parameter integer RAM_BYTES=131072,
    parameter integer READ_LATENCY=1,
    parameter integer ADDRESS_WIDTH=(RAM_BYTES/16)>1 ? $clog2(RAM_BYTES/16) : 1
) (
    input wire clk, reset, valid, write,
    input wire [31:0] address,
    input wire [15:0] mask,
    input wire [127:0] wdata,
    output wire ready,
    output logic fault,
    output logic [127:0] rdata,
    output wire sram_enable, sram_write,
    output wire [ADDRESS_WIDTH-1:0] sram_address,
    output wire [15:0] sram_byte_enable,
    output wire [127:0] sram_wdata,
    input wire [127:0] sram_rdata
);
    localparam integer WORDS=RAM_BYTES/16,
        COUNT_WIDTH=READ_LATENCY>1 ? $clog2(READ_LATENCY+1) : 1;
    typedef enum logic [2:0] {IDLE,ISSUE,WAIT_READ,RESPONSE,RELEASE} state_t;
    state_t state;
    logic write_q;
    logic [ADDRESS_WIDTH-1:0] address_q;
    logic [15:0] mask_q;
    logic [127:0] data_q;
    logic [COUNT_WIDTH-1:0] remaining;
    wire legal=address[3:0]==0 && {1'b0,address}+33'd16<=33'(RAM_BYTES) && mask!=0;
    assign ready=state==RESPONSE;
    assign sram_enable=state==ISSUE && !reset;
    assign sram_write=sram_enable && write_q;
    assign sram_address=address_q;
    assign sram_byte_enable=mask_q;
    assign sram_wdata=data_q;

    always_ff @(posedge clk) begin
        if(reset) begin
            state<=IDLE;write_q<=0;address_q<=0;mask_q<=0;data_q<=0;
            remaining<=0;fault<=0;rdata<=0;
        end else case(state)
            IDLE: if(valid) begin
                write_q<=write;address_q<=address[ADDRESS_WIDTH+3:4];mask_q<=mask;data_q<=wdata;
                rdata<=0;fault<=!legal;remaining<=0;
                state<=legal ? ISSUE : RESPONSE;
            end
            ISSUE: if(write_q) state<=RESPONSE;
                else begin remaining<=COUNT_WIDTH'(READ_LATENCY);state<=WAIT_READ;end
            WAIT_READ: if(remaining==1) begin rdata<=sram_rdata;remaining<=0;state<=RESPONSE;end
                else remaining<=remaining-1'b1;
            RESPONSE: state<=RELEASE;
            RELEASE: if(!valid) state<=IDLE;
            default: begin fault<=1;rdata<=0;state<=RESPONSE;end
        endcase
    end

`ifdef WASMETAL_ASSERTIONS
    initial begin
        assert(RAM_BYTES>=16 && RAM_BYTES%16==0 && READ_LATENCY>=1);
        assert(ADDRESS_WIDTH==((WORDS>1) ? $clog2(WORDS) : 1));
    end
    // A command scoreboard checks timing and payload independently of the
    // implementation's countdown. It does not model the SRAM's stored data.
    logic tracked, waiting_release, expected_legal, expected_write;
    logic [31:0] expected_address;
    logic [COUNT_WIDTH:0] age;
    logic [15:0] expected_mask;
    logic [127:0] expected_data, prior_read_data;
    always_ff @(posedge clk) begin
        if(reset) begin
            tracked<=0;waiting_release<=0;expected_legal<=0;expected_write<=0;
            expected_address<=0;age<=0;expected_mask<=0;expected_data<=0;prior_read_data<=0;
        end else begin
            prior_read_data<=sram_rdata;
            assert(state<=RELEASE);
            assert(tracked==(state==ISSUE || state==WAIT_READ || state==RESPONSE));
            assert(waiting_release==(state==RELEASE));
            if(sram_enable || ready) assert(tracked);
            if(waiting_release) begin
                assert(!sram_enable && !ready);
                if(!valid) waiting_release<=0;
            end
            if(tracked) begin
                assert(32'(age)<=READ_LATENCY+1);
                assert(sram_enable==(expected_legal && age==0));
                assert(ready==(32'(age)==(expected_legal ? (expected_write ? 1 : READ_LATENCY+1) : 0)));
                if(sram_enable) begin
                    assert(sram_write==expected_write);
                    assert(32'(sram_address)==expected_address/16 && 32'(sram_address)<WORDS);
                    assert(sram_byte_enable==expected_mask && sram_byte_enable!=0);
                    assert(sram_wdata==expected_data && !fault);
                end
                if(ready) begin
                    assert(fault==!expected_legal);
                    if(expected_legal && !expected_write) begin assert(rdata==prior_read_data);end
                    else begin assert(rdata==0);end
                    tracked<=0;waiting_release<=1;
                end else age<=age+1'b1;
            end
            if(state==IDLE && valid) begin
                assert(!tracked && !waiting_release);
                tracked<=1;age<=0;expected_write<=write;
                expected_legal<=mask!=0 && address%16==0 && {1'b0,address}+33'd16<=33'(RAM_BYTES);
                expected_address<=address;expected_mask<=mask;expected_data<=wdata;
            end
        end
    end
`endif
endmodule
