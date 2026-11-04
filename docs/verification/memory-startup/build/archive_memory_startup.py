"""Archive completed startup component gates; whole-CPU integration is separate."""
from pathlib import Path
import gzip,json,shutil,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from prepare_standalone import digest
names=['memory-startup-mapped','memory-startup-proof','memory-startup-four-state']
reports={n:json.loads((ROOT/'reports'/f'{n}.json').read_text()) for n in names}
for name,controls in zip(names,[8,4,3]):
    if reports[name]['status']!='passed' or reports[name]['negative_controls_rejected']!=controls:raise ValueError('unfinished gate '+name)
files={ROOT/'reports'/f'{n}.json' for n in names};files.add(Path(__file__).resolve())
verified={};allowed={'.v','.sv','.svh','.ys','.vlt','.log','.json','.py','.cpp','.hpp','.vvp'}
def verify(value):
    if isinstance(value,list):
        for x in value:verify(x)
    elif isinstance(value,dict):
        for key,value in value.items():
            if key in {'inputs','artifacts'} and isinstance(value,dict):
                for name,sha in value.items():
                    if not isinstance(sha,str) or len(sha)!=64:continue
                    path=ROOT/name
                    if digest(path)!=sha:raise ValueError('changed startup input: '+name)
                    if name in verified and verified[name]!=sha:raise ValueError('conflicting startup input')
                    verified[name]=sha
                    if path.is_relative_to(ROOT) and not path.is_relative_to(ROOT/'.cache') and path.suffix in allowed:files.add(path)
            verify(value)
for report in reports.values():verify(report)
r=reports['memory-startup-mapped'];totals={}
for check in r['checks']:
    base=ROOT/'build/memory-startup'/f"{check['ram_bytes']}-{check['read_latency']}-{check['response_timeout']}"
    if check['tests']['rtl']['observations']!=check['tests']['mapped']['observations']:raise ValueError('unequal startup observations')
    for key,value in check['tests']['rtl']['observations'].items():
        if type(value) is int and key!='trace':totals[key]=totals.get(key,0)+value
    for backend,test in check['tests'].items():
        binary=base/('native/obj/Vwasmetal_startup_sram' if backend=='rtl' else 'mapped-model/obj/Vwasmetal_startup_sram')
        if digest(binary)!=test['binary_sha256'] or digest(base/(backend+'-observations.log'))!=test['log_sha256']:raise ValueError('changed startup executable or observations')
    if digest(base/'mapped.json')!=check['mapped_identity']['netlist_sha256']:raise ValueError('changed startup circuit')
for control in r['negative_controls']:
    if control['name']=='corrupt-read':
        binary=ROOT/'build/memory-startup/80-3-11/native/obj/Vwasmetal_startup_sram';log=ROOT/'build/memory-startup/corrupt-read.log'
    else:
        base=ROOT/'build/memory-startup/negative'/control['name'];binary=base/'native/obj/Vwasmetal_startup_sram';log=base/'rejection.log'
        if digest(base/'wasmetal_memory_startup.sv')!=control['source_sha256']:raise ValueError('changed startup mutation')
    if digest(binary)!=control['binary_sha256'] or digest(log)!=control['log_sha256']:raise ValueError('changed startup fault result')
proof=reports['memory-startup-proof'];base=ROOT/'build/formal-memory-startup'
for check in proof['checks']:
    label=f"{check['ram_bytes']}-{check['response_timeout']}"
    for suffix,key in [('.log','log_sha256'),('.ys','script_sha256')]:
        if digest(base/(label+suffix))!=check[key]:raise ValueError('changed startup proof')
    if 'Induction step proven: SUCCESS!' not in (base/(label+'.log')).read_text():raise ValueError('missing induction result')
for control in proof['negative_controls']:
    for suffix,key in [('.sv','source_sha256'),('.log','log_sha256'),('.ys','script_sha256')]:
        if digest(base/(control['name']+suffix))!=control[key]:raise ValueError('changed startup proof control')
