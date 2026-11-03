// SPDX-License-Identifier: MIT
module wasmetal_loadable_ulx3s #(
    parameter logic [127:0] PROFILE_TAG=0
) (
    input wire clk_25mhz, btn_n, ftdi_txd,
    output wire ftdi_rxd, led_busy, led_error
);
    // Same free-running 781.25 kHz clock and 9600-baud setting as standalone.
    logic [4:0] divider=0;
    always_ff @(posedge clk_25mhz) divider<=divider+1'b1;
    (* keep *) wire core_clock;
`ifdef SYNTHESIS
    DCCA core_clock_buffer(.CLKI(divider[4]),.CE(1'b1),.CLKO(core_clock));
`else
    assign core_clock=divider[4];
`endif
    (* ASYNC_REG="TRUE", async_reg="true" *) logic [1:0] reset_sync=0;
    always_ff @(posedge core_clock or negedge btn_n)
        if(!btn_n) reset_sync<=0;
        else reset_sync<={reset_sync[0],1'b1};
    wire finished,ignored_image_valid;
    wasmetal_loadable #(.PROFILE_TAG(PROFILE_TAG),
`include "standalone_parameters.svh"
    ) system(.clk(core_clock),.reset(!reset_sync[1]),.rx(ftdi_txd),
        .tx(ftdi_rxd),.finished(finished),.error(led_error),.image_valid(ignored_image_valid));
    assign led_busy=!finished;
endmodule
