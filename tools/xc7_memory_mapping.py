#!/usr/bin/env python3
"""Correct pinned 7-series RAM wiring without changing installed CAD tools."""
import json
from pathlib import Path

from prepare_standalone import ROOT, digest

LIBRARY = ROOT / '.cache/tools/usr/share/yosys/xilinx'
PINNED = {
    'brams_xc6v_map.v': '678908f431dd3304aa41f2d1cb87ed6958c20adff848a0b3a6ea8903e59a1008',
    'brams_defs.vh': '6060e135ee7cc4a391d06547f0c6f37bf6da55878cc58be89165078526b04a55',
    'brams_xc4v.txt': '13e895e452af7e34161aa7572f4e11ab81d787fc1b9b85d10c713f03554b85f2',
    'lutrams_xc5v.txt': '88b460c2a164059c4fb7cf89f71f7a657a993905c275e6acd8685a316d3a8ce9',
    'lutrams_xc5v_map.v': 'a88ef19a3318a4b45655d826bfcb80f17bd241fa4f573fca8dcd6b12c5640cff',
}
BEFORE = '.DIPBDIP(PORT_W_WIDTH == 71 ? DIP[7:4] : DIP[3:0])'
AFTER = '.DIPBDIP(PORT_W_WIDTH == 72 ? DIP[7:4] : DIP[3:0])'
UPSTREAM = 'https://github.com/YosysHQ/yosys/blob/24471b847a1c90b6b7a0e0535f15ea48b477d5b4/techlibs/xilinx/brams_xc6v_map.v'
PIN_GUIDE = 'https://docs.amd.com/api/khub/documents/9gZGbqBxtlKXxBfkBt~lAg/content'
ADDRESS_FUNCTION = '''
// WasMetal adaptation: UG473 pp. 30 and 38, non-cascaded RAMB36E1 pins.
function [15:0] wasmetal_ramb36_unused;
    input integer read_width, write_width;
    integer width;
    reg [15:0] unused_low;
    begin
        // Mixed-width ports must retain every bit needed by either direction.
        width = read_width == 0 ? write_width :
                write_width == 0 ? read_width :
                read_width < write_width ? read_width : write_width;
        case (width)
            0: unused_low=16'h7fff;
            1: unused_low=16'h0000;
            2: unused_low=16'h0001;
            4: unused_low=16'h0003;
            9: unused_low=16'h0007;
            18: unused_low=16'h000f;
            36: unused_low=16'h001f;
            72: unused_low=16'h003f;
            default: unused_low=16'hxxxx;
        endcase
        wasmetal_ramb36_unused=16'h8000 | unused_low;
    end
endfunction
'''
ADDRESS_PATCHES = {
    ".ADDRARDADDR({1'b1, PORT_A_ADDR[14:0]})":
        '.ADDRARDADDR(PORT_A_ADDR | wasmetal_ramb36_unused(PORT_A_RD_USED ? PORT_A_RD_WIDTH : 0, PORT_A_WR_USED ? PORT_A_WR_WIDTH : 0))',
    ".ADDRBWRADDR({1'b1, PORT_B_ADDR[14:0]})":
        '.ADDRBWRADDR(PORT_B_ADDR | wasmetal_ramb36_unused(PORT_B_RD_USED ? PORT_B_RD_WIDTH : 0, PORT_B_WR_USED ? PORT_B_WR_WIDTH : 0))',
    ".ADDRARDADDR({1'b1, PORT_R_ADDR})":
        '.ADDRARDADDR(PORT_R_ADDR | wasmetal_ramb36_unused(PORT_R_USED ? PORT_R_WIDTH : 0, 0))',
    ".ADDRBWRADDR({1'b1, PORT_W_ADDR})":
        '.ADDRBWRADDR(PORT_W_ADDR | wasmetal_ramb36_unused(0, PORT_W_USED ? PORT_W_WIDTH : 0))',
}