four=reports['memory-startup-four-state'];base=ROOT/'build/memory-startup-four-state'
if digest(base/'positive.log')!=four['positive_log_sha256']:raise ValueError('changed startup four-state result')
for control in four['negative_controls']:
    for suffix,key in [('.sv','source_sha256'),('.log','log_sha256')]:
        if digest(base/(control['name']+suffix))!=control[key]:raise ValueError('changed startup four-state control')
inventory_path=ROOT/'reports/memory-startup-source-inventory.json';inventory=json.loads(inventory_path.read_text())
for name,sha in inventory['sources'].items():
    if digest(ROOT/name)!=sha:raise ValueError('changed default source inventory')
if digest(ROOT/'tools/build_standalone_sim.py')!=inventory['builder_sha256']:raise ValueError('changed source selector')
files.update({inventory_path,ROOT/'tools/build_standalone_sim.py',ROOT/'tools/build_loadable_sim.py'})
summary={'status':'passed','scope':'destructive startup test and CPU transaction handoff through SRAM adapter',
    'totals_per_model':totals,'rtl_and_mapped_observations_identical':True,'configuration_count':len(r['checks']),
    'unbounded_safety_configurations':len(proof['checks']),'dedicated_fault_controls_rejected':15,
    'reports':{n:digest(ROOT/'reports'/f'{n}.json') for n in names},
    'default_cpu_source_inventory_unchanged':True,'default_cpu_lint_passed':True,
    'default_cpu_lint_command':'python3 tools/build_loadable_sim.py --lint',
    'default_cpu_integration':False,'complete_cpu_simulation_passed':False,'physical_hardware_tested':False,
    'limitations':['CPU requests in this campaign come from an independent transaction generator.',
        'The complete-CPU startup integration is a separate ongoing experiment.',
        'The memory bridge must stay in reset until startup grants access; its ordinary transaction timeout is not extended.',
        'These are functional ECP5 mapping and RTL protocol results, not ASIC timing or a foundry macro test.']}
summary_path=ROOT/'reports/memory-startup-summary.json';summary_path.write_text(json.dumps(summary,indent=2)+'\n');files.add(summary_path)
for directory in ['build/memory-startup','build/formal-memory-startup','build/memory-startup-four-state','build/memory-startup-initial-rejected']:
    for path in (ROOT/directory).rglob('*'):
        if path.is_file() and 'obj' not in path.relative_to(ROOT/directory).parts and path.suffix in allowed:files.add(path)
for name in ['memory-startup-driver.log','memory-startup-proof-driver.log','memory-startup-four-state-driver.log',
             'memory-startup-default-lint.log','memory-startup-workflow-lint.log','loadable-sim/build.log']:
    files.add(ROOT/'build'/name)
notices=ROOT/'build/memory-startup-notices';notices.mkdir(exist_ok=True)
shutil.copyfile(ROOT/'.cache/tools/usr/share/doc/yosys/copyright',notices/'YOSYS_COPYRIGHT');files.add(notices/'YOSYS_COPYRIGHT')
destination=ROOT/'docs/verification/memory-startup';destination.mkdir(parents=True,exist_ok=True);index=[]
for path in sorted(files):
    raw=path.read_bytes();compressed=len(raw)>262144;target=destination/path.relative_to(ROOT)
    if compressed:target=Path(str(target)+'.gz')
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)
    if (gzip.decompress(target.read_bytes()) if compressed else target.read_bytes())!=raw:raise ValueError('startup archive differs')
    index.append({'original_path':str(path.relative_to(ROOT)),'archive_path':str(target.relative_to(ROOT)),
                  'original_sha256':digest(path),'archive_sha256':digest(target),'compressed':compressed})
(destination/'index.json').write_text(json.dumps(index,indent=2)+'\n')
for name in [*names,'memory-startup-summary','memory-startup-source-inventory']:
    (ROOT/'docs/verification'/f'{name}.json').write_bytes((ROOT/'reports'/f'{name}.json').read_bytes())
for report in reports.values():verify(report)
print('PASS startup archive:',len(index),'artifacts;',len(verified),'bound hashes;',sum((ROOT/r['archive_path']).stat().st_size for r in index),'bytes')
