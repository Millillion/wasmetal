// SPDX-License-Identifier: MIT
// Clocked Wasm execution engine. The image loader supplies decoded immediates
// and branch metadata; it never supplies instruction results.
module wasmetal_core #(
    parameter integer VALUE_DEPTH = 16384,
    parameter integer CONTROL_DEPTH = 2048,
    parameter integer CALL_DEPTH = 512,
    parameter integer MEMORY_COUNT = 256
) (
    input logic clk, reset,
    input logic cmd_valid,
    input logic [3:0] cmd_kind,
    input logic [31:0] cmd_index,
    input logic [127:0] cmd_data,
    input logic [63:0] cmd_aux,
    output logic busy, done,
    output logic [7:0] trap,
    output logic [31:0] result_count,
    input logic [31:0] result_index,
    output logic [127:0] result_data,

    output logic [31:0] pc,
    input logic [31:0] insn_op, insn_x, insn_y, insn_z, insn_w,
    input logic [127:0] insn_imm,
    input logic insn_valid,

    output logic [31:0] function_index,
    input logic [31:0] function_entry, function_params, function_locals,
    input logic [31:0] function_results, function_type,
    input logic function_valid,

    output logic mem_valid, mem_write,
    output logic [2:0] mem_kind,
    output logic [31:0] mem_index,
    output logic [63:0] mem_address,
    output logic [4:0] mem_bytes,
    output logic [127:0] mem_wdata,
    input logic mem_ready, mem_fault,
    input logic [127:0] mem_rdata
);
    localparam logic [7:0] T_UNREACHABLE=1, T_BOUNDS=4,
        T_EXHAUSTION=9, T_IMAGE=254, T_UNSUPPORTED=255;
    typedef enum logic [4:0] {
        IDLE, EXECUTE, CALL_SETUP, ENTER, INIT_LOCALS, BRANCH,
        BR_TABLE, COPY_VALUES, RETURN_SETUP, RETURN_RESTORE,
        DIV_WAIT, MEMORY_WAIT, GROW_ZERO, GROW_WAIT, INDIRECT_WAIT, FP_WAIT
    } state_t;
    state_t state, copy_next;
    logic [127:0] values [0:VALUE_DEPTH-1];
    logic [31:0] labels_height [0:CONTROL_DEPTH-1];
    logic [31:0] labels_pc [0:CONTROL_DEPTH-1];
    logic [31:0] labels_arity [0:CONTROL_DEPTH-1];
    logic labels_loop [0:CONTROL_DEPTH-1];
    logic [31:0] frames_pc [0:CALL_DEPTH-1];
    logic [31:0] frames_fp [0:CALL_DEPTH-1];
    logic [31:0] frames_control [0:CALL_DEPTH-1];
    logic [31:0] frames_results [0:CALL_DEPTH-1];
    logic [63:0] memory_pages [0:MEMORY_COUNT-1];
    logic [63:0] memory_max [0:MEMORY_COUNT-1];
    logic memory_wide [0:MEMORY_COUNT-1];
    logic [63:0] table_size [0:MEMORY_COUNT-1];
    logic [63:0] table_max [0:MEMORY_COUNT-1];
    logic table_wide [0:MEMORY_COUNT-1];
    logic check_type;
    logic [31:0] expected_type;
    logic [31:0] sp, fp, control_sp, control_base, call_depth, result_arity;
    logic [31:0] init_left, callee_base, pending_branch;
    logic [1:0] call_kind;
    logic [31:0] copy_src, copy_dst, copy_len, copy_pos;
    logic [31:0] load_op, load_dst;
    logic [63:0] grow_end;
    logic [127:0] top, below, third;
    logic [63:0] alu_a, alu_result;
    logic alu_unary, alu_supported, unary_input;
    logic div_start, div_done, div_wide, div_signed, div_rem;
    logic [63:0] div_result;
    logic [7:0] div_trap;
    logic fp_supported, fp_unary, fp_done, fp_start;
    logic [63:0] fp_result;
    logic [7:0] fp_trap;
    logic [4:0] access_size;
    logic access_store;
    logic [63:0] access_base;
    logic [65:0] access_end, memory_limit;
    logic [64:0] effective_address, grown_pages;
    logic [31:0] label_index;
    integer k;

    assign busy = state != IDLE;
    assign result_data = result_index < VALUE_DEPTH ? values[result_index] : 128'b0;
    assign top = (sp > 0 && sp <= VALUE_DEPTH) ? values[sp-1] : 128'b0;
    assign below = (sp > 1 && sp <= VALUE_DEPTH) ? values[sp-2] : 128'b0;
    assign third = (sp > 2 && sp <= VALUE_DEPTH) ? values[sp-3] : 128'b0;
    assign unary_input = insn_op == 'h45 || insn_op == 'h50 ||
        (insn_op >= 'h67 && insn_op <= 'h69) ||
        (insn_op >= 'h79 && insn_op <= 'h7b) ||
        (insn_op >= 'ha7 && insn_op <= 'hc4);
    assign alu_a = unary_input ? top[63:0] : below[63:0];
    wasmetal_alu alu(.op(insn_op),.a(alu_a),.b(top[63:0]),
        .result(alu_result),.unary_op(alu_unary),.supported(alu_supported));
    assign div_start = state == EXECUTE && insn_valid &&
        ((insn_op >= 'h6d && insn_op <= 'h70) || (insn_op >= 'h7f && insn_op <= 'h82));
    assign div_wide = insn_op >= 'h7f;
    assign div_signed = insn_op == 'h6d || insn_op == 'h6f || insn_op == 'h7f || insn_op == 'h81;
    assign div_rem = insn_op == 'h6f || insn_op == 'h70 || insn_op == 'h81 || insn_op == 'h82;
    wasmetal_divider divider(.clk(clk),.reset(reset),.start(div_start),
        .wide(div_wide),.signed_op(div_signed),.remainder_op(div_rem),
        .a(below[63:0]),.b(top[63:0]),.done(div_done),.result(div_result),.trap(div_trap));
    assign fp_start = state == EXECUTE && insn_valid && fp_supported;
    wasmetal_fpu fpu(.clk(clk),.reset(reset),.start(fp_start),.op(insn_op),
        .a(fp_unary ? top[63:0] : below[63:0]),.b(top[63:0]),.supported(fp_supported),
        .unary_op(fp_unary),.done(fp_done),.result(fp_result),.trap(fp_trap));

    always_comb begin
        access_store = insn_op >= 'h36 && insn_op <= 'h3e;
        access_size = 4;
        case (insn_op)
            'h29, 'h2b, 'h37, 'h39: access_size = 8;
            'h2c, 'h2d, 'h30, 'h31, 'h3a, 'h3c: access_size = 1;
            'h2e, 'h2f, 'h32, 'h33, 'h3b, 'h3d: access_size = 2;
            default: access_size = 4;
        endcase
        access_base = access_store ? below[63:0] : top[63:0];
        memory_limit = 0; grown_pages = 0;
        if (insn_x < MEMORY_COUNT) begin
            if (!memory_wide[insn_x]) access_base[63:32] = 0;
            memory_limit = {2'b0,memory_pages[insn_x]} << 16;
            grown_pages = {1'b0,memory_pages[insn_x]} +
                (memory_wide[insn_x] ? {1'b0,top[63:0]} : {33'b0,top[31:0]});
        end
        effective_address = {1'b0,access_base} + {1'b0,insn_imm[63:0]};
        access_end = {1'b0,effective_address} + {61'b0,access_size};
        label_index = control_sp-1-pending_branch;
    end

    task automatic fail(input logic [7:0] code);
        begin trap <= code; done <= 1; state <= IDLE; mem_valid <= 0; result_count <= 0; end
    endtask

    always_ff @(posedge clk) begin
        if (reset) begin
            state <= IDLE; copy_next <= IDLE; done <= 0; trap <= 0; result_count <= 0;
            pc <= 0; function_index <= 0;
            sp <= 0; fp <= 0; control_sp <= 0; control_base <= 0; call_depth <= 0; result_arity <= 0;
            init_left <= 0; callee_base <= 0; pending_branch <= 0; call_kind <= 0;
            copy_src <= 0; copy_dst <= 0; copy_len <= 0; copy_pos <= 0;
            load_op <= 0; load_dst <= 0; grow_end <= 0; check_type <= 0; expected_type <= 0;
            mem_valid <= 0; mem_write <= 0; mem_kind <= 0; mem_index <= 0;
            mem_address <= 0; mem_bytes <= 0; mem_wdata <= 0;
            for (k=0; k<MEMORY_COUNT; k=k+1) begin
                memory_pages[k] <= 0; memory_max[k] <= 0; memory_wide[k] <= 0;
                table_size[k] <= 0; table_max[k] <= 0; table_wide[k] <= 0;
            end
        end else begin
            case (state)
                IDLE: if (cmd_valid) begin
                    case (cmd_kind)
                        0: begin
                            done <= 0; trap <= 0; result_count <= 0;
                            sp <= cmd_aux[31:0]; fp <= 0; control_sp <= 0; control_base <= 0; call_depth <= 0;
                            function_index <= cmd_index; call_kind <= 0; check_type <= 0; state <= CALL_SETUP;
                        end
                        1: if (cmd_index < VALUE_DEPTH) values[cmd_index] <= cmd_data;
                        2: if (cmd_index < MEMORY_COUNT) begin
                            memory_pages[cmd_index] <= cmd_data[63:0];
                            memory_max[cmd_index] <= cmd_data[127:64]; memory_wide[cmd_index] <= cmd_aux[0];
                        end
                        3: if (cmd_index < MEMORY_COUNT) begin
                            table_size[cmd_index] <= cmd_data[63:0];
                            table_max[cmd_index] <= cmd_data[127:64]; table_wide[cmd_index] <= cmd_aux[0];
                        end
                        default: fail(T_IMAGE);
                    endcase
                end
                CALL_SETUP: begin
                    if (!function_valid || function_params > sp) fail(T_IMAGE);
                    else if (check_type && function_type != expected_type) fail(7);
                    else if (call_kind == 1 && call_depth >= CALL_DEPTH) fail(T_EXHAUSTION);
                    else if (function_params + function_locals > VALUE_DEPTH ||
                        sp - function_params > VALUE_DEPTH - (function_params + function_locals)) fail(T_EXHAUSTION);
                    else begin
                        if (call_kind == 1) begin
                            frames_pc[call_depth] <= pc+1;
                            frames_fp[call_depth] <= fp;
                            frames_control[call_depth] <= control_base;
                            frames_results[call_depth] <= result_arity;
                            call_depth <= call_depth+1;
                            callee_base <= sp-function_params;
                            state <= ENTER;
                        end else if (call_kind == 2) begin
                            copy_src <= sp-function_params; copy_dst <= fp;
                            copy_len <= function_params; copy_pos <= 0;
                            callee_base <= fp; control_sp <= control_base;
                            copy_next <= ENTER; state <= COPY_VALUES;
                        end else begin callee_base <= 0; state <= ENTER; end
                    end
                end
                ENTER: begin
                    fp <= callee_base; sp <= callee_base+function_params;
                    result_arity <= function_results; control_base <= control_sp;
                    pc <= function_entry; init_left <= function_locals;
                    state <= function_locals == 0 ? EXECUTE : INIT_LOCALS;
                end
                INIT_LOCALS: begin
                    values[sp] <= 0; sp <= sp+1; init_left <= init_left-1;
                    if (init_left == 1) state <= EXECUTE;
                end
                EXECUTE: begin
                    if (!insn_valid) fail(T_IMAGE);
                    else if (sp >= VALUE_DEPTH) fail(T_EXHAUSTION);
                    else if (alu_supported) begin
                        values[sp-(alu_unary ? 1 : 2)] <= {64'b0,alu_result};
                        if (!alu_unary) sp <= sp-1;
                        pc <= pc+1;
                    end else if (div_start) state <= DIV_WAIT;
                    else if (fp_supported) state <= FP_WAIT;
                    else if (insn_op >= 'h28 && insn_op <= 'h3e) begin
                        if (insn_x >= MEMORY_COUNT || effective_address[64] || access_end > memory_limit) fail(T_BOUNDS);
                        else begin
                            mem_valid <= 1; mem_write <= access_store; mem_kind <= 0;
                            mem_index <= insn_x; mem_address <= effective_address[63:0]; mem_bytes <= access_size;
                            mem_wdata <= top; load_op <= insn_op; load_dst <= sp-1;
                            if (access_store) sp <= sp-2;
                            state <= MEMORY_WAIT;
                        end
                    end else case (insn_op)
                        'h00: fail(T_UNREACHABLE);
                        'h01: pc <= pc+1;
                        'h02, 'h03, 'h04: begin
                            if (control_sp >= CONTROL_DEPTH) fail(T_EXHAUSTION);
                            else begin
                                labels_height[control_sp] <= sp-insn_x-(insn_op == 'h04 ? 1 : 0);
                                labels_pc[control_sp] <= insn_op == 'h03 ? pc+1 : insn_z+1;
                                labels_arity[control_sp] <= insn_op == 'h03 ? insn_x : insn_y;
                                labels_loop[control_sp] <= insn_op == 'h03;
                                control_sp <= control_sp+1;
                                if (insn_op == 'h04) begin
                                    sp <= sp-1;
                                    pc <= top[31:0] == 0 ? insn_w : pc+1;
                                end else pc <= pc+1;
                            end
                        end
                        'h05: begin pending_branch <= 0; state <= BRANCH; end
                        'h0b: begin
                            if (control_sp == control_base) state <= RETURN_SETUP;
                            else begin control_sp <= control_sp-1; pc <= pc+1; end
                        end
                        'h0c: begin pending_branch <= insn_x; state <= BRANCH; end
                        'h0d: begin
                            sp <= sp-1;
                            if (top[31:0] != 0) begin pending_branch <= insn_x; state <= BRANCH; end
                            else pc <= pc+1;
                        end
                        'h0e: begin
                            sp <= sp-1; pc <= insn_x+(top[31:0] < insn_y ? top[31:0] : insn_y);
                            state <= BR_TABLE;
                        end
                        'h0f: state <= RETURN_SETUP;
                        'h10, 'h12: begin
                            function_index <= insn_x; call_kind <= insn_op == 'h12 ? 2 : 1; check_type <= 0; state <= CALL_SETUP;
                        end
                        'h11, 'h13: begin
                            if (insn_y >= MEMORY_COUNT || top[63:0] >= table_size[insn_y]) fail(5);
                            else begin
                                mem_valid <= 1; mem_write <= 0; mem_kind <= 2; mem_index <= insn_y;
                                mem_address <= top[63:0]; mem_bytes <= 16;
                                expected_type <= insn_x; check_type <= 1;
                                call_kind <= insn_op == 'h13 ? 2 : 1;
                                sp <= sp-1; state <= INDIRECT_WAIT;
                            end
                        end
                        'h14, 'h15: begin
                            if (top == 0) fail(6);
                            else begin
                                function_index <= top[31:0]-1; expected_type <= insn_x; check_type <= 1;
                                call_kind <= insn_op == 'h15 ? 2 : 1; sp <= sp-1; state <= CALL_SETUP;
                            end
                        end
                        'h1a: begin sp <= sp-1; pc <= pc+1; end
                        'h1b, 'h1c: begin values[sp-3] <= top[31:0] != 0 ? third : below; sp <= sp-2; pc <= pc+1; end
                        'h20: begin
                            if (fp+insn_x >= VALUE_DEPTH) fail(T_IMAGE);
                            else begin values[sp] <= values[fp+insn_x]; sp <= sp+1; pc <= pc+1; end
                        end
                        'h21, 'h22: begin
                            if (fp+insn_x >= VALUE_DEPTH) fail(T_IMAGE);
                            else begin values[fp+insn_x] <= top; if (insn_op == 'h21) sp <= sp-1; pc <= pc+1; end
                        end
                        'h23, 'h24: begin
                            mem_valid <= 1; mem_write <= insn_op == 'h24; mem_kind <= 1;
                            mem_index <= insn_x; mem_address <= 0; mem_bytes <= 16; mem_wdata <= top;
                            load_op <= insn_op; load_dst <= sp;
                            sp <= insn_op == 'h24 ? sp-1 : sp+1; state <= MEMORY_WAIT;
                        end
                        'h25, 'h26: begin
                            if (insn_x >= MEMORY_COUNT ||
                                (insn_op == 'h26 ? below[63:0] : top[63:0]) >= table_size[insn_x]) fail(5);
                            else begin
                                mem_valid <= 1; mem_write <= insn_op == 'h26; mem_kind <= 2;
                                mem_index <= insn_x; mem_address <= insn_op == 'h26 ? below[63:0] : top[63:0];
                                mem_bytes <= 16; mem_wdata <= top; load_op <= insn_op; load_dst <= sp-1;
                                if (insn_op == 'h26) sp <= sp-2;
                                state <= MEMORY_WAIT;
                            end
                        end
                        'hfc0010: begin
                            if (insn_x >= MEMORY_COUNT) fail(T_IMAGE);
                            else begin values[sp] <= {64'b0,table_size[insn_x]}; sp <= sp+1; pc <= pc+1; end
                        end
                        'h3f: begin
                            if (insn_x >= MEMORY_COUNT) fail(T_IMAGE);
                            else begin values[sp] <= {64'b0,memory_pages[insn_x]}; sp <= sp+1; pc <= pc+1; end
                        end
                        'h40: begin
                            if (insn_x >= MEMORY_COUNT) fail(T_IMAGE);
                            else if (grown_pages[64] || grown_pages > {1'b0,memory_max[insn_x]}) begin
                                values[sp-1] <= memory_wide[insn_x] ? {64'b0,64'hffffffffffffffff} : {96'b0,32'hffffffff};
                                pc <= pc+1;
                            end else begin
                                values[sp-1] <= {64'b0,memory_pages[insn_x]};
                                memory_pages[insn_x] <= grown_pages[63:0];
                                if (grown_pages[63:0] == memory_pages[insn_x]) pc <= pc+1;
                                else begin
                                    mem_index <= insn_x; mem_kind <= 0; mem_bytes <= 16;
                                    mem_address <= memory_pages[insn_x] << 16;
                                    grow_end <= grown_pages[63:0] << 16;
                                    mem_wdata <= 0; state <= GROW_ZERO;
                                end
                            end
                        end
                        'h41, 'h42, 'h43, 'h44, 'h00fd000c: begin values[sp] <= insn_imm; sp <= sp+1; pc <= pc+1; end
                        'hd0: begin values[sp] <= 0; sp <= sp+1; pc <= pc+1; end
                        'hd1: begin values[sp-1] <= {127'b0,top == 0}; pc <= pc+1; end
                        'hd2: begin values[sp] <= {96'b0,insn_x+32'd1}; sp <= sp+1; pc <= pc+1; end
                        'hd3: begin values[sp-2] <= {127'b0,top == below}; sp <= sp-1; pc <= pc+1; end
                        'hd4: begin if (top == 0) fail(6); else pc <= pc+1; end
                        'hd5: begin
                            if (top == 0) begin sp <= sp-1; pending_branch <= insn_x; state <= BRANCH; end
                            else pc <= pc+1;
                        end
                        'hd6: begin
                            if (top != 0) begin pending_branch <= insn_x; state <= BRANCH; end
                            else begin sp <= sp-1; pc <= pc+1; end
                        end
                        default: fail(T_UNSUPPORTED);
                    endcase
                end
                BR_TABLE: begin
                    if (!insn_valid) fail(T_IMAGE);
                    else begin pending_branch <= insn_x; state <= BRANCH; end
                end
                BRANCH: begin
                    if (pending_branch > control_sp-control_base) fail(T_IMAGE);
                    else if (pending_branch == control_sp-control_base) state <= RETURN_SETUP;
                    else begin
                        copy_src <= sp-labels_arity[label_index]; copy_dst <= labels_height[label_index];
                        copy_len <= labels_arity[label_index]; copy_pos <= 0;
                        control_sp <= label_index+(labels_loop[label_index] ? 1 : 0);
                        pc <= labels_pc[label_index]; copy_next <= EXECUTE; state <= COPY_VALUES;
                    end
                end
                COPY_VALUES: begin
                    if (copy_pos < copy_len) begin
                        if (copy_dst+copy_pos >= VALUE_DEPTH || copy_src+copy_pos >= VALUE_DEPTH) fail(T_EXHAUSTION);
                        else begin values[copy_dst+copy_pos] <= values[copy_src+copy_pos]; copy_pos <= copy_pos+1; end
                    end else begin sp <= copy_dst+copy_len; state <= copy_next; end
                end
                RETURN_SETUP: begin
                    copy_src <= sp-result_arity; copy_dst <= fp; copy_len <= result_arity; copy_pos <= 0;
                    control_sp <= control_base; copy_next <= RETURN_RESTORE; state <= COPY_VALUES;
                end
                RETURN_RESTORE: begin
                    if (call_depth == 0) begin result_count <= result_arity; done <= 1; state <= IDLE; end
                    else begin
                        pc <= frames_pc[call_depth-1]; fp <= frames_fp[call_depth-1];
                        control_base <= frames_control[call_depth-1]; result_arity <= frames_results[call_depth-1];
                        call_depth <= call_depth-1; state <= EXECUTE;
                    end
                end
                DIV_WAIT: if (div_done) begin
                    if (div_trap != 0) fail(div_trap);
                    else begin values[sp-2] <= {64'b0,div_result}; sp <= sp-1; pc <= pc+1; state <= EXECUTE; end
                end
                FP_WAIT: if (fp_done) begin
                    if (fp_trap != 0) fail(fp_trap);
                    else begin
                        values[sp-(fp_unary ? 1 : 2)] <= {64'b0,fp_result};
                        if (!fp_unary) sp <= sp-1;
                        pc <= pc+1; state <= EXECUTE;
                    end
                end
                INDIRECT_WAIT: if (mem_ready) begin
                    mem_valid <= 0;
                    if (mem_fault) fail(5);
                    else if (mem_rdata == 0) fail(6);
                    else begin function_index <= mem_rdata[31:0]-1; state <= CALL_SETUP; end
                end
                MEMORY_WAIT: if (mem_ready) begin
                    mem_valid <= 0;
                    if (mem_fault) fail(T_BOUNDS);
                    else begin
                        if (!mem_write) begin
                            case (load_op)
                                'h2c: values[load_dst] <= {96'b0,{24{mem_rdata[7]}},mem_rdata[7:0]};
                                'h2e: values[load_dst] <= {96'b0,{16{mem_rdata[15]}},mem_rdata[15:0]};
                                'h30: values[load_dst] <= {64'b0,{56{mem_rdata[7]}},mem_rdata[7:0]};
                                'h32: values[load_dst] <= {64'b0,{48{mem_rdata[15]}},mem_rdata[15:0]};
                                'h34: values[load_dst] <= {64'b0,{32{mem_rdata[31]}},mem_rdata[31:0]};
                                default: values[load_dst] <= mem_rdata;
                            endcase
                        end
                        pc <= pc+1; state <= EXECUTE;
                    end
                end
                GROW_ZERO: begin mem_valid <= 1; mem_write <= 1; state <= GROW_WAIT; end
                GROW_WAIT: if (mem_ready) begin
                    mem_valid <= 0;
                    if (mem_fault) fail(T_BOUNDS);
                    else if (mem_address+16 == grow_end) begin pc <= pc+1; state <= EXECUTE; end
                    else begin mem_address <= mem_address+16; state <= GROW_ZERO; end
                end
                default: fail(T_IMAGE);
            endcase
        end
    end

`ifdef WASMETAL_ASSERTIONS
    always_ff @(posedge clk) if (!reset && busy) begin
        assert (sp <= VALUE_DEPTH);
        assert (control_sp <= CONTROL_DEPTH);
        assert (call_depth <= CALL_DEPTH);
        assert (control_base <= control_sp);
        if (mem_valid) assert (mem_bytes > 0 && mem_bytes <= 16);
    end
`endif
endmodule
