module original1(output O, input I0, input [1:0] INIT);
  
  assign O = I0 ? INIT[1] : INIT[0];
  
endmodule
module candidate1(output O, input I0, input [1:0] INIT);
  
  assign O = $isunknown({I0}) ? (I0 ? INIT[1] : INIT[0]) : INIT[{I0}];
  
endmodule
