#!/usr/bin/env python3
"""Check initialized deep RAM, both read edges, banking, and read-before-write."""
from pathlib import Path
import copy,json,re,subprocess
root=Path(__file__).resolve().parent.parent;d=root/'build/ecp5-ram-deep'
d.mkdir(parents=True,exist_ok=True)
import ecp5_ram
tools=root/'.cache/tools/usr'
source='''module ram_reference(input clk,we,input [11:0] wa,ra,input [127:0] data,output reg [127:0] result,previous);
(* ram_style="block" *) reg [127:0] memory [0:4095];
integer row;
initial for(row=0;row<4096;row=row+1)
    memory[row]={32'(row^32'hdeadbeef),32'(row*65539),32'(row*17),32'(~row)};
always @(posedge clk) begin
 previous<=memory[wa];
 if(we) memory[wa]<=data;
end
always @(negedge clk) result<=memory[ra];
endmodule
'''
(d/'reference.sv').write_text(source);(d/'input.sv').write_text(source.replace('ram_reference','ram_mapped'))
(d/'synth.ys').write_text(f'''read_verilog -sv {d}/input.sv
synth_ecp5 -top ram_mapped
check -assert
write_json {d}/mapped.json
select ram_mapped
write_verilog -selected -noattr {d}/mapped.v
''')
with (d/'synth.log').open('w') as log:subprocess.run([str(tools/'bin/yosys'),'-Q','-T','-s',str(d/'synth.ys')],stdout=log,stderr=subprocess.STDOUT,check=True)
j=json.loads((d/'mapped.json').read_text())['modules']['ram_mapped'];rams=[]
for c in j['cells'].values():
 if c['type']=='DP16KD':ecp5_ram.check(c);rams.append(c)
 elif c['type'] not in ('LUT4','TRELLIS_FF'):raise ValueError(c['type'])
assert len(rams)==30
for group,name,value in [('parameters','WRITEMODE_A','NORMAL'),
                         ('parameters','DATA_WIDTH_B',format(18,'032b')),
                         ('connections','ADA0',['1']),('connections','OCEA',['0'])]:
 invalid=copy.deepcopy(rams[0]);invalid[group][name]=value
 try:ecp5_ram.check(invalid)
 except ValueError:pass
 else:raise AssertionError('narrow RAM mode guard accepted '+name)
models=[ecp5_ram.model()];library=(tools/'share/yosys/ecp5/cells_sim.v').read_text()
for name in ['LUT4','TRELLIS_FF']:
 match=re.search(r'\bmodule\s+'+name+r'\b.*?\bendmodule',library,re.S)
 models.append(re.sub(r'\bspecify\b.*?\bendspecify\b','',match[0],flags=re.S))
(d/'cells.v').write_text('\n'.join(models))
(d/'test.sv').write_text('''module ram_test;
reg clk=0,we=0;
reg [11:0] wa=0,ra=0;
reg [127:0] data=0;
wire [127:0] actual,reference,actual_previous,reference_previous;
integer trial,bit_index,checks=0;
ram_mapped mapped(clk,we,wa,ra,data,actual,actual_previous);
ram_reference original(clk,we,wa,ra,data,reference,reference_previous);
initial begin
 for(trial=0;trial<4096;trial=trial+1) begin
  ra=12'(trial);#5 clk=1;#5 clk=0;#1;
  if(actual!==reference || actual_previous!==reference_previous) $fatal(1,"deep RAM initialization mismatch at %0d",trial);
  checks=checks+1;
 end
 for(trial=0;trial<10000;trial=trial+1) begin
  wa=12'($random);ra=trial%3==0 ? wa : 12'($random);we=trial%5!=0;
  for(bit_index=0;bit_index<128;bit_index=bit_index+1) data[bit_index]=1'($random);
  #5 clk=1;#5 clk=0;#1;
  if(actual!==reference || actual_previous!==reference_previous) $fatal(1,"deep RAM read/write mismatch at %0d",trial);
  checks=checks+1;
 end
 $display("PASS deep ECP5 RAM mapping: %0d dual-port checks across thirty RAMs; four rejected configurations",checks);$finish;
end
endmodule
''')
subprocess.run([str(tools/'bin/iverilog'),'-B'+str(tools/'lib/x86_64-linux-gnu/ivl'),'-g2012','-s','ram_test','-o',str(d/'test.vvp')]+[str(d/name) for name in ['cells.v','mapped.v','reference.sv','test.sv']],check=True)
subprocess.run([str(tools/'bin/vvp'),str(d/'test.vvp')],check=True)
