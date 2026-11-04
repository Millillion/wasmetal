#!/usr/bin/env python3
"""Compare complete CPU logic cones between LUT4 and ABC9 mappings.

Only matching flip-flop, RAM and multiplier primitives are abstracted. Their
parameters must match; their outputs become shared arbitrary inputs and their
inputs remain observations. No combinational intermediate is an assumed input.
Output partitioning retains each original cone and every original input. This
compares two technology mappings, not RTL against silicon or primitive behavior.
"""
import argparse
from collections import Counter, deque
import copy
import json
from pathlib import Path
import re
import subprocess
import time

import cad
import ecp5_ram
from prepare_standalone import ROOT, digest

MACROS={'TRELLIS_FF','DP16KD','MULT18X18D','TRELLIS_DPR16X4'}
LOGIC={'LUT4','CCU2C','PFUMX','L6MUX21'}


class Aig:
    """Read strict combinational binary AIGER, preserving positional symbols."""
    def __init__(self,path):
        data=path.read_bytes();position=data.index(b'\n');header=data[:position].split()
        if len(header)!=6 or header[0]!=b'aig':raise ValueError('expected binary AIGER without properties')
        self.maximum,self.inputs,latches,outputs,self.ands=map(int,header[1:])
        if latches or self.maximum!=self.inputs+self.ands:raise ValueError('expected dense combinational AIG')
        position+=1;self.outputs=[]
        for _ in range(outputs):
            end=data.index(b'\n',position);value=int(data[position:end]);position=end+1
            if not 0<=value<=2*self.maximum+1:raise ValueError('invalid AIG output literal')
            self.outputs.append(value)
        start=position
        def delta():
            nonlocal position
            value=0;shift=0
            while True:
                if position>=len(data) or shift>63:raise ValueError('truncated or oversized AIG delta')
                byte=data[position];position+=1;value|=(byte&127)<<shift
                if byte<128:return value
                shift+=7
        for index in range(self.ands):
            left=2*(self.inputs+index+1);a=left-delta();b=a-delta()
            if not 0<=b<=a<left:raise ValueError('non-topological AIG')
        self.gates=data[start:position];symbols={}
        for line in data[position:].decode('ascii').splitlines():
            if line=='c':break
            match=re.fullmatch(r'([io])(\d+) (.+)',line)
            if not match:
                if line:raise ValueError('unrecognized AIG symbol')
                continue
            key=(match[1],int(match[2]))
            if key in symbols:raise ValueError('duplicate AIG symbol')
            symbols[key]=match[3]
        expected={('i',n) for n in range(self.inputs)}|{('o',n) for n in range(outputs)}
        if set(symbols)!=expected:raise ValueError('missing or extra AIG positional symbols')
        self.input_names=[symbols['i',n] for n in range(self.inputs)]
        self.output_names=[symbols['o',n] for n in range(outputs)]
        if len(set(self.input_names))!=self.inputs or len(set(self.output_names))!=outputs:
            raise ValueError('ambiguous AIG symbols')

    def subset(self,path,indices,invert=False):
        if not indices or len(set(indices))!=len(indices) or any(not 0<=i<len(self.outputs) for i in indices):
            raise ValueError('invalid AIG observation subset')
        # Retain all AND nodes and all input positions. The solver can remove
        # unused gates itself; no new unconstrained internal input is created.
        outputs=[self.outputs[i]^(int(invert) if n==0 else 0) for n,i in enumerate(indices)]
        header=f'aig {self.maximum} {self.inputs} 0 {len(indices)} {self.ands}\n'
        symbols=''.join(f'i{i} {name}\n' for i,name in enumerate(self.input_names))
        symbols+=''.join(f'o{i} {self.output_names[n]}\n' for i,n in enumerate(indices))
        path.write_bytes(header.encode()+''.join(f'{v}\n' for v in outputs).encode()+self.gates+
            symbols.encode()+b'c\nWasMetal complete-cone observation subset\n')
        check=Aig(path)
        if check.input_names!=self.input_names or check.outputs!=outputs or check.gates!=self.gates:
            raise ValueError('AIG subset changed the original circuit or input positions')


def verify_hashes(hashes):
    for name,value in hashes.items():
        if digest(ROOT/name)!=value:raise ValueError('proof input changed: '+name)


