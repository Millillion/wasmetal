// SPDX-License-Identifier: MIT
// One outstanding bundled-data transaction with a synchronized toggle in each
// direction. Payloads remain registered until the complete return handshake.
// A common asynchronous reset asserts both domains; release is synchronized
// separately. The backend must use m_reset and reset any accepted transactions.
// Physical implementation also needs synchronizer and bundled-data constraints.
module wasmetal_memory_cdc (
    input wire s_clk, m_clk, reset,
    output wire source_online, s_reset, m_reset,
    input wire s_valid, s_write,
    input wire [31:0] s_address,
    input wire [15:0] s_mask,
    input wire [127:0] s_wdata,
    output wire s_ready,
    output logic s_fault,
    output logic [127:0] s_rdata,
    output wire m_valid, m_write,
    output wire [31:0] m_address,
    output wire [15:0] m_mask,
    output wire [127:0] m_wdata,
    input wire m_ready, m_fault,
    input wire [127:0] m_rdata
);
    (* ASYNC_REG="TRUE", async_reg="true" *) logic [1:0] source_release, destination_release;
    always_ff @(posedge s_clk or posedge reset)
        if(reset) source_release<=0;
        else source_release<={source_release[0],1'b1};
    always_ff @(posedge m_clk or posedge reset)
        if(reset) destination_release<=0;
        else destination_release<={destination_release[0],1'b1};
    assign s_reset=!source_release[1];
    assign m_reset=!destination_release[1];

    typedef enum logic [1:0] {SOURCE_IDLE,SOURCE_WAIT,SOURCE_RESPONSE,SOURCE_RELEASE} source_state_t;
    typedef enum logic [1:0] {DEST_IDLE,DEST_WAIT,DEST_RELEASE} destination_state_t;
    source_state_t source_state;
    destination_state_t destination_state;
    logic request_toggle, response_toggle;
    logic destination_up;
    logic [176:0] request_payload, destination_request;
    logic [128:0] response_payload;
    (* ASYNC_REG="TRUE", async_reg="true" *) logic [1:0] request_sync, response_sync, destination_up_sync;
    assign source_online=!s_reset && destination_up_sync[1];
    assign s_ready=source_state==SOURCE_RESPONSE && !s_reset;
    assign m_valid=destination_state==DEST_WAIT && !m_reset;
    assign {m_write,m_address,m_mask,m_wdata}=destination_request;

    always_ff @(posedge s_clk or posedge s_reset) begin
        if(s_reset) begin response_sync<=0;destination_up_sync<=0;end
        else begin
            response_sync<={response_sync[0],response_toggle};
            destination_up_sync<={destination_up_sync[0],destination_up};
        end
    end
    always_ff @(posedge m_clk or posedge m_reset)
        if(m_reset) request_sync<=0;
        else request_sync<={request_sync[0],request_toggle};
    always_ff @(posedge m_clk or posedge m_reset)
        if(m_reset) destination_up<=0;
        else destination_up<=1;

    always_ff @(posedge s_clk or posedge s_reset) begin
        if(s_reset) begin
            source_state<=SOURCE_IDLE;request_toggle<=0;request_payload<=0;
            s_fault<=0;s_rdata<=0;
        end else case(source_state)
            SOURCE_IDLE: if(s_valid && source_online) begin
                request_payload<={s_write,s_address,s_mask,s_wdata};
                request_toggle<=!request_toggle;source_state<=SOURCE_WAIT;
            end
            SOURCE_WAIT: if(response_sync[1]==request_toggle) begin
                s_fault<=response_payload[128];
                s_rdata<=response_payload[128] ? 128'b0 : response_payload[127:0];
                source_state<=SOURCE_RESPONSE;
            end
            SOURCE_RESPONSE: source_state<=SOURCE_RELEASE;
            SOURCE_RELEASE: if(!s_valid) source_state<=SOURCE_IDLE;
            default: source_state<=SOURCE_IDLE;
        endcase
    end
    always_ff @(posedge m_clk or posedge m_reset) begin
        if(m_reset) begin
            destination_state<=DEST_IDLE;response_toggle<=0;
            destination_request<=0;response_payload<=0;
        end else case(destination_state)
            DEST_IDLE: if(request_sync[1]!=response_toggle) begin
                destination_request<=request_payload;destination_state<=DEST_WAIT;
            end
            DEST_WAIT: if(m_ready) begin
                response_payload<={m_fault,m_rdata};response_toggle<=request_sync[1];
                destination_state<=DEST_RELEASE;
            end
            DEST_RELEASE: destination_state<=DEST_IDLE;
            default: destination_state<=DEST_IDLE;
        endcase
    end

`ifdef WASMETAL_ASSERTIONS
    logic source_held, destination_held;
    logic [176:0] prior_source, prior_destination;
    always_ff @(posedge s_clk or posedge s_reset) begin
        if(s_reset) begin source_held<=0;prior_source<=0;end
        else begin
            if(source_held) assert(request_payload==prior_source);
            source_held<=source_state==SOURCE_WAIT;
            prior_source<=request_payload;
        end
    end
    always_ff @(posedge m_clk or posedge m_reset) begin
        if(m_reset) begin destination_held<=0;prior_destination<=0;end
        else begin
            if(destination_held) assert(m_valid && destination_request==prior_destination);
            destination_held<=m_valid && !m_ready;prior_destination<=destination_request;
        end
    end
`endif
endmodule
