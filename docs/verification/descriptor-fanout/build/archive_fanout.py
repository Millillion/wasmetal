"""Archive the completed descriptor-fanout placement and its structural checks."""
from pathlib import Path
import gzip
import json
import re
import shutil
import sys
ROOT=Path(__file__).resolve().parent.parent
OLD=Path('/tmp/wasmetal-direct-rounding')
sys.path.insert(0,str(ROOT/'tools'))
import route_reset_experiment as routing
from replicate_fanout import CLOCK_PORTS
from prepare_standalone import digest
base=ROOT/'build/descriptor-fanout';path=base/'experiment.json'
experiment,candidate,placement=routing.prepare(path,ROOT/'build/reset-replication')
if not experiment['placement_completed'] or not experiment['final_input_checks_passed'] or experiment['negative_controls_rejected']!=7:
    raise ValueError('unfinished fanout experiment')
preflight_path=ROOT/'build/descriptor-fanout-preflight/manifest.json';preflight=json.loads(preflight_path.read_text())
if preflight['status']!='checked' or not preflight['final_input_checks_passed']:raise ValueError('unfinished route preflight')
routing.check_inputs(preflight['inputs'])
controls_path=ROOT/'reports/routing-placement-driver.json';controls=json.loads(controls_path.read_text())
if controls['status']!='passed' or controls['negative_controls_rejected']!=21:raise ValueError('routing controls incomplete')
routing.check_inputs(controls['inputs'])
fixture_log=ROOT/'build/fanout-fixtures.log'
if 'Ran 6 tests' not in fixture_log.read_text() or '\nOK\n' not in fixture_log.read_text():raise ValueError('independent fixtures incomplete')
oldlog=OLD/'build/reset-replication/placement.log';newlog=base/'placement.log'
def wirelength(p):
    values=re.findall(r'at iteration #\d+: temp = [\d.]+, timing cost = \d+, wirelen = (\d+)',p.read_text())
    if not values:raise ValueError('missing placement wirelength')
    return int(values[-1])
before=wirelength(oldlog);after=wirelength(newlog)
clock_ports={port for cell in json.loads(candidate.read_text())['modules']['wasmetal_loadable_ulx3s']['cells'].values()
             for port in cell['connections'] if cell['port_directions'][port]=='input' and ('CLK' in port.upper() or port in {'WCK','CK'})}
if not clock_ports<=CLOCK_PORTS:raise ValueError('unreviewed clock-port name')
counts={kind:int(value) for kind,value in re.findall(r'^Info:\s+(TRELLIS_COMB|TRELLIS_FF|DP16KD|MULT18X18D):\s+(\d+)/',newlog.read_text(),re.M)}
if counts!={'TRELLIS_COMB':61405,'TRELLIS_FF':6958,'DP16KD':192,'MULT18X18D':26}:raise ValueError('unexpected placed resources')
report={**experiment,'scope':'four descriptor-address bit fanouts with verified LUT substitutions and completed fresh placement',
        'archival_structural_check_passed':True,'source_experiment_sha256':digest(path),
        'placed_resources':counts,'clock_port_inventory':sorted(clock_ports),
        'placement_wirelength_cost':{'baseline':before,'candidate':after,'relative_change_percent':100*(after-before)/before,
            'note':'Placer estimate only; not routed wirelength or evidence of improved routing.'},
        'independent_fixture_tests_passed':6,'fixture_source_sha256':digest(ROOT/'tests/fanout_replication_test.py'),
        'fixture_log_sha256':digest(fixture_log),'route_preflight_sha256':digest(preflight_path),
        'routing_controls_sha256':digest(controls_path),'routing_fault_controls_rejected':21,
        'routing_trial_status_at_capture':'running','routing_completed':False,'timing_passed':False,
        'bitstream_round_trip_passed':False,'physical_hardware_tested':False,'default_board_build_changed':False}
report_path=ROOT/'reports/descriptor-fanout.json';report_path.write_text(json.dumps(report,indent=2)+'\n')
files={path,candidate,placement,newlog,report_path,preflight_path,controls_path,fixture_log,
       ROOT/'build/fanout-route-preflight.log',ROOT/'build/fanout-routing-controls.log',
       ROOT/'build/descriptor-fanout-driver.log',ROOT/'build/fanout-candidates.json',
       ROOT/'build/fanout-selection.json',ROOT/'build/prepare_fanout_baseline.py',
       ROOT/'build/counter-fanout-workflow-lint.log',Path(__file__).resolve(),
       ROOT/'tools/replicate_fanout.py',ROOT/'tools/replicate_reset.py',ROOT/'tools/route_reset_experiment.py',
       ROOT/'tests/fanout_replication_test.py',ROOT/'tools/check_routing_placement.py',
       ROOT/'build/reset-replication/design.json',ROOT/'build/reset-replication/placed.json',
       ROOT/'build/reset-replication/design.manifest.json',ROOT/'build/reset-replication/experiment.json'}
for p in (ROOT/'build/routing-placement-driver').rglob('*'):
    if p.is_file() and p.suffix in {'.json','.log','.py'}:files.add(p)
notices=ROOT/'build/fanout-notices';notices.mkdir(exist_ok=True)
shutil.copyfile(ROOT/'.cache/tools/usr/share/doc/yosys/copyright',notices/'YOSYS_COPYRIGHT');files.add(notices/'YOSYS_COPYRIGHT')
destination=ROOT/'docs/verification/descriptor-fanout';destination.mkdir(parents=True,exist_ok=True);index=[]
pairs=[(p,p.relative_to(ROOT)) for p in files]+[(oldlog,Path('build/reset-replication/placement.log'))]
for p,relative in sorted(pairs,key=lambda pair:str(pair[1])):
    original=p.read_bytes();compressed=len(original)>262144;target=destination/relative
    if compressed:target=Path(str(target)+'.gz')
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(gzip.compress(original,mtime=0) if compressed else original)
    if (gzip.decompress(target.read_bytes()) if compressed else target.read_bytes())!=original:raise ValueError('fanout archive differs')
    index.append({'original_path':str(relative),'archive_path':str(target.relative_to(ROOT)),
                  'original_sha256':digest(p),'archive_sha256':digest(target),'compressed':compressed})
(destination/'index.json').write_text(json.dumps(index,indent=2)+'\n')
(ROOT/'docs/verification/descriptor-fanout.json').write_bytes(report_path.read_bytes())
routing.check_inputs(experiment['inputs']);routing.check_inputs(preflight['inputs'])
print('PASS archived fanout placement',len(index),'artifacts; cost',before,'->',after,
      '; bytes',sum((ROOT/row['archive_path']).stat().st_size for row in index))
