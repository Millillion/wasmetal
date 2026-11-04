// SPDX-License-Identifier: MIT
// Full programmable RTL, ordinary four-state storage, and UART pins as stimulus.
`timescale 1ns/1ps
module loadable_four_state;
    localparam integer TICKS=4, MAX_PACKET=65536, MAX_REPLY=1024;
    logic clk=0, reset=1, rx=1;
    wire tx, finished, error, image_valid;
`ifdef WASMETAL_ROM_SMOKE
    wasmetal_rom_smoke_harness dut(.clk(clk),.reset(reset),.rx(rx),.tx(tx),
        .finished(finished),.error(error),.image_valid(image_valid));
`else
    `include "instance.svh"
`endif
    always #5 clk=~clk;

    reg [7:0] packet[0:MAX_PACKET-1], received[0:MAX_REPLY-1];
    integer received_count=0, receive_state=0, sample_left=0, receive_bit=0;
    reg [7:0] receiving=0;
    integer cycles_elapsed=0, checked_words=0;
    reg armed=0, previously_uncommitted=0;
    string image0, image1;
    integer packet_length, expected0, expected1;

    // Sample after the sequential logic has settled. An unknown pin must never
    // become a fabricated binary byte in the observer.
    always @(negedge clk) begin
        cycles_elapsed=cycles_elapsed+1;
        if(cycles_elapsed%100000==0) begin
            $display("PROGRESS %0d clocks, %0d UART bytes",cycles_elapsed,received_count);
            $fflush();
        end
        if(reset) begin
            received_count=0; receive_state=0; sample_left=0; receive_bit=0;
            previously_uncommitted=0;
        end else if(armed) begin
            if(tx!==1'b0 && tx!==1'b1) $fatal(1,"UNKNOWN_TX");
            if(image_valid!==1'b0 && image_valid!==1'b1) $fatal(1,"UNKNOWN_IMAGE_VALID");
            // Allow the execution registers their synchronous reset edge when
            // the loader revokes an old image.
            if(image_valid!==1'b1 && previously_uncommitted &&
                (dut.execution.boot_index!==32'd0 || dut.execution.code_count!==32'd0 ||
                 dut.execution.function_count!==32'd0 || dut.execution.boot_count!==32'd0 ||
                 dut.execution.command_valid!==1'b0))
                $fatal(1,"BOOT_BEFORE_COMMIT");
            previously_uncommitted=image_valid===1'b0;
            case(receive_state)
                0: if(tx===1'b0) begin
                    sample_left=TICKS+TICKS/2-1; receive_bit=0; receiving=0; receive_state=1;
                end
                1: if(sample_left!=0) sample_left=sample_left-1;
                   else begin
                       receiving[receive_bit]=tx; sample_left=TICKS-1;
                       if(receive_bit==7) receive_state=2;
                       else receive_bit=receive_bit+1;
                   end
                2: if(sample_left!=0) sample_left=sample_left-1;
                   else begin
                       if(tx!==1'b1) $fatal(1,"BAD_UART_STOP");
                       if(received_count>=MAX_REPLY) $fatal(1,"REPLY_OVERFLOW");
                       received[received_count]=receiving; received_count=received_count+1;
                       receive_state=0;
                   end
                default: $fatal(1,"BAD_OBSERVER_STATE");
            endcase
        end
        if(cycles_elapsed>8000000) $fatal(1,"CAMPAIGN_TIMEOUT");
    end

    task automatic clocks(input integer count);
        repeat(count) begin @(posedge clk); #1; end
    endtask

    task automatic reset_system;
        reset=1; rx=1; clocks(8); reset=0; clocks(4);
        if(image_valid!==1'b0) $fatal(1,"RESET_DID_NOT_REVOKE_IMAGE");
    endtask

    task automatic send_byte(input reg [7:0] value);
        rx=0; clocks(TICKS);
        for(integer bit_number=0;bit_number<8;bit_number=bit_number+1) begin
            rx=value[bit_number]; clocks(TICKS);
        end
        rx=1; clocks(TICKS);
    endtask

    task automatic wait_bytes(input integer count, input integer budget);
        integer started;
        begin
            started=cycles_elapsed;
            while(received_count<count) begin
                clocks(1);
                if(cycles_elapsed-started>budget) $fatal(1,"UART_REPLY_TIMEOUT");
            end
            if(received_count!=count) $fatal(1,"UNEXPECTED_REPLY_LENGTH");
        end
    endtask

    task automatic print_uart(input integer index);
        $write("UART %0d ",index);
        for(integer i=0;i<received_count;i=i+1) $write("%02x",received[i]);
        $display("");
    endtask

    task automatic header(input string path);
        begin
            $readmemh(path,packet,0,packet_length-1);
            for(integer i=0;i<33;i=i+1) send_byte(packet[i]);
            wait_bytes(20,10000);
            if(received[0]!==8'h57 || received[1]!==8'h4d || received[2]!==8'h4c ||
               received[3]!==8'h52 || received[4]!==8'h01 || received[5]!==8'h00)
                $fatal(1,"UPLOAD_NOT_READY");
        end
    endtask

    task automatic upload(input string path, input integer reply_bytes, input integer index);
        begin
            header(path);
            for(integer i=33;i<packet_length;i=i+1) send_byte(packet[i]);
            wait_bytes(reply_bytes,1000000); clocks(20*TICKS);
            if(received_count!=reply_bytes || receive_state!=0) $fatal(1,"EXTRA_UART_RESULT");
            if(image_valid!==1'b1 || finished!==1'b1 || error!==1'b0) $fatal(1,"SYSTEM_DID_NOT_FINISH");
            print_uart(index);
        end
    endtask

    initial begin
        if(!$value$plusargs("image0=%s",image0) || !$value$plusargs("image1=%s",image1) ||
           !$value$plusargs("length=%d",packet_length) || !$value$plusargs("expected0=%d",expected0) ||
           !$value$plusargs("expected1=%d",expected1)) $fatal(1,"MISSING_STIMULUS");
        if(packet_length<104 || packet_length>MAX_PACKET || expected0>MAX_REPLY || expected1>MAX_REPLY)
            $fatal(1,"INVALID_STIMULUS_SIZE");
        clocks(8);
        // This negative control checks that a silently zero-initialized model
        // cannot masquerade as the uninitialized-storage campaign.
`ifdef WASMETAL_ROM_SMOKE
        `include "unknown_ram.svh"
`else
        if($test$plusargs("known-initial-word")) dut.execution.instructions[0]=0;
        `include "unknown_storage.svh"
`endif
        $display("UNKNOWN_STORAGE %0d",checked_words);
        $fflush();
        armed=1; reset=0; clocks(4);
`ifdef WASMETAL_ROM_SMOKE
        wait_bytes(expected0-40,1000000); clocks(20*TICKS);
        if(received_count!=expected0-40 || receive_state!=0 || finished!==1'b1 || error!==1'b0)
            $fatal(1,"ROM_SYSTEM_DID_NOT_FINISH");
        print_uart(0);
        $display("PASS complete ROM four-state boot");
        $finish;
`else
        if($test$plusargs("boot-gating-negative")) begin
            clocks(200000); $fatal(1,"MUTATION_WAS_NOT_DETECTED");
        end
        upload(image0,expected0,0);
        reset_system(); header(image1);
        for(integer i=33;i<103;i=i+1) send_byte(packet[i]);
        if(image_valid!==1'b0 || finished!==1'b0) $fatal(1,"PARTIAL_IMAGE_EXECUTED");
        print_uart(1);
        reset_system(); upload(image1,expected1,2);
        $display("PASS complete programmable four-state: 2 images, 1 interrupted upload");
        $finish;
`endif
    end
endmodule
