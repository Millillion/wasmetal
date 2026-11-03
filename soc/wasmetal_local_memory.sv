// SPDX-License-Identifier: MIT
// One bounded byte RAM serves all six core memory spaces. Whole-transaction
// checks precede every write; a response is held for one complete clock cycle.
module wasmetal_local_memory #(
    parameter integer RAM_BYTES=131072,
    parameter integer REGIONS_PER_KIND=16,
    parameter IMAGE_DIR="build/standalone-image"
) (
    input logic clk, reset,
    output wire initialized,
    input logic valid, write, initialize,
    input logic [2:0] kind,
    input logic [31:0] index,
    input logic [63:0] address,
    input logic [4:0] bytes,
    input logic [127:0] wdata,
    output wire ready,
    output logic fault,
    output logic [127:0] rdata
);
    localparam integer AW=$clog2(RAM_BYTES), IW=$clog2(REGIONS_PER_KIND);
    (* ram_style="block" *) logic [7:0] storage [0:RAM_BYTES-1];
    (* rom_style="block" *) logic [63:0] regions [0:6*REGIONS_PER_KIND-1];
    initial $readmemh({IMAGE_DIR,"/regions.hex"},regions);
    typedef enum logic [2:0] {CLEAR,IDLE,CHECK,READ_BYTE,CAPTURE,WRITE_BYTE,RESPONSE} state_t;
    state_t state;
    logic [AW-1:0] clear_index, location;
    logic [4:0] position, length;
    logic [63:0] offset, region;
    logic [2:0] saved_kind;
    logic saved_write, saved_initialize, valid_region;
    logic [127:0] payload;
    logic [7:0] read_byte;
    wire [AW-1:0] ram_address=state==CLEAR ? clear_index : location+AW'(position);
    wire value_slots=saved_kind==1 || saved_kind==2 || saved_kind==4 || saved_kind==5;
    wire [68:0] relative_address=value_slots ? {1'b0,offset,4'b0} : {5'b0,offset};
    wire [68:0] end_address=relative_address+{64'b0,length};
    wire [68:0] physical_end={37'b0,region[31:0]}+end_address;
    wire normal_valid=valid_region && length!=0 && length<=16 &&
        (!value_slots || length==16) && end_address<={37'b0,region[63:32]} &&
        physical_end<=69'(RAM_BYTES) && !(saved_write && (saved_kind==3 || saved_kind==4));
    wire init_valid=saved_write && length!=0 && length<=16 &&
        ({5'b0,offset}+{64'b0,length})<=69'(RAM_BYTES);
    assign initialized=state!=CLEAR;
    assign ready=state==RESPONSE;

    always_ff @(posedge clk) begin
        region<=regions[(kind<6 && index<REGIONS_PER_KIND) ?
                        (32'(kind)*REGIONS_PER_KIND+32'(index[IW-1:0])) : 0];
        read_byte<=storage[ram_address];
        if(!reset) begin
            if(state==CLEAR) storage[ram_address]<=0;
            else if(state==WRITE_BYTE) storage[ram_address]<=payload[position*8+:8];
        end
    end

    always_ff @(posedge clk) begin
        if(reset) begin
            state<=CLEAR; clear_index<=0; location<=0; position<=0; length<=0;
            offset<=0; saved_kind<=0; saved_write<=0; saved_initialize<=0;
            valid_region<=0; payload<=0; fault<=0; rdata<=0;
        end else case(state)
            CLEAR: begin
                if(clear_index==AW'(RAM_BYTES-1)) state<=IDLE;
                else clear_index<=clear_index+1'b1;
            end
            IDLE: if(valid) begin
                saved_kind<=kind; saved_write<=write; saved_initialize<=initialize;
                valid_region<=kind<6 && index<REGIONS_PER_KIND;
                offset<=address; length<=bytes; payload<=wdata;
                position<=0; fault<=0; rdata<=0; state<=CHECK;
            end
            CHECK: begin
                if(!(saved_initialize ? init_valid : normal_valid)) begin
                    fault<=1; state<=RESPONSE;
                end else begin
                    location<=saved_initialize ? offset[AW-1:0] :
                              AW'(region[31:0])+relative_address[AW-1:0];
                    state<=saved_write ? WRITE_BYTE : READ_BYTE;
                end
            end
            READ_BYTE: state<=CAPTURE;
            CAPTURE: begin
                rdata[position*8+:8]<=read_byte;
                if(position+5'd1==length) state<=RESPONSE;
                else begin position<=position+1'b1; state<=READ_BYTE; end
            end
            WRITE_BYTE: begin
                if(position+5'd1==length) state<=RESPONSE;
                else position<=position+1'b1;
            end
            RESPONSE: state<=IDLE;
            default: begin state<=CLEAR; clear_index<=0; end
        endcase
    end

`ifdef WASMETAL_ASSERTIONS
    always_ff @(posedge clk) if(!reset) begin
        if(state!=CLEAR && state!=IDLE) assert(valid);
        if(state==WRITE_BYTE || state==READ_BYTE || state==CAPTURE) begin
            assert(position<length && length<=16);
            assert(saved_initialize ? init_valid : normal_valid);
        end
    end
`endif
endmodule
