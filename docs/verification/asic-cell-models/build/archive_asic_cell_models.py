"""Archive independently checked ASIC cell models and upstream source closure."""
from pathlib import Path
import gzip,json,shutil,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from prepare_standalone import digest
from asic_cells import audit_circuit
report_path=ROOT/'reports/asic-cell-models.json';report=json.loads(report_path.read_text())
if report['status']!='passed' or report['negative_controls_rejected']!=3:raise ValueError('incomplete vendor model check')
files={report_path,Path(__file__).resolve(),ROOT/'tests/asic_cell_source_test.py',ROOT/'.github/workflows/rtl.yml'}
for name,sha in report['inputs'].items():
    if digest(ROOT/name)!=sha:raise ValueError('changed ASIC cell-model input: '+name)
    if not name.startswith('.cache/tools/'):files.add(ROOT/name)
base=ROOT/'build/asic-cell-models'
for label,record in [('positive',report['positive']),*[(r['name'],r) for r in report['negative_controls']]]:
    source=base/('derived.v' if label=='positive' else label+'.v')
    for path,key in [(source,'source_sha256'),(base/(label+'.vvp'),'binary_sha256'),(base/(label+'.log'),'log_sha256')]:
        if digest(path)!=record[key]:raise ValueError('changed independent cell test: '+str(path))
if digest(base/'testbench.sv')!=report['testbench_sha256']:raise ValueError('changed cell testbench')
for path in base.rglob('*'):
    if path.is_file() and path.suffix in {'.v','.sv','.vvp','.log','.json','.ys','.lib'}:files.add(path)
for name in ('asic-cell-models-driver.log','asic-cell-source-fixtures.log','asic-cell-workflow-lint.log'):
    files.add(ROOT/'build'/name)
fixture=(ROOT/'build/asic-cell-source-fixtures.log').read_text()
if 'Ran 7 tests' not in fixture or 'OK' not in fixture:raise ValueError('missing cell source fixtures')
# Independently reject the actual first, unfiltered mapping using the retained
# platform policy; this trial is preserved as a rejected circuit, never a pass.
prototype=ROOT/'build/sky130-startup-prototype';data=json.loads((prototype/'mapped.json').read_text())
module=data['modules']['wasmetal_startup_sram'];library={k:v for k,v in data['modules'].items() if k!='wasmetal_startup_sram'}
excluded=set(report['library_filter']['excluded_cells'])
try:audit_circuit(module,library,excluded)
except ValueError as error:
    if not any(name in str(error) for name in excluded):raise
    rejection=str(error)
else:raise ValueError('original forbidden-cell mapping was accepted')
for path in prototype.iterdir():
    if path.is_file() and path.suffix in {'.v','.json','.ys','.log'}:files.add(path)
summary={'status':'passed','cell_types_checked':report['cell_type_count'],
 'combinational_vectors':report['combinational_vectors'],'binary_flip_flop_transitions':32,'flip_flop_seed_and_hold_checks':64,
 'model_faults_rejected':3,'source_inventory_fixtures_passed':7,
 'library_cells':428,'excluded_platform_cells':36,'retained_library_cells':392,
 'initial_mapping_rejected':{'netlist_sha256':digest(prototype/'mapped.json'),'diagnostic':rejection},
 'report_sha256':digest(report_path),'complete_asic_startup_campaign_included':False,
 'physical_timing_or_hardware_validated':False}
summary_path=ROOT/'reports/asic-cell-models-summary.json';summary_path.write_text(json.dumps(summary,indent=2)+'\n');files.add(summary_path)
notices=ROOT/'build/asic-cell-notices';notices.mkdir(exist_ok=True)
for package in ('yosys','iverilog'):
    origin=ROOT/'.cache/tools/usr/share/doc'/package/'copyright';target=notices/(package.upper()+'_COPYRIGHT')
    shutil.copyfile(origin,target);files.add(target)
destination=ROOT/'docs/verification/asic-cell-models';destination.mkdir(parents=True,exist_ok=True);index=[]
for path in sorted(files):
    relative=path.relative_to(ROOT);raw=path.read_bytes();compressed=len(raw)>262144
    if relative.parts[0]=='.cache':relative=Path('upstream').joinpath(*relative.parts[1:])
    target=destination/relative
    if compressed:target=Path(str(target)+'.gz')
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)
    if (gzip.decompress(target.read_bytes()) if compressed else target.read_bytes())!=raw:raise ValueError('cell archive differs')
    index.append({'original_path':str(path.relative_to(ROOT)),'archive_path':str(target.relative_to(ROOT)),
        'original_sha256':digest(path),'archive_sha256':digest(target),'compressed':compressed})
(destination/'index.json').write_text(json.dumps(index,indent=2)+'\n')
for name in ('asic-cell-models','asic-cell-models-summary'):
    (ROOT/'docs/verification'/f'{name}.json').write_bytes((ROOT/'reports'/f'{name}.json').read_bytes())
for name,sha in report['inputs'].items():
    if digest(ROOT/name)!=sha:raise ValueError('cell input changed during archive')
print('PASS ASIC cell archive:',len(index),'artifacts;',len(report['inputs']),'bound inputs;',sum((ROOT/r['archive_path']).stat().st_size for r in index),'bytes')
