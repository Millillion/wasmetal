#!/usr/bin/env python3
"""Map the host-backed execution core to corrected 7-series primitives."""
from collections import Counter
import datetime
import json
from pathlib import Path
import re
import subprocess
import time

from build_board import yosys
from prepare_standalone import ROOT, digest
from xc7_memory_mapping import audit_address_pins, prepare as prepare_memory_mapping


def main():
    started = time.monotonic()
    top = 'wasmetal_core'; directory = ROOT/'build/xc7-core'
    directory.mkdir(parents=True,exist_ok=True)
    report = ROOT/'reports/xc7-core-estimate.json';report.parent.mkdir(exist_ok=True)
    manifest = directory/'mapped.manifest.json'
    report.unlink(missing_ok=True);manifest.unlink(missing_ok=True)
    profile_path = ROOT/'fpga/profile.json';profile = json.loads(profile_path.read_text())
    expected_parameters = {'VALUE_DEPTH','CONTROL_DEPTH','CALL_DEPTH','MEMORY_COUNT','HEAP_SLOTS'}
    if set(profile)!=expected_parameters or any(type(v) is not int or not 1<=v<1<<30 for v in profile.values()):
        raise ValueError('invalid host-backed core capacities')
    ports = json.loads((ROOT/'fpga/ports.json').read_text())
    expected_ports = {'clk':('input',1)}
    expected_ports.update({p['name']:(direction,p['width']) for direction,items in ports.items() for p in items})
    vendor = ROOT/'third_party/hardfloat/source'
    rtl = [*sorted((ROOT/'rtl').glob('*.sv')),*sorted(vendor.glob('*.v')),vendor/'RISCV/HardFloat_specialize.v']
    library = ROOT/'.cache/tools/usr/share/yosys'
    memory_commands,memory_mapping = prepare_memory_mapping(directory/'mapping-overlay')
    inputs = [*rtl,*sorted(vendor.rglob('*.vi')),Path(__file__).resolve(),profile_path,ROOT/'fpga/ports.json',
        ROOT/'tools/xc7_memory_mapping.py',ROOT/'tools/build_board.py',ROOT/'tools/prepare_standalone.py',
        ROOT/'tools/upstream.lock.json',*[ROOT/name for name in memory_mapping['outputs']],
        *[p for p in sorted((library/'xilinx').rglob('*')) if p.is_file()],
        *[p for p in sorted(library.glob('*.v')) if p.is_file()],
        ROOT/'.cache/tools/usr/bin/yosys',ROOT/'.cache/tools/usr/bin/yosys-abc']
    hashes = {str(p.relative_to(ROOT)):digest(p) for p in inputs}
    base = f'synth_xilinx -family xc7 -top {top} -noiopad -noclkbuf'
    # Use the verified whole-system recipe with the core top and host-backed
    # capacity profile. The ending -run labels are exclusive.
    script = 'read_verilog -sv -defer -Ithird_party/hardfloat/source -Ithird_party/hardfloat/source/RISCV '+\
        ' '.join(str(p.relative_to(ROOT)) for p in rtl)+'\nchparam '+\
        ' '.join(f'-set {k} {v}' for k,v in profile.items())+f' {top}\n'+f'''
{base} -flatten -run begin:map_dsp
share -fast
{base} -run map_dsp:coarse
techmap -map +/cmp2lut.v -map +/cmp2lcu.v -D LUT_WIDTH=6
alumacc
opt
memory -nomap
opt_clean
check -assert
write_json {directory}/generic.json
{memory_commands}{base} -run map_ffram:check
check -assert
write_json {directory}/mapped.json
'''
    yosys(script,'synthesis',directory)
    generic = json.loads((directory/'generic.json').read_text())['modules'][top]
    memories = {name:c for name,c in generic['cells'].items() if c['type']=='$mem_v2'}
    bits = lambda c:int(c['parameters']['WIDTH'],2)*int(c['parameters']['SIZE'],2)
    if sum(bits(c) for name,c in memories.items() if name.startswith('value_file.'))!=profile['VALUE_DEPTH']*128:
        raise ValueError('value-stack capacity changed before mapping')
    module = json.loads((directory/'mapped.json').read_text())['modules'][top]
    if {n:int(v,2) for n,v in module['parameter_default_values'].items()}!=profile:
        raise ValueError('mapped core capacities differ from the requested profile')
    if {n:(p['direction'],len(p['bits'])) for n,p in module['ports'].items()}!=expected_ports:
        raise ValueError('mapped core interface differs from the host contract')
    counts = Counter(c['type'] for c in module['cells'].values())
    allowed = {'CARRY4','DSP48E1','FDCE','FDRE','FDRE_1','FDSE','INV','MUXF7','MUXF8',
               'RAM64M','RAMB18E1','RAMB36E1',*['LUT'+str(n) for n in range(1,7)]}
    if set(counts)-allowed:raise ValueError('unreviewed mapped primitive: '+str(set(counts)-allowed))
    address_audit = audit_address_pins(module)
    for name,value in hashes.items():
        if digest(ROOT/name)!=value:raise ValueError('synthesis input changed: '+name)
    executable = ROOT/'.cache/tools/usr/bin/yosys'
    result = {'status':'synthesized_and_structurally_checked','family':'xc7','top':top,
        'captured_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope':'execution core at the host-backed official-suite capacities; host memory/runtime services remain in the harness',
        'parameters':profile,'inputs':hashes,'memory_mapping':memory_mapping,'ram_address_pin_audit':address_audit,
        'cell_counts':dict(sorted(counts.items())),'generic_memory_count':len(memories),
        'generic_memory_bits':sum(bits(c) for c in memories.values()),
        'logic_lut_primitives':sum(counts['LUT'+str(n)] for n in range(1,7)),
        'flip_flops':sum(n for kind,n in counts.items() if kind.startswith('FD')),
        'ram36_equivalent':counts['RAMB36E1']+counts['RAMB18E1']/2,
        'netlist_sha256':digest(directory/'mapped.json'),'generic_netlist_sha256':digest(directory/'generic.json'),
        'script_sha256':digest(directory/'synthesis.ys'),'log_sha256':digest(directory/'synthesis.log'),
        'tool_version':subprocess.check_output([str(executable),'-V'],text=True).strip(),
        'warnings':sorted(set(re.findall(r'^Warning: (.*)$',(directory/'synthesis.log').read_text(),re.M))),
        'official_corpus_tested':False,'timing_verified':False,'physical_hardware_tested':False,
        'elapsed_seconds':time.monotonic()-started}
    text = json.dumps(result,indent=2)+'\n';manifest.write_text(text);report.write_text(text)
    print(json.dumps({k:result[k] for k in ['status','parameters','logic_lut_primitives','flip_flops','ram36_equivalent','cell_counts']},indent=2))


if __name__=='__main__':main()
