"""Fresh, isolated, hash-bound inputs for one official-suite runner process."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from threading import Lock

from check_spec_conversion import converter_identity, digest, official_sources, payloads, read_json, references, require


class ConversionSession:
    def __init__(self, root, lock, executable):
        self.root, self.lock, self.executable = Path(root), deepcopy(lock), Path(executable)
        self.archive = self.root/'.cache/packages/wasm-tools.tar.gz'
        self.converter = converter_identity(self.archive, self.executable, self.lock['wasm_tools'])
        self.source_dir = self.root/'.cache/upstream'/('spec-'+self.lock['spec']['revision'])/'test/core'
        self.spec_archive = self.root/'.cache/upstream/spec.tar.gz'
        self.sources, self.source_hash = official_sources(self.spec_archive, self.source_dir, self.lock['spec'])
        parent = self.root/'build/spec-inputs'
        parent.mkdir(parents=True, exist_ok=True)
        self.directory = Path(tempfile.mkdtemp(prefix='run-', dir=parent))
        self.entries, self.locks, self.mutex = {}, {}, Lock()

    def suite(self, source):
        name = str(Path(source).relative_to(self.source_dir))
        require(name in self.sources, 'conversion source is not an official script')
        require(digest(source) == self.sources[name], 'conversion source differs from pinned archive: '+name)
        return name

    def convert(self, source):
        name = self.suite(source)
        with self.mutex:
            lock = self.locks.setdefault(name, Lock())
        with lock:
            if name in self.entries:
                self.verify(source)
                return self.directory/'scripts'/Path(name).with_suffix('')/'test.json'
            directory = self.directory/'scripts'/Path(name).with_suffix('')
            directory.mkdir(parents=True)
            target = directory/'test.json'
            command = [str(self.executable), 'json-from-wast', str(source),
                       '--wasm-dir', str(directory), '-o', str(target)]
            result = subprocess.run(command, capture_output=True, text=True, timeout=120)
            log = self.directory/'logs'/Path(name).with_suffix('.json')
            log.parent.mkdir(parents=True, exist_ok=True)
            log.write_text(json.dumps({'command': command, 'returncode': result.returncode,
                                      'stdout': result.stdout, 'stderr': result.stderr}, indent=2)+'\n')
            require(result.returncode == 0, 'fresh official conversion failed: '+name+': '+result.stderr)
            document = read_json(target)
            names = references(document, name, self.lock['spec']['revision'])
            generated = {str(p.relative_to(directory)) for p in directory.rglob('*') if p.is_file()}
            require(generated == names | {'test.json'}, 'unreviewed fresh conversion output inventory')
            modules = payloads(directory, names)
            # Source-directory prefixes are informational and vary across CI workers.
            document['source_filename'] = name
            semantic = hashlib.sha256(json.dumps(document, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
            entry = {'schema': 1, 'identity': {'source_sha256': self.sources[name], 'converter': self.converter,
                     'json_semantic_sha256': semantic, 'payloads': modules}, 'json_sha256': digest(target),
                     'directory': str(directory.relative_to(self.root)),
                     'conversion_log': str(log.relative_to(self.root)), 'conversion_log_sha256': digest(log)}
            self.entries[name] = deepcopy(entry)
            self.verify(source)
            return target

    def verify(self, source, target=None):
        name = self.suite(source)
        require(name in self.entries, 'script was not freshly converted in this process')
        entry = self.entries[name]
        directory = self.root/entry['directory']
        actual_target = directory/'test.json'
        require(target is None or Path(target) == actual_target, 'execution substituted another converted script')
        require(not actual_target.is_symlink() and digest(actual_target) == entry['json_sha256'],
                'converted JSON changed after generation: '+name)
        require(payloads(directory, entry['identity']['payloads']) == entry['identity']['payloads'],
                'converted module changed after generation: '+name)
        require(digest(self.root/entry['conversion_log']) == entry['conversion_log_sha256'],
                'conversion command receipt changed: '+name)
        return deepcopy(entry)

    def verify_all(self):
        require(converter_identity(self.archive, self.executable, self.lock['wasm_tools']) == self.converter,
                'converter changed during test execution')
        require(official_sources(self.spec_archive, self.source_dir, self.lock['spec'])[1] == self.source_hash,
                'official source inventory changed during test execution')
        for name in sorted(self.entries):
            self.verify(self.source_dir/name)


def checked_evidence(suite, expected):
    """Reject missing, altered, or incomplete input evidence in a CI report."""
    entry = suite.get('test_inputs')
    require(isinstance(entry, dict) and type(entry.get('schema')) is int and entry.get('schema') == 1,
            'missing fresh conversion evidence')
    require(entry.get('verified_before_execution') is True and entry.get('verified_after_execution') is True,
            'conversion inputs were not verified around execution')
    require(entry.get('identity') == expected, 'fresh conversion identity mismatch')
    for field in ('json_sha256', 'conversion_log_sha256'):
        value = entry.get(field)
        require(isinstance(value, str) and len(value) == 64 and all(c in '0123456789abcdef' for c in value),
                'invalid conversion artifact hash: '+field)
    for field in ('directory', 'conversion_log'):
        value = entry.get(field)
        require(isinstance(value, str) and value.startswith('build/spec-inputs/')
                and '..' not in Path(value).parts and '\\' not in value and not Path(value).is_absolute(),
                'unsafe conversion artifact path')
    return entry
