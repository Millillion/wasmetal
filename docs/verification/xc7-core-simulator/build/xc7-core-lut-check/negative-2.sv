module original1(output O, input I0, input [1:0] INIT);
  
  assign O = I0 ? INIT[1] : INIT[0];
  
endmodule
module candidate1(output O, input I0, input [1:0] INIT);
  
  assign O = $isunknown({I0}) ? (I0 ? INIT[1] : INIT[0]) : INIT[{I0}];
  
endmodule
module original2(output O, input I0, I1, input [3:0] INIT);
  
  wire [ 1: 0] s1 = I1 ? INIT[ 3: 2] : INIT[ 1: 0];
  assign O = I0 ? s1[1] : s1[0];
  
endmodule
module candidate2(output O, input I0, I1, input [3:0] INIT);
  
  wire [ 1: 0] s1 = I1 ? INIT[ 3: 2] : INIT[ 1: 0];
  assign O = ~($isunknown({I1,I0}) ? (I0 ? s1[1] : s1[0]) : INIT[{I1,I0}]);
  
endmodule
module original3(output O, input I0, I1, I2, input [7:0] INIT);
  
  wire [ 3: 0] s2 = I2 ? INIT[ 7: 4] : INIT[ 3: 0];
  wire [ 1: 0] s1 = I1 ?   s2[ 3: 2] :   s2[ 1: 0];
  assign O = I0 ? s1[1] : s1[0];
  
endmodule
module candidate3(output O, input I0, I1, I2, input [7:0] INIT);
  
  wire [ 3: 0] s2 = I2 ? INIT[ 7: 4] : INIT[ 3: 0];
  wire [ 1: 0] s1 = I1 ?   s2[ 3: 2] :   s2[ 1: 0];
  assign O = $isunknown({I2,I1,I0}) ? (I0 ? s1[1] : s1[0]) : INIT[{I2,I1,I0}];
  
endmodule
module original4(output O, input I0, I1, I2, I3, input [15:0] INIT);
  
  wire [ 7: 0] s3 = I3 ? INIT[15: 8] : INIT[ 7: 0];
  wire [ 3: 0] s2 = I2 ?   s3[ 7: 4] :   s3[ 3: 0];
  wire [ 1: 0] s1 = I1 ?   s2[ 3: 2] :   s2[ 1: 0];
  assign O = I0 ? s1[1] : s1[0];
  
endmodule
module candidate4(output O, input I0, I1, I2, I3, input [15:0] INIT);
  
  wire [ 7: 0] s3 = I3 ? INIT[15: 8] : INIT[ 7: 0];
  wire [ 3: 0] s2 = I2 ?   s3[ 7: 4] :   s3[ 3: 0];
  wire [ 1: 0] s1 = I1 ?   s2[ 3: 2] :   s2[ 1: 0];
  assign O = $isunknown({I3,I2,I1,I0}) ? (I0 ? s1[1] : s1[0]) : INIT[{I3,I2,I1,I0}];
  
endmodule
module original5(output O, input I0, I1, I2, I3, I4, input [31:0] INIT);
  
  wire [15: 0] s4 = I4 ? INIT[31:16] : INIT[15: 0];
  wire [ 7: 0] s3 = I3 ?   s4[15: 8] :   s4[ 7: 0];
  wire [ 3: 0] s2 = I2 ?   s3[ 7: 4] :   s3[ 3: 0];
  wire [ 1: 0] s1 = I1 ?   s2[ 3: 2] :   s2[ 1: 0];
  assign O = I0 ? s1[1] : s1[0];
  
endmodule
module candidate5(output O, input I0, I1, I2, I3, I4, input [31:0] INIT);
  
  wire [15: 0] s4 = I4 ? INIT[31:16] : INIT[15: 0];
  wire [ 7: 0] s3 = I3 ?   s4[15: 8] :   s4[ 7: 0];
  wire [ 3: 0] s2 = I2 ?   s3[ 7: 4] :   s3[ 3: 0];
  wire [ 1: 0] s1 = I1 ?   s2[ 3: 2] :   s2[ 1: 0];
  assign O = $isunknown({I4,I3,I2,I1,I0}) ? (I0 ? s1[1] : s1[0]) : INIT[{I4,I3,I2,I1,I0}];
  
