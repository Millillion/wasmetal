#!/usr/bin/env python3
"""Check startup functionality after placement, clock trees and global routing.

Run check_asic_startup.py first. This does not perform detailed routing or
accept physical timing, DRC, SRAM integration or a complete CPU implementation.
"""
from copy import deepcopy
import json
import os
from pathlib import Path
import re
import shutil
import sys
import time

from asic_cells import audit_circuit, require
from asic_clock_tree import FLIP_FLOPS, canonical_clock_view, fault_controls
from asic_physical_tools import PDK, provision
from check_asic_cell_models import module_bodies
from check_asic_startup import build_model, execute, proofs, rtl, yosys
from check_memory_startup import CONFIGURATIONS, TOP
from prepare_standalone import ROOT, digest


BASE = ROOT / 'build/asic-physical-startup'
SIZE, LATENCY, TIMEOUT = 131072, 3, 11
TAP = 'sky130_fd_sc_hd__tapvpwrvgnd_1'


def normalized_circuit(raw, normalized):
    original, actual = raw['modules'][TOP], normalized['modules'][TOP]
    removed = {name: cell for name, cell in original['cells'].items() if cell['type'] == TAP}
    require(all(not cell['connections'] for cell in removed.values()),
            'cannot discard a connected physical cell')
    expected = {name: cell for name, cell in original['cells'].items() if name not in removed}
    require(set(expected) == set(actual['cells']), 'normalization changed functional-cell inventory')
    fields = ('type', 'parameters', 'connections', 'port_directions')
    require(all(all(cell[field] == actual['cells'][name][field] for field in fields)
                for name, cell in expected.items()), 'normalization changed cell-pin incidence')
    require(original['ports'] == actual['ports'], 'normalization changed top ports')
    return {'physical_taps_removed': len(removed), 'removed_cell_connections_empty': True,
            'functional_cells': len(expected), 'surviving_cell_connections_unchanged': True,
            'top_ports_unchanged': True}


def normalization_faults(raw, normalized):
    controls = []
    tap = next(name for name, cell in raw['modules'][TOP]['cells'].items() if cell['type'] == TAP)
    functional = next(iter(normalized['modules'][TOP]['cells']))
    flop = next(name for name, cell in normalized['modules'][TOP]['cells'].items()
                if cell['type'] in FLIP_FLOPS)
    for label in ('connected-physical-tap', 'deleted-functional-cell', 'rewired-functional-input'):
        before, after = deepcopy(raw), deepcopy(normalized)
        if label == 'connected-physical-tap':
            before['modules'][TOP]['cells'][tap]['connections']['A'] = before['modules'][TOP]['ports']['clk']['bits']
        elif label == 'deleted-functional-cell':
            del after['modules'][TOP]['cells'][functional]
        else:
            after['modules'][TOP]['cells'][flop]['connections']['D'] = after['modules'][TOP]['ports']['reset']['bits']
        try:
            normalized_circuit(before, after)
        except ValueError as error:
            controls.append({'name': label, 'diagnostic': str(error)})
        else:
            raise ValueError('physical normalization accepted fault: ' + label)
    return controls


def comparison_setup(directory, reference):
    data = json.loads((directory / 'reference.json').read_text())['modules'][TOP]
    names = sorted(name for name, cell in data['cells'].items() if cell['type'] in FLIP_FLOPS)
    require(names and all(re.fullmatch(r'_[0-9]+_', name) for name in names),
            'unsupported state-instance naming for this experimental flow')
    selectors = ' '.join(TOP + '/w:' + name + '.Q' for name in names)
    setup = ''
    for label, source in [('gold', reference), ('gate', directory / 'mapped.v')]:
        setup += f'read_verilog {directory}/equivalence-cells.v {source}\n'
        setup += f'prep -top {TOP} -flatten\nopt\nsplitnets\n'
        setup += f'select -assert-count {len(names)} {selectors}\nselect -set state_points {selectors}\n'
        # Preserve every state Q and output port. Hiding other internal wire
        # names avoids thousands of redundant or changed combinational aliases.
        # The corresponding reset proof must establish every comparison point.
        setup += f'rename -hide {TOP}/w:* @state_points %d\nselect *\n'
        setup += f'rename {TOP} {label}\ndesign -stash {label}\n'
    setup += 'design -copy-from gold -as gold gold\ndesign -copy-from gate -as gate gate\n'
    return setup, len(names)


