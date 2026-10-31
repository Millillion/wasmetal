"""Checked functional model for the exact ECP5 block-RAM mode WasMetal uses.

The pin packing follows pinned Yosys' ecp5/brams_map.v. Clocked 512-by-36 pseudo-dual-port and 2048-by-9 dual-port
behavior follows Lattice FPGA-TN-02204-1.6, sections 4.3 and A.2. This model is
not a general replacement for Lattice's simulation library or a timing model.
"""
import re


MODES = {
    'REGMODE_A': 'NOREG', 'REGMODE_B': 'NOREG',
    'CLKAMUX': 'CLKA', 'CLKBMUX': 'INV',
    'RESETMODE': 'ASYNC', 'ASYNC_RESET_RELEASE': 'ASYNC',
    'CSDECODE_A': '0b000', 'CSDECODE_B': '0b000',
    'WRITEMODE_A': 'NORMAL', 'WRITEMODE_B': 'NORMAL', 'GSR': 'DISABLED',
}
PINS = {}
for side in 'AB':
    for prefix, width in [('DI', 18), ('AD', 14), ('CS', 3)]:
        PINS.update({f'{prefix}{side}{bit}': 'input' for bit in range(width)})
    PINS.update({name+side: 'input' for name in ['CE', 'OCE', 'CLK', 'WE', 'RST']})
    PINS.update({f'DO{side}{bit}': 'output' for bit in range(18)})


def check(cell):
    """Reject every configuration not covered by this model and its tests."""
    parameters = cell['parameters']
    for name, value in parameters.items():
        if re.fullmatch(r'INITVAL_[0-3][0-9A-F]', name):
            if len(value) != 320 or set(value)-set('01x'):
                raise ValueError('unsupported ECP5 RAM initialization')
        elif name not in MODES and name not in ('DATA_WIDTH_A', 'DATA_WIDTH_B'):
            raise ValueError('unsupported ECP5 RAM parameter: '+name)
    widths=[int(parameters.get(name,'0'),2) for name in ('DATA_WIDTH_A','DATA_WIDTH_B')]
    if widths[0] != widths[1] or widths[0] not in (9,36):
        raise ValueError('ECP5 RAM model requires matching 9-bit or 36-bit ports')
    width=widths[0]
    for name, value in MODES.items():
        if width==9 and name.startswith('WRITEMODE_'): value='READBEFOREWRITE'
        actual = parameters.get(name, 'NORMAL' if name.startswith('WRITEMODE_') else '')
        if actual.rstrip() != value:
            raise ValueError('unsupported ECP5 RAM mode: '+name)
    pins = cell['connections']
    if set(pins) != set(PINS):
        raise ValueError('unexpected ECP5 RAM ports')
    for name, direction in PINS.items():
        if direction == 'input' and len(pins[name]) != 1:
            raise ValueError('missing ECP5 RAM input: '+name)
    fixed = {'CEA': '1', 'CEB': '1', 'WEB': '0',
             'OCEA': '0' if width==36 else '1', 'OCEB': '1', 'RSTA': '0', 'RSTB': '0'}
    if width==36: fixed.update({'WEA':'1','ADA4':'0'})
    else: fixed.update({f'ADA{bit}':'0' for bit in range(3)})
    fixed.update({f'CS{side}{bit}': '0' for side in 'AB' for bit in range(3)})
    fixed.update({f'ADB{bit}': '0' for bit in range(5 if width==36 else 3)})
    for name, value in fixed.items():
        if pins[name] != [value]:
            raise ValueError('unsupported ECP5 RAM control: '+name)
    if pins['CLKA'] != pins['CLKB']:
        raise ValueError('ECP5 RAM model requires opposite edges of one clock')


def model():
    concat = lambda prefix, width: '{'+','.join(prefix+str(bit) for bit in reversed(range(width)))+'}'
    lines = ['module DP16KD ('+',\n'.join(direction+' wire '+name for name, direction in PINS.items())+');']
    lines += [f'parameter {name}="{value}";' for name, value in MODES.items()]
    lines += ['parameter DATA_WIDTH_A=36, DATA_WIDTH_B=36;']
    lines += [f"parameter [319:0] INITVAL_{i:02X}=320'b0;" for i in range(64)]
    lines += [
        'wire [35:0] data_in={'+concat('DIB', 18)+','+concat('DIA', 18)+'};',
        'wire [13:0] address_a='+concat('ADA', 14)+';',
        'wire [13:0] address_b='+concat('ADB', 14)+';',
        'localparam [20479:0] INITIAL={'+','.join(f'INITVAL_{i:02X}' for i in reversed(range(64)))+'};',
        'generate if(DATA_WIDTH_A==36) begin: wide',
        'reg [35:0] memory [0:511];', 'reg [35:0] read_value;',
        'assign {'+concat('DOB', 18)+','+concat('DOA', 18)+'}=read_value;',
        'integer row,lane;',
        'initial begin',
        '    for(row=0;row<512;row=row+1)',
        '        memory[row]={INITIAL[(2*row+1)*20+:18],INITIAL[2*row*20+:18]};',
        'end',
        '// The low four address pins enable separate nine-bit write lanes.',
        'always @(posedge CLKA) if(CEA && WEA) begin',
        '    for(lane=0;lane<4;lane=lane+1)',
        '        if(address_a[lane]) memory[address_a[13:5]][lane*9+:9]<=data_in[lane*9+:9];',
        'end',
        '// NOREG omits the additional output pipeline, not the clocked read.',
        'always @(negedge CLKB) if(CEB) read_value<=memory[address_b[13:5]];',
        'end else begin: narrow',
        'reg [8:0] memory [0:2047];',
        'reg [8:0] read_a,read_b;',
        'assign '+concat('DOA',18)+"={9'b0,read_a};",
        'assign '+concat('DOB',18)+"={9'b0,read_b};",
        'integer row;',
        'initial for(row=0;row<2048;row=row+1)',
        '    memory[row]=INITIAL[(row/2)*20+(row%2)*9+:9];',
        'always @(posedge CLKA) if(CEA) begin',
        '    read_a<=memory[address_a[13:3]];',
        '    if(WEA) memory[address_a[13:3]]<=data_in[8:0];',
        'end',
        'always @(negedge CLKB) if(CEB) read_b<=memory[address_b[13:3]];',
        'end endgenerate',
        'endmodule',
    ]
    return '\n'.join(lines)+'\n'
