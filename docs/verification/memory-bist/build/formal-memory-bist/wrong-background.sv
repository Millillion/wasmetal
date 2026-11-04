// SPDX-License-Identifier: MIT
// Destructive, exclusive-access test master for the physical memory interface.
// Eight complete March C- passes: seven separating bit backgrounds, then zero.
// A timeout retains the pending request and busy until its response or reset.
// Reset this master and its memory controller together. No arbitration is here.
module wasmetal_memory_bist #(
    parameter integer RAM_BYTES=131072,
    parameter integer RESPONSE_TIMEOUT=1024
) (
    input wire clk, reset, start,
    output wire busy,
    output logic done, failed,
    output logic [1:0] error_code,
    output logic [31:0] error_address,
    output logic [127:0] expected_data, observed_data,
    output logic [63:0] completed_operations,
    output wire valid, write,
    output wire [31:0] address,
    output wire [15:0] mask,
    output wire [127:0] wdata,
    input wire ready, fault,
    input wire [127:0] rdata
);
    localparam integer WORDS=RAM_BYTES/16,
        AW=WORDS>1 ? $clog2(WORDS) : 1,
        TW=RESPONSE_TIMEOUT>1 ? $clog2(RESPONSE_TIMEOUT) : 1;
    localparam logic [1:0] READ_MISMATCH=1, BUS_FAULT=2, TIMEOUT=3;
    typedef enum logic [1:0] {IDLE,REQUEST,RELEASE,FINISH} state_t;
    state_t state;
    logic [AW-1:0] word_index;
    logic [TW-1:0] waiting;
    logic [2:0] phase, background_index;
    logic write_half, stop_after_release;
    logic [127:0] background;
    wire descending=phase==3 || phase==4;
    wire final_word=descending ? word_index==0 : word_index==AW'(WORDS-1);
    wire [127:0] expected_read=(phase==2 || phase==4) ? ~background : background;
    wire mismatch=rdata!==expected_read;

    always_comb begin
        case(background_index)
            0:background=128'h0;
            1:background=128'hcccccccccccccccccccccccccccccccc;
            2:background={16{8'hf0}};
            3:background=128'hff00ff00ff00ff00ff00ff00ff00ff00;
            4:background=128'hffff0000ffff0000ffff0000ffff0000;
            5:background=128'hffffffff00000000ffffffff00000000;
            6:background=128'hffffffffffffffff0000000000000000;
            default:background=0;
        endcase
    end
    assign busy=state==REQUEST || state==RELEASE;
    assign valid=state==REQUEST && !reset;
    assign write=phase==0 || write_half;
    assign address=32'(word_index)<<4;
    assign mask=16'hffff;
    assign wdata=(phase==1 || phase==3) ? ~background : background;

    always_ff @(posedge clk) begin
        if(reset) begin
            state<=IDLE;word_index<=0;waiting<=0;phase<=0;background_index<=0;
            write_half<=0;stop_after_release<=0;done<=0;failed<=0;error_code<=0;
            error_address<=0;expected_data<=0;observed_data<=0;completed_operations<=0;
        end else case(state)
            IDLE: if(start) begin
                state<=REQUEST;word_index<=0;waiting<=0;phase<=0;background_index<=0;
                write_half<=0;stop_after_release<=0;done<=0;failed<=0;error_code<=0;
                error_address<=0;expected_data<=0;observed_data<=0;completed_operations<=0;
            end
            REQUEST: if(ready) begin
                completed_operations<=completed_operations+1'b1;
                waiting<=0;state<=RELEASE;
                if(failed || fault || (!write && mismatch)) begin
                    stop_after_release<=1;
                    if(!failed) begin
                        failed<=1;error_code<=fault ? BUS_FAULT : READ_MISMATCH;
                        error_address<=address;expected_data<=write ? wdata : expected_read;
                        observed_data<=rdata;
                    end
                end else if(phase>=1 && phase<=4 && !write_half) begin
                    write_half<=1;
                end else begin
                    write_half<=0;
                    if(!final_word) word_index<=descending ? word_index-1'b1 : word_index+1'b1;
                    else begin
                        case(phase)
                            0:begin phase<=1;word_index<=0;end
                            1:begin phase<=2;word_index<=0;end
                            2:begin phase<=3;word_index<=AW'(WORDS-1);end
                            3:begin phase<=4;word_index<=AW'(WORDS-1);end
                            4:begin phase<=5;word_index<=0;end
                            default:if(background_index==7) stop_after_release<=1;
                                else begin background_index<=background_index+1'b1;phase<=0;word_index<=0;end
                        endcase
                    end
                end
            end else if(!failed) begin
                if(waiting==TW'(RESPONSE_TIMEOUT-1)) begin
                    failed<=1;error_code<=TIMEOUT;error_address<=address;
                    expected_data<=write ? wdata : expected_read;observed_data<=0;
                    // Retain valid and payload until the outstanding access
                    // completes. Software must reset both sides if it never does.
                end else waiting<=waiting+1'b1;
            end
            RELEASE: if(stop_after_release) begin done<=1;state<=FINISH;end
                else state<=REQUEST;
            FINISH: if(!start) state<=IDLE;
        endcase
    end

`ifdef WASMETAL_ASSERTIONS
    initial begin
        assert(RAM_BYTES>=16 && RAM_BYTES%16==0 && RESPONSE_TIMEOUT>=1);
    end
    logic was_waiting;
    logic [160:0] pending_payload;
    always_ff @(posedge clk) begin
        if(reset) begin was_waiting<=0;pending_payload<=0;end
        else begin
            assert(phase<=5 && 32'(word_index)<WORDS);
            assert(!valid || (busy && address%16==0 && {1'b0,address}+33'd16<=33'(RAM_BYTES)));
            assert(!done || !busy);
            assert(!failed || error_code!=0);
            assert(completed_operations<=64'(WORDS)*64'd80);
            if(was_waiting) begin
                assert(valid);
                assert({write,address,wdata}==pending_payload);
            end
            was_waiting<=valid && !ready;
            pending_payload<={write,address,wdata};
        end
    end
`endif

    reg formal_started=0;
    reg keep_error;
    reg [290:0] saved_error;
    wire [127:0] mathematical_background;
    for(genvar formal_bit=0;formal_bit<128;formal_bit=formal_bit+1) begin: formal_background
        assign mathematical_background[formal_bit]=background_index==7 ? 1'b0 :
            1'((formal_bit>>background_index)&1);
    end
    reg [63:0] position_in_pass;
    always_comb case(phase)
        0:position_in_pass=64'(word_index);
        1:position_in_pass=64'(WORDS)+2*64'(word_index)+64'(write_half);
        2:position_in_pass=3*64'(WORDS)+2*64'(word_index)+64'(write_half);
        3:position_in_pass=5*64'(WORDS)+2*(64'(WORDS-1)-64'(word_index))+64'(write_half);
        4:position_in_pass=7*64'(WORDS)+2*(64'(WORDS-1)-64'(word_index))+64'(write_half);
        default:position_in_pass=9*64'(WORDS)+64'(word_index);
    endcase
    always @(posedge clk) begin
        if(!formal_started) assume(reset);
        formal_started<=1;
        if(reset) begin keep_error<=0;saved_error<=0;end
        else begin
            if(formal_started) begin
                assert((^{state,word_index,waiting,phase,background_index,write_half,
                    stop_after_release,done,failed,error_code,error_address,expected_data,
                    observed_data,completed_operations,was_waiting,pending_payload})!==1'bx);
                assert(background==mathematical_background);
                assert(completed_operations==64'(background_index)*10*64'(WORDS)+
                    position_in_pass+64'(stop_after_release));
                assert(32'(waiting)<RESPONSE_TIMEOUT);
                assert(!write_half || (phase>=1 && phase<=4));
                assert(state!=REQUEST || !stop_after_release);
                assert(!stop_after_release || state==RELEASE || state==FINISH || state==IDLE);
                assert(failed==(error_code!=0));
                if(done && !failed) assert(completed_operations==80*64'(WORDS));
                if(keep_error) assert({failed,error_code,error_address,expected_data,observed_data}==saved_error);
            end
            keep_error<=failed && !(state==IDLE && start);
            saved_error<={failed,error_code,error_address,expected_data,observed_data};
        end
    end

endmodule
