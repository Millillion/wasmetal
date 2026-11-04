"""Copy and reverify the completed reset-distribution experiment as a new baseline."""
from pathlib import Path
import json
import shutil
import sys
ROOT=Path(__file__).resolve().parent.parent
OLD=Path('/tmp/wasmetal-direct-rounding')
sys.path.insert(0,str(ROOT/'tools'))
from prepare_standalone import digest
from route_reset_experiment import prepare
old_experiment=json.loads((OLD/'build/reset-replication/experiment.json').read_text())
paths=set(old_experiment['inputs'])|{'build/reset-replication/design.json',
    'build/reset-replication/placed.json','build/reset-replication/experiment.json'}
for name in sorted(paths):
    target=ROOT/name;original=OLD/name
    if target.exists():
        if digest(target)!=digest(original):raise ValueError('refusing to replace differing input: '+name)
    else:
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original,target)
    if digest(target)!=digest(original):raise ValueError('copied input differs: '+name)
experiment,candidate,placement=prepare(ROOT/'build/reset-replication/experiment.json',ROOT/'build/loadable-ulx3s')
original=json.loads((ROOT/'build/loadable-ulx3s/design.manifest.json').read_text())
inputs=dict(experiment['inputs'])
for path in [candidate,placement,ROOT/'build/reset-replication/experiment.json',Path(__file__).resolve()]:
    inputs[str(path.relative_to(ROOT))]=digest(path)
manifest={**original,'inputs':inputs,'netlist_sha256':digest(candidate),
    'provenance':'verified reset-distribution candidate; placement completed, routing incomplete',
    'structural_equivalence_rechecked':True,'physical_hardware_tested':False}
(ROOT/'build/reset-replication/design.manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
selection=[{'net':'system.execution.core.descriptor_read_'+side,'bit':bit} for side in ['a','b'] for bit in [0,1]]
(ROOT/'build/fanout-selection.json').write_text(json.dumps(selection,indent=2)+'\n')
print('PASS copied and reverified',len(paths),'frozen baseline inputs; selected four descriptor-address bits')
