// SPDX-License-Identifier: MIT
module cdc_four_state;
    reg s_clk=0,m_clk=0,reset=0,clocks_on=0;
    reg s_valid=0,s_write=0;
    reg [31:0] s_address=0;
    reg [15:0] s_mask=0;
    reg [127:0] s_wdata=0;
    wire source_online,s_reset,m_reset,s_ready,s_fault,m_valid,m_write;
    wire [127:0] s_rdata,m_wdata;
    wire [31:0] m_address;
    wire [15:0] m_mask;
    reg m_ready,m_fault,force_error=0,reference_active=0;
    reg [127:0] m_rdata;
    reg [176:0] expected_request;
    localparam [127:0] TRANSFORM=128'h123456789abcdef0_fedcba9876543210;
    wasmetal_memory_cdc dut(.*);
    always #3 if(clocks_on) s_clk=~s_clk;
    always #5 if(clocks_on) m_clk=~m_clk;
    always @(posedge m_clk or posedge m_reset) begin
        if(m_reset) begin m_ready<=0;m_fault<=0;m_rdata<=0;end
        else if(m_valid) begin
            if(!reference_active || {m_write,m_address,m_mask,m_wdata}!==expected_request)
                $fatal(1,"four-state request mismatch or phantom request");
            if(!m_ready) begin
                m_ready<=1;m_fault<=force_error;
                m_rdata<=force_error ? 128'bx : m_wdata^TRANSFORM;
            end
        end else m_ready<=0;
    end
    task check_reset;
        begin
            #1;
            if(s_reset!==1 || m_reset!==1 || s_ready!==0 || m_valid!==0 || source_online!==0)
                $fatal(1,"reset did not isolate unknown startup state");
        end
    endtask
    task online;
        integer n;
        begin
            n=0;
            while(source_online!==1 && n<100) begin @(posedge s_clk);#1;n=n+1;end
            if(source_online!==1) $fatal(1,"four-state online timeout");
        end
    endtask
    task transfer(input [127:0] value,input error);
        integer n;
        begin
            @(negedge s_clk);
            s_write=1;s_address=32'hfedcba90;s_mask=16'h5aa5;s_wdata=value;
            expected_request={s_write,s_address,s_mask,s_wdata};reference_active=1;
            force_error=error;s_valid=1;n=0;
            while(s_ready!==1 && n<100) begin @(posedge s_clk);#1;n=n+1;end
            if(s_ready!==1) $fatal(1,"four-state response timeout");
            if(s_fault!==error || s_rdata!==(error ? 128'b0 : value^TRANSFORM))
                $fatal(1,"four-state response mismatch");
            repeat(3) begin @(posedge s_clk);#1;if(s_ready!==0) $fatal(1,"duplicate response");end
            @(negedge s_clk);s_valid=0;
            repeat(4) @(posedge s_clk);
            reference_active=0;
        end
    endtask
    initial begin
        #1;reset=1;check_reset();reset=0;#20;check_reset();
        clocks_on=1;online();
        transfer(128'hffffffff_01020304_abcdef01_76543210,0);
        transfer(128'h87654321_fedcba98_00000000_ffffffff,1);
        // A reset pulse must also work with both clocks stopped, including
        // while a request is crossing. No old response may reach the next boot.
        @(negedge s_clk);s_valid=1;reference_active=1;
        @(posedge s_clk);#1;clocks_on=0;reset=1;check_reset();
        reference_active=0;s_valid=0;reset=0;#20;check_reset();
        clocks_on=1;online();transfer(128'h55aa55aa_aa55aa55_11223344_99887766,0);
        $display("PASS CDC four-state startup, fault masking and stopped-clock reset");$finish;
    end
    initial begin #20000;$fatal(1,"four-state test timed out");end
endmodule
