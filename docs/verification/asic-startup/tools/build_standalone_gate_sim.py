#!/usr/bin/env python3
"""Functional simulation of the complete mapped standalone board circuit."""
import argparse
import collections
import copy
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import ecp5_ram
import ecp5_standalone_ram
import ecp5_loadable_ram
from build_gate_sim import compilation, fast_lut_model
from prepare_standalone import ROOT, digest


def normalize(source, top):
    cells=source['modules'][top]['cells']
    consumed={b for c in cells.values() for name,bs in c['connections'].items()
              if c['port_directions'][name]=='input' for b in bs}
    consumed.update(b for port in source['modules'][top]['ports'].values()
                    if port['direction']=='output' for b in port['bits'])
    kinds=collections.Counter()
    supported={'LUT4','PFUMX','L6MUX21','CCU2C','TRELLIS_DPR16X4','TRELLIS_FF','MULT18X18D','DP16KD','DCCA'}
    for name,c in cells.items():
        ty=c['type'];params=c['parameters'];pins=c['connections']
        if ty not in supported: raise ValueError('unmodeled standalone primitive: '+ty)
        if ty=='DP16KD':
            try: ecp5_ram.check(c)
            except ValueError:
                try:kind=ecp5_standalone_ram.check(c,consumed)
                except ValueError:
                    kind=ecp5_loadable_ram.check(c,consumed);c['type']=ecp5_loadable_ram.NAME
                else:c['type']=ecp5_standalone_ram.NAME
                kinds[kind]+=1
            else: kinds['core']+=1
        elif ty=='DCCA':
            if params or set(pins)!={'CLKI','CE','CLKO'} or pins['CE']!=['1']:
                raise ValueError('only permanently enabled DCCA is modeled')
        elif ty in ('PFUMX','L6MUX21') and params:
            raise ValueError('unsupported LUT multiplexer parameters')
        elif ty=='TRELLIS_FF':
            if 'M' not in pins:
                if params.get('LSRMODE','LSR').rstrip()=='PRLD': raise ValueError('missing preload pin')
                pins['M']=['0'];c['port_directions']['M']='input'
            if 'CE' not in pins:
                if params.get('CEMUX','1 ').rstrip() not in ('0','1'): raise ValueError('missing active clock enable')
                pins['CE']=['0'];c['port_directions']['CE']='input'
        elif ty=='MULT18X18D':
            allowed={f'{p}{i}' for p in 'ABC' for i in range(18)}|{f'P{i}' for i in range(36)}|{'SIGNEDA','SIGNEDB','SOURCEA','SOURCEB'}
            if params or set(pins)!=allowed: raise ValueError('unsupported multiplier configuration')
            if any(pins[p]!=['0'] for p in ['SOURCEA','SOURCEB']+[f'C{i}' for i in range(18)]):
                raise ValueError('unsupported multiplier cascade')
    if any(c['type']==ecp5_standalone_ram.NAME for c in cells.values()):
        source['modules'][ecp5_standalone_ram.NAME]=copy.deepcopy(source['modules']['DP16KD'])
    if any(c['type']==ecp5_loadable_ram.NAME for c in cells.values()):
        source['modules'][ecp5_loadable_ram.NAME]=copy.deepcopy(source['modules']['DP16KD'])
    return dict(kinds)


def models(library):
    text=library.read_text(); result=[]
    for name in ('LUT2','LUT4','PFUMX','L6MUX21','CCU2C','TRELLIS_DPR16X4','TRELLIS_FF'):
        match=re.search(r'\bmodule\s+'+name+r'\b.*?\bendmodule',text,re.S)
        if not match: raise ValueError('missing official cell model: '+name)
        model=re.sub(r'\bspecify\b.*?\bendspecify\b','',match[0],flags=re.S)
        if name in ('LUT2','LUT4'): model=fast_lut_model(model,name)
        result.append(model)
    pins=sorted({f'{p}{i}' for p in 'ABC' for i in range(18)}|{f'P{i}' for i in range(36)}|{'SIGNEDA','SIGNEDB','SOURCEA','SOURCEB'})
    concat=lambda prefix,n:'{'+','.join(f'{prefix}{i}' for i in reversed(range(n)))+'}'
    result+=['module MULT18X18D('+','.join(('output' if p.startswith('P') else 'input')+' wire '+p for p in pins)+');',
             f'wire signed [18:0] a={{SIGNEDA && A17,{concat("A",18)}}};',
             f'wire signed [18:0] b={{SIGNEDB && B17,{concat("B",18)}}};',
             'wire signed [37:0] product=a*b;',f'assign {concat("P",36)}=product[35:0];','endmodule',
             'module DCCA(input wire CLKI,CE,output wire CLKO); assign CLKO=CLKI & CE; endmodule',
             ecp5_ram.model(),ecp5_standalone_ram.model(),ecp5_loadable_ram.model()]
    return '\n'.join(result)+'\n'


