#!/usr/bin/env python3
"""Compile the exact complete 7-series mapped netlist for functional simulation."""
import argparse
import collections
import json
import os
from pathlib import Path
import re
import subprocess

from build_gate_sim import compilation
from check_xc7_dsp import audit as audit_dsp
from prepare_standalone import ROOT, digest, load_profile
from program_upload import profile_tag
from xc7_memory_mapping import audit_address_pins
from xc7_dsp_model import split_carries


def check_inputs(inputs):
    for name,value in inputs.items():
        path=Path(name)
        if path.is_absolute() or '..' in path.parts or digest(ROOT/path)!=value:
            raise ValueError('mapped simulation input changed: '+name)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=2)
    parser.add_argument('--estimate',type=Path,default=ROOT/'reports/xc7-system-estimate.json')
    parser.add_argument('--netlist',type=Path,default=ROOT/'build/xc7-system/mapped.json')
    parser.add_argument('--directory',type=Path,default=ROOT/'build/xc7-gate-sim')
    args=parser.parse_args()
    if args.jobs<1:parser.error('--jobs must be positive')
    estimate=args.estimate.resolve()
    directory=args.directory.resolve()
    if ROOT/'build' not in directory.parents:parser.error('--directory must be inside the repository build directory')
    reference=json.loads(estimate.read_text());profile=load_profile();top='wasmetal_loadable'
    if reference['status']!='synthesized_and_structurally_checked' or reference['top']!=top or reference['profile']!=profile:
        raise ValueError('need the checked complete-system estimate for the current profile')
    check_inputs(reference['inputs'])
    component_reports=[ROOT/'reports/xc7-ram-models.json',ROOT/'reports/xc7-dsp.json']
    component_receipts=[]
    for path in component_reports:
        receipt=json.loads(path.read_text())
        if receipt['status']!='passed':raise ValueError('primitive model checks did not pass')
        check_inputs(receipt['inputs']);component_receipts.append(receipt)
    if component_receipts[0]['negative_controls_rejected']!=14 or component_receipts[1]['negative_controls_rejected']!=6 or \
            component_receipts[1]['inventory_controls_rejected']!=8:
        raise ValueError('primitive verification controls are incomplete')
    netlist=args.netlist.resolve()
    if digest(netlist)!=reference['netlist_sha256']:raise ValueError('mapped circuit changed')
    design=json.loads(netlist.read_text());module=design['modules'][top]
    if audit_address_pins(module)!=reference['ram_address_pin_audit']:
        raise ValueError('RAM address audit differs')
    audit_dsp(module)
    kinds=collections.Counter(c['type'] for c in module['cells'].values())
    supported={'CARRY4','DSP48E1','FDCE','FDRE','FDRE_1','FDSE','INV','MUXF7','MUXF8',
               'RAM64M','RAMB18E1','RAMB36E1',*['LUT'+str(n) for n in range(1,7)]}
    if set(kinds)-supported:raise ValueError('unreviewed primitive: '+str(set(kinds)-supported))
    reset=module['netnames']['execution.core.reset']['bits']
    asynchronous=[c for c in module['cells'].values() if c['type']=='FDCE']
    if len(asynchronous)!=6 or any(c['connections']['CLR']!=reset or
            'HardFloat' not in c['attributes'].get('src','') and 'divSqrtRecFN_small.v' not in c['attributes'].get('src','')
            for c in asynchronous):
        raise ValueError('asynchronous reset consumers changed; review the shared reset domain')
    library=ROOT/'.cache/tools/usr/share/yosys/xilinx/cells_sim.v'
    ram=ROOT/'tests/xc7/ram_primitives.sv'
    harness=ROOT/'tests/standalone/loadable.cpp'
    directory.mkdir(parents=True,exist_ok=True)
    obj=directory/'obj';binary=obj/('V'+top);output=Path(str(binary)+'.build.json');output.unlink(missing_ok=True)
    dependencies=[netlist,estimate,*component_reports,library,ram,harness,Path(__file__).resolve(),
        ROOT/'tools/build_gate_sim.py',ROOT/'tools/check_xc7_dsp.py',ROOT/'tools/xc7_memory_mapping.py',
        ROOT/'tools/xc7_dsp_model.py',
        ROOT/'tools/prepare_standalone.py',ROOT/'tools/program_upload.py',
        ROOT/'.cache/tools/usr/bin/yosys',ROOT/'.cache/tools/usr/bin/verilator',ROOT/'.cache/tools/usr/bin/verilator_bin']
    inputs={**reference['inputs'],**{str(p.relative_to(ROOT)):digest(p) for p in dependencies}}
    for receipt in component_receipts:inputs.update(receipt['inputs'])
    check_inputs(inputs)
    text=library.read_text();models=[]
    for kind in sorted(set(kinds)-{'RAMB18E1','RAMB36E1'}):
        matches=re.findall(r'\bmodule\s+'+re.escape(kind)+r'\b.*?\bendmodule',text,re.S)
        if len(matches)!=1:raise ValueError('ambiguous primitive model: '+kind)
        model=split_carries(matches[0]) if kind=='DSP48E1' else matches[0]
        models.append(re.sub(r'\bspecify\b.*?\bendspecify\b','',model,flags=re.S))
    # Preserve the source library's notices with its extracted functional models.
    prefix=text[:re.search(r'^module\b',text,re.M).start()]
    cells=directory/'cells.v';cells.write_text(prefix+'\n'.join(models)+'\n')
    circuit=directory/'circuit.v';script=directory/'export.ys'
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
        f'lint_off -rule SYNCASYNCNET -file "{circuit}" -match "*wasmetal_loadable.execution.core.data_sizes.reset*"\n'+''.join(
        f'lint_off -rule {rule} -file "{path}"\n'
        for path,rules in [(circuit,['DECLFILENAME','PINCONNECTEMPTY','PINMISSING']),
            (cells,['DECLFILENAME','UNUSEDPARAM','GENUNNAMED','INITIALDLY','WIDTHEXPAND','WIDTHTRUNC','WIDTHCONCAT','COMBDLY']),
            (ram,['DECLFILENAME','UNUSEDPARAM','GENUNNAMED','WIDTHEXPAND','WIDTHTRUNC','WIDTHCONCAT'])]
        for rule in rules))
    params=reference['parameters'];options=compilation(True,True)
    flags=options['cflags']+f" -DBIT_TICKS={params['UART_TICKS']} -DCLOCK_SCALE=1 -DUPLOAD_TIMEOUT={params['UPLOAD_TIMEOUT_CYCLES']}"
    command=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL','--assert',
        '--top-module',top,'--cc','--exe','--output-split','10000','--output-split-cfuncs','10000',
        '--Mdir',str(obj),'-CFLAGS',flags,str(config),str(cells),str(ram),str(circuit),str(harness)]
    make=['make','-C',str(obj),'-f','V'+top+'.mk','-j',str(args.jobs),
        'CXX='+options['compiler'],'LINK='+options['compiler'],'VM_USER_CFLAGS='+flags,
        'OPT_FAST=-O3','OPT_SLOW=-O3','OPT_GLOBAL=-O3']
    env=dict(os.environ,VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator'))
    with (directory/'build.log').open('w') as log:
        subprocess.run(command,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
        for path in obj.glob('V*.cpp'):
            body=path.read_text()
            dsp_warning=('#pragma GCC diagnostic ignored \"-Wunused-but-set-variable\"\n'
                if '_DSP48E1' in path.name else '')
            path.write_text(dsp_warning+'#pragma GCC diagnostic ignored "-Wint-in-bool-context"\n'
                '#pragma GCC diagnostic ignored "-Wbool-operation"\n'
                '#pragma GCC diagnostic ignored "-Wbitwise-instead-of-logical"\n'+body)
        subprocess.run(make,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
    check_inputs(inputs)
    if digest(Path(options['compiler']))!=options['compiler_sha256']:raise ValueError('compiler changed')
    inputs.update({str(p.relative_to(ROOT)):digest(p) for p in [cells,circuit,config,script]})
    output.write_text(json.dumps({'backend':'loadable-mapped-xc7-functional','top':top,'inputs':inputs,
        'profile':profile,'profile_tag':profile_tag(profile).hex(),'parameters':params,
        'uart_ticks':params['UART_TICKS'],'clock_scale':1,'upload_timeout':params['UPLOAD_TIMEOUT_CYCLES'],
        'binary_sha256':digest(binary),'netlist_sha256':digest(netlist),'cell_counts':dict(kinds),
        'compilation':options,'commands':[command,make],'build_log_sha256':digest(directory/'build.log'),
        'scope':'Untimed complete core-clock netlist; board clock/reset, timing and physical behavior excluded',
        'whole_system_tests_passed':False,'physical_hardware_tested':False},indent=2)+'\n')
    print(binary)


if __name__=='__main__':main()
