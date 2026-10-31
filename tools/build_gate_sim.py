#!/usr/bin/env python3
"""Simulate the mapped FPGA CPU with Yosys cell models and a checked DSP model."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

import build_identity

ROOT=Path(__file__).resolve().parent.parent


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()


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


def relink(directory,netlist,parameters):
    binary=directory/'obj/Vwasmetal_core'
    previous=json.loads(Path(str(binary)+'.build.json').read_text())
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
                    model_generation_script_sha256=generation_sha)
    path.write_text(json.dumps(snapshot,indent=2)+'\n')
    subprocess.run(['make','-C',str(binary.parent),'-f','Vwasmetal_core.mk','-j','2'],check=True,cwd=ROOT,
                   env=dict(os.environ,VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')))
    build_identity.finish(binary)
    print('Relinked unchanged mapped CPU model',binary)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--core-netlist',type=Path,default=ROOT/'build/core-ecp5.json')
    parser.add_argument('--relink-only',action='store_true',help='reuse a verified unchanged mapped model after host/configuration changes')
    args=parser.parse_args()
    netlist=args.core_netlist.resolve()
    manifest_path=netlist.with_suffix('.manifest.json')
    manifest=json.loads(manifest_path.read_text())
    if digest(netlist)!=manifest['netlist_sha256']: raise ValueError('netlist digest mismatch')
    for name,sha in manifest['inputs'].items():
        if digest(ROOT/name)!=sha: raise ValueError(f'stale mapped core: {name}')
    source=json.loads(netlist.read_text())
    core=source['modules']['wasmetal_core']
    parameters={name:int(value,2) for name,value in core['parameter_default_values'].items()}
    directory=ROOT/'build/gate-model';directory.mkdir(parents=True,exist_ok=True)
    if args.relink_only:
        relink(directory,netlist,parameters)
        return
    supported={'LUT4','CCU2C','TRELLIS_DPR16X4','TRELLIS_FF','MULT18X18D'}
    def parameter_text(value):
        # JSON appends a space to distinguish digit-only strings from bit vectors.
        if value.endswith(' '): return value[:-1]
        if set(value)<={'0','1'}:
            return int(value,2).to_bytes((len(value)+7)//8,'big').lstrip(b'\0').decode('ascii')
        return value
    for name,cell in core['cells'].items():
        if cell['type'] not in supported: raise ValueError(f'unmodeled primitive {cell["type"]}')
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
    models=[]
    for name in ['LUT2','LUT4','CCU2C','TRELLIS_DPR16X4','TRELLIS_FF']:
        match=re.search(r'\bmodule\s+'+name+r'\b.*?\bendmodule',library.read_text(),re.S)
        if not match: raise ValueError(f'missing official model {name}')
        # This is functional netlist simulation; routed timing is checked by STA.
        models.append(re.sub(r'\bspecify\b.*?\bendspecify\b','',match[0],flags=re.S))
    ports=source['modules']['MULT18X18D']['ports']
    used=sorted({f'{p}{i}' for p in 'ABC' for i in range(18)}|{f'P{i}' for i in range(36)}|{'SIGNEDA','SIGNEDB','SOURCEA','SOURCEB'})
    models.append('module MULT18X18D('+','.join(ports[p]['direction']+' wire '+p for p in used)+');')
    concat=lambda prefix,n:'{'+','.join(f'{prefix}{i}' for i in reversed(range(n)))+'}'
    models += [f'wire signed [18:0] a={{SIGNEDA && A17,{concat("A",18)}}};',
               f'wire signed [18:0] b={{SIGNEDB && B17,{concat("B",18)}}};',
               'wire signed [37:0] product=a*b;',f'assign {concat("P",36)}=product[35:0];','endmodule']
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
    extras=[netlist,manifest_path,library,yosys,Path(__file__).resolve()]+list(directory.glob('*.v'))+list(directory.glob('*.vlt'))+[directory/'main.cpp',directory/'gate_config.hpp']
    snapshot.update(backend='mapped-ecp5-functional',parameters=parameters,
                    extra_inputs={str(p.relative_to(ROOT)):digest(p) for p in extras})
    snapshot_path.write_text(json.dumps(snapshot,indent=2)+'\n')
    args=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL','--top-module','wasmetal_core',
          '--cc','--exe','--output-split','10000','--output-split-cfuncs','10000',
          '--Mdir',str(binary.parent),'-CFLAGS','-std=c++17 -O2 -Wall -Wextra -Werror',
          str(directory/'vendor.vlt'),str(directory/'cells.v'),str(directory/'core.v'),str(directory/'main.cpp')]
    subprocess.run(args,cwd=ROOT,env=dict(os.environ,VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),check=True)
    # Verilator 5.020 emits integer-valued LUT ternaries in Boolean contexts.
    # Suppress that C++ style warning only in its generated implementation;
    # the handwritten host adapter still compiles with all warnings as errors.
    generated=list(binary.parent.glob('Vwasmetal_core*.cpp'))
    for path in generated:
        path.write_text('#pragma GCC diagnostic ignored "-Wint-in-bool-context"\n'+path.read_text())
    snapshot['extra_inputs'].update({str(p.relative_to(ROOT)):digest(p) for p in generated+list(binary.parent.glob('V*.h'))})
    snapshot_path.write_text(json.dumps(snapshot,indent=2)+'\n')
    subprocess.run(['make','-C',str(binary.parent),'-f','Vwasmetal_core.mk','-j','2'],check=True,cwd=ROOT,
                   env=dict(os.environ,VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')))
    build_identity.finish(binary)
    print('Built mapped CPU simulator',binary)


if __name__=='__main__': main()
