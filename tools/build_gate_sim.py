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


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--core-netlist',type=Path,default=ROOT/'build/core-ecp5.json')
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
    supported={'LUT4','CCU2C','TRELLIS_DPR16X4','TRELLIS_FF','MULT18X18D'}
    for name,cell in core['cells'].items():
        if cell['type'] not in supported: raise ValueError(f'unmodeled primitive {cell["type"]}')
        if cell['type']=='MULT18X18D':
            # Yosys' basic DSP mapper uses unregistered multipliers, without
            # cascade, bypass, clocking, or pipeline settings. Reject other modes.
            if cell['parameters']: raise ValueError(f'unsupported DSP configuration: {name}')
            connections=cell['connections']
            allowed={f'{p}{i}' for p in 'ABC' for i in range(18)}|{f'P{i}' for i in range(36)}|{'SIGNEDA','SIGNEDB','SOURCEA','SOURCEB'}
            if set(connections)!=allowed: raise ValueError('unsupported DSP ports')
            for port in ['SOURCEA','SOURCEB']+[f'C{i}' for i in range(18)]:
                if connections[port]!=['0']: raise ValueError(f'unsupported DSP source: {port}')
    directory=ROOT/'build/gate-model';directory.mkdir(parents=True,exist_ok=True)
    yosys=ROOT/'.cache/tools/usr/bin/yosys'
    script=directory/'export.ys'
    script.write_text(f'read_json {netlist}\nwrite_verilog -noattr {directory}/core.v\n')
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
    main_cpp=(ROOT/'sim/main.cpp').read_text()
    assert main_cpp.count('#include "core_config.hpp"')==1
    (directory/'main.cpp').write_text(main_cpp.replace('#include "core_config.hpp"','#include "gate_config.hpp"'))
    config=(ROOT/'sim/core_config.hpp').read_text()
    for name,value in parameters.items():
        config,n=re.subn(r'(unsigned '+name+r'=)\d+;',lambda m:m[1]+str(value)+';',config)
        assert n==1,name
    (directory/'gate_config.hpp').write_text(config)
    # Scope generated-name and vendor-model warnings; structural warnings remain fatal.
    (directory/'vendor.vlt').write_text('`verilator_config\n'+''.join(
        f'lint_off -rule {rule} -file "{directory}/{name}"\n'
        for name,rules in [('core.v',['DECLFILENAME','PINCONNECTEMPTY']),('cells.v',['DECLFILENAME','INITIALDLY'])]
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
          '--cc','--exe','--build','-j','2','--output-split','10000','--output-split-cfuncs','10000',
          '--Mdir',str(binary.parent),'-CFLAGS','-std=c++17 -O2 -Wall -Wextra -Werror',
          str(directory/'vendor.vlt'),str(directory/'cells.v'),str(directory/'core.v'),str(directory/'main.cpp')]
    subprocess.run(args,cwd=ROOT,env=dict(os.environ,VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),check=True)
    build_identity.finish(binary)
    print('Built mapped CPU simulator',binary)


if __name__=='__main__': main()
