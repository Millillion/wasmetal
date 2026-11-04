// SPDX-License-Identifier: MIT
// Trusted prepared-image boot. No host clock stepping or memory service.
module wasmetal_standalone #(
    parameter integer VALUE_DEPTH=8192, CONTROL_DEPTH=2048, CALL_DEPTH=512,
    parameter integer MEMORY_COUNT=256, HEAP_SLOTS=1024,
    parameter integer INSTRUCTION_DEPTH=1024, FUNCTION_DEPTH=128, TYPE_DEPTH=64,
    parameter integer BOOT_DEPTH=512, REGIONS_PER_KIND=16, RAM_BYTES=131072,
    parameter integer MAX_RESULTS=16, WATCHDOG_CYCLES=10000000,
    parameter integer UART_TICKS=81,
    parameter integer LOADABLE=0, EXTERNAL_UART=0,
    parameter IMAGE_DIR="build/standalone-image"
) (
    input logic clk, reset,
    output wire tx, finished, error,
    input wire image_write_valid,
    input wire [2:0] image_section,
    input wire [31:0] image_index,
    input wire [(TYPE_DEPTH>288 ? TYPE_DEPTH : 288)-1:0] image_word,
    output wire result_valid,
    output wire [7:0] result_byte,
    input wire result_ready
);
    localparam integer CW=$clog2(INSTRUCTION_DEPTH), FW=$clog2(FUNCTION_DEPTH),
                       TW=$clog2(TYPE_DEPTH), BW=$clog2(BOOT_DEPTH),
                       UW=$clog2(12+16*MAX_RESULTS);
    (* rom_style="block" *) logic [287:0] instructions [0:INSTRUCTION_DEPTH-1];
    (* rom_style="block" *) logic [159:0] functions [0:FUNCTION_DEPTH-1];
    logic [TYPE_DEPTH-1:0] types [0:TYPE_DEPTH-1];
    (* rom_style="block" *) logic [231:0] boot [0:BOOT_DEPTH-1];
    generate if(LOADABLE==0) begin: read_only_image
    initial begin
        $readmemh({IMAGE_DIR,"/code.hex"},instructions);
        $readmemh({IMAGE_DIR,"/functions.hex"},functions);
        $readmemh({IMAGE_DIR,"/types.hex"},types);
        $readmemh({IMAGE_DIR,"/boot.hex"},boot);
    end
    end else begin: writable_image
        // A loader may write only while the execution system is held in reset.
        // All rows must be supplied before that reset can be released.
        always_ff @(posedge clk) if(reset && image_write_valid) case(image_section)
            0: if(image_index<INSTRUCTION_DEPTH) instructions[image_index[CW-1:0]]<=image_word[287:0];
            1: if(image_index<FUNCTION_DEPTH) functions[image_index[FW-1:0]]<=image_word[159:0];
            2: if(image_index<TYPE_DEPTH) types[image_index[TW-1:0]]<=image_word[TYPE_DEPTH-1:0];
            4: if(image_index<BOOT_DEPTH) boot[image_index[BW-1:0]]<=image_word[231:0];
            default: begin end
        endcase
    end endgenerate
    logic [287:0] instruction;
    logic [159:0] function_data;
    logic [231:0] boot_record;
    logic [31:0] boot_index, code_count, function_count, boot_count;
    wire [3:0] mode=boot_record[231:228], command=boot_record[227:224];
    wire [31:0] record_index=boot_record[223:192];
    wire [63:0] record_aux=boot_record[191:128];
    wire [127:0] record_data=boot_record[127:0];
    typedef enum logic [3:0] {WAIT_CLEAR,HEADER,FETCH,ISSUE,DRAIN,RUN,ADVANCE,SEND,HALT} state_t;
    state_t state;
    logic final_seen, halted_core;
    logic [7:0] status, reported_trap, count;
    logic [31:0] run_cycles;
    logic [UW-1:0] tx_index;
    logic [15:0] crc;
    wire [UW-1:0] payload_end=UW'(9)+UW'(count)*UW'(16);
    wire tx_ready;
    logic [7:0] tx_data;
    wire busy, done;
    wire [7:0] trap;
    wire [31:0] result_count, pc, function_index, type_actual, type_expected;
    wire [127:0] result_data;
    wire [31:0] result_index=tx_index>=10 ? (32'(tx_index)-32'd10)>>4 : 32'b0;
    wire mem_valid, mem_write, mem_ready, mem_fault, memory_initialized, memory_failed;
    wire [2:0] mem_kind;
    wire [31:0] mem_index;
    wire [63:0] mem_address;
    wire [4:0] mem_bytes;
    wire [127:0] mem_wdata, mem_rdata;
    wire initializing=state==ISSUE && mode==2;
    wire command_valid=state==ISSUE && (mode==1 || mode==3) && command<=5 &&
        (!final_seen) && (mode!=3 || command==0);
    wire core_reset=reset || !memory_initialized || halted_core;
    wire type_matches=type_actual<TYPE_DEPTH && type_expected<TYPE_DEPTH &&
                     types[type_actual[TW-1:0]][type_expected[TW-1:0]];
    assign finished=state==HALT && tx_ready;
    assign error=status!=0;
    assign result_valid=state==SEND;
    assign result_byte=tx_data;

    always_ff @(negedge clk) begin
        instruction<=instructions[pc[CW-1:0]];
        function_data<=functions[function_index[FW-1:0]];
        boot_record<=boot[boot_index[BW-1:0]];
    end

