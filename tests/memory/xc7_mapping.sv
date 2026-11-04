`timescale 1ps/1ps
`include "fixture_parameters.svh"
module xc7_mapping;
    reg wclk=0, rclk=0, wen=0, ren=0, rst=0;
    reg [`ADDR_WIDTH-1:0] wa=0, ra=0;
    reg [`WIDTH-1:0] wd=0;
    reg [`LANES-1:0] wmask=0;
    wire [`WIDTH-1:0] rd;
    reg [`WIDTH-1:0] expected, previous;
    reg [`ADDR_WIDTH-1:0] scanned_wa,scanned_ra;
    reg [`WIDTH-1:0] scanned_wd;
    reg [`LANES-1:0] scanned_mask;
    integer fd, scan, op, count=0, required;
    string vectors;
    ram_fixture dut(.*);

    task check_value(input [`WIDTH-1:0] value, input string phase);
        if(rd !== value)
            $fatal(1,"READ_DATA_MISMATCH vector=%0d op=%0d wa=%0d ra=%0d phase=%s observed=%h expected=%h",
                count,op,wa,ra,phase,rd,value);
    endtask

    initial begin
        if(!$value$plusargs("VECTORS=%s",vectors) || !$value$plusargs("COUNT=%d",required) || required<=0)
            $fatal(1,"MISSING_VECTOR_ARGUMENTS");
        fd=$fopen(vectors,"r");
        if(!fd) $fatal(1,"VECTOR_FILE_UNREADABLE");
        // The unmodified vendor glbl model releases configuration GSR at 100 ns.
        #200000;
        scan=$fscanf(fd,"%h %h %h %h %h %h\n",op,scanned_wa,scanned_ra,scanned_wd,scanned_mask,expected);
        while(scan!=-1 && !(scan==0 && $feof(fd))) begin
            if(scan!=6 || op<0 || op>5 || count>=required) $fatal(1,"MALFORMED_VECTORS");
            // Explicit assignments schedule port updates in both event-driven
            // and compiled simulators, including wide $fscanf destinations.
            wa=scanned_wa; ra=scanned_ra; wd=scanned_wd; wmask=scanned_mask;
            wen=(op==1); ren=(op==0 || op==4); rst=(op==4 || op==5);
            #5000;
            if(count!=0) check_value(previous,"before edge");
            if(op==1 || op==3) wclk=1; else rclk=1;
            #5000; check_value(expected,"active edge");
            wclk=0; rclk=0;
            #5000; check_value(expected,"inactive edge");
            previous=expected; count=count+1;
            scan=$fscanf(fd,"%h %h %h %h %h %h\n",op,scanned_wa,scanned_ra,scanned_wd,scanned_mask,expected);
        end
        $fclose(fd);
        if(count!=required) $fatal(1,"INCOMPLETE_VECTORS");
        $display("PASS XC7_MEMORY vectors=%0d width=%0d depth=%0d",count,`WIDTH,`DEPTH);
        $finish;
    end
endmodule
