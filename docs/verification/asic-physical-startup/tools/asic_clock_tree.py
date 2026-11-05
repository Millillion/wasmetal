"""Audit the non-inverting clock tree used by the experimental startup block."""
from copy import deepcopy

from asic_cells import require


FLIP_FLOPS = {'sky130_fd_sc_hd__dfxtp_' + str(drive) for drive in (1, 2, 4)}
CLOCK_BUFFERS = {'sky130_fd_sc_hd__clkbuf_' + str(drive) for drive in (4, 8, 16)}


def audit_clock_tree(module, reference):
    """Check actual clock wiring before using a synchronous equivalence engine.

    This is a binary connectivity check, not a delay, skew or pulse-width check.
    The caller must also validate the selected cell definitions and pin schemas.
    """
    port = module['ports']['clk']
    require(port['direction'] == 'input' and len(port['bits']) == 1 and
            type(port['bits'][0]) is int, 'invalid primary clock port')
    clock = port['bits'][0]
    flops = {name: cell for name, cell in module['cells'].items() if cell['type'] in FLIP_FLOPS}
    expected = {name for name, cell in reference['cells'].items() if cell['type'] in FLIP_FLOPS}
    require(flops and set(flops) == expected, 'physical optimization changed state-instance inventory')
    drivers = {}
    for name, entry in module['ports'].items():
        if entry['direction'] == 'input':
            for bit in entry['bits']:
                drivers.setdefault(bit, []).append(('input', name, ''))
    for name, cell in module['cells'].items():
        for pin, direction in cell['port_directions'].items():
            if direction == 'output':
                for bit in cell['connections'][pin]:
                    drivers.setdefault(bit, []).append(('cell', name, pin))
    require(drivers.get(clock) == [('input', 'clk', '')], 'primary clock has another driver')
    paths = {}
    for name, cell in flops.items():
        pins = cell['connections'].get('CLK', [])
        require(len(pins) == 1 and type(pins[0]) is int, 'missing or nonscalar flip-flop clock')
        bit, seen, path = pins[0], set(), []
        while bit != clock:
            require(bit not in seen, 'clock tree contains a cycle')
            seen.add(bit)
            require(len(drivers.get(bit, [])) == 1, 'undriven or multiply driven clock-tree signal')
            kind, driver, pin = drivers[bit][0]
            require(kind == 'cell', 'flip-flop clock reaches an input other than clk')
            gate = module['cells'][driver]
            require(gate['type'] in CLOCK_BUFFERS and pin == 'X',
                    'clock path contains an unapproved or inverting cell')
            inputs = gate['connections'].get('A', [])
            require(len(inputs) == 1 and type(inputs[0]) is int, 'invalid clock-buffer input')
            path.append(driver)
            bit = inputs[0]
        paths[name] = path
    return {'status': 'passed', 'flip_flops': len(flops),
            'state_instance_names_unchanged': True,
            'all_clock_sources_original_primary_clock': True,
            'allowed_clock_cells': sorted(CLOCK_BUFFERS),
            'minimum_buffer_depth': min(map(len, paths.values())),
            'maximum_buffer_depth': max(map(len, paths.values())), 'paths': paths}


def canonical_clock_view(module, reference):
    """Return an audited copy for the separate single-clock structural checker.

    The original circuit remains the input to simulation and equivalence.
    """
    audit = audit_clock_tree(module, reference)
    canonical = deepcopy(module)
    for name in audit['paths']:
        canonical['cells'][name]['connections']['CLK'] = list(canonical['ports']['clk']['bits'])
    return canonical, audit


def fault_controls(module, reference):
    """Inject clock faults into the actual circuit; none may pass the audit."""
    good = audit_clock_tree(module, reference)
    controls = []

    def reject(label, mutate):
        variant = deepcopy(module)
        mutate(variant)
        try:
            audit_clock_tree(variant, reference)
        except ValueError as error:
            controls.append({'name': label, 'diagnostic': str(error)})
        else:
            raise ValueError('clock audit accepted fault: ' + label)

    for kind in sorted(FLIP_FLOPS):
        names = [name for name, cell in module['cells'].items() if cell['type'] == kind]
        if names:
            reject('wrong-clock-' + kind.rsplit('_', 1)[1], lambda m, name=names[0]:
                   m['cells'][name]['connections'].update(CLK=list(m['ports']['reset']['bits'])))
    name = next(iter(good['paths']))
    buffers = sorted({buffer for path in good['paths'].values() for buffer in path})
    require(buffers, 'clock-tree fault campaign requires inserted clock buffers')
    buffer = buffers[0]

    def invert(m):
        cell = m['cells'][buffer]
        cell['type'] = cell['type'].replace('__clkbuf_', '__clkinv_')
        cell['connections']['Y'] = cell['connections'].pop('X')
        cell['port_directions']['Y'] = cell['port_directions'].pop('X')

    reject('inverted-clock-buffer', invert)
    reject('clock-buffer-cycle', lambda m: m['cells'][buffer]['connections'].update(
        A=list(m['cells'][buffer]['connections']['X'])))
    require('fault_duplicate_clock' not in module['cells'], 'fault-control name collision')
    reject('duplicate-clock-driver', lambda m: m['cells'].update(
        fault_duplicate_clock=deepcopy(m['cells'][buffer])))
    reject('missing-flop-clock', lambda m: m['cells'][name]['connections'].pop('CLK'))
    reject('wide-flop-clock', lambda m: m['cells'][name]['connections']['CLK'].append(
        m['ports']['clk']['bits'][0]))
    require('fault_renamed_state' not in module['cells'], 'fault-control name collision')
    reject('changed-state-instance', lambda m: m['cells'].update(
        fault_renamed_state=m['cells'].pop(name)))
    return controls
