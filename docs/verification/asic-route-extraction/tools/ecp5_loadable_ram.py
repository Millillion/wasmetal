"""Strict models for programmable 1024x18 and same-clock 512x36 EBR stores.

Pin/initialization packing follows pinned Yosys ecp5/brams_map.v; clock behavior
follows Lattice FPGA-TN-02204-1.6. Same-clock write/read collisions return X.
The integration must independently prove those collisions cannot occur.
"""
import re
import ecp5_ram

NAME='WASMETAL_PROGRAM_DP16KD'


def check(cell,consumed=None):
    p=cell['parameters'];pins=cell['connections']
    if set(pins)!=set(ecp5_ram.PINS):raise ValueError('unexpected programmable RAM ports')
    if any(len(pins[name])!=1 for name,direction in ecp5_ram.PINS.items() if direction=='input'):
        raise ValueError('missing programmable RAM input')
    widths=tuple(int(p.get(name,'0'),2) for name in ('DATA_WIDTH_A','DATA_WIDTH_B'))
    if widths not in ((18,18),(36,36)):raise ValueError('unsupported programmable RAM widths')
    width=widths[0];expected=dict(ecp5_ram.MODES)
    if width==18:expected.update(WRITEMODE_A='READBEFOREWRITE',WRITEMODE_B='READBEFOREWRITE')
    else:expected['CLKBMUX']='CLKB'
    for name,value in p.items():
        if re.fullmatch(r'INITVAL_[0-3][0-9A-F]',name):
            if len(value)!=320 or set(value)-set('01x'):raise ValueError('unsupported programmable RAM initialization')
        elif name not in expected and name not in ('DATA_WIDTH_A','DATA_WIDTH_B'):
            raise ValueError('unexpected programmable RAM parameter')
    for name,value in expected.items():
        if p.get(name,'NORMAL' if name.startswith('WRITEMODE_') else '').rstrip()!=value:
            raise ValueError('unsupported programmable RAM mode: '+name)
    fixed={'RSTA':'0','RSTB':'0','WEB':'0','CEA':'1','OCEB':'1','OCEA':'1' if width==18 else '0'}
    fixed.update({f'CS{side}{n}':'0' for side in 'AB' for n in range(3)})
    fixed.update({f'ADB{n}':'0' for n in range(4 if width==18 else 5)})
    if width==18:fixed.update(CEB='1',ADA2='0',ADA3='0')
    else:fixed.update(WEA='1',ADA4='0')
    for name,value in fixed.items():
        if pins[name]!=[value]:raise ValueError('unsupported programmable RAM control: '+name)
    if pins['CLKA']!=pins['CLKB']:raise ValueError('programmable RAM requires a shared clock')
    return 'ram18-opposite-edges' if width==18 else 'ram36-same-edge'


def model():
    concat=lambda prefix,width:'{'+','.join(prefix+str(n) for n in reversed(range(width)))+'}'
    lines=['module '+NAME+'('+','.join(direction+' wire '+name for name,direction in ecp5_ram.PINS.items())+');']
    lines += [f'parameter {name}="{value}";' for name,value in ecp5_ram.MODES.items()]
    lines += ['parameter DATA_WIDTH_A=18,DATA_WIDTH_B=18;']
    lines += [f"parameter [319:0] INITVAL_{n:02X}=320'bx;" for n in range(64)]
    lines += ['localparam [20479:0] INITIAL={'+','.join(f'INITVAL_{n:02X}' for n in reversed(range(64)))+'};',
        'wire [13:0] address_a='+concat('ADA',14)+',address_b='+concat('ADB',14)+';',
        'wire [17:0] data_a='+concat('DIA',18)+',data_b='+concat('DIB',18)+';',
        'generate if(DATA_WIDTH_A==18) begin: instructions',
        'reg [17:0] memory[0:1023];reg [17:0] read_a,read_b;integer row,lane;',
        'initial for(row=0;row<1024;row=row+1) memory[row]=INITIAL[row*20+:18];',
        'assign '+concat('DOA',18)+'=read_a;',
        'assign '+concat('DOB',18)+'=read_b;',
        'always @(posedge CLKA) if(CEA) begin',
        '    read_a<=memory[address_a[13:4]];',
        '    if(WEA) for(lane=0;lane<2;lane=lane+1)',
        '        if(address_a[lane]) memory[address_a[13:4]][lane*9+:9]<=data_a[lane*9+:9];',
        'end',
        'always @(negedge CLKB) if(CEB) read_b<=memory[address_b[13:4]];',
        'end else begin: regions',
        'reg [35:0] memory[0:511];reg [35:0] read_value;integer row,lane;',
        'initial for(row=0;row<512;row=row+1) memory[row]={INITIAL[(2*row+1)*20+:18],INITIAL[2*row*20+:18]};',
        'assign {'+concat('DOB',18)+','+concat('DOA',18)+'}=read_value;',
        'wire [35:0] data_in={data_b,data_a};',
        'always @(posedge CLKA) if(CEA && WEA) begin',
        '    for(lane=0;lane<4;lane=lane+1)',
        '        if(address_a[lane]) memory[address_a[13:5]][lane*9+:9]<=data_in[lane*9+:9];',
        'end',
        'always @(posedge CLKB) if(CEB) begin',
        "    if(CEA && WEA && (|address_a[3:0]) && address_a[13:5]==address_b[13:5]) read_value<='x;",
        '    else read_value<=memory[address_b[13:5]];',
        'end',
        'end endgenerate',
        'endmodule']
    return '\n'.join(lines)+'\n'
