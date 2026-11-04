"""Archive the resized counter and compare against the immutable earlier campaigns."""
from pathlib import Path
from collections import Counter
import gzip
import json
import shutil
import sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from prepare_standalone import digest
names=['memory-bist-mapped','memory-bist-four-state','memory-bist-proof','bist-sram-mapped','memory-bist-widths']
reports={name:json.loads((ROOT/'reports'/f'{name}.json').read_text()) for name in names}
for name,count in zip(names,[6,2,4,4,2]):
    if reports[name]['status']!='passed' or reports[name]['negative_controls_rejected']!=count:raise ValueError('incomplete gate: '+name)
files={ROOT/'reports'/f'{name}.json' for name in names};files.add(Path(__file__).resolve());verified={}
allowed={'.v','.sv','.svh','.ys','.vlt','.log','.json','.py','.cpp','.hpp','.vvp'}
def verify_inputs(value):
    if isinstance(value,list):
        for item in value:verify_inputs(item)
    elif isinstance(value,dict):
        for key,item in value.items():
            if key in {'inputs','artifacts'} and isinstance(item,dict):
                for name,sha in item.items():
                    if not isinstance(sha,str) or len(sha)!=64:continue
                    path=ROOT/name
                    if digest(path)!=sha:raise ValueError('changed counter verification input: '+name)
                    if name in verified and verified[name]!=sha:raise ValueError('conflicting identity: '+name)
                    verified[name]=sha
                    if path.is_relative_to(ROOT) and not path.is_relative_to(ROOT/'.cache') and path.suffix in allowed:files.add(path)
            verify_inputs(item)
