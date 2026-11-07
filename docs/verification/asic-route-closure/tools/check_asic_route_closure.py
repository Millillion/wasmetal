#!/usr/bin/env python3
"""Check functionality of the detailed-routed, repaired startup block.

Run close_asic_startup_route.py first. This verifies the routed netlist against
the startup RTL; it does not accept physical timing, DRC/LVS or a complete CPU.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import re
import shutil
import sys
import time

from asic_cells import audit_circuit, connectivity, require, verify_bytes
from asic_clock_tree import canonical_clock_view, fault_controls
from asic_physical_tools import provision
from check_asic_cell_models import module_bodies
from check_asic_physical_startup import (LATENCY, SIZE, TAP, TIMEOUT, normalization_faults,
                                         normalized_circuit, verify_equivalence)
from check_asic_startup import build_model, execute, proofs, yosys
from check_memory_startup import TOP
from prepare_standalone import ROOT, digest

DIODE = 'sky130_fd_sc_hd__diode_2'
DIODE_LOCK = ROOT/'tools/asic_repair_diode.lock.json'
PRIOR = ROOT/'build/asic-physical-startup'
ORIGINAL = ROOT/'build/asic-startup/131072-3-11'


def without_diodes(module):
    module = deepcopy(module)
    module['cells'] = {n: c for n, c in module['cells'].items() if c['type'] != DIODE}
    return module


def diodes(module):
    return {n for n, c in module['cells'].items() if c['type'] == DIODE}


def passive(module):
    require(set(module['ports']) == {'DIODE'} and module['ports']['DIODE']['direction'] == 'input' and
            len(module['ports']['DIODE']['bits']) == 1 and not module.get('cells') and
            not module.get('memories') and not module.get('processes'), 'diode is not a purely passive digital input')


def diode_controls(derived):
    controls = []
    for fault in ('driven-output', 'internal-logic', 'extra-port'):
        module = deepcopy(derived)
        if fault == 'driven-output':
            module['ports']['DIODE']['direction'] = 'output'
        elif fault == 'internal-logic':
            module['cells']['bad'] = {'type': '$_NOT_'}
        else:
            module['ports']['bad'] = {'direction': 'output', 'bits': [99]}
        try:
            passive(module)
        except ValueError as error:
            controls.append({'name': 'diode-' + fault, 'diagnostic': str(error)})
        else:
            raise ValueError('passive diode check accepted ' + fault)
    return controls


def attachment_controls(routed, global_module):
    """Diode-only edits must leave the remaining pin incidence unchanged."""
    controls = []
    flop = next(n for n, c in routed['cells'].items() if c['type'].startswith('sky130_fd_sc_hd__dfxtp_'))
    logic = next(n for n, c in routed['cells'].items() if c['type'] not in (DIODE, TAP) and n != flop)
    for label in ('rewired-flip-flop', 'deleted-logic-cell', 'diode-as-driver'):
        mutant = deepcopy(routed)
        if label == 'rewired-flip-flop':
            mutant['cells'][flop]['connections']['D'] = list(mutant['ports']['reset']['bits'])
        elif label == 'deleted-logic-cell':
            del mutant['cells'][logic]
        else:
            name = next(iter(diodes(mutant)))
            mutant['cells'][name]['port_directions']['DIODE'] = 'output'
        try:
            require(all(c['port_directions'] == {'DIODE': 'input'} for c in mutant['cells'].values() if c['type'] == DIODE),
                    'diode drives a net')
            require(connectivity(without_diodes(mutant)) == connectivity(without_diodes(global_module)),
                    'detailed routing changed non-diode pin incidence')
        except ValueError as error:
            controls.append({'name': label, 'diagnostic': str(error)})
        else:
            raise ValueError('diode attachment check accepted ' + label)
    return controls


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--route', type=Path, default=ROOT/'build/asic-route-closure')
    parser.add_argument('--cell-lock', type=Path, default=ROOT/'tools/asic_physical_cell_models.lock.json')
    parser.add_argument('--label', default='asic-route-closure-functional')
    args = parser.parse_args()
    started = time.monotonic()
    route = args.route.resolve()
    base = ROOT/'build'/args.label
    output = ROOT/'reports'/(args.label + '.json')
    output.unlink(missing_ok=True)
    base.mkdir(parents=True, exist_ok=False)
    status = json.loads((route/'status.json').read_text())
    require(status['status'] == 'diagnostic-completed' and status['inputs_unchanged'], 'incomplete route closure')
    for name, value in status['artifacts'].items():
        require(digest(route/name) == value, 'route closure artifact changed: ' + name)
    bound = {str((route/n).relative_to(ROOT)): h for n, h in status['artifacts'].items()}
    bound[str((route/'status.json').relative_to(ROOT))] = digest(route/'status.json')
    bound.update({n: h for n, h in status['inputs'].items() if not n.endswith('.py') or n.startswith('tools/close')})
    source_report = ROOT/'reports/asic-startup.json'
    baseline = json.loads(source_report.read_text())
    require(baseline['status'] == 'passed' and baseline['backend'] == 'mapped-sky130hd-functional',
            'complete startup functional campaign required')
    case = next(c for c in baseline['checks'] if (c['ram_bytes'], c['read_latency'], c['response_timeout']) == (SIZE, LATENCY, TIMEOUT))
    expected = case['tests']['rtl']['observations']
    require(expected['status'] == 'passed' and expected == case['tests']['standard_cells']['observations'],
            'reference observations differ')
    bound.update(baseline['inputs'])
    library = PRIOR/'cells.lib'
    bound.update({str(p.relative_to(ROOT)): digest(p) for p in (
        source_report, library, PRIOR/'baseline.v', ORIGINAL/'mapped.json', DIODE_LOCK, args.cell_lock.resolve(),
        Path(__file__).resolve(), ROOT/'tools/check_asic_physical_startup.py', ROOT/'tools/check_asic_startup.py',
        ROOT/'tools/asic_clock_tree.py', ROOT/'tools/asic_cells.py', ROOT/'tools/check_asic_cell_models.py')})
    require(digest(ORIGINAL/'mapped.json') == case['netlist_sha256'], 'startup reference circuit changed')
    for name, value in bound.items():
        require(digest(ROOT/name) == value, 'route closure input changed: ' + name)

    imported = {}
    for label, netlist in (('routed', route/'routed.v'), ('global', route/'repaired-global.v')):
        script = f'read_liberty -lib -ignore_miss_func {library}\nread_verilog {netlist}\nwrite_json {base}/{label}-raw.json\n'
        script += f'delete t:{TAP}\nhierarchy -check -top {TOP}\ncheck -assert\nwrite_json {base}/{label}.json\n'
        if label == 'routed':
            script += f'write_verilog -noattr -noexpr -nodec {base}/mapped.v\n'
        yosys(script, base, label + '-import')
        imported[label] = (json.loads((base/f'{label}-raw.json').read_text()), json.loads((base/f'{label}.json').read_text()))
    raw, mapped = imported['routed']
    global_raw, global_mapped = imported['global']
    shutil.copyfile(base/'routed.json', base/'mapped.json')
    normalization = normalized_circuit(raw, mapped)
    normalized_circuit(global_raw, global_mapped)
    controls = normalization_faults(raw, mapped)
    taps = lambda data: {n for n, c in data['modules'][TOP]['cells'].items() if c['type'] == TAP}
    require(taps(raw) == taps(global_raw), 'physical tap inventory changed during detailed routing')
    module, global_module = mapped['modules'][TOP], global_mapped['modules'][TOP]
    require(diodes(global_module) <= diodes(module), 'detailed routing removed a global-route diode')
    require(all(c['port_directions'] == {'DIODE': 'input'} for c in module['cells'].values() if c['type'] == DIODE),
            'diode drives a net')
    require(connectivity(without_diodes(module)) == connectivity(without_diodes(global_module)),
            'detailed routing changed non-diode pin incidence')
    controls += attachment_controls(module, global_module)

    shutil.copyfile(PRIOR/'baseline.v', base/'baseline.v')
    yosys(f'read_liberty -lib -ignore_miss_func {library}\nread_verilog {base}/baseline.v\nhierarchy -check -top {TOP}\n'
          f'write_json {base}/reference.json\n', base, 'reference')
    reference = json.loads((base/'reference.json').read_text())['modules'][TOP]
    canonical, clock = canonical_clock_view(module, reference)
    counts = audit_circuit(canonical, {n: m for n, m in mapped['modules'].items() if n != TOP},
                           set(baseline['filter']['excluded_cells']))
    controls += fault_controls(module, reference)
    union = sorted(set(counts) | {c['type'] for c in reference['cells'].values()})
    for label, types in (('cells', sorted(counts)), ('equivalence-cells', union)):
        script = f'read_liberty -ignore_miss_func -ignore_miss_dir -ignore_miss_data_latch {library}\nwrite_json {base}/library.json\n'
        script += 'select -clear\nselect ' + ' '.join(types) + f'\nwrite_verilog -selected -noattr {base}/{label}.v\n'
        yosys(script, base, label)

    # The diode is a passive pin in both the pinned upstream and Liberty-derived
    # models. Remove only diodes before the independent active-cell comparison.
    record = json.loads(DIODE_LOCK.read_text())['files'][0]
    vendor = ROOT/'.cache/sky130hd-vendor'/record['path']
    verify_bytes(vendor.read_bytes(), record)
    yosys(f'read_verilog {vendor}\nhierarchy -check -top {DIODE}\nproc\nwrite_json {base}/vendor-diode.json\n', base, 'vendor-diode')
    derived = json.loads((base/'library.json').read_text())['modules'][DIODE]
    passive(json.loads((base/'vendor-diode.json').read_text())['modules'][DIODE])
    passive(derived)
    controls += diode_controls(derived)
    logic = deepcopy(mapped)
    logic['modules'][TOP] = without_diodes(module)
    (base/'logic-inventory.json').write_text(json.dumps(logic) + '\n')
    bodies = module_bodies((base/'cells.v').read_text())
    (base/'logic-models.v').write_text('\n\n'.join(b for n, b in bodies.items() if n != DIODE) + '\n')
    locked = set(json.loads(args.cell_lock.read_text())['cell_types'])
    active = set(bodies) - {DIODE}
    require(active == locked, 'active cell types differ from the cell-model lock: added '
            f'{sorted(active - locked)}, removed {sorted(locked - active)}')
    cells_label = args.label + '-cells'
    execute([sys.executable, 'tools/check_asic_cell_models.py', '--cell-lock', str(args.cell_lock.resolve()),
             '--netlist', str(base/'logic-inventory.json'), '--cell-models', str(base/'logic-models.v'),
             '--label', cells_label], base/'independent-cells.log')
    cells_path = ROOT/'reports'/(cells_label + '.json')
    cells_report = json.loads(cells_path.read_text())
    require(cells_report['status'] == 'passed' and cells_report['model_source_mode'] == 'single-netlist' and
            set(cells_report['mapped_types_checked']) == active, 'incomplete routed cell-model check')

    _, acyclic = yosys(f'read_verilog {base}/cells.v {base}/mapped.v\nhierarchy -check -top {TOP}\nproc\nflatten\nopt\n'
                       'scc -expect 0\ncheck -assert\n', base, 'acyclic')
    require('Found 0 SCCs' in acyclic.read_text(), 'routed circuit has a combinational cycle')
    proof = verify_equivalence(base, base/'baseline.v')
    print('PASS routed state/output equivalence and reset proofs', flush=True)
    config = re.sub(r'"[^"]*/build/asic-startup/131072-3-11/', f'"{base}/', (ORIGINAL/'vendor.vlt').read_text())
    require(config.count(str(base)) == 4, 'unexpected simulator lint configuration')
    (base/'vendor.vlt').write_text(config)
    binary = build_model(base, SIZE, LATENCY, TIMEOUT)
    observations = base/'observations.log'
    execute([str(binary)], observations, timeout=900)
    actual = json.loads(observations.read_text())
    require(actual == expected, 'routed and RTL observations differ')
    corrupt = base/'corrupt-read.log'
    require(execute([str(binary), '--corrupt-read'], corrupt, accepted_failure=True) != 0 and 'startup' in corrupt.read_text(),
            'routed model accepted a corrupt SRAM read')
    controls.append({'name': 'corrupt-sram-read', 'log_sha256': digest(corrupt)})
    fault = base/'wrong-constant'
    fault.mkdir()
    target = module['ports']['completed_operations']['bits'][-1]
    ties = [n for n, c in module['cells'].items() if c['type'] == 'sky130_fd_sc_hd__conb_1'
            and c['connections'].get('LO') == [target] and 'HI' not in c['connections']]
    require(len(ties) == 1, 'ambiguous observable tie-cell fault target')
    mutant = deepcopy(mapped)
    cell = mutant['modules'][TOP]['cells'][ties[0]]
    cell['connections']['HI'] = cell['connections'].pop('LO')
    cell['port_directions']['HI'] = cell['port_directions'].pop('LO')
    (fault/'mapped.json').write_text(json.dumps(mutant) + '\n')
    yosys(f'read_json {fault}/mapped.json\nwrite_verilog -noattr -noexpr -nodec {fault}/proof-circuit.v\n', fault, 'emit')
    shutil.copyfile(base/'cells.v', fault/'cells.v')
    controls.append({'name': 'wrong-routed-tie-formal', **proofs(fault, SIZE, LATENCY, TIMEOUT, accepted_failure=True)})
    for name, value in {**bound, **cells_report['inputs']}.items():
        require(digest(ROOT/name) == value, 'routed verification input changed: ' + name)
    _, _, tools = provision()
    report = {'status': 'passed', 'scope': 'startup controller, test master and SRAM adapter after detailed routing and repair; no CPU or SRAM array',
              'backend': 'sky130hd-routed-functional', 'inputs': bound, 'route_status_sha256': digest(route/'status.json'),
              'ram_bytes': SIZE, 'read_latency': LATENCY, 'response_timeout': TIMEOUT, 'clock_period_ns': 100,
              'normalization': normalization, 'clock_tree': clock, 'standard_cells': counts,
              'diodes': len(diodes(module)), 'post_route_diodes': len(diodes(module) - diodes(global_module)),
              'non_diode_pin_incidence_unchanged_by_detailed_routing': True, 'proofs': proof,
              'cell_report_sha256': digest(cells_path), 'netlist_sha256': digest(base/'mapped.json'),
              'functional_models_sha256': digest(base/'cells.v'), 'binary_sha256': digest(binary),
              'observations': actual, 'observations_log_sha256': digest(observations),
              'negative_controls': controls, 'negative_controls_rejected': len(controls),
              'tool_lock_sha256': tools['lock_sha256'], 'elapsed_seconds': time.monotonic() - started,
              'physical_hardware_tested': False, 'physical_timing_accepted': False,
              'limitations': ['Binary functionality with zero cell delays; no SDF, analog or power-pin simulation.',
                              'One typical 1.8 V, 25 C library; no multi-corner timing, DRC/LVS signoff, SRAM macro, pads or test logic.']}
    output.write_text(json.dumps(report, indent=2) + '\n')
    print('PASS routed startup functionality', actual['cycles'], 'clocks;', sum(counts.values()), 'cells;',
          len(controls), 'fault controls; physical signoff remains open', flush=True)


if __name__ == '__main__':
    main()
