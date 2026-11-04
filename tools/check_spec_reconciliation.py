#!/usr/bin/env python3
"""Reaggregate real official-suite evidence and exercise identity/coverage faults."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import time

import spec_ci
from spec_shards import require, sha256

ROOT = Path(__file__).resolve().parent.parent


def protect_outputs(inputs, outputs, root=ROOT):
    targets = [path.resolve() for path in outputs]
    require(len(targets) == len(set(targets)), 'reconciliation outputs overlap')
    require(all(any(base in path.parents for base in (root/'build',root/'reports')) for path in targets),
            'reconciliation outputs must be files within build/ or reports/')
    require({path.resolve() for path in inputs}.isdisjoint(targets),
            'reconciliation output would overwrite an input')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference', type=Path, required=True)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--reports', type=Path, required=True)
    parser.add_argument('--native-simulator', type=Path, required=True)
    parser.add_argument('--mapped-simulator', type=Path, required=True)
    parser.add_argument('--mapped-backend', choices=spec_ci.MAPPED_BACKENDS, default=spec_ci.MAPPED_BACKENDS[0])
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--aggregate', type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    paths = sorted(args.reports.glob('mapped-shard-*.json'))
    consumed = [args.reference, args.plan, *paths, Path(__file__).resolve(),
                ROOT/'tools/spec_ci.py', ROOT/'tools/spec_shards.py', ROOT/'tools/build_identity.py']
    models = {'native': args.native_simulator.resolve(), 'mapped': args.mapped_simulator.resolve()}
    manifests = [spec_ci.build_identity.verify(path) for path in models.values()]
    protected = [*consumed,*models.values(),*[Path(str(p)+'.build.json') for p in models.values()],
                 *[ROOT/name for model in manifests for name in set(model['inputs'])|set(model.get('extra_inputs',{}))]]
    directory = ROOT/'build/spec-reconciliation-controls'
    corrupt = directory/'corrupt-simulator'
    try:
        protect_outputs(protected,[args.output,args.aggregate,corrupt,Path(str(corrupt)+'.build.json')])
    except ValueError as error:
        parser.error(str(error))
    args.output.unlink(missing_ok=True)
    args.aggregate.unlink(missing_ok=True)
    inputs = {str(p.resolve().relative_to(ROOT)): sha256(p) for p in consumed}
    reference = json.loads(args.reference.read_text())
    plan = json.loads(args.plan.read_text())
    reports = [json.loads(p.read_text()) for p in paths]
    source_hash, entries = spec_ci.catalog()

    def merge(ref, rows, partition, selected_models, backend=args.mapped_backend):
        return spec_ci.merge_reports(partition, sha256(args.plan), ref, sha256(args.reference),
                                     rows, source_hash, entries, execution_models=selected_models,
                                     expected_backend=backend)

    # The default CI policy must still reject differing workspace snapshots.
    try:
        merge(reference, reports, plan, None)
    except ValueError as error:
        require(str(error) == 'native/mapped identity mismatch: source_sha256',
                'baseline failed for an unexpected reason: '+str(error))
    else:
        raise ValueError('fixture needs the real differing workspace snapshots')
    result = merge(reference, reports, plan, models)
    require(result['source_sha256'] is None, 'heterogeneous snapshots misrepresented as one source identity')
    require(result['full_core_suite_passed'] and result['exact_native_command_cycles'], 'incomplete aggregate')
    identity = result['workspace_reconciliation']
    controls = []

    def reject(name, mutation):
        ref, rows, partition, selected = deepcopy((reference, reports, plan, models))
        mutation(ref, rows, partition, selected)
        try:
            merge(ref, rows, partition, selected)
        except (ValueError, RuntimeError, OSError) as error:
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
            print('REJECT', name, str(error), flush=True)
        else:
            raise ValueError('accepted deliberate defect: '+name)

    bad = '0'*64
    reject('native-binary-identity', lambda r,s,p,m: r.update(simulator_sha256=bad))
    reject('native-rtl-input', lambda r,s,p,m: r['build_manifest']['inputs'].update({'rtl/wasmetal_core.sv': bad}))
    reject('mapped-rtl-input', lambda r,s,p,m: s[0]['build_manifest']['inputs'].update({'rtl/wasmetal_core.sv': bad}))
    extra = next(iter(reports[0]['build_manifest']['extra_inputs']))
    reject('mapped-model-input', lambda r,s,p,m: s[0]['build_manifest']['extra_inputs'].update({extra: bad}))
    reject('mapped-compiler-identity', lambda r,s,p,m: s[0]['build_manifest']['compilation'].update(compiler_sha256=bad))
    reject('mapped-binary-identity', lambda r,s,p,m: s[0].update(simulator_sha256=bad))
    reject('native-executable-substitution', lambda r,s,p,m: m.update(native=m['mapped']))
    reject('mapped-executable-substitution', lambda r,s,p,m: m.update(mapped=m['native']))
    reject('native-runner-input', lambda r,s,p,m: r['runner_inputs'].update({'tools/run_spec.py': bad}))
    reject('missing-runner-input', lambda r,s,p,m: r['runner_inputs'].pop('tools/wasm_image.py'))
    reject('mapped-runner-input', lambda r,s,p,m: s[0]['runner_inputs'].update({'tools/run_spec.py': bad}))
    reject('build-id', lambda r,s,p,m: s[0].update(rtl_build_id='0'*32))
    reject('capacity', lambda r,s,p,m: s[0]['capacities'].update(value=1))
    reject('memory-wait-states', lambda r,s,p,m: s[0].update(memory_wait_states=0))
    reject('invocation-cycle-budget', lambda r,s,p,m: s[0].update(max_cycles_per_invocation=1))
    reject('official-source-identity', lambda r,s,p,m: s[0].update(official_sources_sha256=bad))
    reject('missing-partition', lambda r,s,p,m: s.pop())
    reject('duplicate-partition', lambda r,s,p,m: s.__setitem__(-1, deepcopy(s[0])))
    reject('wrong-plan-identity', lambda r,s,p,m: s[0].update(shard_plan_sha256=bad))
    reject('missing-command', lambda r,s,p,m: s[0]['suites'][0]['executed_commands'].pop())
    suite = reports[0]['suites'][0]
    selected_command = suite['executed_commands'][0]
    reject('command-cycle-count', lambda r,s,p,m: s[0]['suites'][0]['command_cycles'].__setitem__(
        selected_command, suite['command_cycles'][selected_command]+1))
    reject('failed-assertion', lambda r,s,p,m: s[0]['totals'].update(failed=1))
    reject('unsupported-command', lambda r,s,p,m: s[0]['totals'].update(unsupported=1))
    reject('false-complete-partition', lambda r,s,p,m: s[0].update(full_core_suite_passed=True))
    reject('invalid-workspace-fingerprint', lambda r,s,p,m: s[0].update(source_sha256='not-a-sha256'))
    directory.mkdir(parents=True, exist_ok=True)
    corrupt.write_bytes(b'deliberate executable corruption\n')
    Path(str(corrupt)+'.build.json').write_bytes(Path(str(models['native'])+'.build.json').read_bytes())
    reject('corrupt-executable-bytes', lambda r,s,p,m: m.update(native=corrupt))
    for backend in [b for b in spec_ci.MAPPED_BACKENDS if b!=args.mapped_backend]+['unreviewed']:
        try:
            merge(reference,reports,plan,models,backend)
        except ValueError as error:
            expected=('unreviewed mapped backend' if backend=='unreviewed' else
                      'shard did not execute the selected mapped CPU')
            require(str(error)==expected,'backend fault failed at an unexpected guard: '+str(error))
            controls.append({'name':'wrong-selected-backend-'+backend,'rejected':True,'reason':str(error)})
            print('REJECT wrong-selected-backend-'+backend,str(error),flush=True)
        else:
            raise ValueError('accepted the wrong selected backend: '+backend)
    require(spec_ci.execution_identity(reference, reports, models) == identity, 'execution identity changed')
    for name, value in inputs.items():
        require(sha256(ROOT/name) == value, 'reconciliation input changed: '+name)
    result['shard_reports'] = [{'path': str(p), 'sha256': sha256(p)} for p in paths]
    args.aggregate.parent.mkdir(parents=True, exist_ok=True)
    args.aggregate.write_text(json.dumps(result, indent=2)+'\n')
    receipt = {'status': 'passed', 'scope': 'real full-corpus aggregation with exact executable/dependency reconciliation',
               'mapped_backend': args.mapped_backend,
               'inputs': inputs, 'aggregate_sha256': sha256(args.aggregate),
               'suite_files': result['suite_files'], 'totals': result['totals'],
               'default_workspace_policy_rejected_drift': True,
               'original_reports_unchanged': True, 'negative_controls_rejected': len(controls),
               'negative_controls': controls, 'execution_identity': identity,
               'elapsed_seconds': time.monotonic()-started, 'physical_hardware_tested': False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2)+'\n')
    print('PASS complete official corpus and', len(controls), 'reconciliation fault controls')


if __name__ == '__main__':
    main()
