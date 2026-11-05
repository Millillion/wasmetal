"""Preserve completed routing and the remaining extracted physical failures."""
from pathlib import Path
import gzip,json,re,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from prepare_standalone import digest
from asic_cells import connectivity
route=ROOT/'build/asic-routing-extended';extraction=ROOT/'build/asic-routing-extraction'
r=json.loads((route/'status.json').read_text());e=json.loads((extraction/'status.json').read_text());c=json.loads((route/'connectivity.json').read_text())
assert r['status']=='zero-router-markers' and r['drc_report_markers']==0 and r['inputs_unchanged']
assert e['status']=='diagnostic-completed' and e['inputs_unchanged'] and len(e['physical_reconciliation_faults'])==4
assert (route/'drc.rpt').read_bytes()==b'' and c['exact_pre_route_connectivity']
bound={}
for group in (r['inputs'],e['inputs'],c['inputs']):
 for name,sha in group.items():
  assert name not in bound or bound[name]==sha,name
  assert digest(ROOT/name)==sha,name;bound[name]=sha
for base,record in ((route,r),(extraction,e)):
 for name,sha in record['artifacts'].items():assert digest(base/name)==sha,name
for name,sha in e['tools']['loaded_libraries'].items():assert digest(Path(name))==sha,name
actual=json.loads((route/'routed-functional.json').read_text())['modules']['wasmetal_startup_sram']
reference=json.loads((ROOT/'build/asic-physical-startup/functional/mapped.json').read_text())['modules']['wasmetal_startup_sram']
assert connectivity(actual)==connectivity(reference)
log=(extraction/'extract.log').read_text();setup=float(re.search(r'worst slack max ([-\d.]+)',log).group(1));hold=float(re.search(r'worst slack min ([-\d.]+)',log).group(1))
nets=int(re.search(r'Found (\d+) net violations',log).group(1));pins=int(re.search(r'Found (\d+) pin violations',log).group(1))
assert setup==75.045525 and hold==-0.008133 and (nets,pins)==(139,148)
assert not (extraction/'electrical.rpt').read_text().strip()
summary={'status':'routed-with-open-physical-checks','scope':'startup/BIST/SRAM-adapter block; no CPU or SRAM array',
 'functional_cells':4183,'physical_taps':1070,'exact_pre_route_logical_connectivity':True,
 'completed_iteration_violations':r['completed_iteration_violations'],'router_drc_markers':0,
 'routing_seconds':r['elapsed_seconds'],'extracted_nets':4419,'resistance_segments':24009,'ground_capacitances':24009,'coupling_capacitances':53034,
 'clock_period_ns':100,'library_corner':'SKY130HD TT 1.8V 25C','setup_slack_ns':setup,'hold_slack_ns':hold,
 'selected_electrical_report_empty':True,'antenna_net_violations':nets,'antenna_pin_violations':pins,
 'setup_passes_at_trial_corner':True,'hold_passes_at_trial_corner':False,'antenna_check_passed':False,
 'physical_timing_accepted':False,'signoff_drc_lvs_passed':False,'physical_hardware_tested':False,
 'route_report_sha256':digest(route/'status.json'),'extraction_report_sha256':digest(extraction/'status.json'),
 'bound_inputs_rechecked':len(bound),'physical_tool_reconciliation_faults_rejected':4,
 'unexecuted_python_snapshot_drift':e['unexecuted_test_tool_snapshot_drift'],
 'extraction_rules':{'repository':'The-OpenROAD-Project/OpenROAD-flow-scripts','revision':'d056a2b304182bf76ff10653531165b1dd9848d4',
  'requested_path':'flow/platforms/sky130hd/rcx_patterns.rules','symlink_git_blob':'7f7fe1ca664a2950c2ba447eaf2b8d39431b89cb',
  'resolved_path':'flow/platforms/sky130hs/rcx_patterns.rules','content_git_blob':'af5cfffd6f7d0699510bfba58f352d8feb71fadf',
  'sha256':'d5bd9b1077ceac9929416abca272a6d52e51cd9a575453a31d129817bb286476'},
 'limitations':['Zero OpenROAD routing markers does not establish signoff DRC/LVS or an antenna pass.',
  'Timing uses one nominal cell corner and the trial block-interface constraints, without a physical SRAM or pad implementation.',
  'The original broad Python-import snapshot changed only in unexecuted Wasm input code; physical binaries, package trees, runtime libraries, launcher code and platform data match.',
  'The initial extraction driver rejected that snapshot difference; its source and rejection are retained.']}
summary_path=ROOT/'reports/asic-route-extraction-summary.json';summary_path.write_text(json.dumps(summary,indent=2)+'\n')
files={summary_path,Path(__file__).resolve(),ROOT/'build/run_asic_route_extension.py',ROOT/'build/run_asic_route_extraction.py',
       ROOT/'build/asic-routing-extended-driver.log',ROOT/'build/asic-routing-extraction-driver.log',
       ROOT/'.cache/sky130hd/ORFS_LICENSE',ROOT/'.cache/sky130hd/SKYWATER_LICENSE'}
for base in (route,extraction):files.update(p for p in base.iterdir() if p.is_file())
for name in bound:
 path=ROOT/name
 if not name.startswith('.cache/asic-tools/') and path.suffix not in {'.deb'}:files.add(path)
# Preserve the one changed pre-routing Python source from its immutable archive.
old_source=ROOT/'docs/verification/xc7-core-corpus/tools/run_spec.py'
assert digest(old_source)==r['tools']['inputs']['tools/run_spec.py'];files.add(old_source)
destination=ROOT/'docs/verification/asic-route-extraction';assert not destination.exists();destination.mkdir()
index=[]
for path in sorted(files):
 data=path.read_bytes();relative=path.relative_to(ROOT);compressed=len(data)>262144
 target=destination/(str(relative)+('.gz' if compressed else ''));target.parent.mkdir(parents=True,exist_ok=True)
 target.write_bytes(gzip.compress(data,mtime=0) if compressed else data)
 assert (gzip.decompress(target.read_bytes()) if compressed else target.read_bytes())==data
 index.append({'original_path':str(relative),'archive_path':str(target.relative_to(ROOT)),
  'original_sha256':digest(path),'archive_sha256':digest(target),'compressed':compressed})
(destination/'index.json').write_text(json.dumps(index,indent=2)+'\n')
(ROOT/'docs/verification/asic-route-extraction-summary.json').write_bytes(summary_path.read_bytes())
for name,sha in bound.items():assert digest(ROOT/name)==sha,name
print('PASS preserved',len(index),'artifacts;',len(bound),'bound inputs; routing is clear but hold/antenna checks fail')
