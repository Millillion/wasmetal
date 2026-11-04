#!/usr/bin/env python3
"""Reconcile downloaded complete-corpus CI evidence with the local CPU mapping.

The directory contains gh-run-download artifact subdirectories and github.json
with the run, jobs and artifact metadata fetched from the GitHub API. Run this
at the source revision represented by the artifacts. It never executes the
downloaded simulator; its packaged executable and inputs are checked by hash.
"""
import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import tarfile

import spec_ci
from spec_shards import require, sha256, clean_report

ROOT = Path(__file__).resolve().parent.parent


def read(path):
    return json.loads(path.read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--local-netlist', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.unlink(missing_ok=True)
    base = args.directory
    paths = {
        'native': base/'verification-reports/core.json',
        'native_stalled': base/'verification-reports/core-stalled.json',
        'mapped': base/'mapped-complete/mapped-complete.json',
        'plan': base/'mapped-simulator/mapped-plan.json',
        'package': base/'mapped-simulator/mapped-simulator.tar.gz',
        'github': base/'github.json',
        'ci_netlist': base/'mapped-build-reports/build/core-ecp5.json',
        'ci_manifest': base/'mapped-build-reports/build/core-ecp5.manifest.json',
        'local_netlist': args.local_netlist,
        'local_manifest': args.local_netlist.with_suffix('.manifest.json'),
    }
    shard_paths = sorted(base.glob('mapped-results-*/mapped-shard-*.json'))
    consumed = list(paths.values())+shard_paths+[Path(__file__).resolve(),
        ROOT/'tools/spec_ci.py', ROOT/'tools/spec_shards.py']
    identities = {str(p): sha256(p) for p in consumed}
    native, reference, mapped = (read(paths[k]) for k in ('native', 'native_stalled', 'mapped'))
    plan = read(paths['plan'])
    source_hash, entries = spec_ci.catalog()
    expected = spec_ci.validate_reference(reference, source_hash, entries)
    merged = spec_ci.merge_reports(plan, sha256(paths['plan']), reference,
        sha256(paths['native_stalled']), [read(p) for p in shard_paths], source_hash, entries)
    merged['shard_reports'] = [{'path': str(p), 'sha256': sha256(p)} for p in shard_paths]
    normalized = []
    for report in (merged, mapped):
        value = deepcopy(report)
        for item in value['shard_reports']:
            item['path'] = Path(item['path']).name
        normalized.append(value)
    require(normalized[0] == normalized[1], 'independent merge differs from CI aggregate')

    clean_report(native)
    require(native['full_core_suite_passed'] and native['full_core_suite_selected'], 'incomplete zero-wait run')
    require(native['memory_wait_states'] == 0, 'wrong zero-wait configuration')
    require(native['build_manifest'] == reference['build_manifest'], 'native models differ')
    for key in ('spec', 'official_sources_sha256', 'runner_inputs', 'rtl_build_id', 'capacities',
                'source_sha256', 'simulator_sha256', 'max_cycles_per_invocation', 'suite_files'):
        require(native[key] == reference[key], 'native run identity differs: '+key)
    require(len(native['suites']) == len(expected) == native['suite_files'], 'wrong zero-wait suite count')
    require({s['suite'] for s in native['suites']} == set(expected), 'missing zero-wait suite')
    counts = Counter()
    for suite in native['suites']:
        other = expected[suite['suite']]
        for key in ('command_count', 'executed_commands', 'replayed_setup_commands', 'replayed_setup_cycles'):
            require(suite[key] == other[key], 'zero-wait command coverage differs')
        cycles = suite['command_cycles']
        require(len(cycles) == suite['command_count'] and all(type(c) is int and c >= 0 for c in cycles),
                'invalid zero-wait cycle trace')
        require(sum(cycles) == suite['total_simulated_cycles'] == suite['counts']['rtl_cycles'],
                'invalid zero-wait cycle total')
        without_cycles = lambda c: {k:v for k,v in c.items() if k != 'rtl_cycles'}
        require(without_cycles(suite['counts']) == without_cycles(other['counts']), 'native assertion counts differ')
        counts.update(suite['counts'])
    require(dict(counts) == native['totals'], 'zero-wait totals differ from suites')

    source_identities = dict(reference['build_manifest']['inputs'])
    for name, value in reference['runner_inputs'].items():
        require(name not in source_identities or source_identities[name] == value, 'inconsistent source identity')
        source_identities[name] = value
    for name, value in source_identities.items():
        require(not Path(name).is_absolute() and '..' not in Path(name).parts, 'unsafe source path')
        require(sha256(ROOT/name) == value, 'local source differs from CI: '+name)

    manifest = mapped['build_manifest']
    with tarfile.open(paths['package']) as archive:
        members = archive.getmembers()
        require(all(m.isfile() and not Path(m.name).is_absolute() and '..' not in Path(m.name).parts
                    for m in members), 'unsafe simulator package member')
        require(len({m.name for m in members}) == len(members), 'duplicate simulator package member')
        hashes = {m.name: hashlib.sha256(archive.extractfile(m).read()).hexdigest() for m in members}
        binaries = [m.name for m in members if m.name.endswith('/Vwasmetal_core')]
        require(len(binaries) == 1 and hashes[binaries[0]] == mapped['simulator_sha256'], 'packaged simulator differs')
        require(json.load(archive.extractfile(binaries[0]+'.build.json')) == manifest, 'packaged build manifest differs')
        for name, value in manifest['extra_inputs'].items():
            require(hashes.get(name) == value, 'packaged input differs: '+name)
        require(hashes['build/core-ecp5.json'] == sha256(paths['ci_netlist']), 'packaged circuit differs')
        require(hashes['build/core-ecp5.manifest.json'] == sha256(paths['ci_manifest']), 'packaged synthesis manifest differs')

    local_manifest, ci_manifest = read(paths['local_manifest']), read(paths['ci_manifest'])
    require(local_manifest['inputs'] == ci_manifest['inputs'], 'synthesis sources differ')
    for name, value in ci_manifest['inputs'].items():
        require(not Path(name).is_absolute() and '..' not in Path(name).parts, 'unsafe synthesis source path')
        require(sha256(ROOT/name) == value, 'synthesis source differs: '+name)
    for key, circuit in (('local', paths['local_netlist']), ('ci', paths['ci_netlist'])):
        require(read(paths[key+'_manifest'])['netlist_sha256'] == sha256(circuit), 'synthesis output hash differs')
    options = lambda m: {k:v for k,v in m['arguments'].items() if k != 'output_name'}
    require(local_manifest['top'] == ci_manifest['top'] and options(local_manifest) == options(ci_manifest),
            'synthesis settings differ')
    ci_text = paths['ci_netlist'].read_text()
    workspace = '/home/runner/work/wasmetal/wasmetal'
    require(ci_text.replace(workspace, str(ROOT)) == paths['local_netlist'].read_text(),
            'netlists differ after workspace path relocation')

    github = read(paths['github'])
    run, jobs = github['run'], github['jobs']
    required = {'core', 'mapped-build', 'Complete mapped corpus'} | {f'Mapped circuit ({s})' for s in merged['shard_ids']}
    selected = [j for j in jobs if j['name'] in required]
    require(len(selected) == len(required) and {j['name'] for j in selected} == required, 'missing CI jobs')
    require(all(j['status'] == 'completed' and j['conclusion'] == 'success' and
                j['head_sha'] == run['head_sha'] and j['run_id'] == run['id'] for j in selected), 'CI job mismatch')
    artifact_names = {'verification-reports', 'mapped-complete', 'mapped-build-reports', 'mapped-simulator'} | {
        'mapped-results-'+s for s in merged['shard_ids']}
    artifacts = [a for a in github['artifacts'] if a['name'] in artifact_names]
    require(len(artifacts) == len(artifact_names) and {a['name'] for a in artifacts} == artifact_names, 'missing CI artifacts')
    require(all(a['workflow_run']['id'] == run['id'] and a['workflow_run']['head_sha'] == run['head_sha']
                for a in artifacts), 'artifact revision mismatch')
    for path, value in identities.items():
        require(sha256(Path(path)) == value, 'verification input changed: '+path)
    for name, value in source_identities.items():
        require(sha256(ROOT/name) == value, 'CPU source changed during verification')
    report = {
        'status': 'passed', 'scope': 'complete official corpus on native RTL and functional mapped CPU; no physical timing claim',
        'checked_at': datetime.now(timezone.utc).isoformat(), 'inputs': identities,
        'github': {'run': {k:run[k] for k in ('id','html_url','head_sha','status','conclusion')},
            'jobs': [{k:j.get(k) for k in ('id','name','status','conclusion','started_at','completed_at')} for j in jobs],
            'artifacts': [{k:a[k] for k in ('id','name','digest','size_in_bytes')} for a in artifacts]},
        'verified_source_inputs': source_identities,
        'suite_files': len(expected), 'totals': reference['totals'], 'shard_ids': merged['shard_ids'],
        'exact_native_command_cycles': True, 'independent_aggregation_identical_except_report_paths': True,
        'packaged_simulator_sha256': hashes[binaries[0]], 'verified_packaged_extra_inputs': len(manifest['extra_inputs']),
        'synthesis_comparison': {'local_netlist_sha256': sha256(paths['local_netlist']),
            'ci_netlist_sha256': sha256(paths['ci_netlist']), 'identical_after_workspace_relocation': True,
            'relocated_workspace_occurrences': ci_text.count(workspace), 'same_inputs_and_options': True},
        'physical_board_tested': False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(f'PASS {len(expected)} official suites, {len(merged["shard_ids"])} mapped partitions, packaged model and local/CI circuit agreement')


if __name__ == '__main__':
    main()
