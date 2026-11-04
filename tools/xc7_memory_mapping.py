#!/usr/bin/env python3
"""Apply the upstream 72-bit parity-pin fix without changing installed CAD tools."""
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


def prepare(directory):
    """Return the exact Yosys 0.33 xc7 map_memory commands with one pin correction."""
    directory = Path(directory).resolve()
    for name, expected in PINNED.items():
        if digest(LIBRARY / name) != expected:
            raise ValueError('review changed pinned Xilinx mapping input: ' + name)
    source = (LIBRARY / 'brams_xc6v_map.v').read_text()
    if source.count(BEFORE) != 1 or AFTER in source:
        raise ValueError('review 72-bit parity mapping patch anchor')
    directory.mkdir(parents=True, exist_ok=True)
    mapping = directory / 'brams_xc6v_map.v'
    mapping.write_text(source.replace(BEFORE, AFTER))
    include = directory / 'brams_defs.vh'
    include.write_bytes((LIBRARY / include.name).read_bytes())
    # Keep every xc7 option from synth_xilinx.cc in pinned Yosys 0.33, including
    # conflict handling and the ROM cost. Only the following map file changes.
    commands = '''memory_libmap -logic-cost-rom 0.015625 -lib +/xilinx/lutrams_xc5v.txt -lib +/xilinx/brams_xc4v.txt -D HAS_SIZE_36 -D HAS_CASCADE -D HAS_CONFLICT_BUG -D HAS_MIXWIDTH_SDP -no-auto-huge
techmap -map +/xilinx/lutrams_xc5v_map.v
techmap -map ''' + json.dumps(str(mapping)) + '\n'
    receipt = {
        'scope': 'Yosys 0.33 xc7 memory mapping; correct upper parity-data inputs in 72-bit SDP mode',
        'upstream_fixed_source': UPSTREAM,
        'patch': {'before': BEFORE, 'after': AFTER, 'replacements': 1},
        'inputs': {str((LIBRARY / n).relative_to(ROOT)): h for n, h in PINNED.items()},
        'outputs': {str(p.relative_to(ROOT)): digest(p) for p in [mapping, include]},
        'commands': commands,
        'installed_tools_modified': False,
    }
    return commands, receipt
