#!/usr/bin/env python3
"""Compare a complete mapped upload at 81 clocks/bit with the verified RTL run."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import shutil
import signal
import subprocess
import time

from prepare_standalone import ROOT, digest
from standalone_support import verify_simulator


def require(condition, message):
    if not condition:
        raise ValueError(message)


def compare(expected, observed):
    require(expected == observed, 'mapped UART bytes, clocks or completion state differ from native RTL')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--timeout-seconds', type=int, default=21600)
    args = parser.parse_args()
    if args.timeout_seconds < 1:
        parser.error('--timeout-seconds must be positive')
    directory = ROOT/'build/xc7-board-rate-check'; directory.mkdir(parents=True, exist_ok=True)
    report_path = ROOT/'reports/xc7-board-rate.json'
    reference_path = ROOT/'reports/xc7-loadable-rtl.json'
    native_binary = ROOT/'build/xc7-native-sim/obj/Vwasmetal_loadable'
    mapped_binary = ROOT/'build/xc7-board-rate-gate-fast/obj/Vwasmetal_loadable'
    reference = json.loads(reference_path.read_text())
    require(reference['status'] == 'passed' and len(reference['cases']) == 35,
            'complete board-rate native reference must pass first')
    native = verify_simulator(native_binary); mapped = verify_simulator(mapped_binary)
    require(reference['model'] == native and native['backend'] == 'loadable-xc7-rtl', 'native reference identity differs')
    require(mapped['backend'] == 'loadable-mapped-xc7-functional' and mapped['top'] == native['top'] == 'wasmetal_loadable',
            'complete mapped core-clock system required')
    for key in ('profile','profile_tag','parameters','clock_scale','uart_ticks','upload_timeout'):
        require(mapped[key] == native[key], 'different model configuration: '+key)
    require(mapped['clock_scale'] == 1 and mapped['uart_ticks'] == 81 and mapped['upload_timeout'] == 2000000,
            'expected the unchanged board-rate parameters')
    for name, value in native['inputs'].items():
        if name in mapped['inputs']:
            require(mapped['inputs'][name] == value, 'different shared execution input: '+name)
        if name.startswith(('rtl/','soc/')) and Path(name).suffix in ('.sv','.svh','.v','.vi','.json'):
            require(mapped['inputs'].get(name) == value, 'different RTL/system source: '+name)
    cases = [c for c in reference['cases'] if c['name'] == 'answer']
    require(len(cases) == 1 and cases[0]['result']['status'] == 0 and cases[0]['result']['trap'] == 0
            and cases[0]['result']['values'] == [42] and type(cases[0]['result']['cycles']) is int
            and cases[0]['result']['cycles'] > 0,
            'unexpected native answer case')
    case = cases[0]
    original_packet = ROOT/'build/loadable-cases/loadable-xc7-rtl/answer/program.wmu'
    require(digest(original_packet) == case['packet_sha256'], 'native upload packet changed')
    packet = directory/'answer.wmu'; shutil.copyfile(original_packet, packet)
    dependencies = [Path(__file__).resolve(), ROOT/'tools/standalone_support.py', ROOT/'tools/prepare_standalone.py',
                    reference_path, original_packet, packet, Path(str(native_binary)+'.build.json'),
                    Path(str(mapped_binary)+'.build.json')]
    inputs = {str(p.relative_to(ROOT)): digest(p) for p in dependencies}
    for name, value in reference['inputs'].items():
        path = Path(name)
        require(not path.is_absolute() and '..' not in path.parts and digest(ROOT/path) == value,
                'native checker input changed: '+name)
        inputs[name] = value
    command = [str(mapped_binary), '--upload', str(packet)]
    started = time.monotonic()
    result = {'status':'running', 'scope':'one complete prepared-program upload and execution at 81 core clocks per UART bit',
              'models':{'rtl':native,'mapped':mapped}, 'inputs':inputs, 'native_reference_case':case,
              'command':command, 'wall_timeout_seconds':args.timeout_seconds, 'case_count':0,
              'uart_and_cycles_identical':False, 'physical_hardware_tested':False}

    def save():
        result['elapsed_seconds'] = time.monotonic()-started
        report_path.write_text(json.dumps(result,indent=2)+'\n')

    def interrupted(number, frame):
        raise InterruptedError('board-rate check interrupted by signal '+str(number))

    signal.signal(signal.SIGTERM, interrupted)
    save()
    stdout = directory/'mapped.jsonl'; stderr = directory/'mapped.stderr'
    process = None
    try:
        with stdout.open('w') as out, stderr.open('w') as err:
            process = subprocess.Popen(command,cwd=ROOT,stdout=out,stderr=err)
            process.wait(timeout=args.timeout_seconds)
        require(process.returncode == 0, 'mapped execution failed: '+stderr.read_text()[-2000:])
        require(not stderr.read_text().strip(), 'unexpected mapped simulator diagnostics')
        observed = json.loads(stdout.read_text())
        compare(case['uart'],observed)
        controls = []
        for field in ('clocks','commit_clock','first_result_clock','interrupted','uart','operation'):
            wrong = deepcopy(observed)
            if field == 'interrupted': wrong[field] = not wrong[field]
            elif field == 'uart': wrong[field] = f"{int(wrong[field][:2],16)^1:02x}"+wrong[field][2:]
            elif field == 'operation': wrong[field] = 'wrong-operation'
            else: wrong[field] += 1
            try:
                compare(case['uart'],wrong)
            except ValueError:
                controls.append(field)
            else:
                raise ValueError('accepted corrupted observed field: '+field)
        require(verify_simulator(native_binary) == native and verify_simulator(mapped_binary) == mapped,
                'execution identity changed during comparison')
        for name, value in inputs.items():
            require(digest(ROOT/name) == value, 'verification input changed: '+name)
        result.update(status='passed',case_count=1,uart_and_cycles_identical=True,mapped_observation=observed,
                      comparison_fault_controls_rejected=controls)
    except BaseException as error:
        result.update(status='timed_out' if isinstance(error,subprocess.TimeoutExpired) else
                      'interrupted' if isinstance(error,(InterruptedError,KeyboardInterrupt)) else 'failed',error=str(error))
        raise
    finally:
        if process is not None and process.poll() is None:
            process.terminate()
            try: process.wait(timeout=10)
            except subprocess.TimeoutExpired: process.kill(); process.wait(timeout=10)
        result['artifacts'] = {str(p.relative_to(ROOT)):digest(p) for p in (stdout,stderr) if p.exists()}
        save()
    print('PASS complete 81-clock/bit mapped upload, CPU result and exact native UART/cycle comparison')


if __name__ == '__main__':
    main()