def mapping(path):
    manifest_path=path.with_suffix('.manifest.json');manifest=json.loads(manifest_path.read_text())
    if manifest['top']!='wasmetal_core' or digest(path)!=manifest['netlist_sha256']:
        raise ValueError('expected an identified complete CPU mapping')
    verify_hashes(manifest['inputs'])
    if digest(path.with_suffix('.ys'))!=manifest['script_sha256']:raise ValueError('synthesis script changed')
    return json.loads(path.read_text())['modules']['wasmetal_core'],manifest


def cut(sources):
    macros=[{n:c for n,c in m['cells'].items() if c['type'] in MACROS} for m in sources]
    if macros[0].keys()!=macros[1].keys():raise ValueError('primitive instances differ')
    for name,a in macros[0].items():
        b=macros[1][name]
        if any(a[k]!=b[k] for k in ('type','parameters','port_directions')):
            raise ValueError('primitive configuration differs: '+name)
        if {p:len(v) for p,v in a['connections'].items()}!={p:len(v) for p,v in b['connections'].items()}:
            raise ValueError('primitive widths differ: '+name)
    interfaces=[{n:(p['direction'],len(p['bits'])) for n,p in m['ports'].items()} for m in sources]
    if interfaces[0]!=interfaces[1]:raise ValueError('CPU ports differ')
    used=[]
    for source in sources:
        bits={b for p in source['ports'].values() if p['direction']=='output' for b in p['bits']}
        bits.update(b for c in source['cells'].values() for p,bs in c['connections'].items()
            if c['port_directions'][p]=='input' for b in bs)
        used.append(bits)
    ignored={}
    for name,a in macros[0].items():
        if a['type']!='DP16KD':continue
        sides=[]
        for index in range(2):
            cell=macros[index][name];ecp5_ram.check(cell)
            width=int(cell['parameters']['DATA_WIDTH_A'],2);pins=set()
            for side in 'AB':
                for bit in range(18):
                    pin=f'DI{side}{bit}'
                    if width==9 and (side=='B' or bit>=9):pins.add(pin);continue
                    reads=[f'DO{side}{bit}'] if width==36 else [f'DOA{bit}',f'DOB{bit}']
                    if all(all(b not in used[index] for b in cell['connections'][p]) for p in reads):pins.add(pin)
            sides.append(pins)
        if sides[0]!=sides[1]:raise ValueError('RAM padding/unused pins differ: '+name)
        ignored[name]=sides[0]
    modules=[];meaning={}
    for source,macro in zip(sources,macros):
        module=copy.deepcopy(source);ports={n:module['ports'][n] for n in sorted(module['ports'])}
        for i,name in enumerate(sorted(macro)):
            cell=module['cells'].pop(name)
            for port in sorted(cell['connections']):
                if port in ignored.get(name,set()):continue
                direction=cell['port_directions'][port]
                if direction not in ('input','output'):raise ValueError('inout primitive')
                alias=f'cut_{i:05}_{port}';meaning[alias]=f'{name}.{port}'
                ports[alias]={'direction':'input' if direction=='output' else 'output','bits':cell['connections'][port]}
        symbolic=[b for p in ports.values() if p['direction']=='input' for b in p['bits']]
        if any(not isinstance(b,int) for b in symbolic) or len(set(symbolic))!=len(symbolic):
            raise ValueError('constant or aliased abstract inputs')
        if any(c['type'] not in LOGIC for c in module['cells'].values()):raise ValueError('unreviewed logic cell')
        for wire in module['netnames'].values():wire['attributes'].pop('init',None)
        module['ports']=ports;modules.append(module)
    return modules,{'primitive_cells':dict(Counter(c['type'] for c in macros[0].values())),
        'ignored_inactive_or_unread_ram_data_pins':{n:sorted(p) for n,p in ignored.items()},'port_meanings':meaning}


