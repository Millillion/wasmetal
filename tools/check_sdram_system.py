#!/usr/bin/env python3
"""Run the complete programmable CPU through SDRAM pins and a behavioral device."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from build_standalone_sim import sources
from check_sdram import PROFILES
from loadable_ci import GROUPS,RECOVERY,check_plan
from prepare_standalone import ROOT,digest,load_profile,prepare
from program_upload import profile_tag,encode
from standalone_support import generate_parameters,parameters,verify_simulator,verify_image


def replace_once(text,before,after):
    if text.count(before)!=1:raise ValueError('review SDRAM system binding: '+before)
    return text.replace(before,after)


def build(timing,startup,negative):
    profile=load_profile();generated=generate_parameters();tag=profile_tag(profile)
    device=dict(PROFILES[timing+'-full']);device['RAM_BYTES']=profile['ram_bytes']
    if startup is not None:
        if startup<device['POWERUP_CYCLES']:raise ValueError('startup override cannot shorten device initialization')
        device['POWERUP_CYCLES']=startup
    label=f'sdram-system-{timing}-{device["POWERUP_CYCLES"]}'+('-'+negative if negative else '')
    directory=ROOT/'build'/label;directory.mkdir(parents=True,exist_ok=True)
    header=directory/'sdram_test_parameters.svh'
    header.write_text('`ifndef WASMETAL_SDRAM_TEST_PARAMETERS\n`define WASMETAL_SDRAM_TEST_PARAMETERS\n'+
        ''.join(f'`define SDRAM_{key} {value}\n' for key,value in device.items())+'`endif\n')
    original=ROOT/'soc/wasmetal_local_memory.sv';text=original.read_text()
    text=replace_once(text,'wire bus_valid, bus_write, bus_ready, bus_fault;',
        'wire bus_valid, bus_write, bus_ready, bus_fault;\n    wire backend_initialized;')
    if negative!='startup-bypass':
        text=replace_once(text,'.reset(reset),.initialized(initialized)',
            '.reset(reset || !backend_initialized),.initialized(initialized)')
    text=replace_once(text,'.ready(bus_ready),.fault(bus_fault),.rdata(bus_rdata));',
        '.ready(bus_ready),.fault(bus_fault),.rdata(bus_rdata),.initialized(backend_initialized));')
    local=directory/'wasmetal_local_memory.sv';local.write_text(text)
    backing=ROOT/'soc/memory/wasmetal_bram.sv';binding=ROOT/'tests/sdram/wasmetal_bram.sv'
    model=ROOT/'tests/sdram/wasmetal_test_sdram.sv';harness=ROOT/'tests/sdram/loadable.cpp'
    source=sources()
    if source.count(original)!=1 or source.count(backing)!=1:raise ValueError('ambiguous SDRAM system replacement')
    source=[binding if path==backing else local if path==original else path for path in source]+[model]
    vendor=ROOT/'third_party/hardfloat/source'
    paths=[*source,*sorted(vendor.rglob('*.vi')),harness,original,header,Path(__file__).resolve(),generated,
        ROOT/'tests/standalone/loadable.cpp',ROOT/'tools/build_standalone_sim.py',ROOT/'tools/prepare_standalone.py',
        ROOT/'tools/standalone_support.py',ROOT/'tools/program_upload.py',ROOT/'tools/loadable_ci.py',
        ROOT/'tools/check_sdram.py',ROOT/'soc/profile.json',ROOT/'tools/upstream.lock.json']
    hashes={str(path.relative_to(ROOT)):digest(path) for path in paths}
    params={**parameters(profile),'UART_TICKS':4,'UPLOAD_TIMEOUT_CYCLES':4096,
        'PROFILE_TAG':f"128'h{int.from_bytes(tag,'little'):032x}"}
    command=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL',
        '--unroll-count','512','--assert','-DWASMETAL_ASSERTIONS',
        f'-DWASMETAL_TEST_SDRAM_COVERAGE="{directory}/coverage.jsonl"',
        '--top-module','wasmetal_loadable','-I'+str(vendor),'-I'+str(vendor/'RISCV'),
        '-I'+str(directory),'-I'+str(ROOT/'build'),*[f'-G{name}={value}' for name,value in params.items()],
        '--cc','--exe','--build','-j','2','--Mdir',str(directory/'obj'),
        '-CFLAGS','-std=c++17 -O3 -Wall -Wextra -Werror -DBIT_TICKS=4 -DCLOCK_SCALE=1 -DUPLOAD_TIMEOUT=4096']
    if negative=='read-corruption':command.append('-DWASMETAL_TEST_CORRUPT_SDRAM')
    command+=[*map(str,source),str(harness)]
    with (directory/'build.log').open('w') as log:
        run=subprocess.run(command,cwd=ROOT,env=dict(os.environ,
            VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),stdout=log,stderr=subprocess.STDOUT)
    if run.returncode:raise RuntimeError((directory/'build.log').read_text()[-10000:])
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise ValueError('SDRAM system build input changed')
    binary=directory/'obj/Vwasmetal_loadable'
    identity={'backend':label+'-rtl','inputs':hashes,'profile':profile,'profile_tag':tag.hex(),
        'uart_ticks':4,'clock_scale':1,'upload_timeout':4096,'binary_sha256':digest(binary),
        'backing_memory':{'implementation':'SDR controller with independent behavioral pin model',
            'device_parameters':device,'nonzero_power_on_contents':True,'reset_clears_array':False,
            'negative_control':negative,'physical_device':False},'command':command}
    Path(str(binary)+'.build.json').write_text(json.dumps(identity,indent=2)+'\n')
    return binary,directory,device


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--timing',choices=('25mhz','100mhz'),required=True)
    parser.add_argument('--startup-cycles',type=int)
    parser.add_argument('--negative-control',choices=('read-corruption','startup-bypass'))
    args=parser.parse_args();started=time.monotonic();check_plan()
    # Remove old success before rebuilding, including if compilation fails.
    startup=args.startup_cycles or PROFILES[args.timing+'-full']['POWERUP_CYCLES']
    label=f'sdram-system-{args.timing}-{startup}'+('-'+args.negative_control if args.negative_control else '')
    report=ROOT/'reports'/(label+'.json');observations=ROOT/'reports'/(label+'-observations.json')
    report.parent.mkdir(exist_ok=True)
    for path in (report,observations):path.unlink(missing_ok=True)
    binary,directory,device=build(args.timing,args.startup_cycles,args.negative_control)
    coverage=directory/'coverage.jsonl';coverage.unlink(missing_ok=True)
    if args.negative_control=='startup-bypass':
        # HDL fatal diagnostics are not UART-driver JSON. Capture this deliberate
        # assertion failure directly instead of letting the JSON parser hide it.
        wat=directory/'startup.wat'
        wat.write_text('(module (func (export "main") (result i32) i32.const 42))\n')
        image=directory/'startup-image';prepare(wat,image);verify_image(image)
        packet=directory/'startup.wmu';packet.write_bytes(encode(image,0x574d000000000000).bytes())
        command=[str(binary),'--upload',str(packet)]
        run=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=600)
        log=directory/'startup-rejection.log';log.write_text(run.stdout+run.stderr)
        marker='memory request issued before SDRAM startup finished'
        if run.returncode==0 or marker not in log.read_text():
            raise ValueError('startup bypass did not trigger the independent readiness assertion')
        identity=verify_simulator(binary)
        report.write_text(json.dumps({'status':'passed','scope':'complete CPU startup wait negative control; RTL only',
            'negative_control_rejected':'startup-bypass','device_parameters':device,
            'expected_diagnostic':marker,'diagnostic_sha256':digest(log),'exit_code':run.returncode,
            'command':command,'packet_sha256':digest(packet),'model':identity,
            'inputs':{'tools/check_sdram_system.py':digest(Path(__file__).resolve())},
            'elapsed_seconds':time.monotonic()-started,'physical_hardware_tested':False},indent=2)+'\n')
        print('PASS SDRAM startup bypass rejected by independent readiness assertion')
        return
    command=[sys.executable,str(ROOT/'tools/check_loadable.py'),'--binary',str(binary),'--report',str(observations)]
    if args.negative_control:
        command+=['--case','answer' if args.negative_control=='startup-bypass' else 'selftest','--no-recovery']
    with (directory/'execution.log').open('w') as log:
        run=subprocess.run(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=3600)
    result=json.loads(observations.read_text());count=0
    if args.negative_control:
        marker=('memory request issued before SDRAM startup finished' if args.negative_control=='startup-bypass'
            else 'AssertionError: UART result differs from independent expectation:')
        if run.returncode==0 or result['status']!='failed' or marker not in (directory/'execution.log').read_text():
            raise ValueError('SDRAM negative control did not fail its independent check')
    else:
        run.check_returncode();expected={name for group in GROUPS for name in group}|set(RECOVERY)
        actual=[case['name'] for case in result['cases']]
        if result['status']!='passed' or len(actual)!=len(expected) or set(actual)!=expected:
            raise ValueError('incomplete SDRAM system execution coverage')
        count=len(actual)
    identity=verify_simulator(binary)
    if identity!=result['model']:raise ValueError('changed SDRAM system simulator')
    samples=[json.loads(line) for line in coverage.read_text().splitlines()] if coverage.exists() else []
    totals={key:sum(sample[key] for sample in samples) for key in
        ('reads','writes','refreshes','read_beats','write_beats','warm_resets','refreshes_during_reset','startup_stalls')} if samples else None
    if not args.negative_control:
        if not samples or any(totals[key]==0 for key in totals if key!='startup_stalls'):
            raise ValueError('incomplete SDRAM device coverage')
        if args.startup_cycles and totals['startup_stalls']==0:raise ValueError('startup delay was not exercised')
        if any(sample['maximum_refresh_gap']>device['REFRESH_CYCLES'] for sample in samples):
            raise ValueError('SDRAM refresh deadline exceeded')
    receipt={'status':'passed','scope':'complete CPU and memory bridge through SDRAM pins; behavioral device, RTL only',
        'device_parameters':device,'case_count':count,'negative_control_rejected':args.negative_control,
        'device_coverage':totals,'device_runs':len(samples),'coverage_sha256':digest(coverage) if coverage.exists() else None,
        'coverage_interrupted_by_expected_rejection':bool(args.negative_control and not samples),
        'observations':result,'observation_report_sha256':digest(observations),'model':identity,
        'inputs':{'tools/check_sdram_system.py':digest(Path(__file__).resolve()),
            'tools/loadable_ci.py':digest(ROOT/'tools/loadable_ci.py')},
        'elapsed_seconds':time.monotonic()-started,'physical_hardware_tested':False,'physical_memory_controller_tested':False}
    report.write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS SDRAM system '+label+': '+(args.negative_control+' rejection' if args.negative_control else f'{count} integration cases'))


if __name__=='__main__':main()
