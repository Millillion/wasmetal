`timescale 1ns/1ps
module cell_check_0(output reg done);
reg [4:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a2111oi_0 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.C1(stimulus[3]),.D1(stimulus[4]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__a2111oi_0 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.C1(stimulus[3]),.D1(stimulus[4]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<32;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a2111oi_0 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_1(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a211o_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.C1(stimulus[3]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__a211o_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.C1(stimulus[3]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a211o_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_2(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a211oi_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.C1(stimulus[3]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__a211oi_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.C1(stimulus[3]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a211oi_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_3(output reg done);
reg [2:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a21bo_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1_N(stimulus[2]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__a21bo_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1_N(stimulus[2]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<8;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a21bo_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_4(output reg done);
reg [2:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a21boi_0 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1_N(stimulus[2]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__a21boi_0 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1_N(stimulus[2]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<8;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a21boi_0 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_5(output reg done);
reg [2:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a21o_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__a21o_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<8;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a21o_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_6(output reg done);
reg [2:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a21oi_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__a21oi_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<8;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a21oi_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_7(output reg done);
reg [4:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a221o_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.C1(stimulus[4]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__a221o_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.C1(stimulus[4]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<32;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a221o_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_8(output reg done);
reg [4:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a221oi_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.C1(stimulus[4]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__a221oi_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.C1(stimulus[4]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<32;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a221oi_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_9(output reg done);
reg [5:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a222oi_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.C1(stimulus[4]),.C2(stimulus[5]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__a222oi_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.C1(stimulus[4]),.C2(stimulus[5]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<64;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a222oi_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_10(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a22o_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__a22o_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a22o_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_11(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a22oi_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__a22oi_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a22oi_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_12(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a2bb2o_1 vendor(.A1_N(stimulus[0]),.A2_N(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__a2bb2o_1 derived(.A1_N(stimulus[0]),.A2_N(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a2bb2o_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_13(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a2bb2oi_1 vendor(.A1_N(stimulus[0]),.A2_N(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__a2bb2oi_1 derived(.A1_N(stimulus[0]),.A2_N(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a2bb2oi_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_14(output reg done);
reg [4:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a311o_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.B1(stimulus[3]),.C1(stimulus[4]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__a311o_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.B1(stimulus[3]),.C1(stimulus[4]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<32;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a311o_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_15(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a31o_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.B1(stimulus[3]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__a31o_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.B1(stimulus[3]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a31o_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_16(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a31oi_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.B1(stimulus[3]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__a31oi_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.B1(stimulus[3]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a31oi_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_17(output reg done);
reg [4:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a32o_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.B1(stimulus[3]),.B2(stimulus[4]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__a32o_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.B1(stimulus[3]),.B2(stimulus[4]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<32;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a32o_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_18(output reg done);
reg [4:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a32oi_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.B1(stimulus[3]),.B2(stimulus[4]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__a32oi_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.B1(stimulus[3]),.B2(stimulus[4]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<32;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a32oi_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_19(output reg done);
reg [4:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a41o_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.A4(stimulus[3]),.B1(stimulus[4]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__a41o_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.A4(stimulus[3]),.B1(stimulus[4]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<32;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a41o_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_20(output reg done);
reg [4:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__a41oi_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.A4(stimulus[3]),.B1(stimulus[4]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__a41oi_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.A4(stimulus[3]),.B1(stimulus[4]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<32;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__a41oi_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_21(output reg done);
reg [1:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__and2_0 vendor(.A(stimulus[0]),.B(stimulus[1]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__and2_0 derived(.A(stimulus[0]),.B(stimulus[1]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<4;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__and2_0 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_22(output reg done);
reg [2:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__and3_1 vendor(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__and3_1 derived(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<8;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__and3_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_23(output reg done);
reg [2:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__and3b_1 vendor(.A_N(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__and3b_1 derived(.A_N(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<8;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__and3b_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_24(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__and4_1 vendor(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.D(stimulus[3]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__and4_1 derived(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.D(stimulus[3]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__and4_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_25(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__and4b_1 vendor(.A_N(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.D(stimulus[3]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__and4b_1 derived(.A_N(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.D(stimulus[3]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__and4b_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_26(output reg done);
reg [0:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__clkinv_1 vendor(.A(stimulus[0]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__clkinv_1 derived(.A(stimulus[0]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<2;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__clkinv_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_27(output reg done);
reg [0:0] stimulus=0;wire [1:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__conb_1 vendor(.HI(vendor_q[0]),.LO(vendor_q[1]));
derived__sky130_fd_sc_hd__conb_1 derived(.HI(derived_q[0]),.LO(derived_q[1]));
initial begin
 done=0;
 for(pattern=0;pattern<1;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__conb_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_28(output reg done);
reg d=0,clk=0;wire vendor_q,derived_q;reg expected;integer seed,prior,following;
sky130_fd_sc_hd__dfxtp_1 vendor(.D(d),.CLK(clk),.Q(vendor_q));
derived__sky130_fd_sc_hd__dfxtp_1 derived(.D(d),.CLK(clk),.Q(derived_q));
initial begin
 done=0;
 for(seed=0;seed<2;seed=seed+1) for(prior=0;prior<4;prior=prior+1) for(following=0;following<4;following=following+1) begin
  clk=0;d=seed[0];#1;clk=1;#1;
  if(vendor_q!==seed[0] || derived_q!==seed[0]) $fatal(1,"DFF seed mismatch");
  d=prior[0];clk=prior[1];#1;
  if(vendor_q!==seed[0] || derived_q!==seed[0]) $fatal(1,"DFF pretransition hold mismatch");
  d=following[0];clk=following[1];#1;
  expected=(!prior[1] && following[1]) ? following[0] : seed[0];
  if(vendor_q!==expected || derived_q!==expected) $fatal(1,"DFF binary transition mismatch");
 end
 done=1;
end
endmodule
module cell_check_29(output reg done);
reg [2:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__maj3_1 vendor(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__maj3_1 derived(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<8;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__maj3_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_30(output reg done);
reg [2:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__mux2_1 vendor(.A0(stimulus[0]),.A1(stimulus[1]),.S(stimulus[2]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__mux2_1 derived(.A0(stimulus[0]),.A1(stimulus[1]),.S(stimulus[2]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<8;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__mux2_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_31(output reg done);
reg [2:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__mux2i_1 vendor(.A0(stimulus[0]),.A1(stimulus[1]),.S(stimulus[2]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__mux2i_1 derived(.A0(stimulus[0]),.A1(stimulus[1]),.S(stimulus[2]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<8;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__mux2i_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_32(output reg done);
reg [1:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__nand2_1 vendor(.A(stimulus[0]),.B(stimulus[1]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__nand2_1 derived(.A(stimulus[0]),.B(stimulus[1]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<4;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__nand2_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_33(output reg done);
reg [1:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__nand2b_1 vendor(.A_N(stimulus[0]),.B(stimulus[1]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__nand2b_1 derived(.A_N(stimulus[0]),.B(stimulus[1]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<4;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__nand2b_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_34(output reg done);
reg [2:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__nand3_1 vendor(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__nand3_1 derived(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<8;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__nand3_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_35(output reg done);
reg [2:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__nand3b_1 vendor(.A_N(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__nand3b_1 derived(.A_N(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<8;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__nand3b_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_36(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__nand4_1 vendor(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.D(stimulus[3]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__nand4_1 derived(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.D(stimulus[3]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__nand4_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_37(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__nand4b_1 vendor(.A_N(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.D(stimulus[3]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__nand4b_1 derived(.A_N(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.D(stimulus[3]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__nand4b_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_38(output reg done);
reg [1:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__nor2_1 vendor(.A(stimulus[0]),.B(stimulus[1]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__nor2_1 derived(.A(stimulus[0]),.B(stimulus[1]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<4;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__nor2_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_39(output reg done);
reg [1:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__nor2b_1 vendor(.A(stimulus[0]),.B_N(stimulus[1]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__nor2b_1 derived(.A(stimulus[0]),.B_N(stimulus[1]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<4;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__nor2b_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_40(output reg done);
reg [2:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__nor3_1 vendor(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__nor3_1 derived(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<8;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__nor3_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_41(output reg done);
reg [2:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__nor3b_1 vendor(.A(stimulus[0]),.B(stimulus[1]),.C_N(stimulus[2]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__nor3b_1 derived(.A(stimulus[0]),.B(stimulus[1]),.C_N(stimulus[2]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<8;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__nor3b_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_42(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__nor4_1 vendor(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.D(stimulus[3]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__nor4_1 derived(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.D(stimulus[3]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__nor4_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_43(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__nor4b_1 vendor(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.D_N(stimulus[3]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__nor4b_1 derived(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.D_N(stimulus[3]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__nor4b_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_44(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__nor4bb_1 vendor(.A(stimulus[0]),.B(stimulus[1]),.C_N(stimulus[2]),.D_N(stimulus[3]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__nor4bb_1 derived(.A(stimulus[0]),.B(stimulus[1]),.C_N(stimulus[2]),.D_N(stimulus[3]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__nor4bb_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_45(output reg done);
reg [4:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__o2111a_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.C1(stimulus[3]),.D1(stimulus[4]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__o2111a_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.C1(stimulus[3]),.D1(stimulus[4]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<32;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__o2111a_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_46(output reg done);
reg [4:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__o2111ai_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.C1(stimulus[3]),.D1(stimulus[4]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__o2111ai_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.C1(stimulus[3]),.D1(stimulus[4]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<32;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__o2111ai_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_47(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__o211ai_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.C1(stimulus[3]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__o211ai_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.C1(stimulus[3]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__o211ai_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_48(output reg done);
reg [2:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__o21a_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__o21a_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<8;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__o21a_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_49(output reg done);
reg [2:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__o21ai_0 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__o21ai_0 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<8;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__o21ai_0 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_50(output reg done);
reg [2:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__o21bai_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1_N(stimulus[2]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__o21bai_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1_N(stimulus[2]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<8;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__o21bai_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_51(output reg done);
reg [4:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__o221a_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.C1(stimulus[4]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__o221a_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.C1(stimulus[4]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<32;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__o221a_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_52(output reg done);
reg [4:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__o221ai_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.C1(stimulus[4]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__o221ai_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.C1(stimulus[4]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<32;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__o221ai_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_53(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__o22ai_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__o22ai_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__o22ai_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_54(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__o2bb2ai_1 vendor(.A1_N(stimulus[0]),.A2_N(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__o2bb2ai_1 derived(.A1_N(stimulus[0]),.A2_N(stimulus[1]),.B1(stimulus[2]),.B2(stimulus[3]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__o2bb2ai_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_55(output reg done);
reg [4:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__o311ai_0 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.B1(stimulus[3]),.C1(stimulus[4]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__o311ai_0 derived(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.B1(stimulus[3]),.C1(stimulus[4]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<32;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__o311ai_0 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_56(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__o31ai_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.B1(stimulus[3]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__o31ai_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.B1(stimulus[3]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__o31ai_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_57(output reg done);
reg [4:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__o32ai_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.B1(stimulus[3]),.B2(stimulus[4]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__o32ai_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.B1(stimulus[3]),.B2(stimulus[4]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<32;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__o32ai_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_58(output reg done);
reg [4:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__o41ai_1 vendor(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.A4(stimulus[3]),.B1(stimulus[4]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__o41ai_1 derived(.A1(stimulus[0]),.A2(stimulus[1]),.A3(stimulus[2]),.A4(stimulus[3]),.B1(stimulus[4]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<32;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__o41ai_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_59(output reg done);
reg [1:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__or2_0 vendor(.A(stimulus[0]),.B(stimulus[1]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__or2_0 derived(.A(stimulus[0]),.B(stimulus[1]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<4;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__or2_0 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_60(output reg done);
reg [2:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__or3_1 vendor(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__or3_1 derived(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<8;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__or3_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_61(output reg done);
reg [2:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__or3b_1 vendor(.A(stimulus[0]),.B(stimulus[1]),.C_N(stimulus[2]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__or3b_1 derived(.A(stimulus[0]),.B(stimulus[1]),.C_N(stimulus[2]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<8;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__or3b_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_62(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__or4_1 vendor(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.D(stimulus[3]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__or4_1 derived(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.D(stimulus[3]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__or4_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_63(output reg done);
reg [3:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__or4b_1 vendor(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.D_N(stimulus[3]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__or4b_1 derived(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.D_N(stimulus[3]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<16;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__or4b_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_64(output reg done);
reg [1:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__xnor2_1 vendor(.A(stimulus[0]),.B(stimulus[1]),.Y(vendor_q[0]));
derived__sky130_fd_sc_hd__xnor2_1 derived(.A(stimulus[0]),.B(stimulus[1]),.Y(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<4;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__xnor2_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_65(output reg done);
reg [2:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__xnor3_1 vendor(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__xnor3_1 derived(.A(stimulus[0]),.B(stimulus[1]),.C(stimulus[2]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<8;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__xnor3_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module cell_check_66(output reg done);
reg [1:0] stimulus=0;wire [0:0] vendor_q,derived_q;integer pattern;
sky130_fd_sc_hd__xor2_1 vendor(.A(stimulus[0]),.B(stimulus[1]),.X(vendor_q[0]));
derived__sky130_fd_sc_hd__xor2_1 derived(.A(stimulus[0]),.B(stimulus[1]),.X(derived_q[0]));
initial begin
 done=0;
 for(pattern=0;pattern<4;pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"sky130_fd_sc_hd__xor2_1 binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
module testbench;wire [66:0] done;
cell_check_0 check_0(.done(done[0]));
cell_check_1 check_1(.done(done[1]));
cell_check_2 check_2(.done(done[2]));
cell_check_3 check_3(.done(done[3]));
cell_check_4 check_4(.done(done[4]));
cell_check_5 check_5(.done(done[5]));
cell_check_6 check_6(.done(done[6]));
cell_check_7 check_7(.done(done[7]));
cell_check_8 check_8(.done(done[8]));
cell_check_9 check_9(.done(done[9]));
cell_check_10 check_10(.done(done[10]));
cell_check_11 check_11(.done(done[11]));
cell_check_12 check_12(.done(done[12]));
cell_check_13 check_13(.done(done[13]));
cell_check_14 check_14(.done(done[14]));
cell_check_15 check_15(.done(done[15]));
cell_check_16 check_16(.done(done[16]));
cell_check_17 check_17(.done(done[17]));
cell_check_18 check_18(.done(done[18]));
cell_check_19 check_19(.done(done[19]));
cell_check_20 check_20(.done(done[20]));
cell_check_21 check_21(.done(done[21]));
cell_check_22 check_22(.done(done[22]));
cell_check_23 check_23(.done(done[23]));
cell_check_24 check_24(.done(done[24]));
cell_check_25 check_25(.done(done[25]));
cell_check_26 check_26(.done(done[26]));
cell_check_27 check_27(.done(done[27]));
cell_check_28 check_28(.done(done[28]));
cell_check_29 check_29(.done(done[29]));
cell_check_30 check_30(.done(done[30]));
cell_check_31 check_31(.done(done[31]));
cell_check_32 check_32(.done(done[32]));
cell_check_33 check_33(.done(done[33]));
cell_check_34 check_34(.done(done[34]));
cell_check_35 check_35(.done(done[35]));
cell_check_36 check_36(.done(done[36]));
cell_check_37 check_37(.done(done[37]));
cell_check_38 check_38(.done(done[38]));
cell_check_39 check_39(.done(done[39]));
cell_check_40 check_40(.done(done[40]));
cell_check_41 check_41(.done(done[41]));
cell_check_42 check_42(.done(done[42]));
cell_check_43 check_43(.done(done[43]));
cell_check_44 check_44(.done(done[44]));
cell_check_45 check_45(.done(done[45]));
cell_check_46 check_46(.done(done[46]));
cell_check_47 check_47(.done(done[47]));
cell_check_48 check_48(.done(done[48]));
cell_check_49 check_49(.done(done[49]));
cell_check_50 check_50(.done(done[50]));
cell_check_51 check_51(.done(done[51]));
cell_check_52 check_52(.done(done[52]));
cell_check_53 check_53(.done(done[53]));
cell_check_54 check_54(.done(done[54]));
cell_check_55 check_55(.done(done[55]));
cell_check_56 check_56(.done(done[56]));
cell_check_57 check_57(.done(done[57]));
cell_check_58 check_58(.done(done[58]));
cell_check_59 check_59(.done(done[59]));
cell_check_60 check_60(.done(done[60]));
cell_check_61 check_61(.done(done[61]));
cell_check_62 check_62(.done(done[62]));
cell_check_63 check_63(.done(done[63]));
cell_check_64 check_64(.done(done[64]));
cell_check_65 check_65(.done(done[65]));
cell_check_66 check_66(.done(done[66]));
initial begin wait(&done);#1;$display("PASS 67 cell types; 1067 combinational vectors; 32 binary DFF transitions; 64 seed/hold checks");$finish;end
initial begin #10000;$fatal(1,"vendor comparison timeout");end
endmodule