def aig_model(directory,label,module,library):
    netlist=directory/(label+'.json');netlist.write_text(json.dumps({'modules':{'wasmetal_core':module}}))
    script=directory/(label+'.ys')
    script.write_text(f'read_json {netlist}\nread_verilog {library}\nhierarchy -check -top wasmetal_core\n'
        f'proc\nflatten\nopt\ntechmap\nopt\naigmap\nclean -purge\ncheck -assert\n'
        f'write_json {directory}/{label}-aig.json\nwrite_aiger -symbols {directory}/{label}.aig\n')
    log=directory/(label+'.log')
    with log.open('w') as out:
        subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-Q','-T','-s',str(script)],
            cwd=ROOT,stdout=out,stderr=subprocess.STDOUT,check=True,timeout=1200)
    aig=json.loads((directory/(label+'-aig.json')).read_text())['modules']['wasmetal_core']
    if any(b in ('x','z') for p in aig['ports'].values() for b in p['bits']):raise ValueError('undefined AIG interface')
    for cell in aig['cells'].values():
        if cell['type'] not in ('$_AND_','$_NOT_') or any(b in ('x','z') for bits in cell['connections'].values() for b in bits):
            raise ValueError('undefined or unreviewed AIG logic')
    model=Aig(directory/(label+'.aig'))
    counts=Counter()
    for p in module['ports'].values():counts[p['direction']]+=len(p['bits'])
    if model.inputs!=counts['input'] or len(model.outputs)!=counts['output']:raise ValueError('AIG conversion omitted a boundary')
    return model


