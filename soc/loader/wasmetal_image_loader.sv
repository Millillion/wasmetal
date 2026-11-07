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
    // Version 1 sends every row. Version 2 first sends five 32-bit row counts
    // and only those rows; after a verified checksum the loader writes zeros
    // to every remaining row, so each accepted upload still writes all rows.
    typedef enum logic [2:0] {SEARCH,HEADER,REPLY,PAYLOAD,CHECKSUM,COUNTS,FILL} state_t;
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
    logic write_pending, checksum_verified, compact;
    logic [31:0] limits [0:4];
    logic [31:0] declared_bytes, verified_crc;
    logic [4:0] counts_index;
    logic [159:0] counts_data;
    wire [159:0] counts_next={rx_data,counts_data[159:8]};
    function automatic [31:0] limit(input [2:0] which);
        limit=which<5 ? (compact ? limits[which] : section_words(which)) : 32'b0;
    endfunction
    // The first section at or after `which` that carries payload rows (5: none).
    function automatic [2:0] first_section(input [2:0] which,input [159:0] counts);
        if(which<=0 && counts[31:0]!=0) first_section=0;
        else if(which<=1 && counts[63:32]!=0) first_section=1;
        else if(which<=2 && counts[95:64]!=0) first_section=2;
        else if(which<=3 && counts[127:96]!=0) first_section=3;
        else if(which<=4 && counts[159:128]!=0) first_section=4;
        else first_section=5;
    endfunction
    wire [159:0] limit_vector={limits[4],limits[3],limits[2],limits[1],limits[0]};
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
            byte_index<=0;idle_cycles<=0;write_pending<=0;checksum_verified<=0;compact<=0;
            declared_bytes<=0;verified_crc<=0;counts_index<=0;counts_data<=0;
            for(integer n=0;n<5;n=n+1) limits[n]<=0;
            image_valid<=0;word_section<=0;word_index<=0;word_data<=0;
        end else begin
            write_pending<=0;
            if(abort_load) begin
                image_valid<=0;checksum_verified<=0;magic_index<=0;reply(7,0);
            end else if((state==HEADER || state==COUNTS || state==PAYLOAD || state==CHECKSUM) &&
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
                                    cursor<=0;section<=0;byte_index<=0;words_sent<=0;compact<=0;
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
                            compact<=header_next[7:0]==2; declared_bytes<=header_next[231:200];
                            if(header_next[7:0]!=1 && header_next[7:0]!=2) reply(2,0);
                            else if(PROFILE_TAG==0 || header_next[199:72]!=PROFILE_TAG) reply(3,0);
                            else if(header_next[7:0]==1 ? header_next[231:200]!=PAYLOAD_BYTES :
                                    (header_next[231:200]<20 || header_next[231:200]>PAYLOAD_BYTES+20)) reply(4,0);
                            else reply(0,0);
                        end else header_index<=header_index+1'b1;
                    end
                    REPLY: if(tx_ready) begin
                        if(reply_index>=4 && reply_index<18) reply_crc<=crc16_byte(reply_crc,tx_data);
                        if(reply_index==19) begin
                            if(reply_status==0) begin
                                if(compact) begin state<=COUNTS;counts_index<=0;counts_data<=0;end
                                else state<=PAYLOAD;
                            end
                            else begin
                                state<=SEARCH;magic_index<=0;
                                if(reply_status==1) image_valid<=1;
                            end
                        end else reply_index<=reply_index+1'b1;
                    end
                    COUNTS: if(rx_valid) begin
                        counts_data<=counts_next;crc<=crc32_byte(crc,rx_data);
                        if(counts_index==19) begin
                            for(integer n=0;n<5;n=n+1) limits[n]<=counts_next[n*32+:32];
                            if(counts_next[31:0]>INSTRUCTION_DEPTH || counts_next[63:32]>FUNCTION_DEPTH ||
                               counts_next[95:64]>TYPE_DEPTH || counts_next[127:96]>6*REGIONS_PER_KIND ||
                               counts_next[159:128]>BOOT_DEPTH ||
                               declared_bytes!=20+36*counts_next[31:0]+20*counts_next[63:32]+
                                   ((TYPE_DEPTH+7)/8)*counts_next[95:64]+8*counts_next[127:96]+
                                   29*counts_next[159:128]) begin
                                image_valid<=0;checksum_verified<=0;magic_index<=0;reply(4,0);
                            end else begin
                                state<=PAYLOAD;cursor<=0;byte_index<=0;section<=0;
                                // A section with no rows is skipped.
                                if(first_section(0,counts_next)==5) begin state<=CHECKSUM;checksum_index<=0;received_crc<=0;end
                                else section<=first_section(0,counts_next);
                            end
                        end else counts_index<=counts_index+1'b1;
                    end
                    PAYLOAD: if(rx_valid) begin
                        word_data[byte_index*8+:8]<=rx_data;crc<=crc32_byte(crc,rx_data);
                        if(32'(byte_index)+1==section_bytes(section)) begin
                            write_pending<=1;word_section<=section;word_index<=cursor;
                            words_sent<=words_sent+1'b1;byte_index<=0;
                            if(cursor+1==limit(section)) begin
                                cursor<=0;
                                if(!compact || first_section(section+1'b1,limit_vector)==5) begin
                                    if(!compact && section!=4) section<=section+1'b1;
                                    else begin state<=CHECKSUM;checksum_index<=0;received_crc<=0;end
                                end else section<=first_section(section+1'b1,limit_vector);
                            end else cursor<=cursor+1'b1;
                        end else byte_index<=byte_index+1'b1;
                    end
                    CHECKSUM: if(rx_valid) begin
                        received_crc<=checksum_next;
                        if(checksum_index==3) begin
                            if(checksum_next==~crc && compact) begin
                                // Clear every row the compact payload omitted.
                                verified_crc<=~crc;state<=FILL;section<=0;cursor<=limits[0];
                            end else if(checksum_next==~crc && words_sent==TOTAL_WORDS) begin
                                checksum_verified<=1;reply(1,~crc);
                            end else reply(5,~crc);
                        end else checksum_index<=checksum_index+1'b1;
                    end
                    FILL: begin
                        if(section==5) begin
                            if(words_sent==TOTAL_WORDS) begin checksum_verified<=1;reply(1,verified_crc);end
                            else reply(5,verified_crc);
                        end else if(cursor>=section_words(section)) begin
                            section<=section+1'b1;cursor<=section==4 ? 32'b0 : limits[section+1'b1];
                        end else begin
                            write_pending<=1;word_section<=section;word_index<=cursor;word_data<=0;
                            words_sent<=words_sent+1'b1;cursor<=cursor+1'b1;
                        end
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
            assert(section<5 && cursor<limit(section) && limit(section)<=section_words(section));
            assert(32'(byte_index)<section_bytes(section));
        end
        assert(words_sent<=TOTAL_WORDS);
    end
`endif
endmodule
