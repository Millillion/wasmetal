// SPDX-License-Identifier: MIT
// Trusted prepared-image transport. The CPU must stay reset while !image_valid.
// Metadata stores accept every word_valid pulse; no memory backpressure exists.
module wasmetal_image_loader #(
    parameter integer INSTRUCTION_DEPTH=1024, FUNCTION_DEPTH=128, TYPE_DEPTH=64,
    parameter integer BOOT_DEPTH=512, REGIONS_PER_KIND=16, TIMEOUT_CYCLES=2000000,
    parameter logic [127:0] PROFILE_TAG=0,
    parameter integer WORD_WIDTH=(TYPE_DEPTH>288 ? TYPE_DEPTH : 288)
) (
    input wire clk, reset, abort_load,
    input wire rx_valid,
    input wire [7:0] rx_data,
    output wire tx_valid,
    output logic [7:0] tx_data,
    input wire tx_ready,
    output logic image_valid,
    output wire word_valid,
    output logic [2:0] word_section,
    output logic [31:0] word_index,
    output logic [WORD_WIDTH-1:0] word_data
);
    localparam integer BCW=$clog2(WORD_WIDTH/8+1), TCW=$clog2(TIMEOUT_CYCLES+1);
    localparam logic [31:0] PAYLOAD_BYTES=36*INSTRUCTION_DEPTH+20*FUNCTION_DEPTH+
        ((TYPE_DEPTH+7)/8)*TYPE_DEPTH+48*REGIONS_PER_KIND+29*BOOT_DEPTH;
    localparam logic [31:0] TOTAL_WORDS=INSTRUCTION_DEPTH+FUNCTION_DEPTH+TYPE_DEPTH+
        6*REGIONS_PER_KIND+BOOT_DEPTH;
    typedef enum logic [2:0] {SEARCH,HEADER,REPLY,PAYLOAD,CHECKSUM} state_t;
    state_t state;
    logic [1:0] magic_index, checksum_index;
    logic [4:0] header_index, reply_index;
    logic [231:0] header_data;
    wire [231:0] header_next={rx_data,header_data[231:8]};
    logic [63:0] nonce;
    logic [31:0] crc, received_crc, reply_image_crc, cursor, words_sent;
    wire [31:0] checksum_next={rx_data,received_crc[31:8]};
    logic [15:0] reply_crc;
    logic [7:0] reply_status;
    logic [2:0] section;
    logic [BCW-1:0] byte_index;
    logic [TCW-1:0] idle_cycles;
    logic write_pending, checksum_verified;
    assign word_valid=write_pending && !reset && !abort_load;
    assign tx_valid=state==REPLY && !reset && !abort_load;

    function automatic [31:0] crc32_byte(input [31:0] previous,input [7:0] data);
        reg [31:0] value;
        begin
            value=previous^{24'b0,data};
            for(integer n=0;n<8;n=n+1) value=value[0] ? (value>>1)^32'hedb88320 : value>>1;
            crc32_byte=value;
        end
    endfunction
    function automatic [15:0] crc16_byte(input [15:0] previous,input [7:0] data);
        reg [15:0] value;
        begin
            value=previous^{data,8'b0};
            for(integer n=0;n<8;n=n+1) value=value[15] ? (value<<1)^16'h1021 : value<<1;
            crc16_byte=value;
        end
    endfunction
    function automatic [31:0] section_words(input [2:0] which);
        case(which)
            0: section_words=INSTRUCTION_DEPTH;
            1: section_words=FUNCTION_DEPTH;
            2: section_words=TYPE_DEPTH;
            3: section_words=6*REGIONS_PER_KIND;
            4: section_words=BOOT_DEPTH;
            default: section_words=0;
        endcase
    endfunction
    function automatic [31:0] section_bytes(input [2:0] which);
        case(which)
            0: section_bytes=36;
            1: section_bytes=20;
            2: section_bytes=(TYPE_DEPTH+7)/8;
            3: section_bytes=8;
            4: section_bytes=29;
            default: section_bytes=0;
        endcase
    endfunction
    function automatic [7:0] magic_byte(input [1:0] position);
        case(position)
            0: magic_byte=8'h57;
            1: magic_byte=8'h4d;
            2: magic_byte=8'h4c;
            3: magic_byte=8'h44;
        endcase
    endfunction
    always_comb begin
        tx_data=0;
        case(reply_index)
            0: tx_data=8'h57;
            1: tx_data=8'h4d;
            2: tx_data=8'h4c;
            3: tx_data=8'h52;
            4: tx_data=1;
            5: tx_data=reply_status;
            6,7,8,9,10,11,12,13: tx_data=nonce[(reply_index-6)*8+:8];
            14,15,16,17: tx_data=reply_image_crc[(reply_index-14)*8+:8];
            18: tx_data=reply_crc[7:0];
            19: tx_data=reply_crc[15:8];
            default: tx_data=0;
        endcase
    end
    task automatic reply(input [7:0] status,input [31:0] checksum);
        begin
            reply_status<=status;reply_image_crc<=checksum;reply_index<=0;
            reply_crc<=16'hffff;idle_cycles<=0;state<=REPLY;
        end
    endtask

    always_ff @(posedge clk) begin
        if(reset) begin
            state<=SEARCH;magic_index<=0;checksum_index<=0;header_index<=0;reply_index<=0;
            header_data<=0;nonce<=0;crc<=32'hffffffff;received_crc<=0;reply_image_crc<=0;
            cursor<=0;words_sent<=0;reply_crc<=16'hffff;reply_status<=0;section<=0;
            byte_index<=0;idle_cycles<=0;write_pending<=0;checksum_verified<=0;
            image_valid<=0;word_section<=0;word_index<=0;word_data<=0;
        end else begin
            write_pending<=0;
            if(abort_load) begin
                image_valid<=0;checksum_verified<=0;magic_index<=0;reply(7,0);
            end else if((state==HEADER || state==PAYLOAD || state==CHECKSUM) &&
                        !rx_valid && idle_cycles==TCW'(TIMEOUT_CYCLES-1)) begin
                image_valid<=0;checksum_verified<=0;magic_index<=0;reply(6,0);
            end else begin
                if(rx_valid) idle_cycles<=0;
                else if(state!=REPLY && (state!=SEARCH || magic_index!=0)) idle_cycles<=idle_cycles+1'b1;
                else idle_cycles<=0;
                case(state)
                    SEARCH: begin
                        if(rx_valid) begin
                            if(rx_data==magic_byte(magic_index)) begin
                                if(magic_index==3) begin
                                    state<=HEADER;magic_index<=0;header_index<=0;header_data<=0;
                                    nonce<=0;crc<=32'hffffffff;image_valid<=0;checksum_verified<=0;
                                    cursor<=0;section<=0;byte_index<=0;words_sent<=0;
                                end else magic_index<=magic_index+1'b1;
                            end else magic_index<=rx_data==8'h57 ? 2'd1 : 2'd0;
                        end else if(idle_cycles==TCW'(TIMEOUT_CYCLES-1)) begin
                            magic_index<=0;idle_cycles<=0;
                        end
                    end
                    HEADER: if(rx_valid) begin
                        header_data<=header_next;crc<=crc32_byte(crc,rx_data);
                        if(header_index==28) begin
                            nonce<=header_next[71:8];
                            if(header_next[7:0]!=1) reply(2,0);
                            else if(PROFILE_TAG==0 || header_next[199:72]!=PROFILE_TAG) reply(3,0);
                            else if(header_next[231:200]!=PAYLOAD_BYTES) reply(4,0);
                            else reply(0,0);
                        end else header_index<=header_index+1'b1;
                    end
                    REPLY: if(tx_ready) begin
                        if(reply_index>=4 && reply_index<18) reply_crc<=crc16_byte(reply_crc,tx_data);
                        if(reply_index==19) begin
                            if(reply_status==0) state<=PAYLOAD;
                            else begin
                                state<=SEARCH;magic_index<=0;
                                if(reply_status==1) image_valid<=1;
                            end
                        end else reply_index<=reply_index+1'b1;
                    end
                    PAYLOAD: if(rx_valid) begin
                        word_data[byte_index*8+:8]<=rx_data;crc<=crc32_byte(crc,rx_data);
                        if(32'(byte_index)+1==section_bytes(section)) begin
                            write_pending<=1;word_section<=section;word_index<=cursor;
                            words_sent<=words_sent+1'b1;byte_index<=0;
                            if(cursor+1==section_words(section)) begin
                                cursor<=0;
                                if(section==4) begin state<=CHECKSUM;checksum_index<=0;received_crc<=0;end
                                else section<=section+1'b1;
                            end else cursor<=cursor+1'b1;
                        end else byte_index<=byte_index+1'b1;
                    end
                    CHECKSUM: if(rx_valid) begin
                        received_crc<=checksum_next;
                        if(checksum_index==3) begin
                            if(checksum_next==~crc && words_sent==TOTAL_WORDS) begin
                                checksum_verified<=1;reply(1,~crc);
                            end else reply(5,~crc);
                        end else checksum_index<=checksum_index+1'b1;
                    end
                    default: begin image_valid<=0;checksum_verified<=0;magic_index<=0;reply(7,0);end
                endcase
            end
        end
    end

`ifdef WASMETAL_ASSERTIONS
    always_ff @(posedge clk) if(!reset) begin
        if(word_valid) begin
            assert(!image_valid && word_section<5);
            assert(word_index<section_words(word_section));
        end
        if(image_valid) assert(checksum_verified && words_sent==TOTAL_WORDS && state==SEARCH);
        if(state==PAYLOAD) begin
            assert(section<5 && cursor<section_words(section));
            assert(32'(byte_index)<section_bytes(section));
        end
        assert(words_sent<=TOTAL_WORDS);
    end
`endif
endmodule
