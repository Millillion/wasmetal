#!/usr/bin/env python3
"""Run prepared official-script sessions on a physical board over its UART.

Each suite directory written by spec_session.py holds the compact upload
(`session.wmu`) and the frames the device must report (`expected.json`),
both derived from the native runner. This tool needs no simulator: it uploads
each session, reads every session frame until the end frame and requires
each frame to equal its expectation, in order. Results are written as they
complete, so an interrupted campaign keeps its finished suites.
"""
import argparse
import json
import math
import os
from pathlib import Path
import select
import termios
import time

from program_upload import MAGIC
from spec_session import decode_session
from upload_program import read_reply, remaining, write_all

BAUD = {9600: termios.B9600, 115200: termios.B115200}


def open_serial(device, baud):
    fd = os.open(device, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
    original = termios.tcgetattr(fd)
    raw = termios.tcgetattr(fd)
    raw[0] = 0; raw[1] = 0; raw[3] = 0
    raw[2] = (raw[2] & ~(termios.CSIZE | termios.PARENB | termios.CSTOPB | termios.CRTSCTS)) | \
        termios.CS8 | termios.CREAD | termios.CLOCAL
    raw[4] = raw[5] = BAUD[baud]
    raw[6][termios.VMIN] = 0; raw[6][termios.VTIME] = 0
    termios.tcsetattr(fd, termios.TCSANOW, raw)
    return fd, original


def read_session_frames(fd, buffer, deadline):
    """Collect session frames until the end frame; an error frame (kind 1) also ends it."""
    frames = []
    while True:
        while True:
            start = buffer.find(b'WM')
            if start < 0:
                del buffer[:max(0, len(buffer) - 1)]
                break
            if len(buffer) - start < 6:
                del buffer[:start]
                break
            kind, count = buffer[start + 2], buffer[start + 5]
            if kind == 1:
                length = 12 + 16 * count
                if len(buffer) - start < length:
                    del buffer[:start]
                    break
                frames.append({'kind': 1, 'raw': bytes(buffer[start:start + length]).hex()})
                del buffer[:start + length]
                return frames
            if kind in (2, 3):
                length = 16 + 16 * count
                if len(buffer) - start < length:
                    del buffer[:start]
                    break
                try:
                    frame = decode_session(bytes(buffer[start:start + length]))
                except ValueError:
                    del buffer[:start + 1]
                    continue
                del buffer[:start + length]
                frames.append(frame)
                if frame['kind'] == 3:
                    return frames
                continue
            del buffer[:start + 1]
        if not select.select([fd], [], [], remaining(deadline))[0]:
            raise TimeoutError('session frames stopped before the end frame')
        chunk = os.read(fd, 4096)
        if not chunk:
            raise EOFError('serial input closed during a session')
        buffer.extend(chunk)


def run_session(fd, packet, expected, timeout):
    if packet[:4] != MAGIC or packet[4] not in (1, 2):
        raise ValueError('not a WasMetal upload packet')
    nonce = int.from_bytes(packet[5:13], 'little')
    checksum = int.from_bytes(packet[-4:], 'little')
    deadline = time.monotonic() + timeout
    buffer = bytearray()
    write_all(fd, packet[:33], deadline)
    ready = read_reply(fd, buffer, nonce, deadline)
    if ready['status'] != 'ready':
        raise ValueError('board rejected the session header: ' + ready['status'])
    write_all(fd, packet[33:], deadline)
    committed = read_reply(fd, buffer, nonce, deadline)
    if committed['status'] != 'committed' or committed['checksum'] != checksum:
        raise ValueError('board did not commit the session: ' + committed['status'])
    frames = read_session_frames(fd, buffer, deadline)
    mismatches = []
    if frames[-1]['kind'] != 3:
        mismatches.append({'error_frame': frames[-1]})
    reported = [f for f in frames if f['kind'] == 2]
    for index, (want, got) in enumerate(zip(expected, reported)):
        actual = {k: got[k] for k in ('record', 'status', 'trap', 'values')}
        if actual != want:
            mismatches.append({'report': index, 'expected': want, 'actual': actual})
            if len(mismatches) > 10:
                break
    if len(reported) != len(expected):
        mismatches.append({'reports': len(reported), 'expected_reports': len(expected)})
    return {'status': 'failed' if mismatches else 'passed', 'reports': len(reported), 'mismatches': mismatches}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--device', required=True, help='serial device, e.g. /dev/serial/by-id/...')
    parser.add_argument('--sessions', type=Path, required=True, help='directory of prepared suite sessions')
    parser.add_argument('--baud', type=int, choices=sorted(BAUD), default=9600)
    parser.add_argument('--timeout', type=float, default=3600, help='seconds allowed per session')
    parser.add_argument('--suite', action='append', default=[])
    parser.add_argument('--report', type=Path, default=Path('reports/board-sessions.json'))
    args = parser.parse_args()
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error('timeout must be finite and positive')
    suites = sorted(p.parent for p in args.sessions.rglob('expected.json'))
    if args.suite:
        suites = [s for s in suites if str(s.relative_to(args.sessions)) in set(args.suite)]
    if not suites:
        parser.error('no prepared sessions found')
    results = {}
    fd, original = open_serial(args.device, args.baud)
    try:
        for directory in suites:
            name = str(directory.relative_to(args.sessions))
            started = time.monotonic()
            try:
                result = run_session(fd, (directory/'session.wmu').read_bytes(),
                                     json.loads((directory/'expected.json').read_text()), args.timeout)
            except (OSError, ValueError, TimeoutError, EOFError) as error:
                result = {'status': 'error', 'error': str(error)}
            result['elapsed_seconds'] = time.monotonic() - started
            results[name] = result
            print(result['status'], name, flush=True)
            args.report.parent.mkdir(parents=True, exist_ok=True)
            statuses = [r['status'] for r in results.values()]
            args.report.write_text(json.dumps({
                'device': args.device, 'baud': args.baud, 'physical_hardware_tested': True,
                'summary': {s: statuses.count(s) for s in sorted(set(statuses))},
                'suites': results}, indent=2) + '\n')
    finally:
        try:
            termios.tcsetattr(fd, termios.TCSANOW, original)
        finally:
            os.close(fd)


if __name__ == '__main__':
    main()
