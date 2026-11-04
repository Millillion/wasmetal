module carry_ports(input [9:0] pins,output [7:0] observed);
CARRY4 dut(.CO(observed[7:4]),.O(observed[3:0]),.CI(pins[0]),.CYINIT(pins[1]),.DI(pins[5:2]),.S(pins[9:6]));
endmodule