endmodule
module original6(output O, input I0, I1, I2, I3, I4, I5, input [63:0] INIT);
  
  wire [31: 0] s5 = I5 ? INIT[63:32] : INIT[31: 0];
  wire [15: 0] s4 = I4 ?   s5[31:16] :   s5[15: 0];
  wire [ 7: 0] s3 = I3 ?   s4[15: 8] :   s4[ 7: 0];
  wire [ 3: 0] s2 = I2 ?   s3[ 7: 4] :   s3[ 3: 0];
  wire [ 1: 0] s1 = I1 ?   s2[ 3: 2] :   s2[ 1: 0];
  assign O = I0 ? s1[1] : s1[0];
  
endmodule
module candidate6(output O, input I0, I1, I2, I3, I4, I5, input [63:0] INIT);
  
  wire [31: 0] s5 = I5 ? INIT[63:32] : INIT[31: 0];
  wire [15: 0] s4 = I4 ?   s5[31:16] :   s5[15: 0];
  wire [ 7: 0] s3 = I3 ?   s4[15: 8] :   s4[ 7: 0];
  wire [ 3: 0] s2 = I2 ?   s3[ 7: 4] :   s3[ 3: 0];
  wire [ 1: 0] s1 = I1 ?   s2[ 3: 2] :   s2[ 1: 0];
  assign O = $isunknown({I5,I4,I3,I2,I1,I0}) ? (I0 ? s1[1] : s1[0]) : INIT[{I5,I4,I3,I2,I1,I0}];
  
endmodule
module proof(input [63:0] table_value,input [5:0] pins,output mismatch);
wire [5:0] a,b;
original1 u_original1(.O(a[0]),.I0(pins[0]),.INIT(table_value[1:0]));
candidate1 u_candidate1(.O(b[0]),.I0(pins[0]),.INIT(table_value[1:0]));
original2 u_original2(.O(a[1]),.I0(pins[0]),.I1(pins[1]),.INIT(table_value[3:0]));
candidate2 u_candidate2(.O(b[1]),.I0(pins[0]),.I1(pins[1]),.INIT(table_value[3:0]));
original3 u_original3(.O(a[2]),.I0(pins[0]),.I1(pins[1]),.I2(pins[2]),.INIT(table_value[7:0]));
candidate3 u_candidate3(.O(b[2]),.I0(pins[0]),.I1(pins[1]),.I2(pins[2]),.INIT(table_value[7:0]));
original4 u_original4(.O(a[3]),.I0(pins[0]),.I1(pins[1]),.I2(pins[2]),.I3(pins[3]),.INIT(table_value[15:0]));
candidate4 u_candidate4(.O(b[3]),.I0(pins[0]),.I1(pins[1]),.I2(pins[2]),.I3(pins[3]),.INIT(table_value[15:0]));
original5 u_original5(.O(a[4]),.I0(pins[0]),.I1(pins[1]),.I2(pins[2]),.I3(pins[3]),.I4(pins[4]),.INIT(table_value[31:0]));
candidate5 u_candidate5(.O(b[4]),.I0(pins[0]),.I1(pins[1]),.I2(pins[2]),.I3(pins[3]),.I4(pins[4]),.INIT(table_value[31:0]));
original6 u_original6(.O(a[5]),.I0(pins[0]),.I1(pins[1]),.I2(pins[2]),.I3(pins[3]),.I4(pins[4]),.I5(pins[5]),.INIT(table_value[63:0]));
candidate6 u_candidate6(.O(b[5]),.I0(pins[0]),.I1(pins[1]),.I2(pins[2]),.I3(pins[3]),.I4(pins[4]),.I5(pins[5]),.INIT(table_value[63:0]));
assign mismatch = |(a ^ b);
endmodule
