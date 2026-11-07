#!/usr/bin/env python3
"""Run complete official scripts on the programmable system, one session each.

For every suite, the unchanged native runner executes the script with the
device's physical memory/table limits and records its exact loader and
execution transcript. That transcript becomes one session image: the
programmable system receives it over its UART, replays the whole store and
executes every invocation, global read and size query itself, reporting each
result as a separate frame. Every frame must equal the native response, in
order, with no frame missing, added or reordered.
"""
import argparse
import binascii
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from pathlib import Path
import subprocess
import time
import types

import run_spec
from check_loadable import parse_frames
from measure_spec_sessions import Recording
from prepare_standalone import ROM_WIDTHS, ROOT, digest, load_profile, pack_trace, profile_path
from program_upload import encode
from standalone_support import verify_image, verify_simulator

SKIPPED = ('V', 'W', 'Q')
MASK = (1 << 128) - 1


def decode_session(raw):
    """Session result (kind 2) and end (kind 3) frames carry the boot-record index."""
    if len(raw) < 16 or raw[:2] != b'WM' or raw[2] not in (2, 3):
        raise ValueError('bad session frame header')
    count = raw[5]
    if len(raw) != 16 + 16 * count:
        raise ValueError('bad session frame length')
    if binascii.crc_hqx(raw[2:-2], 0xffff) != int.from_bytes(raw[-2:], 'little'):
        raise ValueError('bad session frame checksum')
    return {'kind': raw[2], 'status': raw[3], 'trap': raw[4], 'cycles': int.from_bytes(raw[6:10], 'little'),
            'record': int.from_bytes(raw[10:14], 'little'),
            'values': [int.from_bytes(raw[n:n+16], 'little') for n in range(14, len(raw)-2, 16)]}


def split_frames(data):
    replies, frames, final = [], [], []
    while data:
        if data[:4] == b'WMLR':
            replies.append(data[:20]); data = data[20:]
        elif data[:2] == b'WM' and len(data) >= 6 and data[2] in (2, 3):
            length = 16 + 16 * data[5]
            frames.append(decode_session(data[:length])); data = data[length:]
        elif data[:3] == b'WM\x01' and len(data) >= 6:
            length = 12 + 16 * data[5]
            final.append(data[:length]); data = data[length:]
        else:
            raise ValueError('unexpected or truncated serial data: ' + data[:20].hex())
    return replies, frames, final


def expected_frame(command, response):
    op, r = command.split()[0], response.split()
    if op == 'R':
        if r[0] == 'OK':
            return {'status': 0, 'trap': 0, 'values': [int(v, 16) & MASK for v in r[2:2+int(r[1])]]}
        if r[0] == 'TRAP':
            return {'status': 1, 'trap': int(r[1]), 'values': []}
        raise ValueError('native execution did not complete: ' + response)
    if op == 'H' and r[0] == 'GLOBAL':
        return {'status': 0, 'trap': 0, 'values': [int(r[1], 16) & MASK]}
    if op == 'S' and r[0] == 'SIZE':
        return {'status': 0, 'trap': 0, 'values': [int(r[1], 16) & MASK]}
    raise ValueError(f'unexpected native response to {command}: {response}')


class PeakRecording(Recording):
    """Record the final, and therefore peak, size of every memory and table."""
    peaks = None

    def close(self):
        if self.proc.poll() is None:
            PeakRecording.peaks = {kind: [self.size(kind, index)
                                          for index in range(count)]
                                   for kind, count in ((0, self.memories), (1, self.tables))}
            # The size queries above are bookkeeping, not part of the script.
            del self.transcript[-(self.memories + self.tables):]
        super().close()


def sized_to_peaks(trace, peaks):
    """Set each memory's and table's physical maximum to the peak the script reached.

    Every growth that succeeded natively stays within that size and every
    growth that failed natively still exceeds it, so behavior is unchanged.
    """
    sized = []
    for line in trace:
        f = line.split()
        if f[0] in ('M', 'T'):
            peak = peaks[0 if f[0] == 'M' else 1][int(f[1])]
            if not int(f[2]) <= peak <= int(f[3]):
                raise ValueError('peak size outside declared limits')
            f[3] = str(peak)
            line = ' '.join(f)
        sized.append(line)
    return sized


