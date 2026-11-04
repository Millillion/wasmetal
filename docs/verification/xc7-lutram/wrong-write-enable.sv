`timescale 1ps/1ps
module bench;
reg we;wire original=(we===1'bz)&&we;
initial begin
 we=0;#1000;if(original!==we)$fatal(1,"LUTRAM_WRITE_ENABLE_MISMATCH");
 we=1;#1000;if(original!==we)$fatal(1,"LUTRAM_WRITE_ENABLE_MISMATCH");
 we=1'bx;#1000;if(original!==1'bx)$fatal(1,"LUTRAM_WRITE_ENABLE_MISMATCH");
 we=1'bz;#1000;if(original!==1'b1)$fatal(1,"LUTRAM_WRITE_ENABLE_MISMATCH");
 $display("PASS all four write-enable states and complete binary specialization");$finish;
end
endmodule
