// SPDX-License-Identifier: MIT
// Serial prepared-image loading, autonomous execution and serial results.
module wasmetal_loadable #(
    parameter integer VALUE_DEPTH=8192, CONTROL_DEPTH=2048, CALL_DEPTH=512,
    parameter integer MEMORY_COUNT=256, HEAP_SLOTS=1024,
    parameter integer INSTRUCTION_DEPTH=1024, FUNCTION_DEPTH=128, TYPE_DEPTH=64,
    parameter integer BOOT_DEPTH=512, REGIONS_PER_KIND=16, RAM_BYTES=131072,
    parameter integer MAX_RESULTS=16, WATCHDOG_CYCLES=10000000,
    parameter integer UART_TICKS=81, UPLOAD_TIMEOUT_CYCLES=2000000,
    parameter logic [127:0] PROFILE_TAG=0
) (
    input wire clk, reset, rx,
    output wire tx, finished, error, image_valid
);
    localparam integer WORD_WIDTH=TYPE_DEPTH>288 ? TYPE_DEPTH : 288;
    wire rx_valid,rx_error,tx_ready,loader_tx_valid,result_valid,word_valid,system_finished,system_error;
    wire [7:0] rx_data,loader_tx_data,result_byte;
    wire [2:0] word_section;
    wire [31:0] word_index;
    wire [WORD_WIDTH-1:0] word_data;
    wire ignored_tx;
    assign finished=image_valid && system_finished;
    assign error=image_valid && system_error;
    wasmetal_uart #(.BIT_TICKS(UART_TICKS)) serial(
        .clk(clk),.reset(reset),.rx(rx),.tx(tx),
        .tx_valid(loader_tx_valid || (image_valid && result_valid)),
        .tx_data(loader_tx_valid ? loader_tx_data : result_byte),.tx_ready(tx_ready),
        .rx_valid(rx_valid),.rx_error(rx_error),.rx_data(rx_data));
    wasmetal_image_loader #(.INSTRUCTION_DEPTH(INSTRUCTION_DEPTH),.FUNCTION_DEPTH(FUNCTION_DEPTH),
        .TYPE_DEPTH(TYPE_DEPTH),.BOOT_DEPTH(BOOT_DEPTH),.REGIONS_PER_KIND(REGIONS_PER_KIND),
        .TIMEOUT_CYCLES(UPLOAD_TIMEOUT_CYCLES),.PROFILE_TAG(PROFILE_TAG)) loader(
        .clk(clk),.reset(reset),.abort_load(rx_error),.rx_valid(rx_valid),.rx_data(rx_data),
        .tx_valid(loader_tx_valid),.tx_data(loader_tx_data),.tx_ready(tx_ready),
        .image_valid(image_valid),.word_valid(word_valid),.word_section(word_section),
        .word_index(word_index),.word_data(word_data));
    wasmetal_standalone #(.VALUE_DEPTH(VALUE_DEPTH),.CONTROL_DEPTH(CONTROL_DEPTH),.CALL_DEPTH(CALL_DEPTH),
        .MEMORY_COUNT(MEMORY_COUNT),.HEAP_SLOTS(HEAP_SLOTS),.INSTRUCTION_DEPTH(INSTRUCTION_DEPTH),
        .FUNCTION_DEPTH(FUNCTION_DEPTH),.TYPE_DEPTH(TYPE_DEPTH),.BOOT_DEPTH(BOOT_DEPTH),
        .REGIONS_PER_KIND(REGIONS_PER_KIND),.RAM_BYTES(RAM_BYTES),.MAX_RESULTS(MAX_RESULTS),
        .WATCHDOG_CYCLES(WATCHDOG_CYCLES),.LOADABLE(1),.EXTERNAL_UART(1)) execution(
        .clk(clk),.reset(reset || !image_valid),.tx(ignored_tx),.finished(system_finished),.error(system_error),
        .image_write_valid(word_valid),.image_section(word_section),.image_index(word_index),.image_word(word_data),
        .result_valid(result_valid),.result_byte(result_byte),
        .result_ready(tx_ready && !loader_tx_valid && image_valid));
endmodule
