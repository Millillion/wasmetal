"""Preserve the complete native run with freshly generated input attestations."""
from pathlib import Path
import gzip,hashlib,io,json,sys,tarfile,tempfile
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
import build_identity,run_spec,spec_ci,spec_inputs
digest=spec_inputs.digest
path=ROOT/'reports/spec-inputs-native-complete.json';report=json.loads(path.read_text())
old_path=ROOT/'reports/core-rounding-wait-3.json';old=json.loads(old_path.read_text());previous={s['suite']:s for s in old['suites']}
source_hash,entries=spec_ci.catalog();spec_ci.validate_reference(report,source_hash,entries)
binary=ROOT/'build/obj/Vwasmetal_core';assert build_identity.verify(binary)==report['build_manifest']
assert report['suite_files']==259 and report['totals']==old['totals'] and report['identity_error'] is None
bound=dict(report['runner_inputs']);bound.update({str(p.relative_to(ROOT)):digest(p) for p in (path,old_path,Path(__file__).resolve(),ROOT/'tools/spec_ci.py')})
files={path,old_path,Path(str(binary)+'.build.json'),ROOT/'build/spec-inputs-native-complete.log',ROOT/'build/spec-inputs-native-progress.json'}
files.update(ROOT/n for n in bound);payloads=set()
for row in report['suites']:
 for field in ('counts','failures','command_count','executed_commands','command_cycles','replayed_setup_commands','replayed_setup_cycles','total_simulated_cycles','fixture_cycles'):
  assert row[field]==previous[row['suite']][field],(row['suite'],field)
 entry=row['test_inputs'];directory=ROOT/entry['directory'];assert digest(directory/'test.json')==entry['json_sha256']
 assert spec_inputs.payloads(directory,entry['identity']['payloads'])==entry['identity']['payloads']
 assert digest(ROOT/entry['conversion_log'])==entry['conversion_log_sha256']
 payloads.update(p for p in directory.iterdir() if p.is_file());payloads.add(ROOT/entry['conversion_log']);payloads.add(run_spec.SPEC/'test/core'/row['suite'])
files.add(run_spec.SPEC/'LICENSE')
for p in (ROOT/'.cache/tools/wasm-tools-1.263.0-x86_64-linux').glob('LICENSE*'):files.add(p)
destination=ROOT/'docs/verification/fresh-native-corpus';assert not destination.exists()
stage=Path(tempfile.mkdtemp(prefix='archive-fresh-native-',dir=ROOT/'build'));index=[]
for p in sorted(files):
 data=p.read_bytes();relative=p.relative_to(ROOT);compressed=len(data)>262144;name=Path(str(relative)+'.gz') if compressed else relative
 target=stage/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(gzip.compress(data,mtime=0) if compressed else data)
 assert (gzip.decompress(target.read_bytes()) if compressed else target.read_bytes())==data
 index.append({'original_path':str(relative),'archive_path':str((destination/name).relative_to(ROOT)),
               'original_sha256':digest(p),'archive_sha256':digest(target),'compressed':compressed})
manifest={};container=stage/'execution-inputs.tar.gz'
with container.open('wb') as raw,gzip.GzipFile(fileobj=raw,mode='wb',filename='',mtime=0) as stream,tarfile.open(fileobj=stream,mode='w|') as archive:
 for p in sorted(payloads):
  data=p.read_bytes();name=str(p.relative_to(ROOT));manifest[name]=hashlib.sha256(data).hexdigest()
  entry=tarfile.TarInfo(name);entry.size=len(data);entry.mode=0o644;archive.addfile(entry,io.BytesIO(data))
with tarfile.open(container) as archive:
 assert {entry.name:hashlib.sha256(archive.extractfile(entry).read()).hexdigest() for entry in archive if entry.isfile()}==manifest
(stage/'execution-inputs.json').write_text(json.dumps(manifest,indent=2)+'\n');(stage/'index.json').write_text(json.dumps(index,indent=2)+'\n')
run_spec.conversion_session().verify_all()
for name,sha in bound.items():assert digest(ROOT/name)==sha,name
for name,sha in manifest.items():assert digest(ROOT/name)==sha,name
summary={'status':'passed','scope':'complete native RTL corpus with fresh test input records','suite_files':259,
         'totals':report['totals'],'memory_wait_states':3,'elapsed_seconds':report['elapsed_seconds'],
         'exact_previous_command_observations':True,'generated_payload_files':sum(len(s['test_inputs']['identity']['payloads']) for s in report['suites']),
         'inputs_verified_before_and_after_execution':True,'publication_replay_passed':True,
         'report_sha256':digest(path),'simulator_sha256':digest(binary),'official_sources_sha256':source_hash,
         'artifact_files':len(index),'execution_input_archive_entries':len(manifest),
         'execution_input_archive_sha256':digest(container),'bound_inputs':bound,
         'fresh_complete_xilinx_rerun_status':'running','physical_hardware_tested':False}
stage.rename(destination)
(ROOT/'docs/verification/fresh-native-corpus.json').write_text(json.dumps(summary,indent=2)+'\n')
print('PASS all 259 native suites, exact prior observations;',len(manifest),'input files archived')
