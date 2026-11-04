module LUT2(input A, B, output Z);
    parameter [3:0] INIT = 4'h0;
    wire [1:0] s1 = B ?     INIT[ 3:2] :     INIT[1:0];
    assign Z = $isunknown({B,A}) ? (A ? s1[1] : s1[0]) : INIT[{B,A}];
endmodule
module LUT4(input A, B, C, D, output Z);
    parameter [15:0] INIT = 16'h0000;
    wire [7:0] s3 = D ?     INIT[15:8] :     INIT[7:0];
    wire [3:0] s2 = C ?       s3[ 7:4] :       s3[3:0];
    wire [1:0] s1 = B ?       s2[ 3:2] :       s2[1:0];
    assign Z = $isunknown({D,C,B,A}) ? (A ? s1[1] : s1[0]) : INIT[{D,C,B,A}];
    
endmodule
module PFUMX (input ALUT, BLUT, C0, output Z);
	assign Z = C0 ? ALUT : BLUT;
	
endmodule
module L6MUX21 (input D0, D1, SD, output Z);
	assign Z = SD ? D1 : D0;
	
endmodule
module CCU2C(
	(* abc9_carry *)
	input  CIN,
	input  A0, B0, C0, D0, A1, B1, C1, D1,
	output S0, S1,
	(* abc9_carry *)
	output COUT
);
	parameter [15:0] INIT0 = 16'h0000;
	parameter [15:0] INIT1 = 16'h0000;
	parameter INJECT1_0 = "YES";
	parameter INJECT1_1 = "YES";

	// First half
	wire LUT4_0, LUT2_0;
	LUT4 #(.INIT(INIT0)) lut4_0(.A(A0), .B(B0), .C(C0), .D(D0), .Z(LUT4_0));
	LUT2 #(.INIT(INIT0[3:0])) lut2_0(.A(A0), .B(B0), .Z(LUT2_0));
	wire gated_cin_0 = (INJECT1_0 == "YES") ? 1'b0 : CIN;
	assign S0 = LUT4_0 ^ gated_cin_0;

	wire gated_lut2_0 = (INJECT1_0 == "YES") ? 1'b0 : LUT2_0;
	wire cout_0 = (~LUT4_0 & gated_lut2_0) | (LUT4_0 & CIN);

	// Second half
	wire LUT4_1, LUT2_1;
	LUT4 #(.INIT(INIT1)) lut4_1(.A(A1), .B(B1), .C(C1), .D(D1), .Z(LUT4_1));
	LUT2 #(.INIT(INIT1[3:0])) lut2_1(.A(A1), .B(B1), .Z(LUT2_1));
	wire gated_cin_1 = (INJECT1_1 == "YES") ? 1'b0 : cout_0;
	assign S1 = LUT4_1 ^ gated_cin_1;

	wire gated_lut2_1 = (INJECT1_1 == "YES") ? 1'b0 : LUT2_1;
	assign COUT = (~LUT4_1 & gated_lut2_1) | (LUT4_1 & cout_0);

	
endmodule
module TRELLIS_DPR16X4 (
	input  [3:0] DI,
	input  [3:0] WAD,
	input        WRE,
	input        WCK,
	input  [3:0] RAD,
	output [3:0] DO
);
	parameter WCKMUX = "WCK";
	parameter WREMUX = "WRE";
	parameter [63:0] INITVAL = 64'h0000000000000000;

	reg [3:0] mem[15:0];

	integer i;
	initial begin
		for (i = 0; i < 16; i = i + 1)
			mem[i] <= INITVAL[4*i +: 4];
	end

	wire muxwck = (WCKMUX == "INV") ? ~WCK : WCK;

	reg muxwre;
	always @(*)
		case (WREMUX)
			"1": muxwre = 1'b1;
			"0": muxwre = 1'b0;
			"INV": muxwre = ~WRE;
			default: muxwre = WRE;
		endcase

	always @(posedge muxwck)
		if (muxwre)
			mem[WAD] <= DI;

	assign DO = mem[RAD];

	
endmodule
module TRELLIS_FF(input CLK, LSR, CE, DI, M, output reg Q);
	parameter GSR = "ENABLED";
	parameter [127:0] CEMUX = "1";
	parameter CLKMUX = "CLK";
	parameter LSRMUX = "LSR";
	parameter SRMODE = "LSR_OVER_CE";
	parameter REGSET = "RESET";
	parameter [127:0] LSRMODE = "LSR";

	wire muxce;
	generate
		case (CEMUX)
			"1": assign muxce = 1'b1;
			"0": assign muxce = 1'b0;
			"INV": assign muxce = ~CE;
			default: assign muxce = CE;
		endcase
	endgenerate

	wire muxlsr = (LSRMUX == "INV") ? ~LSR : LSR;
	wire muxclk = (CLKMUX == "INV") ? ~CLK : CLK;
	wire srval;
	generate
		if (LSRMODE == "PRLD")
			assign srval = M;
		else
			assign srval = (REGSET == "SET") ? 1'b1 : 1'b0;
	endgenerate

	initial Q = srval;

	generate
		if (SRMODE == "ASYNC") begin
			always @(posedge muxclk, posedge muxlsr)
				if (muxlsr)
					Q <= srval;
				else if (muxce)
					Q <= DI;
		end else begin
			always @(posedge muxclk)
				if (muxlsr)
					Q <= srval;
				else if (muxce)
					Q <= DI;
		end
	endgenerate

	
