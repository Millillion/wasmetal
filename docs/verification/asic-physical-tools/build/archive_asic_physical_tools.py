"""Archive the verified physical-tool inputs without redistributing binaries."""
from pathlib import Path
import gzip
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from prepare_standalone import digest
from asic_cells import verify_bytes

report_path = ROOT / 'reports/asic-physical-tools.json'
report = json.loads(report_path.read_text())
assert report['status'] == 'passed' and not report['system_packages_installed']
lock_path = ROOT / 'tools/asic_physical.lock.json'
assert digest(lock_path) == report['lock_sha256']
lock = json.loads(lock_path.read_text())
assert report['version'] == lock['packages'][0]['version']
assert sum(tree['files'] for tree in report['package_trees'].values()) == 11632
assert len(report['loaded_libraries']) == 133
files = {report_path, lock_path, Path(__file__).resolve(),
    ROOT / '.github/workflows/rtl.yml', ROOT / 'build/asic-physical-tools.log',
    ROOT / 'build/asic-physical-workflow-lint.log'}
for name, sha in report['inputs'].items():
    assert digest(ROOT / name) == sha, name
    files.add(ROOT / name)
for name, sha in report['loaded_libraries'].items():
    assert digest(Path(name)) == sha, name
for record in lock['platform_files']:
    path = ROOT / '.cache/sky130hd-physical' / record['cache_name']
    verify_bytes(path.read_bytes(), record)
    files.add(path)
for record in lock['packages']:
    path = ROOT / '.cache/asic-tools/downloads' / record['archive']
    assert digest(path) == record['sha256'] and path.stat().st_size == record['bytes']
    files.add(ROOT / '.cache/asic-tools' / record['directory'] / 'usr/share/doc' / record['name'] / 'copyright')
files.update({ROOT / '.cache/sky130hd/ORFS_LICENSE', ROOT / '.cache/sky130hd/SKYWATER_LICENSE'})
assert 'PASS pinned OpenROAD' in (ROOT / 'build/asic-physical-tools.log').read_text()
assert not (ROOT / 'build/asic-physical-workflow-lint.log').read_text()
destination = ROOT / 'docs/verification/asic-physical-tools'
destination.mkdir(parents=True, exist_ok=True)
index = []
for path in sorted(files):
    relative = path.relative_to(ROOT)
    if relative.parts[0] == '.cache':
        relative = Path('upstream').joinpath(*relative.parts[1:])
    raw = path.read_bytes()
    compressed = len(raw) > 262144
    target = destination / relative
    if compressed:
        target = Path(str(target) + '.gz')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(gzip.compress(raw, mtime=0) if compressed else raw)
    assert (gzip.decompress(target.read_bytes()) if compressed else target.read_bytes()) == raw
    index.append({'original_path': str(path.relative_to(ROOT)), 'archive_path': str(target.relative_to(ROOT)),
        'original_sha256': digest(path), 'archive_sha256': digest(target), 'compressed': compressed})
(destination / 'index.json').write_text(json.dumps(index, indent=2) + '\n')
(ROOT / 'docs/verification/asic-physical-tools.json').write_bytes(report_path.read_bytes())
for name, sha in report['inputs'].items():
    assert digest(ROOT / name) == sha, name
print('PASS physical-tool archive:', len(index), 'artifacts;',
      sum((ROOT / row['archive_path']).stat().st_size for row in index), 'bytes')
