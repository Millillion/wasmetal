`timescale 1ps/1ps
module glbl;
reg GSR=1'b0;
initial begin #100 GSR=1'b1; #1000 GSR=1'b0; end
endmodule
module bench;
reg [3:0] pins=0,next_pins;
reg expected_yosys,expected_vendor;
wire observed;
FDSE #(.INIT(1'b0)) dut(.Q(observed),.C(pins[3]),.S(pins[2]),.CE(pins[1]),.D(pins[0]));
integer fd,j,n,extra;
initial begin
 #2000;
 if(observed!==1'b0)$fatal(1,"FLOP_INIT_MISMATCH observed=%b",observed);
 fd=$fopen("/tmp/wasmetal-direct-rounding/build/xc7-flops/FDSE/known-init-0.txt","r");if(fd==0)$fatal(1,"FLOP_TRACE_OPEN_FAILED");
 for(j=0;j<4416;j=j+1)begin
  n=$fscanf(fd,"%b %b %b",next_pins,expected_yosys,expected_vendor);
  if(n!=3)$fatal(1,"FLOP_TRACE_TRUNCATED_OR_MALFORMED");
  pins=next_pins;
  #1000;
  if(observed!==expected_yosys)
   $fatal(1,"FLOP_ORACLE_MISMATCH row=%0d pins=%b observed=%b yosys=%b vendor=%b",j,pins,observed,expected_yosys,expected_vendor);
 end
 n=$fscanf(fd,"%s",extra);
 if(n!=-1 && !(n==0 && $feof(fd)))$fatal(1,"FLOP_TRACE_EXTRA_DATA");
 $fclose(fd);$display("PASS 4416 flip-flop transitions");$finish;
end
endmodule
