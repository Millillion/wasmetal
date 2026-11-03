// SPDX-License-Identifier: MIT
// Simulation-only backend binding. The CPU uses the production CDC and AXI
// adapters; the AXI slave below is a behavioral byte-masked RAM, not a DDR PHY.
module wasmetal_bram #(
    parameter integer RAM_BYTES=131072
) (
    input wire clk, reset, valid, write,
    input wire [31:0] address,
    input wire [15:0] mask,
    input wire [127:0] wdata,
    output wire ready, fault,
    output wire [127:0] rdata
);
    localparam integer DIVIDER=`WASMETAL_TEST_AXI_DIVIDER,
        LATENCY=`WASMETAL_TEST_AXI_LATENCY, WORDS=RAM_BYTES/16;
    // Free-running, slower test clock with edges offset from CPU rising edges.
    // These clocks are related; independent-clock component tests are separate.
    logic axi_clk=0;
    integer phase=0;
    always @(negedge clk) begin
        if(phase==DIVIDER-1) begin phase<=0;axi_clk<=!axi_clk;end
        else phase<=phase+1;
    end
    wire axi_reset,online,source_reset;
    wire awvalid,wvalid,arvalid,bready,rready,awready,wready,arready;
    logic bvalid,rvalid;
    wire [31:0] awaddr,araddr;
    wire [3:0] awid,arid,awcache,arcache,awqos,arqos;
    wire [7:0] awlen,arlen;
    wire [2:0] awsize,arsize,awprot,arprot;
    wire [1:0] awburst,arburst;
    wire awlock,arlock,wlast;
    wire [127:0] write_data;
    wire [15:0] wstrb;
    logic [127:0] response_data;
`ifdef WASMETAL_TEST_CORRUPT_AXI
    wire [127:0] read_data=response_data^128'h1;
`else
    wire [127:0] read_data=response_data;
`endif
    wasmetal_async_axi_memory adapter(.bid(4'b0),.rid(4'b0),.bresp(2'b0),
        .rresp(2'b0),.rlast(1'b1),.*);

    logic [127:0] memory [0:WORDS-1];
    logic have_aw,have_w,have_ar;
    logic [31:0] saved_aw,saved_ar;
    logic [127:0] saved_data;
    logic [15:0] saved_mask;
    integer delay_left;
    longint unsigned writes=0,reads=0,aw_first=0,w_first=0,resets=0,ticks=0;
    // Alternate which write channel can arrive first, with unrelated stalls on
    // each channel. Neither accepting AW nor accepting W implies accepting both.
    assign awready=!axi_reset && !have_aw && !bvalid && ticks%3!=0 &&
        (writes[0]==0 || have_w);
    assign wready=!axi_reset && !have_w && !bvalid && ticks%5!=0 &&
        (writes[0]==1 || have_aw);
    assign arready=!axi_reset && !have_ar && !rvalid && ticks%7!=0;
    initial begin
        for(integer word=0;word<WORDS;word=word+1)
            memory[word]=128'hd1b54a32d192ed039e3779b97f4a7c15^128'(word);
    end
    always @(posedge axi_reset) resets<=resets+1;
    always @(posedge axi_clk) ticks<=ticks+1;
    // Reset cancels outstanding bus transfers on both sides of the interface,
    // while the memory contents deliberately survive every reset.
    always @(posedge axi_clk or posedge axi_reset) begin
        if(axi_reset) begin
            have_aw<=0;have_w<=0;have_ar<=0;bvalid<=0;rvalid<=0;
            saved_aw<=0;saved_ar<=0;saved_data<=0;saved_mask<=0;
            response_data<=0;delay_left<=0;
        end else begin
            if(awvalid && awready) begin
                assert(awaddr[3:0]==0 && {1'b0,awaddr}+33'd16<=33'(RAM_BYTES));
                assert(awid==0 && awlen==0 && awsize==4 && awburst==1 &&
                    !awlock && awcache==0 && awprot==0 && awqos==0);
                saved_aw<=awaddr;have_aw<=1;
                if(!have_w) aw_first<=aw_first+1;
            end
            if(wvalid && wready) begin
                assert(wlast && wstrb!=0);
                saved_data<=write_data;saved_mask<=wstrb;have_w<=1;
                if(!have_aw) w_first<=w_first+1;
            end
            if(have_aw && have_w && !bvalid) begin
                for(integer lane=0;lane<16;lane=lane+1)
                    if(saved_mask[lane]) memory[saved_aw/16][lane*8+:8]<=saved_data[lane*8+:8];
                have_aw<=0;have_w<=0;bvalid<=1;writes<=writes+1;
            end
            if(bvalid && bready) bvalid<=0;
            if(arvalid && arready) begin
                assert(araddr[3:0]==0 && {1'b0,araddr}+33'd16<=33'(RAM_BYTES));
                assert(arid==0 && arlen==0 && arsize==4 && arburst==1 &&
                    !arlock && arcache==0 && arprot==0 && arqos==0);
                saved_ar<=araddr;have_ar<=1;delay_left<=LATENCY+integer'(araddr[5:4]);
            end
            if(have_ar) begin
                if(delay_left!=0) delay_left<=delay_left-1;
                else begin
                    response_data<=memory[saved_ar/16];rvalid<=1;have_ar<=0;reads<=reads+1;
                end
            end
            if(rvalid && rready) rvalid<=0;
        end
    end
    final begin
        integer file;
        file=$fopen(`WASMETAL_TEST_AXI_COVERAGE,"a");
        if(file==0) $fatal(1,"could not write AXI system coverage");
        $fdisplay(file,"{\"writes\":%0d,\"reads\":%0d,\"aw_first\":%0d,\"w_first\":%0d,\"resets\":%0d}",
            writes,reads,aw_first,w_first,resets);
        $fclose(file);
    end
endmodule
