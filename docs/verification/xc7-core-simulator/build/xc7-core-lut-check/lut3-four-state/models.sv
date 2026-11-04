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
