#!/usr/bin/env python3
"""Exercise the bank wrapper against unchanged, pinned OpenRAM behavioral RTL.

This is functional simulation, not characterized SRAM timing or physical closure.
"""
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import time
import urllib.request

from asic_cells import require, verify_bytes
from bootstrap import PACKAGES
from prepare_standalone import ROOT, digest

BASE = ROOT / 'build/sky130-sram'
CACHE = ROOT / '.cache/sky130-sram'
LOCK = ROOT / 'tools/sky130_sram.lock.json'
WRAPPER = ROOT / 'soc/asic/wasmetal_sky130_sram.sv'
BENCH = ROOT / 'tests/memory/sky130_sram.sv'
TOP = 'sky130_sram_tb'
CONFIGURATIONS = ((8192, 1, 9, 65535), (16384, 3, 3, 65535),
                  (24576, 2, 5, 255), (131072, 3, 3, 255))


def upstream():
    lock = json.loads(LOCK.read_text())
    require(lock['schema_version'] == 1 and re.fullmatch('[0-9a-f]{40}', lock['revision']),
            'unpinned SRAM source')
    macro = lock['macro']
    require(re.fullmatch('sky130_sram_[a-z0-9_]+', macro), 'invalid macro name')
    require([r['path'] for r in lock['files']] == [macro + '/' + macro + '.v', 'LICENSE'],
            'unexpected SRAM model inventory')
    paths = []
    for record in lock['files']:
        path = CACHE / record['path']
        if not path.exists():
            url = 'https://raw.githubusercontent.com/' + '/'.join([
                lock['repository'], lock['revision'], record['path']])
            with urllib.request.urlopen(url, timeout=60) as stream:
                data = stream.read(record['bytes'] + 1)
            verify_bytes(data, record)
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary = path.with_name(path.name + '.download')
            temporary.write_bytes(data)
            temporary.replace(path)
        require(not path.is_symlink(), 'SRAM model must be a regular file')
        verify_bytes(path.read_bytes(), record)
        paths.append(path)
    require(not re.search(r'\$(system|fopen|readmem[hb]|fwrite|fdisplay)\b|`include',
                          paths[0].read_text()), 'unbound model operation/include')
    return lock, paths


def tools_identity():
    """Verify installed Icarus/Verilator payloads against their pinned packages.

    The shared tool directory also contains Yosys and other legitimate tools;
    this checks each selected package's members, not an exclusive directory.
    """
    records, paths = {}, []
    for filename, (_, expected) in PACKAGES.items():
        if not filename.startswith(('iverilog_', 'verilator_')):
            continue
        package = ROOT / '.cache/packages' / filename
        require(digest(package) == expected, 'tool package changed: ' + filename)
        paths.append(package)
        payload = subprocess.run(['dpkg-deb', '--fsys-tarfile', str(package)],
                                 check=True, capture_output=True, timeout=60).stdout
        inventory = {}
        with tarfile.open(fileobj=io.BytesIO(payload)) as archive:
            for member in archive:
                relative = Path(member.name)
                require(not relative.is_absolute() and '..' not in relative.parts,
                        'unsafe tool package member')
                target = ROOT / '.cache/tools' / relative
                if member.isfile():
                    sha = hashlib.file_digest(archive.extractfile(member), 'sha256').hexdigest()
                    require(target.is_file() and not target.is_symlink() and digest(target) == sha,
                            'installed tool differs: ' + str(relative))
                    require(target.stat().st_mode & 0o111 == member.mode & 0o111,
                            'tool executable mode differs')
                    inventory[str(relative)] = {'sha256': sha}
                    paths.append(target)
                elif member.issym():
                    require(target.is_symlink() and os.readlink(target) == member.linkname,
                            'tool symlink differs')
                    inventory[str(relative)] = {'symlink': member.linkname}
                else:
                    require(member.isdir(), 'unsupported tool package member')
        records[filename] = {'archive_sha256': expected, 'members': inventory}
    link = ROOT / '.cache/tools/usr/share/verilator/bin/verilator_bin'
    target = ROOT / '.cache/tools/usr/bin/verilator_bin'
    require(link.is_symlink() and link.resolve() == target.resolve(),
            'unexpected Verilator bootstrap link')
    records['verilator_bootstrap_link'] = {'symlink': os.readlink(link), 'target_sha256': digest(target)}
    paths.append(link)
    return records, paths


