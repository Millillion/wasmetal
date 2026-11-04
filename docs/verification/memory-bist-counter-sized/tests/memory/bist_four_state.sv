module bist_four_state_tb;
    reg clk=0,reset=1,start=0;
    wire busy,done,failed,valid,write;
    wire [1:0] error_code;
    wire [31:0] address,error_address;
    wire [15:0] mask;
    wire [127:0] wdata,expected_data,observed_data;
    wire [63:0] completed_operations;
    reg ready=0,fault=0;
    reg [127:0] rdata='x,storage='x,read_q='x;
    reg pending=0,release_request=0,write_q=0;
    integer mode=0,commands=0;
    wasmetal_memory_bist #(.RAM_BYTES(16),.RESPONSE_TIMEOUT(32)) dut(.*);
    always #5 clk=~clk;
    always @(posedge clk) begin
        if(reset) begin ready<=0;pending<=0;release_request<=0;end
        else if(ready) ready<=0;
        else if(release_request) begin if(!valid) release_request<=0;end
        else if(pending) begin
            pending<=0;ready<=1;release_request<=1;
            if(write_q) rdata<='x;
            else if(mode==1) rdata<={read_q[127:1],1'bx};
            else if(mode==2) rdata<={read_q[127:1],1'bz};
            else rdata<=read_q;
        end else if(valid) begin
            if(address!==0 || mask!==16'hffff)$fatal(1,"BIST invalid memory request");
            commands<=commands+1;pending<=1;write_q<=write;read_q<=storage;
            if(write) storage<=wdata;
        end
    end
    task cycle;begin @(posedge clk);#1;end endtask
    task restart(input integer injection);
        begin
            @(negedge clk);reset=1;start=0;#1;
            if(valid!==0)$fatal(1,"BIST reset did not isolate pending request");
            cycle();cycle();@(negedge clk);reset=0;mode=injection;
            cycle();@(negedge clk);start=1;cycle();@(negedge clk);start=0;
        end
    endtask
    task finish(input integer injection);
        integer budget;
        begin
            budget=1000;
            while(done!==1 && budget>0)begin cycle();budget=budget-1;end
            if(budget==0)$fatal(1,"BIST four-state test timed out");
            if(busy!==0 || valid!==0)$fatal(1,"BIST completed with pending traffic");
            if(injection==0)begin
                if(failed!==0 || completed_operations!==80 || storage!==128'b0)
                    $fatal(1,"BIST healthy unknown-start memory failed");
            end else begin
                if(failed!==1 || error_code!==1 || expected_data!==128'haaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa || error_address!==0)
                    $fatal(1,"BIST unknown read was not diagnosed");
                if(injection==1 && observed_data[0]!==1'bx)$fatal(1,"BIST lost unknown observation");
                if(injection==2 && observed_data[0]!==1'bz)$fatal(1,"BIST lost high-impedance observation");
            end
            cycle();cycle();
        end
    endtask
    initial begin
        #1;if(valid!==0)$fatal(1,"BIST reset did not isolate pending request");
        restart(0);finish(0);
        restart(1);finish(1);
        restart(2);finish(2);
        // Reset in an outstanding request, before any clock can cancel it.
        restart(0);restart(0);finish(0);
        $display("PASS BIST four-state startup, X/Z diagnostics, reset isolation and recovery; commands=%0d",commands);
        $finish;
    end
endmodule
