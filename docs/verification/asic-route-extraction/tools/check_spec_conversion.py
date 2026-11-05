#!/usr/bin/env python3
"""Independently regenerate the complete pinned official-script conversion cache.

This is a post-run input audit, not an RTL test run or historical attestation.
It reads the existing cache without modifying it. Only the informational
absolute source-directory prefix may differ between the two JSON documents.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tarfile
import tempfile
import time

ROOT = Path(__file__).resolve().parent.parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: '+key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(), object_pairs_hook=unique_object)


def converter_identity(archive_path, executable, record):
    require(digest(archive_path) == record['sha256'], 'converter archive checksum mismatch')
    with tarfile.open(archive_path) as archive:
        entries = [entry for entry in archive if entry.isfile() and PurePosixPath(entry.name).name == 'wasm-tools']
        require(len(entries) == 1, 'converter archive executable inventory mismatch')
        expected = hashlib.sha256(archive.extractfile(entries[0]).read()).hexdigest()
    require(digest(executable) == expected, 'installed converter differs from pinned release')
    return {'archive_sha256': record['sha256'], 'executable_sha256': expected,
            'archive_member': entries[0].name, 'version': record['version']}


def official_sources(archive_path, source_dir, record):
    require(digest(archive_path) == record['sha256'], 'official source archive checksum mismatch')
    expected = {}
    with tarfile.open(archive_path) as archive:
        for entry in archive:
            marker = '/test/core/'
            if entry.isfile() and marker in entry.name and entry.name.endswith('.wast'):
                name = entry.name.split(marker, 1)[1]
                require(name not in expected, 'duplicate official source in archive')
                expected[name] = hashlib.sha256(archive.extractfile(entry).read()).hexdigest()
    actual = {str(path.relative_to(source_dir)): digest(path) for path in source_dir.rglob('*.wast')}
    require(expected and actual == expected, 'official source tree differs from pinned archive')
    return expected, hashlib.sha256(json.dumps(expected, sort_keys=True).encode()).hexdigest()


def references(document, suite, revision):
    require(set(document) == {'source_filename', 'commands'}, 'unreviewed converted JSON fields')
    filename = document['source_filename']
    suffix = '/spec-'+revision+'/test/core/'+suite
    require(isinstance(filename, str) and filename.endswith(suffix), 'converted script source identity mismatch')
    require(isinstance(document['commands'], list), 'converted commands must be a list')
    names = set()

    def visit(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key in {'filename', 'binary_filename'}:
                    require(isinstance(item, str) and item not in {'', '.', '..'}
                            and PurePosixPath(item).name == item and '\\' not in item
                            and item.endswith(('.wasm', '.wat')), 'unsafe converted payload filename')
                    names.add(item)
                else:
                    visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    visit(document['commands'])
    return names


def payloads(directory, names):
    result = {}
    for name in sorted(names):
        path = directory/name
        require(path.is_file() and not path.is_symlink(), 'missing or indirect converted payload: '+name)
        result[name] = digest(path)
    return result


def compare(cached, fresh, suite, revision):
    old, new = read_json(cached/'test.json'), read_json(fresh/'test.json')
    old_names, new_names = references(old, suite, revision), references(new, suite, revision)
    require(old['commands'] == new['commands'], 'converted command or expected-value mismatch')
    require(old_names == new_names, 'converted payload inventory mismatch')
    generated = {str(path.relative_to(fresh)) for path in fresh.rglob('*') if path.is_file()}
    require(generated == new_names | {'test.json'}, 'fresh converter emitted unreferenced files')
    old_files, new_files = payloads(cached, old_names), payloads(fresh, new_names)
    require(old_files == new_files, 'converted payload bytes differ')
    return {'suite': suite, 'command_count': len(old['commands']), 'payloads': old_files,
            'cached_json_sha256': digest(cached/'test.json'), 'fresh_json_sha256': digest(fresh/'test.json'),
            'informational_source_prefix_changed': old['source_filename'] != new['source_filename']}


def stamp_matches(path, source_hash, version):
    require(path.read_text() == source_hash+':'+version, 'conversion source/version stamp mismatch')


def controls(base, cached, fresh, suite, revision, archive, executable, converter, source_hash):
    cases = []

    def reject(name, action, expected):
        try:
            action()
        except (ValueError, OSError) as error:
            require(expected in str(error), 'fault rejected for unexpected reason: '+name+': '+str(error))
            cases.append({'name': name, 'rejected': True, 'reason': str(error)})
        else:
            raise ValueError('accepted deliberate conversion defect: '+name)

    names = references(read_json(cached/'test.json'), suite, revision)

    def fixture(name):
        directory = base/'faults'/name
        directory.mkdir(parents=True)
        for item in names | {'test.json', 'source.sha256'}:
            shutil.copyfile(cached/item, directory/item)
        return directory

    def json_fault(name, mutate, expected):
        directory = fixture(name)
        document = read_json(directory/'test.json')
        mutate(document)
        (directory/'test.json').write_text(json.dumps(document))
        reject(name, lambda: compare(directory, fresh, suite, revision), expected)

    def wrong_expected(document):
        command = next(item for item in document['commands'] if item['type'] == 'assert_return' and item.get('expected'))
        command['expected'][0]['value'] = 'deliberately wrong expected value'

    json_fault('wrong-expected-value', wrong_expected, 'command or expected-value mismatch')
    json_fault('missing-command', lambda d: d['commands'].pop(), 'command or expected-value mismatch')
    json_fault('duplicated-command', lambda d: d['commands'].append(deepcopy(d['commands'][0])), 'command or expected-value mismatch')
    json_fault('wrong-script-identity', lambda d: d.update(source_filename='/wrong.wast'), 'source identity mismatch')
    json_fault('unreviewed-json-field', lambda d: d.update(extra=True), 'unreviewed converted JSON fields')

    def wrong_filename(document):
        next(item for item in document['commands'] if 'filename' in item)['filename'] = '../escape.wasm'

    json_fault('escaping-payload-filename', wrong_filename, 'unsafe converted payload filename')
    selected = sorted(names)[0]
    directory = fixture('altered-module')
    path = directory/selected
    path.write_bytes(path.read_bytes()+b'corruption')
    reject('altered-module', lambda: compare(directory, fresh, suite, revision), 'converted payload bytes differ')
    directory2 = fixture('missing-module')
    (directory2/selected).unlink()
    reject('missing-module', lambda: compare(directory2, fresh, suite, revision), 'missing or indirect converted payload')
    directory3 = fixture('indirect-module')
    (directory3/selected).unlink()
    (directory3/selected).symlink_to(cached/selected)
    reject('indirect-module', lambda: compare(directory3, fresh, suite, revision), 'missing or indirect converted payload')
    directory4 = fixture('stale-source-stamp')
    (directory4/'source.sha256').write_text('0'*64+':'+converter['version'])
    reject('stale-source-stamp', lambda: stamp_matches(directory4/'source.sha256', source_hash, converter['version']), 'source/version stamp mismatch')
    altered = dict(converter, sha256='0'*64)
    reject('wrong-converter-archive', lambda: converter_identity(archive, executable, altered), 'archive checksum mismatch')
    binary = base/'faults'/'altered-converter'
    binary.write_bytes(b'not the pinned release executable')
    reject('altered-converter-executable', lambda: converter_identity(archive, binary, converter), 'installed converter differs')
    duplicate = base/'faults'/'duplicate.json'
    duplicate.write_text('{"commands": [], "commands": [1]}')
    reject('duplicate-json-key', lambda: read_json(duplicate), 'duplicate JSON key')
    # Relocation of the informational source prefix must not alter execution data.
    relocated = fixture('relocated-source-prefix')
    document = read_json(relocated/'test.json')
    document['source_filename'] = '/another-root/spec-'+revision+'/test/core/'+suite
    (relocated/'test.json').write_text(json.dumps(document))
    compare(relocated, fresh, suite, revision)
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--label', default='spec-conversion')
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    require(re.fullmatch(r'spec-conversion(?:-[a-z0-9-]{1,64})?', args.label), 'unsafe output label')
    require(1 <= args.jobs <= 16, 'conversion workers must be between 1 and 16')
    started = time.monotonic()
    output = ROOT/'reports'/(args.label+'.json')
    output.unlink(missing_ok=True)
    parent = ROOT/'build'/args.label
    parent.mkdir(parents=True, exist_ok=True)
    base = Path(tempfile.mkdtemp(prefix='replay-', dir=parent))
    lock_path = ROOT/'tools/upstream.lock.json'
    lock = read_json(lock_path)
    converter = lock['wasm_tools']
    archive = ROOT/'.cache/packages/wasm-tools.tar.gz'
    executable = ROOT/'.cache/tools'/('wasm-tools-'+converter['version']+'-x86_64-linux/wasm-tools')
    identity = converter_identity(archive, executable, converter)
    spec_archive = ROOT/'.cache/upstream/spec.tar.gz'
    source_dir = ROOT/'.cache/upstream'/('spec-'+lock['spec']['revision'])/'test/core'
    sources, source_hash = official_sources(spec_archive, source_dir, lock['spec'])
    inputs = {}

    def bind(path):
        # Preserve the lexical cache path: .cache may be a shared workspace symlink.
        inputs[str(path.relative_to(ROOT))] = digest(path)

    for path in (Path(__file__).resolve(), lock_path, archive, executable, spec_archive):
        bind(path)
    for suite, source_digest in sorted(sources.items()):
        cached = ROOT/'build/spec'/Path(suite).with_suffix('')
        stamp_matches(cached/'source.sha256', source_digest, converter['version'])
        names = references(read_json(cached/'test.json'), suite, lock['spec']['revision'])
        payloads(cached, names)
        for path in [source_dir/suite, cached/'test.json', cached/'source.sha256', *[cached/name for name in sorted(names)]]:
            bind(path)

    def replay(suite):
        fresh = base/'fresh'/Path(suite).with_suffix('')
        fresh.mkdir(parents=True)
        command = [str(executable), 'json-from-wast', str(source_dir/suite), '--wasm-dir', str(fresh), '-o', str(fresh/'test.json')]
        result = subprocess.run(command, capture_output=True, text=True, timeout=120)
        log = base/'logs'/Path(suite).with_suffix('.json')
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text(json.dumps({'command': command, 'returncode': result.returncode,
                                   'stdout': result.stdout, 'stderr': result.stderr}, indent=2)+'\n')
        require(result.returncode == 0, 'fresh conversion failed: '+suite+': '+result.stderr)
        return compare(ROOT/'build/spec'/Path(suite).with_suffix(''), fresh, suite, lock['spec']['revision'])

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        rows = list(pool.map(replay, sorted(sources)))
    suite = 'i32.wast'
    faults = controls(base, ROOT/'build/spec/i32', base/'fresh/i32', suite, lock['spec']['revision'],
                      archive, executable, converter, sources[suite])
    for name, expected in inputs.items():
        require(digest(ROOT/name) == expected, 'conversion audit input changed: '+name)
    require(official_sources(spec_archive, source_dir, lock['spec'])[1] == source_hash, 'official source inventory changed')
    require(converter_identity(archive, executable, converter) == identity, 'converter identity changed')
    report = {'status': 'passed', 'scope': 'post-run independent replay of all pinned official script conversions',
              'historical_execution_input_attestation': False, 'existing_cache_unchanged': True,
              'suite_files': len(rows), 'script_commands': sum(row['command_count'] for row in rows),
              'payload_files': sum(len(row['payloads']) for row in rows),
              'official_sources_sha256': source_hash, 'converter': identity,
              'normalization': 'Only the informational absolute source prefix; pinned revision and suite suffix must match.',
              'unreferenced_cache_files': 'Excluded: the runner may create derived .parsed.wasm validation outputs.',
              'negative_controls_rejected': len(faults), 'negative_controls': faults,
              'relocated_source_prefix_control_passed': True, 'inputs': inputs, 'suites': rows,
              'replay_directory': str(base.relative_to(ROOT)), 'elapsed_seconds': time.monotonic()-started}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2)+'\n')
    print('PASS', len(rows), 'scripts;', report['payload_files'], 'payloads;', len(faults), 'fault controls', flush=True)


if __name__ == '__main__':
    main()
