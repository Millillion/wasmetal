module ram_fixture(
input wclk,rclk,wen,ren,rst,
input [9:0] wa,ra,
input [35:0] wd,
input [3:0] wmask,
output reg [35:0] rd);
reg [35:0] memory [0:1023];
initial $readmemh("/tmp/wasmetal-direct-rounding/build/xc7-memory-mapping/w36-d1024/initial.hex",memory);
genvar lane;
generate for(lane=0;lane<4;lane=lane+1) begin
always @(posedge wclk) if(wen && wmask[lane]) memory[wa][lane*9+:9]<=wd[lane*9+:9];
end endgenerate
always @(posedge rclk) if(ren) begin
if(rst) rd<=36'h5a5a5a5a5; else rd<=memory[ra];
end
endmodule
