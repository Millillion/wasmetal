#!/usr/bin/env python3
"""Exercise the board session runner against a fake board on a pseudo-terminal."""
import binascii
import json
import os
from pathlib import Path
import pty
import struct
import sys
import threading
import tty

sys.path.insert(0, str(Path(__file__).resolve().parent.parent/'tools'))
import board_sessions  # noqa: E402
from program_upload import MAGIC, REPLY_MAGIC  # noqa: E402


def reply(status, nonce, checksum=0):
    body = struct.pack('<BBQI', 1, status, nonce, checksum)
    return REPLY_MAGIC + body + struct.pack('<H', binascii.crc_hqx(body, 0xffff))


def frame(kind, record, values=(), status=0, trap=0, cycles=7):
    body = bytes([kind, status, trap, len(values)]) + struct.pack('<II', cycles, record)
    body += b''.join(v.to_bytes(16, 'little') for v in values)
    return b'WM' + body + struct.pack('<H', binascii.crc_hqx(body, 0xffff))


def packet(nonce):
    payload = struct.pack('<5I', 1, 0, 0, 0, 0) + bytes(36)
    header = MAGIC + struct.pack('<BQ16sI', 2, nonce, bytes(16), len(payload))
    checksum = binascii.crc32(header[4:] + payload)
    return header + payload + struct.pack('<I', checksum), checksum


def fake_board(master, nonce, checksum, length, frames):
    received = bytearray()
    while len(received) < 33:
        received += os.read(master, 4096)
    os.write(master, reply(0, nonce))
    while len(received) < 33 + length + 4:
        received += os.read(master, 4096)
    os.write(master, reply(1, nonce, checksum) + b''.join(frames))


def run(frames, expected, timeout=5):
    master, slave = pty.openpty()
    tty.setraw(slave)
    name = os.ttyname(slave)
    data, checksum = packet(0x1234)
    worker = threading.Thread(target=fake_board, args=(master, 0x1234, checksum, len(data) - 37, frames))
    worker.start()
    fd, original = board_sessions.open_serial(name, 9600)
    try:
        return board_sessions.run_session(fd, data, expected, timeout)
    except TimeoutError as error:
        return {'status': 'timeout', 'error': str(error)}
    finally:
        os.close(fd)
        worker.join(timeout=5)
        os.close(master)
        os.close(slave)


def main():
    expected = [{'record': 3, 'status': 0, 'trap': 0, 'values': [42]},
                {'record': 5, 'status': 1, 'trap': 4, 'values': []}]
    good = [frame(2, 3, [42]), frame(2, 5, status=1, trap=4), frame(3, 6)]
    cases = {
        'passes': (good, 'passed'),
        'wrong-value': ([frame(2, 3, [43]), good[1], good[2]], 'failed'),
        'missing-frame': ([good[0], good[2]], 'failed'),
        'error-frame': ([good[0], b'WM\x01\x02\xfe\x00' + bytes(6)], 'failed'),
        'corrupt-then-valid': ([good[0][:-1] + bytes([good[0][-1] ^ 1]), good[0], good[1], good[2]], 'passed'),
        'no-end-frame': (good[:2], 'timeout'),
    }
    results = {}
    for name, (frames, want) in cases.items():
        result = run(frames, expected, timeout=2 if want == 'timeout' else 5)
        assert result['status'] == want, (name, result)
        results[name] = result['status']
    print(json.dumps({'status': 'passed', 'cases': results}))


if __name__ == '__main__':
    main()
