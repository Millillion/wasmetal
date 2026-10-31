#!/usr/bin/env python3
"""Check the restricted ECP5 RAM model against independently inferred storage."""
import copy
import json
from pathlib import Path
import subprocess

import ecp5_ram

ROOT = Path(__file__).resolve().parent.parent


def main():
    directory = ROOT/'build/ecp5-ram'
    directory.mkdir(parents=True, exist_ok=True)
    source = '''module ram_reference(input clk,input [19:0] we,input [8:0] wa,ra,
        input [179:0] data,output reg [179:0] result);
    (* ram_style="block" *) reg [179:0] memory [0:511];
    integer row,lane;
    initial for(row=0;row<512;row=row+1)
        memory[row]={36'(row^36'habcdef012),36'(row*17),36'(~row),
                     36'(row*65539),36'(row)};
    always @(posedge clk) for(lane=0;lane<20;lane=lane+1)
        if(we[lane]) memory[wa][lane*9+:9]<=data[lane*9+:9];
    always @(negedge clk) result<=memory[ra];
endmodule
'''
    (directory/'reference.sv').write_text(source)
    (directory/'input.sv').write_text(source.replace('module ram_reference', 'module ram_mapped'))
    (directory/'synth.ys').write_text('''read_verilog -sv build/ecp5-ram/input.sv
synth_ecp5 -top ram_mapped
check -assert
write_json build/ecp5-ram/mapped.json
select ram_mapped
write_verilog -selected -noattr build/ecp5-ram/mapped.v
''')
    with (directory/'synth.log').open('w') as stream:
        subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'), '-Q', '-T', '-s', str(directory/'synth.ys')],
                       cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, check=True)
    mapped = json.loads((directory/'mapped.json').read_text())['modules']['ram_mapped']
    cells = list(mapped['cells'].values())
    if len(cells) != 5 or any(c['type'] != 'DP16KD' for c in cells):
        raise ValueError('RAM probe did not map to exactly five ECP5 block RAMs')
    for cell in cells:
        ecp5_ram.check(cell)
    for group, name, value in [('parameters', 'DATA_WIDTH_A', format(18, '032b')),
                               ('parameters', 'CLKBMUX', 'CLKB'),
                               ('parameters', 'REGMODE_B', 'OUTREG'),
                               ('parameters', 'GSR', 'ENABLED'),
                               ('connections', 'WEB', ['1']),
                               ('connections', 'CEB', ['0']),
                               ('connections', 'ADA4', ['1'])]:
        invalid = copy.deepcopy(cells[0])
        invalid[group][name] = value
        try:
            ecp5_ram.check(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError('RAM mode guard accepted '+name)
    (directory/'cells.v').write_text(ecp5_ram.model())
    (directory/'test.sv').write_text('''module ram_test;
    reg clk=0;
    reg [19:0] we=0;
    reg [8:0] wa=0,ra=0;
    reg [179:0] data=0;
    wire [179:0] actual,reference;
    integer trial,bit_index,checks=0;
    ram_mapped mapped(clk,we,wa,ra,data,actual);
    ram_reference original(clk,we,wa,ra,data,reference);
    initial begin
        // Read every initialized word, including both ends of the physical RAM.
        for(trial=0;trial<512;trial=trial+1) begin
            ra=trial[8:0];
            #5 clk=1; #5 clk=0; #1;
            if(actual!==reference) $fatal(1,"RAM initialization mismatch at %0d",trial);
            checks=checks+1;
        end
        for(trial=0;trial<10000;trial=trial+1) begin
            wa=9'($random);ra=trial%3==0 ? wa : 9'($random);
            we=trial%5==0 ? 20'b0 : 20'($random);
            for(bit_index=0;bit_index<180;bit_index=bit_index+1) data[bit_index]=1'($random);
            #5 clk=1; #5 clk=0; #1;
            if(actual!==reference) $fatal(1,"RAM read/write mismatch at %0d",trial);
            checks=checks+1;
        end
        $display("PASS ECP5 RAM mapping: %0d reads plus seven rejected configurations",checks);
        $finish;
    end
endmodule
''')
    tools = ROOT/'.cache/tools/usr'
    subprocess.run([str(tools/'bin/iverilog'), '-B'+str(tools/'lib/x86_64-linux-gnu/ivl'),
                    '-g2012', '-s', 'ram_test', '-o', str(directory/'test.vvp')]+
                   [str(directory/name) for name in ('cells.v', 'mapped.v', 'reference.sv', 'test.sv')], check=True)
    subprocess.run([str(tools/'bin/vvp'), str(directory/'test.vvp')], check=True)


if __name__ == '__main__':
    main()
