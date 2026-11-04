module original2(output O, input I0, I1, input [3:0] INIT);
  
  wire [ 1: 0] s1 = I1 ? INIT[ 3: 2] : INIT[ 1: 0];
  assign O = I0 ? s1[1] : s1[0];
  
endmodule
module candidate2(output O, input I0, I1, input [3:0] INIT);
  
  wire [ 1: 0] s1 = I1 ? INIT[ 3: 2] : INIT[ 1: 0];
  assign O = INIT[{I1,I0}];
  
endmodule