def verify_equivalence(directory, reference):
    setup, count = comparison_setup(directory, reference)
    script = setup + f'equiv_make gold gate equiv\nhierarchy -top equiv\nwrite_rtlil {directory}/equiv.il\n'
    script += 'equiv_induct -undef -seq 1\nequiv_status -assert\n'
    _, induction = yosys(script, directory, 'equivalence')
    require('Equivalence successfully proven!' in induction.read_text(), 'missing physical induction result')
    script = f'read_rtlil {directory}/equiv.il\nequiv_miter -assert -undef reset_points\n'
    script += 'hierarchy -top reset_points\nflatten\nopt_clean\n'
    script += 'sat -seq 12 -set-at 1 reset 1 -set-def-inputs -set-init-undef -enable_undef -prove-skip 1 -prove-asserts -verify\n'
    _, base = yosys(script, directory, 'reset-points')
    require('SAT proof finished - no model found: SUCCESS!' in base.read_text(), 'missing physical reset base')
    # Independently compare current RTL and the physically modified circuit's
    # output pins, without assuming equivalence of any internal state point.
    setup = rtl(SIZE, LATENCY, TIMEOUT) + f'prep -top {TOP} -flatten\nmemory_map\nopt_clean\n'
    setup += f'rename {TOP} gold\ndesign -stash gold\n'
    setup += f'read_verilog {directory}/cells.v {directory}/mapped.v\nprep -top {TOP} -flatten\n'
    setup += f'rename {TOP} gate\ndesign -stash gate\n'
    setup += 'design -copy-from gold -as gold gold\ndesign -copy-from gate -as gate gate\n'
    setup += 'miter -equiv -flatten gold gate reset_pins\nhierarchy -top reset_pins\n'
    setup += 'sat -seq 12 -set-at 1 in_reset 1 -set-def-inputs -set-init-undef -enable_undef -prove-skip 1 -prove trigger 0 -verify\n'
    _, pins = yosys(setup, directory, 'reset-pins')
    require('SAT proof finished - no model found: SUCCESS!' in pins.read_text(), 'missing independent physical pin proof')
    return {'inductive_equivalence': True, 'induction_steps': 1, 'state_points': count,
            'reset_base_cycles': 12, 'induction_log_sha256': digest(induction),
            'reset_point_log_sha256': digest(base), 'reset_pin_log_sha256': digest(pins)}


