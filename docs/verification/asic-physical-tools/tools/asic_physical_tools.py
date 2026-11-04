"""Provision pinned ASIC experiment tools without installing system packages."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

from asic_cells import require, verify_bytes
from prepare_standalone import ROOT, digest
from run_xc7_system import stop_workers

LOCK = ROOT / 'tools/asic_physical.lock.json'
CACHE = ROOT / '.cache/asic-tools'
PDK = ROOT / '.cache/sky130hd-physical'


def download(path, record, url, git=False):
    require(url.startswith('https://'), 'ASIC downloads require HTTPS')
    if not path.exists():
        with urllib.request.urlopen(url, timeout=60) as stream:
            data = stream.read(record['bytes'] + 1)
        require(len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256'],
                'downloaded ASIC input has wrong size or SHA256')
        if git:
            verify_bytes(data, record)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + '.download')
        temporary.write_bytes(data)
        temporary.replace(path)
    require(path.stat().st_size == record['bytes'] and digest(path) == record['sha256'],
            'cached ASIC input changed: ' + str(path))
    if git:
        verify_bytes(path.read_bytes(), record)


def package_tree(package, destination):
    """Check every extracted file against the hash-checked package payload."""
    process = subprocess.Popen(['dpkg-deb', '--fsys-tarfile', str(package)],
        stdout=subprocess.PIPE, start_new_session=True)
    inventory = {}
    try:
        with tarfile.open(fileobj=process.stdout, mode='r|') as archive:
            for member in archive:
                relative = PurePosixPath(member.name)
                require(not relative.is_absolute() and '..' not in relative.parts,
                        'unsafe ASIC package path')
                if str(relative) == '.':
                    continue
                target = destination / str(relative)
                require(target.resolve().is_relative_to(destination.resolve()),
                        'ASIC package path escapes its private directory')
                if member.isdir():
                    require(target.is_dir() and not target.is_symlink(), 'ASIC package directory differs')
                elif member.issym():
                    require(target.is_symlink() and os.readlink(target) == member.linkname,
                            'ASIC package symlink differs')
                    inventory[str(relative)] = {'symlink': member.linkname}
                elif member.isfile():
                    expected = hashlib.file_digest(archive.extractfile(member), 'sha256').hexdigest()
                    require(target.is_file() and not target.is_symlink() and digest(target) == expected,
                            'extracted ASIC package file differs: ' + str(relative))
                    require(target.stat().st_mode & 0o111 == member.mode & 0o111,
                            'ASIC package executable permissions differ')
                    inventory[str(relative)] = {'sha256': expected}
                else:
                    raise ValueError('unsupported special file in ASIC package')
        require(process.wait(timeout=60) == 0, 'cannot read ASIC package payload')
    finally:
        process.stdout.close()
        stop_workers([process])
    present = {str(path.relative_to(destination)) for path in destination.rglob('*')
               if path.is_file() or path.is_symlink()}
    require(present == set(inventory), 'extra or missing files in private ASIC tool directory')
    return inventory


def extract_package(package, destination):
    with tempfile.TemporaryDirectory(prefix='asic-extract-', dir=CACHE) as temporary:
        process = subprocess.Popen(['dpkg-deb', '--fsys-tarfile', str(package)],
            stdout=subprocess.PIPE, start_new_session=True)
        try:
            with tarfile.open(fileobj=process.stdout, mode='r|') as archive:
                archive.extractall(temporary, filter='data')
            require(process.wait(timeout=60) == 0, 'cannot extract ASIC package')
        finally:
            process.stdout.close()
            stop_workers([process])
        inventory = package_tree(package, Path(temporary))
        Path(temporary).rename(destination)
    return inventory


def provision():
    sources = {LOCK}
    for module in tuple(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            path = Path(filename).resolve()
            if path.is_relative_to(ROOT / 'tools') and path.suffix == '.py':
                sources.add(path)
    bound = {str(path.relative_to(ROOT)): digest(path) for path in sources}
    lock = json.loads(LOCK.read_text())
    require(lock['schema_version'] == 1 and platform.machine() == 'x86_64', 'unsupported ASIC tool host')
    require(re.fullmatch('[0-9a-f]{40}', lock['platform_revision']) and
            re.fullmatch('[0-9a-f]{40}', lock['source_revision']), 'moving ASIC source revision')
    require(len({record['name'] for record in lock['packages']}) == len(lock['packages']), 'duplicate ASIC package')
    trees, roots = {}, {}
    for record in lock['packages']:
        require(re.fullmatch(r'[A-Za-z0-9_.+-]+', record['directory']) and
                re.fullmatch(r'[A-Za-z0-9_.+-]+', record['archive']), 'unsafe ASIC package destination')
        package = CACHE / 'downloads' / record['archive']
        download(package, record, record['url'])
        destination = CACHE / record['directory']
        trees[record['name']] = (package_tree(package, destination) if destination.exists()
                                else extract_package(package, destination))
        roots[record['name']] = destination
    names = [record['cache_name'] for record in lock['platform_files']]
    require(len(names) == len(set(names)), 'duplicate physical platform input')
    for record in lock['platform_files']:
        relative = Path(record['cache_name'])
        require(not relative.is_absolute() and '..' not in relative.parts, 'unsafe physical platform path')
        url = 'https://raw.githubusercontent.com/' + '/'.join([
            lock['platform_repository'], lock['platform_revision'], record['path']])
        download(PDK / relative, record, url, git=True)
    executable = roots['openroad'] / 'usr/bin/openroad'
    require(digest(executable) == lock['executable_sha256'], 'OpenROAD executable changed')
    environment = dict(os.environ)
    environment.pop('LD_PRELOAD', None)
    environment.pop('LD_AUDIT', None)
    environment['LD_LIBRARY_PATH'] = ':'.join(map(str, [
        roots['libqt5charts5'] / 'usr/lib/x86_64-linux-gnu',
        roots['tcl-tclreadline'] / 'usr/lib/x86_64-linux-gnu',
        roots['openroad'] / 'opt/or-tools/lib']))
    environment['TCLLIBPATH'] = str(roots['tcl-tclreadline'] / 'usr/lib/tcltk/x86_64-linux-gnu')
    libraries = subprocess.run(['ldd', str(executable)], env=environment,
        capture_output=True, text=True, check=True, timeout=30).stdout
    require('not found' not in libraries, 'missing host OpenROAD runtime dependencies:\n' + libraries)
    loaded = sorted(set(re.findall(r'(?:=>\s+|^\s*)(/[^\s]+)\s+\(', libraries, re.M)))
    library_hashes = {path: digest(Path(path)) for path in loaded}
    result = subprocess.run([str(executable), '-version'], env=environment,
        capture_output=True, text=True, check=True, timeout=30)
    require(not result.stderr and result.stdout.strip() == lock['packages'][0]['version'],
            'unexpected OpenROAD version or initialization diagnostic')
    for name, expected in bound.items():
        require(digest(ROOT / name) == expected, 'ASIC provisioning source changed: ' + name)
    for name, expected in library_hashes.items():
        require(digest(Path(name)) == expected, 'OpenROAD runtime library changed: ' + name)
    report = {'status': 'passed', 'lock_sha256': digest(LOCK), 'version': result.stdout.strip(),
        'inputs': bound,
        'executable_sha256': digest(executable), 'loaded_libraries': library_hashes,
        'package_trees': {name: {'files': len(tree), 'sha256': hashlib.sha256(
            json.dumps(tree, sort_keys=True, separators=(',', ':')).encode()).hexdigest()}
            for name, tree in trees.items()},
        'platform_files_verified': len(names), 'system_packages_installed': False,
        'host_runtime_note': 'Other OpenROAD runtime dependencies must exist on the host; every resolved shared library is fingerprinted.'}
    return executable, environment, report


if __name__ == '__main__':
    destination = ROOT / 'reports/asic-physical-tools.json'
    destination.parent.mkdir(exist_ok=True)
    destination.unlink(missing_ok=True)
    _, _, report = provision()
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print('PASS pinned OpenROAD executable, package payloads and physical platform inputs')
