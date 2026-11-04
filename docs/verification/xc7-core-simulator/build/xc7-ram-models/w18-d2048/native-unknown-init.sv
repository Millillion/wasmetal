module ram_fixture(
input wclk,rclk,wen,ren,rst,
input [10:0] wa,ra,
input [17:0] wd,
input [1:0] wmask,
output reg [17:0] rd);
reg [17:0] memory [0:2047];
genvar lane;
generate for(lane=0;lane<2;lane=lane+1) begin
always @(posedge wclk) if(wen && wmask[lane]) memory[wa][lane*9+:9]<=wd[lane*9+:9];
end endgenerate
always @(posedge rclk) if(ren) begin
if(rst) rd<=18'h1a5a5; else rd<=memory[ra];
end
endmodule
