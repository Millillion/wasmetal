// SPDX-License-Identifier: MIT
// Destructive startup test followed by exclusive CPU ownership. Reset this
// controller and its memory backend together. Every reset starts a new test.
module wasmetal_memory_startup #(
    parameter integer RAM_BYTES=131072,
    parameter integer RESPONSE_TIMEOUT=1024
) (
    input wire clk, reset,
    input wire cpu_valid, cpu_write,
    input wire [31:0] cpu_address,
    input wire [15:0] cpu_mask,
    input wire [127:0] cpu_wdata,
    output wire cpu_ready, cpu_fault,
    output wire [127:0] cpu_rdata,
    output wire cpu_enabled, test_busy, test_done, test_failed,
    output wire [1:0] error_code,
    output wire [31:0] error_address,
    output wire [127:0] expected_data, observed_data,
    output wire [63:0] completed_operations,
    output wire memory_valid, memory_write,
    output wire [31:0] memory_address,
    output wire [15:0] memory_mask,
    output wire [127:0] memory_wdata,
    input wire memory_ready, memory_fault,
    input wire [127:0] memory_rdata
);
    logic launched;
    wire test_valid, test_write;
    wire [31:0] test_address;
    wire [15:0] test_mask;
    wire [127:0] test_wdata;
    always_ff @(posedge clk) begin
        if(reset) launched<=0;
        else launched<=1;
    end

    // done follows a complete low-valid release cycle. Failed tests retain
    // ownership, including a timed-out request waiting for its late response.
    assign cpu_enabled=test_done && !test_failed && !reset;
    assign memory_valid=!reset && (cpu_enabled ? cpu_valid : test_valid);
    assign memory_write=memory_valid && (cpu_enabled ? cpu_write : test_write);
    assign memory_address=cpu_enabled ? cpu_address : test_address;
    assign memory_mask=cpu_enabled ? cpu_mask : test_mask;
    assign memory_wdata=cpu_enabled ? cpu_wdata : test_wdata;
    assign cpu_ready=cpu_enabled && cpu_valid && memory_ready;
    assign cpu_fault=cpu_ready && memory_fault;
    assign cpu_rdata=cpu_enabled ? memory_rdata : 128'b0;

    wasmetal_memory_bist #(.RAM_BYTES(RAM_BYTES),.RESPONSE_TIMEOUT(RESPONSE_TIMEOUT)) test_master(
        .clk(clk),.reset(reset),.start(!launched),
        .busy(test_busy),.done(test_done),.failed(test_failed),
        .error_code(error_code),.error_address(error_address),
        .expected_data(expected_data),.observed_data(observed_data),
        .completed_operations(completed_operations),
        .valid(test_valid),.write(test_write),.address(test_address),
        .mask(test_mask),.wdata(test_wdata),
        .ready(!cpu_enabled && memory_ready),.fault(memory_fault),.rdata(memory_rdata));

    reg formal_started=0;
    reg previous_enabled,previous_valid,waiting_memory,waiting_cpu;
    reg [176:0] previous_memory_payload,previous_cpu_payload;
    reg [63:0] previous_count;
    always @(posedge clk) begin
        if(!formal_started) assume(reset);
        formal_started<=1;
        if(reset) begin
            assert(!cpu_enabled && !memory_valid && !memory_write && !cpu_ready && !cpu_fault);
            previous_enabled<=0;previous_valid<=0;waiting_memory<=0;waiting_cpu<=0;
            previous_memory_payload<=0;previous_cpu_payload<=0;previous_count<=0;
        end else begin
            if(formal_started) begin
                if(waiting_cpu) begin
                    assume(cpu_valid);
                    assume({cpu_write,cpu_address,cpu_mask,cpu_wdata}==previous_cpu_payload);
                end
                assert((^{launched,test_busy,test_done,test_failed,completed_operations})!==1'bx);
                if(test_done || test_busy) assert(launched);
                if(previous_enabled) begin
                    assert(cpu_enabled);
                    assert(completed_operations==previous_count);
                end
                if(cpu_enabled) begin
                    assert(test_done && !test_busy && !test_failed);
                    assert(completed_operations==64'(RAM_BYTES/16)*64'd80);
                    assert(memory_valid==cpu_valid);
                    assert(memory_write==(cpu_valid && cpu_write));
                    assert({memory_address,memory_mask,memory_wdata}=={cpu_address,cpu_mask,cpu_wdata});
                    assert(cpu_ready==(cpu_valid && memory_ready));
                    assert(cpu_fault==(cpu_valid && memory_ready && memory_fault));
                    assert(cpu_rdata==memory_rdata);
                    if(!previous_enabled) assert(!previous_valid);
                end else begin
                    assert(!cpu_ready && !cpu_fault && cpu_rdata==0);
                    assert(memory_valid==test_valid);
                    assert(memory_write==(test_valid && test_write));
                    assert({memory_address,memory_mask,memory_wdata}=={test_address,test_mask,test_wdata});
                end
                if(test_failed) assert(!cpu_enabled);
                if(waiting_memory) begin
                    assert(memory_valid);
                    assert({memory_write,memory_address,memory_mask,memory_wdata}==previous_memory_payload);
                end
            end
            previous_enabled<=cpu_enabled;previous_valid<=memory_valid;
            waiting_memory<=memory_valid && !memory_ready;
            waiting_cpu<=cpu_valid && !cpu_ready;
            previous_memory_payload<={memory_write,memory_address,memory_mask,memory_wdata};
            previous_cpu_payload<={cpu_write,cpu_address,cpu_mask,cpu_wdata};
            previous_count<=completed_operations;
        end
    end

endmodule
