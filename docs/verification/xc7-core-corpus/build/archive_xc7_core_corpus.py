"""Archive the completed corpus and a separately identified post-run input audit."""
from pathlib import Path
import gzip,hashlib,io,json,shutil,sys,tarfile,tempfile
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
import build_identity,spec_ci
from spec_shards import sha256,require,clean_report

destination=ROOT/'docs/verification/xc7-core-corpus'
require(not destination.exists(),'refusing to overwrite an existing evidence archive')
stage=Path(tempfile.mkdtemp(prefix='archive-xc7-corpus-',dir=ROOT/'build'))
campaign_path=ROOT/'build/xc7-core-corpus/campaign.json'
reconciliation_path=ROOT/'reports/xc7-core-reconciliation.json'
conversion_path=ROOT/'reports/spec-conversion.json'
aggregate_path=ROOT/'reports/xc7-core-reconciled.json'
original_path=ROOT/'reports/xc7-core-complete.json'
reference_path=ROOT/'reports/core-rounding-wait-3.json'
plan_path=ROOT/'reports/xc7-core-plan.json'
campaign,reconciliation,conversion,aggregate,original,reference,plan=[json.loads(p.read_text()) for p in
 (campaign_path,reconciliation_path,conversion_path,aggregate_path,original_path,reference_path,plan_path)]
require(campaign['status']==reconciliation['status']==conversion['status']=='passed','incomplete campaign')
require(sha256(original_path)==campaign['result_sha256'],'original aggregate identity changed')
require(sha256(aggregate_path)==reconciliation['aggregate_sha256'],'reconciled aggregate identity changed')
require(aggregate['full_core_suite_passed'] and aggregate['suite_files']==259,'incomplete official corpus')
require(aggregate['totals']==original['totals']==reconciliation['totals'],'aggregate observations differ')
require(conversion['suite_files']==259 and conversion['script_commands']==aggregate['totals']['script_commands'],
        'conversion corpus size differs')
require(conversion['official_sources_sha256']==aggregate['official_sources_sha256'],'conversion source identity differs')
require(conversion['negative_controls_rejected']==13 and not conversion['historical_execution_input_attestation'],
        'incorrect conversion audit scope')
models={'native':ROOT/'build/obj/Vwasmetal_core','mapped':ROOT/'build/xc7-core-sim/obj/Vwasmetal_core'}
manifests={name:build_identity.verify(path) for name,path in models.items()}
require(manifests==campaign['models'],'campaign execution models changed')
paths=sorted((ROOT/'reports/xc7-core-shards').glob('mapped-shard-*.json'))
rows=[json.loads(path.read_text()) for path in paths]
require(len(rows)==16,'missing original shard report')
for row in rows:clean_report(row)
identity=spec_ci.execution_identity(reference,rows,models)
require(identity==reconciliation['execution_identity'],'execution dependencies changed')
bound={}
for group in (campaign['inputs'],reconciliation['inputs'],identity['verified_inputs'],conversion['inputs']):
 for name,sha in group.items():
  require(name not in bound or bound[name]==sha,'conflicting input identity: '+name)
  require(sha256(ROOT/name)==sha,'changed bound input: '+name)
  bound[name]=sha

files={campaign_path,reconciliation_path,conversion_path,aggregate_path,original_path,reference_path,plan_path,
       Path(__file__).resolve(),ROOT/'build/run_xc7_core_corpus.py',ROOT/'build/xc7-core-corpus-driver.log',
       ROOT/'build/xc7-core-reconciliation.log',ROOT/'build/spec-conversion-driver.log',
       ROOT/'third_party/xilinx-unisim/LICENSE',ROOT/'third_party/hardfloat/COPYING.txt'}
for path in (ROOT/'build/xc7-core-corpus').iterdir():
 if path.is_file():files.add(path)
files.update(paths)
for path in models.values():files.add(Path(str(path)+'.build.json'))
allowed={'.v','.sv','.svh','.vh','.vi','.vlt','.ys','.log','.json','.py','.cpp','.hpp','.h','.tcl','.mk','.txt','.wasm'}
test_inputs={ROOT/name for name in conversion['inputs'] if name.startswith('build/spec/') or name.endswith('.wast')}
for row in conversion['suites']:
 fresh=ROOT/conversion['replay_directory']/'fresh'/Path(row['suite']).with_suffix('')/'test.json'
 require(sha256(fresh)==row['fresh_json_sha256'],'fresh conversion JSON changed')
 test_inputs.add(fresh)
 test_inputs.add(ROOT/conversion['replay_directory']/'logs'/Path(row['suite']).with_suffix('.json'))
for name in bound:
 path=ROOT/name
 if path not in test_inputs and (path.suffix in allowed or path.name=='Makefile'):files.add(path)
