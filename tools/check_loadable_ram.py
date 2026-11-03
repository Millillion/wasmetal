#!/usr/bin/env python3
"""Check every programmable EBR address/lane and prove no region read/write overlap."""
import copy
import json
from pathlib import Path
import random
import subprocess
import ecp5_ram
import ecp5_loadable_ram as model
from build_board import yosys
from prepare_standalone import ROOT,digest


def collision_cone(module,cells):
    """Conservatively cut at every non-LUT/mux output, including all registers."""
    drivers={}
    for cell in module['cells'].values():
        for port,bits in cell['connections'].items():
            if cell['port_directions'][port]=='output':
                for bit in bits:
                    if isinstance(bit,int):drivers[bit]=cell
    assignments={};leaves=set();active=set()
    def signal(bit):
        if isinstance(bit,str):return "1'b"+bit
        name='n'+str(bit)
        if bit in assignments or bit in leaves:return name
        if bit in active:raise ValueError('combinational loop in collision cone')
        active.add(bit);cell=drivers.get(bit);kind=cell['type'] if cell else ''
        pins=cell['connections'] if cell else {}
        if kind=='LUT4':
            address='{'+','.join(signal(pins['A' if n==0 else chr(ord('A')+n)][0]) for n in reversed(range(4)))+'}'
            init=cell['parameters']['INIT'];expression=f"(16'b{init} >> {address}) & 1'b1"
        elif kind in ('PFUMX','L6MUX21'):
            one,zero,select=('ALUT','BLUT','C0') if kind=='PFUMX' else ('D1','D0','SD')
            expression=signal(pins[select][0])+' ? '+signal(pins[one][0])+' : '+signal(pins[zero][0])
        else:leaves.add(bit);expression=None
        active.remove(bit)
        if expression is not None:assignments[bit]=expression
        return name
    failures=[]
    for cell in cells:
        p=cell['connections']
        failures.append('('+signal(p['CEB'][0])+' & '+signal(p['CEA'][0])+' & '+signal(p['WEA'][0])+
            ' & ('+' | '.join(signal(p[f'ADA{n}'][0]) for n in range(4))+'))')
    declarations=[f'wire n{bit};' for bit in sorted(set(assignments)|leaves)]
    connections=[f'assign n{bit}=symbolic[{n}];' for n,bit in enumerate(sorted(leaves))]
    connections += [f'assign n{bit}={expression};' for bit,expression in assignments.items()]
    return f'module cone(input wire [{max(1,len(leaves))-1}:0] symbolic,output wire bad);\n'+\
        '\n'.join(declarations+connections+['assign bad='+' | '.join(failures)+';','endmodule'])+'\n'