for report in reports.values():verify_inputs(report)
comparisons=[]
for name,base_name,top,harness in [
    ('memory-bist-mapped','memory-bist','wasmetal_memory_bist','tests/memory/bist.cpp'),
    ('bist-sram-mapped','bist-sram','wasmetal_bist_sram','tests/asic/bist_sram.cpp')]:
    baseline_path=ROOT/'docs/verification'/base_name/'reports'/f'{name}.json'
    baseline=json.loads(baseline_path.read_text());current=reports[name]
    if baseline['inputs'][harness]!=current['inputs'][harness]:raise ValueError('independent oracle changed')
    def key(check):return (check['ram_bytes'],check.get('read_latency'),check['response_timeout'])
    before={key(check):check for check in baseline['checks']};after={key(check):check for check in current['checks']}
    if before.keys()!=after.keys():raise ValueError('configuration coverage changed')
    rows=[]
    for config,new in after.items():
        old=before[config]
        for backend in ['rtl','mapped']:
            if old['tests'][backend]['observations']!=new['tests'][backend]['observations']:
                raise ValueError('observable behavior changed: '+str(config))
        width=(80*(new['ram_bytes']//16)).bit_length()
        old_cells=old['mapped_primitives'];new_cells=new['mapped_primitives']
        if old_cells['TRELLIS_FF']-new_cells['TRELLIS_FF']!=64-width:raise ValueError('unexpected register saving')
        if new_cells['LUT4']>old_cells['LUT4']:raise ValueError('LUT cost grew')
        rows.append({'ram_bytes':new['ram_bytes'],'read_latency':new.get('read_latency'),
            'response_timeout':new['response_timeout'],'internal_counter_bits':width,
            'before_primitives':old_cells,'after_primitives':new_cells,
            'registers_saved':64-width,'lut4_saved':old_cells['LUT4']-new_cells['LUT4'],
            'exact_prior_observations_and_cycles':True})
        label=f"{new['ram_bytes']}-{new['response_timeout']}" if name=='memory-bist-mapped' else f"{new['ram_bytes']}-{new['read_latency']}-{new['response_timeout']}"
        base=ROOT/'build'/base_name/label
        for backend,test in new['tests'].items():
            binary=base/('native/obj/V'+top if backend=='rtl' else 'mapped-model/obj/V'+top)
            if digest(binary)!=test['binary_sha256'] or digest(base/(backend+'-observations.log'))!=test['log_sha256']:
                raise ValueError('changed execution artifact')
        if digest(base/'mapped.json')!=new['mapped_identity']['netlist_sha256']:raise ValueError('changed mapped circuit')
    comparisons.append({'campaign':name,'baseline_report':str(baseline_path.relative_to(ROOT)),
                        'baseline_sha256':digest(baseline_path),'current_report_sha256':digest(ROOT/'reports'/f'{name}.json'),
                        'unchanged_independent_oracle_sha256':current['inputs'][harness],'configurations':rows})
    for control in current['negative_controls']:
        if control['name']=='corrupt-read':
            base=ROOT/'build/bist-sram';binary=base/'80-3-11/native/obj/Vwasmetal_bist_sram';log=base/'corrupt-read.log'
        else:
            base=ROOT/'build'/base_name/'negative'/control['name'];binary=base/('native/obj/V'+top);log=base/'rejection.log'
            if digest(base/(top+'.sv'))!=control['source_sha256']:raise ValueError('changed negative source')
        if digest(binary)!=control['binary_sha256'] or digest(log)!=control['log_sha256']:raise ValueError('changed negative observation')
proof=reports['memory-bist-proof'];base=ROOT/'build/formal-memory-bist'
for check in proof['checks']:
    name=f"{check['ram_bytes']}-{check['response_timeout']}";log=base/(name+'.log')
    if digest(log)!=check['log_sha256'] or 'Induction step proven: SUCCESS!' not in log.read_text():raise ValueError('missing induction')
    files.update({log,base/(name+'.ys')})
for control in proof['negative_controls']:
    for suffix,field in [('.sv','source_sha256'),('.log','log_sha256')]:
        path=base/(control['name']+suffix)
        if digest(path)!=control[field]:raise ValueError('changed proof control')
        files.add(path)
    files.add(base/(control['name']+'.ys'))
four=reports['memory-bist-four-state'];base=ROOT/'build/memory-bist-four-state'
if digest(base/'positive.log')!=four['positive_log_sha256']:raise ValueError('changed four-state result')
for control in four['negative_controls']:
    for suffix,field in [('.sv','source_sha256'),('.log','log_sha256')]:
        if digest(base/(control['name']+suffix))!=control[field]:raise ValueError('changed four-state control')
for check in reports['memory-bist-widths']['checks']:
    base=ROOT/'build/memory-bist-widths'/str(check['ram_bytes'])
    for name,field in [('elaborated.json','netlist_sha256'),('boundary.ys','script_sha256'),('boundary.log','log_sha256')]:
        if digest(base/name)!=check[field]:raise ValueError('changed capacity-boundary proof')
for control in reports['memory-bist-widths']['negative_controls']:
    base=ROOT/'build/memory-bist-widths'
    for path,field in [(base/(control['name']+'.sv'),'source_sha256'),
                       (base/control['name']/'boundary.ys','script_sha256'),(base/control['name']/'boundary.log','log_sha256')]:
        if digest(path)!=control[field]:raise ValueError('changed capacity fault control')
for directory in ['build/memory-bist','build/bist-sram','build/memory-bist-four-state','build/memory-bist-widths']:
    for path in (ROOT/directory).rglob('*'):
        if path.is_file() and 'obj' not in path.relative_to(ROOT/directory).parts and path.suffix in allowed:files.add(path)
for directory in ['memory-bist-widths-unsized-initial','memory-bist-widths-explicit-size-initial','memory-bist-widths-json-initial']:
    # These are rejected fixture setups, not accepted circuit-failure results.
    for path in (ROOT/'build'/directory).rglob('*'):
        if path.is_file() and path.suffix in {'.py','.ys','.log'}:files.add(path)
for name in ['memory-bist-counter-driver.log','memory-bist-counter-proof-driver.log',
             'memory-bist-counter-four-state-driver.log','bist-sram-counter-driver.log',
             'memory-bist-widths-driver.log','counter-fanout-workflow-lint.log']:
    files.add(ROOT/'build'/name)
notices=ROOT/'build/counter-sizing-notices';notices.mkdir(exist_ok=True)
shutil.copyfile(ROOT/'.cache/tools/usr/share/doc/yosys/copyright',notices/'YOSYS_COPYRIGHT');files.add(notices/'YOSYS_COPYRIGHT')
result={'status':'passed','scope':'capacity-sized internal memory-test counter with unchanged 64-bit public interface',
        'comparisons':comparisons,'dedicated_fault_controls_rejected':18,
        'unbounded_safety_configurations':len(proof['checks']),'capacity_boundary_configurations':len(reports['memory-bist-widths']['checks']),
        'source_sha256':digest(ROOT/'soc/asic/wasmetal_memory_bist.sv'),
        'physical_hardware_tested':False,'default_cpu_integration':False,
        'limitations':['Resource savings describe the separate ECP5-mapped memory-test controller, not the default CPU or ASIC area.',
            'Large-capacity boundary checks use seeded final-read states and do not sweep large memories.',
            'Earlier rejected fixture setups exposed unsized signed SAT constants, width matching and JSON-alias setup issues; no success was accepted from those attempts.']}
summary=ROOT/'reports/memory-bist-counter-sizing.json';summary.write_text(json.dumps(result,indent=2)+'\n');files.add(summary)
destination=ROOT/'docs/verification/memory-bist-counter-sized';destination.mkdir(parents=True,exist_ok=True);index=[]
for path in sorted(files):
    original=path.read_bytes();relative=path.relative_to(ROOT);target=destination/relative;compressed=len(original)>262144
    if compressed:target=Path(str(target)+'.gz')
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(gzip.compress(original,mtime=0) if compressed else original)
    if (gzip.decompress(target.read_bytes()) if compressed else target.read_bytes())!=original:raise ValueError('archive differs')
    index.append({'original_path':str(relative),'archive_path':str(target.relative_to(ROOT)),
                  'original_sha256':digest(path),'archive_sha256':digest(target),'compressed':compressed})
(destination/'index.json').write_text(json.dumps(index,indent=2)+'\n')
for name in [*names,'memory-bist-counter-sizing']:
    (ROOT/'docs/verification'/f'{name}.json').write_bytes((ROOT/'reports'/f'{name}.json').read_bytes())
for report in reports.values():verify_inputs(report)
print('PASS counter comparison and',len(index),'archived artifacts;',len(verified),'bound input hashes;',
      'archive bytes',sum((ROOT/row['archive_path']).stat().st_size for row in index))
