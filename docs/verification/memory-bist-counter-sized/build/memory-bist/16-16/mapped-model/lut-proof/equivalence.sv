module original2(input A, B, input [3:0] INIT, output Z);
    wire [1:0] s1 = B ?     INIT[ 3:2] :     INIT[1:0];
    assign Z =      A ?          s1[1] :         s1[0];
endmodule
module candidate2(input A, B, input [3:0] INIT, output Z);
    wire [1:0] s1 = B ?     INIT[ 3:2] :     INIT[1:0];
    assign Z = $isunknown({B,A}) ? (A ? s1[1] : s1[0]) : INIT[{B,A}];
endmodule
module original4(input A, B, C, D, input [15:0] INIT, output Z);
    wire [7:0] s3 = D ?     INIT[15:8] :     INIT[7:0];
    wire [3:0] s2 = C ?       s3[ 7:4] :       s3[3:0];
    wire [1:0] s1 = B ?       s2[ 3:2] :       s2[1:0];
    assign Z =      A ?          s1[1] :         s1[0];
    
endmodule
module candidate4(input A, B, C, D, input [15:0] INIT, output Z);
    wire [7:0] s3 = D ?     INIT[15:8] :     INIT[7:0];
    wire [3:0] s2 = C ?       s3[ 7:4] :       s3[3:0];
    wire [1:0] s1 = B ?       s2[ 3:2] :       s2[1:0];
    assign Z = $isunknown({D,C,B,A}) ? (A ? s1[1] : s1[0]) : INIT[{D,C,B,A}];
    
endmodule
module proof(input [15:0] table_value, input [3:0] pins, output mismatch);

wire a,b,c,d;
original4 u0(pins[0],pins[1],pins[2],pins[3],table_value,a);
candidate4 u1(pins[0],pins[1],pins[2],pins[3],table_value,b);
original2 u2(pins[0],pins[1],table_value[3:0],c);
candidate2 u3(pins[0],pins[1],table_value[3:0],d);
assign mismatch=(a!=b)||(c!=d);
endmodule