def main():
    directory=ROOT/'build/loadable-ram-check';directory.mkdir(parents=True,exist_ok=True)
    netlist=ROOT/'build/loadable-mapped/design.json';module=json.loads(netlist.read_text())['modules']['wasmetal_loadable']
    inputs=[Path(__file__).resolve(),ROOT/'tools/ecp5_ram.py',ROOT/'tools/ecp5_loadable_ram.py',ROOT/'tools/build_board.py',netlist]
    hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs};examples={};same_edge=[]
    for cell in module['cells'].values():
        if cell['type']!='DP16KD':continue
        try:kind=model.check(cell)
        except ValueError:continue
        examples.setdefault(kind,cell)
        if kind=='ram36-same-edge':same_edge.append(cell)
    if set(examples)!={'ram18-opposite-edges','ram36-same-edge'}:raise ValueError('programmable EBR modes missing')
    rng=random.Random(0x574d50524f47);initial18=[rng.getrandbits(18) for _ in range(1024)];initial36=[rng.getrandbits(36) for _ in range(512)]
    initial18[17]=None;initial36[19]=None
    bench=['module bench;reg clk=0,write18=0,read36=1;reg [1:0] mask18=0;reg [3:0] mask36=0;',
        'reg [9:0] addr18=0;reg [8:0] addr36=0;reg [17:0] data18=0;reg [35:0] data36=0;',
        'wire [17:0] qa18,qb18;wire [35:0] q36;reg [17:0] saved18;reg [35:0] saved36;',
        'reg [17:0] expected18[0:1023];reg [35:0] expected36[0:511];integer n,mask,lane;']
    for width,kind,values in [(18,'ram18-opposite-edges',initial18),(36,'ram36-same-edge',initial36)]:
        cell=copy.deepcopy(examples[kind]);p=cell['parameters'];packed=[]
        for value in values:
            halves=[value] if width==18 else [None,None] if value is None else [value&((1<<18)-1),value>>18]
            for half in halves:packed.append('00'+('x'*18 if half is None else f'{half:018b}'))
        initial=''.join(reversed(packed))
        for block in range(64):p[f'INITVAL_{block:02X}']=initial[len(initial)-(block+1)*320:len(initial)-block*320]
        model.check(cell)
        literals=[f'.{name}('+ (f"{len(value)}'b{value}" if set(value)<=set('01x') else json.dumps(value.rstrip()))+')' for name,value in p.items()]
        pins=[]
        for name,direction in ecp5_ram.PINS.items():
            if direction=='output':expression=(('qa18' if name.startswith('DOA') else 'qb18')+f'[{name[3:]}]' if width==18
                else 'q36['+str(int(name[3:])+(18 if name.startswith('DOB') else 0))+']')
            elif name in ('CLKA','CLKB'):expression='clk'
            elif name=='WEA' and width==18:expression='write18'
            elif name=='CEB' and width==36:expression='read36'
            elif name.startswith('DI'):
                bit=int(name[3:])+(18 if name.startswith('DIB') else 0)
                expression=f'data{width}[{bit}]' if bit<width else "1'b0"
            elif name.startswith('AD'):
                bit=int(name[3:]);low=4 if width==18 else 5
                if name.startswith('ADA') and bit<width//9:expression=f'mask{width}[{bit}]'
                else:expression=f'addr{width}[{bit-low}]' if bit>=low else "1'b0"
            else:
                pin=cell['connections'][name][0];expression="1'b"+pin if isinstance(pin,str) else "1'b0"
            pins.append('.'+name+'('+expression+')')
        bench.append(model.NAME+' #('+','.join(literals)+f') ram{width}('+','.join(pins)+');')
    bench.append('initial begin')
    for width,values in [(18,initial18),(36,initial36)]:
        bench.extend(f'expected{width}[{n}]='+ (f"{width}'bx" if value is None else f"{width}'h{value:x}")+';' for n,value in enumerate(values))
    bench.append('''#2;
for(n=0;n<1024;n=n+1) begin
 addr18=10'(n);#2;saved18=qb18;clk=1;#2;
 if(qa18!==expected18[n] || qb18!==saved18) $fatal(1,"programmable 18 read edge mismatch");
 clk=0;#2;if(qb18!==expected18[n]) $fatal(1,"programmable 18 read mismatch");
 for(mask=0;mask<4;mask=mask+1) begin
  write18=1;mask18=2'(mask);data18=18'((n*31)^(mask*12345));#2;clk=1;#2;
  if(qa18!==expected18[n]) $fatal(1,"programmable 18 read-before-write mismatch");
  for(lane=0;lane<2;lane=lane+1) if(mask18[lane]) expected18[n][lane*9+:9]=data18[lane*9+:9];
  clk=0;#2;if(qb18!==expected18[n]) $fatal(1,"programmable 18 masked write mismatch");
 end
 write18=0;mask18=0;
end
for(n=1023;n>=0;n=n-1) begin
 addr18=10'(n);#2;clk=1;#2;clk=0;#2;
 if(qb18!==expected18[n]) $fatal(1,"programmable 18 address alias");
end
for(n=0;n<512;n=n+1) begin
 addr36=9'(n);read36=1;mask36=0;#2;clk=1;#2;
 if(q36!==expected36[n]) $fatal(1,"programmable 36 read mismatch");
 saved36=q36;clk=0;#2;if(q36!==saved36) $fatal(1,"programmable 36 read on wrong edge");
 for(mask=0;mask<16;mask=mask+1) begin
  read36=0;mask36=4'(mask);data36=36'((n*31)^(mask*12345));#2;clk=1;#2;
  if(q36!==saved36) $fatal(1,"programmable 36 disabled read changed");
  for(lane=0;lane<4;lane=lane+1) if(mask36[lane]) expected36[n][lane*9+:9]=data36[lane*9+:9];
  clk=0;#2;mask36=0;read36=1;clk=1;#2;
  if(q36!==expected36[n]) $fatal(1,"programmable 36 masked write mismatch");
  saved36=q36;clk=0;#2;
 end
end
for(n=511;n>=0;n=n-1) begin
 addr36=9'(n);#2;clk=1;#2;
 if(q36!==expected36[n]) $fatal(1,"programmable 36 address alias");
 clk=0;#2;
end
addr18='x;addr36='x;#2;clk=1;#2;clk=0;#2;
if((^qb18)!==1'bx || (^q36)!==1'bx) $fatal(1,"unknown programmable address became known");
addr36=0;mask36=1;read36=1;#2;clk=1;#2;
if((^q36)!==1'bx) $fatal(1,"read/write collision was treated as valid data");
$display("PASS programmable EBR addresses, lanes, edges, enables and four-state behavior");$finish;
end endmodule
''')
    testbench=directory/'bench.sv';testbench.write_text('\n'.join(bench));behavior=directory/'model.v';behavior.write_text(model.model())
    def run(path,name):
        binary=directory/(name+'.vvp')
        subprocess.run([str(ROOT/'.cache/tools/usr/bin/iverilog'),'-B'+str(ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl'),
            '-g2012','-s','bench','-o',str(binary),str(path),str(testbench)],cwd=ROOT,check=True,capture_output=True,timeout=60)
        result=subprocess.run([str(ROOT/'.cache/tools/usr/bin/vvp'),str(binary)],cwd=ROOT,capture_output=True,text=True,timeout=60)
        (directory/(name+'.log')).write_text(result.stdout+result.stderr);return result
    result=run(behavior,'positive')
    if result.returncode:raise RuntimeError(result.stdout+result.stderr)
    rejected=[]
    for name,old,new,message in [('bad-read','read_b<=memory[address_b[13:4]];',"read_b<=18'b0;",'programmable 18 read mismatch'),
            ('ignored-mask','if(address_a[lane]) memory[address_a[13:5]]','if(1\'b1) memory[address_a[13:5]]','programmable 36 read mismatch')]:
        text=behavior.read_text();assert text.count(old)==1
        path=directory/(name+'.v');path.write_text(text.replace(old,new));negative=run(path,name)
        if negative.returncode==0 or message not in negative.stdout:raise ValueError('bad primitive negative control: '+name)
        rejected.append(name)
    def prove(cells,name,positive):
        cone=directory/(name+'.sv');cone.write_text(collision_cone(module,cells))
        try:yosys(f'read_verilog -sv {cone}\nprep -top cone\nsat -set-def-inputs -enable_undef -prove bad 0 -verify\n',name,directory)
        except subprocess.CalledProcessError:
            if positive or 'proof did fail' not in (directory/(name+'.log')).read_text():raise
        else:
            if not positive:raise ValueError('collision proof accepted disabled read protection')
    prove(same_edge,'collision',True)
    broken=copy.deepcopy(same_edge);broken[0]['connections']['CEB']=['1'];prove(broken,'collision-negative',False)
    rejected.append('disabled-read-protection')
    admission_rejected=0
    for original in examples.values():
        for name,value in [('REGMODE_A','OUTREG'),('DATA_WIDTH_A','100'),('WEB',['1'])]:
            cell=copy.deepcopy(original)
            if name=='WEB':cell['connections'][name]=value
            else:cell['parameters'][name]=value
            try:model.check(cell)
            except ValueError:admission_rejected+=1
            else:raise ValueError('primitive admission accepted an unsupported configuration')
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise RuntimeError('programmable RAM test inputs changed')
    report={'status':'passed','scope':'exact mapped programmable EBR modes and combinational exclusion of same-edge read/write',
        'modes':list(examples),'addresses':{'ram18':1024,'ram36':512},'mask_patterns':{'ram18':4,'ram36':16},
        'same_edge_memories_proven':len(same_edge),'proof_abstraction':'every non-LUT/mux output is an unconstrained Boolean input; all physical addresses conservatively ignored',
        'negative_controls_rejected':rejected,'unsupported_configurations_rejected':admission_rejected,
        'inputs':hashes,'physical_hardware_tested':False}
    (ROOT/'reports/loadable-ram.json').write_text(json.dumps(report,indent=2)+'\n');print(result.stdout.strip())


if __name__=='__main__':main()
