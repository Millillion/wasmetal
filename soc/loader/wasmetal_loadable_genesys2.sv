// SPDX-License-Identifier: MIT
module wasmetal_loadable_genesys2 #(
    parameter logic [127:0] PROFILE_TAG=0
) (
    input wire sysclk_p, sysclk_n, cpu_resetn, uart_tx_in,
    output wire uart_rx_out,
    output wire [1:0] led
);
    // 200 MHz / 256 gives the same free-running 781.25 kHz CPU clock and
    // 9600-baud UART setting as the verified ULX3S programmable system.
    wire board_clock;
`ifdef SYNTHESIS
    IBUFDS clock_input(.I(sysclk_p),.IB(sysclk_n),.O(board_clock));
`else
    assign board_clock=sysclk_p;
    wire ignored_clock_n=sysclk_n;
`endif
    logic [7:0] divider=0;
    always_ff @(posedge board_clock) divider<=divider+1'b1;
    (* keep *) wire core_clock;
`ifdef SYNTHESIS
    BUFG core_clock_buffer(.I(divider[7]),.O(core_clock));
`else
    assign core_clock=divider[7];
`endif
    (* ASYNC_REG="TRUE", async_reg="true" *) logic [1:0] reset_sync=0;
    always_ff @(posedge core_clock or negedge cpu_resetn)
        if(!cpu_resetn) reset_sync<=0;
        else reset_sync<={reset_sync[0],1'b1};
    wire finished,error,ignored_image_valid;
    wasmetal_loadable #(.PROFILE_TAG(PROFILE_TAG),
`include "standalone_parameters.svh"
    ) system(.clk(core_clock),.reset(!reset_sync[1]),.rx(uart_tx_in),
        .tx(uart_rx_out),.finished(finished),.error(error),.image_valid(ignored_image_valid));
    // LD0 lights while a program is loading or running; LD1 reports an error.
    assign led={error,!finished};
endmodule
