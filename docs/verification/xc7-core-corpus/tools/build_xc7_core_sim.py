#!/usr/bin/env python3
"""Build the Xilinx-mapped execution core with the unchanged official-suite host."""
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import re
import subprocess

import build_identity
from build_gate_sim import compilation, compile_model, write_adapter
from check_xc7_dsp import CORE_GROUPS, audit as audit_dsp
from check_xc7_flops import audit as audit_flops
from check_xc7_lutram import audit as audit_lutram
from prepare_standalone import ROOT,digest
from xc7_dsp_model import split_carries
from xc7_lut_model import fast_lut
from xc7_memory_mapping import audit_address_pins


def verify_inputs(inputs):
    for name,value in inputs.items():
        path=Path(name)
        if path.is_absolute() or '..' in path.parts or digest(ROOT/path)!=value:
            raise ValueError('mapped core input changed: '+name)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--netlist',type=Path,default=ROOT/'build/xc7-core/mapped.json')
    parser.add_argument('--directory',type=Path,default=ROOT/'build/xc7-core-sim')
    parser.add_argument('--jobs',type=int,default=2)
    args=parser.parse_args();netlist=args.netlist.resolve();directory=args.directory.resolve()
    if args.jobs<1 or ROOT/'build' not in directory.parents or directory in netlist.parents:
        parser.error('use positive jobs and a separate simulator directory inside build/')
    manifest_path=netlist.with_suffix('.manifest.json')
    reference=json.loads(manifest_path.read_text());profile=json.loads((ROOT/'fpga/profile.json').read_text())
    if reference['status']!='synthesized_and_structurally_checked' or reference['family']!='xc7' or \
            reference['top']!='wasmetal_core' or reference['parameters']!=profile:
        raise ValueError('verified Xilinx mapping at the official-suite capacities required')
    verify_inputs(reference['inputs'])
    if digest(netlist)!=reference['netlist_sha256']:raise ValueError('synthesized circuit changed')
    module=json.loads(netlist.read_text())['modules']['wasmetal_core']
    if {n:int(v,2) for n,v in module['parameter_default_values'].items()}!=profile:
        raise ValueError('mapped parameter mismatch')
    if audit_address_pins(module)!=reference['ram_address_pin_audit']:raise ValueError('RAM wiring audit differs')
    kinds=Counter(c['type'] for c in module['cells'].values())
    dsp=audit_dsp(module,CORE_GROUPS);flops=audit_flops(module)
    lutram=audit_lutram(module) if kinds['RAM64M'] else 0
    supported={'CARRY4','DSP48E1','FDCE','FDRE','FDRE_1','FDSE','INV','MUXF7','MUXF8',
               'RAM64M','RAMB18E1','RAMB36E1',*['LUT'+str(n) for n in range(1,7)]}
    if set(kinds)-supported:raise ValueError('unreviewed core primitive: '+str(set(kinds)-supported))
    if dict(sorted(kinds.items()))!=reference['cell_counts']:raise ValueError('mapped primitive inventory differs')
    reset=module['ports']['reset']['bits'];asynchronous=[c for c in module['cells'].values() if c['type']=='FDCE']
    if len(asynchronous)!=6 or any(c['connections']['CLR']!=reset or
            'divSqrtRecFN_small.v' not in c['attributes'].get('src','') for c in asynchronous):
        raise ValueError('review the shared reset and asynchronous HardFloat consumers')
    reports={name:ROOT/'reports'/('xc7-'+name+'.json') for name in ('ram-models','dsp','carry','muxes','flops')}
    if lutram:reports['lutram']=ROOT/'reports/xc7-lutram.json'
    reports['luts']=ROOT/'reports/xc7-core-luts.json'
    receipts={}
    for name,path in reports.items():
        receipt=json.loads(path.read_text())
        if receipt['status']!='passed':raise ValueError('component verification did not pass: '+name)
        verify_inputs(receipt['inputs']);receipts[name]=receipt
    for name,count in [('ram-models',14),('dsp',6),('carry',11),('muxes',11),('flops',12),('lutram',16),('luts',11)]:
        if name not in receipts:continue
        if receipts[name]['negative_controls_rejected']!=count:raise ValueError('incomplete fault controls: '+name)
    if receipts['dsp']['inventory_controls_rejected']!=8:raise ValueError('incomplete DSP inventory controls')
    proof=receipts['luts']
    if not proof['binary_equivalence_proven'] or \
            {(c['width'],c['mode']) for c in proof['checks']}!={(w,m) for w in range(1,7) for m in ('known','four-state')} or \
            any(not c['icarus_passed'] or c['mode']=='known' and not c['verilator_passed'] for c in proof['checks']):
        raise ValueError('complete LUT proofs and independent oracles required')
    for name in ['luts','flops']+(['lutram'] if lutram else []):
        if reference['netlist_sha256'] not in {n['sha256'] for n in receipts[name]['netlists']}:
            raise ValueError('component audit omitted this exact core: '+name)
    directory.mkdir(parents=True,exist_ok=True);top='wasmetal_core';obj=directory/'obj';binary=obj/('V'+top)
    Path(str(binary)+'.build.json').unlink(missing_ok=True)
    library=ROOT/'.cache/tools/usr/share/yosys/xilinx/cells_sim.v';ram=ROOT/'tests/xc7/ram_primitives.sv'
    dependencies=[manifest_path,netlist,*reports.values(),library,ram,Path(__file__).resolve(),
        ROOT/'tools/build_gate_sim.py',ROOT/'tools/check_xc7_dsp.py',ROOT/'tools/check_xc7_flops.py',
        ROOT/'tools/check_xc7_lutram.py',ROOT/'tools/xc7_lut_model.py',ROOT/'tools/xc7_dsp_model.py',
        ROOT/'tools/xc7_memory_mapping.py',ROOT/'tools/prepare_standalone.py',
        ROOT/'.cache/tools/usr/bin/yosys',ROOT/'.cache/tools/usr/bin/verilator',ROOT/'.cache/tools/usr/bin/verilator_bin']
    extra={**reference['inputs'],**{str(p.relative_to(ROOT)):digest(p) for p in dependencies}}
    for receipt in receipts.values():extra.update(receipt['inputs'])
    verify_inputs(extra)
    source=library.read_text();models=[]
    for kind in sorted(set(kinds)-{'RAMB18E1','RAMB36E1'}):
        matches=re.findall(r'\bmodule\s+'+re.escape(kind)+r'\b.*?\bendmodule',source,re.S)
        if len(matches)!=1:raise ValueError('ambiguous library model: '+kind)
        model=matches[0]
        if kind=='DSP48E1':model=split_carries(model)
        if kind.startswith('LUT'):model=fast_lut(model,kind)
        models.append(re.sub(r'\bspecify\b.*?\bendspecify\b','',model,flags=re.S))
    cells=directory/'cells.v';cells.write_text(source[:re.search(r'^module\b',source,re.M).start()]+'\n'.join(models)+'\n')
    circuit=directory/'core.v';script=directory/'export.ys'
    script.write_text(f'read_json {netlist}\nread_verilog -lib -overwrite {library}\n'+
        f'hierarchy -check -top {top}\nsplitnets\nclean -purge\ncheck -assert\nwrite_verilog -noattr {circuit}\n')
    with (directory/'export.log').open('w') as log:
        subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-Q','-T','-s',str(script)],
            cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
    config=directory/'vendor.vlt'
    config.write_text('`verilator_config\n'+
        'split_var -module "CARRY4" -var "CO"\n'+
        'split_var -module "DSP48E1" -var "int_carry_in"\n'+
        'split_var -module "DSP48E1" -var "int_carry_out"\n'+
        f'lint_off -rule SYNCASYNCNET -file "{circuit}" -match "*\'reset\'*"\n'+''.join(
        f'lint_off -rule {rule} -file "{path}"\n' for path,rules in
        [(circuit,['DECLFILENAME','PINCONNECTEMPTY','PINMISSING']),
         (cells,['DECLFILENAME','UNUSEDPARAM','GENUNNAMED','INITIALDLY','WIDTHEXPAND','WIDTHTRUNC','WIDTHCONCAT','COMBDLY']),
         (ram,['DECLFILENAME','UNUSEDPARAM','GENUNNAMED','WIDTHEXPAND','WIDTHTRUNC','WIDTHCONCAT'])] for rule in rules))
    write_adapter(directory,profile);options=compilation(True,True)
    build_identity.begin(binary,'native')
    snapshot_path=Path(str(binary)+'.inputs.json');snapshot=json.loads(snapshot_path.read_text())
    command=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL','--assert',
        '--top-module',top,'--cc','--exe','--output-split','10000','--output-split-cfuncs','10000',
        '--Mdir',str(obj),'-CFLAGS',options['cflags'],str(config),str(cells),str(ram),str(circuit),str(directory/'main.cpp')]
    env=dict(os.environ,VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator'))
    with (directory/'verilation.log').open('w') as log:
        subprocess.run(command,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
    for path in obj.glob('V*.cpp'):
        warnings=['Wint-in-bool-context','Wbool-operation','Wbitwise-instead-of-logical']
        if '_DSP48E1' in path.name:warnings.append('Wunused-but-set-variable')
        path.write_text(''.join(f'#pragma GCC diagnostic ignored "-{w}"\n' for w in warnings)+path.read_text())
    generated=[cells,circuit,config,script,directory/'main.cpp',directory/'gate_config.hpp',*obj.glob('V*.cpp'),*obj.glob('V*.h')]
    extra.update({str(p.relative_to(ROOT)):digest(p) for p in generated})
    snapshot.update(backend='mapped-xc7-functional',parameters=profile,extra_inputs=extra,
        compilation=options,model_options={'fast_luts':True},netlist_sha256=reference['netlist_sha256'],
        synthesis_manifest_sha256=digest(manifest_path),verilator_command=command,
        component_reports={name:digest(path) for name,path in reports.items()},
        inventory={'dsp':[{'configuration':list(k),'instances':v} for k,v in sorted(dsp.items())],
                   'flops':flops,'distributed_ram_instances':lutram},
        scope='Untimed host-backed execution core; no board, local-memory capacity or physical timing claim')
    snapshot_path.write_text(json.dumps(snapshot,indent=2)+'\n')
    compile_model(directory,options,args.jobs,False)
    build_identity.finish(binary)
    print('Built identified Xilinx execution-core simulator',binary)


if __name__=='__main__':main()
