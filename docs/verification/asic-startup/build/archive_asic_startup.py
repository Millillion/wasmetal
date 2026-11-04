"""Archive the complete startup circuit campaign and its independent cell check."""
from pathlib import Path
import gzip
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from prepare_standalone import digest
from check_memory_startup import CONFIGURATIONS, TOP

report_path = ROOT / 'reports/asic-startup.json'
models_path = ROOT / 'reports/asic-cell-models.json'
report = json.loads(report_path.read_text())
models = json.loads(models_path.read_text())
assert report['status'] == models['status'] == 'passed'
assert report['backend'] == 'mapped-sky130hd-functional'
assert report['negative_controls_rejected'] == 14
assert models['negative_controls_rejected'] == 3
assert {(c['ram_bytes'], c['read_latency'], c['response_timeout']) for c in report['checks']} == set(CONFIGURATIONS)
assert len(report['checks']) == len(CONFIGURATIONS) == 6
selected = sorted({name for check in report['checks'] for name in check['standard_cells']})
assert selected == models['mapped_types_checked'] == models['cell_types']
bound = dict(report['inputs'])
for name, sha in models['inputs'].items():
    assert name not in bound or bound[name] == sha, name
    bound[name] = sha
files = {report_path, models_path, Path(__file__).resolve(), ROOT / '.github/workflows/rtl.yml',
    ROOT / 'tests/asic_cell_source_test.py'}
for name, sha in bound.items():
    assert digest(ROOT / name) == sha, name
    if not name.startswith('.cache/tools/'):
        files.add(ROOT / name)
totals = {}
circuits = []
for check in report['checks']:
    size, latency, timeout = check['ram_bytes'], check['read_latency'], check['response_timeout']
    directory = ROOT / 'build/asic-startup' / f'{size}-{latency}-{timeout}'
    assert digest(directory / 'mapped.json') == check['netlist_sha256']
    assert digest(directory / 'cells.v') == check['functional_models_sha256']
    for key, filename in [('reset_pin_log_sha256', 'reset-pins.log'),
                          ('reset_point_log_sha256', 'reset-points.log'),
                          ('induction_log_sha256', 'equivalence.log')]:
        assert digest(directory / filename) == check['proofs'][key]
    assert check['proofs']['inductive_equivalence'] and check['proofs']['reset_base_cycles'] == 12
    for kind, subdirectory in [('rtl', directory / 'native'), ('standard_cells', directory)]:
        test = check['tests'][kind]
        assert digest(subdirectory / 'obj' / ('V' + TOP)) == test['binary_sha256']
        log = directory / (kind + '-observations.log')
        assert digest(log) == test['log_sha256']
        assert json.loads(log.read_text()) == test['observations']
    observation = check['tests']['rtl']['observations']
    assert observation == check['tests']['standard_cells']['observations']
    for key, value in observation.items():
        if key not in ('trace', 'status'):
            totals[key] = totals.get(key, 0) + value
    circuits.append({'ram_bytes': size, 'read_latency': latency, 'response_timeout': timeout,
        'standard_cells': sum(check['standard_cells'].values()),
        'flip_flops': check['standard_cells'].get('sky130_fd_sc_hd__dfxtp_1', 0),
        'cycles': observation['cycles']})
assert totals['cycles'] == 59107887
base = ROOT / 'build/asic-cell-models'
for label, record in [('positive', models['positive']), *[(r['name'], r) for r in models['negative_controls']]]:
    source = base / ('derived.v' if label == 'positive' else label + '.v')
    for path, key in [(source, 'source_sha256'), (base / (label + '.vvp'), 'binary_sha256'),
                      (base / (label + '.log'), 'log_sha256')]:
        assert digest(path) == record[key]
assert digest(base / 'testbench.sv') == models['testbench_sha256']
for directory in (ROOT / 'build/asic-startup', base, ROOT / 'build/asic-startup-initial-trial'):
    for path in directory.rglob('*'):
        if path.is_file() and not any(part.startswith('obj') for part in path.parts) and path.suffix in {
            '.v', '.sv', '.vlt', '.ys', '.log', '.json', '.lib', '.enc', '.il', '.py', '.vvp'}:
            files.add(path)
for name in ('asic-startup-driver.log', 'asic-startup-cell-models.log',
             'asic-startup-cell-source-fixtures.log', 'asic-startup-workflow-lint.log',
             'asic-startup-negative-preflight.log', 'asic-startup-initial-cell-inventory.log'):
    files.add(ROOT / 'build' / name)
fixtures = (ROOT / 'build/asic-startup-cell-source-fixtures.log').read_text()
assert 'Ran 7 tests' in fixtures and 'OK' in fixtures
assert not (ROOT / 'build/asic-startup-workflow-lint.log').read_text()
summary = {'status': 'passed', 'scope': report['scope'], 'backend': report['backend'],
    'configurations': circuits, 'totals_per_model': totals,
    'inductive_equivalence_checks': 6, 'independent_reset_pin_checks': 6,
    'comparison_point_reset_base_checks': 6, 'reset_base_cycles': 12,
    'circuit_fault_controls_rejected': 14, 'upstream_cell_types_checked': len(selected),
    'combinational_cell_vectors': models['combinational_vectors'],
    'binary_flip_flop_transitions': models['flip_flop_transitions'],
    'flip_flop_seed_and_hold_checks': models['flip_flop_seed_and_hold_checks'],
    'cell_model_faults_rejected': 3, 'source_inventory_fixtures_passed': 7,
    'frozen_inputs_rechecked': len(bound), 'functional_report_sha256': digest(report_path),
    'independent_cell_report_sha256': digest(models_path),
    'physical_hardware_tested': False, 'physical_timing_or_routing_included': False,
    'initial_incomplete_trial': 'All six normal cases matched, but a negative-test build warning stopped the first attempt; its source and failure logs are retained. The complete campaign was rerun after fixing that test setup.'}
summary_path = ROOT / 'reports/asic-startup-summary.json'
summary_path.write_text(json.dumps(summary, indent=2) + '\n')
files.add(summary_path)
notices = ROOT / 'build/asic-startup-notices'
notices.mkdir(exist_ok=True)
for package in ('yosys', 'iverilog', 'verilator'):
    origin = ROOT / '.cache/tools/usr/share/doc' / package / 'copyright'
    target = notices / (package.upper() + '_COPYRIGHT')
    shutil.copyfile(origin, target)
    files.add(target)
destination = ROOT / 'docs/verification/asic-startup'
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
for source, name in [(report_path, 'asic-startup'), (summary_path, 'asic-startup-summary'),
                     (models_path, 'asic-startup-cell-models')]:
    (ROOT / 'docs/verification' / (name + '.json')).write_bytes(source.read_bytes())
for name, sha in bound.items():
    assert digest(ROOT / name) == sha, name
print('PASS ASIC startup archive:', len(index), 'artifacts;', len(bound), 'bound inputs;',
      sum((ROOT / row['archive_path']).stat().st_size for row in index), 'bytes')
