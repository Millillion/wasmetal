#!/usr/bin/env python3
"""Run the complete programmable CPU with an asynchronous AXI path and behavioral RAM."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from build_standalone_sim import sources
from loadable_ci import GROUPS,RECOVERY,check_plan
from prepare_standalone import ROOT,digest,load_profile
from program_upload import profile_tag
from standalone_support import generate_parameters,parameters,verify_simulator


def build(divider,latency,corrupt=False):
    profile=load_profile();generated=generate_parameters();tag=profile_tag(profile)
    top='wasmetal_loadable';label=f'axi-system-{divider}-{latency}'+('-corrupt' if corrupt else '')
    directory=ROOT/'build'/label;directory.mkdir(parents=True,exist_ok=True)
    original=ROOT/'soc/memory/wasmetal_bram.sv';binding=ROOT/'tests/external/wasmetal_bram.sv'
    source=sources()
    if source.count(original)!=1:raise ValueError('expected exactly one FPGA backing-memory implementation')
    source=[binding if path==original else path for path in source]
    vendor=ROOT/'third_party/hardfloat/source';harness=ROOT/'tests/external/loadable.cpp'
    # The common module reset is deliberately synchronous for the local-memory
    # descriptors and asynchronous for the CDC's reset-release synchronizers.
    config=directory/'reset.vlt'
    config.write_text('`verilator_config\n'+
        f'lint_off -rule SYNCASYNCNET -file "{ROOT}/soc/wasmetal_local_memory.sv" '+
        '-match "*wasmetal_loadable.execution.__Vcellinp__memory__reset*"\n')
    source=[config,*source]
    paths=[*source,*sorted(vendor.rglob('*.vi')),harness,Path(__file__).resolve(),generated,
        ROOT/'tools/build_standalone_sim.py',ROOT/'tools/prepare_standalone.py',ROOT/'tools/standalone_support.py',
        ROOT/'tools/program_upload.py',ROOT/'tools/loadable_ci.py',ROOT/'soc/profile.json',ROOT/'tools/upstream.lock.json',
        ROOT/'tests/standalone/loadable.cpp']
    hashes={str(path.relative_to(ROOT)):digest(path) for path in paths}
    params={**parameters(profile),'UART_TICKS':4,'UPLOAD_TIMEOUT_CYCLES':4096,
        'PROFILE_TAG':f"128'h{int.from_bytes(tag,'little'):032x}"}
    command=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL',
        '--unroll-count','512','--assert','-DWASMETAL_ASSERTIONS',f'-DWASMETAL_TEST_AXI_DIVIDER={divider}',f'-DWASMETAL_TEST_AXI_LATENCY={latency}',
        '-DWASMETAL_TEST_AXI_COVERAGE="'+str(directory/'coverage.jsonl')+'"',
        '--top-module',top,'-I'+str(vendor),'-I'+str(vendor/'RISCV'),'-I'+str(ROOT/'build'),
        *[f'-G{name}={value}' for name,value in params.items()],
        '--cc','--exe','--build','-j','1','--Mdir',str(directory),
        '-CFLAGS','-std=c++17 -O3 -Wall -Wextra -Werror -DBIT_TICKS=4 -DCLOCK_SCALE=1 -DUPLOAD_TIMEOUT=4096']
    if corrupt:command.append('-DWASMETAL_TEST_CORRUPT_AXI')
    command+=[*map(str,source),str(harness)]
    with (directory/'build.log').open('w') as log:
        result=subprocess.run(command,cwd=ROOT,env=dict(os.environ,
            VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),stdout=log,stderr=subprocess.STDOUT)
    if result.returncode:print((directory/'build.log').read_text()[-10000:]);result.check_returncode()
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise ValueError('AXI system build input changed')
    binary=directory/('V'+top)
    identity={'backend':label+'-rtl','inputs':hashes,'profile':profile,'profile_tag':tag.hex(),
        'uart_ticks':4,'clock_scale':1,'upload_timeout':4096,'binary_sha256':digest(binary),
        'backing_memory':{'implementation':'production asynchronous AXI adapter with behavioral RAM slave',
            'read_delay_axi_cycles':latency,'axi_half_period_cpu_cycles':divider,'nonzero_power_on_contents':True,'reset_clears_array':False,
            'deliberately_corrupt_read_data':corrupt,'physical_memory_controller':False},'command':command}
    Path(str(binary)+'.build.json').write_text(json.dumps(identity,indent=2)+'\n')
    return binary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--latency',type=int,choices=(1,5),required=True)
    parser.add_argument('--divider',type=int,choices=(1,3),required=True)
    parser.add_argument('--negative-control',action='store_true')
    args=parser.parse_args();started=time.monotonic();check_plan()
    label=f'axi-system-{args.divider}-{args.latency}'+('-negative' if args.negative_control else '')
    report=ROOT/'reports'/(label+'.json');report.parent.mkdir(exist_ok=True)
    observations=ROOT/'reports'/(label+'-observations.json')
    for path in (report,observations):path.unlink(missing_ok=True)
    binary=build(args.divider,args.latency,args.negative_control)
    coverage=binary.parent/'coverage.jsonl';coverage.unlink(missing_ok=True)
    log_path=ROOT/'build'/label;log_path.mkdir(exist_ok=True)
    command=[sys.executable,str(ROOT/'tools/check_loadable.py'),'--binary',str(binary),'--report',str(observations)]
    if args.negative_control:command+=['--case','selftest','--no-recovery']
    with (log_path/'execution.log').open('w') as log:
        run=subprocess.run(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=1800)
    result=json.loads(observations.read_text())
    if args.negative_control:
        log=(log_path/'execution.log').read_text()
        if run.returncode==0 or result['status']!='failed' or \
                'AssertionError: UART result differs from independent expectation:' not in log:
            raise ValueError('corrupt AXI did not fail the independent execution-result oracle')
        count=0
    else:
        run.check_returncode()
        expected={name for group in GROUPS for name in group}|set(RECOVERY)
        actual=[case['name'] for case in result['cases']]
        if result['status']!='passed' or len(actual)!=len(expected) or set(actual)!=expected:
            raise ValueError('incomplete AXI-system execution coverage')
        count=len(actual)
    identity=verify_simulator(binary)
    if identity!=result['model']:raise ValueError('changed AXI system simulator')
    # The result checker terminates a rejected simulator immediately. An
    # expected wrong-value rejection can therefore precede its HDL final block.
    # Successful campaigns must still finish and supply complete bus coverage.
    samples=[json.loads(line) for line in coverage.read_text().splitlines()] if coverage.exists() else []
    totals={key:sum(sample[key] for sample in samples) for key in ('writes','reads','aw_first','w_first','resets')} if samples else None
    if not args.negative_control and (not samples or any(value==0 for value in totals.values())):
        raise ValueError('incomplete AXI bus coverage')
    receipt={'status':'passed','scope':'complete CPU and memory bridge through CDC and AXI with a behavioral slave; related test clocks, RTL only',
        'read_delay_axi_cycles':args.latency,'axi_half_period_cpu_cycles':args.divider,'case_count':count,'corrupt_read_negative_control_rejected':args.negative_control,
        'bus_coverage':totals,'bus_runs':len(samples),'coverage_sha256':digest(coverage) if coverage.exists() else None,
        'coverage_interrupted_by_expected_rejection':args.negative_control and not samples,
        'observations':result,'observation_report_sha256':digest(observations),'model':identity,
        'inputs':{'tools/check_axi_system.py':digest(Path(__file__).resolve()),
            'tools/loadable_ci.py':digest(ROOT/'tools/loadable_ci.py')},
        'elapsed_seconds':time.monotonic()-started,'physical_hardware_tested':False,'physical_memory_controller_tested':False}
    report.write_text(json.dumps(receipt,indent=2)+'\n')
    print(f'PASS AXI system divider {args.divider}, delay {args.latency}: '+('corrupt-read rejection' if args.negative_control else f'{count} integration cases'))


if __name__=='__main__':main()
