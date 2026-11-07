#!/usr/bin/env python3
"""Archive the routed startup-block closure, its functional check and earlier repair trials."""
from collections import Counter
import gzip
import json
from pathlib import Path
import shutil

from prepare_standalone import ROOT, digest

ARCHIVE = ROOT/'docs/verification/asic-route-closure'
SUMMARY = ROOT/'docs/verification/asic-route-closure-summary.json'
LARGE = 500_000
# Small records of the first repair trial and the interrupted jumper trial.
TRIALS = {'build/asic-routing-repair': ('status.json', 'repair.tcl', 'repair.log', 'antennas.rpt', 'electrical.rpt',
                                        'global-antennas.rpt', 'drc.rpt', 'timing-paths.rpt'),
          'build/asic-routing-repair-v2': ('status.json', 'repair.tcl', 'repair.log', 'global-antennas.rpt')}
SCRATCH = ('build/run_asic_physical_repair.py', 'build/run_asic_physical_repair_v2.py',
           'build/asic-routing-repair-driver.log')


def main():
    route = ROOT/'build/asic-route-closure'
    status = json.loads((route/'status.json').read_text())
    functional_path = ROOT/'reports/asic-route-closure-functional.json'
    cells_path = ROOT/'reports/asic-route-closure-functional-cells.json'
    functional = json.loads(functional_path.read_text())
    cells = json.loads(cells_path.read_text())
    assert status['status'] == 'diagnostic-completed' and status['inputs_unchanged']
    assert functional['status'] == 'passed' and functional['route_status_sha256'] == digest(route/'status.json')
    assert cells['status'] == 'passed'
    for name, value in status['artifacts'].items():
        assert digest(route/name) == value, name
    for name, value in {**functional['inputs'], **cells['inputs']}.items():
        assert digest(ROOT/name) == value, name
    if ARCHIVE.exists():
        raise SystemExit(f'refusing to overwrite {ARCHIVE}')
    files = [route/name for name in sorted(status['artifacts'])] + [route/'status.json']
    files += [ROOT/'build/asic-route-closure-driver.log', ROOT/'build/asic-route-closure-functional-driver.log',
              functional_path, cells_path]
    work = ROOT/'build/asic-route-closure-functional'
    files += [work/name for name in ('mapped.json', 'cells.v', 'logic-models.v', 'equivalence.log', 'reset-points.log',
                                     'reset-pins.log', 'acyclic.log', 'observations.log', 'corrupt-read.log',
                                     'independent-cells.log', 'build.log', 'vendor.vlt')]
    for directory, names in TRIALS.items():
        files += [ROOT/directory/name for name in names]
    files += [ROOT/name for name in SCRATCH]
    # Exact tool versions that produced this evidence.
    files += [ROOT/'tools'/name for name in ('asic-startup-route-closure.tcl', 'close_asic_startup_route.py',
                                             'check_asic_route_closure.py', 'asic_repair_diode.lock.json')]
    entries = []
    for path in files:
        relative = path.relative_to(ROOT)
        compress = path.stat().st_size > LARGE
        target = ARCHIVE/(str(relative) + ('.gz' if compress else ''))
        target.parent.mkdir(parents=True, exist_ok=True)
        if compress:
            with path.open('rb') as source, gzip.GzipFile(target, 'wb', mtime=0) as sink:
                shutil.copyfileobj(source, sink)
            assert gzip.decompress(target.read_bytes()) == path.read_bytes()
        else:
            shutil.copyfile(path, target)
        entries.append({'original_path': str(relative), 'archive_path': str(target.relative_to(ROOT)),
                        'original_sha256': digest(path), 'archive_sha256': digest(target), 'compressed': compress})
    (ARCHIVE/'index.json').write_text(json.dumps(entries, indent=2) + '\n')
    first = json.loads((ROOT/'build/asic-routing-repair/status.json').read_text())
    # Count edits from the netlists; the resizer's summary message undercounts hold buffers.
    top = 'wasmetal_startup_sram'
    before = Counter(c['type'] for c in json.loads((ROOT/'build/asic-routing-extended/routed-functional.json').read_text())['modules'][top]['cells'].values())
    after = Counter(c['type'] for c in json.loads((work/'mapped.json').read_text())['modules'][top]['cells'].values())
    changes = {k: after[k] - before[k] for k in sorted(set(before) | set(after)) if after[k] != before[k]}
    keys = ('detailed_iteration_violations', 'post_route_antenna_rounds', 'diodes_inserted',
            'router_drc_markers', 'setup_slack_ns', 'hold_slack_ns', 'antenna_net_violations', 'antenna_pin_violations',
            'electrical_violators', 'global_electrical_violators_before_repair', 'global_electrical_violators_after_repair',
            'setup_passes_at_trial_corner', 'hold_passes_at_trial_corner', 'antenna_check_passed',
            'electrical_check_passed', 'elapsed_seconds')
    summary = {'status': 'routed-checks-pass-at-trial-corner',
               'scope': 'startup/BIST/SRAM-adapter block; no CPU or SRAM array',
               'baseline': 'asic-route-extraction-summary.json', 'clock_period_ns': 100,
               'library_corner': status['library_corner'], **{k: status[k] for k in keys},
               'baseline_functional_cells': sum(before.values()), 'functional_cells': sum(after.values()),
               'cell_type_changes': changes,
               'status_hold_buffer_field_note': 'route status hold_buffers_inserted sums resizer summary messages and undercounts; cell_type_changes is authoritative',
               'functional': {k: functional[k] for k in ('standard_cells', 'diodes', 'post_route_diodes', 'proofs',
                              'observations', 'negative_controls_rejected',
                              'non_diode_pin_incidence_unchanged_by_detailed_routing')},
               'active_cell_types_checked_upstream': len(cells['mapped_types_checked']),
               'first_repair_trial': {'hold_slack_ns': 0.067417, 'antenna_net_violations': 15,
                                      'antenna_pin_violations': 16, 'electrical_violators': ['_5033_/Y', '_5034_/C'],
                                      'router_drc_markers': first['drc_report_markers'], 'status': first['status']},
               'jumper_trial': 'stopped during detailed routing when the earlier session ended; no result',
               'route_status_sha256': digest(route/'status.json'), 'functional_report_sha256': digest(functional_path),
               'archive': str((ARCHIVE/'index.json').relative_to(ROOT)), 'archived_files': len(entries),
               'physical_timing_accepted': False, 'signoff_drc_lvs_passed': False, 'fabrication_ready': False,
               'physical_hardware_tested': False,
               'limitations': ['Zero OpenROAD router markers is not signoff DRC/LVS; the router reports skipping some LEF58 via-enclosure rules.',
                               'Timing uses one typical 1.8 V, 25 C library corner, the trial 100 ns clock and block-interface constraints.',
                               'The block contains no CPU, SRAM macro, pads, power analysis or manufacturing-test implementation.']}
    SUMMARY.write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({'archived_files': len(entries), 'summary': str(SUMMARY.relative_to(ROOT))}))


if __name__ == '__main__':
    main()
