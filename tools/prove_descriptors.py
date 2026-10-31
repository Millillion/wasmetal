#!/usr/bin/env python3
"""Prove descriptor reset elision and forwarding against fully reset storage."""
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parent.parent

HARNESS=r'''
    reg formal_started=0, formal_read_started=0;
    reg [WIDTH-1:0] formal_words[0:COUNT-1];
    reg [WIDTH-1:0] formal_word_a,formal_word_b;
    reg [31:0] formal_index_a,formal_index_b;
    integer formal_i;
    always @(posedge clk) begin
        if(!formal_started) assume(reset);
        formal_started<=1;
        if(reset) begin
            for(formal_i=0;formal_i<COUNT;formal_i=formal_i+1) formal_words[formal_i]<=0;
        end else if(pending_write && write_index<COUNT) formal_words[write_index]<=write_data;
    end
    always @(negedge clk) begin
        formal_read_started<=formal_started;
        formal_index_a<=read_index_a;formal_index_b<=read_index_b;
        formal_word_a<=read_index_a<COUNT ? formal_words[read_index_a]:{WIDTH{1'b0}};
        formal_word_b<=read_index_b<COUNT ? formal_words[read_index_b]:{WIDTH{1'b0}};
    end
    genvar formal_row;
    generate for(formal_row=0;formal_row<COUNT;formal_row=formal_row+1) begin
        always @* if(formal_started)
            assert((valid[formal_row] ? words[formal_row]:{WIDTH{1'b0}})==formal_words[formal_row]);
    end endgenerate
    wire [WIDTH-1:0] formal_a=formal_index_a>=COUNT ? {WIDTH{1'b0}} :
        pending_write && write_index==formal_index_a ? write_data:formal_word_a;
    wire [WIDTH-1:0] formal_b=formal_index_b>=COUNT ? {WIDTH{1'b0}} :
        pending_write && write_index==formal_index_b ? write_data:formal_word_b;
    always @* if(formal_read_started) begin
        assert(index_a==formal_index_a);assert(index_b==formal_index_b);
        assert((valid_a ? word_a:{WIDTH{1'b0}})==formal_word_a);
        assert((valid_b ? word_b:{WIDTH{1'b0}})==formal_word_b);
        assert(read_data_a==formal_a);assert(read_data_b==formal_b);
    end
'''


def main():
    directory=ROOT/'build/formal-descriptors';directory.mkdir(parents=True,exist_ok=True)
    original=(ROOT/'rtl/wasmetal_descriptors.sv').read_text()
    # A formal step is one clock edge. Alternating the phase explicitly lets
    # clk2fflogic model both edges; elapsed time between edges has no state effect.
    original=original.replace('input logic clk,reset,pending_write,','input logic reset,pending_write,')
    original=original.replace('    localparam integer ADDRESS_BITS',
        '    reg clk=0;\n    always @($global_clock) clk<=!clk;\n    localparam integer ADDRESS_BITS')
    assert original.count('endmodule')==1
    source=directory/'miter.sv';source.write_text(original.replace('endmodule',HARNESS+'\nendmodule'))
    # Bits of a word never interact. Prove an arbitrary bit, plus a multibit
    # non-power-of-two configuration to check the parameterized elaboration.
    for count,width in [(1,1),(13,5),(16,1),(256,1)]:
        stem=f'count-{count}-width-{width}'
        script=directory/(stem+'.ys')
        script.write_text(f'''read_verilog -formal -sv {source}
chparam -set COUNT {count} -set WIDTH {width} wasmetal_descriptors
prep -top wasmetal_descriptors
memory_map
clk2fflogic
opt
sat -seq 1 -tempinduct -maxsteps 12 -set-assumes -set-def-inputs -set-init-undef -enable_undef -prove-asserts -verify
''')
        with (directory/(stem+'.log')).open('w') as stream:
            subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-Q','-T','-s',str(script)],
                           stdout=stream,stderr=subprocess.STDOUT,check=True,cwd=ROOT)
        text=(directory/(stem+'.log')).read_text()
        if 'Induction step proven: SUCCESS!' not in text:
            raise RuntimeError(f'{stem}: no successful unbounded induction result')
        print(f'PASS descriptor induction COUNT={count} WIDTH={width}',flush=True)


if __name__=='__main__': main()
