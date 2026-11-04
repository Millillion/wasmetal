"""Archive verified destructive memory-test evidence without simulation binaries."""
from pathlib import Path
import gzip
import hashlib
import json
import shutil
import sys

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from prepare_standalone import digest

names=('memory-bist-mapped','memory-bist-four-state','memory-bist-proof')
reports={name:json.loads((ROOT/'reports'/f'{name}.json').read_text()) for name in names}
files={ROOT/'reports'/f'{name}.json' for name in names}
files.update({ROOT/'reports/memory-bist-source-inventory.json',
              ROOT/'tools/build_standalone_sim.py',ROOT/'build/memory-bist-default-lint.log',
              ROOT/'build/loadable-sim/build.log'})
inventory=json.loads((ROOT/'reports/memory-bist-source-inventory.json').read_text())
if digest(ROOT/'tools/build_standalone_sim.py')!=inventory['builder_sha256']:
    raise ValueError('changed default source-selection code')
for name,sha in inventory['sources'].items():
    if digest(ROOT/name)!=sha:raise ValueError('changed default CPU source: '+name)
experiment=ROOT/'build/xc7-system-bist-inventory-experiment'
for name in ['report.json','synthesis.ys','synthesis.log','estimate_xc7_system.py','driver.log']:
    files.add(experiment/name)
verified={}
allowed={'.v','.sv','.svh','.vlt','.ys','.log','.json','.py','.cpp','.hpp','.vvp'}

def verify_inputs(value):
    if isinstance(value,list):
        for item in value:verify_inputs(item)
    elif isinstance(value,dict):
        for key,item in value.items():
            if key in {'inputs','artifacts'} and isinstance(item,dict):
                for name,sha in item.items():
                    if not isinstance(sha,str) or len(sha)!=64:continue
                    path=ROOT/name
                    if digest(path)!=sha:raise ValueError('changed verification input: '+name)
                    if name in verified and verified[name]!=sha:raise ValueError('conflicting input: '+name)
                    verified[name]=sha
                    if not path.is_relative_to(ROOT/'.cache') and path.is_relative_to(ROOT) and path.suffix in allowed:
                        files.add(path)
            verify_inputs(item)

for name,report in reports.items():
    if report['status']!='passed':raise ValueError('unfinished report: '+name)
    verify_inputs(report)
for check in reports['memory-bist-mapped']['checks']:
    base=ROOT/'build/memory-bist'/f"{check['ram_bytes']}-{check['response_timeout']}"
    for backend,test in check['tests'].items():
        binary=base/('native/obj/Vwasmetal_memory_bist' if backend=='rtl' else 'mapped-model/obj/Vwasmetal_memory_bist')
        if digest(binary)!=test['binary_sha256']:raise ValueError('changed positive executable')
        if digest(base/(backend+'-observations.log'))!=test['log_sha256']:raise ValueError('changed observation log')
    if check['tests']['rtl']['observations']!=check['tests']['mapped']['observations']:
        raise ValueError('mapped observations differ')
    if digest(base/'mapped.json')!=check['mapped_identity']['netlist_sha256']:
        raise ValueError('changed mapped circuit')
for control in reports['memory-bist-mapped']['negative_controls']:
    base=ROOT/'build/memory-bist/negative'/control['name']
    for filename,field in [('wasmetal_memory_bist.sv','source_sha256'),
                           ('native/obj/Vwasmetal_memory_bist','binary_sha256'),('rejection.log','log_sha256')]:
        if digest(base/filename)!=control[field]:raise ValueError('changed simulation fault artifact')
four=reports['memory-bist-four-state'];base=ROOT/'build/memory-bist-four-state'
if digest(base/'positive.log')!=four['positive_log_sha256']:raise ValueError('changed four-state result')
for control in four['negative_controls']:
    for extension,field in [('.sv','source_sha256'),('.log','log_sha256')]:
        if digest(base/(control['name']+extension))!=control[field]:raise ValueError('changed four-state fault artifact')
