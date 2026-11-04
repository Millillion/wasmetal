// SPDX-License-Identifier: MIT
// Exact rational arithmetic in the Python driver supplies all binary
// completions of each X/Z vector. Neither circuit may assert a known bit
// contradicted by a completion; pessimistic unknown bits are permitted.
module fp_round_four_state;
    parameter integer EXP=8,SIG=24;
    localparam integer N=EXP+SIG;
    reg [N-1:0] a;
    reg [1:0] mode;
    wire [N-1:0] native_result,mapped_result;
    reg [N-1:0] possible_ones,always_ones;
    integer fd,fields,checks=0,binary_checks=0,bit_index;
    string vectors;
    wasmetal_fp_round #(.EXP(EXP),.SIG(SIG)) native_round(a,mode,native_result);
    mapped_round_component mapped_round(.a(a),.mode(mode),.result(mapped_result));
    initial begin
        if (!$value$plusargs("vectors=%s",vectors)) $fatal(1,"missing rounding vectors");
        fd=$fopen(vectors,"r");
        if (fd==0) $fatal(1,"cannot open rounding vectors");
        fields=$fscanf(fd,"%b %b %h %h\n",a,mode,possible_ones,always_ones);
        while (fields==4) begin
            #1;
            if (!$isunknown({a,mode})) begin
                if (possible_ones!==always_ones || native_result!==always_ones ||
                    mapped_result!==always_ones)
                    $fatal(1,"binary rounding mismatch at vector %0d",checks);
                binary_checks=binary_checks+1;
            end
            for (bit_index=0;bit_index<N;bit_index=bit_index+1) begin
                if ((native_result[bit_index]===1'b0 && possible_ones[bit_index]) ||
                    (native_result[bit_index]===1'b1 && !always_ones[bit_index]))
                    $fatal(1,"optimistic native rounded bit at vector %0d bit %0d",checks,bit_index);
                if ((mapped_result[bit_index]===1'b0 && possible_ones[bit_index]) ||
                    (mapped_result[bit_index]===1'b1 && !always_ones[bit_index]))
                    $fatal(1,"optimistic mapped rounded bit at vector %0d bit %0d",checks,bit_index);
            end
            checks=checks+1;
            fields=$fscanf(fd,"%b %b %h %h\n",a,mode,possible_ones,always_ones);
        end
        if (!$feof(fd) || checks==0 || binary_checks==0)
            $fatal(1,"incomplete rounding vectors");
        $fclose(fd);
        $display("PASS %0d rounding vectors; %0d binary",checks,binary_checks);
        $finish;
    end
endmodule
