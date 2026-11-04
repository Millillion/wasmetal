module bench;
reg [3:0] scan_table, table_value;
reg [15:0] expected;
reg [1:0] pins;
wire original_value,candidate_value;
original2 u0(.O(original_value),.I0(pins[0]),.I1(pins[1]),.INIT(table_value));
candidate2 u1(.O(candidate_value),.I0(pins[0]),.I1(pins[1]),.INIT(table_value));
integer fd,i,j,k,n,extra;
initial begin
 fd=$fopen("/tmp/wasmetal-xc7-core/build/xc7-core-lut-check/lut2-four-state/malformed-trace.txt","r");
 if(fd==0)$fatal(1,"LUT_TRACE_OPEN_FAILED");
 for(i=0;i<30;i=i+1)begin
  n=$fscanf(fd,"%b %b",scan_table,expected);
  if(n!=2)$fatal(1,"LUT_TRACE_TRUNCATED");
  table_value=scan_table;
  for(j=0;j<16;j=j+1)begin
   for(k=0;k<2;k=k+1)begin case ((j >> (2*k)) & 3)
0:pins[k]=0;1:pins[k]=1;2:pins[k]=1'bx;3:pins[k]=1'bz;endcase end
   #1;
   if(original_value!==expected[j] || candidate_value!==expected[j])
    $fatal(1,"LUT_ORACLE_MISMATCH table=%b pins=%b expected=%b original=%b candidate=%b",table_value,pins,expected[j],original_value,candidate_value);
  end
 end
 n=$fscanf(fd,"%s",extra);
 if(n!=-1 && !(n==0 && $feof(fd)))$fatal(1,"LUT_TRACE_EXTRA_DATA");
 $fclose(fd);
 $display("PASS 480 LUT2 oracle comparisons per model");
 $finish;
end
endmodule
