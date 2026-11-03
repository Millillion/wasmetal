// SPDX-License-Identifier: MIT
module wasmetal_standalone_ulx3s (
    input logic clk_25mhz, btn_n,
    output wire ftdi_rxd, led_busy, led_error
);
    // 25 MHz / 32 = 781.25 kHz, with equal high and low phases. It never
    // stops during reset. UART uses 81 clocks/bit: 9645 baud (0.47% from 9600).
    logic [4:0] divider=0;
    always_ff @(posedge clk_25mhz) divider<=divider+1'b1;
    (* keep *) wire core_clock;
`ifdef SYNTHESIS
    DCCA core_clock_buffer(.CLKI(divider[4]),.CE(1'b1),.CLKO(core_clock));
`else
    assign core_clock=divider[4];
`endif
    // Asynchronous assertion, two-stage synchronous release. FPGA INIT values
    // also request reset after configuration when the button is not pressed.
    (* async_reg="true" *) logic [1:0] reset_sync=0;
    always_ff @(posedge core_clock or negedge btn_n) begin
        if(!btn_n) reset_sync<=0;
        else reset_sync<={reset_sync[0],1'b1};
    end
    wire finished;
    wasmetal_standalone #(
`include "standalone_parameters.svh"
    ) system(.clk(core_clock),.reset(!reset_sync[1]),
        .tx(ftdi_rxd),.finished(finished),.error(led_error));
    assign led_busy=!finished;
endmodule
