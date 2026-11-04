#!/usr/bin/env python3
"""Check startup RTL against SKY130HD standard-cell functional mapping."""
from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from asic_cells import LOCK, audit_circuit, connectivity, filter_library, inputs, require
from check_memory_startup import CONFIGURATIONS, TOP, BINDING, HARNESS, SOURCE, DEPENDENCIES
from prepare_standalone import ROOT, digest
from run_xc7_system import stop_workers


YOSYS = ROOT / '.cache/tools/usr/bin/yosys'
BASE = ROOT / 'build/asic-startup'


def execute(command, logfile, timeout=600, env=None, accepted_failure=False):
    with logfile.open('w') as log:
        process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=log,
                                   stderr=subprocess.STDOUT, start_new_session=True)
        try:
            result = process.wait(timeout=timeout)
        finally:
            stop_workers([process])
    if result and not accepted_failure:
        raise ValueError(f'ASIC verification command failed ({result}); see {logfile}')
    return result


def yosys(script, directory, label, accepted_failure=False):
    path, logfile = directory / (label + '.ys'), directory / (label + '.log')
    path.write_text(script)
    result = execute([str(YOSYS), '-Q', '-T', '-s', str(path)], logfile,
                     accepted_failure=accepted_failure)
    return result, logfile


def rtl(size, latency, timeout):
    return ('read_verilog -sv ' + ' '.join(map(str, [*DEPENDENCIES, SOURCE, BINDING])) + '\n' +
            f'chparam -set RAM_BYTES {size} -set READ_LATENCY {latency} -set RESPONSE_TIMEOUT {timeout} {TOP}\n')


def build_model(directory, size, latency, timeout):
    command = [str(ROOT / '.cache/tools/usr/bin/verilator'), '-Wall', '-Wno-UNUSEDSIGNAL',
        '--top-module', TOP, '--cc', '--exe', '--build', '-j', '2', '--Mdir', str(directory / 'obj'),
        '-CFLAGS', f'-std=c++17 -O2 -Wall -Wextra -Werror -DTEST_BYTES={size} -DTEST_LATENCY={latency} -DTEST_TIMEOUT={timeout}',
        str(directory / 'vendor.vlt'), str(directory / 'cells.v'), str(directory / 'mapped.v'), str(HARNESS)]
    execute(command, directory / 'build.log', env=dict(os.environ,
            VERILATOR_ROOT=str(ROOT / '.cache/tools/usr/share/verilator')))
    return directory / ('obj/V' + TOP)


def proofs(directory, size, latency, timeout, accepted_failure=False):
    # Keep the unnormalized netlist's public state names and the synthesizer's
    # explicit FSM encoding map. The simulated netlist has identical pin incidence.
    setup = rtl(size, latency, timeout) + f'prep -top {TOP} -flatten\nmemory_map\nopt_clean\n'
    setup += f'rename {TOP} gold\ndesign -stash gold\n'
    setup += f'read_verilog {directory}/cells.v {directory}/proof-circuit.v\nprep -top {TOP} -flatten\n'
    setup += f'rename {TOP} gate\ndesign -stash gate\n'
    setup += 'design -copy-from gold -as gold gold\ndesign -copy-from gate -as gate gate\n'
    direct = setup + 'miter -equiv -flatten gold gate reset_pins\nhierarchy -top reset_pins\n'
    direct += 'sat -seq 12 -set-at 1 in_reset 1 -set-def-inputs -set-init-undef -enable_undef -prove-skip 1 -prove trigger 0 -verify\n'
    result, log = yosys(direct, directory, 'reset-pins', accepted_failure)
    if accepted_failure:
        require(result != 0 and 'proof did fail' in log.read_text(), 'faulty ASIC circuit escaped reset proof')
        return {'rejected': True, 'log_sha256': digest(log)}
    require('SAT proof finished - no model found: SUCCESS!' in log.read_text(), 'missing independent reset-pin proof')
    script = setup + f'equiv_make -encfile {directory}/fsm.enc gold gate equiv\nhierarchy -top equiv\n'
    script += f'write_rtlil {directory}/equiv.il\nequiv_simple\nequiv_induct -undef -seq 12\nequiv_status -assert\n'
    _, induction = yosys(script, directory, 'equivalence')
    require('Equivalence successfully proven!' in induction.read_text(), 'missing inductive equivalence result')
    script = f'read_rtlil {directory}/equiv.il\nequiv_miter -assert -undef reset_points\n'
    script += 'hierarchy -top reset_points\nflatten\nopt_clean\n'
    script += 'sat -seq 12 -set-at 1 reset 1 -set-def-inputs -set-init-undef -enable_undef -prove-skip 1 -prove-asserts -verify\n'
    _, base = yosys(script, directory, 'reset-points')
    require('SAT proof finished - no model found: SUCCESS!' in base.read_text(), 'missing comparison-point reset base')
    return {'inductive_equivalence': True, 'reset_base_cycles': 12,
            'reset_pin_log_sha256': digest(log), 'reset_point_log_sha256': digest(base),
            'induction_log_sha256': digest(induction)}


