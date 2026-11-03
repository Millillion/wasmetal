// SPDX-License-Identifier: MIT
// One outstanding, aligned 128-bit AXI4 transfer. AW and W are independent.
// All ports share clk. Reset must also reset the connected AXI interface;
// resetting only this master cannot cancel an already accepted AXI transfer.
module wasmetal_axi_memory #(
    parameter logic [31:0] BASE_ADDRESS=0,
    parameter integer ID_WIDTH=4
) (
    input wire clk, reset, valid, write,
    input wire [31:0] address,
    input wire [15:0] mask,
    input wire [127:0] wdata,
    output wire ready,
    output logic fault,
    output logic [127:0] rdata,
    output wire awvalid, wvalid, arvalid, bready, rready,
    input wire awready, wready, arready, bvalid, rvalid,
    output wire [31:0] awaddr, araddr,
    output wire [ID_WIDTH-1:0] awid, arid,
    input wire [ID_WIDTH-1:0] bid, rid,
    output wire [7:0] awlen, arlen,
    output wire [2:0] awsize, arsize, awprot, arprot,
    output wire [1:0] awburst, arburst,
    output wire awlock, arlock,
    output wire [3:0] awcache, arcache, awqos, arqos,
    output wire [127:0] write_data,
    output wire [15:0] wstrb,
    output wire wlast,
    input wire [127:0] read_data,
    input wire [1:0] bresp, rresp,
    input wire rlast
);
    typedef enum logic [2:0] {IDLE,WRITE,READ,RESPONSE,RELEASE} state_t;
    state_t state;
    logic [31:0] address_q;
    logic [15:0] mask_q;
    logic [127:0] data_q;
    logic aw_sent, w_sent, ar_sent, poisoned;
    wire [32:0] translated={1'b0,BASE_ADDRESS}+{1'b0,address};
    wire legal=mask!=0 && address[3:0]==0 && BASE_ADDRESS[3:0]==0 && translated<=33'h0_fffffff0;
    assign ready=state==RESPONSE;
    assign awvalid=state==WRITE && !aw_sent && !reset;
    assign wvalid=state==WRITE && !w_sent && !reset;
    assign bready=state==WRITE && aw_sent && w_sent && !reset;
    assign arvalid=state==READ && !ar_sent && !reset;
    assign rready=state==READ && ar_sent && !reset;
    assign awaddr=address_q;
    assign araddr=address_q;
    assign write_data=data_q;
    assign wstrb=mask_q;
    assign wlast=1;
    assign awid=0;
    assign arid=0;
    assign awlen=0;
    assign arlen=0;
    assign awsize=4;
    assign arsize=4;
    assign awburst=1;
    assign arburst=1;
    assign awlock=0;
    assign arlock=0;
    assign awcache=0;
    assign arcache=0;
    assign awprot=0;
    assign arprot=0;
    assign awqos=0;
    assign arqos=0;

    always_ff @(posedge clk) begin
        if(reset) begin
            state<=IDLE;address_q<=0;mask_q<=0;data_q<=0;
            aw_sent<=0;w_sent<=0;ar_sent<=0;poisoned<=0;fault<=0;rdata<=0;
        end else case(state)
            IDLE: if(valid) begin
                address_q<=translated[31:0];mask_q<=mask;data_q<=wdata;
                aw_sent<=0;w_sent<=0;ar_sent<=0;fault<=0;rdata<=0;
                if(!legal || poisoned) begin fault<=1;state<=RESPONSE;end
                else state<=write ? WRITE : READ;
            end
            WRITE: begin
                if(awvalid && awready) aw_sent<=1;
                if(wvalid && wready) w_sent<=1;
                if(bready && bvalid) begin
                    if(bresp!=0 || bid!=0) begin fault<=1;poisoned<=1;end
                    state<=RESPONSE;
                end
            end
            READ: begin
                if(arvalid && arready) ar_sent<=1;
                if(rready && rvalid) begin
                    if(rresp!=0 || rid!=0 || !rlast) begin fault<=1;poisoned<=1;end
                    else rdata<=read_data;
                    state<=RESPONSE;
                end
            end
            RESPONSE: state<=RELEASE;
            RELEASE: if(!valid) state<=IDLE;
            default: begin fault<=1;poisoned<=1;state<=RESPONSE;end
        endcase
    end

`ifdef WASMETAL_ASSERTIONS
    logic held_aw, held_w, held_ar;
    logic [31:0] prior_address;
    logic [143:0] prior_write;
    always_ff @(posedge clk) begin
        if(reset) begin held_aw<=0;held_w<=0;held_ar<=0;prior_address<=0;prior_write<=0;end
        else begin
            if(held_aw) assert(awvalid && awaddr==prior_address);
            if(held_w) assert(wvalid && {wstrb,write_data}==prior_write);
            if(held_ar) assert(arvalid && araddr==prior_address);
            if(awvalid || wvalid || arvalid) assert(address_q[3:0]==0 && mask_q!=0);
            if(state==WRITE || state==READ) assert(!poisoned && address_q[3:0]==0 && mask_q!=0);
            if(state==WRITE) assert(awvalid==!aw_sent && wvalid==!w_sent);
            if(state==READ) assert(arvalid==!ar_sent);
            if(bready) assert(aw_sent && w_sent);
            if(rready) assert(ar_sent);
            if(poisoned) assert(!awvalid && !wvalid && !arvalid && !bready && !rready);
            assert(!(arvalid && (awvalid || wvalid)));
            held_aw<=awvalid && !awready;held_w<=wvalid && !wready;held_ar<=arvalid && !arready;
            prior_address<=address_q;prior_write<={wstrb,write_data};
        end
    end
`endif
endmodule
