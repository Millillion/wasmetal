#!/usr/bin/env python3
"""Route a verified reset-replication placement without rebuilding its inputs.

The experiment remains separate from the default board build. A successful
receipt requires structural rechecking, unchanged clocks, routed timing and a
bitstream unpack/repack check. It does not claim physical hardware testing.
"""
import argparse
import gc
import json
from pathlib import Path
import signal
import subprocess

import cad
from build_standalone_board import audit
from prepare_standalone import ROOT, digest
from replicate_reset import verify


def check_inputs(inputs):
    for name, expected in inputs.items():
        if digest(ROOT/name) != expected:
            raise ValueError('routing input changed: '+name)


def prepare(experiment_path, baseline):
    experiment = json.loads(experiment_path.read_text())
    if (experiment['status'] != 'structurally_verified' or
            not experiment.get('placement_completed') or
            not experiment.get('final_input_checks_passed')):
        raise ValueError('experiment lacks a verified completed placement')
    candidate_path = experiment_path.parent/'design.json'
    placement = experiment_path.parent/'placed.json'
    if digest(candidate_path) != experiment['candidate_sha256']:
        raise ValueError('experiment candidate changed')
    if digest(placement) != experiment['artifacts']['placement']:
        raise ValueError('experiment placement changed')
    check_inputs(experiment['inputs'])
    reference_path = baseline/'design.json'
    if digest(reference_path) != experiment['inputs'][str(reference_path.relative_to(ROOT))]:
        raise ValueError('wrong experiment baseline')
    reference = json.loads(reference_path.read_text())
    candidate = json.loads(candidate_path.read_text())
    top = 'wasmetal_loadable_ulx3s'
    proof = verify(reference, candidate, top, experiment['groups'][0]['driver'])
    if proof != experiment['proof']:
        raise ValueError('structural recheck differs from experiment receipt')
    clock_ports = {'CLK', 'CLKA', 'CLKB', 'CLKI', 'WCK', 'CLK0', 'CLK1', 'CLK2', 'CLK3'}
    for name, cell in reference['modules'][top]['cells'].items():
        for port, bits in cell['connections'].items():
            if port in clock_ports and cell['port_directions'][port] == 'input':
                if candidate['modules'][top]['cells'][name]['connections'][port] != bits:
                    raise ValueError('original clock input changed: '+name+'.'+port)
    return experiment, candidate_path, placement


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--experiment', type=Path, default=ROOT/'build/reset-replication/experiment.json')
    parser.add_argument('--baseline', type=Path, default=ROOT/'build/loadable-ulx3s')
    parser.add_argument('--directory', type=Path, default=ROOT/'build/reset-replication-route')
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    experiment_path = args.experiment.resolve(); baseline = args.baseline.resolve()
    directory = args.directory.resolve()
    if directory in (baseline, experiment_path.parent):
        parser.error('routing outputs must be separate from input artifacts')
    directory.mkdir(parents=True, exist_ok=True)
    receipt = directory/'manifest.json'
    for name in ('manifest.json', 'wasmetal.bit', 'wasmetal.pending.bit'):
        (directory/name).unlink(missing_ok=True)
    experiment, candidate, placement = prepare(experiment_path, baseline)
    dependencies = [experiment_path, candidate, placement, Path(__file__).resolve(),
        ROOT/'tools/replicate_reset.py', ROOT/'tools/build_standalone_board.py',
        ROOT/'tools/build_board.py', ROOT/'tools/check_timing.py', ROOT/'tools/standalone_support.py',
        ROOT/'tools/prepare_standalone.py', ROOT/'tools/cad.py', ROOT/'soc/loader/ulx3s.lpf',
        *[cad.SUITE/'libexec'/name for name in ('nextpnr-ecp5', 'ecppack', 'ecpunpack')]]
    inputs = dict(experiment['inputs'])
    inputs[str(candidate.relative_to(ROOT))] = experiment['candidate_sha256']
    inputs[str(placement.relative_to(ROOT))] = experiment['artifacts']['placement']
    for path in dependencies:
        name = str(path.relative_to(ROOT)); value = digest(path)
        if name in inputs and inputs[name] != value:
            raise ValueError('inconsistent input identity: '+name)
        inputs[name] = value
    check_inputs(inputs)
    report = {'status': 'checked' if args.check_only else 'running', 'inputs': inputs,
        'structural_equivalence_rechecked': True, 'original_clock_inputs_unchanged': True,
        'routing_completed': False, 'timing_passed': False, 'bitstream_round_trip_passed': False,
        'physical_hardware_tested': False, 'default_board_build_changed': False}
    receipt.write_text(json.dumps(report, indent=2)+'\n')
    if args.check_only:
        print('PASS structural equivalence, unchanged clock inputs and artifact identities')
        return
    gc.collect()
    command = ['--85k', '--package', 'CABGA381', '--speed', '6', '--seed', '1',
        '--router', 'router2', '--lpf', str(ROOT/'soc/loader/ulx3s.lpf'), '--freq', '25',
        '--json', str(placement), '--write', str(directory/'routed.json'), '--no-pack', '--no-place',
        '--textcfg', str(directory/'design.config'), '--report', str(directory/'timing.json'),
        '--router2-heatmap', str(directory/'congestion')]
    report['routing_command'] = command
    def interrupted(number, frame):
        raise InterruptedError('routing interrupted by signal '+str(number))
    signal.signal(signal.SIGTERM, interrupted)
    try:
        receipt.write_text(json.dumps(report, indent=2)+'\n')
        with (directory/'routing.log').open('w') as log:
            subprocess.run(cad.command('nextpnr-ecp5')+command, cwd=ROOT, env=cad.environment(),
                stdout=log, stderr=subprocess.STDOUT, check=True)
        report['routing_completed'] = True
        report['timing'] = audit(directory/'timing.json'); report['timing_passed'] = True
        pending = directory/'wasmetal.pending.bit'
        with (directory/'packing.log').open('w') as log:
            for tool, arguments in [('ecppack', [str(directory/'design.config'), str(pending), '--compress']),
                    ('ecpunpack', [str(pending), str(directory/'unpacked.config')]),
                    ('ecppack', [str(directory/'unpacked.config'), str(directory/'repacked.bit'), '--compress'])]:
                subprocess.run(cad.command(tool)+arguments, cwd=ROOT, env=cad.environment(),
                    stdout=log, stderr=subprocess.STDOUT, check=True)
        if pending.read_bytes() != (directory/'repacked.bit').read_bytes():
            raise ValueError('bitstream round trip differs')
        check_inputs(inputs)
        report['bitstream_round_trip_passed'] = True
        report['artifacts'] = {name: digest(directory/name) for name in
            ('routed.json', 'design.config', 'timing.json', 'routing.log', 'packing.log')}
        report['artifacts']['wasmetal.bit'] = digest(pending)
        pending.replace(directory/'wasmetal.bit')
        report['status'] = 'passed'
    except BaseException as error:
        report['status'] = 'interrupted' if isinstance(error, (InterruptedError, KeyboardInterrupt)) else 'failed'
        report['error'] = str(error)
        raise
    finally:
        receipt.write_text(json.dumps(report, indent=2)+'\n')
    print(directory/'wasmetal.bit')


if __name__ == '__main__':
    main()