def map_circuit(directory, library, excluded, size, latency, timeout):
    directory.mkdir(parents=True, exist_ok=True)
    script = f'read_liberty -lib -ignore_miss_func {library}\n' + rtl(size, latency, timeout)
    script += f'synth -top {TOP} -flatten -noabc -encfile {directory}/fsm.enc\n'
    script += f'dfflibmap -liberty {library}\nabc -liberty {library}\n'
    script += 'hilomap -singleton -hicell sky130_fd_sc_hd__conb_1 HI -locell sky130_fd_sc_hd__conb_1 LO\nclean\ncheck -assert\n'
    script += f'write_json {directory}/proof-circuit.json\nwrite_verilog -noattr -noexpr -nodec {directory}/proof-circuit.v\n'
    script += f'splitnets\nclean -purge\ncheck -assert\nstat -liberty {library}\n'
    script += f'write_json {directory}/mapped.json\nwrite_verilog -noattr -noexpr -nodec {directory}/mapped.v\n'
    yosys(script, directory, 'mapping')
    raw = json.loads((directory / 'proof-circuit.json').read_text())
    mapped = json.loads((directory / 'mapped.json').read_text())
    modules = {name: module for name, module in mapped['modules'].items() if name != TOP}
    counts = audit_circuit(mapped['modules'][TOP], modules, excluded)
    require(connectivity(raw['modules'][TOP]) == connectivity(mapped['modules'][TOP]),
            'simulator normalization changed circuit pin incidence')
    script = f'read_liberty -ignore_miss_func -ignore_miss_dir -ignore_miss_data_latch {library}\nselect -clear\n'
    script += 'select ' + ' '.join(sorted(counts)) + f'\nwrite_verilog -selected -noattr {directory}/cells.v\n'
    yosys(script, directory, 'cell-models')
    script = f'read_verilog {directory}/cells.v {directory}/mapped.v\nhierarchy -check -top {TOP}\n'
    script += 'proc\nflatten\nopt\nscc -expect 0\ncheck -assert\n'
    _, log = yosys(script, directory, 'acyclic')
    require('Found 0 SCCs' in log.read_text(), 'ASIC circuit has a combinational cycle')
    # All inputs and driven output bits were checked above. The tie cell's unused
    # HI output may be omitted. A constant output bit feeds other bits of the
    # completed_operations vector; the bit-level graph has no cycle.
    config = '`verilator_config\n'
    for filename, rules in [('cells.v', ['DECLFILENAME']), ('mapped.v', ['DECLFILENAME', 'PINMISSING'])]:
        for rule in rules:
            config += f'lint_off -rule {rule} -file "{directory}/{filename}"\n'
    config += f'lint_off -rule UNOPTFLAT -file "{directory}/mapped.v" -match "*Circular combinational logic: \'completed_operations\'*"\n'
    (directory / 'vendor.vlt').write_text(config)
    return counts


