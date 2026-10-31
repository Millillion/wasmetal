// SPDX-License-Identifier: MIT
module core_tb;
reg clk=0,reset=1,cmd_valid=0;
reg [3:0] cmd_kind=0;
reg [31:0] cmd_index=0,result_index=0;
reg [127:0] cmd_data=0;
reg [63:0] cmd_aux=0;
wire busy,done;
wire [7:0] trap;
wire [31:0] result_count,pc,function_index,type_actual,type_expected;
wire [127:0] result_data,mem_wdata;
reg [31:0] insn_op,insn_x,insn_y,insn_z,insn_w;
reg [127:0] insn_imm;
reg insn_valid;
reg [31:0] function_entry,function_params,function_locals,function_results,function_type;
reg function_valid;
wire mem_valid,mem_write;
wire [2:0] mem_kind;
wire [31:0] mem_index;
wire [63:0] mem_address;
wire [4:0] mem_bytes;
integer checks=0;
wasmetal_core #(.VALUE_DEPTH(129),.CONTROL_DEPTH(13),.CALL_DEPTH(17),.MEMORY_COUNT(13)) dut(
.clk(clk),.reset(reset),.cmd_valid(cmd_valid),.cmd_kind(cmd_kind),.cmd_index(cmd_index),.cmd_data(cmd_data),.cmd_aux(cmd_aux),
.busy(busy),.done(done),.trap(trap),.result_count(result_count),.result_index(result_index),.result_data(result_data),
.pc(pc),.insn_op(insn_op),.insn_x(insn_x),.insn_y(insn_y),.insn_z(insn_z),.insn_w(insn_w),.insn_imm(insn_imm),.insn_valid(insn_valid),
.function_index(function_index),.function_entry(function_entry),.function_params(function_params),.function_locals(function_locals),
.function_results(function_results),.function_type(function_type),.function_valid(function_valid),
.type_actual(type_actual),.type_expected(type_expected),.type_matches(1'b1),
.mem_valid(mem_valid),.mem_write(mem_write),.mem_kind(mem_kind),.mem_index(mem_index),.mem_address(mem_address),.mem_bytes(mem_bytes),.mem_wdata(mem_wdata),
.mem_ready(1'b1),.mem_fault(1'b0),.mem_rdata(128'b0));
always #5 clk=~clk;
always @* begin
 function_entry=function_index*8;function_params=0;function_locals=function_index==3 ? 3:0;
 function_results=1;function_type=0;function_valid=function_index<6;
 insn_valid=1;insn_op='h0b;insn_x=0;insn_y=0;insn_z=0;insn_w=0;insn_imm=0;
 case(pc)
  0:begin insn_op='h41;insn_imm=40;end
  1:begin insn_op='h41;insn_imm=2;end
  2:insn_op='h6a;
  8:begin insn_op='h44;insn_imm=64'h3ff8000000000000;end
  9:begin insn_op='h44;insn_imm=64'h4002000000000000;end
  10:insn_op='ha0;
  16:begin insn_op='hfd000c;insn_imm={16{8'h01}};end
  17:begin insn_op='hfd000c;insn_imm={16{8'h02}};end
  18:insn_op='hfd006e;
  24:begin insn_op='h20;insn_x=2;end
  25:begin insn_op='h41;insn_imm=7;end
  26:insn_op='h6a;
  32:begin insn_op='h41;insn_imm=21;end
  33:begin insn_op='h10;insn_x=0;end
  34:insn_op='h6a;
  40:begin insn_op='h41;insn_imm=1;end
  41:insn_op='h40;
  42:insn_op='h1a;
  43:insn_op='h3f;
  default:begin end
 endcase
end
task command(input [3:0] kind,input [31:0] index,input [127:0] data);
 begin
  @(negedge clk);#1;cmd_kind=kind;cmd_index=index;cmd_data=data;cmd_valid=1;
  @(negedge clk);#1;cmd_valid=0;
 end
endtask
task run(input [31:0] index,input [127:0] expected);
 integer cycles;
 begin
  command(0,index,0);cycles=0;
  while(done!==1'b1 && cycles<2000) begin @(negedge clk);#1;cycles=cycles+1;end
  if(done!==1'b1 || trap!==0 || result_count!==1 || result_data!==expected)
   $fatal(1,"four-state core failure fn=%0d done=%b trap=%h result=%h expected=%h pc=%0d",index,done,trap,result_data,expected,pc);
  checks=checks+1;
 end
endtask
initial begin
 repeat(3) @(negedge clk);#1;reset=0;
 run(0,42);run(1,128'h400e000000000000);run(2,{16{8'h03}});run(3,7);run(4,63);
 command(2,0,{64'd3,64'd1});run(5,2);
 command(6,0,0);repeat(3) @(negedge clk);#1;
 if(result_data!==2 || busy!==0) $fatal(1,"memory-size command failed");checks=checks+1;
 reset=1;repeat(3) @(negedge clk);#1;reset=0;
 command(6,0,0);repeat(3) @(negedge clk);#1;
 if(result_data!==0 || busy!==0) $fatal(1,"descriptor reset failed");checks=checks+1;
 $display("PASS four-state CPU execution: %0d checks",checks);$finish;
end
initial begin #100000;$fatal(1,"four-state CPU timeout");end
endmodule