notices=stage/'notices';notices.mkdir()
for package in ('yosys','verilator','iverilog'):
 source=ROOT/'.cache/tools/usr/share/doc'/package/'copyright'
 target=ROOT/'build/xc7-core-notices'/(package.upper()+'_COPYRIGHT')
 target.parent.mkdir(exist_ok=True);shutil.copyfile(source,target);files.add(target)
for path in (ROOT/'.cache/tools/wasm-tools-1.263.0-x86_64-linux').glob('LICENSE*'):files.add(path)
spec_license=ROOT/'.cache/upstream/spec-6057acdb1a213f85369c64454c078a15f11ac4b1/LICENSE'
files.add(spec_license)
index=[]
for path in sorted(files):
 original_bytes=path.read_bytes();relative=path.relative_to(ROOT);compressed=len(original_bytes)>262144
 archive_relative=Path(str(relative)+'.gz') if compressed else relative
 target=stage/archive_relative;target.parent.mkdir(parents=True,exist_ok=True)
 target.write_bytes(gzip.compress(original_bytes,mtime=0) if compressed else original_bytes)
 require((gzip.decompress(target.read_bytes()) if compressed else target.read_bytes())==original_bytes,'archive differs: '+str(path))
 index.append({'original_path':str(relative),'archive_path':str((destination/archive_relative).relative_to(ROOT)),
  'original_sha256':hashlib.sha256(original_bytes).hexdigest(),'archive_sha256':sha256(target),'compressed':compressed})

container=stage/'conversion-inputs.tar.gz';test_manifest={}
with container.open('wb') as raw,gzip.GzipFile(fileobj=raw,mode='wb',mtime=0,filename='') as compressed,tarfile.open(fileobj=compressed,mode='w|') as archive:
 for path in sorted(test_inputs):
  data=path.read_bytes();name=str(path.relative_to(ROOT));test_manifest[name]=hashlib.sha256(data).hexdigest()
  info=tarfile.TarInfo(name);info.size=len(data);info.mode=0o644;archive.addfile(info,io.BytesIO(data))
with tarfile.open(container) as archive:
 recovered={entry.name:hashlib.sha256(archive.extractfile(entry).read()).hexdigest() for entry in archive if entry.isfile()}
 require(recovered==test_manifest,'converted-input archive differs')
(stage/'conversion-inputs.json').write_text(json.dumps(test_manifest,indent=2)+'\n')
(stage/'index.json').write_text(json.dumps(index,indent=2)+'\n')
summary={'status':'passed','scope':'complete local official corpus on the host-backed Xilinx functional core',
 'suite_files':259,'partitions':16,'worker_limit':8,'elapsed_seconds':campaign['elapsed_seconds'],
 'totals':aggregate['totals'],'exact_native_command_cycles':True,'memory_wait_states':3,
 'native_simulator_sha256':manifests['native']['binary_sha256'],'mapped_simulator_sha256':manifests['mapped']['binary_sha256'],
 'official_sources_sha256':aggregate['official_sources_sha256'],'reconciliation_faults_rejected':28,
 'campaign_inputs_rechecked':len(campaign['inputs']),'execution_dependencies_rechecked':len(identity['verified_inputs']),
 'all_bound_inputs_rechecked':len(bound),'post_run_conversion_audit':{
  'report_sha256':sha256(conversion_path),'suite_files':259,'payload_files':conversion['payload_files'],
  'fault_controls_rejected':13,'existing_cache_unchanged':True,'historical_execution_input_attestation':False},
 'original_aggregate_sha256':sha256(original_path),'reconciled_aggregate_sha256':sha256(aggregate_path),
 'reconciliation_report_sha256':sha256(reconciliation_path),'archive_files':len(index),
 'conversion_archive_entries':len(test_manifest),'conversion_archive_sha256':sha256(container),
 'physical_hardware_tested':False,'xilinx_routing_or_timing_accepted':False,
 'limitations':['Execution uses host-backed memory/runtime services, not the bounded board-system storage.',
  'Validation and embedding assertions are counted separately from RTL execution assertions.',
  'Canonical cycles exclude duplicated setup replay in partitioned workers.',
  'The post-run conversion replay establishes current input consistency; the original runner did not hash every generated input before execution.',
  'Untimed functional primitive models retain the documented X/Z limitations; no physical implementation or exhaustive semantic proof is claimed.']}
for name,sha in bound.items():require(sha256(ROOT/name)==sha,'input changed during archival: '+name)
require({name:build_identity.verify(path) for name,path in models.items()}==manifests,'models changed during archival')
stage.rename(destination)
(ROOT/'docs/verification/xc7-core-corpus-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
for source,name in [(reconciliation_path,'xc7-core-reconciliation.json'),(conversion_path,'spec-conversion.json')]:
 (ROOT/'docs/verification'/name).write_bytes(source.read_bytes())
print('PASS',len(index),'archived artifacts,',len(test_manifest),'test-input archive entries,',len(bound),'bound inputs rechecked')