def build(netlist,directory,top='wasmetal_standalone_ulx3s',harness=None,cflags=' -DWASMETAL_BOARD',jobs=4):
    directory.mkdir(parents=True,exist_ok=True)
    harness=harness or ROOT/'tests/standalone/system.cpp'
    library=ROOT/'.cache/tools/usr/share/yosys/ecp5/cells_sim.v'
    inputs=[netlist,Path(__file__).resolve(),ROOT/'tools/build_gate_sim.py',ROOT/'tools/ecp5_ram.py',
            ROOT/'tools/ecp5_standalone_ram.py',ROOT/'tools/ecp5_loadable_ram.py',ROOT/'tools/check_ecp5_luts.py',library,harness]
    manifest_path=netlist.with_suffix('.manifest.json')
    manifest=json.loads(manifest_path.read_text())
    if digest(netlist)!=manifest['netlist_sha256']: raise ValueError('standalone netlist hash mismatch')
    for name,value in manifest['inputs'].items():
        if digest(ROOT/name)!=value: raise ValueError('stale standalone netlist: '+name)
    inputs.append(manifest_path)
    hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs}
    source=json.loads(netlist.read_text()); kinds=normalize(source,top)
    (directory/'normalized.json').write_text(json.dumps(source))
    script=directory/'export.ys'
    script.write_text(f'read_json {directory}/normalized.json\nsplitnets\nclean -purge\ncheck -assert\nwrite_verilog -noattr {directory}/circuit.v\n')
    with (directory/'export.log').open('w') as log:
        subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-Q','-T','-s',str(script)],
                       stdout=log,stderr=subprocess.STDOUT,check=True)
    subprocess.run([sys.executable,str(ROOT/'tools/check_ecp5_luts.py'),'--top',top,
                    '--core-netlist',str(netlist),'--directory',str(directory/'lut-proof')],check=True)
    (directory/'cells.v').write_text(models(library))
    (directory/'vendor.vlt').write_text('`verilator_config\n'+''.join(
        f'lint_off -rule {rule} -file "{directory}/{name}"\n'
        for name,rules in [('circuit.v',['DECLFILENAME','PINCONNECTEMPTY']),
            ('cells.v',['DECLFILENAME','INITIALDLY','GENUNNAMED','UNUSEDPARAM','WIDTHEXPAND','SYNCASYNCNET'])]
        for rule in rules))
    options=compilation(True,True); flags=options['cflags']+cflags
    obj=directory/'obj'; binary=obj/('V'+top)
    args=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL',
          '--top-module',top,'--cc','--exe','--output-split','10000','--output-split-cfuncs','10000',
          '--Mdir',str(obj),'-CFLAGS',flags,str(directory/'vendor.vlt'),str(directory/'cells.v'),
          str(directory/'circuit.v'),str(harness)]
    env=dict(os.environ,VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator'))
    with (directory/'build.log').open('w') as log:
        result=subprocess.run(args,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
        if result.returncode:
            log.flush(); print((directory/'build.log').read_text()[-12000:]); result.check_returncode()
        # Verilator uses integer masks/negation on Boolean LUT expressions.
        # Scope these C++ style warnings to generated implementation files;
        # handwritten test code and HDL structural warnings remain fatal.
        for path in obj.glob('V*.cpp'):
            text=path.read_text()
            body=re.sub(r'^(?:#pragma GCC diagnostic ignored "-(?:Wint-in-bool-context|Wbool-operation)"\n)+','',text)
            candidate='#pragma GCC diagnostic ignored "-Wint-in-bool-context"\n#pragma GCC diagnostic ignored "-Wbool-operation"\n'+body
            if candidate!=text: path.write_text(candidate)
        command=['make','-C',str(obj),'-f','V'+top+'.mk','-j',str(jobs),
                 'CXX='+options['compiler'],'LINK='+options['compiler'],'VM_USER_CFLAGS='+flags,
                 'OPT_FAST=-O3','OPT_SLOW=-O3','OPT_GLOBAL=-O3']
        result=subprocess.run(command,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
        if result.returncode:
            log.flush(); print((directory/'build.log').read_text()[-12000:]); result.check_returncode()
    for name,value in {**manifest['inputs'],**hashes}.items():
        if digest(ROOT/name)!=value: raise ValueError('mapped model input changed: '+name)
    hashes.update(manifest['inputs'])
    hashes.update({str(p.relative_to(ROOT)):digest(p) for p in
        [directory/'circuit.v',directory/'cells.v',directory/'lut-proof/report.json']})
    receipt={'backend':'standalone-mapped-ecp5-functional','top':top,'inputs':hashes,
             'binary_sha256':digest(binary),'netlist_sha256':digest(netlist),
             'ram_modes':kinds,'compilation':options,'physical_hardware_tested':False}
    Path(str(binary)+'.build.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(binary)
    return binary


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--netlist',type=Path,default=ROOT/'build/standalone-ulx3s/design.json')
    parser.add_argument('--directory',type=Path,default=ROOT/'build/standalone-gate-sim')
    args=parser.parse_args()
    build(args.netlist.resolve(),args.directory.resolve())
