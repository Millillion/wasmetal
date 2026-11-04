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
  assign O = $isunknown({I1,I0}) ? (I0 ? s1[1] : s1[0]) : INIT[{I1,I0}];
  
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
