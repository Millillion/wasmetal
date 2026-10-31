// SPDX-License-Identifier: MIT
// Host-backed, single-step FPGA bring-up interface. Arithmetic executes in core.
module wasmetal_ulx3s #(parameter integer VALUE_DEPTH=256) (
    input logic clk_25mhz, btn_n, ftdi_txd,
    output logic ftdi_rxd, led_busy, led_error
);
    (* async_reg="true" *) logic [1:0] reset_sync=0;
    always_ff @(posedge clk_25mhz) reset_sync<={reset_sync[0],btn_n};
    wire reset_bridge=!reset_sync[1];
    logic cpu_pulse;
    (* keep *) wire core_clock;
`ifdef SYNTHESIS
    DCCA core_clock_buffer(.CLKI(cpu_pulse),.CE(1'b1),.CLKO(core_clock));
`else
    assign core_clock=cpu_pulse;
`endif
`include "core_ports.svh"
    logic [INPUT_BYTES*8-1:0] active_inputs, rx_payload;
    wire [OUTPUT_BYTES*8-1:0] outgoing_outputs;
    logic [OUTPUT_BYTES*8-1:0] response_payload;
    typedef enum logic [3:0] {SYNC0,SYNC1,FLAGS,SEQUENCE,PAYLOAD,CRC_LOW,CRC_HIGH,
                             SETTLE,HIGH_PULSE,LOW_PULSE,SNAPSHOT,SEND} state_t;
    state_t state;
    logic [7:0] flags, sequence_number, status, crc_low;
    logic [15:0] rx_crc, tx_crc;
    logic [7:0] payload_index, tx_index, settle_count;
    logic [20:0] receive_idle;
    wire rx_valid, rx_error, tx_ready;
    wire [7:0] rx_data;
    logic [7:0] tx_data;
    wire tx_valid=state==SEND;
    wasmetal_uart uart(.clk(clk_25mhz),.reset(reset_bridge),.rx(ftdi_txd),.tx(ftdi_rxd),
        .tx_valid(tx_valid),.tx_data(tx_data),.tx_ready(tx_ready),
        .rx_valid(rx_valid),.rx_error(rx_error),.rx_data(rx_data));
    assign led_busy=core_busy;

    function automatic [15:0] crc_byte(input [15:0] previous,input [7:0] data);
        reg [15:0] value;
        integer bit_index;
        begin
            value=previous^{data,8'b0};
            for(bit_index=0;bit_index<8;bit_index=bit_index+1)
                value=value[15] ? (value<<1)^16'h1021 : value<<1;
            crc_byte=value;
        end
    endfunction

    always_comb begin
        case(tx_index)
            0: tx_data=8'h57;
            1: tx_data=8'h52;
            2: tx_data=status;
            3: tx_data=sequence_number;
            8'(4+OUTPUT_BYTES): tx_data=tx_crc[7:0];
            8'(5+OUTPUT_BYTES): tx_data=tx_crc[15:8];
            default: tx_data=response_payload[(tx_index-4)*8+:8];
        endcase
    end

    always_ff @(posedge clk_25mhz) begin
        if(reset_bridge) begin
            state<=SYNC0; cpu_pulse<=0; active_inputs<=0; rx_payload<=0; response_payload<=0;
            flags<=0; sequence_number<=0; status<=0; crc_low<=0;
            rx_crc<=16'hffff; tx_crc<=16'hffff; payload_index<=0; tx_index<=0; settle_count<=0;
            led_error<=0;
            receive_idle<=0;
        end else begin
            if(rx_valid || state==SYNC0 || state>=SETTLE) receive_idle<=0;
            else receive_idle<=receive_idle+1'b1;
            if((rx_error || receive_idle==21'd1250000) && state<SETTLE) begin state<=SYNC0; led_error<=1; end
            else case(state)
                SYNC0: if(rx_valid && rx_data==8'h57) state<=SYNC1;
                SYNC1: if(rx_valid) begin
                    if(rx_data==8'h4d) begin state<=FLAGS; rx_crc<=16'hffff; end
                    else if(rx_data!=8'h57) state<=SYNC0;
                end
                FLAGS: if(rx_valid) begin flags<=rx_data; rx_crc<=crc_byte(rx_crc,rx_data); state<=SEQUENCE; end
                SEQUENCE: if(rx_valid) begin
                    sequence_number<=rx_data; rx_crc<=crc_byte(rx_crc,rx_data); payload_index<=0; state<=PAYLOAD;
                end
                PAYLOAD: if(rx_valid) begin
                    rx_payload<={rx_data,rx_payload[INPUT_BYTES*8-1:8]}; rx_crc<=crc_byte(rx_crc,rx_data);
                    if(payload_index==8'(INPUT_BYTES-1)) state<=CRC_LOW;
                    else payload_index<=payload_index+1'b1;
                end
                CRC_LOW: if(rx_valid) begin crc_low<=rx_data; state<=CRC_HIGH; end
                CRC_HIGH: if(rx_valid) begin
                    if({rx_data,crc_low}!=rx_crc || flags[7:2]!=0 || flags[1:0]==3) begin
                        status<=({rx_data,crc_low}!=rx_crc) ? 8'd1 : 8'd2;
                        response_payload<=0; tx_index<=0; tx_crc<=16'hffff; led_error<=1; state<=SEND;
                    end else if(flags[1]) begin
                        response_payload<=0;
                        response_payload[0+:32]<=32'h574d0001;
                        response_payload[32+:32]<=32'(VALUE_DEPTH);
                        response_payload[64+:32]<=32'd128;
                        response_payload[96+:32]<=32'd64;
                        response_payload[128+:32]<=32'd16;
                        response_payload[160+:32]<=32'(HEAP_CAPACITY);
                        response_payload[192+:32]<=32'(INPUT_BYTES);
                        response_payload[224+:32]<=32'(OUTPUT_BYTES);
                        response_payload[256+:32]<=SCHEMA_ID;
                        tx_index<=0; tx_crc<=16'hffff; status<=0; state<=SEND;
                    end else begin
                        active_inputs<=rx_payload; settle_count<=99; led_error<=0; state<=SETTLE;
                    end
                end
                SETTLE: begin
                    if(settle_count!=0) settle_count<=settle_count-1'b1;
                    else if(flags[0]) begin cpu_pulse<=1; settle_count<=24; state<=HIGH_PULSE; end
                    else state<=SNAPSHOT;
                end
                HIGH_PULSE: begin
                    if(settle_count!=0) settle_count<=settle_count-1'b1;
                    else begin cpu_pulse<=0; settle_count<=49; state<=LOW_PULSE; end
                end
                LOW_PULSE: begin
                    if(settle_count!=0) settle_count<=settle_count-1'b1;
                    else state<=SNAPSHOT;
                end
                SNAPSHOT: begin
                    response_payload<=outgoing_outputs; status<=0; tx_index<=0; tx_crc<=16'hffff; state<=SEND;
                end
                SEND: if(tx_ready) begin
                    if(tx_index>=2 && tx_index<8'(4+OUTPUT_BYTES)) tx_crc<=crc_byte(tx_crc,tx_data);
                    if(tx_index==8'(5+OUTPUT_BYTES)) state<=SYNC0;
                    else tx_index<=tx_index+1'b1;
                end
                default: state<=SYNC0;
            endcase
        end
    end
endmodule
