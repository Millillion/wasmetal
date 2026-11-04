#!/usr/bin/env python3
"""Compare every original CPU boundary together with ABC's classic CEC engine.

Consumes the identified circuits from prove_core_mapping.py without introducing
any further cut points. An interrupted or partial run never establishes a proof.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import time

import cad
from prepare_standalone import ROOT, digest
from prove_core_mapping import Aig, verify_hashes
from resume_core_mapping import check_attempt, replay


def compare(paths, directory, seconds, conflicts, negative=False):
    command = cad.command('yosys-abc')+['-c',
        f'cec -n -T {seconds} -C {conflicts} {paths[0]} {paths[1]}']
    log = directory/('negative.log' if negative else 'positive.log')
    started = time.monotonic(); timeout = False
    with log.open('w') as stream:
        try:
            run = subprocess.run(command, cwd=directory, env=cad.environment(),
                stdout=stream, stderr=subprocess.STDOUT, timeout=seconds*3+60)
            code = run.returncode
        except subprocess.TimeoutExpired:
            timeout = True; code = None
    text = log.read_text()
    if code == 0 and re.search(r'^Networks are equivalent\b', text, re.M):
        status = 'proven'
    elif code == 0 and re.search(r'^Networks are NOT EQUIVALENT\b', text, re.M):
        status = 'counterexample'
    elif timeout or (code == 0 and any(s in text.lower() for s in ('timeout', 'timed out', 'undecided'))):
        status = 'inconclusive'
    else:
        raise ValueError('unrecognized classic CEC result: '+str(log))
    return {'status': status, 'command': command, 'exit_code': code, 'wall_timeout': timeout,
        'elapsed_seconds': time.monotonic()-started, 'log_sha256': digest(log),
        'circuits': {str(p.relative_to(ROOT)): digest(p) for p in paths}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-directory', type=Path, required=True)
    parser.add_argument('--checkpoint', type=Path, required=True)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--seconds', type=int, default=180)
    parser.add_argument('--conflicts', type=int, default=1000000)
    args = parser.parse_args()
    if not 1 <= args.seconds <= 600 or not 1 <= args.conflicts <= 10000000:
        parser.error('invalid solver bounds')
    args.report.unlink(missing_ok=True)
    source = args.source_directory.resolve(); directory = args.directory.resolve()
    directory.mkdir(exist_ok=True, parents=True)
    data = args.checkpoint.read_bytes(); checkpoint = json.loads(data)
    verify_hashes(checkpoint['inputs']); replay(checkpoint)
    if checkpoint['negative']['status'] != 'counterexample' or not checkpoint['primitive_configuration_mutation_rejected']:
        raise ValueError('missing boundary-generation negative controls')
    check_attempt(source/'negative', checkpoint['negative'])
    paths = [source/(label+'.aig') for label in ('reference', 'candidate')]
    for p in paths:
        if checkpoint['inputs'].get(str(p.relative_to(ROOT))) != digest(p):
            raise ValueError('original complete circuit is not identified by the checkpoint')
    models = [Aig(path) for path in paths]
    observations = source/'observations.json'
    if digest(observations) != checkpoint['observations_sha256']:
        raise ValueError('original boundary names changed')
    if (models[0].input_names != models[1].input_names or
            models[0].output_names != models[1].output_names or
            models[0].output_names != json.loads(observations.read_text()) or
            len(models[0].outputs) != checkpoint['required_observation_bits'] or
            models[0].inputs != checkpoint['primary_and_abstract_input_bits']):
        raise ValueError('original complete circuit interfaces differ')
    snapshot = directory/'source-checkpoint.json'; snapshot.write_bytes(data)
    inputs = {**checkpoint['inputs'], **{str(p.relative_to(ROOT)): digest(p) for p in
        (snapshot, Path(__file__).resolve(), ROOT/'tools/resume_core_mapping.py')}}
    negative = directory/'inverted-candidate.aig'
    models[1].subset(negative, list(range(len(models[1].outputs))), invert=True)
    inputs[str(negative.relative_to(ROOT))] = digest(negative)
    result = {'status': 'running', 'scope': 'all complete logic cones between two CPU technology mappings; matched storage and DSP primitives abstracted',
        'inputs': inputs, 'boundaries': checkpoint['boundaries'],
        'primary_and_abstract_input_bits': models[0].inputs,
        'required_observation_bits': len(models[0].outputs), 'complete_boundary_comparison_proven': False,
        'whole_mapping_equivalence_proven': False, 'physical_hardware_tested': False}
    args.report.parent.mkdir(exist_ok=True, parents=True)
    args.report.write_text(json.dumps(result, indent=2)+'\n')
    result['negative'] = compare([paths[0], negative], directory, args.seconds, args.conflicts, True)
    if result['negative']['status'] != 'counterexample':
        raise ValueError('classic CEC did not reject the inverted original output')
    print('PASS classic CEC rejects inverted output with the complete original interface', flush=True)
    result['positive'] = compare(paths, directory, args.seconds, args.conflicts)
    verify_hashes(inputs)
    result['status'] = 'passed' if result['positive']['status'] == 'proven' else result['positive']['status']
    result['complete_boundary_comparison_proven'] = result['status'] == 'passed'
    args.report.write_text(json.dumps(result, indent=2)+'\n')
    if result['status'] != 'passed':
        raise RuntimeError('complete classic CEC comparison not proven: '+result['status'])
    print(f'PASS all {len(models[0].outputs)} original boundary bits in one classic CEC comparison', flush=True)


if __name__ == '__main__':
    main()
