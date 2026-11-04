`timescale 1ps/1ps
module bench;
reg [2:0] pins,next_pins;
reg expected_yosys,expected_vendor;
wire value;
wire observed=value;
MUXF8 dut(.O(value),.I0(pins[0]),.I1(pins[1]),.S(pins[2]));
integer fd,n,j,extra;
initial begin
 fd=$fopen("/tmp/wasmetal-xc7-core/build/xc7-muxes/MUXF8/four-state.txt","r");if(fd==0)$fatal(1,"MUX_TRACE_OPEN_FAILED");
 for(j=0;j<64;j=j+1)begin
  n=$fscanf(fd,"%b %b %b",next_pins,expected_yosys,expected_vendor);
  if(n!=3)$fatal(1,"MUX_TRACE_TRUNCATED_OR_MALFORMED");
  pins=next_pins; #1000;
  if(observed!==expected_vendor)
   $fatal(1,"MUX_ORACLE_MISMATCH pins=%b observed=%b yosys=%b vendor=%b",pins,observed,expected_yosys,expected_vendor);
 end
 n=$fscanf(fd,"%s",extra);
 if(n!=-1 && !(n==0 && $feof(fd)))$fatal(1,"MUX_TRACE_EXTRA_DATA");
 $fclose(fd);$display("PASS 64 logic oracle comparisons");$finish;
end
endmodule
