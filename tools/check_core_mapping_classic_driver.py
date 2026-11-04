#!/usr/bin/env python3
"""Check inherited proof coverage, classic CEC and resumable batch bookkeeping."""
import copy
import json
from pathlib import Path
import subprocess
import sys

import cad
from prepare_standalone import ROOT, digest
from prove_core_mapping import Aig, compare as original_compare, cut
from prove_core_mapping_classic import compare
from resume_core_mapping_classic import coverage, check_classic


def main():
    directory = ROOT/'build/core-classic-driver'; directory.mkdir(parents=True, exist_ok=True)
    report = ROOT/'reports/core-classic-driver.json'; report.unlink(missing_ok=True)
    paths = [Path(__file__).resolve(), ROOT/'tools/prove_core_mapping.py',
        ROOT/'tools/resume_core_mapping.py', ROOT/'tools/prove_core_mapping_classic.py',
        ROOT/'tools/resume_core_mapping_classic.py', ROOT/'tools/cad.py',
        ROOT/'tools/prepare_standalone.py', cad.SUITE/'libexec/yosys-abc']
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in paths}
    source = directory/'original'; source.mkdir(exist_ok=True)
    data = b'aig 3 2 0 3 1\n6\n7\n1\n'+bytes([2,2])+b'i0 a\ni1 b\no0 both\no1 either_not\no2 true\nc\nfixture\n'
    models = []
    for label in ('reference', 'candidate'):
        path = source/(label+'.aig'); path.write_bytes(data); models.append(Aig(path))
    observations = source/'observations.json'; observations.write_text(json.dumps(models[0].output_names))
    original = original_compare(source/'00000-00001', models, [0,1], 5)
    negative = original_compare(source/'negative', models, [0], 5, negative=True)
    if original['status'] != 'proven' or negative['status'] != 'counterexample':
        raise ValueError('known original solver fixture failed')
    rejected = []
    def reject(name, action):
        try:
            action()
        except ValueError as error:
            rejected.append({'name': name, 'reason': str(error)})
        else:
            raise ValueError('classic driver accepted '+name)
    module = {'ports': {}, 'cells': {'register': {'type': 'TRELLIS_FF',
        'parameters': {'REGSET': 'RESET'}, 'port_directions': {'D': 'input', 'Q': 'output'},
        'connections': {'D': [1], 'Q': [2]}}}, 'netnames': {}}
    changed = copy.deepcopy(module); changed['cells']['register']['parameters']['REGSET'] = 'SET'
    reject('changed abstract primitive configuration', lambda: cut([module, changed]))
    baseline = {'status': 'checkpoint', 'required_observation_bits': 3,
        'primary_and_abstract_input_bits': 2, 'attempts': [original], 'negative': negative,
        'proven_observation_bits': 2, 'pending_groups': 1, 'unresolved': [],
        'primitive_configuration_mutation_rejected': True,
        'observations_sha256': digest(observations), 'boundaries': {'synthetic_fixture': True},
        'inputs': {**hashes, **{str(p.relative_to(ROOT)): digest(p) for p in source.glob('*.aig')}}}
    checkpoint = source/'checkpoint.json'; checkpoint.write_text(json.dumps(baseline, indent=2)+'\n')
    completed = directory/'completed.json'; completed.unlink(missing_ok=True)
    command = [sys.executable, str(ROOT/'tools/resume_core_mapping_classic.py'),
        '--source-directory', str(source), '--source-checkpoint', str(checkpoint),
        '--directory', str(directory/'resumed'), '--report', str(completed),
        '--solver-seconds', '5', '--work-seconds', '30']
    for label in ('initial', 'repeat-completed'):
        with (directory/(label+'.log')).open('w') as log:
            subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=90)
        record = json.loads(completed.read_text())
        if record['status'] != 'passed' or record['proven_observation_bits'] != 3 or len(record['attempts']) != 1:
            raise ValueError('classic completion or repeated verification differs')
    # A classic negative result must not be accepted after changing its label.
    inversion = directory/'inverted'; inversion.mkdir(exist_ok=True)
    altered = inversion/'candidate.aig'; models[1].subset(altered, [0,1,2], invert=True)
    result = compare([source/'reference.aig', altered], inversion, 5, 100000, True)
    if result['status'] != 'counterexample':
        raise ValueError('classic CEC accepted a known inverted output')
    check_classic(inversion, result, True)
    forged = copy.deepcopy(result); forged['status'] = 'proven'
    reject('counterexample relabeled as proof', lambda: check_classic(inversion, forged, True))
    altered.write_bytes(altered.read_bytes()+b'changed\n')
    reject('changed solver input', lambda: check_classic(inversion, result, True))
    inherited = {1,4,6}
    attempts = [{'status': 'inconclusive', 'indices': [0,2,3]},
        {'status': 'proven', 'indices': [5,7]}, {'status': 'proven', 'indices': [8,9,10]}]
    queue, proven, unresolved = coverage(11, inherited, attempts, 4)
    if list(queue) != [[0],[2,3]] or proven != {1,4,5,6,7,8,9,10} or unresolved:
        raise ValueError('split queue lost inherited or pending observations')
    attempts += [{'status': 'inconclusive', 'indices': [0]}, {'status': 'proven', 'indices': [2,3]}]
    queue, proven, unresolved = coverage(11, inherited, attempts, 4)
    if queue or proven != set(range(1,11)) or unresolved != [attempts[-2]]:
        raise ValueError('inconclusive singleton contributed to proven coverage')
    reject('inherited out-of-range bit', lambda: coverage(11, {11}, [], 4))
    reject('Boolean as inherited bit', lambda: coverage(11, {True}, [], 4))
    reject('zero group size', lambda: coverage(11, inherited, [], 0))
    for label, replacement in [('wrong completion order',[5,7]), ('duplicate bit',[0,2,2,3]),
            ('inherited bit counted twice',[0,1,2,3]), ('omitted obligation',[0,2])]:
        changed = copy.deepcopy(attempts); changed[0]['indices'] = replacement
        reject(label, lambda changed=changed: coverage(11, inherited, changed, 4))
    changed = copy.deepcopy(attempts); changed[0]['status'] = 'counterexample'
    reject('hidden counterexample', lambda: coverage(11, inherited, changed, 4))
    changed[0]['status'] = 'unknown'
    reject('unrecognized status', lambda: coverage(11, inherited, changed, 4))
    valid = completed.read_bytes()
    for label, key, value in [('forged proof count','proven_observation_bits',2),
            ('forged pending count','pending_groups',1), ('missing negative control','negative',dict(record['negative'],status='proven'))]:
        wrong = json.loads(valid); wrong[key] = value; completed.write_text(json.dumps(wrong))
        with (directory/(label.replace(' ','-')+'.log')).open('w') as log:
            failure = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, timeout=90)
        if failure.returncode == 0:
            raise ValueError('real resume command accepted '+label)
        rejected.append({'name': label, 'reason': 'real resume command rejected inconsistent checkpoint'})
    completed.write_bytes(valid)
    for name, value in hashes.items():
        if digest(ROOT/name) != value:
            raise ValueError('classic driver input changed: '+name)
    report.write_text(json.dumps({'status': 'passed', 'scope': 'synthetic proof-driver fixtures, not the CPU proof',
        'inputs': hashes, 'rejected_defects': rejected, 'inherited_bits': 2, 'completed_fixture_bits': 3,
        'inconclusive_singleton_preserved': True, 'completed_run_reverified': True,
        'artifacts': {str(p.relative_to(ROOT)): digest(p) for p in directory.glob('*.log')}}, indent=2)+'\n')
    print(f'PASS classic proof driver, including {len(rejected)} rejected defects')


if __name__ == '__main__':
    main()