proof=reports['memory-bist-proof'];base=ROOT/'build/formal-memory-bist'
for check in proof['checks']:
    log=base/f"{check['ram_bytes']}-{check['response_timeout']}.log"
    if check['status']!='proven' or digest(log)!=check['log_sha256'] or 'Induction step proven: SUCCESS!' not in log.read_text():
        raise ValueError('incomplete positive proof')
for control in proof['negative_controls']:
    for extension,field in [('.sv','source_sha256'),('.log','log_sha256')]:
        if digest(base/(control['name']+extension))!=control[field]:raise ValueError('changed proof fault artifact')
    if 'proof did fail' not in (base/(control['name']+'.log')).read_text():raise ValueError('missing proof fault rejection')
if [reports[n]['negative_controls_rejected'] for n in names]!=[6,2,4]:raise ValueError('wrong fault-control counts')
for directory in ['build/memory-bist','build/memory-bist-four-state','build/formal-memory-bist']:
    for path in (ROOT/directory).rglob('*'):
        if path.is_file() and 'obj' not in path.relative_to(ROOT/directory).parts and path.suffix in allowed:files.add(path)
for filename in ['memory-bist-driver.log','memory-bist-four-state-driver.log','memory-bist-proof-driver.log','memory-bist-workflow-lint.log']:
    files.add(ROOT/'build'/filename)
files.add(Path(__file__).resolve())
notices=ROOT/'build/memory-bist-notices';notices.mkdir(exist_ok=True)
shutil.copyfile(ROOT/'.cache/tools/usr/share/doc/yosys/copyright',notices/'YOSYS_COPYRIGHT')
files.add(notices/'YOSYS_COPYRIGHT')
# Retain unsuccessful early bounds and the successful directed experiment as
# exploratory evidence; none substitutes for the four accepted positive proofs.
experiment=ROOT/'build/formal-memory-bist/descent-bound-experiments'
if experiment.exists():
    note={'scope':'exploratory descending-sweep fault controls',
          'unconstrained_12_steps':'did not expose the late fault',
          'unconstrained_32_steps':'timed out after 180 seconds; no accepted result',
          'directed_32_steps':'reachable fault exposed with a single reset, held start, immediate responses and expected read values',
          'directed_source_sha256':digest(ROOT/'build/formal-memory-bist/directed-descent.sv'),
          'directed_log_sha256':digest(ROOT/'build/formal-memory-bist/directed-descent.log'),
          'accepted_positive_proofs':'separate unbounded induction with arbitrary binary starts, responses, data and resets',
          'physical_hardware_tested':False}
    if 'proof did fail' not in (ROOT/'build/formal-memory-bist/directed-descent.log').read_text():
        raise ValueError('missing directed experiment counterexample')
    path=experiment/'outcome.json';path.write_text(json.dumps(note,indent=2)+'\n');files.add(path)

destination=ROOT/'docs/verification/memory-bist';destination.mkdir(parents=True,exist_ok=True)
index=[]
for path in sorted(files):
    original=path.read_bytes();relative=path.relative_to(ROOT);target=destination/relative
    compressed=len(original)>262144
    if compressed:target=Path(str(target)+'.gz')
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(gzip.compress(original,mtime=0) if compressed else original)
    if (gzip.decompress(target.read_bytes()) if compressed else target.read_bytes())!=original:
        raise ValueError('archive differs: '+str(path))
    index.append({'original_path':str(relative),'archive_path':str(target.relative_to(ROOT)),
                  'original_sha256':hashlib.sha256(original).hexdigest(),'archive_sha256':digest(target),'compressed':compressed})
(destination/'index.json').write_text(json.dumps(index,indent=2)+'\n')
for name in (*names,'memory-bist-source-inventory'):
    (ROOT/'docs/verification'/f'{name}.json').write_bytes((ROOT/'reports'/f'{name}.json').read_bytes())
for report in reports.values():verify_inputs(report)
print('PASS archived',len(index),'artifacts;',len(verified),'bound artifact hashes checked;',
      'archive bytes',sum((ROOT/row['archive_path']).stat().st_size for row in index))
