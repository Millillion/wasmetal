module cycle(input wire toggle,output wire result);
wire feedback;assign feedback=result;assign result=feedback^toggle;
endmodule