def main():
    started = time.monotonic()
    BASE.mkdir(parents=True, exist_ok=True)
    output = ROOT / 'reports/asic-physical-startup.json'
    output.unlink(missing_ok=True)
    progress = BASE / 'progress.json'
    progress.write_text(json.dumps({'status': 'incomplete', 'phase': 'verify-inputs'}) + '\n')
    source_report = ROOT / 'reports/asic-startup.json'
    baseline = json.loads(source_report.read_text())
    require(baseline['status'] == 'passed' and baseline['backend'] == 'mapped-sky130hd-functional',
            'complete startup functional campaign required')
    require(len(baseline['checks']) == len(CONFIGURATIONS) and {
        (c['ram_bytes'], c['read_latency'], c['response_timeout']) for c in baseline['checks']} == set(CONFIGURATIONS),
        'complete startup configuration matrix required')
    case = next(c for c in baseline['checks'] if
                (c['ram_bytes'], c['read_latency'], c['response_timeout']) == (SIZE, LATENCY, TIMEOUT))
    original = ROOT / 'build/asic-startup/131072-3-11'
    bound = dict(baseline['inputs'])
    for name, expected in bound.items():
        require(digest(ROOT / name) == expected, 'startup reference input changed: ' + name)
    require(digest(original / 'mapped.json') == case['netlist_sha256'] and
            digest(original / 'cells.v') == case['functional_models_sha256'], 'startup reference circuit changed')
    for label, directory in [('rtl', original / 'native'), ('standard_cells', original)]:
        require(digest(directory / ('obj/V' + TOP)) == case['tests'][label]['binary_sha256'], 'reference binary changed')
        require(digest(original / (label + '-observations.log')) == case['tests'][label]['log_sha256'],
                'reference observations changed')
    expected = case['tests']['rtl']['observations']
    require(expected['status'] == 'passed' and expected == case['tests']['standard_cells']['observations'],
            'reference observations do not match')
    templates = [ROOT / 'tools' / ('asic-startup-' + name + '.tcl')
                 for name in ('floorplan', 'clock-tree', 'global-route')]
    executable, environment, tool_report = provision()
    bound.update(tool_report['inputs'])
    paths = [source_report, original / 'mapped.json', original / 'mapped.v', original / 'cells.v',
             ROOT / 'tools/asic_physical_cell_models.lock.json', *templates]
    paths += [PDK / row['cache_name'] for row in json.loads((ROOT / 'tools/asic_physical.lock.json').read_text())['platform_files']]
    bound.update({str(path.relative_to(ROOT)): digest(path) for path in paths})
    library = ROOT / 'build/asic-startup/library/cells.lib'
    require(digest(library) == baseline['filter']['filtered_sha256'], 'reference mapping library changed')
    shutil.copyfile(library, BASE / 'cells.lib')
    # Re-serialize the hash-bound JSON rather than trusting an unrelated Verilog
    # file to represent the circuit that passed the reference simulation.
    yosys(f'read_json {original}/mapped.json\nwrite_verilog -noattr -noexpr -nodec {BASE}/baseline.v\n', BASE, 'reference-serialize')
    require((BASE / 'baseline.v').read_bytes() == (original / 'mapped.v').read_bytes(),
            'reference JSON and simulated Verilog serialization differ')
    environment.update(WASMETAL_ASIC_TRIAL=str(BASE), WASMETAL_ASIC_PLATFORM=str(PDK))
    for template in templates:
        progress.write_text(json.dumps({'status': 'incomplete', 'phase': template.stem, 'inputs': bound}, indent=2) + '\n')
        execute([str(executable), '-no_init', '-no_settings', '-exit', '-threads', '2', str(template)],
                BASE / (template.stem + '.log'), env=environment)
    directory = BASE / 'functional'
    directory.mkdir(exist_ok=True)
    script = f'read_liberty -lib -ignore_miss_func {BASE}/cells.lib\nread_verilog {BASE}/global-routed.v\n'
    script += f'write_json {directory}/raw.json\ndelete t:{TAP}\nhierarchy -check -top {TOP}\ncheck -assert\n'
    script += f'write_json {directory}/mapped.json\nwrite_verilog -noattr -noexpr -nodec {directory}/mapped.v\n'
    yosys(script, directory, 'normalize')
    raw = json.loads((directory / 'raw.json').read_text())
    mapped = json.loads((directory / 'mapped.json').read_text())
    normalization = normalized_circuit(raw, mapped)
    controls = normalization_faults(raw, mapped)
    script = f'read_liberty -lib -ignore_miss_func {BASE}/cells.lib\nread_verilog {BASE}/baseline.v\n'
    script += f'hierarchy -check -top {TOP}\nwrite_json {directory}/reference.json\n'
    yosys(script, directory, 'reference-import')
    reference = json.loads((directory / 'reference.json').read_text())['modules'][TOP]
    module = mapped['modules'][TOP]
    canonical, clock = canonical_clock_view(module, reference)
    controls += fault_controls(module, reference)
    counts = audit_circuit(canonical, {n: m for n, m in mapped['modules'].items() if n != TOP},
                           set(baseline['filter']['excluded_cells']))
    (directory / 'clock-audit.json').write_text(json.dumps(clock, indent=2) + '\n')
    union = sorted(set(counts) | {cell['type'] for cell in reference['cells'].values()})
    for label, types in [('cells', sorted(counts)), ('equivalence-cells', union)]:
        script = f'read_liberty -ignore_miss_func -ignore_miss_dir -ignore_miss_data_latch {BASE}/cells.lib\n'
        script += 'select -clear\nselect ' + ' '.join(types) + f'\nwrite_verilog -selected -noattr {directory}/{label}.v\n'
        yosys(script, directory, label)
    union_bodies = module_bodies((directory / 'equivalence-cells.v').read_text())
    for source in (directory / 'cells.v', original / 'cells.v'):
        require(all(union_bodies[name] == body for name, body in module_bodies(source.read_text()).items()),
                'proof and simulation cell definitions differ')
    execute([sys.executable, 'tools/check_asic_cell_models.py', '--cell-lock',
             'tools/asic_physical_cell_models.lock.json', '--netlist', str(directory / 'mapped.json'),
             '--cell-models', str(directory / 'cells.v'), '--label', 'asic-physical-startup-cells'],
            BASE / 'independent-cells.log')
    cells_report_path = ROOT / 'reports/asic-physical-startup-cells.json'
    cells_report = json.loads(cells_report_path.read_text())
    require(cells_report['status'] == 'passed' and cells_report['model_source_mode'] == 'single-netlist' and
            set(cells_report['mapped_types_checked']) == set(counts), 'incomplete physical cell-model check')
    script = f'read_verilog {directory}/cells.v {directory}/mapped.v\nhierarchy -check -top {TOP}\n'
    script += 'proc\nflatten\nopt\nscc -expect 0\ncheck -assert\n'
    _, acyclic = yosys(script, directory, 'acyclic')
    require('Found 0 SCCs' in acyclic.read_text(), 'physical circuit has a combinational cycle')
    progress.write_text(json.dumps({'status': 'incomplete', 'phase': 'proof-and-simulation', 'inputs': bound}, indent=2) + '\n')
    proof = verify_equivalence(directory, BASE / 'baseline.v')
    config = (original / 'vendor.vlt').read_text().replace(str(original), str(directory))
    (directory / 'vendor.vlt').write_text(config)
    binary = build_model(directory, SIZE, LATENCY, TIMEOUT)
    observations = directory / 'observations.log'
    execute([str(binary)], observations, timeout=900)
    actual = json.loads(observations.read_text())
    require(actual == expected, 'post-physical and RTL observations differ')
    corrupt = directory / 'corrupt-read.log'
    result = execute([str(binary), '--corrupt-read'], corrupt, accepted_failure=True)
    require(result != 0 and 'startup' in corrupt.read_text(), 'post-physical model accepted a corrupt SRAM read')
    controls.append({'name': 'corrupt-sram-read', 'log_sha256': digest(corrupt)})
    fault = directory / 'wrong-constant'
    fault.mkdir(exist_ok=True)
    target = module['ports']['completed_operations']['bits'][-1]
    ties = [name for name, cell in module['cells'].items() if cell['type'] == 'sky130_fd_sc_hd__conb_1'
            and cell['connections'].get('LO') == [target] and 'HI' not in cell['connections']]
    require(len(ties) == 1, 'ambiguous observable physical tie-cell fault target')
    mutant = deepcopy(mapped)
    cell = mutant['modules'][TOP]['cells'][ties[0]]
    cell['connections']['HI'] = cell['connections'].pop('LO')
    cell['port_directions']['HI'] = cell['port_directions'].pop('LO')
    canonical, _ = canonical_clock_view(mutant['modules'][TOP], reference)
    audit_circuit(canonical, {n: m for n, m in mapped['modules'].items() if n != TOP},
                  set(baseline['filter']['excluded_cells']))
    (fault / 'mapped.json').write_text(json.dumps(mutant) + '\n')
    yosys(f'read_json {fault}/mapped.json\nwrite_verilog -noattr -noexpr -nodec {fault}/proof-circuit.v\n', fault, 'emit')
    shutil.copyfile(directory / 'cells.v', fault / 'cells.v')
    controls.append({'name': 'wrong-physical-tie-formal', **proofs(fault, SIZE, LATENCY, TIMEOUT, accepted_failure=True)})
    for name, expected_hash in {**bound, **cells_report['inputs']}.items():
        require(digest(ROOT / name) == expected_hash, 'physical verification input changed: ' + name)
    _, _, after = provision()
    require(all(tool_report[key] == after[key] for key in ('inputs', 'lock_sha256', 'executable_sha256',
                'package_trees', 'loaded_libraries')), 'physical tool or runtime changed during verification')
    report = {'status': 'passed', 'scope': 'startup controller, test master and SRAM adapter after physical optimization; no CPU or SRAM array',
              'backend': 'sky130hd-post-physical-functional', 'inputs': bound, 'tools': tool_report,
              'ram_bytes': SIZE, 'read_latency': LATENCY, 'response_timeout': TIMEOUT,
              'clock_period_ns': 100, 'clock_period_is_experimental_constraint': True,
              'normalization': normalization, 'clock_tree': clock, 'standard_cells': counts, 'proofs': proof,
              'reference_report_sha256': digest(source_report), 'cell_report_sha256': digest(cells_report_path),
              'netlist_sha256': digest(directory / 'mapped.json'), 'functional_models_sha256': digest(directory / 'cells.v'),
              'binary_sha256': digest(binary), 'observations': actual, 'observations_log_sha256': digest(observations),
              'negative_controls': controls, 'negative_controls_rejected': len(controls),
              'elapsed_seconds': time.monotonic() - started, 'physical_hardware_tested': False,
              'detailed_routing_included': False, 'physical_timing_accepted': False,
              'limitations': ['Binary functionality with zero cell delays; no SDF, analog or power-pin simulation.',
                  'Global routing supplies coarse paths and estimated parasitics; no completed detailed route, extracted timing or DRC/LVS signoff.',
                  'Only the typical 1.8 V, 25 C library is used; no process-corner closure, SRAM macro, pads or manufacturing-test implementation.']}
    output.write_text(json.dumps(report, indent=2) + '\n')
    print('PASS post-physical startup functionality', actual['cycles'], 'clocks;', sum(counts.values()),
          'cells;', len(controls), 'circuit fault controls; detailed routing and timing remain unaccepted')


if __name__ == '__main__':
    main()
