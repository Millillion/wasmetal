// SPDX-License-Identifier: MIT
`timescale 1ns/1ps
module image_loader_tb;
    reg clk=0,reset=1,abort_load=0,rx_valid=0,tx_ready=1;
    reg [7:0] rx_data=0;
    wire tx_valid,image_valid,word_valid;
    wire [7:0] tx_data;
    wire [2:0] word_section;
    wire [31:0] word_index;
    wire [287:0] word_data;
    reg [7:0] packet [0:440];
    integer reply_count,reply_position,word_count;
    reg [7:0] last_status;
    wasmetal_image_loader #(.INSTRUCTION_DEPTH(4),.FUNCTION_DEPTH(2),.TYPE_DEPTH(8),
        .BOOT_DEPTH(4),.REGIONS_PER_KIND(2),.TIMEOUT_CYCLES(64),
        .PROFILE_TAG(128'h0f0e0d0c0b0a09080706050403020100)) dut(.*);
    always #1 clk=~clk;
    always @(posedge clk) begin
        if(reset) begin reply_count=0;reply_position=0;word_count=0;last_status=0;end
        else begin
            if(word_valid) begin
                if(image_valid!==0) $fatal(1,"write to executable image");
                word_count=word_count+1;
            end
            if(tx_valid && tx_ready) begin
                if(reply_position==5) last_status=tx_data;
                if(reply_position==19) begin reply_count=reply_count+1;reply_position=0;end
                else reply_position=reply_position+1;
            end
        end
    end
    task automatic reset_device;
        begin
            @(negedge clk);reset=1;rx_valid=0;
            repeat(2) @(negedge clk);
            reset=0;
            if(image_valid!==0 || (^word_data)===1'bx || (^word_index)===1'bx)
                $fatal(1,"loader reset retained unknown state");
        end
    endtask
    task automatic send_byte(input [7:0] value);
        begin @(negedge clk);rx_valid=1;rx_data=value;end
    endtask
    task automatic wait_reply(input integer count);
        integer n;
        begin
            n=0;
            while(reply_count<count && n<200) begin @(negedge clk);n=n+1;end
            if(reply_count!=count) $fatal(1,"four-state loader reply timeout");
        end
    endtask
    initial begin
        $readmemh("build/image-loader/four-state/packet.hex",packet);
        for(integer attempt=0;attempt<2;attempt=attempt+1) begin
            reset_device();
            for(integer n=0;n<33;n=n+1) send_byte(packet[n]);
            @(negedge clk);rx_valid=0;wait_reply(1);
            if(last_status!==0 || image_valid!==0) $fatal(1,"bad ready acknowledgment");
            for(integer n=33;n<441;n=n+1)
                send_byte(attempt==1 && n==133 ? 8'bxxxxxxxx : packet[n]);
            @(negedge clk);rx_valid=0;wait_reply(2);
            if(word_count!=30) $fatal(1,"wrong complete-image write count");
            if(attempt==0 && (image_valid!==1 || last_status!==1)) $fatal(1,"valid image did not commit");
            if(attempt==1 && (image_valid!==0 || last_status!==5)) $fatal(1,"unknown payload became executable");
        end
        reset_device();
        $display("PASS loader four-state startup, complete upload and unknown-payload rejection");$finish;
    end
    initial begin #10000;$fatal(1,"four-state loader test timeout");end
endmodule
