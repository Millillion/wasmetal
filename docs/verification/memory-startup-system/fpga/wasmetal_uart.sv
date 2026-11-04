// SPDX-License-Identifier: MIT
module wasmetal_uart #(parameter integer BIT_TICKS=25) (
    input logic clk, reset, rx,
    output logic tx,
    input logic tx_valid,
    input logic [7:0] tx_data,
    output logic tx_ready,
    output logic rx_valid, rx_error,
    output logic [7:0] rx_data
);
    localparam integer CW=$clog2(BIT_TICKS);
    (* async_reg="true" *) logic [1:0] rx_sync;
    logic [1:0] rx_state;
    logic [CW-1:0] rx_count, tx_count;
    logic [2:0] rx_bit;
    logic [7:0] rx_shift;
    logic tx_busy;
    logic [9:0] tx_shift;
    logic [3:0] tx_left;
    assign tx_ready=!tx_busy;
    assign tx=tx_busy ? tx_shift[0] : 1'b1;
    always_ff @(posedge clk) begin
        if(reset) begin
            rx_sync<=3; rx_state<=0; rx_count<=0; rx_bit<=0; rx_shift<=0;
            rx_valid<=0; rx_error<=0; rx_data<=0;
            tx_busy<=0; tx_shift<=10'h3ff; tx_left<=0; tx_count<=0;
        end else begin
            rx_sync<={rx_sync[0],rx}; rx_valid<=0; rx_error<=0;
            if(rx_state==0) begin
                if(!rx_sync[1]) begin rx_state<=1; rx_count<=CW'(BIT_TICKS/2-1); end
            end else if(rx_count!=0) rx_count<=rx_count-1'b1;
            else case(rx_state)
                1: begin
                    if(rx_sync[1]) rx_state<=0;
                    else begin rx_state<=2; rx_bit<=0; rx_count<=CW'(BIT_TICKS-1); end
                end
                2: begin
                    rx_shift[rx_bit]<=rx_sync[1]; rx_count<=CW'(BIT_TICKS-1);
                    if(rx_bit==7) rx_state<=3; else rx_bit<=rx_bit+1'b1;
                end
                3: begin
                    rx_state<=0;
                    if(rx_sync[1]) begin rx_data<=rx_shift; rx_valid<=1; end
                    else rx_error<=1;
                end
                default: rx_state<=0;
            endcase
            if(!tx_busy) begin
                if(tx_valid) begin
                    tx_shift<={1'b1,tx_data,1'b0}; tx_busy<=1; tx_left<=10;
                    tx_count<=CW'(BIT_TICKS-1);
                end
            end else if(tx_count!=0) tx_count<=tx_count-1'b1;
            else if(tx_left==1) tx_busy<=0;
            else begin
                tx_shift<={1'b1,tx_shift[9:1]}; tx_left<=tx_left-1'b1; tx_count<=CW'(BIT_TICKS-1);
            end
        end
    end
endmodule