def run(command, log, environment=None, timeout=600):
    with log.open('w') as stream:
        result = subprocess.run(command, cwd=ROOT, env=environment, stdout=stream,
                                stderr=subprocess.STDOUT, timeout=timeout)
    return result.returncode


def result(log, simulator, configuration):
    text = log.read_text()
    match = re.search(r'^PASS vendor SRAM adapter bytes=(\d+) latency=(\d+) masks=(\d+) '
                      r'transactions=(\d+) commands=(\d+) resets=(\d+)$', text, re.M)
    require(match is not None, 'missing complete SRAM result: ' + str(log))
    size, latency, masks, transactions, commands, resets = map(int, match.groups())
    expected_size, expected_latency, delay, expected_masks = configuration
    require((size, latency, masks) == (expected_size, expected_latency, expected_masks),
            'wrong SRAM configuration completed')
    extra = int(simulator == 'icarus')  # Four-state initial unknown-data read.
    require(transactions == 3 * (size // 16) + 2 * masks + 5 + extra and
            commands == transactions - 3 and resets == 2, 'incomplete SRAM operation counts')
    return {'simulator': simulator, 'ram_bytes': size, 'read_latency': latency,
            'model_delay_ns': delay, 'model_hold_ns': 1, 'clock_period_ns': 20,
            'nonzero_write_masks': masks, 'transactions': transactions,
            'macro_commands': commands, 'resets': resets,
            'initial_unknown_read_checked': simulator == 'icarus',
            'log': str(log.relative_to(ROOT)), 'log_sha256': digest(log)}


def icarus(source, model, name, configuration):
    binary, log = BASE / (name + '.vvp'), BASE / (name + '.log')
    command = [str(ROOT / '.cache/tools/usr/bin/iverilog'),
        '-B' + str(ROOT / '.cache/tools/usr/lib/x86_64-linux-gnu/ivl'), '-g2012',
        '-DWASMETAL_SKY130_SRAM_MODEL', '-s', TOP, '-o', str(binary)]
    for key, value in zip(('RAM_BYTES', 'READ_LATENCY', 'MODEL_DELAY', 'MASK_LIMIT'), configuration):
        command.append(f'-P{TOP}.{key}={value}')
    command += [str(BENCH), str(ROOT / 'soc/asic/wasmetal_sram_memory.sv'), str(source), str(model)]
    require(run(command, BASE / (name + '-build.log')) == 0, 'Icarus build failed: ' + name)
    code = run([str(ROOT / '.cache/tools/usr/bin/vvp'), str(binary)], log)
    return code, log, binary


def verilator(model, configuration):
    size, latency, delay, masks = configuration
    name = f'verilator-{size}-{latency}'
    directory = BASE / name
    environment = dict(os.environ)
    environment['VERILATOR_ROOT'] = str(ROOT / '.cache/tools/usr/share/verilator')
    for key in ('LD_PRELOAD', 'LD_AUDIT', 'MAKEFLAGS', 'CXXFLAGS', 'CPPFLAGS',
                'CPATH', 'CPLUS_INCLUDE_PATH', 'CXX', 'CC'):
        environment.pop(key, None)
    command = [str(ROOT / '.cache/tools/usr/bin/verilator'), '--binary', '--timing',
        '--timescale-override', '1ns/1ps', '--top-module', TOP,
        '--Mdir', str(directory), '-j', '2', '-Wno-DECLFILENAME', '-Wno-TIMESCALEMOD',
        '-Wno-PINCONNECTEMPTY', '-DWASMETAL_SKY130_SRAM_MODEL']
    command += [f'-G{key}={value}' for key, value in zip(
        ('RAM_BYTES', 'READ_LATENCY', 'MODEL_DELAY', 'MASK_LIMIT'), configuration)]
    command += [str(BENCH), str(ROOT / 'soc/asic/wasmetal_sram_memory.sv'), str(WRAPPER), str(model)]
    require(run(command, BASE / (name + '-build.log'), environment) == 0,
            'Verilator build failed: ' + name)
    binary = directory / ('V' + TOP)
    log = BASE / (name + '.log')
    require(run([str(binary)], log, environment) == 0, 'Verilator execution failed: ' + name)
    record = result(log, 'verilator', configuration)
    record['binary_sha256'] = digest(binary)
    return record


def fault_controls(model):
    original = WRAPPER.read_text()
    mutations = {
        'lost-read-hold': ('assign rdata = pending ? sampled : held;', 'assign rdata = sampled;'),
        'wrong-byte-lanes': ('.wmask0(byte_enable[lane*4+:4])', '.wmask0(byte_enable[(3-lane)*4+:4])'),
        'wrong-bank': ("(32'(address) >> 9) == bank", "(32'(address) >> 9) == 0"),
        'wrong-read-hold-edge': ('if (pending) held <= sampled;', 'if (enable) held <= sampled;'),
        'wrong-macro-clock': ('.clk0(clk)', '.clk0(!clk)'),
    }
    rejected = []
    for name, (before, after) in mutations.items():
        require(original.count(before) == 1, 'ambiguous SRAM mutation: ' + name)
        source = BASE / (name + '.sv')
        source.write_text(original.replace(before, after))
        code, log, binary = icarus(source, model, name, (16384, 3, 3, 255))
        require(code != 0 and 'read differs' in log.read_text(),
                'SRAM circuit fault escaped: ' + name)
        rejected.append({'name': name, 'exit_code': code, 'log_sha256': digest(log),
                         'mutant_sha256': digest(source), 'binary_sha256': digest(binary)})
        print('REJECT ' + name, flush=True)
    name = 'read-beyond-capture-window'
    code, log, binary = icarus(WRAPPER, model, name, (16384, 3, 12, 255))
    require(code != 0 and 'read differs' in log.read_text(), 'late macro response escaped')
    rejected.append({'name': name, 'model_delay_ns': 12, 'exit_code': code,
                     'log_sha256': digest(log), 'binary_sha256': digest(binary)})
    return rejected


def main():
    started = time.monotonic()
    BASE.mkdir(parents=True, exist_ok=True)
    output = ROOT / 'reports/sky130-sram.json'
    output.parent.mkdir(exist_ok=True)
    output.unlink(missing_ok=True)
    (BASE / 'progress.json').write_text(json.dumps({'status': 'incomplete', 'phase': 'verify-inputs'}) + '\n')
    lock, vendor = upstream()
    tool_record, tool_paths = tools_identity()
    paths = {LOCK, WRAPPER, BENCH, ROOT / 'soc/asic/wasmetal_sram_memory.sv',
             ROOT / 'tools/upstream.lock.json', *vendor, *tool_paths}
    for module in tuple(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            path = Path(filename).resolve()
            if path.is_relative_to(ROOT / 'tools') and path.suffix == '.py':
                paths.add(path)
    bound = {str(path.relative_to(ROOT)): digest(path) for path in sorted(paths)}
    (BASE / 'tool-payloads.json').write_text(json.dumps(tool_record, indent=2) + '\n')
    checks = []
    for configuration in CONFIGURATIONS:
        name = f'icarus-{configuration[0]}-{configuration[1]}'
        code, log, binary = icarus(WRAPPER, vendor[0], name, configuration)
        require(code == 0, 'Icarus execution failed: ' + name)
        record = result(log, 'icarus', configuration)
        record['binary_sha256'] = digest(binary)
        checks.append(record)
        (BASE / 'progress.json').write_text(json.dumps({'status': 'incomplete', 'checks': checks}, indent=2) + '\n')
        print('PASS ' + name, flush=True)
    for configuration in CONFIGURATIONS[:2]:
        checks.append(verilator(vendor[0], configuration))
        print(f'PASS verilator-{configuration[0]}-{configuration[1]}', flush=True)
    rejected = fault_controls(vendor[0])
    require(all(digest(ROOT / name) == sha for name, sha in bound.items()),
            'SRAM verification inputs changed during execution')
    require(tools_identity()[0] == tool_record and upstream()[0] == lock,
            'SRAM tool/model identity changed during execution')
    report = {'status': 'passed', 'scope': 'bank wrapper and real adapter with pinned upstream behavioral SRAM',
        'upstream': lock, 'inputs': bound, 'checks': checks, 'negative_controls_rejected': rejected,
        'tool_payloads_sha256': digest(BASE / 'tool-payloads.json'),
        'elapsed_seconds': time.monotonic() - started,
        'vendor_model_modified': False, 'timing_delays_are_characterized': False,
        'complete_cpu_macro_integration': False, 'physical_hardware_tested': False,
        'physical_timing_accepted': False, 'fabrication_ready': False}
    output.write_text(json.dumps(report, indent=2) + '\n')
    (BASE / 'progress.json').write_text(json.dumps({'status': 'passed', 'checks': checks}, indent=2) + '\n')
    print('PASS upstream SRAM models: six configurations and six negative controls', flush=True)


if __name__ == '__main__':
    main()
