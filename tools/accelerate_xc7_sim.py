#!/usr/bin/env python3
"""Recompile a verified 7-series simulator with proven faster LUT models."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess

from build_gate_sim import compilation
from prepare_standalone import ROOT, digest
from standalone_support import verify_simulator
from xc7_lut_model import fast_lut


def build(parent_binary, directory, jobs):
    parent = verify_simulator(parent_binary)
    if parent['backend'] != 'loadable-mapped-xc7-functional' or parent['clock_scale'] != 1:
        raise ValueError('need a verified complete core-clock 7-series simulator')
    if parent.get('model_options', {}).get('fast_luts'):
        raise ValueError('parent already uses accelerated LUT models')
    receipt_path = ROOT/'reports/xc7-luts.json'
    proof = json.loads(receipt_path.read_text())
    if proof['status'] != 'passed' or not proof['binary_equivalence_proven'] or proof['negative_controls_rejected'] != 11:
        raise ValueError('complete LUT proofs and oracle controls must pass first')
    if {(c['width'], c['mode']) for c in proof['checks']} != {(w, m) for w in range(1,7) for m in ('known','four-state')}:
        raise ValueError('incomplete LUT oracle coverage')
    if any(not c['icarus_passed'] or c['mode']=='known' and not c['verilator_passed'] for c in proof['checks']):
        raise ValueError('LUT simulation checks did not pass')
    if parent['netlist_sha256'] not in {n['sha256'] for n in proof['netlists']}:
        raise ValueError('oracle regression omitted the parent circuit tables')
    original = parent_binary.parent.parent
    circuit = original/'circuit.v'; cells = original/'cells.v'; config = original/'vendor.vlt'
    for path in (circuit, cells, config):
        if parent['inputs'].get(str(path.relative_to(ROOT))) != digest(path):
            raise ValueError('parent simulator did not verify generated model: '+str(path))
    parent_receipt = Path(str(parent_binary)+'.build.json')
    dependencies = [Path(__file__).resolve(), ROOT/'tools/xc7_lut_model.py',
                    ROOT/'tools/standalone_support.py', receipt_path, parent_receipt]
    inputs = {**parent['inputs'], **proof['inputs'],
              **{str(p.relative_to(ROOT)): digest(p) for p in dependencies}}

    def recheck():
        for name, value in inputs.items():
            path = Path(name)
            if path.is_absolute() or '..' in path.parts or digest(ROOT/path) != value:
                raise ValueError('accelerated simulation input changed: '+name)
        if verify_simulator(parent_binary) != parent:
            raise ValueError('parent simulator changed')

    recheck()
    candidate = cells.read_text()
    library = (ROOT/'.cache/tools/usr/share/yosys/xilinx/cells_sim.v').read_text()
    for width in range(1,7):
        name = 'LUT'+str(width)
        pattern = r'\bmodule\s+'+name+r'\b.*?\bendmodule'
        original = re.findall(pattern, library, re.S)
        present = re.findall(pattern, candidate, re.S)
        if len(original) != 1 or present != [re.sub(r'\bspecify\b.*?\bendspecify\b', '', original[0], flags=re.S)]:
            raise ValueError('parent LUT differs from the proven library model: '+name)
        candidate, count = re.subn(pattern,
            lambda m: fast_lut(m[0], name), candidate, flags=re.S)
        if count != 1:
            raise ValueError('unexpected parent LUT model inventory: '+name)
    candidate_cells = directory/'cells.v'; candidate_cells.write_text(candidate)
    candidate_config = directory/'vendor.vlt'
    candidate_config.write_text(config.read_text().replace(str(cells), str(candidate_cells)))
    top = parent['top']; obj = directory/'obj'; binary = obj/('V'+top)
    receipt = Path(str(binary)+'.build.json'); receipt.unlink(missing_ok=True)
    options = compilation(True, True)
    flags = options['cflags']+f" -DBIT_TICKS={parent['uart_ticks']} -DCLOCK_SCALE=1 -DUPLOAD_TIMEOUT={parent['upload_timeout']}"
    command = [str(ROOT/'.cache/tools/usr/bin/verilator'), '-Wall', '-Wno-UNUSEDSIGNAL', '--assert',
               '--top-module', top, '--cc', '--exe', '--output-split', '10000', '--output-split-cfuncs', '10000',
               '--Mdir', str(obj), '-CFLAGS', flags, str(candidate_config), str(candidate_cells),
               str(ROOT/'tests/xc7/ram_primitives.sv'), str(circuit), str(ROOT/'tests/standalone/loadable.cpp')]
    make = ['make', '-C', str(obj), '-f', 'V'+top+'.mk', '-j', str(jobs),
            'CXX='+options['compiler'], 'LINK='+options['compiler'], 'VM_USER_CFLAGS='+flags,
            'OPT_FAST=-O3', 'OPT_SLOW=-O3', 'OPT_GLOBAL=-O3']
    env = dict(os.environ, VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator'))
    log = directory/'build.log'
    with log.open('w') as stream:
        subprocess.run(command, cwd=ROOT, env=env, stdout=stream, stderr=subprocess.STDOUT, check=True)
        for path in obj.glob('V*.cpp'):
            warnings = ['Wint-in-bool-context', 'Wbool-operation', 'Wbitwise-instead-of-logical']
            if '_DSP48E1' in path.name:
                warnings.append('Wunused-but-set-variable')
            path.write_text(''.join(f'#pragma GCC diagnostic ignored "-{w}"\n' for w in warnings)+path.read_text())
        subprocess.run(make, cwd=ROOT, env=env, stdout=stream, stderr=subprocess.STDOUT, check=True)
    recheck()
    if digest(Path(options['compiler'])) != options['compiler_sha256']:
        raise ValueError('compiler changed during compilation')
    inputs.update({str(p.relative_to(ROOT)): digest(p) for p in (candidate_cells, candidate_config)})
    result = {**parent, 'inputs': inputs, 'binary_sha256': digest(binary), 'compilation': options,
              'commands': [command, make], 'build_log_sha256': digest(log),
              'parent_simulator_binary_sha256': parent['binary_sha256'],
              'model_options': {'fast_luts': True}, 'whole_system_tests_passed': False,
              'physical_hardware_tested': False}
    receipt.write_text(json.dumps(result, indent=2)+'\n')
    print(binary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--simulator', type=Path, required=True)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--jobs', type=int, default=2)
    args = parser.parse_args()
    directory = args.directory.resolve(); binary = args.simulator.resolve()
    if args.jobs < 1:
        parser.error('--jobs must be positive')
    if ROOT/'build' not in directory.parents or directory == binary.parent.parent:
        parser.error('use a separate directory inside the repository build directory')
    directory.mkdir(parents=True, exist_ok=True)
    with (directory/'.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX|fcntl.LOCK_NB)
        build(binary, directory, args.jobs)


if __name__ == '__main__':
    main()
