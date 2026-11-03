// SPDX-License-Identifier: MIT
module sram_four_state_tb;
    reg clk=0,reset=1,valid=1'bx,write=1'bx;
    reg [31:0] address='x;
    reg [15:0] mask='x;
    reg [127:0] wdata='x,sram_rdata='x;
    wire ready,fault,sram_enable,sram_write;
    wire [127:0] rdata,sram_wdata;
    wire [2:0] sram_address;
    wire [15:0] sram_byte_enable;
    wasmetal_sram_memory #(.RAM_BYTES(80),.READ_LATENCY(2)) dut(.*);
    always #5 clk=~clk;
    initial begin #5000;$fatal(1,"SRAM four-state test timed out");end
    task step;begin @(posedge clk);#1;end endtask
    task release_request;begin
        valid=0;step();step();step();
        if(ready!==0 || sram_enable!==0)$fatal(1,"request did not release");
    end endtask
    initial begin
        #1;
        if(sram_enable!==0 || sram_write!==0)$fatal(1,"reset did not block unknown-state macro strobes");
        step();step();
        if((^{ready,fault,rdata,sram_address,sram_byte_enable,sram_wdata})===1'bx)
            $fatal(1,"reset left unknown controller outputs");
        valid=0;reset=0;step();
        address=0;mask=16'hffff;write=1;wdata=128'hfedcba98765432100123456789abcdef;valid=1;
        step();
        if(sram_enable!==1 || sram_write!==1 || sram_wdata!==wdata)$fatal(1,"write command mismatch");
        step();if(ready!==1 || fault!==0 || rdata!==0)$fatal(1,"write response depends on unknown SRAM data");
        release_request();
        write=0;valid=1;sram_rdata='x;
        step();step();step();step();
        if(ready!==1 || fault!==0)$fatal(1,"read did not complete at fixed latency");
        if((^rdata)!==1'bx)$fatal(1,"unknown SRAM data was coerced to a known value");
        release_request();
        // A later known read must recover without retaining unknown output bits.
        sram_rdata=128'h123456789abcdef001122334455667788;valid=1;
        step();step();step();step();
        if(ready!==1 || fault!==0 || rdata!==sram_rdata)$fatal(1,"known read failed after unknown data");
        release_request();
        // An invalid address cannot issue a macro command or leak unknown data.
        address=80;valid=1;sram_rdata='x;step();
        if(ready!==1 || fault!==1 || rdata!==0 || sram_enable!==0)$fatal(1,"invalid read reached macro or leaked data");
        reset=1;valid='x;step();
        if(ready!==0 || sram_enable!==0 || rdata!==0)$fatal(1,"reset did not clear response state");
        $display("PASS SRAM four-state reset and read-data propagation");$finish;
    end
endmodule
