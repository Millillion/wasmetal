#!/usr/bin/env python3
"""Prove wrapper combinational equivalence with identical state and CPU outputs.

Re-map the same prepared synthesis input with ABC, then compare every input of
every retained register, RAM and CPU instance and every external output against
ABC9. State/CPU outputs are arbitrary shared inputs. This is a combinational
cutpoint proof, not a formal proof of the CPU or physical clock behavior.
"""
import argparse
from collections import Counter,defaultdict
import copy
import json
from pathlib import Path
import re
import subprocess

from build_board import yosys
from prepare_standalone import ROOT,digest


STATE={'TRELLIS_FF','DP16KD','TRELLIS_DPR16X4','wasmetal_core'}
COMBINATIONAL={'LUT4','PFUMX','L6MUX21','CCU2C','DCCA'}


def register_aliases(module):
    aliases=defaultdict(set)
    for name,wire in module['netnames'].items():
        # Ignore technology-generated aliases, whose names can change meaning
        # between mappers. Retain RTL names and synthesized FSM state vectors.
        if name.startswith('$') or re.search(r'_(LUT4|TRELLIS_FF|CCU2C|PFUMX|L6MUX21)_',name):continue
        for index,bit in enumerate(wire['bits']):
            if isinstance(bit,int):aliases[bit].add((name,index))
    return aliases


def cut(reference,candidate):
    modules=[copy.deepcopy(reference),copy.deepcopy(candidate)]
    old_aliases,new_aliases=map(register_aliases,modules)
    register_index=defaultdict(set)
    for name,cell in candidate['cells'].items():
        if cell['type']=='TRELLIS_FF':
            for alias in new_aliases[cell['connections']['Q'][0]]:register_index[alias].add(name)
    inputs={name:port for name,port in reference['ports'].items() if port['direction']=='input'}
    if any(port['direction'] not in ('input','output') for m in modules for port in m['ports'].values()):
        raise ValueError('inout ports are not supported by the equivalence proof')
    interfaces=[{name:(p['direction'],len(p['bits'])) for name,p in m['ports'].items()} for m in modules]
    if interfaces[0]!=interfaces[1]:raise ValueError('wrapper interfaces differ')
    outputs=[[],[]];state_outputs=[[],[]];labels=[];pairs=[];used=set();kinds=Counter()
    for name,port in reference['ports'].items():
        if port['direction']=='output':
            for side,m in enumerate(modules):outputs[side]+=m['ports'][name]['bits']
            labels += [f'output {name}[{n}]' for n in range(len(port['bits']))]
    for name,cell in sorted(reference['cells'].items()):
        kind=cell['type']
        if kind not in STATE:
            if kind not in COMBINATIONAL:raise ValueError('unreviewed reference cell: '+kind)
            continue
        if kind=='TRELLIS_FF':
            matches=set().union(*(register_index[a] for a in old_aliases[cell['connections']['Q'][0]]))
            if len(matches)!=1:raise ValueError('register lacks a unique RTL alias match: '+name)
            target=matches.pop()
        else:target=name
        if target in used or target not in candidate['cells']:raise ValueError('missing or duplicate state match: '+target)
        other=candidate['cells'][target]
        if (cell['type'],cell['parameters'],cell['port_directions'])!=(other['type'],other['parameters'],other['port_directions']):
            raise ValueError('state primitive configuration differs: '+name)
        used.add(target);pairs.append((name,target));kinds[kind]+=1
        for port,direction in sorted(cell['port_directions'].items()):
            bits=[c['connections'][port] for c in (cell,other)]
            if len(bits[0])!=len(bits[1]):raise ValueError('state port widths differ: '+name+'.'+port)
            if direction=='output':
                if any(not isinstance(b,int) for group in bits for b in group):raise ValueError('constant state output')
                for side in range(2):state_outputs[side]+=bits[side]
            elif direction=='input':
                for side in range(2):outputs[side]+=bits[side]
                labels += [f'{name}.{port}[{n}]' for n in range(len(bits[0]))]
            else:raise ValueError('state cell has an inout port')
    if used!={name for name,c in candidate['cells'].items() if c['type'] in STATE}:
        raise ValueError('unmatched candidate state')
    for side,m in enumerate(modules):
        if len(set(state_outputs[side]))!=len(state_outputs[side]):raise ValueError('aliased state outputs')
        for pair in pairs:del m['cells'][pair[side]]
        if any(c['type'] not in COMBINATIONAL for c in m['cells'].values()):raise ValueError('unreviewed remaining cell')
        m['ports']={name:m['ports'][name] for name in inputs}
        m['ports']['state_outputs']={'direction':'input','bits':state_outputs[side]}
        m['ports']['observations']={'direction':'output','bits':outputs[side]}
        m['attributes']={}
        # Cut state is unconstrained, including registers initialized by RTL.
        for wire in m['netnames'].values():wire['attributes'].pop('init',None)
    return modules,dict(kinds),labels


