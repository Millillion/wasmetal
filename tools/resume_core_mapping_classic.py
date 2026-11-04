#!/usr/bin/env python3
"""Finish verified CPU mapping obligations with bounded classic CEC batches.

The original proven observations remain checked evidence. Each new comparison
retains all original AIG gates and inputs. No logic node becomes an assumption.
Exit 75 is a checkpoint, never a completed proof.
"""
import argparse
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import fcntl
import json
from pathlib import Path
import re
import sys
import time

from prepare_standalone import ROOT, digest
from prove_core_mapping import Aig, verify_hashes
from prove_core_mapping_classic import compare
from resume_core_mapping import check_attempt, replay


def coverage(total, inherited, attempts, group):
    if total < 1 or not 1 <= group <= 256 or any(type(i) is not int or not 0 <= i < total for i in inherited):
        raise ValueError('invalid original proof coverage')
    queue = deque()
    for begin in range(0, total, group):
        indices = [i for i in range(begin, min(begin+group, total)) if i not in inherited]
        if indices:
            queue.append(indices)
    proven = set(inherited); unresolved = []
    for attempt in attempts:
        if not queue or queue.popleft() != attempt['indices']:
            raise ValueError('classic proof partition order differs')
        indices = attempt['indices']; status = attempt['status']
        if status == 'proven':
            if proven.intersection(indices):
                raise ValueError('classic proof double-counted observations')
            proven.update(indices)
        elif status == 'inconclusive' and len(indices) > 1:
            half = len(indices)//2; queue.append(indices[:half]); queue.append(indices[half:])
        elif status == 'inconclusive':
            unresolved.append(attempt)
        else:
            raise ValueError('counterexample or unknown classic proof status')
    return queue, proven, unresolved


def check_classic(directory, attempt, negative=False):
    verify_hashes(attempt['circuits'])
    log = directory/('negative.log' if negative else 'positive.log')
    if digest(log) != attempt['log_sha256']:
        raise ValueError('classic solver log changed')
    text = log.read_text(); status = attempt['status']
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
        raise ValueError('classic proof status does not match solver output')


