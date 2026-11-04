from pathlib import Path
import json
import subprocess
import sys
sys.path.insert(0,'tools')
import cad
from prepare_standalone import ROOT,digest
from route_reset_experiment import ALTERNATE_WEIGHTS

directory=ROOT/'build/reset-alternate-preflight'
source=directory/'placement-for-routing.json'
output=directory/'native-roundtrip.json'
command=cad.command('nextpnr-ecp5')+['--85k','--package','CABGA381','--speed','6',
    '--json',str(source),'--no-pack','--no-place','--no-route','--write',str(output)]
with (directory/'native-roundtrip.log').open('w') as log:
    subprocess.run(command,env=cad.environment(),stdout=log,stderr=subprocess.STDOUT,check=True,timeout=60)
before=json.loads(source.read_text())['modules']['top']['settings']
after=json.loads(output.read_text())['modules']['top']['settings']
expected={'router':'router2',**ALTERNATE_WEIGHTS}
assert all(after[k]==v for k,v in expected.items()),after
for name in ('seed','target_freq','timing_driven','arch.type','arch.speed','arch.package'):
    assert after[name]==before[name],name
report={'status':'passed','scope':'actual pinned nextpnr import/export of selected routing settings; no routing or physical-fit claim',
    'command':command,'settings':expected,'preserved_settings':{k:after[k] for k in ('seed','target_freq','timing_driven','arch.type','arch.speed','arch.package')},
    'inputs':{str(p.relative_to(ROOT)):digest(p) for p in [source,Path(__file__).resolve(),ROOT/'tools/cad.py',ROOT/'tools/route_reset_experiment.py',cad.SUITE/'libexec/nextpnr-ecp5']},
    'output_sha256':digest(output),'log_sha256':digest(directory/'native-roundtrip.log')}
(directory/'native-settings-check.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS native settings import/export, preserved seed/target/device and explicit alternate weights')
