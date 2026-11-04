#!/usr/bin/env python3
"""Plan, package and validate the complete synthesized-CPU CI regression."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import tarfile

import build_identity
import run_spec
import spec_shards as checks

ROOT = Path(__file__).resolve().parent.parent


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2)+'\n')


def catalog():
    source_hash = run_spec.verify_official_sources()
    entries = {}
    run_spec.prepare_spectest()
    for source in sorted((run_spec.SPEC/'test/core').rglob('*.wast')):
        _, target, error = run_spec.convert(source)
        checks.require(not error, f'cannot convert official script: {source}: {error}')
        commands = json.loads(target.read_text())['commands']
        entries[str(source.relative_to(run_spec.SPEC/'test/core'))] = (target, commands)
    return source_hash, entries


def validate_reference(reference, source_hash, entries):
    checks.clean_report(reference)
    checks.require(reference['full_core_suite_selected'] and reference['full_core_suite_passed'],
                   'native reference must pass the complete corpus')
    checks.require(reference['spec'] == run_spec.LOCK['spec'] and reference['official_sources_sha256'] == source_hash,
                   'native reference describes different official sources')
    checks.require(reference['memory_wait_states'] == 3, 'native reference must use three memory wait states')
    checks.require('backend' not in reference['build_manifest'], 'reference must execute original RTL')
    suites = {s['suite']:s for s in reference['suites']}
    checks.require(set(suites) == set(entries), 'native reference omits official suites')
    for name, (_, commands) in entries.items():
        suite = suites[name]
        checks.require(suite['command_count'] == len(commands) and suite['executed_commands'] == list(range(len(commands))),
                       f'incomplete native command trace: {name}')
        cycles = suite['command_cycles']
        checks.require(len(cycles) == len(commands) and all(type(c) is int and c >= 0 for c in cycles),
                       f'invalid native cycle trace: {name}')
        checks.require(sum(cycles) == suite['counts'].get('rtl_cycles',0), f'native cycle trace mismatch: {name}')
        checks.require(suite['counts']['script_commands'] == len(commands), f'native script count mismatch: {name}')
        checks.require(suite['replayed_setup_commands'] == [] and suite['replayed_setup_cycles'] == 0,
                       f'native reference contains replayed commands: {name}')
        checks.require(suite['total_simulated_cycles'] == sum(cycles), f'native total cycles mismatch: {name}')
    totals = Counter()
    for suite in suites.values():
        totals.update(suite['counts'])
    checks.require(dict(totals) == reference['totals'], 'native report totals do not match suite counts')
    return suites


def create_plan(reference, reference_hash, source_hash, entries, count):
    checks.require(1 <= count <= 64, 'invalid shard count')
    suites = validate_reference(reference, source_hash, entries)
    tasks = []
    for name, (target, commands) in entries.items():
        if name in checks.PARTITIONABLE:
            checks.independent_script(name, target, commands, ROOT/'build/spectest.wasm')
            tasks += [(max(1, cycles),name,index) for index,cycles in enumerate(suites[name]['command_cycles'])]
        else:
            tasks.append((max(1,suites[name]['counts'].get('rtl_cycles',0)),name,None))
    bins = [{'id':f'{i:02d}','estimated_cycles':0,'entries':{}} for i in range(count)]
    # Stable longest-first packing. Measured cycle counts affect placement only.
    for weight,name,index in sorted(tasks,key=lambda t:(-t[0],t[1],-1 if t[2] is None else t[2])):
        bucket = min(bins,key=lambda b:(b['estimated_cycles'],b['id']))
        entry = bucket['entries'].setdefault(name,{'suite':name,'commands':None if index is None else [],'estimated_cycles':0})
        if index is not None:
            entry['commands'].append(index)
        entry['estimated_cycles'] += weight
        bucket['estimated_cycles'] += weight
    for bucket in bins:
        bucket['entries'] = sorted(bucket['entries'].values(),key=lambda e:e['suite'])
        for entry in bucket['entries']:
            if entry['commands'] is not None:
                entry['commands'].sort()
    plan = {'version':1,'spec':reference['spec'],'official_sources_sha256':source_hash,
            'native_reference_sha256':reference_hash,
            'command_counts':{name:len(commands) for name,(_,commands) in entries.items()},'shards':bins}
    checks.validate_plan(plan,source_hash,plan['command_counts'])
    return plan


def execution_identity(reference, reports, models):
    """Recheck actual executables when unrelated workspace snapshots differ.

    The broad source_sha256 includes every Python tool, even unused tools added
    during a long run. It is not a dependency manifest. This optional path keeps
    those original fingerprints while requiring the complete executable and
    runner dependency identities to match the recorded runs and current files.
    """
    checks.require(set(models) == {'native', 'mapped'}, 'need both execution models')
    native = build_identity.verify(Path(models['native']))
    mapped = build_identity.verify(Path(models['mapped']))
    checks.require(native == reference['build_manifest'], 'native executable differs from reference')
    checks.require(native['binary_sha256'] == reference['simulator_sha256'], 'native binary identity mismatch')
    checks.require(all(mapped == r['build_manifest'] and mapped['binary_sha256'] == r['simulator_sha256']
                       for r in reports), 'mapped executable differs from shard evidence')
    expected_runner = {'tools/run_spec.py', 'tools/wasm_image.py', 'tools/spec_shards.py', 'build/spectest.wasm'}
    checks.require(set(reference['runner_inputs']) == expected_runner, 'unreviewed runner input inventory')
    for name, value in reference['runner_inputs'].items():
        checks.require(checks.sha256(ROOT/name) == value, 'runner input changed: '+name)
    snapshots = {'native': reference['source_sha256'],
                 'mapped_shards': {r['shard_id']: r['source_sha256'] for r in reports}}
    for value in [snapshots['native'], *snapshots['mapped_shards'].values()]:
        checks.require(isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None,
                       'invalid reported workspace fingerprint')
    inputs = {**native['inputs'], **mapped['inputs'], **mapped.get('extra_inputs', {}),
              **reference['runner_inputs']}
    for name in ('tools/spec_ci.py', 'tools/build_identity.py'):
        inputs[name] = checks.sha256(ROOT/name)
    return {'policy': 'rechecked executables and exact execution dependencies; workspace snapshots retained',
            'models': {name: {'path': str(Path(path).resolve()),
                              'binary_sha256': checks.sha256(path),
                              'manifest_sha256': checks.sha256(str(path)+'.build.json')}
                       for name, path in models.items()},
            'reported_workspace_sha256': snapshots, 'verified_inputs': inputs}


def merge_reports(plan, plan_hash, reference, reference_hash, reports, source_hash, entries, *, execution_models=None):
    checks.require(plan['native_reference_sha256'] == reference_hash, 'wrong native reference')
    checks.require(plan['spec'] == reference['spec'], 'plan specification mismatch')
    expected = validate_reference(reference,source_hash,entries)
    checks.validate_plan(plan,source_hash,{n:len(c) for n,(_,c) in entries.items()})
    identity = execution_identity(reference, reports, execution_models) if execution_models is not None else None
    expected_shards = {s['id']:s for s in plan['shards']}
    checks.require(len(reports) == len(expected_shards), 'missing or extra shard reports')
    seen_shards, coverage = set(), {name:set() for name in entries}
    combined = {name:Counter() for name in entries}
    command_cycles = {name:[None]*len(c) for name,(_,c) in entries.items()}
    first = None
    for report in reports:
        checks.clean_report(report)
        shard_id = report['shard_id']
        checks.require(shard_id in expected_shards and shard_id not in seen_shards, 'unknown or duplicate shard report')
        seen_shards.add(shard_id)
        checks.require(report['shard_plan_sha256'] == plan_hash, 'shard used a different plan')
        checks.require(not report['full_core_suite_selected'] and not report['full_core_suite_passed'], 'shard claims a full pass')
        checks.require(report['build_manifest'].get('backend') == 'mapped-ecp5-functional', 'shard did not execute the mapped CPU')
        checks.require(report['build_manifest']['binary_sha256'] == report['simulator_sha256'], 'mapped binary identity mismatch')
        checks.require(report['build_manifest']['inputs'] == reference['build_manifest']['inputs'], 'different RTL build inputs')
        for key in ['spec','official_sources_sha256','runner_inputs','rtl_build_id','capacities',
                    'memory_wait_states','max_cycles_per_invocation']:
            checks.require(report[key] == reference[key], f'native/mapped identity mismatch: {key}')
        if identity is None:
            checks.require(report['source_sha256'] == reference['source_sha256'],
                           'native/mapped identity mismatch: source_sha256')
        if first is not None:
            for key in ['simulator_sha256','build_manifest','response_timeout_seconds']:
                checks.require(report[key] == first[key], f'mixed mapped models/settings: {key}')
        first = report
        owned = {e['suite']:e for e in expected_shards[shard_id]['entries']}
        checks.require({s['suite'] for s in report['suites']} == set(owned), 'shard suite set mismatch')
        shard_totals = Counter()
        for suite in report['suites']:
            name = suite['suite']
            commands = entries[name][1]
            selected = owned[name]['commands']
            selected = list(range(len(commands))) if selected is None else selected
            checks.require(suite['command_count'] == len(commands) and suite['executed_commands'] == selected,
                           f'missing or reordered command execution: {name}')
            checks.require(not coverage[name].intersection(selected), f'duplicate command execution: {name}')
            coverage[name].update(selected)
            replayed = [i for i,c in enumerate(commands) if i not in selected and c['type']=='module']
            checks.require(suite['replayed_setup_commands'] == replayed, f'unexpected setup replay: {name}')
            fixture = expected[name]['fixture_cycles']
            checks.require(suite['fixture_cycles'] == fixture, f'fixture cycle mismatch: {name}')
            replay_cycles = sum(expected[name]['command_cycles'][i] - (fixture if i == 0 else 0) for i in replayed)
            replay_cycles += fixture if 0 not in selected else 0
            checks.require(suite['replayed_setup_cycles'] == replay_cycles, f'setup replay cycle mismatch: {name}')
            checks.require(suite['total_simulated_cycles'] == suite['counts']['rtl_cycles'] + replay_cycles,
                           f'unaccounted simulator cycles: {name}')
            cycles = suite['command_cycles']
            checks.require(len(cycles) == len(commands), 'wrong command trace length')
            for i,value in enumerate(cycles):
                checks.require(value == (expected[name]['command_cycles'][i] if i in selected else None),
                               f'command cycle mismatch: {name}:{i}')
                if i in selected:
                    command_cycles[name][i] = value
            checks.require(sum(c for c in cycles if c is not None) == suite['counts'].get('rtl_cycles',0), 'cycle total mismatch')
            checks.require(suite['counts']['script_commands'] == len(selected), 'command total mismatch')
            combined[name].update(suite['counts'])
            shard_totals.update(suite['counts'])
        checks.require(dict(shard_totals) == report['totals'], 'shard totals do not match suite results')
    suites, totals = [], Counter()
    for name in sorted(entries):
        checks.require(coverage[name] == set(range(len(entries[name][1]))), f'incomplete command coverage: {name}')
        checks.require(dict(combined[name]) == expected[name]['counts'], f'native/mapped count mismatch: {name}')
        totals.update(combined[name])
        suites.append({'suite':name,'counts':dict(combined[name]),'failures':[],
                       'command_count':len(command_cycles[name]),'command_cycles':command_cycles[name],
                       'executed_commands':sorted(coverage[name]),'replayed_setup_commands':[],
                       'fixture_cycles':expected[name]['fixture_cycles']})
    checks.require(dict(totals) == reference['totals'], 'full corpus totals differ')
    result = {k:v for k,v in first.items() if k not in {'suites','totals','elapsed_seconds','shard_id'}}
    result.update(full_core_suite_selected=True,full_core_suite_passed=True,suite_files=len(suites),suites=suites,
                  totals=dict(totals),shard_ids=sorted(seen_shards),native_reference_sha256=reference_hash,
                  exact_native_command_cycles=True,verification='aggregate of exhaustive disjoint CI command ownership')
    if identity is not None:
        checks.require(execution_identity(reference, reports, execution_models) == identity,
                       'execution inputs changed during reconciliation')
        # There is no single workspace snapshot when development continued.
        snapshots = identity['reported_workspace_sha256']
        result['source_sha256'] = (snapshots['native'] if
            all(v == snapshots['native'] for v in snapshots['mapped_shards'].values()) else None)
        result['workspace_reconciliation'] = identity
    return result


def pack(binary, destination):
    manifest = build_identity.verify(binary)
    checks.require(manifest.get('backend') == 'mapped-ecp5-functional', 'expected mapped CPU')
    checks.require(manifest['compilation'].get('portable') is True, 'shared CI simulator must use a portable CPU target')
    paths = set(manifest['extra_inputs']) | {'sim/core_config.hpp','sim/fpga_ports.hpp','fpga/core_ports.svh',str(binary.relative_to(ROOT)),
             str(binary.relative_to(ROOT))+'.build.json',str(binary.relative_to(ROOT))+'.inputs.json'}
    destination.parent.mkdir(parents=True,exist_ok=True)
    with tarfile.open(destination,'w:gz') as archive:
        for name in sorted(paths):
            path = Path(name)
            checks.require(not path.is_absolute() and '..' not in path.parts, 'unsafe artifact path')
            archive.add(ROOT/path,arcname=str(path),recursive=False)


def main():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest='command',required=True)
    plan = commands.add_parser('plan')
    plan.add_argument('--reference',type=Path,required=True)
    plan.add_argument('--output',type=Path,required=True)
    plan.add_argument('--shards',type=int,default=16)
    plan.add_argument('--github-output',type=Path)
    merge = commands.add_parser('merge')
    merge.add_argument('--reference',type=Path,required=True)
    merge.add_argument('--plan',type=Path,required=True)
    merge.add_argument('--reports',type=Path,required=True)
    merge.add_argument('--output',type=Path,required=True)
    merge.add_argument('--native-simulator', type=Path,
                       help='with --mapped-simulator, recheck exact execution inputs despite unrelated workspace changes')
    merge.add_argument('--mapped-simulator', type=Path)
    package = commands.add_parser('pack')
    package.add_argument('--simulator',type=Path,required=True)
    package.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    if args.command == 'merge' and bool(args.native_simulator) != bool(args.mapped_simulator):
        parser.error('workspace reconciliation requires both simulator paths')
    if args.command == 'pack':
        pack(args.simulator.resolve(),args.output)
        return
    paths = sorted(args.reports.rglob('mapped-shard-*.json')) if args.command == 'merge' else []
    protected = [args.reference, *paths]
    if args.command == 'merge':
        protected.append(args.plan)
        if args.native_simulator:
            protected += [args.native_simulator, args.mapped_simulator,
                          Path(str(args.native_simulator)+'.build.json'),
                          Path(str(args.mapped_simulator)+'.build.json')]
    if args.output.resolve() in {p.resolve() for p in protected}:
        parser.error('output must not overwrite a verification input')
    # A failed new aggregation must not leave an older success at its output.
    args.output.unlink(missing_ok=True)
    source_hash, entries = catalog()
    reference = json.loads(args.reference.read_text())
    if args.command == 'plan':
        result = create_plan(reference,checks.sha256(args.reference),source_hash,entries,args.shards)
        write_json(args.output,result)
        if args.github_output:
            with args.github_output.open('a') as stream:
                stream.write('matrix='+json.dumps({'shard':[s['id'] for s in result['shards']]},separators=(',',':'))+'\n')
    else:
        reports = [json.loads(p.read_text()) for p in paths]
        result = merge_reports(json.loads(args.plan.read_text()),checks.sha256(args.plan),reference,
                               checks.sha256(args.reference),reports,source_hash,entries,
                               execution_models=({'native': args.native_simulator.resolve(),
                                                  'mapped': args.mapped_simulator.resolve()}
                                                 if args.native_simulator else None))
        result['shard_reports'] = [{'path':str(p),'sha256':checks.sha256(p)} for p in paths]
        write_json(args.output,result)
    print(json.dumps({'command':args.command,'output':str(args.output),
                      'full_core_suite_passed':result.get('full_core_suite_passed',False)}))


if __name__ == '__main__':
    main()
