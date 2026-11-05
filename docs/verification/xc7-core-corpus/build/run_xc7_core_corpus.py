"""Supervise the complete pinned Xilinx corpus using the checked worker lifecycle."""
from pathlib import Path
import json
import signal
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/'tools'))
import build_identity
import spec_ci
import spec_shards
from run_xc7_system import run_workers

logs = ROOT/'build/xc7-core-corpus'
reports = ROOT/'reports/xc7-core-shards'
logs.mkdir(exist_ok=True)
reports.mkdir(exist_ok=True)
if list(reports.glob('mapped-shard-*.json')):
    raise RuntimeError('use an empty output directory; preserve existing evidence')
reference_path = ROOT/'reports/core-rounding-wait-3.json'
plan_path = ROOT/'reports/xc7-core-plan.json'
reference = json.loads(reference_path.read_text())
plan = json.loads(plan_path.read_text())
models = {'native': ROOT/'build/obj/Vwasmetal_core',
          'mapped': ROOT/'build/xc7-core-sim/obj/Vwasmetal_core'}
manifests = {name: build_identity.verify(path) for name,path in models.items()}
assert manifests['native'] == reference['build_manifest']
assert manifests['mapped']['backend'] == 'mapped-xc7-functional'
source_hash, entries = spec_ci.catalog()
spec_ci.validate_reference(reference, source_hash, entries)
spec_shards.validate_plan(plan, source_hash, {n:len(c) for n,(_,c) in entries.items()})
inputs = dict(reference['runner_inputs'])
for model in manifests.values():
    for name, value in {**model['inputs'],**model.get('extra_inputs',{})}.items():
        if name in inputs and inputs[name] != value:
            raise ValueError('conflicting input identity: '+name)
        inputs[name] = value
for path in [Path(__file__),reference_path,plan_path,
             *[ROOT/'tools'/n for n in ('spec_ci.py','run_xc7_system.py','check_xc7_system.py',
                 'loadable_ci.py','standalone_support.py','prepare_standalone.py','program_upload.py')]]:
    inputs[str(path.relative_to(ROOT))] = spec_shards.sha256(path)

def verify():
    for name,value in inputs.items():
        if spec_shards.sha256(ROOT/name) != value:
            raise ValueError('campaign input changed: '+name)
    for name,path in models.items():
        if build_identity.verify(path) != manifests[name]:
            raise ValueError('campaign model changed: '+name)

verify()
commands = {s['id']:[sys.executable,'tools/run_spec.py','--simulator',str(models['mapped']),
    '--shard-plan',str(plan_path),'--shard-id',s['id'],'--wait-states','3','--jobs','1',
    '--response-timeout','36000','--progress-report',str(logs/('progress-'+s['id']+'.json')),
    '--report',str(reports/('mapped-shard-'+s['id']+'.json'))] for s in plan['shards']}
started = time.monotonic()
receipt = {'status':'running','inputs':inputs,'models':manifests,'commands':commands,
           'worker_limit':8,'completed_shards':[],'physical_hardware_tested':False}

def save(status):
    receipt.update(status=status,elapsed_seconds=time.monotonic()-started)
    temporary=logs/'campaign.json.tmp'
    temporary.write_text(json.dumps(receipt,indent=2)+'\n')
    temporary.replace(logs/'campaign.json')

def completed(index):
    report=json.loads((reports/('mapped-shard-'+index+'.json')).read_text())
    spec_shards.clean_report(report)
    assert report['build_manifest']==manifests['mapped'] and report['shard_id']==index
    receipt['completed_shards'].append(index)
    save('running')

def interrupted(number,frame):
    raise InterruptedError('signal '+str(number))

signal.signal(signal.SIGTERM,interrupted)
save('running')
output=ROOT/'reports/xc7-core-complete.json'
output.unlink(missing_ok=True)
try:
    run_workers(commands,list(commands),logs,8,completed)
    verify()
    paths=sorted(reports.glob('mapped-shard-*.json'))
    result=spec_ci.merge_reports(plan,spec_shards.sha256(plan_path),reference,
        spec_shards.sha256(reference_path),[json.loads(p.read_text()) for p in paths],source_hash,entries,
        execution_models=models,expected_backend='mapped-xc7-functional')
    verify()
    result['shard_reports']=[{'path':str(p),'sha256':spec_shards.sha256(p)} for p in paths]
    spec_ci.write_json(output,result)
    receipt['result_sha256']=spec_shards.sha256(output)
    save('passed')
    print('PASS all official suites, commands and exact native cycle traces',flush=True)
except BaseException as error:
    output.unlink(missing_ok=True)
    receipt['error']=repr(error)
    save('failed')
    raise
