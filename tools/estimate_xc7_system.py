#!/usr/bin/env python3
"""Measure the complete programmable SoC on 7-series primitives, without physical-fit claims."""
import collections
import datetime
import json
from pathlib import Path
import re
import subprocess
import time

from build_board import yosys
from prepare_standalone import ROOT,digest,load_profile
from program_upload import profile_tag
from standalone_support import parameters


def main():
    started=time.monotonic();profile=load_profile();top='wasmetal_loadable'
    directory=ROOT/'build/xc7-system';directory.mkdir(parents=True,exist_ok=True)
    report=ROOT/'reports/xc7-system-estimate.json';report.parent.mkdir(exist_ok=True)
    report.unlink(missing_ok=True)
    vendor=ROOT/'third_party/hardfloat/source'
    rtl=[*sorted((ROOT/'rtl').glob('*.sv')),*sorted(vendor.glob('*.v')),
        vendor/'RISCV/HardFloat_specialize.v',ROOT/'fpga/wasmetal_uart.sv',
        ROOT/'soc/wasmetal_standalone.sv',ROOT/'soc/wasmetal_local_memory.sv',
        *sorted((ROOT/'soc/memory').glob('*.sv')),
        ROOT/'soc/loader/wasmetal_image_loader.sv',ROOT/'soc/loader/wasmetal_loadable.sv']
    library=ROOT/'.cache/tools/usr/share/yosys'
    inputs=[*rtl,*sorted(vendor.rglob('*.vi')),Path(__file__).resolve(),
        ROOT/'tools/build_board.py',ROOT/'tools/prepare_standalone.py',ROOT/'tools/standalone_support.py',
        ROOT/'tools/program_upload.py',ROOT/'soc/profile.json',ROOT/'tools/upstream.lock.json',
        *[p for p in sorted((library/'xilinx').rglob('*')) if p.is_file()],
        *[p for p in sorted(library.glob('*.v')) if p.is_file()]]
    hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs}
    params={**parameters(profile),'UART_TICKS':81,'UPLOAD_TIMEOUT_CYCLES':2000000,
        'PROFILE_TAG':f"128'h{int.from_bytes(profile_tag(profile),'little'):032x}"}
    base=f'synth_xilinx -family xc7 -top {top} -noiopad -noclkbuf'
    # Match the earlier core-only estimator's resource-sharing sequence.
    # The ending -run label is exclusive; the explicit final check is required.
    script='read_verilog -sv -defer -Ithird_party/hardfloat/source -Ithird_party/hardfloat/source/RISCV '+\
        ' '.join(str(p.relative_to(ROOT)) for p in rtl)+'\nchparam '+\
        ' '.join(f'-set {k} {v}' for k,v in params.items())+f' {top}\n'+f'''
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
{base} -run map_memory:check
check -assert
write_json {directory}/mapped.json
'''
    yosys(script,'synthesis',directory)
    generic=json.loads((directory/'generic.json').read_text())['modules'][top]
    memories=[(name,c) for name,c in generic['cells'].items() if c['type']=='$mem_v2']
    bits=lambda c:int(c['parameters']['WIDTH'],2)*int(c['parameters']['SIZE'],2)
    for prefix,expected in [('execution.memory.ram_backend.',profile['ram_bytes']*8),
            ('execution.core.value_file.',profile['core']['VALUE_DEPTH']*128)]:
        if sum(bits(c) for name,c in memories if name.startswith(prefix))!=expected:
            raise ValueError('storage capacity changed before technology mapping: '+prefix)
    design=json.loads((directory/'mapped.json').read_text())['modules'][top]
    counts=collections.Counter(c['type'] for c in design['cells'].values())
    allowed={'CARRY4','DSP48E1','INV','MUXF7','MUXF8','RAMB18E1','RAMB36E1',
        'RAM32M','RAM64M','RAM32X1S','RAM64X1S','RAM128X1S','RAM256X1S',
        'RAM32X1D','RAM64X1D','RAM128X1D','SRL16E','SRLC32E',
        *['LUT'+str(n) for n in range(1,7)],
        *[name+suffix for name in ('FDCE','FDPE','FDRE','FDSE') for suffix in ('','_1')]}
    if set(counts)-allowed:raise ValueError('unexpected mapped primitives: '+str(set(counts)-allowed))
    expected_ports={'clk':'input','reset':'input','rx':'input','tx':'output',
        'finished':'output','error':'output','image_valid':'output'}
    if {n:p['direction'] for n,p in design['ports'].items()}!=expected_ports or \
            any(len(p['bits'])!=1 for p in design['ports'].values()):
        raise ValueError('programmable system interface was changed')
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise ValueError('estimate inputs changed')
    log=(directory/'synthesis.log').read_text()
    executable=ROOT/'.cache/tools/usr/bin/yosys'
    result={'status':'synthesized_and_structurally_checked','captured_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope':'complete programmable core-clock SoC; excludes board pads, clock/reset generation and external-memory controller',
        'top':top,'family':'xc7','profile':profile,'parameters':params,
        'inputs':hashes,'tool':{'version':subprocess.check_output([str(executable),'-V'],text=True).strip(),
            'yosys_sha256':digest(executable),'abc_sha256':digest(executable.with_name('yosys-abc'))},
        'script_sha256':digest(directory/'synthesis.ys'),'log_sha256':digest(directory/'synthesis.log'),
        'generic_netlist_sha256':digest(directory/'generic.json'),'netlist_sha256':digest(directory/'mapped.json'),
        'generic_memory_count':len(memories),'generic_memory_bits':sum(bits(c) for name,c in memories),
        'cell_counts':dict(sorted(counts.items())),
        'logic_lut_primitives':sum(counts['LUT'+str(n)] for n in range(1,7)),
        'flip_flops':sum(n for kind,n in counts.items() if kind.startswith('FD')),
        'ram36_equivalent':counts['RAMB36E1']+counts['RAMB18E1']/2,
        'distributed_ram_primitives':{k:v for k,v in sorted(counts.items()) if k.startswith('RAM') and not k.startswith('RAMB')},
        'warnings':sorted(set(re.findall(r'^Warning: (.*)$',log,re.M))),
        'functional_mapping_verified':False,'physical_placement_performed':False,'timing_verified':False,
        'bitstream_generated':False,'physical_hardware_tested':False,
        'limitations':['Logic LUT totals exclude distributed-RAM and shift-register use of LUT sites.',
            'Primitive counts are not packed utilization, a Vivado report, a clock-speed estimate or proof of physical fit.',
            'Only the bounded standalone profile is represented; no DDR controller, cache, host runtime or reclaiming GC is included.'],
        'elapsed_seconds':time.monotonic()-started}
    report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','logic_lut_primitives','flip_flops','ram36_equivalent','distributed_ram_primitives','cell_counts']},indent=2))


if __name__=='__main__':main()