`ifdef WASMETAL_MAPPED_CORE
    wasmetal_core core(
`else
    wasmetal_core #(.VALUE_DEPTH(VALUE_DEPTH),.CONTROL_DEPTH(CONTROL_DEPTH),
        .CALL_DEPTH(CALL_DEPTH),.MEMORY_COUNT(MEMORY_COUNT),.HEAP_SLOTS(HEAP_SLOTS)) core(
`endif
        .clk(clk),.reset(core_reset),.cmd_valid(command_valid),.cmd_kind(command),
        .cmd_index(record_index),.cmd_data(record_data),.cmd_aux(record_aux),
        .busy(busy),.done(done),.trap(trap),.result_count(result_count),
        .result_index(result_index),.result_data(result_data),.pc(pc),
        .insn_op(instruction[31:0]),.insn_x(instruction[63:32]),.insn_y(instruction[95:64]),
        .insn_z(instruction[127:96]),.insn_w(instruction[159:128]),.insn_imm(instruction[287:160]),
        .insn_valid(pc<code_count),.function_index(function_index),
        .function_entry(function_data[31:0]),.function_params(function_data[63:32]),
        .function_locals(function_data[95:64]),.function_results(function_data[127:96]),
        .function_type(function_data[159:128]),.function_valid(function_index<function_count),
        .type_actual(type_actual),.type_expected(type_expected),.type_matches(type_matches),
        .mem_valid(mem_valid),.mem_write(mem_write),.mem_kind(mem_kind),.mem_index(mem_index),
        .mem_address(mem_address),.mem_bytes(mem_bytes),.mem_wdata(mem_wdata),
        .mem_ready(mem_ready && !initializing),.mem_fault(mem_fault),.mem_rdata(mem_rdata));

    wasmetal_local_memory #(.RAM_BYTES(RAM_BYTES),.REGIONS_PER_KIND(REGIONS_PER_KIND),.LOADABLE(LOADABLE),
        .IMAGE_DIR(IMAGE_DIR)) memory(
        .clk(clk),.reset(reset || halted_core),.initialized(memory_initialized),
        .initialization_failed(memory_failed),
        .valid(initializing || mem_valid),.write(initializing || mem_write),.initialize(initializing),
        .kind(mem_kind),.index(mem_index),
        .address(initializing ? {32'b0,record_index} : mem_address),
        .bytes(initializing ? record_aux[4:0] : mem_bytes),
        .wdata(initializing ? record_data : mem_wdata),
        .ready(mem_ready),.fault(mem_fault),.rdata(mem_rdata),
        .image_write_valid(image_write_valid && image_section==3),
        .image_index(image_index),.image_region(image_word[63:0]));

    generate if(EXTERNAL_UART==0) begin: internal_uart
    wire ignored_rx_valid,ignored_rx_error;
    wire [7:0] ignored_rx_data;
    wasmetal_uart #(.BIT_TICKS(UART_TICKS)) uart(
        .clk(clk),.reset(reset),.rx(1'b1),.tx(tx),.tx_valid(state==SEND),
        .tx_data(tx_data),.tx_ready(tx_ready),.rx_valid(ignored_rx_valid),
        .rx_error(ignored_rx_error),.rx_data(ignored_rx_data));
    end else begin: external_uart
        assign tx=1'b1;
        assign tx_ready=result_ready;
    end endgenerate

    function automatic [15:0] crc_byte(input [15:0] previous,input [7:0] data);
        reg [15:0] value;
        begin
            value=previous^{data,8'b0};
            for(integer i=0;i<8;i=i+1) value=value[15] ? (value<<1)^16'h1021 : value<<1;
            crc_byte=value;
        end
    endfunction
    always_comb begin
        tx_data=0;
        case(tx_index)
            0: tx_data=8'h57;
            1: tx_data=8'h4d;
            2: tx_data=1;
            3: tx_data=status;
            4: tx_data=reported_trap;
            5: tx_data=count;
            6,7,8,9: tx_data=run_cycles[(tx_index-6)*8+:8];
            default: begin
                if(tx_index<=payload_end) tx_data=result_data[((tx_index-10)%16)*8+:8];
                else if(tx_index==payload_end+UW'(1)) tx_data=crc[7:0];
                else tx_data=crc[15:8];
            end
        endcase
    end

    task automatic finish_error(input [7:0] reason,input [7:0] code);
        begin
            status<=reason; reported_trap<=code; count<=0;
            halted_core<=1; tx_index<=0; crc<=16'hffff; state<=SEND;
        end
    endtask
    always_ff @(posedge clk) begin
        if(reset) begin
            state<=WAIT_CLEAR; boot_index<=0; code_count<=0; function_count<=0; boot_count<=0;
            final_seen<=0; halted_core<=0; status<=0; reported_trap<=0; count<=0;
            run_cycles<=0; tx_index<=0; crc<=16'hffff;
        end else case(state)
            WAIT_CLEAR: begin
                if(memory_failed) finish_error(5,0);
                else if(memory_initialized) state<=HEADER;
            end
            HEADER: begin
                if(mode!=15 || boot_record[227:128]!=0 || record_data[31:0]!=32'h574d5301 ||
                   record_data[63:32]==0 || record_data[63:32]>INSTRUCTION_DEPTH ||
                   record_data[95:64]==0 || record_data[95:64]>FUNCTION_DEPTH ||
                   record_data[127:96]<3 || record_data[127:96]>BOOT_DEPTH) finish_error(2,254);
                else begin
                    code_count<=record_data[63:32]; function_count<=record_data[95:64];
                    boot_count<=record_data[127:96]; boot_index<=1; state<=FETCH;
                end
            end
            FETCH: if(boot_index>=boot_count) finish_error(2,254); else state<=ISSUE;
            ISSUE: begin
                if(final_seen && mode!=0) finish_error(2,254);
                else case(mode)
                    0: begin
                        if(!final_seen || boot_record!=0 || boot_index+1!=boot_count ||
                           result_count>MAX_RESULTS) finish_error(2,254);
                        else begin count<=8'(result_count); state<=SEND; tx_index<=0; crc<=16'hffff; end
                    end
                    1,3: begin
                        if(command>5 || (mode==3 && command!=0) || busy ||
                           (command==1 && record_index>=VALUE_DEPTH) ||
                           (command>=2 && record_index>=MEMORY_COUNT)) finish_error(2,254);
                        else if(command==0) begin
                            final_seen<=mode==3; run_cycles<=1; state<=RUN;
                        end else state<=DRAIN;
                    end
                    2: begin
                        if(command!=0 || record_aux==0 || record_aux>16) finish_error(2,254);
                        else if(mem_ready) begin
                            if(mem_fault) finish_error(2,254); else state<=ADVANCE;
                        end
                    end
                    default: finish_error(2,254);
                endcase
            end
            DRAIN: state<=ADVANCE;
            RUN: begin
                if(done) begin
                    if(trap!=0) finish_error(final_seen ? 8'd1 : 8'd4,trap);
                    else state<=ADVANCE;
                end else if(run_cycles>=WATCHDOG_CYCLES) finish_error(3,0);
                else run_cycles<=run_cycles+1'b1;
            end
            ADVANCE: begin boot_index<=boot_index+1'b1; state<=FETCH; end
            SEND: if(tx_ready) begin
                if(tx_index>=2 && tx_index<=payload_end) crc<=crc_byte(crc,tx_data);
                if(tx_index==payload_end+UW'(2)) state<=HALT;
                else tx_index<=tx_index+1'b1;
            end
            HALT: begin end
            default: finish_error(2,254);
        endcase
    end

`ifdef WASMETAL_ASSERTIONS
    always_ff @(posedge clk) if(!reset && !halted_core) begin
        if(initializing) assert(!busy);
        if(command_valid) assert(!busy);
        if(state==SEND && status==0) assert(done && !busy && trap==0);
    end
`endif
endmodule
