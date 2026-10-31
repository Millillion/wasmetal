"""Checked functional model for the exact ECP5 block-RAM mode WasMetal uses.

The pin packing follows pinned Yosys' ecp5/brams_map.v. Clocked pseudo-dual-port
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
    for name, value in MODES.items():
        actual = parameters.get(name, 'NORMAL' if name.startswith('WRITEMODE_') else '')
        if actual.rstrip() != value:
            raise ValueError('unsupported ECP5 RAM mode: '+name)
    for name in ('DATA_WIDTH_A', 'DATA_WIDTH_B'):
        if int(parameters.get(name, '0'), 2) != 36:
            raise ValueError('ECP5 RAM model requires 512 by 36 mode')
    pins = cell['connections']
    if set(pins) != set(PINS):
        raise ValueError('unexpected ECP5 RAM ports')
    for name, direction in PINS.items():
        if direction == 'input' and len(pins[name]) != 1:
            raise ValueError('missing ECP5 RAM input: '+name)
    fixed = {'CEA': '1', 'CEB': '1', 'WEA': '1', 'WEB': '0',
             'OCEA': '0', 'OCEB': '1', 'RSTA': '0', 'RSTB': '0', 'ADA4': '0'}
    fixed.update({f'CS{side}{bit}': '0' for side in 'AB' for bit in range(3)})
    fixed.update({f'ADB{bit}': '0' for bit in range(5)})
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
        'reg [35:0] memory [0:511];', 'reg [35:0] read_value;',
        'assign {'+concat('DOB', 18)+','+concat('DOA', 18)+'}=read_value;',
        'localparam [20479:0] INITIAL={'+','.join(f'INITVAL_{i:02X}' for i in reversed(range(64)))+'};',
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
        'endmodule',
    ]
    return '\n'.join(lines)+'\n'