def audit_address_pins(design):
    """Fail closed on incorrect non-cascaded RAMB36E1 widths or unused addresses."""
    shifts = {1: 0, 2: 1, 4: 2, 9: 3, 18: 4, 36: 5, 72: 6}
    checked_cells = checked_pins = 0
    for name, cell in design['cells'].items():
        if cell['type'] != 'RAMB36E1':
            continue
        checked_cells += 1
        params = cell['parameters']
        if params.get('RAM_MODE', '').strip() not in ('TDP', 'SDP'):
            raise ValueError('review RAM mode: ' + name)
        for side, port in [('A', 'ADDRARDADDR'), ('B', 'ADDRBWRADDR')]:
            if params.get('RAM_EXTENSION_' + side, 'NONE').strip() != 'NONE':
                raise ValueError('review cascaded RAM address pins: ' + name)
            widths = []
            for direction in ['READ', 'WRITE']:
                bits = params[f'{direction}_WIDTH_{side}']
                if not bits or set(bits) - {'0', '1'}:
                    raise ValueError('unknown RAM port width: ' + name)
                width = int(bits, 2)
                if width:
                    if width not in shifts:
                        raise ValueError('unsupported RAM port width: ' + name)
                    widths.append(width)
            unused = [15, *range(shifts[min(widths)] if widths else 15)]
            pins = cell['connections'][port]
            if len(pins) != 16 or any(pins[bit] != '1' for bit in unused):
                raise ValueError('non-cascaded RAM address-pin contract: ' + name + '.' + port)
            checked_pins += len(unused)
    return {'status': 'passed', 'ram36_cells': checked_cells,
            'constant_high_address_pins': checked_pins, 'source': PIN_GUIDE}


def prepare(directory):
    """Return pinned xc7 map_memory commands with parity and address corrections."""
    directory = Path(directory).resolve()
    for name, expected in PINNED.items():
        if digest(LIBRARY / name) != expected:
            raise ValueError('review changed pinned Xilinx mapping input: ' + name)
    source = (LIBRARY / 'brams_xc6v_map.v').read_text()
    if source.count(BEFORE) != 1 or AFTER in source:
        raise ValueError('review 72-bit parity mapping patch anchor')
    source = source.replace(BEFORE, AFTER)
    for before, after in ADDRESS_PATCHES.items():
        if source.count(before) != 1:
            raise ValueError('review RAM address mapping patch anchor: ' + before)
        source = source.replace(before, after)
    anchor = '`include "brams_defs.vh"'
    if source.count(anchor) != 2:
        raise ValueError('review RAM address helper insertion points')
    source = source.replace(anchor, anchor + '\n' + ADDRESS_FUNCTION)
    directory.mkdir(parents=True, exist_ok=True)
    mapping = directory / 'brams_xc6v_map.v'
    mapping.write_text(source)
    include = directory / 'brams_defs.vh'
    include.write_bytes((LIBRARY / include.name).read_bytes())
    # Keep every xc7 option from synth_xilinx.cc in pinned Yosys 0.33, including
    # conflict handling and the ROM cost. Only the following map file changes.
    commands = '''memory_libmap -logic-cost-rom 0.015625 -lib +/xilinx/lutrams_xc5v.txt -lib +/xilinx/brams_xc4v.txt -D HAS_SIZE_36 -D HAS_CASCADE -D HAS_CONFLICT_BUG -D HAS_MIXWIDTH_SDP -no-auto-huge
techmap -map +/xilinx/lutrams_xc5v_map.v
techmap -map ''' + json.dumps(str(mapping)) + '\n'
    receipt = {
        'scope': 'Yosys 0.33 xc7 memory mapping; correct 72-bit SDP parity inputs and non-cascaded RAMB36E1 unused address pins',
        'upstream_fixed_source': UPSTREAM,
        'patch': {'before': BEFORE, 'after': AFTER, 'replacements': 1},
        'address_pin_guidance': PIN_GUIDE,
        'address_patches': ADDRESS_PATCHES,
        'address_function_insertions': 2,
        'inputs': {str((LIBRARY / n).relative_to(ROOT)): h for n, h in PINNED.items()},
        'outputs': {str(p.relative_to(ROOT)): digest(p) for p in [mapping, include]},
        'commands': commands,
        'installed_tools_modified': False,
    }
    return commands, receipt
