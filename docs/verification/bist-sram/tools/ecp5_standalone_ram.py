"""Functional models for additional, explicitly checked standalone EBR modes.

Port/address packing follows the pinned Yosys ecp5/brams_map.v and brams.txt.
Clocked NOREG and READBEFOREWRITE behavior follows Lattice FPGA-TN-02204.
This accepts only the configurations actually used by the standalone wrapper;
the existing core RAM model and its admission checks are unchanged.
"""
import re
import ecp5_ram

NAME='WASMETAL_LOCAL_DP16KD'


def check(cell, consumed=None):
    p=cell['parameters']; pins=cell['connections']
    if set(pins)!=set(ecp5_ram.PINS): raise ValueError('unexpected standalone RAM ports')
    for name,direction in ecp5_ram.PINS.items():
        if direction=='input' and len(pins[name])!=1: raise ValueError('missing standalone RAM input')
    widths=tuple(int(p.get(name,'0'),2) for name in ('DATA_WIDTH_A','DATA_WIDTH_B'))
    if widths not in ((36,36),(18,18),(1,18)): raise ValueError('unmodeled standalone RAM widths')
    width=widths[0]
    expected=dict(ecp5_ram.MODES)
    if width==36 and p.get('CLKBMUX')=='CLKB': expected['CLKBMUX']='CLKB'
    if width!=36:
        expected.update(CLKBMUX='CLKB',WRITEMODE_A='READBEFOREWRITE',WRITEMODE_B='READBEFOREWRITE')
        if width==18 and p.get('CLKAMUX')=='INV': expected['CLKAMUX']='INV'
    for name,value in p.items():
        if re.fullmatch(r'INITVAL_[0-3][0-9A-F]',name):
            if len(value)!=320 or set(value)-set('01x'): raise ValueError('unsupported RAM initialization')
            if width==1 and set(value)-{'0'}: raise ValueError('single-bit RAM model requires zero initialization')
        elif name not in expected and name not in ('DATA_WIDTH_A','DATA_WIDTH_B'):
            raise ValueError('unmodeled standalone RAM parameter: '+name)
    for name,value in expected.items():
        if p.get(name,'NORMAL' if name.startswith('WRITEMODE_') else '').rstrip()!=value:
            raise ValueError('unmodeled standalone RAM mode: '+name)
    fixed={name:'0' for name in ('RSTA','RSTB','WEB')}
    fixed.update({f'CS{side}{n}':'0' for side in 'AB' for n in range(3)})
    fixed.update({'CEA':'0' if width==36 else '1','CEB':'1' if width==36 else '0',
                  'OCEA':'0' if width==36 else '1','OCEB':'1'})
    if width==36:
        fixed.update(CLKA='0',WEA='1')
        fixed.update({f'ADB{n}':'0' for n in range(5)})
    else:
        fixed['CLKB']='0'
        if width==18:
            fixed['WEA']='0'
            fixed.update({f'ADA{n}':'0' for n in range(4)})
    for name,value in fixed.items():
        if pins[name]!=[value]: raise ValueError('unmodeled standalone RAM control: '+name)
    unused=[]
    if width!=36: unused += [f'DOB{n}' for n in range(18)]
    if width==1: unused += [f'DOA{n}' for n in range(1,18)]
    if consumed is not None and any(bit in consumed for name in unused for bit in pins[name]):
        raise ValueError('unused RAM data bits feed live logic')
    return ('rom36' if expected['CLKBMUX']=='INV' else 'rom36-positive') if width==36 else (
        'ram1' if width==1 else 'rom18-'+expected['CLKAMUX'])


def model():
    concat=lambda prefix,width:'{'+','.join(prefix+str(n) for n in reversed(range(width)))+'}'
    lines=['module '+NAME+' ('+',\n'.join(direction+' wire '+name for name,direction in ecp5_ram.PINS.items())+');']
    lines += [f'parameter {name}="{value}";' for name,value in ecp5_ram.MODES.items()]
    lines += ['parameter DATA_WIDTH_A=36, DATA_WIDTH_B=36;']
    lines += [f"parameter [319:0] INITVAL_{n:02X}=320'b0;" for n in range(64)]
    lines += ['localparam [20479:0] INITIAL={'+','.join(f'INITVAL_{n:02X}' for n in reversed(range(64)))+'};',
              'wire [13:0] address_a='+concat('ADA',14)+';',
              'wire clock_a=CLKAMUX=="INV" ? !CLKA : CLKA;',
              'wire clock_b_for_negedge=CLKBMUX=="INV" ? CLKB : !CLKB;',
              'generate if(DATA_WIDTH_A==36) begin: readonly_wide']
    params=list(ecp5_ram.MODES)+['DATA_WIDTH_A','DATA_WIDTH_B']+[f'INITVAL_{n:02X}' for n in range(64)]
    lines += ['DP16KD #('+','.join('.'+name+'('+name+')' for name in params)+') storage('+','.join(
        '.'+name+'('+('clock_b_for_negedge' if name=='CLKB' else name)+')' for name in ecp5_ram.PINS)+');',
        'end else if(DATA_WIDTH_A==18) begin: readonly_word',
        'reg [17:0] result_a;',
        'assign '+concat('DOA',18)+'=result_a;',
        'assign '+concat('DOB',18)+"=18'bx;",
        'always @(posedge clock_a) if(CEA) result_a<=INITIAL[address_a[13:4]*20+:18];',
        'end else begin: single_bit',
        'reg memory [0:16383]; reg result_a; integer row;',
        # Only all-zero initial contents are admitted for this single-bit mode.
        'initial for(row=0;row<16384;row=row+1) memory[row]=0;',
        'assign '+concat('DOA',18)+"={17'bx,result_a};",
        'assign '+concat('DOB',18)+"=18'bx;",
        'always @(posedge clock_a) if(CEA) begin',
        '    result_a<=memory[address_a];',
        '    if(WEA) memory[address_a]<=DIA0;',
        'end',
        'end endgenerate',
        'endmodule']
    return '\n'.join(lines)+'\n'
