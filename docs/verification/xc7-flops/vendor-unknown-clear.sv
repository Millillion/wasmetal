`timescale 1ps/1ps
module glbl;
reg GSR=0; initial begin #100 GSR=1; #1000 GSR=0; end
endmodule
module bench;
reg c=0,r=0,d=1; wire q; integer unknown_pulses=0;
FDCE #(.INIT(1'b0)) dut(.C(c),.CLR(r),.D(d),.CE(1'b1),.Q(q));
always @(dut.CLR_in) if($time>2000 && dut.CLR_in===1'bx)unknown_pulses=unknown_pulses+1;
initial begin
 #2000; c=1; #1000; c=0; #1000; r=1'bz; #1000; d=0; #1000;
 if(q!==1'b1)$fatal(1,"VENDOR_DIAGNOSTIC_SETUP_FAILED");
 r=0; #1000;
 if(c!==1'b0 || q!==1'b0 || unknown_pulses==0)$fatal(1,"VENDOR_DIAGNOSTIC_CHANGED");
 $display("PASS vendor unknown-clear diagnostic: Q changed without a clock edge; internal X pulses=%0d",unknown_pulses);
 $finish;
end
endmodule