endmodule
module MULT18X18D(input wire A0,input wire A1,input wire A10,input wire A11,input wire A12,input wire A13,input wire A14,input wire A15,input wire A16,input wire A17,input wire A2,input wire A3,input wire A4,input wire A5,input wire A6,input wire A7,input wire A8,input wire A9,input wire B0,input wire B1,input wire B10,input wire B11,input wire B12,input wire B13,input wire B14,input wire B15,input wire B16,input wire B17,input wire B2,input wire B3,input wire B4,input wire B5,input wire B6,input wire B7,input wire B8,input wire B9,input wire C0,input wire C1,input wire C10,input wire C11,input wire C12,input wire C13,input wire C14,input wire C15,input wire C16,input wire C17,input wire C2,input wire C3,input wire C4,input wire C5,input wire C6,input wire C7,input wire C8,input wire C9,output wire P0,output wire P1,output wire P10,output wire P11,output wire P12,output wire P13,output wire P14,output wire P15,output wire P16,output wire P17,output wire P18,output wire P19,output wire P2,output wire P20,output wire P21,output wire P22,output wire P23,output wire P24,output wire P25,output wire P26,output wire P27,output wire P28,output wire P29,output wire P3,output wire P30,output wire P31,output wire P32,output wire P33,output wire P34,output wire P35,output wire P4,output wire P5,output wire P6,output wire P7,output wire P8,output wire P9,input wire SIGNEDA,input wire SIGNEDB,input wire SOURCEA,input wire SOURCEB);
wire signed [18:0] a={SIGNEDA && A17,{A17,A16,A15,A14,A13,A12,A11,A10,A9,A8,A7,A6,A5,A4,A3,A2,A1,A0}};
wire signed [18:0] b={SIGNEDB && B17,{B17,B16,B15,B14,B13,B12,B11,B10,B9,B8,B7,B6,B5,B4,B3,B2,B1,B0}};
wire signed [37:0] product=a*b;
assign {P35,P34,P33,P32,P31,P30,P29,P28,P27,P26,P25,P24,P23,P22,P21,P20,P19,P18,P17,P16,P15,P14,P13,P12,P11,P10,P9,P8,P7,P6,P5,P4,P3,P2,P1,P0}=product[35:0];
endmodule
module DCCA(input wire CLKI,CE,output wire CLKO); assign CLKO=CLKI & CE; endmodule
module DP16KD (input wire DIA0,
input wire DIA1,
input wire DIA2,
input wire DIA3,
input wire DIA4,
input wire DIA5,
input wire DIA6,
input wire DIA7,
input wire DIA8,
input wire DIA9,
input wire DIA10,
input wire DIA11,
input wire DIA12,
input wire DIA13,
input wire DIA14,
input wire DIA15,
input wire DIA16,
input wire DIA17,
input wire ADA0,
input wire ADA1,
input wire ADA2,
input wire ADA3,
input wire ADA4,
input wire ADA5,
input wire ADA6,
input wire ADA7,
input wire ADA8,
input wire ADA9,
input wire ADA10,
input wire ADA11,
input wire ADA12,
input wire ADA13,
input wire CSA0,
input wire CSA1,
input wire CSA2,
input wire CEA,
input wire OCEA,
input wire CLKA,
input wire WEA,
input wire RSTA,
output wire DOA0,
output wire DOA1,
output wire DOA2,
output wire DOA3,
output wire DOA4,
output wire DOA5,
output wire DOA6,
output wire DOA7,
output wire DOA8,
output wire DOA9,
output wire DOA10,
output wire DOA11,
output wire DOA12,
output wire DOA13,
output wire DOA14,
output wire DOA15,
output wire DOA16,
output wire DOA17,
input wire DIB0,
input wire DIB1,
input wire DIB2,
input wire DIB3,
input wire DIB4,
input wire DIB5,
input wire DIB6,
input wire DIB7,
input wire DIB8,
input wire DIB9,
input wire DIB10,
input wire DIB11,
input wire DIB12,
input wire DIB13,
input wire DIB14,
input wire DIB15,
input wire DIB16,
input wire DIB17,
input wire ADB0,
input wire ADB1,
input wire ADB2,
input wire ADB3,
input wire ADB4,
input wire ADB5,
input wire ADB6,
input wire ADB7,
input wire ADB8,
input wire ADB9,
input wire ADB10,
input wire ADB11,
input wire ADB12,
input wire ADB13,
input wire CSB0,
input wire CSB1,
input wire CSB2,
input wire CEB,
input wire OCEB,
input wire CLKB,
input wire WEB,
input wire RSTB,
output wire DOB0,
output wire DOB1,
output wire DOB2,
output wire DOB3,
output wire DOB4,
output wire DOB5,
output wire DOB6,
output wire DOB7,
output wire DOB8,
output wire DOB9,
output wire DOB10,
output wire DOB11,
output wire DOB12,
output wire DOB13,
output wire DOB14,
output wire DOB15,
output wire DOB16,
output wire DOB17);
parameter REGMODE_A="NOREG";
parameter REGMODE_B="NOREG";
parameter CLKAMUX="CLKA";
parameter CLKBMUX="INV";
parameter RESETMODE="ASYNC";
parameter ASYNC_RESET_RELEASE="ASYNC";
parameter CSDECODE_A="0b000";
parameter CSDECODE_B="0b000";
parameter WRITEMODE_A="NORMAL";
parameter WRITEMODE_B="NORMAL";
parameter GSR="DISABLED";
parameter DATA_WIDTH_A=36, DATA_WIDTH_B=36;
parameter [319:0] INITVAL_00=320'b0;
parameter [319:0] INITVAL_01=320'b0;
parameter [319:0] INITVAL_02=320'b0;
parameter [319:0] INITVAL_03=320'b0;
parameter [319:0] INITVAL_04=320'b0;
parameter [319:0] INITVAL_05=320'b0;
parameter [319:0] INITVAL_06=320'b0;
parameter [319:0] INITVAL_07=320'b0;
parameter [319:0] INITVAL_08=320'b0;
parameter [319:0] INITVAL_09=320'b0;
parameter [319:0] INITVAL_0A=320'b0;
parameter [319:0] INITVAL_0B=320'b0;
parameter [319:0] INITVAL_0C=320'b0;
parameter [319:0] INITVAL_0D=320'b0;
parameter [319:0] INITVAL_0E=320'b0;
parameter [319:0] INITVAL_0F=320'b0;
parameter [319:0] INITVAL_10=320'b0;
parameter [319:0] INITVAL_11=320'b0;
parameter [319:0] INITVAL_12=320'b0;
parameter [319:0] INITVAL_13=320'b0;
parameter [319:0] INITVAL_14=320'b0;
parameter [319:0] INITVAL_15=320'b0;
parameter [319:0] INITVAL_16=320'b0;
parameter [319:0] INITVAL_17=320'b0;
parameter [319:0] INITVAL_18=320'b0;
parameter [319:0] INITVAL_19=320'b0;
parameter [319:0] INITVAL_1A=320'b0;
parameter [319:0] INITVAL_1B=320'b0;
parameter [319:0] INITVAL_1C=320'b0;
parameter [319:0] INITVAL_1D=320'b0;
parameter [319:0] INITVAL_1E=320'b0;
parameter [319:0] INITVAL_1F=320'b0;
parameter [319:0] INITVAL_20=320'b0;
parameter [319:0] INITVAL_21=320'b0;
parameter [319:0] INITVAL_22=320'b0;
parameter [319:0] INITVAL_23=320'b0;
parameter [319:0] INITVAL_24=320'b0;
parameter [319:0] INITVAL_25=320'b0;
parameter [319:0] INITVAL_26=320'b0;
parameter [319:0] INITVAL_27=320'b0;
parameter [319:0] INITVAL_28=320'b0;
parameter [319:0] INITVAL_29=320'b0;
parameter [319:0] INITVAL_2A=320'b0;
parameter [319:0] INITVAL_2B=320'b0;
parameter [319:0] INITVAL_2C=320'b0;
parameter [319:0] INITVAL_2D=320'b0;
parameter [319:0] INITVAL_2E=320'b0;
parameter [319:0] INITVAL_2F=320'b0;
parameter [319:0] INITVAL_30=320'b0;
parameter [319:0] INITVAL_31=320'b0;
parameter [319:0] INITVAL_32=320'b0;
parameter [319:0] INITVAL_33=320'b0;
parameter [319:0] INITVAL_34=320'b0;
parameter [319:0] INITVAL_35=320'b0;
parameter [319:0] INITVAL_36=320'b0;
parameter [319:0] INITVAL_37=320'b0;
parameter [319:0] INITVAL_38=320'b0;
parameter [319:0] INITVAL_39=320'b0;
parameter [319:0] INITVAL_3A=320'b0;
parameter [319:0] INITVAL_3B=320'b0;
parameter [319:0] INITVAL_3C=320'b0;
parameter [319:0] INITVAL_3D=320'b0;
parameter [319:0] INITVAL_3E=320'b0;
parameter [319:0] INITVAL_3F=320'b0;
wire [35:0] data_in={{DIB17,DIB16,DIB15,DIB14,DIB13,DIB12,DIB11,DIB10,DIB9,DIB8,DIB7,DIB6,DIB5,DIB4,DIB3,DIB2,DIB1,DIB0},{DIA17,DIA16,DIA15,DIA14,DIA13,DIA12,DIA11,DIA10,DIA9,DIA8,DIA7,DIA6,DIA5,DIA4,DIA3,DIA2,DIA1,DIA0}};
wire [13:0] address_a={ADA13,ADA12,ADA11,ADA10,ADA9,ADA8,ADA7,ADA6,ADA5,ADA4,ADA3,ADA2,ADA1,ADA0};
wire [13:0] address_b={ADB13,ADB12,ADB11,ADB10,ADB9,ADB8,ADB7,ADB6,ADB5,ADB4,ADB3,ADB2,ADB1,ADB0};
localparam [20479:0] INITIAL={INITVAL_3F,INITVAL_3E,INITVAL_3D,INITVAL_3C,INITVAL_3B,INITVAL_3A,INITVAL_39,INITVAL_38,INITVAL_37,INITVAL_36,INITVAL_35,INITVAL_34,INITVAL_33,INITVAL_32,INITVAL_31,INITVAL_30,INITVAL_2F,INITVAL_2E,INITVAL_2D,INITVAL_2C,INITVAL_2B,INITVAL_2A,INITVAL_29,INITVAL_28,INITVAL_27,INITVAL_26,INITVAL_25,INITVAL_24,INITVAL_23,INITVAL_22,INITVAL_21,INITVAL_20,INITVAL_1F,INITVAL_1E,INITVAL_1D,INITVAL_1C,INITVAL_1B,INITVAL_1A,INITVAL_19,INITVAL_18,INITVAL_17,INITVAL_16,INITVAL_15,INITVAL_14,INITVAL_13,INITVAL_12,INITVAL_11,INITVAL_10,INITVAL_0F,INITVAL_0E,INITVAL_0D,INITVAL_0C,INITVAL_0B,INITVAL_0A,INITVAL_09,INITVAL_08,INITVAL_07,INITVAL_06,INITVAL_05,INITVAL_04,INITVAL_03,INITVAL_02,INITVAL_01,INITVAL_00};
generate if(DATA_WIDTH_A==36) begin: wide
reg [35:0] memory [0:511];
reg [35:0] read_value;
assign {{DOB17,DOB16,DOB15,DOB14,DOB13,DOB12,DOB11,DOB10,DOB9,DOB8,DOB7,DOB6,DOB5,DOB4,DOB3,DOB2,DOB1,DOB0},{DOA17,DOA16,DOA15,DOA14,DOA13,DOA12,DOA11,DOA10,DOA9,DOA8,DOA7,DOA6,DOA5,DOA4,DOA3,DOA2,DOA1,DOA0}}=read_value;
integer row,lane;
initial begin
    for(row=0;row<512;row=row+1)
        memory[row]={INITIAL[(2*row+1)*20+:18],INITIAL[2*row*20+:18]};