def negative_controls(excluded):
    good = BASE / '80-3-11'
    original = json.loads((good / 'mapped.json').read_text())
    module = original['modules'][TOP]
    library_modules = {name: value for name, value in original['modules'].items() if name != TOP}
    directory = BASE / 'negative'
    directory.mkdir(exist_ok=True)
    controls = []
    flop = next(name for name, cell in module['cells'].items() if cell['type'] == 'sky130_fd_sc_hd__dfxtp_1')
    tie = next(name for name, cell in module['cells'].items() if cell['type'] == 'sky130_fd_sc_hd__conb_1' and 'LO' in cell['connections'])

    def reject(name, change):
        mutant = deepcopy(module)
        change(mutant)
        try:
            audit_circuit(mutant, library_modules, excluded)
        except ValueError as error:
            controls.append({'name': name, 'diagnostic': str(error)})
        else:
            raise ValueError('ASIC structural audit accepted fault: ' + name)

    reject('forbidden-power-cell', lambda m: m['cells'][flop].update(type='sky130_fd_sc_hd__lpflow_inputiso1p_1'))
    reject('unmapped-generic-cell', lambda m: m['cells'][flop].update(type='$_DFF_P_'))
    reject('missing-cell-input', lambda m: m['cells'][flop]['connections'].pop('D'))
    reject('undriven-constant', lambda m: m['cells'][tie]['connections'].pop('LO'))
    reject('multiple-drivers', lambda m: m['cells'].update(duplicate_driver=deepcopy(m['cells'][flop])))
    reject('wrong-flop-clock', lambda m: m['cells'][flop]['connections'].update(CLK=m['ports']['reset']['bits']))
    reject('unknown-cell-input', lambda m: m['cells'][flop]['connections'].update(D=['x']))
    reject('wrong-pin-width', lambda m: m['cells'][flop]['connections']['D'].append(m['ports']['reset']['bits'][0]))
    reject('power-on-initialization', lambda m: next(iter(m['netnames'].values()))['attributes'].update(init='0'))
    mutant = deepcopy(module)
    mutant['cells'][flop]['connections']['D'] = mutant['ports']['reset']['bits']
    require(connectivity(mutant) != connectivity(module), 'normalization audit missed a changed connection')
    controls.append({'name': 'normalization-rewired-input', 'diagnostic': 'canonical cell-pin incidence differs'})
    renamed = deepcopy(module)
    for port in renamed['ports'].values():
        port['bits'] = [bit + 100000 for bit in port['bits']]
    for cell in renamed['cells'].values():
        cell['connections'] = {pin: [bit + 100000 for bit in bits] for pin, bits in cell['connections'].items()}
    require(connectivity(renamed) == connectivity(module), 'normalization audit depends on arbitrary bit numbers')
    probe = directory / 'cycle.sv'
    probe.write_text('module cycle(input wire toggle,output wire result);\nwire feedback;assign feedback=result;assign result=feedback^toggle;\nendmodule\n')
    result, log = yosys(f'read_verilog {probe}\nprep -top cycle\nscc -expect 0\n', directory, 'cycle', True)
    require(result != 0 and 'Found 1 SCCs but expected 0' in log.read_text(), 'ASIC cycle audit accepted feedback')
    controls.append({'name': 'combinational-feedback', 'log_sha256': digest(log)})

    # A legal standard-cell circuit with its sole tie-low output wired to HI.
    # It passes structural checks, then must fail both the functional oracle and
    # a proof comparing independent copies of RTL and the mutated circuit.
    fault = directory / 'wrong-constant'
    fault.mkdir(exist_ok=True)
    for label in ('mapped', 'proof-circuit'):
        data = json.loads((good / (label + '.json')).read_text())
        cell = data['modules'][TOP]['cells'][tie]
        cell['connections']['HI'] = cell['connections'].pop('LO')
        cell['port_directions']['HI'] = cell['port_directions'].pop('LO')
        audit_circuit(data['modules'][TOP], library_modules, excluded)
        path = fault / (label + '.json')
        path.write_text(json.dumps(data) + '\n')
        yosys(f'read_json {path}\nwrite_verilog -noattr -noexpr -nodec {fault}/{label}.v\n', fault, label + '-emit')
    (fault / 'cells.v').write_bytes((good / 'cells.v').read_bytes())
    (fault / 'vendor.vlt').write_text((good / 'vendor.vlt').read_text().replace(str(good), str(fault)))
    binary = build_model(fault, 80, 3, 11)
    logfile = fault / 'rejection.log'
    result = execute([str(binary)], logfile, accepted_failure=True)
    require(result != 0 and 'startup' in logfile.read_text(), 'wrong ASIC tie cell escaped the independent SRAM oracle')
    controls.append({'name': 'wrong-tie-cell-simulation', 'binary_sha256': digest(binary),
                     'netlist_sha256': digest(fault / 'mapped.json'), 'log_sha256': digest(logfile),
                     'diagnostic': logfile.read_text().strip()})
    proof = proofs(fault, 80, 3, 11, accepted_failure=True)
    controls.append({'name': 'wrong-tie-cell-formal', **proof})
    binary = good / ('obj/V' + TOP)
    logfile = directory / 'corrupt-read.log'
    result = execute([str(binary), '--corrupt-read'], logfile, accepted_failure=True)
    require(result != 0 and 'startup' in logfile.read_text(), 'ASIC model accepted a corrupt SRAM read')
    controls.append({'name': 'corrupt-sram-read', 'binary_sha256': digest(binary),
                     'log_sha256': digest(logfile), 'diagnostic': logfile.read_text().strip()})
    (directory / 'controls.json').write_text(json.dumps(controls, indent=2) + '\n')
    return controls