def native_session(source, profile):
    """Run the official script natively and record its transcript and peak sizes."""
    Recording.transcripts = []
    Recording.limits = None
    PeakRecording.peaks = None
    run_spec.RTL = PeakRecording
    _, target, error = run_spec.convert(source)
    if error:
        raise run_spec.ExecutionError(error)
    args = types.SimpleNamespace(wait_states=0, max_cycles=300000000, simulator=ROOT/'build/obj/Vwasmetal_core',
                                 response_timeout=3600, verbose=False, command_partitions={})
    report = run_spec.run_file(source, target, args)
    if len(Recording.transcripts) != 1:
        raise ValueError('a session needs exactly one native store')
    return report, target, Recording.transcripts[0]


def write_image(output, roms, summary, profile, trace, script):
    output.mkdir(parents=True, exist_ok=True)
    (output/'manifest.json').unlink(missing_ok=True)
    files = {}
    for name, values in roms.items():
        width = ROM_WIDTHS[name] or profile['type_depth']
        path = output/(name + '.hex')
        path.write_text(''.join(f'{v:0{(width+3)//4}x}\n' for v in values))
        files[path.name] = digest(path)
    (output/'initialization.txt').write_text('\n'.join(trace) + '\n')
    (output/'script.json').write_bytes(script.read_bytes())
    files.update({n: digest(output/n) for n in ('initialization.txt', 'script.json')})
    manifest = {'format': 'wasmetal-standalone-v1', 'session': True, 'profile': profile, **summary, 'files': files,
                'physical_hardware_tested': False,
                'preparation_inputs': {n: digest(ROOT/n) for n in (
                    'tools/prepare_standalone.py', 'tools/wasm_image.py', 'tools/run_spec.py',
                    'tools/spec_session.py', 'tools/upstream.lock.json')}}
    (output/'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def run_suite(source, binary, deadline, native_only=False):
    name = str(source.relative_to(run_spec.SPEC/'test/core').with_suffix(''))
    profile = load_profile()
    started = time.monotonic()
    result = {'suite': name}
    native, target, transcript = native_session(source, profile)
    result['native_counts'] = native['counts']
    if native['failures'] or native['counts'].get('unsupported', 0):
        return {**result, 'status': 'native-fails-at-capacity', 'failures': native['failures'][:5]}
    lines = [(c, r) for c, r in transcript if c.split()[0] not in SKIPPED]
    trace = sized_to_peaks([c for c, _ in lines], PeakRecording.peaks)
    try:
        roms, summary = pack_trace(trace, profile, session=True)
    except ValueError as error:
        return {**result, 'status': 'exceeds-profile', 'reason': str(error)}
    regions = summary['regions']
    usage = {'allocated_ram_bytes': summary['allocated_ram_bytes'], 'counts': summary['counts'],
             'memory_bytes': sum(r['bytes'] for r in regions if r['kind'] == 0),
             'reports': len(summary['reports'])}
    if native_only:
        return {**result, 'status': 'packed', **usage, 'elapsed_seconds': time.monotonic() - started}
    directory = ROOT/'build/spec-sessions'/profile_path().stem/name
    image = directory/'image'
    write_image(image, roms, summary, profile, trace, target)
    verify_image(image)
    packet = encode(image, 0x5753000000000000, compact=True)
    path = directory/'session.wmu'
    path.write_bytes(packet.bytes())
    expected = [{'record': row['boot_record'], **expected_frame(*lines[row['trace_line']])}
                for row in summary['reports']]
    # A board campaign needs only the packet and these expectations.
    (directory/'expected.json').write_text(json.dumps(expected) + '\n')
    rows = (profile['instruction_depth'] + profile['function_depth'] + profile['type_depth'] +
            6 * profile['regions_per_kind'] + profile['boot_depth'])
    run = subprocess.run([str(binary), '--deadline-clocks', str(deadline), '--fill-clocks', str(rows),
                          '--upload', str(path)],
                         capture_output=True, text=True, timeout=24*3600)
    if run.returncode:
        return {**result, 'status': 'simulator-error', 'error': run.stderr[-2000:]}
    output = json.loads(run.stdout.strip().splitlines()[-1])
    replies, frames, final = split_frames(bytes.fromhex(output['uart']))
    mismatches = []
    if final:
        mismatches.append({'error_frame': final[0].hex()})
    if len(replies) != 2:
        mismatches.append({'replies': len(replies)})
    if not frames or frames[-1]['kind'] != 3:
        mismatches.append({'missing_end_frame': True})
    reported = [f for f in frames if f['kind'] == 2]
    for index, (want, got) in enumerate(zip(expected, reported)):
        actual = {k: got[k] for k in ('record', 'status', 'trap', 'values')}
        if actual != want:
            mismatches.append({'report': index, 'command': trace[summary['reports'][index]['trace_line']],
                               'expected': want, 'actual': actual})
            if len(mismatches) > 10:
                break
    if len(reported) != len(expected):
        mismatches.append({'reports': len(reported), 'expected_reports': len(expected)})
    return {**result, 'status': 'failed' if mismatches else 'passed', 'reports': len(expected),
            'mismatches': mismatches, 'counts': summary['counts'], 'allocated_ram_bytes': summary['allocated_ram_bytes'],
            'device_execution_cycles': sum(f['cycles'] for f in reported),
            'clocks': output['clocks'], 'packet_sha256': digest(path), 'elapsed_seconds': time.monotonic() - started}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path, required=True, help='core-clock programmable simulator')
    parser.add_argument('--suite', action='append', default=[])
    parser.add_argument('--jobs', type=int, default=2)
    parser.add_argument('--deadline-clocks', type=int, default=4_000_000_000)
    parser.add_argument('--native-only', action='store_true',
                        help='stop after packing each session; measure without device simulation')
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    import build_identity
    build_identity.verify(ROOT/'build/obj/Vwasmetal_core')
    identity = None if args.native_only else verify_simulator(args.binary.resolve())
    if identity and (identity['profile'] != load_profile() or identity['clock_scale'] != 1):
        raise SystemExit('simulator profile or clock configuration differs from the selected profile')
    run_spec.conversion_session()
    run_spec.prepare_spectest()
    sources = sorted((run_spec.SPEC/'test/core').rglob('*.wast'))
    if args.suite:
        wanted = set(args.suite)
        sources = [s for s in sources if str(s.relative_to(run_spec.SPEC/'test/core').with_suffix('')) in wanted]
        if len(sources) != len(wanted):
            parser.error('unknown suite')
    results = {}

    def save(status):
        args.report.parent.mkdir(parents=True, exist_ok=True)
        statuses = [r['status'] for r in results.values()]
        args.report.write_text(json.dumps({
            'status': status, 'profile': load_profile(), 'simulator': identity, 'suite_count': len(sources),
            'summary': {s: statuses.count(s) for s in sorted(set(statuses))},
            'suites': dict(sorted(results.items())), 'physical_hardware_tested': False}, indent=2) + '\n')
    with ProcessPoolExecutor(args.jobs) as pool:
        futures = {pool.submit(run_suite, s, args.binary.resolve(), args.deadline_clocks, args.native_only): s
                   for s in sources}
        for future in as_completed(futures):
            try:
                value = future.result()
            except Exception as error:
                source = futures[future]
                value = {'suite': str(source.relative_to(run_spec.SPEC/'test/core').with_suffix('')),
                         'status': 'error', 'error': str(error)[-2000:]}
            results[value['suite']] = value
            print(value['status'], value['suite'], flush=True)
            save('running')
    save('complete')
    print(json.dumps({s: [r['status'] for r in results.values()].count(s)
                      for s in sorted({r['status'] for r in results.values()})}))


if __name__ == '__main__':
    main()
