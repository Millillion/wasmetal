#!/usr/bin/env python3
"""Reject changes outside the selected router when replaying a placement."""
import copy
import json
from pathlib import Path
import tempfile

from prepare_standalone import ROOT, digest
from route_reset_experiment import observed_router, routing_placement, verify_routing_placement


def main():
    original = {'creator': 'fixture', 'modules': {'top': {
        'settings': {'router': 'router2', 'seed': '1011001', 'target_freq': '25000000'},
        'ports': {'clock': {'direction': 'input', 'bits': [2]}},
        'cells': {'lut': {'type': 'TRELLIS_COMB', 'parameters': {'LUT0_INITVAL': '01'},
                         'attributes': {'NEXTPNR_BEL': 'X1/Y1/SLICEA'}, 'connections': {'A': [3]}},
                  'ff': {'type': 'TRELLIS_FF', 'connections': {'CLK': [2], 'DI': [4]}}},
        'netnames': {'clock': {'bits': [2], 'attributes': {'clock': 'yes'}}}}}}
    inputs = {str(p.relative_to(ROOT)): digest(p) for p in
        [Path(__file__).resolve(), ROOT/'tools/route_reset_experiment.py', ROOT/'tools/prepare_standalone.py']}
    negatives = []
    with tempfile.TemporaryDirectory(prefix='routing-placement-') as temporary:
        directory = Path(temporary)
        source = directory/'placed.json'
        source.write_text(json.dumps(original)+'\n')
        source_digest = digest(source)
        for selected in ['router1', 'router2']:
            path, proof = routing_placement(source, directory, selected)
            replay = json.loads(path.read_text())
            assert proof['only_router_setting_changed'] and digest(source) == source_digest
            assert replay['modules']['top']['settings']['router'] == selected
        path, _ = routing_placement(source, directory, 'router1')
        replay = json.loads(path.read_text())
        mutations = [
            ('logic-value', ('cells','lut','parameters','LUT0_INITVAL'), '10'),
            ('placed-location', ('cells','lut','attributes','NEXTPNR_BEL'), 'X2/Y2/SLICEA'),
            ('clock-connection', ('cells','ff','connections','CLK'), [8]),
            ('data-connection', ('cells','ff','connections','DI'), [8]),
            ('primitive-type', ('cells','ff','type'), 'TRELLIS_COMB'),
            ('random-state', ('settings','seed'), '1'),
            ('timing-target', ('settings','target_freq'), '1000000'),
            ('port-connection', ('ports','clock','bits'), [9]),
            ('net-attribute', ('netnames','clock','attributes','clock'), 'no'),
            ('wrong-router', ('settings','router'), 'router2')]
        for name, keys, value in mutations:
            mutant = copy.deepcopy(replay)
            current = mutant['modules']['top']
            for key in keys[:-1]:
                current = current[key]
            current[keys[-1]] = value
            try:
                verify_routing_placement(original, mutant, 'router1')
            except ValueError as error:
                negatives.append({'name': name, 'diagnostic': str(error)})
            else:
                raise AssertionError('mutation accepted: '+name)
        for name in ['extra-settings-module', 'missing-saved-router']:
            mutant = copy.deepcopy(original)
            if name == 'extra-settings-module':
                mutant['modules']['extra'] = {'settings': {'router': 'router2'}}
            else:
                del mutant['modules']['top']['settings']['router']
            try:
                verify_routing_placement(mutant, replay, 'router1')
            except ValueError as error:
                negatives.append({'name': name, 'diagnostic': str(error)})
            else:
                raise AssertionError('invalid source accepted: '+name)
        assert digest(source) == source_digest
    assert observed_router('Info: Routing..\nInfo: Routing 123 arcs.\n') == 'router1'
    assert observed_router('Info: Running router2...\n') == 'router2'
    assert observed_router('Info: Setting up routing resources...\n') is None
    try:
        observed_router('Info: Routing..\nInfo: Running router2...\n')
    except ValueError as error:
        negatives.append({'name': 'ambiguous-router-log', 'diagnostic': str(error)})
    else:
        raise AssertionError('ambiguous router log accepted')
    assert len(negatives) == 13
    assert all(digest(ROOT/name) == value for name, value in inputs.items())
    report = ROOT/'reports/routing-placement-driver.json'
    report.parent.mkdir(exist_ok=True)
    report.write_text(json.dumps({'status': 'passed', 'inputs': inputs,
        'scope': 'Placement replay metadata guard and pinned router-log parser; no physical-fit claim',
        'supported_routers': ['router1', 'router2'], 'source_unchanged': True,
        'negative_controls_rejected': len(negatives), 'negative_controls': negatives}, indent=2)+'\n')
    print('PASS placement replay: both routers and 13 rejected changes or ambiguous logs')


if __name__ == '__main__':
    main()
