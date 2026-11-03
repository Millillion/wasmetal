"""Shared standalone profile bindings and immutable image checks."""
import json
from pathlib import Path
from prepare_standalone import ROOT, digest, load_profile


def parameters(profile):
    p = dict(profile['core'])
    p.update({k.upper(): v for k, v in profile.items() if k not in
              ('core', 'memory_pages', 'table_slots')})
    return p


def generate_parameters():
    path = ROOT/'build/standalone_parameters.svh'
    path.parent.mkdir(parents=True, exist_ok=True)
    text = '// Generated from soc/profile.json.\n' + ',\n'.join(
        f'.{name}({value})' for name, value in parameters(load_profile()).items()) + '\n'
    if not path.exists() or path.read_text() != text:
        path.write_text(text)
    return path


def verify_image(directory):
    manifest = json.loads((directory/'manifest.json').read_text())
    if manifest['format'] != 'wasmetal-standalone-v1' or manifest['profile'] != load_profile():
        raise ValueError('prepared image has the wrong format or hardware profile')
    required = {'code.hex','functions.hex','types.hex','regions.hex','boot.hex',
                'program.wasm','initialization.txt'}
    if set(manifest['files']) != required:
        raise ValueError('prepared image is incomplete')
    for name, value in manifest['files'].items():
        if digest(directory/name) != value:
            raise ValueError('prepared image hash mismatch: '+name)
    for name, value in manifest['preparation_inputs'].items():
        path=Path(name)
        if path.is_absolute() or '..' in path.parts or digest(ROOT/path) != value:
            raise ValueError('prepared image loader has changed: '+name)
    return manifest


def verify_simulator(binary):
    manifest = json.loads(Path(str(binary)+'.build.json').read_text())
    if digest(binary) != manifest['binary_sha256']:
        raise ValueError('standalone simulator binary has changed')
    for name, value in manifest['inputs'].items():
        path=Path(name)
        if path.is_absolute() or '..' in path.parts or digest(ROOT/path) != value:
            raise ValueError('standalone simulator input has changed: '+name)
    return manifest