end
// The low four address pins enable separate nine-bit write lanes.
always @(posedge CLKA) if(CEA && WEA) begin
    for(lane=0;lane<4;lane=lane+1)
        if(address_a[lane]) memory[address_a[13:5]][lane*9+:9]<=data_in[lane*9+:9];
end
// NOREG omits the additional output pipeline, not the clocked read.
always @(negedge CLKB) if(CEB) read_value<=memory[address_b[13:5]];
end else begin: narrow
reg [8:0] memory [0:2047];
reg [8:0] read_a,read_b;
assign {DOA17,DOA16,DOA15,DOA14,DOA13,DOA12,DOA11,DOA10,DOA9,DOA8,DOA7,DOA6,DOA5,DOA4,DOA3,DOA2,DOA1,DOA0}={9'b0,read_a};
assign {DOB17,DOB16,DOB15,DOB14,DOB13,DOB12,DOB11,DOB10,DOB9,DOB8,DOB7,DOB6,DOB5,DOB4,DOB3,DOB2,DOB1,DOB0}={9'b0,read_b};
integer row;
initial for(row=0;row<2048;row=row+1)
    memory[row]=INITIAL[(row/2)*20+(row%2)*9+:9];
always @(posedge CLKA) if(CEA) begin
    read_a<=memory[address_a[13:3]];
    if(WEA) memory[address_a[13:3]]<=data_in[8:0];
end
always @(negedge CLKB) if(CEB) read_b<=memory[address_b[13:3]];
end endgenerate
endmodule

module WASMETAL_LOCAL_DP16KD (input wire DIA0,
input wire DIA1,
input wire DIA2,
input wire DIA3,
input wire DIA4,
input wire DIA5,
input wire DIA6,
input wire DIA7,
input wire DIA8,
input wire DIA9,
input wire DIA10,
input wire DIA11,
input wire DIA12,
input wire DIA13,
input wire DIA14,
input wire DIA15,
input wire DIA16,
input wire DIA17,
input wire ADA0,
input wire ADA1,
input wire ADA2,
input wire ADA3,
input wire ADA4,
input wire ADA5,
input wire ADA6,
input wire ADA7,
input wire ADA8,
input wire ADA9,
input wire ADA10,
input wire ADA11,
input wire ADA12,
input wire ADA13,
input wire CSA0,
input wire CSA1,
input wire CSA2,
input wire CEA,
input wire OCEA,
input wire CLKA,
input wire WEA,
input wire RSTA,
output wire DOA0,
output wire DOA1,
output wire DOA2,
output wire DOA3,
output wire DOA4,
output wire DOA5,
output wire DOA6,
output wire DOA7,
output wire DOA8,
output wire DOA9,
output wire DOA10,
output wire DOA11,
output wire DOA12,
output wire DOA13,
output wire DOA14,
output wire DOA15,
output wire DOA16,
output wire DOA17,
input wire DIB0,
input wire DIB1,
input wire DIB2,
input wire DIB3,
input wire DIB4,
input wire DIB5,
input wire DIB6,
input wire DIB7,
input wire DIB8,
input wire DIB9,
input wire DIB10,
input wire DIB11,
input wire DIB12,
input wire DIB13,
input wire DIB14,
input wire DIB15,
input wire DIB16,
input wire DIB17,
input wire ADB0,
input wire ADB1,
input wire ADB2,
input wire ADB3,
input wire ADB4,
input wire ADB5,
input wire ADB6,
input wire ADB7,
input wire ADB8,
input wire ADB9,
input wire ADB10,
input wire ADB11,
input wire ADB12,
input wire ADB13,
input wire CSB0,
input wire CSB1,
input wire CSB2,
input wire CEB,
input wire OCEB,
input wire CLKB,
input wire WEB,
input wire RSTB,
output wire DOB0,
output wire DOB1,
output wire DOB2,
output wire DOB3,
output wire DOB4,
output wire DOB5,
output wire DOB6,
output wire DOB7,
output wire DOB8,
output wire DOB9,
output wire DOB10,
output wire DOB11,
output wire DOB12,
output wire DOB13,
output wire DOB14,
output wire DOB15,
output wire DOB16,
output wire DOB17);
parameter REGMODE_A="NOREG";
parameter REGMODE_B="NOREG";
parameter CLKAMUX="CLKA";
parameter CLKBMUX="INV";
parameter RESETMODE="ASYNC";
parameter ASYNC_RESET_RELEASE="ASYNC";
parameter CSDECODE_A="0b000";
parameter CSDECODE_B="0b000";
parameter WRITEMODE_A="NORMAL";
parameter WRITEMODE_B="NORMAL";
parameter GSR="DISABLED";
parameter DATA_WIDTH_A=36, DATA_WIDTH_B=36;
parameter [319:0] INITVAL_00=320'b0;
parameter [319:0] INITVAL_01=320'b0;
parameter [319:0] INITVAL_02=320'b0;
parameter [319:0] INITVAL_03=320'b0;
parameter [319:0] INITVAL_04=320'b0;
parameter [319:0] INITVAL_05=320'b0;
parameter [319:0] INITVAL_06=320'b0;
parameter [319:0] INITVAL_07=320'b0;
parameter [319:0] INITVAL_08=320'b0;
parameter [319:0] INITVAL_09=320'b0;
parameter [319:0] INITVAL_0A=320'b0;
parameter [319:0] INITVAL_0B=320'b0;
parameter [319:0] INITVAL_0C=320'b0;
parameter [319:0] INITVAL_0D=320'b0;
parameter [319:0] INITVAL_0E=320'b0;
parameter [319:0] INITVAL_0F=320'b0;
parameter [319:0] INITVAL_10=320'b0;
parameter [319:0] INITVAL_11=320'b0;
parameter [319:0] INITVAL_12=320'b0;
parameter [319:0] INITVAL_13=320'b0;
parameter [319:0] INITVAL_14=320'b0;
parameter [319:0] INITVAL_15=320'b0;
parameter [319:0] INITVAL_16=320'b0;
parameter [319:0] INITVAL_17=320'b0;
parameter [319:0] INITVAL_18=320'b0;
parameter [319:0] INITVAL_19=320'b0;
parameter [319:0] INITVAL_1A=320'b0;
parameter [319:0] INITVAL_1B=320'b0;
parameter [319:0] INITVAL_1C=320'b0;
parameter [319:0] INITVAL_1D=320'b0;
parameter [319:0] INITVAL_1E=320'b0;
parameter [319:0] INITVAL_1F=320'b0;
parameter [319:0] INITVAL_20=320'b0;
parameter [319:0] INITVAL_21=320'b0;
parameter [319:0] INITVAL_22=320'b0;
parameter [319:0] INITVAL_23=320'b0;
parameter [319:0] INITVAL_24=320'b0;
parameter [319:0] INITVAL_25=320'b0;
parameter [319:0] INITVAL_26=320'b0;
parameter [319:0] INITVAL_27=320'b0;
parameter [319:0] INITVAL_28=320'b0;
parameter [319:0] INITVAL_29=320'b0;
parameter [319:0] INITVAL_2A=320'b0;
parameter [319:0] INITVAL_2B=320'b0;
parameter [319:0] INITVAL_2C=320'b0;
parameter [319:0] INITVAL_2D=320'b0;
parameter [319:0] INITVAL_2E=320'b0;
parameter [319:0] INITVAL_2F=320'b0;
parameter [319:0] INITVAL_30=320'b0;
parameter [319:0] INITVAL_31=320'b0;
parameter [319:0] INITVAL_32=320'b0;
parameter [319:0] INITVAL_33=320'b0;
parameter [319:0] INITVAL_34=320'b0;
parameter [319:0] INITVAL_35=320'b0;
parameter [319:0] INITVAL_36=320'b0;
parameter [319:0] INITVAL_37=320'b0;
parameter [319:0] INITVAL_38=320'b0;
parameter [319:0] INITVAL_39=320'b0;
parameter [319:0] INITVAL_3A=320'b0;
parameter [319:0] INITVAL_3B=320'b0;
parameter [319:0] INITVAL_3C=320'b0;
parameter [319:0] INITVAL_3D=320'b0;
parameter [319:0] INITVAL_3E=320'b0;
parameter [319:0] INITVAL_3F=320'b0;
localparam [20479:0] INITIAL={INITVAL_3F,INITVAL_3E,INITVAL_3D,INITVAL_3C,INITVAL_3B,INITVAL_3A,INITVAL_39,INITVAL_38,INITVAL_37,INITVAL_36,INITVAL_35,INITVAL_34,INITVAL_33,INITVAL_32,INITVAL_31,INITVAL_30,INITVAL_2F,INITVAL_2E,INITVAL_2D,INITVAL_2C,INITVAL_2B,INITVAL_2A,INITVAL_29,INITVAL_28,INITVAL_27,INITVAL_26,INITVAL_25,INITVAL_24,INITVAL_23,INITVAL_22,INITVAL_21,INITVAL_20,INITVAL_1F,INITVAL_1E,INITVAL_1D,INITVAL_1C,INITVAL_1B,INITVAL_1A,INITVAL_19,INITVAL_18,INITVAL_17,INITVAL_16,INITVAL_15,INITVAL_14,INITVAL_13,INITVAL_12,INITVAL_11,INITVAL_10,INITVAL_0F,INITVAL_0E,INITVAL_0D,INITVAL_0C,INITVAL_0B,INITVAL_0A,INITVAL_09,INITVAL_08,INITVAL_07,INITVAL_06,INITVAL_05,INITVAL_04,INITVAL_03,INITVAL_02,INITVAL_01,INITVAL_00};
wire [13:0] address_a={ADA13,ADA12,ADA11,ADA10,ADA9,ADA8,ADA7,ADA6,ADA5,ADA4,ADA3,ADA2,ADA1,ADA0};
wire clock_a=CLKAMUX=="INV" ? !CLKA : CLKA;
wire clock_b_for_negedge=CLKBMUX=="INV" ? CLKB : !CLKB;
generate if(DATA_WIDTH_A==36) begin: readonly_wide
DP16KD #(.REGMODE_A(REGMODE_A),.REGMODE_B(REGMODE_B),.CLKAMUX(CLKAMUX),.CLKBMUX(CLKBMUX),.RESETMODE(RESETMODE),.ASYNC_RESET_RELEASE(ASYNC_RESET_RELEASE),.CSDECODE_A(CSDECODE_A),.CSDECODE_B(CSDECODE_B),.WRITEMODE_A(WRITEMODE_A),.WRITEMODE_B(WRITEMODE_B),.GSR(GSR),.DATA_WIDTH_A(DATA_WIDTH_A),.DATA_WIDTH_B(DATA_WIDTH_B),.INITVAL_00(INITVAL_00),.INITVAL_01(INITVAL_01),.INITVAL_02(INITVAL_02),.INITVAL_03(INITVAL_03),.INITVAL_04(INITVAL_04),.INITVAL_05(INITVAL_05),.INITVAL_06(INITVAL_06),.INITVAL_07(INITVAL_07),.INITVAL_08(INITVAL_08),.INITVAL_09(INITVAL_09),.INITVAL_0A(INITVAL_0A),.INITVAL_0B(INITVAL_0B),.INITVAL_0C(INITVAL_0C),.INITVAL_0D(INITVAL_0D),.INITVAL_0E(INITVAL_0E),.INITVAL_0F(INITVAL_0F),.INITVAL_10(INITVAL_10),.INITVAL_11(INITVAL_11),.INITVAL_12(INITVAL_12),.INITVAL_13(INITVAL_13),.INITVAL_14(INITVAL_14),.INITVAL_15(INITVAL_15),.INITVAL_16(INITVAL_16),.INITVAL_17(INITVAL_17),.INITVAL_18(INITVAL_18),.INITVAL_19(INITVAL_19),.INITVAL_1A(INITVAL_1A),.INITVAL_1B(INITVAL_1B),.INITVAL_1C(INITVAL_1C),.INITVAL_1D(INITVAL_1D),.INITVAL_1E(INITVAL_1E),.INITVAL_1F(INITVAL_1F),.INITVAL_20(INITVAL_20),.INITVAL_21(INITVAL_21),.INITVAL_22(INITVAL_22),.INITVAL_23(INITVAL_23),.INITVAL_24(INITVAL_24),.INITVAL_25(INITVAL_25),.INITVAL_26(INITVAL_26),.INITVAL_27(INITVAL_27),.INITVAL_28(INITVAL_28),.INITVAL_29(INITVAL_29),.INITVAL_2A(INITVAL_2A),.INITVAL_2B(INITVAL_2B),.INITVAL_2C(INITVAL_2C),.INITVAL_2D(INITVAL_2D),.INITVAL_2E(INITVAL_2E),.INITVAL_2F(INITVAL_2F),.INITVAL_30(INITVAL_30),.INITVAL_31(INITVAL_31),.INITVAL_32(INITVAL_32),.INITVAL_33(INITVAL_33),.INITVAL_34(INITVAL_34),.INITVAL_35(INITVAL_35),.INITVAL_36(INITVAL_36),.INITVAL_37(INITVAL_37),.INITVAL_38(INITVAL_38),.INITVAL_39(INITVAL_39),.INITVAL_3A(INITVAL_3A),.INITVAL_3B(INITVAL_3B),.INITVAL_3C(INITVAL_3C),.INITVAL_3D(INITVAL_3D),.INITVAL_3E(INITVAL_3E),.INITVAL_3F(INITVAL_3F)) storage(.DIA0(DIA0),.DIA1(DIA1),.DIA2(DIA2),.DIA3(DIA3),.DIA4(DIA4),.DIA5(DIA5),.DIA6(DIA6),.DIA7(DIA7),.DIA8(DIA8),.DIA9(DIA9),.DIA10(DIA10),.DIA11(DIA11),.DIA12(DIA12),.DIA13(DIA13),.DIA14(DIA14),.DIA15(DIA15),.DIA16(DIA16),.DIA17(DIA17),.ADA0(ADA0),.ADA1(ADA1),.ADA2(ADA2),.ADA3(ADA3),.ADA4(ADA4),.ADA5(ADA5),.ADA6(ADA6),.ADA7(ADA7),.ADA8(ADA8),.ADA9(ADA9),.ADA10(ADA10),.ADA11(ADA11),.ADA12(ADA12),.ADA13(ADA13),.CSA0(CSA0),.CSA1(CSA1),.CSA2(CSA2),.CEA(CEA),.OCEA(OCEA),.CLKA(CLKA),.WEA(WEA),.RSTA(RSTA),.DOA0(DOA0),.DOA1(DOA1),.DOA2(DOA2),.DOA3(DOA3),.DOA4(DOA4),.DOA5(DOA5),.DOA6(DOA6),.DOA7(DOA7),.DOA8(DOA8),.DOA9(DOA9),.DOA10(DOA10),.DOA11(DOA11),.DOA12(DOA12),.DOA13(DOA13),.DOA14(DOA14),.DOA15(DOA15),.DOA16(DOA16),.DOA17(DOA17),.DIB0(DIB0),.DIB1(DIB1),.DIB2(DIB2),.DIB3(DIB3),.DIB4(DIB4),.DIB5(DIB5),.DIB6(DIB6),.DIB7(DIB7),.DIB8(DIB8),.DIB9(DIB9),.DIB10(DIB10),.DIB11(DIB11),.DIB12(DIB12),.DIB13(DIB13),.DIB14(DIB14),.DIB15(DIB15),.DIB16(DIB16),.DIB17(DIB17),.ADB0(ADB0),.ADB1(ADB1),.ADB2(ADB2),.ADB3(ADB3),.ADB4(ADB4),.ADB5(ADB5),.ADB6(ADB6),.ADB7(ADB7),.ADB8(ADB8),.ADB9(ADB9),.ADB10(ADB10),.ADB11(ADB11),.ADB12(ADB12),.ADB13(ADB13),.CSB0(CSB0),.CSB1(CSB1),.CSB2(CSB2),.CEB(CEB),.OCEB(OCEB),.CLKB(clock_b_for_negedge),.WEB(WEB),.RSTB(RSTB),.DOB0(DOB0),.DOB1(DOB1),.DOB2(DOB2),.DOB3(DOB3),.DOB4(DOB4),.DOB5(DOB5),.DOB6(DOB6),.DOB7(DOB7),.DOB8(DOB8),.DOB9(DOB9),.DOB10(DOB10),.DOB11(DOB11),.DOB12(DOB12),.DOB13(DOB13),.DOB14(DOB14),.DOB15(DOB15),.DOB16(DOB16),.DOB17(DOB17));
end else if(DATA_WIDTH_A==18) begin: readonly_word
reg [17:0] result_a;
assign {DOA17,DOA16,DOA15,DOA14,DOA13,DOA12,DOA11,DOA10,DOA9,DOA8,DOA7,DOA6,DOA5,DOA4,DOA3,DOA2,DOA1,DOA0}=result_a;
assign {DOB17,DOB16,DOB15,DOB14,DOB13,DOB12,DOB11,DOB10,DOB9,DOB8,DOB7,DOB6,DOB5,DOB4,DOB3,DOB2,DOB1,DOB0}=18'bx;
always @(posedge clock_a) if(CEA) result_a<=INITIAL[address_a[13:4]*20+:18];
end else begin: single_bit
reg memory [0:16383]; reg result_a; integer row;
initial for(row=0;row<16384;row=row+1) memory[row]=0;
assign {DOA17,DOA16,DOA15,DOA14,DOA13,DOA12,DOA11,DOA10,DOA9,DOA8,DOA7,DOA6,DOA5,DOA4,DOA3,DOA2,DOA1,DOA0}={17'bx,result_a};
assign {DOB17,DOB16,DOB15,DOB14,DOB13,DOB12,DOB11,DOB10,DOB9,DOB8,DOB7,DOB6,DOB5,DOB4,DOB3,DOB2,DOB1,DOB0}=18'bx;
always @(posedge clock_a) if(CEA) begin
    result_a<=memory[address_a];
    if(WEA) memory[address_a]<=DIA0;
end
end endgenerate
endmodule

module WASMETAL_PROGRAM_DP16KD(input wire DIA0,input wire DIA1,input wire DIA2,input wire DIA3,input wire DIA4,input wire DIA5,input wire DIA6,input wire DIA7,input wire DIA8,input wire DIA9,input wire DIA10,input wire DIA11,input wire DIA12,input wire DIA13,input wire DIA14,input wire DIA15,input wire DIA16,input wire DIA17,input wire ADA0,input wire ADA1,input wire ADA2,input wire ADA3,input wire ADA4,input wire ADA5,input wire ADA6,input wire ADA7,input wire ADA8,input wire ADA9,input wire ADA10,input wire ADA11,input wire ADA12,input wire ADA13,input wire CSA0,input wire CSA1,input wire CSA2,input wire CEA,input wire OCEA,input wire CLKA,input wire WEA,input wire RSTA,output wire DOA0,output wire DOA1,output wire DOA2,output wire DOA3,output wire DOA4,output wire DOA5,output wire DOA6,output wire DOA7,output wire DOA8,output wire DOA9,output wire DOA10,output wire DOA11,output wire DOA12,output wire DOA13,output wire DOA14,output wire DOA15,output wire DOA16,output wire DOA17,input wire DIB0,input wire DIB1,input wire DIB2,input wire DIB3,input wire DIB4,input wire DIB5,input wire DIB6,input wire DIB7,input wire DIB8,input wire DIB9,input wire DIB10,input wire DIB11,input wire DIB12,input wire DIB13,input wire DIB14,input wire DIB15,input wire DIB16,input wire DIB17,input wire ADB0,input wire ADB1,input wire ADB2,input wire ADB3,input wire ADB4,input wire ADB5,input wire ADB6,input wire ADB7,input wire ADB8,input wire ADB9,input wire ADB10,input wire ADB11,input wire ADB12,input wire ADB13,input wire CSB0,input wire CSB1,input wire CSB2,input wire CEB,input wire OCEB,input wire CLKB,input wire WEB,input wire RSTB,output wire DOB0,output wire DOB1,output wire DOB2,output wire DOB3,output wire DOB4,output wire DOB5,output wire DOB6,output wire DOB7,output wire DOB8,output wire DOB9,output wire DOB10,output wire DOB11,output wire DOB12,output wire DOB13,output wire DOB14,output wire DOB15,output wire DOB16,output wire DOB17);
parameter REGMODE_A="NOREG";
parameter REGMODE_B="NOREG";
parameter CLKAMUX="CLKA";
parameter CLKBMUX="INV";
parameter RESETMODE="ASYNC";
parameter ASYNC_RESET_RELEASE="ASYNC";
parameter CSDECODE_A="0b000";
parameter CSDECODE_B="0b000";
parameter WRITEMODE_A="NORMAL";
parameter WRITEMODE_B="NORMAL";
parameter GSR="DISABLED";
parameter DATA_WIDTH_A=18,DATA_WIDTH_B=18;
parameter [319:0] INITVAL_00=320'bx;
parameter [319:0] INITVAL_01=320'bx;
parameter [319:0] INITVAL_02=320'bx;
parameter [319:0] INITVAL_03=320'bx;
parameter [319:0] INITVAL_04=320'bx;
parameter [319:0] INITVAL_05=320'bx;
parameter [319:0] INITVAL_06=320'bx;
parameter [319:0] INITVAL_07=320'bx;
parameter [319:0] INITVAL_08=320'bx;
parameter [319:0] INITVAL_09=320'bx;
parameter [319:0] INITVAL_0A=320'bx;
parameter [319:0] INITVAL_0B=320'bx;
parameter [319:0] INITVAL_0C=320'bx;
parameter [319:0] INITVAL_0D=320'bx;
parameter [319:0] INITVAL_0E=320'bx;
parameter [319:0] INITVAL_0F=320'bx;
parameter [319:0] INITVAL_10=320'bx;
parameter [319:0] INITVAL_11=320'bx;
parameter [319:0] INITVAL_12=320'bx;
parameter [319:0] INITVAL_13=320'bx;
parameter [319:0] INITVAL_14=320'bx;
parameter [319:0] INITVAL_15=320'bx;
parameter [319:0] INITVAL_16=320'bx;
parameter [319:0] INITVAL_17=320'bx;
parameter [319:0] INITVAL_18=320'bx;
parameter [319:0] INITVAL_19=320'bx;
parameter [319:0] INITVAL_1A=320'bx;
parameter [319:0] INITVAL_1B=320'bx;
parameter [319:0] INITVAL_1C=320'bx;
parameter [319:0] INITVAL_1D=320'bx;
parameter [319:0] INITVAL_1E=320'bx;
parameter [319:0] INITVAL_1F=320'bx;
parameter [319:0] INITVAL_20=320'bx;
parameter [319:0] INITVAL_21=320'bx;
parameter [319:0] INITVAL_22=320'bx;
parameter [319:0] INITVAL_23=320'bx;
parameter [319:0] INITVAL_24=320'bx;
parameter [319:0] INITVAL_25=320'bx;
parameter [319:0] INITVAL_26=320'bx;
parameter [319:0] INITVAL_27=320'bx;
parameter [319:0] INITVAL_28=320'bx;
parameter [319:0] INITVAL_29=320'bx;
parameter [319:0] INITVAL_2A=320'bx;
parameter [319:0] INITVAL_2B=320'bx;
parameter [319:0] INITVAL_2C=320'bx;
parameter [319:0] INITVAL_2D=320'bx;
parameter [319:0] INITVAL_2E=320'bx;
parameter [319:0] INITVAL_2F=320'bx;
parameter [319:0] INITVAL_30=320'bx;
parameter [319:0] INITVAL_31=320'bx;
parameter [319:0] INITVAL_32=320'bx;
parameter [319:0] INITVAL_33=320'bx;
parameter [319:0] INITVAL_34=320'bx;
parameter [319:0] INITVAL_35=320'bx;
parameter [319:0] INITVAL_36=320'bx;
parameter [319:0] INITVAL_37=320'bx;
parameter [319:0] INITVAL_38=320'bx;
parameter [319:0] INITVAL_39=320'bx;
parameter [319:0] INITVAL_3A=320'bx;
parameter [319:0] INITVAL_3B=320'bx;
parameter [319:0] INITVAL_3C=320'bx;
parameter [319:0] INITVAL_3D=320'bx;
parameter [319:0] INITVAL_3E=320'bx;
parameter [319:0] INITVAL_3F=320'bx;
localparam [20479:0] INITIAL={INITVAL_3F,INITVAL_3E,INITVAL_3D,INITVAL_3C,INITVAL_3B,INITVAL_3A,INITVAL_39,INITVAL_38,INITVAL_37,INITVAL_36,INITVAL_35,INITVAL_34,INITVAL_33,INITVAL_32,INITVAL_31,INITVAL_30,INITVAL_2F,INITVAL_2E,INITVAL_2D,INITVAL_2C,INITVAL_2B,INITVAL_2A,INITVAL_29,INITVAL_28,INITVAL_27,INITVAL_26,INITVAL_25,INITVAL_24,INITVAL_23,INITVAL_22,INITVAL_21,INITVAL_20,INITVAL_1F,INITVAL_1E,INITVAL_1D,INITVAL_1C,INITVAL_1B,INITVAL_1A,INITVAL_19,INITVAL_18,INITVAL_17,INITVAL_16,INITVAL_15,INITVAL_14,INITVAL_13,INITVAL_12,INITVAL_11,INITVAL_10,INITVAL_0F,INITVAL_0E,INITVAL_0D,INITVAL_0C,INITVAL_0B,INITVAL_0A,INITVAL_09,INITVAL_08,INITVAL_07,INITVAL_06,INITVAL_05,INITVAL_04,INITVAL_03,INITVAL_02,INITVAL_01,INITVAL_00};
wire [13:0] address_a={ADA13,ADA12,ADA11,ADA10,ADA9,ADA8,ADA7,ADA6,ADA5,ADA4,ADA3,ADA2,ADA1,ADA0},address_b={ADB13,ADB12,ADB11,ADB10,ADB9,ADB8,ADB7,ADB6,ADB5,ADB4,ADB3,ADB2,ADB1,ADB0};
wire [17:0] data_a={DIA17,DIA16,DIA15,DIA14,DIA13,DIA12,DIA11,DIA10,DIA9,DIA8,DIA7,DIA6,DIA5,DIA4,DIA3,DIA2,DIA1,DIA0},data_b={DIB17,DIB16,DIB15,DIB14,DIB13,DIB12,DIB11,DIB10,DIB9,DIB8,DIB7,DIB6,DIB5,DIB4,DIB3,DIB2,DIB1,DIB0};
generate if(DATA_WIDTH_A==18) begin: instructions
reg [17:0] memory[0:1023];reg [17:0] read_a,read_b;integer row,lane;
initial for(row=0;row<1024;row=row+1) memory[row]=INITIAL[row*20+:18];
assign {DOA17,DOA16,DOA15,DOA14,DOA13,DOA12,DOA11,DOA10,DOA9,DOA8,DOA7,DOA6,DOA5,DOA4,DOA3,DOA2,DOA1,DOA0}=read_a;
assign {DOB17,DOB16,DOB15,DOB14,DOB13,DOB12,DOB11,DOB10,DOB9,DOB8,DOB7,DOB6,DOB5,DOB4,DOB3,DOB2,DOB1,DOB0}=read_b;
always @(posedge CLKA) if(CEA) begin
    read_a<=memory[address_a[13:4]];
    if(WEA) for(lane=0;lane<2;lane=lane+1)
        if(address_a[lane]) memory[address_a[13:4]][lane*9+:9]<=data_a[lane*9+:9];
end
always @(negedge CLKB) if(CEB) read_b<=memory[address_b[13:4]];
end else begin: regions
reg [35:0] memory[0:511];reg [35:0] read_value;integer row,lane;
initial for(row=0;row<512;row=row+1) memory[row]={INITIAL[(2*row+1)*20+:18],INITIAL[2*row*20+:18]};
assign {{DOB17,DOB16,DOB15,DOB14,DOB13,DOB12,DOB11,DOB10,DOB9,DOB8,DOB7,DOB6,DOB5,DOB4,DOB3,DOB2,DOB1,DOB0},{DOA17,DOA16,DOA15,DOA14,DOA13,DOA12,DOA11,DOA10,DOA9,DOA8,DOA7,DOA6,DOA5,DOA4,DOA3,DOA2,DOA1,DOA0}}=read_value;
wire [35:0] data_in={data_b,data_a};
always @(posedge CLKA) if(CEA && WEA) begin
    for(lane=0;lane<4;lane=lane+1)
        if(address_a[lane]) memory[address_a[13:5]][lane*9+:9]<=data_in[lane*9+:9];
end
always @(posedge CLKB) if(CEB) begin
    if(CEA && WEA && (|address_a[3:0]) && address_a[13:5]==address_b[13:5]) read_value<='x;
    else read_value<=memory[address_b[13:5]];
end
end endgenerate
endmodule

