#!/usr/bin/env python3
"""Prepare and check the Vivado build of the programmable system for Genesys 2.

`prepare` pins the exact sources, profile and constraints. Run Vivado, then
`check` accepts the build only if every timing, DRC and bitstream check passes.
"""
import argparse
import json
from pathlib import Path
import re

from prepare_standalone import ROOT, digest, load_profile
from program_upload import profile_tag
from standalone_support import generate_parameters

PART = 'xc7k325tffg900-2'
OUTPUT = ROOT/'build/genesys2'
CONSTRAINTS = ROOT/'soc/loader/genesys2.xdc'
SCRIPT = ROOT/'tools/vivado/genesys2.tcl'


def sources():
    vendor = ROOT/'third_party/hardfloat/source'
    return [*sorted((ROOT/'rtl').glob('*.sv')), *sorted(vendor.glob('*.v')), vendor/'RISCV/HardFloat_specialize.v',
            ROOT/'fpga/wasmetal_uart.sv', ROOT/'soc/wasmetal_standalone.sv', ROOT/'soc/wasmetal_local_memory.sv',
            *sorted((ROOT/'soc/memory').glob('*.sv')), ROOT/'soc/loader/wasmetal_image_loader.sv',
            ROOT/'soc/loader/wasmetal_loadable.sv', ROOT/'soc/loader/wasmetal_loadable_genesys2.sv']


def tcl_list(paths):
    return '[list ' + ' '.join('{' + str(p) + '}' for p in paths) + ']'


def prepare(output):
    output.mkdir(parents=True, exist_ok=True)
    profile = load_profile()
    tag = f"128'h{int.from_bytes(profile_tag(profile), 'little'):032x}"
    vendor = ROOT/'third_party/hardfloat/source'
    parameters = generate_parameters()
    files = [*sources(), *sorted(vendor.rglob('*.vi')), parameters, CONSTRAINTS, SCRIPT, Path(__file__).resolve(),
             ROOT/'soc/profile.json']
    manifest = {'part': PART, 'top': 'wasmetal_loadable_genesys2', 'profile_tag': tag,
                'inputs': {str(p.relative_to(ROOT)): digest(p) for p in files},
                'command': f'vivado -mode batch -log {(output/"vivado.log").relative_to(ROOT)} -journal '
                f'{(output/"vivado.jou").relative_to(ROOT)} -source {SCRIPT.relative_to(ROOT)} -tclargs {output.relative_to(ROOT)}'}
    (output/'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (output/'manifest.tcl').write_text(
        f'set wasmetal_part {PART}\nset wasmetal_profile_tag {{{tag}}}\n'
        f'set wasmetal_sources {tcl_list(sources())}\nset wasmetal_constraints {{{CONSTRAINTS}}}\n'
        f'set wasmetal_include_dirs {tcl_list([vendor, vendor/"RISCV", parameters.parent])}\n')
    print('Run from the repository root:', manifest['command'])


def worst(report):
    match = re.search(r'WNS\(ns\)\s+TNS\(ns\).*?\n\s*-+.*?\n\s*(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)',
                      report, re.S)
    if not match:
        raise SystemExit('timing summary table missing')
    values = [float(v) if re.fullmatch(r'-?[0-9.]+', v) else v for v in match.groups()]
    return dict(zip(('wns', 'tns', 'tns_failing', 'tns_total', 'whs', 'ths', 'ths_failing', 'ths_total'), values))


def check(output):
    manifest = json.loads((output/'manifest.json').read_text())
    changed = [n for n, h in manifest['inputs'].items() if digest(ROOT/n) != h]
    failures = [f'input changed after prepare: {n}' for n in changed]
    log = (output/'vivado.log').read_text() if (output/'vivado.log').exists() else ''
    if 'WASMETAL Vivado build finished' not in log:
        failures.append('Vivado did not finish; run the command printed by prepare')
    summary = (output/'timing-summary.rpt').read_text()
    timing = worst(summary)
    if 'All user specified timing constraints are met.' not in summary:
        failures.append('timing constraints are not met')
    if not (isinstance(timing['wns'], float) and timing['wns'] >= 0 and timing['whs'] >= 0):
        failures.append(f'negative setup or hold slack: {timing}')
    clocks = (output/'clocks.rpt').read_text()
    for clock in ('sysclk', 'core_clock'):
        if not re.search(rf'^{clock}\s', clocks, re.M):
            failures.append('missing clock ' + clock)
    unconstrained = (output/'check-timing.rpt').read_text()
    for section in ('no_clock', 'unconstrained_internal_endpoints', 'generated_clocks', 'loops'):
        count = re.search(rf'checking {section}.*?There (?:is|are) (\d+)', unconstrained, re.S)
        if count and int(count.group(1)):
            failures.append(f'check_timing {section}: {count.group(1)}')
    drc = (output/'drc.rpt').read_text()
    errors = re.search(r'Errors\s*:\s*(\d+)', drc)
    if not errors or int(errors.group(1)):
        failures.append('DRC errors present')
    bitstream = output/'wasmetal.bit'
    if not bitstream.exists():
        failures.append('bitstream missing')
    report = {'status': 'failed' if failures else 'passed', 'part': PART, 'timing': timing, 'failures': failures,
              'manifest_sha256': digest(output/'manifest.json'),
              'bitstream_sha256': digest(bitstream) if bitstream.exists() else None,
              'utilization': (output/'utilization.rpt').read_text()[:20000],
              'physical_hardware_tested': False}
    path = ROOT/'reports/genesys2-vivado.json'
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(report['status'], *failures, sep='\n')
    raise SystemExit(1 if failures else 0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('prepare', 'check'))
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    (prepare if args.command == 'prepare' else check)(args.output.resolve())


if __name__ == '__main__':
    main()
