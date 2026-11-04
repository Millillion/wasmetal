"""Retain the exact self-test/SRAM integration observations and fault controls."""
from pathlib import Path
import gzip
import json
import shutil
import sys

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from prepare_standalone import digest
report_path=ROOT/'reports/bist-sram-mapped.json'
report=json.loads(report_path.read_text())
if report['status']!='passed' or report['negative_controls_rejected']!=4:raise ValueError('unfinished integration')
files={report_path,Path(__file__).resolve(),ROOT/'build/bist-sram-driver.log',ROOT/'build/bist-sram-workflow-lint.log'}
verified={};allowed={'.sv','.v','.ys','.vlt','.log','.json','.cpp','.hpp','.py'}

def verify(value):
    if isinstance(value,list):
        for item in value:verify(item)
    elif isinstance(value,dict):
        for key,item in value.items():
            if key in {'inputs','artifacts'} and isinstance(item,dict):
                for name,sha in item.items():
                    if not isinstance(sha,str) or len(sha)!=64:continue
                    path=ROOT/name
                    if digest(path)!=sha:raise ValueError('changed integration input: '+name)
                    if name in verified and verified[name]!=sha:raise ValueError('conflicting input: '+name)
                    verified[name]=sha
                    if path.is_relative_to(ROOT) and not path.is_relative_to(ROOT/'.cache') and path.suffix in allowed:files.add(path)
            verify(item)

verify(report)
for check in report['checks']:
    base=ROOT/'build/bist-sram'/f"{check['ram_bytes']}-{check['read_latency']}-{check['response_timeout']}"
    if check['tests']['rtl']['observations']!=check['tests']['mapped']['observations']:raise ValueError('unequal observations')
    for backend,test in check['tests'].items():
        binary=base/('native/obj/Vwasmetal_bist_sram' if backend=='rtl' else 'mapped-model/obj/Vwasmetal_bist_sram')
        if digest(binary)!=test['binary_sha256']:raise ValueError('changed integration executable')
        if digest(base/(backend+'-observations.log'))!=test['log_sha256']:raise ValueError('changed observations')
    if digest(base/'mapped.json')!=check['mapped_identity']['netlist_sha256']:raise ValueError('changed circuit')
for control in report['negative_controls']:
    if control['name']=='corrupt-read':
        binary=ROOT/'build/bist-sram/80-3-11/native/obj/Vwasmetal_bist_sram';log=ROOT/'build/bist-sram/corrupt-read.log'
    else:
        base=ROOT/'build/bist-sram/negative'/control['name'];binary=base/'native/obj/Vwasmetal_bist_sram';log=base/'rejection.log'
        if digest(base/'wasmetal_bist_sram.sv')!=control['source_sha256']:raise ValueError('changed mutation')
    if digest(binary)!=control['binary_sha256'] or digest(log)!=control['log_sha256']:raise ValueError('changed fault result')
for path in (ROOT/'build/bist-sram').rglob('*'):
    if path.is_file() and 'obj' not in path.relative_to(ROOT/'build/bist-sram').parts and path.suffix in allowed:files.add(path)
# Preserve the initial rejected ambiguous mutation setup, without representing
# its incomplete campaign as an accepted gate result.
for name in ['driver.py','driver.log']:
    files.add(ROOT/'build/bist-sram-initial-control'/name)
notices=ROOT/'build/bist-sram-notices';notices.mkdir(exist_ok=True)
shutil.copyfile(ROOT/'.cache/tools/usr/share/doc/yosys/copyright',notices/'YOSYS_COPYRIGHT');files.add(notices/'YOSYS_COPYRIGHT')
destination=ROOT/'docs/verification/bist-sram';destination.mkdir(parents=True,exist_ok=True);index=[]
for path in sorted(files):
    relative=path.relative_to(ROOT);original=path.read_bytes();compressed=len(original)>262144
    target=destination/relative
    if compressed:target=Path(str(target)+'.gz')
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(gzip.compress(original,mtime=0) if compressed else original)
    if (gzip.decompress(target.read_bytes()) if compressed else target.read_bytes())!=original:raise ValueError('archive mismatch')
    index.append({'original_path':str(relative),'archive_path':str(target.relative_to(ROOT)),
                  'original_sha256':digest(path),'archive_sha256':digest(target),'compressed':compressed})
(destination/'index.json').write_text(json.dumps(index,indent=2)+'\n')
(ROOT/'docs/verification/bist-sram-mapped.json').write_bytes(report_path.read_bytes())
verify(report)
print('PASS archived',len(index),'integration artifacts;',len(verified),'bound input hashes checked;',
      'archive bytes',sum((ROOT/row['archive_path']).stat().st_size for row in index))
