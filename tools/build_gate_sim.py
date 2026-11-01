#!/usr/bin/env python3
"""Simulate the mapped FPGA CPU with Yosys cell models and a checked DSP model."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

import build_identity
import ecp5_ram

ROOT=Path(__file__).resolve().parent.parent


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def fast_lut_model(model,name):
    """Use a direct lookup for known selectors; retain exact X/Z behavior."""
    pins={'LUT2':'{B,A}','LUT4':'{D,C,B,A}'}[name]
    model,count=re.subn(r'assign Z\s*=\s*A \?\s*s1\[1\]\s*:\s*s1\[0\];',
        f'assign Z = $isunknown({pins}) ? (A ? s1[1] : s1[0]) : INIT[{pins}];',model)
    if count!=1: raise ValueError('unrecognized pinned LUT model: '+name)
    return model


def compilation(fast):
    compiler=shutil.which('clang++' if fast else 'g++')
    if compiler is None: raise ValueError('install clang++ to use --fast-sim' if fast else 'g++ is missing')
    flags='-std=c++17 -O2 -Wall -Wextra -Werror'
    if fast:
        # These two style-warning exceptions are needed by the pinned
        # Verilator-generated code/runtime when compiled with Clang.
        flags='-std=c++17 -O3 -march=native -Wall -Wextra -Werror -Wno-unknown-warning-option -Wno-unused-parameter'
    return {'fast_sim':fast,'compiler':compiler,'compiler_sha256':digest(Path(compiler)),
            'compiler_version':subprocess.check_output([compiler,'--version'],text=True).splitlines()[0],
            'cflags':flags}


def compile_model(directory,options,jobs,force):
    command=['make','-C',str(directory/'obj'),'-f','Vwasmetal_core.mk','-j',str(jobs),
             'CXX='+options['compiler'],'LINK='+options['compiler'],'VM_USER_CFLAGS='+options['cflags']]
    if force: command.append('-B')  # A changed compiler/flags must not reuse old objects.
    if options['fast_sim']: command+=['OPT_FAST=-O3','OPT_SLOW=-O3','OPT_GLOBAL=-O3']
    subprocess.run(command,check=True,cwd=ROOT,
                   env=dict(os.environ,VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')))
    if digest(Path(options['compiler']))!=options['compiler_sha256']:
        raise ValueError('C++ compiler changed during compilation')


def write_adapter(directory,parameters):
    main_cpp=(ROOT/'sim/main.cpp').read_text()
    assert main_cpp.count('#include "core_config.hpp"')==1
    config=(ROOT/'sim/core_config.hpp').read_text()
    for name,value in parameters.items():
        config,n=re.subn(r'(unsigned '+name+r'=)\d+;',lambda m:m[1]+str(value)+';',config)
        assert n==1,name
    for name,text in [('main.cpp',main_cpp.replace('#include "core_config.hpp"','#include "gate_config.hpp"')),('gate_config.hpp',config)]:
        path=directory/name
        if not path.exists() or path.read_text()!=text: path.write_text(text)


def relink(directory,netlist,parameters,options,jobs,model_options):
    binary=directory/'obj/Vwasmetal_core'
    previous=json.loads(Path(str(binary)+'.build.json').read_text())
    if previous.get('model_options',{'fast_luts':False})!=model_options:
        raise ValueError('changing primitive models requires a full rebuild without --relink-only')
    previous_compilation=previous.get('compilation')
    if previous_compilation is not None and previous_compilation!=options:
        raise ValueError('changing compiler identity or flags requires a full rebuild without --relink-only')
    if digest(binary)!=previous['binary_sha256']: raise ValueError('existing mapped executable changed')
    for name,sha in previous['inputs'].items():
        if name.startswith(('rtl/','third_party/hardfloat/')) and digest(ROOT/name)!=sha:
            raise ValueError('cannot reuse a model after an RTL change: '+name)
    extra=previous['extra_inputs'].copy()
    tool_name=str(Path(__file__).resolve().relative_to(ROOT))
    generation_sha=previous.get('model_generation_script_sha256',extra[tool_name])
    for name,sha in extra.items():
        if name!=tool_name and digest(ROOT/name)!=sha: raise ValueError('mapped model input changed: '+name)
    if extra.get(str(netlist.relative_to(ROOT)))!=digest(netlist): raise ValueError('cannot relink a different netlist')
    write_adapter(directory,parameters)
    build_identity.begin(binary,'native')
    path=Path(str(binary)+'.inputs.json');snapshot=json.loads(path.read_text())
    for p in [Path(__file__).resolve(),directory/'main.cpp',directory/'gate_config.hpp']+list(binary.parent.glob('V*.h')):
        extra[str(p.relative_to(ROOT))]=digest(p)
    snapshot.update(backend='mapped-ecp5-functional',parameters=parameters,extra_inputs=extra,
                    model_generation_script_sha256=generation_sha,compilation=options,model_options=model_options)
    path.write_text(json.dumps(snapshot,indent=2)+'\n')
    # Old manifests did not record the compiler. Recompile their C++ once so
    # the new compiler record describes the whole executable, not only its host.
    compile_model(directory,options,jobs,previous_compilation is None)
    build_identity.finish(binary)
    print('Relinked unchanged mapped CPU model',binary)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--core-netlist',type=Path,default=ROOT/'build/core-ecp5.json')
    parser.add_argument('--relink-only',action='store_true',help='reuse a verified unchanged mapped model after host/configuration changes')
    parser.add_argument('--build-directory',type=Path,default=ROOT/'build/gate-model')
    parser.add_argument('--jobs',type=int,default=2,help='parallel C++ compilation jobs')
    parser.add_argument('--fast-sim',action='store_true',help='compile with Clang -O3 and the current host CPU instruction set')
    parser.add_argument('--fast-luts',action='store_true',help='use equivalence-checked lookup models without changing the mapped circuit')
    args=parser.parse_args()
    if args.jobs<1: parser.error('jobs must be positive')
    directory=args.build_directory.resolve()
    if ROOT/'build' not in directory.parents: parser.error('build directory must be inside the repository build directory')
    options=compilation(args.fast_sim)
    model_options={'fast_luts':args.fast_luts}
    netlist=args.core_netlist.resolve()
    manifest_path=netlist.with_suffix('.manifest.json')
    manifest=json.loads(manifest_path.read_text())
    if digest(netlist)!=manifest['netlist_sha256']: raise ValueError('netlist digest mismatch')
    for name,sha in manifest['inputs'].items():
        if digest(ROOT/name)!=sha: raise ValueError(f'stale mapped core: {name}')
    source=json.loads(netlist.read_text())
    core=source['modules']['wasmetal_core']
    parameters={name:int(value,2) for name,value in core['parameter_default_values'].items()}
    directory.mkdir(parents=True,exist_ok=True)
    if args.relink_only:
        relink(directory,netlist,parameters,options,args.jobs,model_options)
        return
    supported={'LUT4','PFUMX','L6MUX21','CCU2C','TRELLIS_DPR16X4','TRELLIS_FF','MULT18X18D','DP16KD'}
    def parameter_text(value):
        # JSON appends a space to distinguish digit-only strings from bit vectors.
        if value.endswith(' '): return value[:-1]
        if set(value)<={'0','1'}:
            return int(value,2).to_bytes((len(value)+7)//8,'big').lstrip(b'\0').decode('ascii')
        return value
    for name,cell in core['cells'].items():
        if cell['type'] not in supported: raise ValueError(f'unmodeled primitive {cell["type"]}')
        if cell['type'] in ('PFUMX','L6MUX21') and cell['parameters']:
            raise ValueError('unsupported wide-LUT multiplexer parameters')
        if cell['type']=='DP16KD': ecp5_ram.check(cell)
        if cell['type']=='TRELLIS_FF':
            cell_parameters=cell['parameters']
            if 'M' not in cell['connections']:
                if parameter_text(cell_parameters.get('LSRMODE','LSR'))=='PRLD': raise ValueError('missing preload pin')
                cell['connections']['M']=['0']
                cell['port_directions']['M']='input'
            if 'CE' not in cell['connections']:
                if parameter_text(cell_parameters.get('CEMUX','1 ')) not in ('0','1'): raise ValueError('missing active enable pin')
                cell['connections']['CE']=['0']
                cell['port_directions']['CE']='input'
        if cell['type']=='MULT18X18D':
            # Yosys' basic DSP mapper uses unregistered multipliers, without
            # cascade, bypass, clocking, or pipeline settings. Reject other modes.
            if cell['parameters']: raise ValueError(f'unsupported DSP configuration: {name}')
            connections=cell['connections']
            allowed={f'{p}{i}' for p in 'ABC' for i in range(18)}|{f'P{i}' for i in range(36)}|{'SIGNEDA','SIGNEDB','SOURCEA','SOURCEB'}
            if set(connections)!=allowed: raise ValueError('unsupported DSP ports')
            for port in ['SOURCEA','SOURCEB']+[f'C{i}' for i in range(18)]:
                if connections[port]!=['0']: raise ValueError(f'unsupported DSP source: {port}')
    # Tie only parameter-disabled pins. No live undriven signal is replaced.
    (directory/'normalized.json').write_text(json.dumps(source))
    yosys=ROOT/'.cache/tools/usr/bin/yosys'
    script=directory/'export.ys'
    # Scalarize internal nets, retaining the external bus interface. Otherwise
    # packed carry-chain aliases create artificial whole-vector dependency loops
    # in event simulators despite an acyclic bit-level circuit.
    script.write_text(f'read_json {directory}/normalized.json\nsplitnets\nclean -purge\ncheck -assert\nwrite_verilog -noattr {directory}/core.v\n')
    with (directory/'export.log').open('w') as stream:
        subprocess.run([str(yosys),'-Q','-T','-s',str(script)],stdout=stream,stderr=subprocess.STDOUT,check=True)
    library=ROOT/'.cache/tools/usr/share/yosys/ecp5/cells_sim.v'
    if args.fast_luts:
        subprocess.run([sys.executable,str(ROOT/'tools/check_ecp5_luts.py'),
                        '--core-netlist',str(netlist),'--directory',str(directory/'lut-proof')],check=True)
    models=[]
    for name in ['LUT2','LUT4','PFUMX','L6MUX21','CCU2C','TRELLIS_DPR16X4','TRELLIS_FF']:
        match=re.search(r'\bmodule\s+'+name+r'\b.*?\bendmodule',library.read_text(),re.S)
        if not match: raise ValueError(f'missing official model {name}')
        # This is functional netlist simulation; routed timing is checked by STA.
        model=re.sub(r'\bspecify\b.*?\bendspecify\b','',match[0],flags=re.S)
        if args.fast_luts and name in ('LUT2','LUT4'): model=fast_lut_model(model,name)
        models.append(model)
    ports=source['modules']['MULT18X18D']['ports']
    used=sorted({f'{p}{i}' for p in 'ABC' for i in range(18)}|{f'P{i}' for i in range(36)}|{'SIGNEDA','SIGNEDB','SOURCEA','SOURCEB'})
    models.append('module MULT18X18D('+','.join(ports[p]['direction']+' wire '+p for p in used)+');')
    concat=lambda prefix,n:'{'+','.join(f'{prefix}{i}' for i in reversed(range(n)))+'}'
    models += [f'wire signed [18:0] a={{SIGNEDA && A17,{concat("A",18)}}};',
               f'wire signed [18:0] b={{SIGNEDB && B17,{concat("B",18)}}};',
               'wire signed [37:0] product=a*b;',f'assign {concat("P",36)}=product[35:0];','endmodule']
    if any(cell['type']=='DP16KD' for cell in core['cells'].values()):
        models.append(ecp5_ram.model())
    (directory/'cells.v').write_text('\n'.join(models)+'\n')
    write_adapter(directory,parameters)
    # Scope generated-name and vendor-model warnings; structural warnings remain fatal.
    (directory/'vendor.vlt').write_text('`verilator_config\n'+''.join(
        f'lint_off -rule {rule} -file "{directory}/{name}"\n'
        for name,rules in [('core.v',['DECLFILENAME','PINCONNECTEMPTY']),('cells.v',['DECLFILENAME','INITIALDLY','GENUNNAMED','UNUSEDPARAM','WIDTHEXPAND','SYNCASYNCNET'])]
        for rule in rules))
    binary=directory/'obj/Vwasmetal_core'
    build_identity.begin(binary,'native')
    snapshot_path=Path(str(binary)+'.inputs.json')
    snapshot=json.loads(snapshot_path.read_text())
    extras=[netlist,manifest_path,library,yosys,Path(__file__).resolve(),ROOT/'tools/ecp5_ram.py']+list(directory.glob('*.v'))+list(directory.glob('*.vlt'))+[directory/'main.cpp',directory/'gate_config.hpp']
    if args.fast_luts:
        extras += [ROOT/'tools/check_ecp5_luts.py']+list((directory/'lut-proof').glob('*'))
    snapshot.update(backend='mapped-ecp5-functional',parameters=parameters,compilation=options,model_options=model_options,
                    extra_inputs={str(p.relative_to(ROOT)):digest(p) for p in extras})
    snapshot_path.write_text(json.dumps(snapshot,indent=2)+'\n')
    verilator_command=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL','--top-module','wasmetal_core',
          '--cc','--exe','--output-split','10000','--output-split-cfuncs','10000',
          '--Mdir',str(binary.parent),'-CFLAGS',options['cflags'],
          str(directory/'vendor.vlt'),str(directory/'cells.v'),str(directory/'core.v'),str(directory/'main.cpp')]
    subprocess.run(verilator_command,cwd=ROOT,env=dict(os.environ,VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),check=True)
    # Verilator 5.020 emits integer-valued LUT ternaries in Boolean contexts.
    # Suppress that C++ style warning only in its generated implementation;
    # the handwritten host adapter still compiles with all warnings as errors.
    generated=list(binary.parent.glob('Vwasmetal_core*.cpp'))
    for path in generated:
        path.write_text('#pragma GCC diagnostic ignored "-Wint-in-bool-context"\n'+path.read_text())
    snapshot['extra_inputs'].update({str(p.relative_to(ROOT)):digest(p) for p in generated+list(binary.parent.glob('V*.h'))})
    snapshot_path.write_text(json.dumps(snapshot,indent=2)+'\n')
    compile_model(directory,options,args.jobs,True)
    build_identity.finish(binary)
    print('Built mapped CPU simulator',binary)


if __name__=='__main__': main()
