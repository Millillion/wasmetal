"""Preserve the verified physical-preparation flow and its incomplete experiments."""
from pathlib import Path
import gzip,json,re,shutil,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from prepare_standalone import digest
report_path=ROOT/'reports/asic-physical-startup.json'
cells_path=ROOT/'reports/asic-physical-startup-cells.json'
r=json.loads(report_path.read_text());cells=json.loads(cells_path.read_text())
assert r['status']==cells['status']=='passed'
assert r['backend']=='sky130hd-post-physical-functional'
assert not r['detailed_routing_included'] and not r['physical_timing_accepted'] and not r['physical_hardware_tested']
assert r['negative_controls_rejected']==15 and cells['negative_controls_rejected']==5
assert set(r['standard_cells'])==set(cells['mapped_types_checked'])==set(cells['cell_types'])
assert len(cells['cell_types'])==98
assert r['clock_tree']['flip_flops']==r['proofs']['state_points']==620
assert r['proofs']['inductive_equivalence'] and r['proofs']['reset_base_cycles']==12
base=ROOT/'build/asic-physical-startup';functional=base/'functional'
for name,key in [('mapped.json','netlist_sha256'),('cells.v','functional_models_sha256'),('observations.log','observations_log_sha256')]:assert digest(functional/name)==r[key]
assert digest(functional/'obj/Vwasmetal_startup_sram')==r['binary_sha256']
for name,key in [('equivalence.log','induction_log_sha256'),('reset-points.log','reset_point_log_sha256'),('reset-pins.log','reset_pin_log_sha256'),('equiv.il','comparison_point_model_sha256')]:assert digest(functional/name)==r['proofs'][key]
assert json.loads((functional/'observations.log').read_text())==r['observations']
reference_path=ROOT/'reports/asic-startup.json';reference=json.loads(reference_path.read_text())
assert digest(reference_path)==r['reference_report_sha256'] and digest(cells_path)==r['cell_report_sha256']
expected=next(c for c in reference['checks'] if c['ram_bytes']==131072)['tests']['rtl']['observations']
assert r['observations']==expected and expected['cycles']==50513199
bound=dict(r['inputs'])
for name,sha in cells['inputs'].items():
 assert name not in bound or bound[name]==sha,name
 bound[name]=sha
files={report_path,cells_path,reference_path,Path(__file__).resolve(),ROOT/'.github/workflows/rtl.yml',ROOT/'tests/asic_cell_source_test.py'}
for name,sha in bound.items():
 path=ROOT/name;assert digest(path)==sha,name
 if not name.startswith('.cache/tools/') and '/obj/' not in name:files.add(path)
for path,sha in r['tools']['loaded_libraries'].items():assert digest(Path(path))==sha,path
cellbase=ROOT/'build/asic-physical-startup-cells'
for label,item in [('positive',cells['positive']),*[(c['name'],c) for c in cells['negative_controls']]]:
 for path,key in [(cellbase/('derived.v' if label=='positive' else label+'.v'),'source_sha256'),(cellbase/(label+'.vvp'),'binary_sha256'),(cellbase/(label+'.log'),'log_sha256')]:assert digest(path)==item[key]
assert digest(cellbase/'testbench.sv')==cells['testbench_sha256']
for directory in (base,cellbase,ROOT/'build/asic-startup-physical',ROOT/'build/asic-startup-post-physical'):
 for path in directory.rglob('*'):
  if path.is_file() and not any(part.startswith('obj') for part in path.parts) and path.suffix in {'.v','.sv','.vlt','.ys','.log','.json','.lib','.enc','.il','.py','.vvp','.tcl','.def','.sdc','.odb','.guide','.rpt'}:files.add(path)
for name in ('asic-physical-startup-driver.log','asic-physical-workflow-lint.log','asic-physical-cells-fixtures.log','asic-cell-models-regression-fixtures.log','run_post_physical_state_proof.py'):
 files.add(ROOT/'build'/name)
for name in ('asic-physical-cells-fixtures.log','asic-cell-models-regression-fixtures.log'):
 text=(ROOT/'build'/name).read_text();assert 'Ran 7 tests' in text and 'OK' in text