def save(path, record):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(record, indent=2)+'\n'); temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-directory', type=Path, required=True)
    parser.add_argument('--source-checkpoint', type=Path, required=True)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--work-seconds', type=int, default=600)
    parser.add_argument('--solver-seconds', type=int, default=30)
    parser.add_argument('--group-size', type=int, default=64)
    parser.add_argument('--jobs', type=int, choices=(1,2), default=2)
    args = parser.parse_args()
    if not 1 <= args.work_seconds <= 1800 or not 1 <= args.solver_seconds <= 180 or not 1 <= args.group_size <= 256:
        parser.error('invalid solver or work bounds')
    source = args.source_directory.resolve(); directory = args.directory.resolve()
    directory.mkdir(parents=True, exist_ok=True); args.report.parent.mkdir(parents=True, exist_ok=True)
    lock = (directory/'run.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    snapshot = directory/'source-checkpoint.json'
    existing = json.loads(args.report.read_text()) if args.report.exists() else None
    if existing:
        verify_hashes(existing['inputs'])
        if (existing['group_size'] != args.group_size or existing['solver_seconds'] != args.solver_seconds or
                existing['source_directory'] != str(source.relative_to(ROOT))):
            raise ValueError('classic proof configuration changed')
    else:
        snapshot.write_bytes(args.source_checkpoint.read_bytes())
    baseline = json.loads(snapshot.read_text()); verify_hashes(baseline['inputs'])
    _, inherited, _ = replay(baseline)
    check_attempt(source/'negative', baseline['negative'])
    if baseline['negative']['status'] != 'counterexample' or not baseline['primitive_configuration_mutation_rejected']:
        raise ValueError('missing original boundary negative controls')
    for attempt in baseline['attempts']:
        indices = attempt['indices']
        check_attempt(source/f'{indices[0]:05}-{indices[-1]:05}', attempt)
    paths = [source/(label+'.aig') for label in ('reference', 'candidate')]
    for path in paths:
        if baseline['inputs'].get(str(path.relative_to(ROOT))) != digest(path):
            raise ValueError('original complete circuit identity differs')
    models = [Aig(path) for path in paths]; total = baseline['required_observation_bits']
    names = source/'observations.json'
    if (digest(names) != baseline['observations_sha256'] or models[0].input_names != models[1].input_names or
            models[0].output_names != models[1].output_names or models[0].output_names != json.loads(names.read_text()) or
            len(models[0].outputs) != total or models[0].inputs != baseline['primary_and_abstract_input_bits']):
        raise ValueError('original AIG boundaries differ')
    input_files = [snapshot, Path(__file__).resolve(), ROOT/'tools/prove_core_mapping_classic.py',
        ROOT/'tools/resume_core_mapping.py']
    inputs = {**baseline['inputs'], **{str(p.relative_to(ROOT)): digest(p) for p in input_files}}
    if existing:
        record = existing
        if record['inputs'] != inputs or record['inherited_proven_bits'] != len(inherited):
            raise ValueError('classic proof source or inherited coverage changed')
        check_classic(directory/'negative', record['negative'], True)
        for attempt in record['attempts']:
            indices = attempt['indices']
            check_classic(directory/f'{indices[0]:05}-{indices[-1]:05}', attempt)
    else:
        negative_dir = directory/'negative'; negative_dir.mkdir(exist_ok=True)
        negative_path = negative_dir/'inverted.aig'
        models[1].subset(negative_path, list(range(total)), invert=True)
        negative = compare([paths[0], negative_path], negative_dir, args.solver_seconds, 100000, True)
        if negative['status'] != 'counterexample':
            raise ValueError('classic CEC failed its complete-interface negative control')
        record = {'status': 'running', 'scope': 'complete CPU mapping cones; inherited checked proofs plus classic CEC on remaining observations',
            'source_directory': str(source.relative_to(ROOT)), 'inputs': inputs, 'boundaries': baseline['boundaries'],
            'inherited_proven_bits': len(inherited), 'required_observation_bits': total,
            'primary_and_abstract_input_bits': models[0].inputs, 'group_size': args.group_size,
            'solver_seconds': args.solver_seconds, 'negative': negative, 'attempts': [],
            'proven_observation_bits': len(inherited), 'unresolved': [], 'elapsed_seconds': 0,
            'whole_mapping_equivalence_proven': False, 'physical_hardware_tested': False}
        record['pending_groups'] = len(coverage(total, inherited, [], args.group_size)[0])
    if record['negative']['status'] != 'counterexample':
        raise ValueError('missing classic negative control')
    queue, proven, unresolved = coverage(total, inherited, record['attempts'], args.group_size)
    if len(proven) != record['proven_observation_bits'] or len(queue) != record['pending_groups'] or unresolved != record['unresolved']:
        raise ValueError('classic checkpoint coverage summary differs')
    record.update(status='running', complete_boundary_comparison_proven=False)
    save(args.report, record)
    started = time.monotonic(); previous = record['elapsed_seconds']
    print(f'Classic CEC: {len(proven)}/{total} verified bits, {len(queue)} groups pending', flush=True)

    def run(indices):
        work = directory/f'{indices[0]:05}-{indices[-1]:05}'; work.mkdir(exist_ok=True)
        selected = [work/(label+'.aig') for label in ('reference', 'candidate')]
        for model, path in zip(models, selected):
            model.subset(path, indices)
        result = compare(selected, work, args.solver_seconds, 100000)
        return dict(result, indices=indices)

    failed = False
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        while queue and time.monotonic()-started < args.work_seconds:
            # Record in queue order, even when the second solver finishes first.
            # A checkpoint retains unfinished groups; no proof result is implied.
            batch = list(queue)[:args.jobs]; futures = [executor.submit(run, indices) for indices in batch]
            for indices, future in zip(batch, futures):
                result = future.result()
                if queue.popleft() != indices:
                    raise ValueError('parallel solver changed partition order')
                record['attempts'].append(result)
                if result['status'] == 'proven':
                    if proven.intersection(indices):
                        raise ValueError('duplicate classic proof coverage')
                    proven.update(indices)
                elif result['status'] == 'inconclusive' and len(indices) > 1:
                    half = len(indices)//2; queue.append(indices[:half]); queue.append(indices[half:])
                else:
                    unresolved.append(result)
                record.update(proven_observation_bits=len(proven), pending_groups=len(queue), unresolved=unresolved,
                    elapsed_seconds=previous+time.monotonic()-started)
                save(args.report, record)
                print(f'{indices[0]:05}-{indices[-1]:05}: {result["status"]}; {len(proven)}/{total} bits', flush=True)
                failed |= result['status'] == 'counterexample'
            if failed:
                break
    verify_hashes(inputs)
    complete = proven == set(range(total)) and not queue and not unresolved
    record.update(status='passed' if complete else 'counterexample' if failed else 'checkpoint' if queue else 'inconclusive',
        complete_boundary_comparison_proven=complete)
    save(args.report, record)
    if complete:
        print(f'PASS all {total} original CPU boundary bits with no additional assumptions', flush=True)
    elif queue and not failed:
        print('CHECKPOINT: remaining comparisons are not proven', flush=True); sys.exit(75)
    else:
        raise RuntimeError('complete CPU mapping proof remains unestablished')


if __name__ == '__main__':
    main()
