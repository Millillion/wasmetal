module bench;
reg [9:0] pins;
reg [7:0] expected_yosys,expected_vendor;
wire [3:0] co,o;
wire [7:0] observed={co,o};
CARRY4 dut(.CO(co),.O(o),.CI(pins[0]),.CYINIT(pins[1]),.DI(pins[5:2]),.S(pins[9:6]));
integer fd,j,k,n,extra;
initial begin
 fd=$fopen("/tmp/wasmetal-xc7-core/build/xc7-carry-check/known.txt","r");if(fd==0)$fatal(1,"CARRY_TRACE_OPEN_FAILED");
 for(j=0;j<1024;j=j+1)begin
  n=$fscanf(fd,"%b %b",expected_yosys,expected_vendor);
  if(n!=2)$fatal(1,"CARRY_TRACE_TRUNCATED");
  pins=j[9:0];
  #1;
  if(observed!==expected_vendor)
   $fatal(1,"CARRY_ORACLE_MISMATCH pins=%b observed=%b yosys=%b vendor=%b",pins,observed,expected_yosys,expected_vendor);
 end
 n=$fscanf(fd,"%s",extra);
 if(n!=-1 && !(n==0 && $feof(fd)))$fatal(1,"CARRY_TRACE_EXTRA_DATA");
 $fclose(fd);$display("PASS 1024 carry oracle comparisons");$finish;
end
endmodule
