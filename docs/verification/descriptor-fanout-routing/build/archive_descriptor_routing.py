"""Preserve a timed-out route, with its actual frozen inputs and congestion data."""
from pathlib import Path
import csv
import gzip
import json
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from prepare_standalone import digest
from route_reset_experiment import check_inputs, observed_router, prepare, verify_routing_placement

base = ROOT / 'build/descriptor-fanout-route'
receipt = base / 'manifest.json'
report = json.loads(receipt.read_text())
assert report['status'] == 'timed_out' and report['routing_timeout_seconds'] == 7200
assert report['final_input_checks_passed'] and report['structural_equivalence_rechecked']
assert report['original_clock_inputs_unchanged']
assert not any(report[key] for key in ('routing_completed', 'timing_passed',
    'bitstream_round_trip_passed', 'physical_hardware_tested', 'default_board_build_changed'))
assert not any((base / name).exists() for name in ('routed.json', 'design.config',
    'timing.json', 'wasmetal.bit', 'wasmetal.pending.bit'))
check_inputs(report['inputs'])
experiment, candidate, placement = prepare(ROOT / 'build/descriptor-fanout/experiment.json',
                                           ROOT / 'build/reset-replication')
proof = verify_routing_placement(json.loads(placement.read_text()),
    json.loads((base / 'placement-for-routing.json').read_text()), 'router2')
assert all(report['routing_placement'][key] == value for key, value in proof.items())
log = (base / 'routing.log').read_text()
assert observed_router(log) == 'router2'
iterations = [dict(zip(('iteration', 'wires', 'conflicting_wires', 'overuse'), map(int, row)))
    for row in re.findall(r'iter=(\d+) wires=(\d+) overused=(\d+) overuse=(\d+)', log)]
assert len(iterations) == 14 and [row['iteration'] for row in iterations] == list(range(1, 15))
best = min(iterations, key=lambda row: row['conflicting_wires'])
last = iterations[-1]
rankings = {}
for iteration in iterations:
    number = iteration['iteration']
    for kind in ('congestion_by_wiretype', 'utilisation_by_wiretype',
                 'congestion_by_coordinate', 'congestion_by_net'):
        assert (base / f'congestion_{kind}_{number}.csv').is_file()
    if number in (best['iteration'], last['iteration']):
        with (base / f'congestion_congestion_by_net_{number}.csv').open() as stream:
            rows = [{'net': row[0], 'conflicting_wires': int(row[1])} for row in csv.reader(stream)]
        assert len({row['net'] for row in rows}) == len(rows)
        rankings[str(number)] = sorted(rows, key=lambda row: (-row['conflicting_wires'], row['net']))[:20]
summary = {
    'status': 'timed_out', 'routing_timeout_seconds': 7200,
    'elapsed_seconds': report['elapsed_seconds'], 'router': 'router2',
    'iterations': iterations, 'best': best, 'last': last,
    'most_conflicted_nets': rankings,
    'frozen_inputs_rechecked': len(report['inputs']),
    'structural_equivalence_rechecked': True, 'original_clock_inputs_unchanged': True,
    'placement_and_routing_settings_rechecked': True,
    'candidate_sha256': digest(candidate), 'placement_sha256': digest(placement),
    'receipt_sha256': digest(receipt),
    'routing_completed': False, 'timing_passed': False,
    'bitstream_round_trip_passed': False, 'physical_hardware_tested': False,
    'comparison_limit': 'Different placements and routing heuristics are experiments, not an isolated benefit measurement.'
}
summary_path = ROOT / 'reports/descriptor-fanout-routing-summary.json'
summary_path.write_text(json.dumps(summary, indent=2) + '\n')
files = set(path for path in base.iterdir() if path.is_file())
assert len(files) == 59
files.update({Path(__file__).resolve(), summary_path, ROOT / 'build/descriptor-fanout-route-driver.log'})
for name in report['inputs']:
    if name.startswith('tools/'):
        files.add(ROOT / name)
destination = ROOT / 'docs/verification/descriptor-fanout-routing'
destination.mkdir(parents=True, exist_ok=True)
index = []
for path in sorted(files):
    raw = path.read_bytes()
    compressed = len(raw) > 262144
    target = destination / path.relative_to(ROOT)
    if compressed:
        target = Path(str(target) + '.gz')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(gzip.compress(raw, mtime=0) if compressed else raw)
    assert (gzip.decompress(target.read_bytes()) if compressed else target.read_bytes()) == raw
    index.append({'original_path': str(path.relative_to(ROOT)),
        'archive_path': str(target.relative_to(ROOT)),
        'original_sha256': digest(path), 'archive_sha256': digest(target), 'compressed': compressed})
(destination / 'index.json').write_text(json.dumps(index, indent=2) + '\n')
(ROOT / 'docs/verification/descriptor-fanout-routing.json').write_bytes(receipt.read_bytes())
(ROOT / 'docs/verification/descriptor-fanout-routing-summary.json').write_bytes(summary_path.read_bytes())
check_inputs(report['inputs'])
print('PASS routing archive:', len(index), 'artifacts;', len(report['inputs']), 'frozen inputs;',
      sum((ROOT / item['archive_path']).stat().st_size for item in index), 'bytes')
print('Best:', best, 'Last:', last)
