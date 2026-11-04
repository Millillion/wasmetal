// SPDX-License-Identifier: MIT
// Logical Wasm regions to a synchronous 128-bit physical memory interface.
// The backend completes a held request with bus_ready and optionally bus_fault.
// After a timeout/fault no further requests are issued until reset: a late
// completion must never be mistaken for a different transaction.
module wasmetal_memory_bridge #(
    parameter integer RAM_BYTES=131072, REGIONS_PER_KIND=16,
    parameter integer TIMEOUT_CYCLES=1024
) (
    input wire clk, reset,
    output wire initialized,
    output logic initialization_failed,
    input wire valid, write, initialize,
    input wire [2:0] kind,
    input wire [31:0] index,
    input wire [63:0] address,
    input wire [4:0] bytes,
    input wire [127:0] wdata,
    // Synchronous region lookup: available in the cycle after request capture.
    input wire [63:0] region,
    output wire ready,
    output logic fault,
    output logic [127:0] rdata,
    output wire bus_valid, bus_write,
    output wire [31:0] bus_address,
    output wire [15:0] bus_mask,
    output wire [127:0] bus_wdata,
    input wire bus_ready, bus_fault,
    input wire [127:0] bus_rdata
);
    typedef enum logic [3:0] {CLEAR_ACCESS,CLEAR_GAP,IDLE,CHECK,ACCESS,GAP,RESPONSE,FAILED} state_t;
    state_t state;
    logic [31:0] location, clear_address, wait_cycles;
    logic [4:0] position, length;
    logic [63:0] offset;
    logic [2:0] saved_kind;
    logic saved_write, saved_initialize, valid_region, poisoned;
    logic [127:0] payload;
    wire value_slots=saved_kind==1 || saved_kind==2 || saved_kind==4 || saved_kind==5;
    wire [68:0] relative_address=value_slots ? {1'b0,offset,4'b0} : {5'b0,offset};
    wire [68:0] end_address=relative_address+{64'b0,length};
    wire [68:0] physical_end={37'b0,region[31:0]}+end_address;
    wire normal_valid=valid_region && length!=0 && length<=16 &&
        (!value_slots || length==16) && end_address<={37'b0,region[63:32]} &&
        physical_end<=69'(RAM_BYTES) && !(saved_write && (saved_kind==3 || saved_kind==4));
    wire init_valid=saved_write && length!=0 && length<=16 &&
        ({5'b0,offset}+{64'b0,length})<=69'(RAM_BYTES);
    wire clearing=state==CLEAR_ACCESS || state==CLEAR_GAP;
    wire [4:0] beat_bytes;
    wire [15:0] write_mask;
    wire [127:0] write_value, read_value;
    wasmetal_memory_lanes lanes(.position(position),.length(length),.offset(location[3:0]),
        .payload(payload),.memory_data(bus_rdata),.count(beat_bytes),.mask(write_mask),
        .write_data(write_value),.read_data(read_value));
    assign initialized=!clearing && state!=FAILED;
    assign ready=state==RESPONSE;
    assign bus_valid=(state==CLEAR_ACCESS || state==ACCESS) && !reset;
    assign bus_write=clearing || saved_write;
    assign bus_address=clearing ? clear_address : {location[31:4],4'b0};

    assign bus_mask=clearing ? 16'hffff : write_mask;
    assign bus_wdata=clearing ? 128'b0 : write_value;

    always_ff @(posedge clk) begin
        if(reset) begin
            state<=CLEAR_ACCESS; clear_address<=0; location<=0; wait_cycles<=0;
            initialization_failed<=0; poisoned<=0; position<=0; length<=0;
            offset<=0; saved_kind<=0; saved_write<=0; saved_initialize<=0;
            valid_region<=0; payload<=0; fault<=0; rdata<=0;
        end else case(state)
            CLEAR_ACCESS: begin
                if(bus_ready) begin
                    wait_cycles<=0;
                    if(bus_fault) begin initialization_failed<=1; poisoned<=1; state<=FAILED; end
                    else state<=CLEAR_GAP;
                end else if(wait_cycles==32'(TIMEOUT_CYCLES-1)) begin
                    initialization_failed<=1; poisoned<=1; state<=FAILED;
                end else wait_cycles<=wait_cycles+1'b1;
            end
            CLEAR_GAP: begin
                if(clear_address==32'(RAM_BYTES-16)) state<=IDLE;
                else begin clear_address<=clear_address+16; state<=CLEAR_ACCESS; end
            end
            IDLE: if(valid) begin
                saved_kind<=kind; saved_write<=write; saved_initialize<=initialize;
                valid_region<=kind<6 && index<REGIONS_PER_KIND;
                offset<=address; length<=bytes; payload<=wdata;
                position<=0; fault<=0; rdata<=0; wait_cycles<=0;
                if(poisoned) begin fault<=1; state<=RESPONSE; end
                else state<=CHECK;
            end
            CHECK: begin
                if(!(saved_initialize ? init_valid : normal_valid)) begin fault<=1; state<=RESPONSE; end
                else begin
                    location<=saved_initialize ? offset[31:0] : region[31:0]+relative_address[31:0];
                    state<=ACCESS;
                end
            end
            ACCESS: begin
                if(bus_ready) begin
                    wait_cycles<=0;
                    if(bus_fault) begin fault<=1; poisoned<=1; rdata<=0; state<=RESPONSE; end
                    else begin
                        if(!saved_write) rdata<=rdata | read_value;
                        if(position+beat_bytes==length) state<=RESPONSE;
                        else begin
                            position<=position+beat_bytes; location<=location+32'(beat_bytes); state<=GAP;
                        end
                    end
                end else if(wait_cycles==32'(TIMEOUT_CYCLES-1)) begin
                    fault<=1; poisoned<=1; rdata<=0; state<=RESPONSE;
                end else wait_cycles<=wait_cycles+1'b1;
            end
            GAP: state<=ACCESS;
            RESPONSE: state<=IDLE;
            FAILED: begin end
            default: begin initialization_failed<=1; poisoned<=1; state<=FAILED; end
        endcase
    end

`ifdef WASMETAL_ASSERTIONS
    logic prior_valid, prior_ready, prior_timeout;
    logic [176:0] prior_request;
    always_ff @(posedge clk) begin
        if(reset) begin prior_valid<=0; prior_ready<=0; prior_timeout<=0; prior_request<=0; end
        else begin
            if(prior_valid && !prior_ready && !prior_timeout) begin
                assert(bus_valid);
                assert({bus_write,bus_address,bus_mask,bus_wdata}==prior_request);
            end
            if(bus_valid) begin
                assert(bus_address[3:0]==0);
                assert({1'b0,bus_address}+33'd16<=33'(RAM_BYTES));
                assert(bus_mask!=0);
            end
            if(poisoned) assert(!bus_valid);
            if(clearing) begin
                assert(clear_address[3:0]==0);
                assert({1'b0,clear_address}+33'd16<=33'(RAM_BYTES));
            end
            if(state==ACCESS || state==CLEAR_ACCESS) assert(wait_cycles<32'(TIMEOUT_CYCLES));
            if(state==ACCESS || state==GAP) begin
                assert(position<length && length<=16 && beat_bytes!=0);
                assert({1'b0,location}+33'(length)-33'(position)<=33'(RAM_BYTES));
                if(position!=0) assert(location[3:0]==0);
            end
            prior_valid<=bus_valid; prior_ready<=bus_ready;
            prior_timeout<=wait_cycles==32'(TIMEOUT_CYCLES-1);
            prior_request<={bus_write,bus_address,bus_mask,bus_wdata};
        end
    end
`endif
endmodule
