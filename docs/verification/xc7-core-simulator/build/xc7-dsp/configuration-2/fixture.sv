module dsp_fixture(input clk,enable,reset,
input [29:0] a,acin,input [17:0] b,bcin,input [47:0] c,pcin,
output [47:0] p,pcout,output [29:0] acout,output [17:0] bcout);
wire [47:0] raw_p,raw_pc;
DSP48E1 #(.ACASCREG(0),.ADREG(0),.ALUMODEREG(0),.AREG(0),.BCASCREG(0),.BREG(0),.CARRYINREG(0),.CARRYINSELREG(0),.CREG(0),.DREG(0),.INMODEREG(0),.MREG(0),.OPMODEREG(0),.PREG(0),.A_INPUT("DIRECT"),.B_INPUT("DIRECT"),.USE_DPORT("FALSE"),.USE_MULT("MULTIPLY"),.USE_SIMD("ONE48")) cell_under_test(.A(a),.ACIN(acin),.B(b),.BCIN(bcin),.C(c),.D(25'b0),.PCIN(pcin),.CLK(clk),.OPMODE(7'd5),.ALUMODE(4'b0),.INMODE(5'b0),.CARRYINSEL(3'b0),.CARRYIN(1'b0),.CARRYCASCIN(1'b0),.MULTSIGNIN(1'b0),.P(raw_p),.PCOUT(raw_pc),.ACOUT(acout),.BCOUT(bcout),.CEA1(enable),.CEA2(enable),.CEAD(enable),.CEALUMODE(enable),.CEB1(enable),.CEB2(enable),.CEC(enable),.CECARRYIN(enable),.CECTRL(enable),.CED(enable),.CEINMODE(enable),.CEM(enable),.CEP(enable),.RSTA(reset),.RSTALLCARRYIN(reset),.RSTALUMODE(reset),.RSTB(reset),.RSTC(reset),.RSTCTRL(reset),.RSTD(reset),.RSTINMODE(reset),.RSTM(reset),.RSTP(reset));
assign p=raw_p ^ 48'd0;
assign pcout=raw_pc;
endmodule
