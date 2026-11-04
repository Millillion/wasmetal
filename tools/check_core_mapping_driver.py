#!/usr/bin/env python3
"""Test mapping-proof partitions and checkpoint recovery with known circuits."""
import copy
import json
from pathlib import Path

import cad
from prepare_standalone import ROOT, digest
from prove_core_mapping import Aig, compare
from resume_core_mapping import replay, check_attempt


def main():
    directory = ROOT/'build/core-mapping-driver'; directory.mkdir(parents=True, exist_ok=True)
    output = ROOT/'reports/core-mapping-driver.json'; output.parent.mkdir(exist_ok=True)
    output.unlink(missing_ok=True)
    paths = [Path(__file__).resolve(), ROOT/'tools/prove_core_mapping.py', ROOT/'tools/resume_core_mapping.py',
        ROOT/'tools/cad.py', ROOT/'tools/prepare_standalone.py', cad.SUITE/'libexec/yosys-abc']
    inputs = {str(path.relative_to(ROOT)): digest(path) for path in paths}
    # Two inputs, one AND, and three outputs: AND, NAND and constant true.
    data = b'aig 3 2 0 3 1\n6\n7\n1\n'+bytes([2, 2])+b'i0 a\ni1 b\no0 both\no1 either_not\no2 true\nc\nfixture\n'
    source = directory/'source.aig'; source.write_bytes(data); model = Aig(source)
    comparisons = []
    for name, indices, negative in [('all', [0, 1, 2], False), ('reordered', [2, 0], False), ('inverted', [0], True)]:
        result = compare(directory/name, [model, model], indices, 5, negative=negative)
        if result['status'] != ('counterexample' if negative else 'proven'):
            raise ValueError('unexpected fixture solver result: '+name)
        check_attempt(directory/name, result); comparisons.append(result)
    rejected = []
    def reject(name, action):
        try:
            action()
        except ValueError as error:
            rejected.append({'name': name, 'reason': str(error)})
        else:
            raise ValueError('proof-driver fixture accepted '+name)
    malformed = {
        'cyclic gate': data.replace(bytes([2, 2]), bytes([0, 2]), 1),
        'latch': data.replace(b'aig 3 2 0 3 1', b'aig 3 2 1 3 1', 1),
        'missing input symbol': data.replace(b'i1 b\n', b''),
        'duplicate input symbol': data.replace(b'i1 b\n', b'i0 b\n'),
        'ambiguous output names': data.replace(b'o2 true\n', b'o2 both\n'),
        'out-of-range output': data.replace(b'\n6\n', b'\n8\n', 1),
        'unreviewed properties': data.replace(b'aig 3 2 0 3 1', b'aig 3 2 0 3 1 1', 1)}
    for name, content in malformed.items():
        path = directory/(name.replace(' ', '-')+'.aig'); path.write_bytes(content)
        reject(name, lambda path=path: Aig(path))
    for name, indices in [('duplicate observations', [0, 0]), ('missing observations', []), ('invalid observation', [3])]:
        reject(name, lambda indices=indices: model.subset(directory/'invalid-subset.aig', indices))
    # Replaying saved results must rebuild the exact original work queue. A
    # timed-out singleton remains unresolved and cannot contribute to coverage.
    attempts = [{'status': 'inconclusive', 'indices': [0, 1]}, {'status': 'proven', 'indices': [2, 3]},
        {'status': 'proven', 'indices': [4]}]
    partial = {'required_observation_bits': 5, 'attempts': attempts, 'proven_observation_bits': 3,
        'pending_groups': 2, 'unresolved': []}
    queue, proven, unresolved = replay(partial)
    if list(queue) != [[0], [1]] or proven != {2, 3, 4} or unresolved:
        raise ValueError('incorrect checkpoint reconstruction')
    singleton = copy.deepcopy(partial)
    singleton['attempts'] += [{'status': 'proven', 'indices': [0]}, {'status': 'inconclusive', 'indices': [1]}]
    singleton.update(proven_observation_bits=4, pending_groups=0, unresolved=[singleton['attempts'][-1]])
    queue, proven, unresolved = replay(singleton)
    if queue or len(proven) != 4 or len(unresolved) != 1:
        raise ValueError('unresolved singleton was lost')
    mutations = {
        'duplicate checkpoint partition': lambda r: r['attempts'].insert(1, copy.deepcopy(r['attempts'][0])),
        'forged coverage count': lambda r: r.update(proven_observation_bits=5),
        'wrong pending count': lambda r: r.update(pending_groups=0),
        'hidden counterexample': lambda r: r['attempts'][0].update(status='counterexample')}
    for name, change in mutations.items():
        altered = copy.deepcopy(partial); change(altered)
        reject(name, lambda altered=altered: replay(altered))
    altered = copy.deepcopy(singleton); altered['unresolved'] = []
    reject('omitted inconclusive bit', lambda: replay(altered))
    forged = copy.deepcopy(comparisons[2]); forged['status'] = 'proven'
    reject('counterexample mislabeled as proof', lambda: check_attempt(directory/'inverted', forged))
    circuit = directory/'all/candidate.aig'; saved = circuit.read_bytes()
    circuit.write_bytes(saved+b'changed\n')
    reject('altered saved circuit', lambda: check_attempt(directory/'all', comparisons[0]))
    circuit.write_bytes(saved); check_attempt(directory/'all', comparisons[0])
    for name, value in inputs.items():
        if digest(ROOT/name) != value:
            raise ValueError('mapping-driver verification input changed: '+name)
    report = {'status': 'passed', 'scope': 'Proof-driver circuits, output selection and checkpoint integrity; not a completed CPU equivalence proof',
        'inputs': inputs, 'comparisons': comparisons, 'rejected_defects': rejected,
        'partial_queue_reconstructed': True, 'inconclusive_singleton_preserved': True,
        'physical_hardware_tested': False}
    output.write_text(json.dumps(report, indent=2)+'\n')
    print(f'PASS proof driver: three real solver comparisons and {len(rejected)} rejected defects')


if __name__ == '__main__':
    main()
