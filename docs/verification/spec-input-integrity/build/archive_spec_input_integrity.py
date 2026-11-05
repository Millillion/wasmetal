"""Bind the new runner's three-model smoke results to their actual fresh inputs."""
from pathlib import Path
import gzip,hashlib,io,json,sys,tarfile,tempfile
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
import build_identity,run_spec,spec_inputs
from spec_shards import clean_report
digest=spec_inputs.digest
reference_path=ROOT/'reports/core-rounding-wait-3.json'
old={s['suite']:s for s in json.loads(reference_path.read_text())['suites']}
models={'native':ROOT/'build/obj/Vwasmetal_core','ecp5':ROOT/'build/rounding-gate/obj/Vwasmetal_core',
        'xc7':ROOT/'build/xc7-core-sim/obj/Vwasmetal_core'}
files={reference_path,Path(__file__).resolve()};bound={};payloads=set();receipts={}
for label,binary in models.items():
 path=ROOT/'reports'/('spec-inputs-'+label+'-smoke.json');report=json.loads(path.read_text());clean_report(report)
 assert report['suite_files']==8 and report['identity_error'] is None
 assert build_identity.verify(binary)==report['build_manifest']
 assert report['converter_identity']==run_spec.conversion_session().converter
 for name,sha in report['runner_inputs'].items():
  assert digest(ROOT/name)==sha,name;assert name not in bound or bound[name]==sha;bound[name]=sha;files.add(ROOT/name)
 files.update({path,Path(str(binary)+'.build.json'),ROOT/'build'/('spec-inputs-'+label+'-smoke.log')})
 for row in report['suites']:
  source=run_spec.SPEC/'test/core'/row['suite'];target=run_spec.conversion_session().convert(source)
  expected=run_spec.conversion_session().verify(source,target)['identity'];entry=spec_inputs.checked_evidence(row,expected)
  directory=ROOT/entry['directory'];assert digest(directory/'test.json')==entry['json_sha256']
  assert spec_inputs.payloads(directory,expected['payloads'])==expected['payloads']
  assert digest(ROOT/entry['conversion_log'])==entry['conversion_log_sha256']
  for field in ('counts','failures','command_count','executed_commands','command_cycles','replayed_setup_commands','replayed_setup_cycles','total_simulated_cycles','fixture_cycles'):
   assert row[field]==old[row['suite']][field],(label,row['suite'],field)
  payloads.update(p for p in directory.iterdir() if p.is_file());payloads.add(ROOT/entry['conversion_log']);payloads.add(source)
 receipts[label]={'report_sha256':digest(path),'simulator_sha256':digest(binary),'totals':report['totals'],
                  'exact_previous_native_observations':True,'fresh_inputs_rechecked':True}
checks={'faults':15,'ci-fixtures':19,'reconciliation-fixtures':5,'runner-fixtures':2,'partition-fixtures':1}
for label,count in checks.items():
 path=ROOT/'build'/('spec-inputs-'+label+'.log');text=path.read_text();assert f'Ran {count} test' in text and text.rstrip().endswith('OK');files.add(path)
for name in ('tests/spec_inputs_test.py','tests/spec_ci_test.py','tests/spec_reconciliation_test.py',
             'tests/run_spec_runner_test.py','tests/spec_partition_runner_test.py','tools/spec_ci.py','.github/workflows/rtl.yml',
             'build/spec-inputs-workflow-lint.log'):
 files.add(ROOT/name);bound[name]=digest(ROOT/name)
assert not (ROOT/'build/spec-inputs-workflow-lint.log').read_text()
files.add(run_spec.SPEC/'LICENSE')
for path in (ROOT/'.cache/tools/wasm-tools-1.263.0-x86_64-linux').glob('LICENSE*'):files.add(path)
destination=ROOT/'docs/verification/spec-input-integrity';assert not destination.exists()
stage=Path(tempfile.mkdtemp(prefix='archive-spec-inputs-',dir=ROOT/'build'));index=[]
for path in sorted(files):
 data=path.read_bytes();relative=path.relative_to(ROOT);compressed=len(data)>262144
 name=Path(str(relative)+'.gz') if compressed else relative;target=stage/name;target.parent.mkdir(parents=True,exist_ok=True)
 target.write_bytes(gzip.compress(data,mtime=0) if compressed else data)
 assert (gzip.decompress(target.read_bytes()) if compressed else target.read_bytes())==data
 index.append({'original_path':str(relative),'archive_path':str((destination/name).relative_to(ROOT)),
               'original_sha256':digest(path),'archive_sha256':digest(target),'compressed':compressed})
manifest={};container=stage/'execution-inputs.tar.gz'
with container.open('wb') as raw,gzip.GzipFile(fileobj=raw,mode='wb',filename='',mtime=0) as stream,tarfile.open(fileobj=stream,mode='w|') as archive:
 for path in sorted(payloads):
  data=path.read_bytes();name=str(path.relative_to(ROOT));manifest[name]=hashlib.sha256(data).hexdigest()
  entry=tarfile.TarInfo(name);entry.size=len(data);entry.mode=0o644;archive.addfile(entry,io.BytesIO(data))
with tarfile.open(container) as archive:
 assert {entry.name:hashlib.sha256(archive.extractfile(entry).read()).hexdigest() for entry in archive if entry.isfile()}==manifest
(stage/'execution-inputs.json').write_text(json.dumps(manifest,indent=2)+'\n')
(stage/'index.json').write_text(json.dumps(index,indent=2)+'\n')
run_spec.conversion_session().verify_all()
for name,sha in bound.items():assert digest(ROOT/name)==sha,name
for name,sha in manifest.items():assert digest(ROOT/name)==sha,name
summary={'status':'passed','scope':'fresh official input generation, integrity failures and eight-suite three-model regression',
 'models':receipts,'suites_per_model':8,'canonical_cycles_per_model':132959,'rtl_assertions_per_model':6647,
 'validation_assertions_per_model':355,'script_commands_per_model':7326,'fixture_test_counts':checks,
 'ci_input_evidence_corruptions_rejected':24,'converter':run_spec.conversion_session().converter,
 'shared_conversion_cache_reused':False,'generated_inputs_verified_before_and_after_execution':True,
 'artifact_files':len(index),'execution_input_archive_entries':len(manifest),'execution_input_archive_sha256':digest(container),
 'bound_inputs':bound,'complete_native_rerun_status':'running','complete_mapped_rerun_with_new_input_evidence_passed':False,
 'physical_hardware_tested':False,'limitations':['This receipt covers eight suites on each model. Earlier complete-corpus results retain their original runner identities.',
  'The complete native corpus is being rerun; fresh complete mapped campaigns have not yet passed.',
  'Input integrity and regression tests do not establish physical FPGA or ASIC timing.']}
stage.rename(destination)
(ROOT/'docs/verification/spec-input-integrity.json').write_text(json.dumps(summary,indent=2)+'\n')
print('PASS',len(index),'artifacts,',len(manifest),'actual input files, exact three-model observations')
