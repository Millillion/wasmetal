#!/usr/bin/env python3
"""Route a verified LUT-replication placement without rebuilding its inputs.

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
import time

import cad
from build_standalone_board import audit
from prepare_standalone import ROOT, digest
from replicate_reset import verify

# Pinned nextpnr Router2Cfg defaults for --router2-alt-weights. Store every
# value explicitly in the replay so saved settings cannot override the trial.
ALTERNATE_WEIGHTS = {
    'router2/alt-weights': '00000000000000000000000000000001',
    'router2/initCurrCongWeight': '5.000000',
    'router2/histCongWeight': '0.500000',
    'router2/currCongWeightMult': '0.000000',
    'router2/estimateWeight': '1.000000',
}


def check_inputs(inputs):
    for name, expected in inputs.items():
        if digest(ROOT/name) != expected:
            raise ValueError('routing input changed: '+name)


def verify_routing_placement(original, replay, router, alternate_weights=False):
    """Allow exactly the selected routing settings; compare every other value."""
    if router not in ('router1', 'router2'):
        raise ValueError('unsupported replay router')
    if alternate_weights and router != 'router2':
        raise ValueError('alternate weights require router2')
    modules = [name for name, module in original['modules'].items()
        if 'settings' in module]
    if len(modules) != 1:
        raise ValueError('placement must have exactly one settings module')
    name = modules[0]
    before = original['modules'][name]['settings']
    if before.get('router') not in ('router1', 'router2'):
        raise ValueError('placement has no recognized saved router')
    after = replay['modules'][name]['settings']
    selected = {'router': router, **(ALTERNATE_WEIGHTS if alternate_weights else {})}
    for key,value in selected.items():
        if after.get(key) != value:
            raise ValueError('replay does not select the requested routing setting: '+key)
    for key in selected:
        if key in before:after[key] = before[key]
        else:after.pop(key)
    try:
        if replay != original:
            raise ValueError('replay changed placement, circuitry or unrelated settings')
    finally:
        after.update(selected)
    return {'settings_module': name, 'saved_router': before['router'],
        'selected_router': router, 'only_router_setting_changed': not alternate_weights,
        'only_selected_routing_settings_changed': True, 'selected_settings': selected,
        'preserved_random_state': before.get('seed')}


def routing_placement(placement, directory, router, alternate_weights=False):
    original = json.loads(placement.read_text())
    replay = json.loads(placement.read_text())
    modules = [module for module in replay['modules'].values() if 'settings' in module]
    if len(modules) != 1:
        raise ValueError('placement must have exactly one settings module')
    modules[0]['settings']['router'] = router
    if alternate_weights:modules[0]['settings'].update(ALTERNATE_WEIGHTS)
    proof = verify_routing_placement(original, replay, router, alternate_weights)
    destination = directory/'placement-for-routing.json'
    destination.write_text(json.dumps(replay, separators=(',', ':'))+'\n')
    if verify_routing_placement(original, json.loads(destination.read_text()), router, alternate_weights) != proof:
        raise ValueError('serialized replay differs from checked placement')
    proof.update({'original_sha256': digest(placement), 'replay_sha256': digest(destination)})
    return destination, proof


def observed_router(text):
    markers = {'router1': 'Info: Routing..', 'router2': 'Info: Running router2...'}
    seen = [name for name, marker in markers.items() if marker in text.splitlines()]
    if len(seen) > 1:
        raise ValueError('routing log identifies multiple algorithms')
    return seen[0] if seen else None


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
    placement_sha = experiment['placement_sha256'] if 'stages' in experiment else experiment['artifacts']['placement']
    if digest(placement) != placement_sha:
        raise ValueError('experiment placement changed')
    check_inputs(experiment['inputs'])
    reference_path = baseline/'design.json'
    if digest(reference_path) != experiment['inputs'][str(reference_path.relative_to(ROOT))]:
        raise ValueError('wrong experiment baseline')
    reference = json.loads(reference_path.read_text())
    candidate = json.loads(candidate_path.read_text())
    top = 'wasmetal_loadable_ulx3s'
    if 'stages' in experiment:
        from replicate_fanout import verify_chain
        proof = verify_chain(reference, candidate, top, experiment['stages'])
    else:
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
    parser.add_argument('--router', choices=['router1', 'router2'], default='router2')
    parser.add_argument('--alternate-weights', action='store_true',
        help='use the pinned router2 alternative congestion weights without changing placement or circuitry')
    parser.add_argument('--timeout-seconds', type=int,
        help='stop routing after this many seconds and retain an incomplete receipt')
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    if args.timeout_seconds is not None and args.timeout_seconds <= 0:
        parser.error('--timeout-seconds must be positive')
    if args.alternate_weights and args.router != 'router2':
        parser.error('--alternate-weights requires --router router2')
    experiment_path = args.experiment.resolve(); baseline = args.baseline.resolve()
    directory = args.directory.resolve()
    if directory in (baseline, experiment_path.parent):
        parser.error('routing outputs must be separate from input artifacts')
    directory.mkdir(parents=True, exist_ok=True)
    receipt = directory/'manifest.json'
    for name in ('manifest.json', 'wasmetal.bit', 'wasmetal.pending.bit'):
        (directory/name).unlink(missing_ok=True)
    experiment, candidate, placement = prepare(experiment_path, baseline)
    replay, replay_proof = routing_placement(placement, directory, args.router, args.alternate_weights)
    dependencies = [experiment_path, candidate, placement, replay, Path(__file__).resolve(),
        ROOT/'tools/replicate_reset.py', ROOT/'tools/build_standalone_board.py',
        ROOT/'tools/build_board.py', ROOT/'tools/check_timing.py', ROOT/'tools/standalone_support.py',
        ROOT/'tools/prepare_standalone.py', ROOT/'tools/cad.py', ROOT/'soc/loader/ulx3s.lpf',
        *[cad.SUITE/'libexec'/name for name in ('nextpnr-ecp5', 'ecppack', 'ecpunpack')]]
    if 'stages' in experiment:
        dependencies.append(ROOT/'tools/replicate_fanout.py')
    inputs = dict(experiment['inputs'])
    inputs[str(candidate.relative_to(ROOT))] = experiment['candidate_sha256']
    inputs[str(placement.relative_to(ROOT))] = digest(placement)
    for path in dependencies:
        name = str(path.relative_to(ROOT)); value = digest(path)
        if name in inputs and inputs[name] != value:
            raise ValueError('inconsistent input identity: '+name)
        inputs[name] = value
    check_inputs(inputs)
    report = {'status': 'checked' if args.check_only else 'running', 'inputs': inputs,
        'router': args.router, 'routing_timeout_seconds': args.timeout_seconds,
        'alternate_weights': args.alternate_weights,
        'routing_placement': replay_proof,
        'structural_equivalence_rechecked': True, 'original_clock_inputs_unchanged': True,
        'routing_completed': False, 'timing_passed': False, 'bitstream_round_trip_passed': False,
        'final_input_checks_passed': False,
        'physical_hardware_tested': False, 'default_board_build_changed': False}
    receipt.write_text(json.dumps(report, indent=2)+'\n')
    if args.check_only:
        check_inputs(inputs);report['final_input_checks_passed'] = True
        receipt.write_text(json.dumps(report, indent=2)+'\n')
        print('PASS structural equivalence, unchanged clock inputs and artifact identities')
        return
    gc.collect()
    command = ['--85k', '--package', 'CABGA381', '--speed', '6', '--seed', '1',
        '--router', args.router, '--lpf', str(ROOT/'soc/loader/ulx3s.lpf'), '--freq', '25',
        '--json', str(replay), '--write', str(directory/'routed.json'), '--no-pack', '--no-place',
        '--textcfg', str(directory/'design.config'), '--report', str(directory/'timing.json')]
    if args.router == 'router2':
        command += ['--router2-heatmap', str(directory/'congestion')]
    report['routing_command'] = command
    def interrupted(number, frame):
        raise InterruptedError('routing interrupted by signal '+str(number))
    signal.signal(signal.SIGTERM, interrupted)
    started = time.monotonic()
    try:
        receipt.write_text(json.dumps(report, indent=2)+'\n')
        with (directory/'routing.log').open('w') as log:
            subprocess.run(cad.command('nextpnr-ecp5')+command, cwd=ROOT, env=cad.environment(),
                stdout=log, stderr=subprocess.STDOUT, check=True, timeout=args.timeout_seconds)
        if observed_router((directory/'routing.log').read_text()) != args.router:
            raise ValueError('routing log does not confirm the requested algorithm')
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
        report['status'] = ('timed_out' if isinstance(error, subprocess.TimeoutExpired) else
            'interrupted' if isinstance(error, (InterruptedError, KeyboardInterrupt)) else 'failed')
        report['error'] = str(error)
        raise
    finally:
        try:
            report['observed_router'] = observed_router((directory/'routing.log').read_text())
        except (OSError, ValueError) as error:
            report['observed_router'] = None
            report['router_observation_error'] = str(error)
        report['elapsed_seconds'] = round(time.monotonic() - started, 3)
        try:
            check_inputs(inputs);report['final_input_checks_passed'] = True
        except BaseException as error:
            report.update(status='failed',final_input_checks_passed=False,input_check_error=str(error))
            (directory/'wasmetal.bit').unlink(missing_ok=True)
            raise
        finally:receipt.write_text(json.dumps(report, indent=2)+'\n')
    print(directory/'wasmetal.bit')


if __name__ == '__main__':
    main()
