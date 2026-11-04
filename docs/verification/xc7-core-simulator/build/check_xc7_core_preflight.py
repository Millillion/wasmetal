"""Exercise real builder rejections without modifying campaign inputs."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
import build_identity
from prepare_standalone import digest

base_path=ROOT/'build/xc7-core/mapped.json'
manifest_path=base_path.with_suffix('.manifest.json')
base=json.loads(base_path.read_text())
manifest=json.loads(manifest_path.read_text())
directory=ROOT/'build/xc7-core-preflight'
directory.mkdir(exist_ok=True)
binary=ROOT/'build/xc7-core-sim/obj/Vwasmetal_core'
model=build_identity.verify(binary)
results=[]

def check(name, expected, mutate_manifest=None, mutate_module=None):
    target=directory/name;target.mkdir(exist_ok=True)
    receipt=deepcopy(manifest)
    netlist=target/'mapped.json'
    if mutate_module is not None:
        circuit=deepcopy(base)
        mutate_module(circuit['modules']['wasmetal_core'])
        netlist.write_text(json.dumps(circuit)+'\n')
        receipt['netlist_sha256']=digest(netlist)
    elif name=='wrong-cell-inventory':
        # An independent copy is deliberately used; no mutable hard link.
        netlist.write_bytes(base_path.read_bytes())
    else:
        netlist.write_text('{}\n')
    if mutate_manifest is not None:mutate_manifest(receipt)
    sidecar=netlist.with_suffix('.manifest.json')
    sidecar.write_text(json.dumps(receipt,indent=2)+'\n')
    command=[sys.executable,'tools/build_xc7_core_sim.py','--netlist',str(netlist),
             '--directory',str(target/'unused-model'),'--jobs','1']
    run=subprocess.run(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
    log=target/'rejection.log';log.write_bytes(run.stdout)
    if run.returncode==0 or expected not in run.stdout.decode():
        raise ValueError('fault did not fail at its intended check: '+name)
    if (target/'unused-model').exists():
        raise ValueError('preflight fault reached model generation: '+name)
    results.append({'name':name,'expected_rejection':expected,'command':command,
        'exit_code':run.returncode,'log':str(log.relative_to(ROOT)),'log_sha256':digest(log),
        'manifest_sha256':digest(sidecar),'netlist_sha256':digest(netlist)})
    print('REJECTED',name,flush=True)

contract='verified Xilinx mapping at the official-suite capacities required'
check('wrong-family',contract,lambda m:m.update(family='ecp5'))
check('wrong-top',contract,lambda m:m.update(top='wasmetal_loadable'))
check('wrong-capacity',contract,lambda m:m['parameters'].update(HEAP_SLOTS=1024))
check('changed-source','mapped core input changed:',lambda m:m['inputs'].update({next(iter(m['inputs'])):'0'*64}))
check('changed-netlist','synthesized circuit changed')
check('wrong-cell-inventory','mapped primitive inventory differs',lambda m:m['cell_counts'].update(LUT1=0))

def mutate_cell(module,kind,mutate):
    mutate(next(c for c in module['cells'].values() if c['type']==kind))

check('unreviewed-primitive','unreviewed core primitive:',mutate_module=lambda m:
      mutate_cell(m,'LUT1',lambda c:c.update(type='UNREVIEWED')))
check('wrong-async-reset','review the shared reset and asynchronous HardFloat consumers',mutate_module=lambda m:
      mutate_cell(m,'FDCE',lambda c:c['connections'].update(CLR=['0'])))
check('unverified-lookup-table','component audit omitted this exact core: luts',mutate_module=lambda m:
      mutate_cell(m,'LUT1',lambda c:c['parameters'].update(INIT=('1' if c['parameters']['INIT'][0]=='0' else '0')+c['parameters']['INIT'][1:])))
if build_identity.verify(binary)!=model:raise ValueError('positive executable changed')
report={'status':'passed','scope':'real builder preflight faults; no simulated instructions in these controls',
        'positive_model':model,'negative_controls_rejected':len(results),'negative_controls':results,
        'inputs':{str(p.relative_to(ROOT)):digest(p) for p in [Path(__file__),base_path,manifest_path,
                      ROOT/'tools/build_xc7_core_sim.py',ROOT/'tools/check_xc7_dsp.py',ROOT/'tools/check_xc7_flops.py']},
        'physical_hardware_tested':False}
(ROOT/'reports/xc7-core-preflight.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS',len(results),'builder fault controls',flush=True)
