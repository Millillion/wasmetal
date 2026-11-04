// SPDX-License-Identifier: MIT
module sdram_four_state;
    reg clk=0;always #5 clk=~clk;
    reg reset=1,bus_reset=0,valid=0,write=0;
    reg [31:0] address=0;
    reg [15:0] mask=16'hffff,dq_in=16'h4ea1;
    reg [127:0] wdata=0;
    wire initialized,ready,fault,cke,cs,ras,cas,we,oe;
    wire [127:0] rdata;
    wire [12:0] sd_address;
    wire [1:0] bank,dqm;
    wire [15:0] dq_out;
    integer writes=0,activations=0,checks=0;
    wasmetal_sdram_memory #(.RAM_BYTES(128),.ROW_BITS(1),.COLUMN_BITS(3),
        .POWERUP_CYCLES(2),.REFRESH_CYCLES(100)) dut(
        .clk(clk),.reset(reset),.bus_reset(bus_reset),.valid(valid),.write(write),
        .address(address),.mask(mask),.wdata(wdata),.initialized(initialized),
        .ready(ready),.fault(fault),.rdata(rdata),.sdram_cke(cke),.sdram_cs_n(cs),
        .sdram_ras_n(ras),.sdram_cas_n(cas),.sdram_we_n(we),
        .sdram_address(sd_address),.sdram_bank(bank),.sdram_dqm(dqm),
        .sdram_dq_out(dq_out),.sdram_dq_oe(oe),.sdram_dq_in(dq_in));
    always @(posedge clk) if(!reset) begin
        if((^{cke,cs,ras,cas,we,dqm,oe})===1'bx)$fatal(1,"unknown SDRAM pin control");
        if({cs,ras,cas,we}===4'b0011)activations=activations+1;
        if({cs,ras,cas,we}===4'b0100)writes=writes+1;
    end

    task automatic transfer(input reg direction,input reg [31:0] location,
        input reg [15:0] byte_mask,input reg [127:0] data,input reg error_expected);
        integer elapsed,old_writes,old_activations;
        begin
            @(negedge clk);
            old_writes=writes;old_activations=activations;
            valid=1;write=direction;address=location;mask=byte_mask;wdata=data;
            elapsed=0;
            while(ready!==1'b1)begin
                @(negedge clk);elapsed=elapsed+1;
                if(elapsed>150)$fatal(1,"four-state transaction timed out");
            end
            if(fault!==error_expected)$fatal(1,"four-state request did not fail closed");
            if(error_expected) begin
                if(writes!=old_writes || activations!=old_activations)$fatal(1,"invalid request reached SDRAM");
                if(rdata!==128'b0)$fatal(1,"invalid request returned data");
            end else if(direction===1'b0)begin
                if(rdata!=={8{dq_in}})$fatal(1,"read did not preserve four-state data");
            end
            @(negedge clk);valid=0;
            repeat(3)@(negedge clk);
            checks=checks+1;
        end
    endtask

    task automatic unknown_control(input reg unknown_value,input reg warm);
        integer old_writes,old_activations;
        begin
            @(negedge clk);
            old_writes=writes;old_activations=activations;
            write=1;address=0;mask=16'hffff;wdata=128'h102030405060708090a0b0c0d0e0f001;
            valid=warm ? 1'b1 : unknown_value;
            bus_reset=warm ? unknown_value : 1'b0;
            repeat(60) begin
                @(negedge clk);
                if(ready!==1'b0 || writes!=old_writes || activations!=old_activations)begin
                    if(warm)$fatal(1,"unknown warm reset accepted a request");
                    else $fatal(1,"unknown valid accepted a request");
                end
            end
            valid=0;bus_reset=1;
            repeat(3)@(negedge clk);
            bus_reset=0;
            repeat(3)@(negedge clk);
            checks=checks+1;
        end
    endtask

    reg [127:0] altered_data;
    reg [31:0] altered_address;
    reg [15:0] altered_mask;
    integer bit_number;
    initial begin
        repeat(3)@(negedge clk);reset=0;
        wait(initialized===1'b1);
        transfer(1,0,16'hffff,128'h123456789abcdef00102030405060708,0);
        transfer(1,0,0,0,1);
        transfer(1'bx,0,16'hffff,0,1);transfer(1'bz,0,16'hffff,0,1);
        for(bit_number=0;bit_number<128;bit_number=bit_number+1) begin
            altered_data=0;altered_data[bit_number]=1'bx;
            transfer(1,0,16'hffff,altered_data,1);
            altered_data[bit_number]=1'bz;transfer(1,0,16'hffff,altered_data,1);
        end
        for(bit_number=0;bit_number<32;bit_number=bit_number+1) begin
            altered_address=0;altered_address[bit_number]=1'bx;
            transfer(1,altered_address,16'hffff,0,1);
            altered_address[bit_number]=1'bz;transfer(1,altered_address,16'hffff,0,1);
        end
        for(bit_number=0;bit_number<16;bit_number=bit_number+1) begin
            altered_mask=16'hffff;altered_mask[bit_number]=1'bx;
            transfer(1,0,altered_mask,0,1);
            altered_mask[bit_number]=1'bz;transfer(1,0,altered_mask,0,1);
        end
        transfer(0,0,16'hffff,0,0);
        dq_in=16'hxxxx;transfer(0,0,16'hffff,0,0);
        dq_in=16'hzzzz;transfer(0,0,16'hffff,0,0);
        dq_in=16'b1x0z_0101_zx10_1010;transfer(0,0,16'hffff,0,0);
        dq_in=16'h4ea1;transfer(0,0,16'hffff,128'hxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx,0);
        unknown_control(1'bx,0);unknown_control(1'bz,0);
        unknown_control(1'bx,1);unknown_control(1'bz,1);
        transfer(1,0,16'hffff,128'h123456789abcdef00102030405060708,0);
        $display("PASS %0d SDRAM four-state checks",checks);$finish;
    end
endmodule
