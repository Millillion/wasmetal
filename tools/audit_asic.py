#!/usr/bin/env python3
"""Elaborate the standalone SoC without FPGA mapping and inventory ASIC boundaries.

This retains generic memories. It does not select cells, estimate silicon area,
prove a macro implementation, or perform physical/timing signoff.
"""
import argparse
import collections
import json
from pathlib import Path
import subprocess

from prepare_standalone import ROOT, digest, load_profile
from standalone_support import parameters, verify_image
from program_upload import profile_tag


def number(value):
    return value if isinstance(value,int) else int(value,2)


def memory_record(name,cell):
    p=cell['parameters'];pins=cell['connections']
    width=number(p['WIDTH']);words=number(p['SIZE'])
    record={'name':name,'width':width,'words':words,'bits':width*words,
            'source':cell.get('attributes',{}).get('src'),
            'known_initial_bits':sum(b in '01' for b in p['INIT']),
            'read_ports':[],'write_ports':[]}
    for prefix,output in [('RD','read_ports'),('WR','write_ports')]:
        count=number(p[prefix+'_PORTS'])
        enabled=number(p[prefix+'_CLK_ENABLE']);polarity=number(p[prefix+'_CLK_POLARITY'])
        for port in range(count):
            clocked=bool(enabled>>port&1)
            entry={'clocked':clocked,'clock_bit':pins[prefix+'_CLK'][port] if clocked else None,
                   'edge':('rising' if polarity>>port&1 else 'falling') if clocked else 'asynchronous'}
            if prefix=='WR':
                entry['enable_bits']=pins['WR_EN'][port*width:(port+1)*width]
                entry['per_bit_masking']=len(set(entry['enable_bits']))>1
                entry['permanently_disabled']=all(b=='0' for b in entry['enable_bits'])
                # Record a digest rather than thousands of repeated bit ids.
                entry['enable_signal_count']=len(set(entry.pop('enable_bits'))-{'0','1'})
            record[output].append(entry)
    for field in ('RD_TRANSPARENCY_MASK','RD_COLLISION_X_MASK','WR_PRIORITY_MASK'):
        record[field.lower()]=p.get(field,'')
    return record


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--loadable',action='store_true',help='audit writable program stores and serial boot, without a prepared ROM image')
    args=parser.parse_args()
    audit_name='asic-loadable-audit' if args.loadable else 'asic-audit'
    top_name='wasmetal_loadable' if args.loadable else 'wasmetal_standalone'
    prefix='execution.' if args.loadable else ''
    directory=ROOT/'build'/audit_name;directory.mkdir(parents=True,exist_ok=True)
    profile=load_profile();image=None if args.loadable else verify_image(ROOT/'build/standalone-image')
    vendor=ROOT/'third_party/hardfloat/source'
    sources=sorted(vendor.glob('*.v'))+[vendor/'RISCV/HardFloat_specialize.v']+sorted((ROOT/'rtl').glob('*.sv'))
    sources+=[ROOT/'fpga/wasmetal_uart.sv',ROOT/'soc/wasmetal_standalone.sv',ROOT/'soc/wasmetal_local_memory.sv']
    sources+=sorted((ROOT/'soc/memory').glob('*.sv'))
    if args.loadable:
        sources += [ROOT/'soc/loader/wasmetal_loadable.sv',ROOT/'soc/loader/wasmetal_image_loader.sv']
    inputs=sources+sorted(vendor.rglob('*.vi'))+[Path(__file__).resolve(),ROOT/'soc/profile.json',
        ROOT/'tools/upstream.lock.json',ROOT/'tools/prepare_standalone.py',ROOT/'tools/standalone_support.py',
        ROOT/'tools/program_upload.py']
    if not args.loadable:inputs+=sorted((ROOT/'build/standalone-image').glob('*'))
    hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs if p.is_file()}
    script=directory/'elaborate.ys';netlist=directory/'generic.json';logfile=directory/'elaborate.log'
    params=parameters(profile)
    if args.loadable:params['PROFILE_TAG']=f"128'h{int.from_bytes(profile_tag(profile),'little'):032x}"
    script.write_text('read_verilog -sv -defer -Ithird_party/hardfloat/source -Ithird_party/hardfloat/source/RISCV '+
        ' '.join(str(p.relative_to(ROOT)) for p in sources)+'\nchparam '+
        ' '.join(f'-set {key} {value}' for key,value in params.items())+f' {top_name}\nhierarchy -check -top {top_name}\n'+'''
proc
flatten
opt -nodffe -nosdff
memory_dff
memory_collect
opt_clean
check -assert
stat
'''+f'write_json {netlist}\n')
    yosys=ROOT/'.cache/tools/usr/bin/yosys'
    with logfile.open('w') as log:
        subprocess.run([str(yosys),'-Q','-T','-s',str(script)],cwd=ROOT,
                       stdout=log,stderr=subprocess.STDOUT,check=True,timeout=600)
    top=json.loads(netlist.read_text())['modules'][top_name]
    cells=top['cells'];counts=collections.Counter(c['type'] for c in cells.values())
    if any(not kind.startswith('$') for kind in counts): raise ValueError('technology-specific or unflattened cell remains')
    if any('latch' in kind for kind in counts): raise ValueError('inferred latch requires investigation')
    memories=[memory_record(name,c) for name,c in sorted(cells.items()) if c['type']=='$mem_v2']
    if not memories: raise ValueError('generic memories were lost')
    backing=[m for m in memories if m['name'].startswith(prefix+'memory.ram_backend.')]
    stack=[m for m in memories if m['name'].startswith(prefix+'core.value_file.')]
    if sum(m['bits'] for m in backing)!=profile['ram_bytes']*8:
        raise ValueError('backing storage capacity changed during elaboration')
    if sum(m['bits'] for m in stack)!=profile['core']['VALUE_DEPTH']*128:
        raise ValueError('value-stack storage capacity changed during elaboration')
    clock=top['ports']['clk']['bits'][0];clocks=collections.Counter();register_bits=0
    for name,cell in cells.items():
        if 'CLK' in cell['connections']:
            if cell['connections']['CLK']!=[clock]: raise ValueError('unexplained internal clock: '+name)
            edge='rising' if number(cell['parameters']['CLK_POLARITY']) else 'falling'
            clocks[edge]+=1
            register_bits+=number(cell['parameters'].get('WIDTH',0))
    for m in memories:
        for port in m['read_ports']+m['write_ports']:
            if port['clocked'] and port['clock_bit']!=clock: raise ValueError('unexplained memory clock')
    initialized_nets=[{'name':name,'bits':len(n['bits']),'initial_value':n['attributes']['init']}
                      for name,n in top['netnames'].items() if 'init' in n.get('attributes',{})]
    program_shapes={
        'instructions':(288,profile['instruction_depth']),
        'functions':(160,profile['function_depth']),
        'types':(profile['type_depth'],profile['type_depth']),
        'boot':(232,profile['boot_depth']),
        'memory.regions':(64,6*profile['regions_per_kind'])}
    program_memories=[m for m in memories if m['name'] in [prefix+name for name in program_shapes]]
    if len(program_memories)!=5:raise ValueError('missing program memory')
    for memory in program_memories:
        if (memory['width'],memory['words'])!=program_shapes[memory['name'].removeprefix(prefix)]:
            raise ValueError('program memory capacity changed during elaboration')
    if args.loadable:
        if any(m['known_initial_bits'] or not m['write_ports'] or
               all(p['permanently_disabled'] for p in m['write_ports']) for m in program_memories):
            raise ValueError('programmable boot must use uninitialized writable memories')
    if initialized_nets:raise ValueError('generic SoC must not require initialized registers')
    report={'status':'elaborated_and_audited','top':top_name,'profile':profile,
        'scope':'generic standalone SoC; excludes FPGA divider, reset synchronizer, pads and clock buffer',
        'inputs':hashes,'image':image,'script_sha256':digest(script),'netlist_sha256':digest(netlist),
        'yosys_sha256':digest(yosys),'cells':dict(sorted(counts.items())),
        'generic_memory_count':len(memories),'generic_memory_bits':sum(m['bits'] for m in memories),
        'backing_memory_bits':sum(m['bits'] for m in backing),'value_stack_bits':sum(m['bits'] for m in stack),
        'register_cell_bits':register_bits,'clocked_cells_by_edge':dict(clocks),
        'initialized_register_nets':initialized_nets,'memories':memories,
        'program_storage':[m['name'] for m in program_memories],
        'program_storage_bits':sum(m['bits'] for m in program_memories),
        'prepared_program_embedded':not args.loadable,
        'requires_macro_review':[m['name'] for m in memories if len(m['write_ports'])>1 or
                                len(m['read_ports'])>1 or m['known_initial_bits'] or
                                any(not p['clocked'] for p in m['read_ports'])],
        'process_selected':False,'sram_macros_mapped':False,'standard_cells_mapped':False,
        'silicon_area_estimated':False,'timing_closed':False,'physical_hardware_tested':False}
    if any(digest(ROOT/name)!=value for name,value in hashes.items()): raise ValueError('ASIC audit inputs changed')
    (ROOT/'reports'/(audit_name+'.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:report[key] for key in ('status','generic_memory_count','generic_memory_bits',
          'backing_memory_bits','value_stack_bits','register_cell_bits','clocked_cells_by_edge')},indent=2))


if __name__=='__main__':main()
