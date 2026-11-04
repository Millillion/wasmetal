// SPDX-License-Identifier: MIT
module startup_four_state_tb;
    reg clk=0,reset=1,cpu_valid=1,cpu_write=1;
    reg [31:0] cpu_address=0;
    reg [15:0] cpu_mask=16'h8081;
    reg [127:0] cpu_wdata='1;
    wire cpu_ready,cpu_fault,cpu_enabled,test_busy,test_done,test_failed;
    wire [127:0] cpu_rdata,expected_data,observed_data;
    wire [1:0] error_code;
    wire [31:0] error_address,memory_address;
    wire [63:0] completed_operations;
    wire memory_valid,memory_write;
    wire [15:0] memory_mask;
    wire [127:0] memory_wdata;
    reg memory_ready=0,memory_fault=0;
    reg [127:0] memory_rdata='x,storage='x,read_q='x;
    reg pending=0,release_request=0,write_q=0;
    integer mode=0,commands=0,cpu_commands=0,n;
    wasmetal_memory_startup #(.RAM_BYTES(16),.RESPONSE_TIMEOUT(32)) dut(.*);
    always #5 clk=~clk;
    always @(posedge clk) begin
        if(reset)begin memory_ready<=0;pending<=0;release_request<=0;end
        else if(memory_ready)memory_ready<=0;
        else if(release_request)begin if(!memory_valid)release_request<=0;end
        else if(pending)begin
            pending<=0;memory_ready<=1;release_request<=1;
            if(write_q)memory_rdata<='x;
            else if(mode==1)memory_rdata<={read_q[127:1],1'bx};
            else if(mode==2)memory_rdata<={read_q[127:1],1'bz};
            else memory_rdata<=read_q;
        end else if(memory_valid)begin
            if(memory_address!==0 || memory_mask===0)$fatal(1,"startup invalid backend request");
            if(!cpu_enabled && memory_mask!==16'hffff)$fatal(1,"startup incomplete test mask");
            commands<=commands+1;pending<=1;write_q<=memory_write;read_q<=storage;
            if(cpu_enabled)cpu_commands<=cpu_commands+1;
            if(memory_write)for(n=0;n<16;n=n+1)if(memory_mask[n])storage[n*8+:8]<=memory_wdata[n*8+:8];
        end
    end
    task isolation;
        begin
            if(reset && (cpu_enabled!==0 || memory_valid!==0 || memory_write!==0 || cpu_ready!==0 || cpu_fault!==0))
                $fatal(1,"startup reset retained CPU ownership");
            if(!cpu_enabled && (cpu_ready!==0 || cpu_fault!==0 || cpu_rdata!==128'b0))
                $fatal(1,"startup leaked test response to CPU");
        end
    endtask
    task cycle;begin @(posedge clk);#1;isolation();end endtask
    task restart(input integer injection);
        begin
            @(negedge clk);reset=1;#1;isolation();cycle();cycle();
            @(negedge clk);mode=injection;reset=0;
        end
    endtask
    task finish(input integer injection);
        integer budget,before_commands,before_cpu;
        begin
            budget=1000;before_cpu=cpu_commands;
            while(test_done!==1 && budget>0)begin cycle();budget=budget-1;end
            if(budget==0)$fatal(1,"startup four-state completion timed out");
            if(test_busy!==0)$fatal(1,"startup completed while test was busy");
            if(injection==0)begin
                if(cpu_enabled!==1 || test_failed!==0 || completed_operations!==80 || storage!==128'b0)
                    $fatal(1,"startup healthy unknown-start memory failed");
                budget=20;
                while(cpu_ready!==1 && budget>0)begin cycle();budget=budget-1;end
                if(budget==0 || cpu_fault!==0 || cpu_commands!==before_cpu+1 || storage!==128'hff00000000000000ff000000000000ff)
                    $fatal(1,"startup queued CPU write did not execute once");
                before_commands=commands;
                repeat(5)begin cycle();if(commands!==before_commands || cpu_ready!==0)$fatal(1,"startup repeated queued CPU write");end
            end else begin
                if(cpu_enabled!==0 || test_failed!==1 || error_code!==1 || completed_operations!==2 ||
                    error_address!==0 || expected_data!==128'haaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa)
                    $fatal(1,"startup unknown memory granted CPU");
                if(injection==1 && observed_data[0]!==1'bx)$fatal(1,"startup lost X observation");
                if(injection==2 && observed_data[0]!==1'bz)$fatal(1,"startup lost Z observation");
                before_commands=commands;
                repeat(8)begin cycle();if(cpu_enabled!==0 || commands!==before_commands || cpu_commands!==before_cpu)
                    $fatal(1,"startup failed memory accepted queued CPU write");end
            end
        end
    endtask
    initial begin
        #1;isolation();restart(0);finish(0);restart(1);finish(1);restart(2);finish(2);
        restart(0);repeat(3)cycle();restart(0);finish(0);
        $display("PASS startup four-state unknown memory, X/Z rejection, queued CPU handoff and reset recovery; commands=%0d cpu_commands=%0d",commands,cpu_commands);
        $finish;
    end
endmodule
