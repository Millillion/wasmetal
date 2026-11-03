#!/usr/bin/env python3
"""Four-state checks of every address in the additional mapped EBR modes."""
import copy
import json
from pathlib import Path
import random
import subprocess

import ecp5_ram
import ecp5_standalone_ram as local
from prepare_standalone import ROOT, digest


def main():
    directory=ROOT/'build/standalone-ram-check';directory.mkdir(parents=True,exist_ok=True)
    netlist=ROOT/'build/standalone-ulx3s/design.json'
    memory_netlist=ROOT/'build/standalone-memory-production/memory.json'
    source=json.loads(netlist.read_text())['modules']['wasmetal_standalone_ulx3s']
    memory=json.loads(memory_netlist.read_text())['modules']['wasmetal_local_memory']
    examples={}
    for cell in list(source['cells'].values())+list(memory['cells'].values()):
        if cell['type']!='DP16KD': continue
        try: kind=local.check(cell)
        except ValueError: continue
        examples.setdefault(kind,cell)
    wanted=['rom18-CLKA','rom18-INV','rom36','ram1','rom36-positive']
    if set(examples)!=set(wanted): raise ValueError('expected standalone RAM modes are missing')
    rng=random.Random(0x574d52414d)
    words=[[rng.getrandbits(18) for _ in range(1024)] for _ in range(2)]
    words.append([rng.getrandbits(36) for _ in range(512)])
    pattern=[rng.getrandbits(1) for _ in range(16384)]
    text=['module bench; reg clk=0,wr=0,bit_data=0; reg [13:0] address=0;',
          'wire [17:0] a[0:4],b[0:4]; reg [17:0] saved_pos,saved_neg;',
          'reg [35:0] saved_wide,saved_wide_pos; integer n;',
          "localparam [16383:0] pattern=16384'h"+f'{sum(v<<n for n,v in enumerate(pattern)):04096x};']
    for j in range(3):
        width=18 if j<2 else 36
        text.append(f'reg [{width-1}:0] expected{j}[0:{len(words[j])-1}];')
    for j,kind in enumerate(wanted):
        cell=copy.deepcopy(examples[kind]); params=cell['parameters']
        initial=0
        if j<2: initial=sum(v<<(20*n) for n,v in enumerate(words[j]))
        elif j in (2,4):
            initial=sum(((v&((1<<18)-1))<<(40*n))|((v>>18)<<(40*n+20)) for n,v in enumerate(words[2]))
        for n in range(64): params[f'INITVAL_{n:02X}']=f'{(initial>>(320*n))&((1<<320)-1):0320b}'
        local.check(cell)
        literals=[]
        for name,value in params.items():
            literal=f"{len(value)}'b{value}" if set(value)<=set('01x') else json.dumps(value.rstrip())
            literals.append('.'+name+'('+literal+')')
        connections=[]
        for name,direction in ecp5_ram.PINS.items():
            if direction=='output': expression=f'{"a" if name.startswith("DOA") else "b"}[{j}][{name[3:]}]'
            elif name=='CLKA': expression="1'b0" if j in (2,4) else 'clk'
            elif name=='CLKB': expression='clk' if j in (2,4) else "1'b0"
            elif name=='WEA' and j==3: expression='wr'
            elif name=='DIA0' and j==3: expression='bit_data'
            elif name.startswith('ADA'):
                bit=int(name[3:]); expression=(f'address[{bit}]' if j==3 else
                    f'address[{bit-4}]' if j<2 and bit>=4 else "1'b0")
            elif name.startswith('ADB'):
                bit=int(name[3:]);expression=f'address[{bit-5}]' if j in (2,4) and bit>=5 else "1'b0"
            else:
                pin=cell['connections'][name][0]
                expression="1'b"+pin if isinstance(pin,str) else "1'b0"
            connections.append('.'+name+'('+expression+')')
        text.append(local.NAME+' #('+','.join(literals)+f') dut{j}('+','.join(connections)+');')
    text.append('initial begin')
    for j,values in enumerate(words):
        text += [f"expected{j}[{n}]={18 if j<2 else 36}'h{v:x};" for n,v in enumerate(values)]
    text += ['''#2;
for(n=0;n<1024;n=n+1) begin
 saved_pos=a[0]; saved_neg=a[1]; saved_wide={b[2],a[2]}; saved_wide_pos={b[4],a[4]};
 address=14'(n); #2;
 if(a[0]!==saved_pos || a[1]!==saved_neg || {b[2],a[2]}!==saved_wide) $fatal(1,"asynchronous ROM read");
 if({b[4],a[4]}!==saved_wide_pos) $fatal(1,"asynchronous positive-edge wide ROM read");
 clk=1; #2;
 if(a[0]!==expected0[n] || a[1]!==saved_neg || {b[2],a[2]}!==saved_wide) $fatal(1,"positive edge ROM mismatch");
 if({b[4],a[4]}!==expected2[n%512]) $fatal(1,"positive edge wide ROM mismatch");
 clk=0; #2;
 if(a[1]!==expected1[n] || a[0]!==expected0[n] || {b[2],a[2]}!==expected2[n%512]) $fatal(1,"negative edge ROM mismatch");
 if({b[4],a[4]}!==expected2[n%512]) $fatal(1,"wide ROM changed on wrong edge");
end
for(n=0;n<16384;n=n+1) begin
 address=14'(n); wr=1; bit_data=pattern[n]; #2;
 clk=1; #2;
 if(a[3][0]!==1'b0) $fatal(1,"read-before-write mismatch");
 clk=0; #2; wr=0;
 clk=1; #2;
 if(a[3][0]!==pattern[n]) $fatal(1,"single-bit write/read mismatch");
 clk=0; #2;
end
for(n=16383;n>=0;n=n-1) begin
 address=14'(n); #2; clk=1; #2;
 if(a[3][0]!==pattern[n]) $fatal(1,"single-bit address alias");
 clk=0; #2;
end
address='x; #2; clk=1; #2;
if(!$isunknown(a[0]) || !$isunknown(a[3][0]) || !$isunknown({b[4],a[4]})) $fatal(1,"unknown address became known");
clk=0; #2;
if(!$isunknown(a[1]) || !$isunknown({b[2],a[2]})) $fatal(1,"unknown negative-edge address became known");
$display("PASS standalone RAM modes and all addresses"); $finish;
end endmodule
''']
    bench=directory/'bench.sv';bench.write_text('\n'.join(text))
    model=directory/'model.v';model.write_text(ecp5_ram.model()+local.model())
    def execute(source,name):
        binary=directory/(name+'.vvp')
        subprocess.run([str(ROOT/'.cache/tools/usr/bin/iverilog'),'-B',str(ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl'),
            '-g2012','-s','bench','-o',str(binary),str(source),str(bench)],check=True)
        result=subprocess.run([str(ROOT/'.cache/tools/usr/bin/vvp'),str(binary)],capture_output=True,text=True)
        (directory/(name+'.log')).write_text(result.stdout+result.stderr)
        return result
    result=execute(model,'positive')
    if result.returncode: print(result.stdout+result.stderr);result.check_returncode()
    negative=directory/'negative.v'
    old='result_a<=memory[address_a];'
    if model.read_text().count(old)!=1: raise ValueError('negative control target changed')
    negative.write_text(model.read_text().replace(old,"result_a<=1'b0;"))
    wrong=execute(negative,'negative')
    if wrong.returncode==0 or 'single-bit write/read mismatch' not in wrong.stdout:
        raise ValueError('memory checker accepted deliberately incorrect read data')
    rejected=0
    for original in examples.values():
        for name,value in [('REGMODE_A','OUTREG'),('WRITEMODE_B','WRITETHROUGH'),('DATA_WIDTH_A','10')]:
            cell=copy.deepcopy(original);cell['parameters'][name]=value
            try: local.check(cell)
            except ValueError: rejected+=1
            else: raise ValueError('unsupported RAM parameter admitted')
        cell=copy.deepcopy(original);cell['connections']['RSTB']=['1']
        try: local.check(cell)
        except ValueError: rejected+=1
        else: raise ValueError('unsupported RAM reset admitted')
    report={'status':'passed','modes':wanted,'rom18_words_per_edge':1024,'rom36_words':512,
            'ram1_addresses':16384,'rom36_clock_edges':['positive','negative'],'four_state_unknown_addresses_checked':True,
            'negative_control_rejected':True,'unsupported_configurations_rejected':rejected,
            'inputs':{str(p.relative_to(ROOT)):digest(p) for p in
                [Path(__file__).resolve(),ROOT/'tools/ecp5_ram.py',ROOT/'tools/ecp5_standalone_ram.py',netlist,memory_netlist,bench,model]},
            'physical_hardware_tested':False}
    (ROOT/'reports/standalone-ram-model.json').write_text(json.dumps(report,indent=2)+'\n')
    print(result.stdout,end='')


if __name__=='__main__': main()
