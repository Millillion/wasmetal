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
        DIV_WAIT, MEMORY_WAIT, INDIRECT_WAIT, FP_WAIT, SIMD_FP_START, SIMD_FP_WAIT,
        BULK_STEP, BULK_READ_WAIT, BULK_WRITE_WAIT
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
    logic [63:0] data_size [0:MEMORY_COUNT-1], element_size [0:MEMORY_COUNT-1];
    logic [63:0] bulk_left, bulk_source, bulk_destination;
    logic [31:0] bulk_source_index, bulk_destination_index;
    logic [2:0] bulk_source_kind, bulk_destination_kind;
    logic bulk_backwards, bulk_fill, bulk_table;
    logic [127:0] bulk_fill_value;
    logic [4:0] bulk_step_size;
    logic decoded_table, decoded_init, decoded_fill;
    logic [31:0] decoded_destination, decoded_source;
    logic [65:0] bulk_destination_limit, bulk_source_limit, bulk_destination_end, bulk_source_end;
    logic [64:0] grown_table;
    logic check_type;
    logic [31:0] expected_type;
    logic [31:0] sp, fp, control_sp, control_base, call_depth, result_arity;
    logic [31:0] init_left, callee_base, pending_branch;
    logic [1:0] call_kind;
    logic [31:0] copy_src, copy_dst, copy_len, copy_pos;
    logic [31:0] load_op, load_dst;
    logic [127:0] top, below, third;
    logic [63:0] alu_a, alu_result;
    logic alu_unary, alu_supported, unary_input;
    logic div_start, div_done, div_wide, div_signed, div_rem;
    logic [63:0] div_result;
    logic [7:0] div_trap;
    logic fp_supported, fp_unary, fp_done, fp_start;
    logic [63:0] fp_result;
    logic [7:0] fp_trap;
    logic simd_int_supported;
    logic [2:0] simd_int_arity;
    logic [127:0] simd_int_result;
    logic simd_fp_supported, simd_source_wide, simd_result_wide, simd_phase, simd_active;
    logic [31:0] simd_scalar_op, fp_operation;
    logic [2:0] simd_lanes, simd_arity, simd_mode, simd_lane;
    logic [127:0] simd_accum, simd_assembled, simd_a, simd_b;
    logic [63:0] simd_product, simd_a_lane, simd_b_lane, simd_c_lane, simd_result_lane;
    logic [63:0] fp_a, fp_b;
    logic [4:0] access_size;
    logic access_store;
    logic access_simd, access_lane;
    logic [127:0] load_vector, loaded_value;
    logic [31:0] load_lane;
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
    assign simd_active = state == SIMD_FP_START || state == SIMD_FP_WAIT;
    assign fp_start = (state == EXECUTE && insn_valid && fp_supported) || state == SIMD_FP_START;
    assign fp_operation = simd_active ? (simd_phase ? (simd_result_wide ? 32'ha0 : 32'h92) : simd_scalar_op) : insn_op;
    assign fp_a = simd_active ? (simd_phase ? (simd_mode == 5 ? simd_product ^ (simd_result_wide ? 64'h8000000000000000 : 64'h80000000) : simd_product) : simd_a_lane) : (fp_unary ? top[63:0] : below[63:0]);
    assign fp_b = simd_active ? (simd_phase ? simd_c_lane : simd_b_lane) : top[63:0];
    wasmetal_fpu fpu(.clk(clk),.reset(reset),.start(fp_start),.op(fp_operation),
        .a(fp_a),.b(fp_b),.supported(fp_supported),
        .unary_op(fp_unary),.done(fp_done),.result(fp_result),.trap(fp_trap));
    wasmetal_simd_int simd_integer(.op(insn_op),.lane(insn_x),.immediate(insn_imm),
        .a(simd_int_arity == 1 ? top : simd_int_arity == 2 ? below : third),
        .b(simd_int_arity == 3 ? below : top),.c(top),
        .supported(simd_int_supported),.arity(simd_int_arity),.result(simd_int_result));
    wasmetal_simd_fp_decode simd_float_decode(.op(insn_op),.supported(simd_fp_supported),
        .source_wide(simd_source_wide),.result_wide(simd_result_wide),.scalar_op(simd_scalar_op),
        .lanes(simd_lanes),.arity(simd_arity),.mode(simd_mode));
    always_comb begin
        simd_a = simd_arity == 1 ? top : simd_arity == 2 ? below : third;
        simd_b = simd_arity == 3 ? below : top;
        simd_a_lane = 64'(simd_a >> (simd_lane*(simd_source_wide ? 64 : 32)));
        simd_b_lane = 64'(simd_b >> (simd_lane*(simd_source_wide ? 64 : 32)));
        simd_c_lane = 64'(top >> (simd_lane*(simd_source_wide ? 64 : 32)));
        if (!simd_source_wide) begin simd_a_lane[63:32]=0; simd_b_lane[63:32]=0; simd_c_lane[63:32]=0; end
        simd_result_lane = fp_result;
        if (simd_mode == 1) simd_result_lane = {64{fp_result[0]}};
        else if (simd_mode == 2 || simd_mode == 3) simd_result_lane = fp_result[0] ? simd_b_lane : simd_a_lane;
        simd_assembled = simd_accum;
        if (simd_result_wide) simd_assembled[simd_lane*64+:64] = simd_result_lane;
        else simd_assembled[simd_lane*32+:32] = simd_result_lane[31:0];
    end

    always_comb begin
        decoded_table = insn_op >= 'hfc000c;
        decoded_init = insn_op == 'hfc0008 || insn_op == 'hfc000c;
        decoded_fill = insn_op == 'hfc000b || insn_op == 'hfc0011;
        decoded_destination = decoded_init ? insn_y : insn_x;
        decoded_source = decoded_init ? insn_x : insn_y;
        bulk_destination_limit = 0; bulk_source_limit = 0;
        if (decoded_destination < MEMORY_COUNT) bulk_destination_limit = decoded_table ?
            {2'b0,table_size[decoded_destination]} : {2'b0,memory_pages[decoded_destination]} << 16;
        if (decoded_source < MEMORY_COUNT) begin
            if (decoded_init) bulk_source_limit = decoded_table ? {2'b0,element_size[decoded_source]} : {2'b0,data_size[decoded_source]};
            else bulk_source_limit = decoded_table ? {2'b0,table_size[decoded_source]} : {2'b0,memory_pages[decoded_source]} << 16;
        end
        bulk_destination_end = {2'b0,third[63:0]}+{2'b0,top[63:0]};
        bulk_source_end = {2'b0,below[63:0]}+{2'b0,top[63:0]};
        bulk_step_size = bulk_table ? 5'd1 : (bulk_left >= 16 ? 5'd16 : bulk_left[4:0]);
        grown_table = 0;
        if (insn_x < MEMORY_COUNT) grown_table = {1'b0,table_size[insn_x]}+{1'b0,top[63:0]};
    end

    always_comb begin
        access_store = insn_op >= 'h36 && insn_op <= 'h3e;
        access_simd = (insn_op >= 'hfd0000 && insn_op <= 'hfd000b) || (insn_op >= 'hfd0054 && insn_op <= 'hfd005d);
        access_lane = insn_op >= 'hfd0054 && insn_op <= 'hfd005b;
        access_size = 4;
        case (insn_op)
            'h29, 'h2b, 'h37, 'h39: access_size = 8;
            'h2c, 'h2d, 'h30, 'h31, 'h3a, 'h3c: access_size = 1;
            'h2e, 'h2f, 'h32, 'h33, 'h3b, 'h3d: access_size = 2;
            default: access_size = 4;
        endcase
        if (access_simd) begin
            access_store = insn_op == 'hfd000b || (insn_op >= 'hfd0058 && insn_op <= 'hfd005b);
            case (insn_op)
                'hfd0000,'hfd000b: access_size=16;
                'hfd0007,'hfd0054,'hfd0058: access_size=1;
                'hfd0008,'hfd0055,'hfd0059: access_size=2;
                'hfd0009,'hfd0056,'hfd005a,'hfd005c: access_size=4;
                default: access_size=8;
            endcase
        end
        access_base = access_store || access_lane ? below[63:0] : top[63:0];
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

    integer v;
    always_comb begin
        loaded_value=mem_rdata; v=0;
        case (load_op)
            'h2c: loaded_value={96'b0,{24{mem_rdata[7]}},mem_rdata[7:0]};
            'h2e: loaded_value={96'b0,{16{mem_rdata[15]}},mem_rdata[15:0]};
            'h30: loaded_value={64'b0,{56{mem_rdata[7]}},mem_rdata[7:0]};
            'h32: loaded_value={64'b0,{48{mem_rdata[15]}},mem_rdata[15:0]};
            'h34: loaded_value={64'b0,{32{mem_rdata[31]}},mem_rdata[31:0]};
            'hfd0001,'hfd0002: for(v=0;v<8;v=v+1) loaded_value[v*16+:16]={{8{load_op=='hfd0001 && mem_rdata[v*8+7]}},mem_rdata[v*8+:8]};
            'hfd0003,'hfd0004: for(v=0;v<4;v=v+1) loaded_value[v*32+:32]={{16{load_op=='hfd0003 && mem_rdata[v*16+15]}},mem_rdata[v*16+:16]};
            'hfd0005,'hfd0006: for(v=0;v<2;v=v+1) loaded_value[v*64+:64]={{32{load_op=='hfd0005 && mem_rdata[v*32+31]}},mem_rdata[v*32+:32]};
            'hfd0007: loaded_value={16{mem_rdata[7:0]}};
            'hfd0008: loaded_value={8{mem_rdata[15:0]}};
            'hfd0009: loaded_value={4{mem_rdata[31:0]}};
            'hfd000a: loaded_value={2{mem_rdata[63:0]}};
            'hfd0054: begin loaded_value=load_vector; loaded_value[load_lane*8+:8]=mem_rdata[7:0]; end
            'hfd0055: begin loaded_value=load_vector; loaded_value[load_lane*16+:16]=mem_rdata[15:0]; end
            'hfd0056: begin loaded_value=load_vector; loaded_value[load_lane*32+:32]=mem_rdata[31:0]; end
            'hfd0057: begin loaded_value=load_vector; loaded_value[load_lane*64+:64]=mem_rdata[63:0]; end
            default: loaded_value=mem_rdata;
        endcase
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
            load_op <= 0; load_dst <= 0; check_type <= 0; expected_type <= 0;
            load_vector <= 0; load_lane <= 0;
            simd_accum <= 0; simd_product <= 0; simd_lane <= 0; simd_phase <= 0;
            bulk_left <= 0; bulk_source <= 0; bulk_destination <= 0;
            bulk_source_index <= 0; bulk_destination_index <= 0;
            bulk_source_kind <= 0; bulk_destination_kind <= 0;
            bulk_backwards <= 0; bulk_fill <= 0; bulk_table <= 0; bulk_fill_value <= 0;
            mem_valid <= 0; mem_write <= 0; mem_kind <= 0; mem_index <= 0;
            mem_address <= 0; mem_bytes <= 0; mem_wdata <= 0;
            for (k=0; k<MEMORY_COUNT; k=k+1) begin
                memory_pages[k] <= 0; memory_max[k] <= 0; memory_wide[k] <= 0;
                table_size[k] <= 0; table_max[k] <= 0; table_wide[k] <= 0;
                data_size[k] <= 0; element_size[k] <= 0;
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
                        4: if (cmd_index < MEMORY_COUNT) data_size[cmd_index] <= cmd_data[63:0];
                        5: if (cmd_index < MEMORY_COUNT) element_size[cmd_index] <= cmd_data[63:0];
                        6: if (cmd_index < MEMORY_COUNT) begin values[0] <= {64'b0,memory_pages[cmd_index]}; end
                        7: if (cmd_index < MEMORY_COUNT) begin values[0] <= {64'b0,table_size[cmd_index]}; end
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
                    else if (simd_int_supported) begin
                        values[sp-{29'b0,simd_int_arity}] <= simd_int_result;
                        sp <= sp-{29'b0,simd_int_arity}+1; pc <= pc+1;
                    end
                    else if (simd_fp_supported) begin
                        simd_accum <= 0; simd_lane <= 0; simd_phase <= 0; state <= SIMD_FP_START;
                    end
                    else if ((insn_op >= 'h28 && insn_op <= 'h3e) || access_simd) begin
                        if (insn_x >= MEMORY_COUNT || effective_address[64] || access_end > memory_limit) fail(T_BOUNDS);
                        else begin
                            mem_valid <= 1; mem_write <= access_store; mem_kind <= 0;
                            mem_index <= insn_x; mem_address <= effective_address[63:0]; mem_bytes <= access_size;
                            mem_wdata <= access_lane ? top >> (insn_y*{27'b0,access_size}*8) : top;
                            load_vector <= top; load_lane <= insn_y;
                            load_op <= insn_op; load_dst <= access_lane ? sp-2 : sp-1;
                            if (access_store) sp <= sp-2;
                            else if (access_lane) sp <= sp-1;
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
                        'hfc0009, 'hfc000d: begin
                            if (insn_x >= MEMORY_COUNT) fail(T_IMAGE);
                            else begin
                                if (insn_op == 'hfc0009) data_size[insn_x] <= 0;
                                else element_size[insn_x] <= 0;
                                pc <= pc+1;
                            end
                        end
                        'hfc000f: begin
                            if (insn_x >= MEMORY_COUNT) fail(T_IMAGE);
                            else if (grown_table[64] || grown_table > {1'b0,table_max[insn_x]}) begin
                                values[sp-2] <= table_wide[insn_x] ? {64'b0,64'hffffffffffffffff} : {96'b0,32'hffffffff};
                                sp <= sp-1; pc <= pc+1;
                            end else begin
                                values[sp-2] <= {64'b0,table_size[insn_x]}; sp <= sp-1;
                                table_size[insn_x] <= grown_table[63:0];
                                bulk_table <= 1; bulk_fill <= 1; bulk_fill_value <= below;
                                bulk_left <= top[63:0]; bulk_destination <= table_size[insn_x];
                                bulk_destination_index <= insn_x; bulk_destination_kind <= 2;
                                bulk_backwards <= 0; state <= BULK_STEP;
                            end
                        end
                        'hfc0008,'hfc000a,'hfc000b,'hfc000c,'hfc000e,'hfc0011: begin
                            if (decoded_destination >= MEMORY_COUNT || (!decoded_fill && decoded_source >= MEMORY_COUNT)) fail(T_IMAGE);
                            else if (bulk_destination_end > bulk_destination_limit ||
                                (!decoded_fill && bulk_source_end > bulk_source_limit)) fail(decoded_table ? 8'd5 : T_BOUNDS);
                            else begin
                                sp <= sp-3; bulk_left <= top[63:0]; bulk_fill <= decoded_fill;
                                bulk_table <= decoded_table; bulk_fill_value <= decoded_table ? below : {16{below[7:0]}};
                                bulk_source_index <= decoded_source; bulk_destination_index <= decoded_destination;
                                bulk_source_kind <= decoded_init ? (decoded_table ? 3'd4 : 3'd3) : (decoded_table ? 3'd2 : 3'd0);
                                bulk_destination_kind <= decoded_table ? 3'd2 : 3'd0;
                                if (!decoded_init && !decoded_fill && decoded_source == decoded_destination &&
                                    third[63:0] > below[63:0] && {2'b0,third[63:0]} < bulk_source_end) begin
                                    bulk_backwards <= 1;
                                    bulk_source <= bulk_source_end[63:0]; bulk_destination <= bulk_destination_end[63:0];
                                end else begin
                                    bulk_backwards <= 0; bulk_source <= below[63:0]; bulk_destination <= third[63:0];
                                end
                                state <= BULK_STEP;
                            end
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
                                // The configured backing capacity is zeroed at
                                // instantiation. Bounds checks prevent accessing
                                // the reserved tail before growth exposes it.
                                pc <= pc+1;
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
                SIMD_FP_START: state <= SIMD_FP_WAIT;
                SIMD_FP_WAIT: if (fp_done) begin
                    if (fp_trap != 0) fail(fp_trap);
                    else if ((simd_mode == 4 || simd_mode == 5) && !simd_phase) begin
                        simd_product <= fp_result; simd_phase <= 1; state <= SIMD_FP_START;
                    end else if (simd_lane+1 == simd_lanes) begin
                        values[sp-{29'b0,simd_arity}] <= simd_assembled;
                        sp <= sp-{29'b0,simd_arity}+1; pc <= pc+1; state <= EXECUTE;
                    end else begin
                        simd_accum <= simd_assembled; simd_lane <= simd_lane+1; simd_phase <= 0; state <= SIMD_FP_START;
                    end
                end
                INDIRECT_WAIT: if (mem_ready) begin
                    mem_valid <= 0;
                    if (mem_fault) fail(5);
                    else if (mem_rdata == 0) fail(6);
                    else begin function_index <= mem_rdata[31:0]-1; state <= CALL_SETUP; end
                end
                BULK_STEP: begin
                    if (bulk_left == 0) begin pc <= pc+1; state <= EXECUTE; end
                    else begin
                        mem_valid <= 1; mem_write <= bulk_fill;
                        mem_kind <= bulk_fill ? bulk_destination_kind : bulk_source_kind;
                        mem_index <= bulk_fill ? bulk_destination_index : bulk_source_index;
                        mem_address <= (bulk_fill ? bulk_destination : bulk_source) -
                            (bulk_backwards ? {59'b0,bulk_step_size} : 64'b0);
                        mem_bytes <= bulk_table ? 5'd16 : bulk_step_size;
                        mem_wdata <= bulk_fill_value;
                        state <= bulk_fill ? BULK_WRITE_WAIT : BULK_READ_WAIT;
                    end
                end
                BULK_READ_WAIT: if (mem_ready) begin
                    if (mem_fault) fail(bulk_table ? 8'd5 : T_BOUNDS);
                    else begin
                        mem_wdata <= mem_rdata; mem_write <= 1;
                        mem_kind <= bulk_destination_kind; mem_index <= bulk_destination_index;
                        mem_address <= bulk_destination-(bulk_backwards ? {59'b0,bulk_step_size} : 64'b0);
                        state <= BULK_WRITE_WAIT;
                    end
                end
                BULK_WRITE_WAIT: if (mem_ready) begin
                    mem_valid <= 0;
                    if (mem_fault) fail(bulk_table ? 8'd5 : T_BOUNDS);
                    else begin
                        bulk_left <= bulk_left-{59'b0,bulk_step_size};
                        bulk_source <= bulk_backwards ? bulk_source-{59'b0,bulk_step_size} : bulk_source+{59'b0,bulk_step_size};
                        bulk_destination <= bulk_backwards ? bulk_destination-{59'b0,bulk_step_size} : bulk_destination+{59'b0,bulk_step_size};
                        state <= BULK_STEP;
                    end
                end
                MEMORY_WAIT: if (mem_ready) begin
                    mem_valid <= 0;
                    if (mem_fault) fail(T_BOUNDS);
                    else begin
                        if (!mem_write) begin
                            values[load_dst] <= loaded_value;
                        end
                        pc <= pc+1; state <= EXECUTE;
                    end
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