def prove(directory,modules,negative=False):
    label='negative' if negative else 'positive';path=directory/label;path.mkdir(exist_ok=True)
    state_width=len(modules[0]['ports']['state_outputs']['bits'])
    width=len(modules[0]['ports']['observations']['bits'])
    declarations=[];connections=[]
    for name,port in modules[0]['ports'].items():
        if port['direction']=='input':
            declarations.append(f'input wire [{len(port["bits"])-1}:0] {name}')
            connections.append(f'.{name}({name})')
    (path/'cut.json').write_text(json.dumps({'modules':dict(zip(('reference','candidate'),modules))}))
    (path/'miter.v').write_text('module mapping_equivalence('+','.join(declarations)+',output wire mismatch);\n'+
        f'wire [{width-1}:0] a,b;\nreference reference_instance('+','.join(connections)+',.observations(a));\n'+
        'candidate candidate_instance('+','.join(connections)+',.observations(b));\n'+
        # Invert one real external output in the negative control.
        ('assign mismatch=|(a ^ b ^ {{'+str(width-1)+"{1'b0}},1'b1});\n" if negative else 'assign mismatch=|(a ^ b);\n')+
        'endmodule\nmodule DCCA(input wire CLKI,CE,output wire CLKO);assign CLKO=CLKI & CE;endmodule\n')
    script=f'''read_verilog +/ecp5/cells_sim.v
read_json {path}/cut.json
read_verilog -overwrite {path}/miter.v
prep -top mapping_equivalence -flatten
techmap
opt -full
abc -g simple
opt_clean
sat -timeout 180 -verify -prove mismatch 0
'''
    failed=False
    try:yosys(script,'proof',path)
    except subprocess.CalledProcessError:failed=True
    log=(path/'proof.log').read_text()
    marker='ERROR: Called with -verify and proof did fail!' if negative else 'SAT proof finished - no model found: SUCCESS!'
    if failed!=negative or marker not in log:raise ValueError(f'{label} equivalence check did not reach its expected result; see {path}/proof.log')
    return {'state_output_bits':state_width,'compared_bits':width,'log_sha256':digest(path/'proof.log')}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory',type=Path,default=ROOT/'build/loadable-ulx3s')
    parser.add_argument('--report',type=Path,default=ROOT/'reports/loadable-mapping-proof.json')
    args=parser.parse_args();mapped=args.directory.resolve();directory=mapped/'mapping-proof';directory.mkdir(exist_ok=True)
    manifest_path=mapped/'design.manifest.json';manifest=json.loads(manifest_path.read_text());top=manifest['top']
    paths=[Path(__file__).resolve(),ROOT/'tools/build_board.py',ROOT/'tools/prepare_standalone.py',
        manifest_path,mapped/'wrapper.json',mapped/'wrapper.ys',ROOT/'.cache/tools/usr/share/yosys/ecp5/cells_sim.v']
    hashes={str(p.relative_to(ROOT)):digest(p) for p in paths}
    hashes.update(manifest['inputs'])
    for name,value in hashes.items():
        if digest(ROOT/name)!=value:raise ValueError('stale mapping proof input: '+name)
    if manifest.get('wrapper_mapper')!='abc9':raise ValueError('ABC9 candidate mapping required')
    script=(mapped/'wrapper.ys').read_text();needle=f'synth_ecp5 -abc9 -top {top} -json {mapped}/wrapper.json'
    if script.count(needle)!=1:raise ValueError('unexpected wrapper synthesis script')
    reference_path=directory/'reference.json'
    yosys(script.replace(needle,f'synth_ecp5 -top {top} -json {reference_path}'),'reference',directory)
    reference=json.loads(reference_path.read_text())['modules'][top]
    candidate=json.loads((mapped/'wrapper.json').read_text())['modules'][top]
    modules,kinds,labels=cut(reference,candidate)
    (directory/'observations.json').write_text(json.dumps(labels,indent=2)+'\n')
    positive=prove(directory,modules);negative=prove(directory,modules,negative=True)
    for name,value in hashes.items():
        if digest(ROOT/name)!=value:raise ValueError('mapping proof input changed: '+name)
    report={'status':'passed','scope':__doc__,'top':top,'state_cells':kinds,'positive':positive,
        'inverted_output_rejected':True,'negative':negative,'inputs':hashes,
        'wrapper_cells':{'abc':dict(Counter(c['type'] for c in reference['cells'].values())),
                         'abc9':dict(Counter(c['type'] for c in candidate['cells'].values()))},
        'reference_sha256':digest(reference_path),'candidate_sha256':digest(mapped/'wrapper.json'),
        'physical_hardware_tested':False}
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS wrapper mapping equivalence and inverted-output negative control',flush=True)


if __name__=='__main__':main()
