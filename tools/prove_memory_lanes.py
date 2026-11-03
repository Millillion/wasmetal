#!/usr/bin/env python3
"""Exhaustively prove physical byte lanes against byte-indexed reference logic."""
import json
from pathlib import Path
import subprocess
from prepare_standalone import ROOT,digest

HARNESS='''module lane_proof(input [4:0] position,length,input [3:0] offset,lane,
    input [127:0] payload,memory_data);
wire [4:0] count; wire [15:0] mask; wire [127:0] write_data,read_data;
wasmetal_memory_lanes dut(.*);
wire [5:0] write_index={1'b0,position}+{2'b0,lane}-{2'b0,offset};
wire [5:0] read_index={2'b0,offset}+{2'b0,lane}-{1'b0,position};
wire selected_write=lane>=offset && write_index<{1'b0,length};
wire selected_read={1'b0,lane}>=position && {1'b0,lane}<length && read_index<16;
reg [4:0] words;
integer n;
always @* begin
    assume(length>=1 && length<=16 && position<length);
    words=0;
    for(n=0;n<16;n=n+1) begin
        if(6'(n)>={2'b0,offset} && ({1'b0,position}+6'(n)-{2'b0,offset})<{1'b0,length}) words=words+1'b1;
    end
    assert(count==words);assert(mask[lane]==selected_write);
    assert(write_data[{lane,3'b0}+:8]==(selected_write ? payload[{write_index,3'b0}+:8]:8'b0));
    assert(read_data[{lane,3'b0}+:8]==(selected_read ? memory_data[{read_index,3'b0}+:8]:8'b0));
end
endmodule
'''

def main():
    directory=ROOT/'build/formal-memory-lanes';directory.mkdir(parents=True,exist_ok=True)
    source=ROOT/'soc/memory/wasmetal_memory_lanes.sv'
    harness=directory/'proof.sv';harness.write_text(HARNESS)
    inputs=[source,Path(__file__).resolve(),harness];hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs}
    script=directory/'proof.ys'
    script.write_text(f'read_verilog -formal -sv {source} {harness}\nprep -top lane_proof -flatten\nsat -set-assumes -prove-asserts -verify\n')
    with (directory/'proof.log').open('w') as log:
        subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-Q','-T','-s',str(script)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=180)
    text=(directory/'proof.log').read_text()
    if 'SUCCESS!' not in text:raise RuntimeError('missing exhaustive proof result')
    negative=directory/'corrupt.sv';negative.write_text(source.read_text().replace('assign mask=','assign mask=16\'h0001 ^ '))
    script.write_text(script.read_text().replace(str(source),str(negative)))
    with (directory/'negative.log').open('w') as log:
        result=subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-Q','-T','-s',str(script)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=180)
    if result.returncode==0 or 'proof did fail' not in (directory/'negative.log').read_text():
        raise RuntimeError('negative proof did not fail for the intended reason')
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise RuntimeError('proof inputs changed')
    report={'status':'passed','scope':'all binary payloads, memory words, valid lengths, positions and offsets',
        'properties':['beat size','byte enables','aligned write payload','zero-padded read assembly'],
        'negative_control_rejected':True,'inputs':hashes,'physical_hardware_tested':False}
    (ROOT/'reports').mkdir(exist_ok=True)
    (ROOT/'reports/memory-lanes-proof.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS exhaustive byte-lane equivalence, including a rejected corrupt mask')

if __name__=='__main__':main()