def main():
    started = time.monotonic()
    BASE.mkdir(parents=True, exist_ok=True)
    output = ROOT / 'reports/asic-startup.json'
    output.parent.mkdir(exist_ok=True)
    output.unlink(missing_ok=True)
    upstream = inputs()
    library, filtering = filter_library(upstream, BASE / 'library')
    paths = [*upstream.values(), LOCK, SOURCE, BINDING, HARNESS, *DEPENDENCIES,
             Path(__file__).resolve(), ROOT / 'tools/asic_cells.py', ROOT / 'tools/check_memory_startup.py',
             ROOT / 'tools/build_standalone_gate_sim.py', ROOT / 'tools/build_board.py',
             ROOT / 'tools/run_xc7_system.py', ROOT / 'tools/prepare_standalone.py', ROOT / 'tools/upstream.lock.json',
             YOSYS, ROOT / '.cache/tools/usr/bin/yosys-abc', ROOT / '.cache/tools/usr/bin/verilator_bin']
    bound = {str(path.relative_to(ROOT)): digest(path) for path in paths}
    checks = []
    for size, latency, timeout in CONFIGURATIONS:
        directory = BASE / f'{size}-{latency}-{timeout}'
        counts = map_circuit(directory, library, set(filtering['excluded_cells']), size, latency, timeout)
        proof = proofs(directory, size, latency, timeout)
        native = directory / 'native'
        code = ('import sys;from pathlib import Path;sys.path.insert(0,"tools");'
                'from check_memory_startup import native,SOURCE;'
                'native(SOURCE,Path(sys.argv[1]),*map(int,sys.argv[2:]))')
        execute([sys.executable, '-c', code, str(native), str(size), str(latency), str(timeout)], directory / 'native-driver.log')
        binaries = {'rtl': native / ('obj/V' + TOP), 'standard_cells': build_model(directory, size, latency, timeout)}
        tests = {}
        for name, binary in binaries.items():
            logfile = directory / (name + '-observations.log')
            execute([str(binary)], logfile, timeout=900)
            tests[name] = {'binary_sha256': digest(binary), 'log_sha256': digest(logfile),
                           'observations': json.loads(logfile.read_text())}
        require(tests['rtl']['observations'] == tests['standard_cells']['observations'],
                'RTL and ASIC-cell observations differ')
        checks.append({'ram_bytes': size, 'read_latency': latency, 'response_timeout': timeout,
                       'standard_cells': counts, 'netlist_sha256': digest(directory / 'mapped.json'),
                       'functional_models_sha256': digest(directory / 'cells.v'), 'proofs': proof, 'tests': tests})
        print('PASS ASIC startup', size, latency, timeout, tests['rtl']['observations'], flush=True)
    controls = negative_controls(set(filtering['excluded_cells']))
    for name, sha in bound.items():
        require(digest(ROOT / name) == sha, 'ASIC mapping input changed: ' + name)
    report = {'status': 'passed', 'scope': 'startup controller, test master and SRAM adapter; no CPU or SRAM array',
              'backend': 'mapped-sky130hd-functional', 'inputs': bound, 'filter': filtering, 'checks': checks,
              'negative_controls': controls, 'negative_controls_rejected': len(controls),
              'elapsed_seconds': time.monotonic() - started, 'physical_hardware_tested': False,
              'limitations': ['Liberty-derived binary functional models; no SDF, analog or power simulation.',
                  'No ASIC placement, routing, clock tree, SRAM macro, timing closure or foundry signoff.',
                  'Only the typical 1.8 V, 25 C cell library is used. No process-corner closure is claimed.']}
    output.write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
