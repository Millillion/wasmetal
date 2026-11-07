#!/usr/bin/env python3
"""Repair hold, electrical and antenna checks on the routed startup block.

Starts from the extracted detailed route of the SKY130HD startup trial, repairs
hold timing and wire-load limits, re-routes, then repeats antenna repair against
the detailed wires. Results are unsigned-off diagnostics at one library corner.
"""
import argparse
import json
from pathlib import Path
import re
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from asic_physical_tools import PDK, provision
from check_asic_startup import execute
from prepare_standalone import ROOT, digest

DIODE = 'sky130_fd_sc_hd__diode_2'
TEMPLATE = ROOT/'tools/asic-startup-route-closure.tcl'
RULES = ROOT/'.cache/sky130hd-extraction/rcx_patterns.rules'


def slack(log, label):
    match = re.search(rf'WASMETAL extracted {label} slack\s+worst slack (?:max|min) (-?[0-9.]+)', log)
    return float(match.group(1)) if match else None


def violators(report):
    return sorted(set(re.findall(r'^(\S+)\s+\S+\s+\S+\s+-\S+ \(VIOLATED\)', report, re.M)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT/'build/asic-routing-extraction')
    parser.add_argument('--sdc', type=Path, default=ROOT/'build/asic-routing-extended/routed.sdc')
    parser.add_argument('--liberty', type=Path, default=ROOT/'build/asic-physical-startup/cells.lib')
    parser.add_argument('--output', type=Path, default=ROOT/'build/asic-route-closure')
    parser.add_argument('--threads', type=int, default=4)
    parser.add_argument('--timeout', type=int, default=4*3600)
    args = parser.parse_args()
    source, output = args.source.resolve(), args.output.resolve()
    record = json.loads((source/'status.json').read_text())
    if record['status'] != 'diagnostic-completed' or not record['inputs_unchanged']:
        raise SystemExit('the extracted baseline route is incomplete')
    for name, value in record['artifacts'].items():
        if digest(source/name) != value:
            raise SystemExit(f'extracted baseline artifact changed: {name}')
    output.mkdir(parents=True, exist_ok=False)
    exe, env, tools = provision()
    paths = [source/'extracted.odb', source/'routed.spef', source/'status.json', args.sdc.resolve(),
             args.liberty.resolve(), PDK/'setRC.tcl', PDK/'fastroute.tcl', RULES, TEMPLATE, Path(__file__).resolve()]
    bound = {str(p.relative_to(ROOT)): digest(p) for p in paths}
    bound.update(tools['inputs'])
    env = dict(env, WASMETAL_ASIC_SOURCE=str(source), WASMETAL_ASIC_OUTPUT=str(output),
               WASMETAL_ASIC_PLATFORM=str(PDK), WASMETAL_ASIC_DIODE=DIODE, WASMETAL_ASIC_SDC=str(args.sdc.resolve()),
               WASMETAL_ASIC_LIBERTY=str(args.liberty.resolve()), WASMETAL_ASIC_RULES=str(RULES))
    status = output/'status.json'
    report = {'status': 'running', 'scope': 'startup/BIST/SRAM-adapter block; no CPU or SRAM array',
              'baseline': str(source.relative_to(ROOT)), 'inputs': bound, 'tools': tools,
              'hold_margin_ns': 0.1, 'electrical_margin_percent': 20, 'global_antenna_margin_percent': 10,
              'post_route_antenna_rounds_limit': 5, 'diode_cell': DIODE, 'library_corner': 'SKY130HD TT 1.8V 25C',
              'physical_timing_accepted': False, 'signoff_drc_lvs_passed': False, 'fabrication_ready': False,
              'physical_hardware_tested': False}
    status.write_text(json.dumps(report, indent=2)+'\n')
    started = time.monotonic()
    try:
        code = execute([str(exe), '-no_init', '-no_settings', '-exit', '-threads', str(args.threads), str(TEMPLATE)],
                       output/'closure.log', timeout=args.timeout, env=env, accepted_failure=True)
        log = (output/'closure.log').read_text()
        complete = code == 0 and 'FINISHED startup route closure diagnostic' in log
        report.update(exit_code=code, status='diagnostic-completed' if complete else 'incomplete',
                      detailed_iteration_violations=[int(x) for x in re.findall(r'Number of violations = (\d+)', log)])
        if complete:
            rounds = re.search(r'WASMETAL post-route antenna rounds (\d+)', log)
            antenna = (output/'antennas.rpt').read_text()
            electrical = (output/'electrical.rpt').read_text()
            nets = re.findall(r'\[INFO ANT-0002\] Found (\d+) net violations', log)
            pins = re.findall(r'\[INFO ANT-0001\] Found (\d+) pin violations', log)
            report.update(
                post_route_antenna_rounds=int(rounds.group(1)),
                # The resizer's "Inserted N hold buffers" summary undercounts;
                # compare netlists for the actual cell edits.
                resizer_hold_buffer_messages=sum(map(int, re.findall(r'Inserted (\d+) hold buffers', log))),
                diodes_inserted=sum(map(int, re.findall(r'Inserted (\d+) diodes', log))),
                router_drc_markers=len(re.findall(r'^violation type:', (output/'drc.rpt').read_text(), re.M)),
                setup_slack_ns=slack(log, 'setup'), hold_slack_ns=slack(log, 'hold'),
                antenna_net_violations=int(nets[-1]), antenna_pin_violations=int(pins[-1]),
                antenna_report_violations=antenna.count('(VIOLATED)'),
                electrical_violators=violators(electrical),
                baseline_electrical_violators=violators((output/'baseline-electrical.rpt').read_text()),
                global_electrical_violators_before_repair=violators((output/'global-electrical-before.rpt').read_text()),
                global_electrical_violators_after_repair=violators((output/'global-electrical-after.rpt').read_text()))
            report['setup_passes_at_trial_corner'] = report['setup_slack_ns'] is not None and report['setup_slack_ns'] >= 0
            report['hold_passes_at_trial_corner'] = report['hold_slack_ns'] is not None and report['hold_slack_ns'] >= 0
            report['antenna_check_passed'] = report['antenna_net_violations'] == report['antenna_pin_violations'] == 0
            report['electrical_check_passed'] = not report['electrical_violators']
    except Exception as error:
        report.update(status='incomplete', error=str(error))
    finally:
        report['elapsed_seconds'] = time.monotonic()-started
        report['inputs_unchanged'] = all(digest(ROOT/name) == value for name, value in bound.items())
        if not report['inputs_unchanged']:
            report['status'] = 'changed-inputs'
        report['artifacts'] = {p.name: digest(p) for p in sorted(output.iterdir()) if p.is_file() and p != status}
        status.write_text(json.dumps(report, indent=2)+'\n')
        print(report['status'], flush=True)


if __name__ == '__main__':
    main()
