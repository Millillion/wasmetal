#!/usr/bin/env python3
"""Prove descriptor reset elision and forwarding against fully reset storage."""
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parent.parent

HARNESS=r'''
    // Proof-only reference storage. Every location is observable to induction;
    // the architectural read ports additionally check bounds and forwarding.
    reg formal_started=0;
    reg [WIDTH-1:0] formal_words[0:COUNT-1];
    integer formal_i;
    always @(posedge clk) begin
        if(!formal_started) assume(reset);
        formal_started<=1;
        if(reset) begin
            for(formal_i=0;formal_i<COUNT;formal_i=formal_i+1) formal_words[formal_i]<=0;
        end else if(pending_write && write_index<COUNT) formal_words[write_index]<=write_data;
    end
    genvar formal_row;
    generate for(formal_row=0;formal_row<COUNT;formal_row=formal_row+1) begin
        always @* if(formal_started)
            assert((valid[formal_row] ? words[formal_row]:{WIDTH{1'b0}})==formal_words[formal_row]);
    end endgenerate
    wire [WIDTH-1:0] formal_a=read_index_a>=COUNT ? {WIDTH{1'b0}} :
        pending_write && write_index==read_index_a ? write_data:formal_words[read_index_a];
    wire [WIDTH-1:0] formal_b=read_index_b>=COUNT ? {WIDTH{1'b0}} :
        pending_write && write_index==read_index_b ? write_data:formal_words[read_index_b];
    always @* if(formal_started) begin
        assert(read_data_a==formal_a);
        assert(read_data_b==formal_b);
    end
'''


def main():
    directory=ROOT/'build/formal-descriptors';directory.mkdir(parents=True,exist_ok=True)
    original=(ROOT/'rtl/wasmetal_descriptors.sv').read_text()
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
opt
sat -seq 1 -tempinduct -maxsteps 6 -set-assumes -set-def-inputs -set-init-undef -enable_undef -prove-asserts -verify
''')
        with (directory/(stem+'.log')).open('w') as stream:
            subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-Q','-T','-s',str(script)],
                           stdout=stream,stderr=subprocess.STDOUT,check=True,cwd=ROOT)
        text=(directory/(stem+'.log')).read_text()
        if 'Induction step proven: SUCCESS!' not in text:
            raise RuntimeError(f'{stem}: no successful unbounded induction result')
        print(f'PASS descriptor induction COUNT={count} WIDTH={width}',flush=True)


if __name__=='__main__': main()
