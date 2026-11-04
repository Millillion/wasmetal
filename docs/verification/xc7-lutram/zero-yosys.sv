`timescale 1ps/1ps
module bench;
reg [29:0] pins=0,next_pins;
reg [3:0] expected_yosys,expected_vendor;
wire [3:0] observed;
RAM64M #(.INIT_A(64'b0000000000000000000000000000000000000000000000000000000000000000),.INIT_B(64'b0000000000000000000000000000000000000000000000000000000000000000),.INIT_C(64'b0000000000000000000000000000000000000000000000000000000000000000),.INIT_D(64'b0000000000000000000000000000000000000000000000000000000000000000)) dut(.WCLK(pins[29]),.WE(pins[28]),
 .DIA(pins[24]),.DIB(pins[25]),.DIC(pins[26]),.DID(pins[27]),
 .ADDRA(pins[23:18]),.ADDRB(pins[17:12]),.ADDRC(pins[11:6]),.ADDRD(pins[5:0]),
 .DOA(observed[0]),.DOB(observed[1]),.DOC(observed[2]),.DOD(observed[3]));
integer fd,n,j,extra;
initial begin
 #1000;
 fd=$fopen("/tmp/wasmetal-direct-rounding/build/xc7-lutram/zero.txt","r");if(fd==0)$fatal(1,"LUTRAM_TRACE_OPEN_FAILED");
 for(j=0;j<37184;j=j+1)begin
  n=$fscanf(fd,"%b %b %b",next_pins,expected_yosys,expected_vendor);
  if(n!=3)$fatal(1,"LUTRAM_TRACE_TRUNCATED_OR_MALFORMED");
  pins=next_pins; #1000;
  if(observed!==expected_yosys)
   $fatal(1,"LUTRAM_ORACLE_MISMATCH row=%0d pins=%b observed=%b yosys=%b vendor=%b",j,pins,observed,expected_yosys,expected_vendor);
 end
 n=$fscanf(fd,"%s",extra);
 if(n!=-1 && !(n==0 && $feof(fd)))$fatal(1,"LUTRAM_TRACE_EXTRA_DATA");
 $fclose(fd);$display("PASS 37184 distributed-RAM observations");$finish;
end
endmodule
