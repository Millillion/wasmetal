// SPDX-License-Identifier: MIT
`timescale 1ns/1ps
module sky130_sram_tb #(
    parameter integer RAM_BYTES=16384,
    parameter integer READ_LATENCY=3,
    parameter integer MODEL_DELAY=3,
    parameter integer MODEL_HOLD=1,
    parameter integer MASK_LIMIT=65535
);
    localparam integer WORDS=RAM_BYTES/16, ADDRESS_WIDTH=$clog2(WORDS);
    logic clk=0,reset=1,valid=0,write=0;
    logic [31:0] address=0;
    logic [15:0] mask=0;
    logic [127:0] wdata=0;
    wire ready,fault,sram_enable,sram_write;
    wire [127:0] rdata,sram_wdata,sram_rdata;
    wire [ADDRESS_WIDTH-1:0] sram_address;
    wire [15:0] sram_byte_enable;
    logic [127:0] oracle[0:WORDS-1];
    integer transactions=0,commands=0,resets=0;
    wasmetal_sram_memory #(.RAM_BYTES(RAM_BYTES),.READ_LATENCY(READ_LATENCY)) adapter(.*);
    wasmetal_sky130_sram #(.RAM_BYTES(RAM_BYTES),.MODEL_DELAY(MODEL_DELAY),.MODEL_HOLD(MODEL_HOLD)) storage(
        .clk(clk),.reset(reset),.enable(sram_enable),.write(sram_write),
        .address(sram_address),.byte_enable(sram_byte_enable),.wdata(sram_wdata),.rdata(sram_rdata));
    always #10 clk=~clk;
    always @(posedge clk) if(sram_enable)commands++;
    initial begin #100000000;$fatal(1,"macro test watchdog");end
    task step;begin @(posedge clk);#2;end endtask
    function automatic [127:0] pattern(input integer a,input integer seed);
        for(integer b=0;b<16;b++) pattern[b*8+:8]=8'((a*73)^(seed*31)^(b*19)^(a>>8));
    endfunction
    task request(input bit wr,input logic[31:0] addr,input logic[15:0] lanes,input logic[127:0] value);
        integer age,before_commands,index;
        bit legal;
        begin
            @(negedge clk);#2;
            write=wr;address=addr;mask=lanes;wdata=value;valid=1;
            before_commands=commands;age=0;
            do begin step();age++;if(age>READ_LATENCY+8)$fatal(1,"no bounded response");end while(ready!==1);
            legal=addr<RAM_BYTES && addr%16==0 && lanes!=0;
            if(age!=(legal ? (wr ? 2 : READ_LATENCY+2) : 1))$fatal(1,"incorrect response timing");
            if(fault!==!legal)$fatal(1,"unexpected fault addr=%h",addr);
            if(commands-before_commands!=(legal?1:0))$fatal(1,"wrong number of macro commands");
            if(!legal || wr)begin
                if(rdata!==128'b0)$fatal(1,"write/fault data not zero");
            end else if(rdata!==oracle[addr/16])$fatal(1,"read differs addr=%h got=%h want=%h",addr,rdata,oracle[addr/16]);
            if(legal && wr)begin
                index=addr/16;
                for(integer b=0;b<16;b++)if(lanes[b])oracle[index][b*8+:8]=value[b*8+:8];
            end
            // Held-valid requests must not be issued twice.
            step();step();if(ready!==0 || sram_enable!==0 || commands-before_commands!=(legal?1:0))$fatal(1,"held request repeated");
            valid=0;step();step();transactions++;
        end
    endtask
    task reset_controller;
        begin @(negedge clk);#2;reset=1;valid=0;step();step();reset=0;step();resets++;end
    endtask
    initial begin
        step();step();reset=0;step();
`ifndef VERILATOR
        request(0,0,16'hffff,0);
        if((^oracle[0])!==1'bx)$fatal(1,"oracle unexpectedly initialized");
`endif
        for(integer i=0;i<WORDS;i++)request(1,32'(i*16),16'hffff,pattern(i,1));
        for(integer i=0;i<WORDS;i++)request(0,32'(i*16),16'hffff,0);
        // Exhaust every nonzero byte mask while cycling through the banks.
        for(integer i=1;i<=MASK_LIMIT;i++)begin
            request(1,32'(((i*97)%WORDS)*16),16'(i),pattern(i,2));
            request(0,32'(((i*97)%WORDS)*16),16'hffff,0);
        end
        request(0,0,0,0);request(1,1,16'hffff,'1);
        request(0,32'(RAM_BYTES),16'hffff,0);request(1,32'hfffffff0,16'hffff,'1);
        reset_controller();
        for(integer i=0;i<WORDS;i++)request(0,32'(i*16),16'hffff,0);
        // Interrupt a read after the macro command; reset must discard its response.
        @(negedge clk);#2;valid=1;write=0;address=0;mask=16'hffff;
        step();step();reset_controller();
        for(integer i=0;i<READ_LATENCY+3;i++)begin step();if(ready!==0)$fatal(1,"stale post-reset read response");end
        request(0,0,16'hffff,0);
        $display("PASS vendor SRAM adapter bytes=%0d latency=%0d masks=%0d transactions=%0d commands=%0d resets=%0d",RAM_BYTES,READ_LATENCY,MASK_LIMIT,transactions,commands,resets);
        $finish;
    end
endmodule
