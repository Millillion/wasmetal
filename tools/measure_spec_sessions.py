#!/usr/bin/env python3
"""Measure the on-device storage each official script needs as one session.

Runs every pinned official suite through the unchanged native runner and
records its complete loader/execution transcript. The report gives the
instruction, metadata, region, RAM and boot-record capacities a programmable
system needs to replay that whole script on the device.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from pathlib import Path
import types

import run_spec
from prepare_standalone import ROOT, digest

KINDS = {'M': 0, 'G': 1, 'T': 2, 'D': 3, 'L': 4}


class Recording(run_spec.RTL):
    transcripts = []
    limits = None

    def __init__(self, *args, **kwargs):
        self.transcript = []
        Recording.transcripts.append(self.transcript)
        super().__init__(*args, **kwargs)

    def send(self, command):
        fields = command.split()
        if Recording.limits and fields[0] in ('M', 'T'):
            # Physical capacity, as on the device: growth beyond it fails.
            limit = Recording.limits[fields[0]]
            if int(fields[2]) > limit:
                raise run_spec.ExecutionError(f'{fields[0]} initial size exceeds physical capacity')
            fields[3] = str(min(int(fields[3]), limit))
            command = ' '.join(fields)
        self.transcript.append([command, None])
        super().send(command)

    def receive(self):
        response = super().receive()
        self.transcript[-1][1] = ' '.join(response)
        return response


def requirements(transcript):
    code = functions = boot = ram = 0
    types_used, regions, pages, slots = set(), {k: set() for k in KINDS}, 0, 0
    results = runs = queries = 0
    max_cycles = max_values = 0
    for command, response in transcript:
        f = command.split()
        op = f[0]
        if op == 'I':
            code = max(code, int(f[1]) + 1)
        elif op == 'F':
            functions = max(functions, int(f[1]) + 1)
            types_used.add(int(f[6]))
            max_values = max(max_values, int(f[3]) + int(f[4]))
        elif op == 'Y':
            types_used.update(map(int, f[1:3]))
        elif op in KINDS:
            regions[op].add(int(f[1]))
            if op in ('M', 'T'):
                size = int(f[3]) * (65536 if op == 'M' else 16)
                pages = max(pages, int(f[3])) if op == 'M' else pages
                slots = max(slots, int(f[3])) if op == 'T' else slots
                boot += 1
            elif op == 'G':
                size = 16
                boot += 1
            elif op == 'D':
                size = 0 if f[3] == '-' else len(f[3]) // 2
                boot += 1 + (size + 15) // 16
            else:
                size = int(f[3]) * 16
                boot += 1 + int(f[3])
            ram += (size + 15) & ~15
        elif op == 'B':
            boot += (len(f[3]) // 2 + 15) // 16
        elif op == 'E':
            boot += 1
        elif op == 'A':
            boot += 1
        elif op == 'R':
            runs += 1
            boot += 1
            if response:
                r = response.split()
                max_cycles = max(max_cycles, int(r[-1]))
                if r[0] == 'OK':
                    results = max(results, int(r[1]))
        elif op in ('H', 'S'):
            queries += 1
            boot += 1
    return {'instructions': code, 'functions': functions, 'types': max(types_used, default=-1) + 1,
            'regions_per_kind': max((max(v) + 1 for v in regions.values() if v), default=0),
            'region_counts': {k: len(v) for k, v in regions.items()}, 'ram_bytes': ram,
            'max_memory_pages': pages, 'max_table_slots': slots, 'boot_records': boot + 2,
            'executions': runs, 'queries': queries, 'max_results': results,
            'max_invocation_cycles': max_cycles, 'max_function_values': max_values}


def measure(source, simulator, limits):
    Recording.transcripts = []
    Recording.limits = limits
    run_spec.RTL = Recording
    _, target, error = run_spec.convert(source)
    if error:
        raise run_spec.ExecutionError(error)
    args = types.SimpleNamespace(wait_states=0, max_cycles=300000000, simulator=simulator,
                                 response_timeout=3600, verbose=False, command_partitions={})
    report = run_spec.run_file(source, target, args)
    name = str(source.relative_to(run_spec.SPEC/'test/core'))
    passed = not report['failures'] and not report['counts'].get('unsupported', 0)
    sessions = [requirements(t) for t in Recording.transcripts]
    return name, {'passed': passed, 'failures': report['failures'][:5], 'counts': report['counts'],
                  'sessions': len(sessions), **requirements(
        [c for t in Recording.transcripts for c in t])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suite', action='append', default=[])
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--simulator', type=Path, default=ROOT/'build/obj/Vwasmetal_core')
    parser.add_argument('--memory-pages', type=int, help='clamp every memory maximum to this many pages')
    parser.add_argument('--table-slots', type=int, help='clamp every table maximum to this many slots')
    parser.add_argument('--report', type=Path, default=ROOT/'reports/spec-session-requirements.json')
    args = parser.parse_args()
    import build_identity
    identity = build_identity.verify(args.simulator)
    run_spec.conversion_session()
    run_spec.prepare_spectest()
    sources = sorted((run_spec.SPEC/'test/core').rglob('*.wast'))
    if args.suite:
        sources = [s for s in sources if str(s.relative_to(run_spec.SPEC/'test/core').with_suffix('')) in set(args.suite)]
    suites = {}
    with ProcessPoolExecutor(args.jobs) as pool:
        limits = {'M': args.memory_pages, 'T': args.table_slots} if args.memory_pages else None
        futures = [pool.submit(measure, s, args.simulator, limits) for s in sources]
        for future in as_completed(futures):
            name, value = future.result()
            suites[name] = value
    keys = ('instructions', 'functions', 'types', 'regions_per_kind', 'ram_bytes', 'max_memory_pages',
            'max_table_slots', 'boot_records', 'max_results', 'max_invocation_cycles', 'max_function_values')
    report = {'suites': dict(sorted(suites.items())), 'suite_count': len(suites),
              'limits': {'memory_pages': args.memory_pages, 'table_slots': args.table_slots},
              'failed_suites': sorted(n for n, v in suites.items() if not v['passed']),
              'all_passed_natively': all(v['passed'] for v in suites.values()),
              'maxima': {k: max(v[k] for v in suites.values()) for k in keys},
              'simulator_sha256': identity['binary_sha256'],
              'tool_sha256': digest(Path(__file__).resolve()), 'physical_hardware_tested': False}
    args.report.parent.mkdir(exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report['maxima'], indent=2))


if __name__ == '__main__':
    main()
