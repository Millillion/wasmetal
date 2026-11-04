"""Record the completed routing timeout from its unchanged frozen worktree."""
from pathlib import Path
import datetime
import gzip
import json
import re
import sys

WORK=Path(__file__).resolve().parent.parent
FROZEN=Path('/tmp/wasmetal-direct-rounding')
sys.path.insert(0,str(FROZEN/'tools'))
import route_reset_experiment as routing
from prepare_standalone import digest
base=FROZEN/'build/reset-replication-router2-alternate'
manifest=json.loads((base/'manifest.json').read_text())
assert manifest['status']=='timed_out' and manifest['final_input_checks_passed']
assert not manifest['routing_completed'] and not manifest['timing_passed'] and not manifest['bitstream_round_trip_passed']
assert manifest['router']=='router2' and manifest['observed_router']=='router2' and manifest['alternate_weights']
routing.check_inputs(manifest['inputs'])
experiment,candidate,placement=routing.prepare(FROZEN/'build/reset-replication/experiment.json',FROZEN/'build/loadable-ulx3s')
proof=routing.verify_routing_placement(json.loads(placement.read_text()),
    json.loads((base/'placement-for-routing.json').read_text()),'router2',True)
assert all(manifest['routing_placement'][k]==v for k,v in proof.items())
assert digest(placement)==manifest['routing_placement']['original_sha256']
assert digest(base/'placement-for-routing.json')==manifest['routing_placement']['replay_sha256']
log=(base/'routing.log').read_text()
rows=[dict(zip(('iteration','used_wires','conflicting_wires','total_overuse'),map(int,values)))
      for values in re.findall(r'iter=(\d+) wires=(\d+) overused=(\d+) overuse=(\d+)',log)]
assert rows and not (base/'wasmetal.bit').exists()
best=min(rows,key=lambda row:row['conflicting_wires']);last=rows[-1]
report={**manifest,'captured_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope':'alternate router2 congestion weights on the same verified programmable placement',
        'original_manifest_sha256':digest(base/'manifest.json'),'routing_log_sha256':digest(base/'routing.log'),
        'archival_input_checks_passed':True,'archival_structural_equivalence_rechecked':True,
        'verified_input_count':len(manifest['inputs']),'completed_iterations':len(rows),
        'iteration_observations':rows,'best_observed':best,'last_observed':last,
        'limitations':['Routing did not finish; remaining conflict counts do not establish routability.',
            'No routed timing result, bitstream round trip or physical-board test.',
            'The unrelated ROM-system CI route is a different circuit and is not a controlled comparison.']}
report_path=WORK/'reports/reset-replication-router2-alternate-timeout.json'
report_path.write_text(json.dumps(report,indent=2)+'\n')
files=[base/'manifest.json',base/'routing.log',FROZEN/'build/reset-alternate-route-driver.log',
       FROZEN/'build/reset-replication/experiment.json',FROZEN/'tools/route_reset_experiment.py',
       FROZEN/'tools/replicate_reset.py']
for iteration in {best['iteration'],last['iteration']}:
    files.extend(sorted(base.glob(f'*_{iteration}.csv')))
destination=WORK/'docs/verification/reset-routing-alternate-timeout';destination.mkdir(parents=True,exist_ok=True)
index=[]
for path,relative in [(p,p.relative_to(FROZEN)) for p in files]+[(report_path,report_path.relative_to(WORK)),(Path(__file__).resolve(),Path(__file__).resolve().relative_to(WORK))]:
    original=path.read_bytes();compressed=len(original)>262144;target=destination/relative
    if compressed:target=Path(str(target)+'.gz')
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(gzip.compress(original,mtime=0) if compressed else original)
    if (gzip.decompress(target.read_bytes()) if compressed else target.read_bytes())!=original:raise ValueError('routing archive mismatch')
    index.append({'original_path':str(relative),'archive_path':str(target.relative_to(WORK)),
                  'original_sha256':digest(path),'archive_sha256':digest(target),'compressed':compressed})
(destination/'index.json').write_text(json.dumps(index,indent=2)+'\n')
(WORK/'docs/verification/reset-replication-router2-alternate-timeout.json').write_bytes(report_path.read_bytes())
routing.check_inputs(manifest['inputs'])
print('PASS archival checks for the incomplete route:',len(index),'artifacts;',len(manifest['inputs']),'inputs;',
      'best',best['conflicting_wires'],'last',last['conflicting_wires'],'conflicting wires')
