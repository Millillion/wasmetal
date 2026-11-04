module bench;
reg [7:0] scan_table, table_value;
reg [7:0] expected;
reg [2:0] pins;
wire original_value,candidate_value;
original3 u0(.O(original_value),.I0(pins[0]),.I1(pins[1]),.I2(pins[2]),.INIT(table_value));
candidate3 u1(.O(candidate_value),.I0(pins[0]),.I1(pins[1]),.I2(pins[2]),.INIT(table_value));
integer fd,i,j,k,n,extra;
initial begin
 fd=$fopen("/tmp/wasmetal-xc7-core/build/xc7-core-lut-check/lut3-known/oracle.txt","r");
 if(fd==0)$fatal(1,"LUT_TRACE_OPEN_FAILED");
 for(i=0;i<81;i=i+1)begin
  n=$fscanf(fd,"%b %b",scan_table,expected);
  if(n!=2)$fatal(1,"LUT_TRACE_TRUNCATED");
  table_value=scan_table;
  for(j=0;j<8;j=j+1)begin
   for(k=0;k<3;k=k+1)begin pins[k]=j[k]; end
   #1;
   if(original_value!==expected[j] || candidate_value!==expected[j])
    $fatal(1,"LUT_ORACLE_MISMATCH table=%b pins=%b expected=%b original=%b candidate=%b",table_value,pins,expected[j],original_value,candidate_value);
  end
 end
 n=$fscanf(fd,"%s",extra);
 if(n!=-1 && !(n==0 && $feof(fd)))$fatal(1,"LUT_TRACE_EXTRA_DATA");
 $fclose(fd);
 $display("PASS 648 LUT3 oracle comparisons per model");
 $finish;
end
endmodule
