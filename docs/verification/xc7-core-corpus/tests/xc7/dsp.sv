`timescale 1ns/1ps
module xc7_dsp;
    reg clk=0,enable=0,reset=0;
    reg [29:0] a,acin,scan_a,scan_acin,expected_ac;
    reg [17:0] b,bcin,scan_b,scan_bcin,expected_bc;
    reg [47:0] c,pcin,scan_c,scan_pcin,expected_p;
    wire [47:0] p,pcout;
    wire [29:0] acout;
    wire [17:0] bcout;
    dsp_fixture dut(.*);
    integer fd,scan,count,expected_count;
    string path;
    task automatic check(input string phase);
        if ({p,pcout,acout,bcout} !== {expected_p,expected_p,expected_ac,expected_bc})
            $fatal(1,"DSP_DATA_MISMATCH vector=%0d phase=%s p=%h expected=%h ac=%h expected_ac=%h bc=%h expected_bc=%h pc=%h",
                count,phase,p,expected_p,acout,expected_ac,bcout,expected_bc,pcout);
    endtask
    initial begin
        if (!$value$plusargs("VECTORS=%s",path) || !$value$plusargs("COUNT=%d",expected_count) || expected_count<=0)
            $fatal(1,"MISSING_DSP_TRACE");
        fd=$fopen(path,"r");
        if (!fd) $fatal(1,"MISSING_DSP_TRACE");
        #200;
        count=0;
        scan=$fscanf(fd,"%h %h %h %h %h %h %h %h %h",scan_a,scan_acin,scan_b,scan_bcin,
            scan_c,scan_pcin,expected_p,expected_ac,expected_bc);
        while(scan!=-1 && !(scan==0 && $feof(fd))) begin
            if(scan!=9 || count>=expected_count) $fatal(1,"MALFORMED_DSP_TRACE");
            a=scan_a;acin=scan_acin;b=scan_b;bcin=scan_bcin;c=scan_c;pcin=scan_pcin;
            enable=(count%7)!=0;reset=(count%11)==0;
            #10;check("before clock");
            clk=1;#10;check("positive edge");
            clk=0;#10;check("negative edge");
            count=count+1;
            scan=$fscanf(fd,"%h %h %h %h %h %h %h %h %h",scan_a,scan_acin,scan_b,scan_bcin,
                scan_c,scan_pcin,expected_p,expected_ac,expected_bc);
        end
        if(count!=expected_count) $fatal(1,"INCOMPLETE_DSP_TRACE");
        $fclose(fd);
        $display("PASS XC7_DSP vectors=%0d",count);
        $finish;
    end
endmodule