assert not (ROOT/'build/asic-physical-workflow-lint.log').read_text()
old_log=(ROOT/'build/asic-startup-physical/route.log').read_text()
violations=[int(x) for x in re.findall(r'Number of violations = (\d+)',old_log)]
assert 'TimeoutExpired' in old_log and violations==[6132,3724,3689]
assert not (ROOT/'build/asic-startup-physical/routed.odb').exists()
prototype=json.loads((ROOT/'build/asic-startup-post-physical/observations.log').read_text());assert prototype==expected
summary={'status':'passed','scope':r['scope'],'functional_backend':r['backend'],'cycles':expected['cycles'],
 'functional_cells':sum(r['standard_cells'].values()),'cell_types':len(cells['cell_types']),'flip_flops':620,
 'clock_buffer_depth':[r['clock_tree']['minimum_buffer_depth'],r['clock_tree']['maximum_buffer_depth']],
 'physical_taps_removed_from_functional_model':r['normalization']['physical_taps_removed'],
 'state_and_output_equivalence_points':1267,'induction_steps':1,'independent_reset_base_cycles':12,
 'circuit_fault_controls_rejected':15,'cell_model_faults_rejected':5,
 'combinational_cell_vectors':cells['combinational_vectors'],'flip_flop_transitions':cells['flip_flop_transitions'],
 'flip_flop_seed_and_hold_checks':cells['flip_flop_seed_and_hold_checks'],'source_inventory_fixtures':14,
 'bound_inputs_rechecked':len(bound),'prototype_and_repeatable_flow_observations_match':True,
 'detailed_routing_included_in_functional_pass':False,'physical_timing_accepted':False,'physical_hardware_tested':False,
 'initial_detailed_routing_trial':{'status':'timed-out','limit_seconds':1200,'completed_iteration_violations':violations,
  'accepted_routing_result':False,'final_routed_database_available':False},
 'retained_incomplete_proof_trials':['RTL FSM-encoding comparison crashed Yosys during equiv_make.','The comparison of every shared internal wire exceeded its 600-second limit.'],
 'proof_resolution':'Compare the encoded circuits at every state Q and output port, prove one-step induction and a separate reset base, and independently audit all clock paths.',
 'reference_serialization':'JSON re-emission changes wire aliases. Exact canonical cell-pin incidence is required; a deliberately rewired reference is rejected.',
 'report_sha256':digest(report_path),'cell_report_sha256':digest(cells_path)}
log=(functional/'equivalence.log').read_text();assert '1267 are proven and 0 are unproven' in log
summary_path=ROOT/'reports/asic-physical-startup-summary.json';summary_path.write_text(json.dumps(summary,indent=2)+'\n');files.add(summary_path)
notices=base/'notices';notices.mkdir(exist_ok=True)
for package in ('yosys','iverilog','verilator'):
 path=notices/(package.upper()+'_COPYRIGHT');shutil.copyfile(ROOT/'.cache/tools/usr/share/doc'/package/'copyright',path);files.add(path)
destination=ROOT/'docs/verification/asic-physical-startup';destination.mkdir(parents=True,exist_ok=True)
index=[]
for path in sorted(files):
 raw=path.read_bytes();relative=path.relative_to(ROOT)
 if relative.parts[0]=='.cache':relative=Path('upstream').joinpath(*relative.parts[1:])
 compressed=len(raw)>262144;target=destination/relative
 if compressed:target=Path(str(target)+'.gz')
 target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)
 assert (gzip.decompress(target.read_bytes()) if compressed else target.read_bytes())==raw
 index.append({'original_path':str(path.relative_to(ROOT)),'archive_path':str(target.relative_to(ROOT)),
  'original_sha256':digest(path),'archive_sha256':digest(target),'compressed':compressed})
(destination/'index.json').write_text(json.dumps(index,indent=2)+'\n')
for source,name in [(report_path,'asic-physical-startup'),(cells_path,'asic-physical-startup-cells'),(summary_path,'asic-physical-startup-summary')]:
 (ROOT/'docs/verification'/(name+'.json')).write_bytes(source.read_bytes())
for name,sha in bound.items():assert digest(ROOT/name)==sha,name
print('PASS physical-preparation archive:',len(index),'artifacts;',len(bound),'bound inputs;',sum((ROOT/i['archive_path']).stat().st_size for i in index),'bytes')
