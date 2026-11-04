module bench;
reg [31:0] scan_table, table_value;
reg [31:0] expected;
reg [4:0] pins;
wire original_value,candidate_value;
original5 u0(.O(original_value),.I0(pins[0]),.I1(pins[1]),.I2(pins[2]),.I3(pins[3]),.I4(pins[4]),.INIT(table_value));
candidate5 u1(.O(candidate_value),.I0(pins[0]),.I1(pins[1]),.I2(pins[2]),.I3(pins[3]),.I4(pins[4]),.INIT(table_value));
integer fd,i,j,k,n,extra;
initial begin
 fd=$fopen("/tmp/wasmetal-xc7-core/build/xc7-core-lut-check/lut5-known/oracle.txt","r");
 if(fd==0)$fatal(1,"LUT_TRACE_OPEN_FAILED");
 for(i=0;i<680;i=i+1)begin
  n=$fscanf(fd,"%b %b",scan_table,expected);
  if(n!=2)$fatal(1,"LUT_TRACE_TRUNCATED");
  table_value=scan_table;
  for(j=0;j<32;j=j+1)begin
   for(k=0;k<5;k=k+1)begin pins[k]=j[k]; end
   #1;
   if(original_value!==expected[j] || candidate_value!==expected[j])
    $fatal(1,"LUT_ORACLE_MISMATCH table=%b pins=%b expected=%b original=%b candidate=%b",table_value,pins,expected[j],original_value,candidate_value);
  end
 end
 n=$fscanf(fd,"%s",extra);
 if(n!=-1 && !(n==0 && $feof(fd)))$fatal(1,"LUT_TRACE_EXTRA_DATA");
 $fclose(fd);
 $display("PASS 21760 LUT5 oracle comparisons per model");
 $finish;
end
endmodule