def compare(directory,models,indices,seconds,negative=False):
    directory.mkdir(parents=True,exist_ok=True)
    paths=[directory/(name+'.aig') for name in ('reference','candidate')]
    for side,(model,path) in enumerate(zip(models,paths)):model.subset(path,indices,invert=negative and side==1)
    reread=[Aig(p) for p in paths]
    if reread[0].input_names!=reread[1].input_names or reread[0].output_names!=reread[1].output_names:
        raise ValueError('positional solver interfaces differ')
    command=cad.command('yosys-abc')+['-c',f'&cec -T {seconds} -C 100000 {paths[0]} {paths[1]}']
    log=directory/'solver.log';started=time.monotonic();timeout=False
    with log.open('w') as out:
        try:
            run=subprocess.run(command,cwd=directory,env=cad.environment(),stdout=out,stderr=subprocess.STDOUT,timeout=seconds+60)
            code=run.returncode
        except subprocess.TimeoutExpired:timeout=True;code=None
    text=log.read_text()
    if code==0 and re.search(r'^Networks are equivalent\b',text,re.M):status='proven'
    elif code==0 and re.search(r'^Networks are NOT EQUIVALENT\b',text,re.M):status='counterexample'
    elif timeout or (code==0 and any(word in text.lower() for word in ('timeout','timed out','undecided'))):status='inconclusive'
    else:raise RuntimeError('solver did not produce a recognized result: '+str(log))
    return {'status':status,'indices':indices,'command':command,'exit_code':code,'wall_timeout':timeout,
        'elapsed_seconds':time.monotonic()-started,'log_sha256':digest(log),
        'circuits':{str(p.relative_to(ROOT)):digest(p) for p in paths}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference',type=Path,required=True);parser.add_argument('--candidate',type=Path,required=True)
    parser.add_argument('--directory',type=Path,default=ROOT/'build/core-mapping-proof')
    parser.add_argument('--report',type=Path,default=ROOT/'reports/core-mapping-proof.json')
    parser.add_argument('--group-size',type=int,default=256);parser.add_argument('--seconds',type=int,default=30)
    args=parser.parse_args()
    if not 1<=args.group_size<=4096 or not 1<=args.seconds<=600:parser.error('invalid proof bounds')
    directory=args.directory.resolve();directory.mkdir(parents=True,exist_ok=True)
    args.report.parent.mkdir(parents=True,exist_ok=True);args.report.unlink(missing_ok=True)
    paths=[p.resolve() for p in (args.reference,args.candidate)]
    loaded=[mapping(p) for p in paths];sources=[x[0] for x in loaded];manifests=[x[1] for x in loaded]
    expected=[{'lut4':True,'abc9':False},{'lut4':False,'abc9':True}]
    for manifest,flags in zip(manifests,expected):
        if any(manifest['arguments'].get(k)!=v for k,v in flags.items()):raise ValueError('expected LUT4 reference and ABC9 candidate')
    ignored={'lut4','abc9','output_name'}
    settings=[{k:v for k,v in m['arguments'].items() if k not in ignored} for m in manifests]
    if settings[0]!=settings[1]:
        raise ValueError('synthesis configurations differ beyond mapper/output name')
    if manifests[0]['inputs']!=manifests[1]['inputs']:raise ValueError('synthesis sources differ')
    library=ROOT/'.cache/tools/usr/share/yosys/ecp5/cells_sim.v'
    dependencies=[*paths,*[p.with_suffix('.manifest.json') for p in paths],*[p.with_suffix('.ys') for p in paths],
        library,Path(__file__).resolve(),ROOT/'tools/ecp5_ram.py',ROOT/'tools/cad.py',ROOT/'tools/prepare_standalone.py',
        ROOT/'.cache/tools/usr/bin/yosys',cad.SUITE/'libexec/yosys-abc']
    inputs={str(p.relative_to(ROOT)):digest(p) for p in dependencies};inputs.update(manifests[0]['inputs'])
    modules,boundaries=cut(sources)
    # A different primitive configuration must fail before any arbitrary-output
    # abstraction could hide it.
    corrupted=copy.deepcopy(sources);name=next(n for n,c in corrupted[1]['cells'].items() if c['type']=='TRELLIS_FF')
    corrupted[1]['cells'][name]['parameters']['REGSET']='SET' if corrupted[1]['cells'][name]['parameters']['REGSET']!='SET' else 'RESET'
    try:cut(corrupted)
    except ValueError as error:
        if 'primitive configuration differs' not in str(error):raise
    else:raise RuntimeError('primitive-configuration mutation was accepted')
    cells=directory/'cells.v';text=library.read_text();definitions=[]
    for name in sorted(LOGIC|{'LUT2'}):
        matches=re.findall(r'\bmodule\s+'+name+r'\b.*?\bendmodule',text,re.S)
        if len(matches)!=1:raise ValueError('ambiguous primitive model: '+name)
        definitions.append(re.sub(r'\bspecify\b.*?\bendspecify\b','',matches[0],flags=re.S))
    cells.write_text('\n'.join(definitions)+'\n')
    models=[aig_model(directory,label,module,cells) for label,module in zip(('reference','candidate'),modules)]
    if models[0].input_names!=models[1].input_names or models[0].output_names!=models[1].output_names:
        raise ValueError('complete positional AIG interfaces differ')
    generated=[cells,*[directory/(label+suffix) for label in ('reference','candidate') for suffix in ('.json','.ys','.aig','-aig.json')]]
    inputs.update({str(p.relative_to(ROOT)):digest(p) for p in generated})
    observations=directory/'observations.json';observations.write_text(json.dumps(models[0].output_names,indent=2)+'\n')
    negative_index=models[0].output_names.index('done')
    negative=compare(directory/'negative',models,[negative_index],args.seconds,negative=True)
    if negative['status']!='counterexample':raise RuntimeError('inverted CPU output was not rejected')
    total=len(models[0].outputs);queue=deque([list(range(i,min(i+args.group_size,total))) for i in range(0,total,args.group_size)])
    proven=set();attempts=[];unresolved=[];start=time.monotonic()
    report={'status':'running','scope':__doc__,'whole_mapping_equivalence_proven':False,'inputs':inputs,
        'boundaries':boundaries,'primary_and_abstract_input_bits':models[0].inputs,'required_observation_bits':total,
        'observations_sha256':digest(observations),'primitive_configuration_mutation_rejected':True,
        'inverted_cpu_output_rejected':True,'negative':negative,'attempts':attempts,'unresolved':unresolved,
        'physical_hardware_tested':False}
    while queue:
        indices=queue.popleft();name=f'{indices[0]:05}-{indices[-1]:05}'
        result=compare(directory/name,models,indices,args.seconds);attempts.append(result)
        if result['status']=='proven':
            if proven.intersection(indices):raise ValueError('duplicate proven observations')
            proven.update(indices)
        elif result['status']=='inconclusive' and len(indices)>1:
            half=len(indices)//2;queue.append(indices[:half]);queue.append(indices[half:])
        else:unresolved.append(result)
        report.update(proven_observation_bits=len(proven),pending_groups=len(queue),elapsed_seconds=time.monotonic()-start)
        args.report.write_text(json.dumps(report,indent=2)+'\n')
        print(f'{name}: {result["status"]}; {len(proven)}/{total} boundary bits proven',flush=True)
        if result['status']=='counterexample':break
    verify_hashes(inputs)
    passed=proven==set(range(total)) and not unresolved and not queue
    report.update(status='passed' if passed else 'inconclusive',complete_boundary_comparison_proven=passed)
    args.report.write_text(json.dumps(report,indent=2)+'\n')
    if not passed:raise RuntimeError('complete CPU boundary equivalence not established; inspect the report')
    print('PASS all original CPU logic cones; no internal combinational assumptions',flush=True)


if __name__=='__main__':main()
