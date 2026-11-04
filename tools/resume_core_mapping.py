#!/usr/bin/env python3
"""Resume an interrupted complete-cone mapping proof from verified checkpoints.

No synthesis or proof inputs are regenerated. Every saved circuit, solver log
and input identity is rechecked, and the original partition queue is replayed.
Exit 75 means a work interval ended with comparisons still pending; only a
complete proof exits successfully. A timeout or counterexample never passes.
"""
import argparse
from collections import deque
import json
from pathlib import Path
import re
import sys
import time

from prepare_standalone import ROOT, digest
from prove_core_mapping import Aig, compare, verify_hashes


def replay(report):
    total = report['required_observation_bits']; attempts = report['attempts']
    if not attempts or total < 1:
        raise ValueError('checkpoint has no completed comparisons')
    size = len(attempts[0]['indices'])
    if not 1 <= size <= 4096:
        raise ValueError('invalid initial partition size')
    queue = deque([list(range(i, min(i+size, total))) for i in range(0, total, size)])
    proven = set(); unresolved = []
    for attempt in attempts:
        if not queue or queue.popleft() != attempt['indices']:
            raise ValueError('checkpoint partition order or coverage differs')
        indices = attempt['indices']; status = attempt['status']
        if status == 'proven':
            if proven.intersection(indices):
                raise ValueError('duplicate proven observations')
            proven.update(indices)
        elif status == 'inconclusive' and len(indices) > 1:
            half = len(indices)//2; queue.append(indices[:half]); queue.append(indices[half:])
        elif status == 'inconclusive':
            unresolved.append(attempt)
        else:
            raise ValueError('cannot resume a counterexample or unknown solver result')
    if (len(proven) != report['proven_observation_bits'] or
            len(queue) != report['pending_groups'] or unresolved != report['unresolved']):
        raise ValueError('checkpoint coverage summary differs from its comparisons')
    return queue, proven, unresolved


def check_attempt(directory, attempt):
    verify_hashes(attempt['circuits'])
    log = directory/'solver.log'
    if digest(log) != attempt['log_sha256']:
        raise ValueError('saved solver log changed: '+str(log))
    text = log.read_text()
    status = attempt['status']
    if status == 'proven':
        valid = attempt['exit_code'] == 0 and re.search(r'^Networks are equivalent\b', text, re.M)
    elif status == 'counterexample':
        valid = attempt['exit_code'] == 0 and re.search(r'^Networks are NOT EQUIVALENT\b', text, re.M)
    elif status == 'inconclusive':
        valid = attempt['wall_timeout'] or (attempt['exit_code'] == 0 and
            any(word in text.lower() for word in ('timeout', 'timed out', 'undecided')))
    else:
        valid = False
    if not valid:
        raise ValueError('saved solver result does not match its log')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--work-seconds', type=int, default=600)
    args = parser.parse_args()
    if not 1 <= args.work_seconds <= 3600:
        parser.error('invalid work interval')
    directory = args.directory.resolve(); report_path = args.report.resolve()
    report = json.loads(report_path.read_text())
    verify_hashes(report['inputs'])
    queue, proven, unresolved = replay(report)
    observations = directory/'observations.json'
    if digest(observations) != report['observations_sha256']:
        raise ValueError('observation names changed')
    models = [Aig(directory/(name+'.aig')) for name in ('reference', 'candidate')]
    if (models[0].input_names != models[1].input_names or
            models[0].output_names != models[1].output_names or
            models[0].output_names != json.loads(observations.read_text()) or
            len(models[0].outputs) != report['required_observation_bits']):
        raise ValueError('saved AIG interfaces differ')
    if report['negative']['status'] != 'counterexample':
        raise ValueError('missing inverted-output rejection')
    check_attempt(directory/'negative', report['negative'])
    seconds = set()
    for attempt in report['attempts']:
        indices = attempt['indices']
        check_attempt(directory/f'{indices[0]:05}-{indices[-1]:05}', attempt)
        match = re.match(r'&cec -T (\d+) -C 100000 ', attempt['command'][-1])
        if not match:
            raise ValueError('unrecognized saved solver bounds')
        seconds.add(int(match[1]))
    if len(seconds) != 1 or not 1 <= next(iter(seconds)) <= 600:
        raise ValueError('inconsistent saved solver bounds')
    seconds = seconds.pop()
    source = str(Path(__file__).resolve().relative_to(ROOT))
    source_hash = digest(ROOT/source)
    if source in report['inputs'] and report['inputs'][source] != source_hash:
        raise ValueError('resume tool changed during this proof')
    report['inputs'][source] = source_hash
    snapshot = directory/('checkpoint-'+digest(report_path)+'.json')
    if not snapshot.exists():
        snapshot.write_bytes(report_path.read_bytes())
    report['inputs'][str(snapshot.relative_to(ROOT))] = digest(snapshot)
    report.setdefault('resumptions', []).append({'checkpoint': str(snapshot.relative_to(ROOT)),
        'verified_completed_attempts': len(report['attempts']), 'work_seconds': args.work_seconds})
    report['status'] = 'running'; start = time.monotonic(); previous_elapsed = report['elapsed_seconds']
    report_path.write_text(json.dumps(report, indent=2)+'\n')
    print(f'Resumed {len(proven)}/{len(models[0].outputs)} proven bits; {len(queue)} groups pending', flush=True)
    while queue and time.monotonic()-start < args.work_seconds:
        indices = queue.popleft(); name = f'{indices[0]:05}-{indices[-1]:05}'
        result = compare(directory/name, models, indices, seconds); report['attempts'].append(result)
        if result['status'] == 'proven':
            if proven.intersection(indices):
                raise ValueError('duplicate proven observations')
            proven.update(indices)
        elif result['status'] == 'inconclusive' and len(indices) > 1:
            half = len(indices)//2; queue.append(indices[:half]); queue.append(indices[half:])
        else:
            unresolved.append(result)
        report.update(proven_observation_bits=len(proven), pending_groups=len(queue), unresolved=unresolved,
            elapsed_seconds=previous_elapsed+time.monotonic()-start)
        report_path.write_text(json.dumps(report, indent=2)+'\n')
        print(f'{name}: {result["status"]}; {len(proven)}/{len(models[0].outputs)} bits proven', flush=True)
        if result['status'] == 'counterexample':
            break
    verify_hashes(report['inputs'])
    passed = proven == set(range(len(models[0].outputs))) and not unresolved and not queue
    counterexample = any(item['status'] == 'counterexample' for item in unresolved)
    report.update(status='passed' if passed else 'counterexample' if counterexample else 'checkpoint' if queue else 'inconclusive',
        complete_boundary_comparison_proven=passed)
    report_path.write_text(json.dumps(report, indent=2)+'\n')
    if passed:
        print('PASS all original CPU logic cones; no internal combinational assumptions', flush=True)
    elif queue and not counterexample:
        print('CHECKPOINT: comparisons remain; this is not a completed proof', flush=True)
        sys.exit(75)
    else:
        raise RuntimeError('complete boundary equivalence not established')


if __name__ == '__main__':
    main()
