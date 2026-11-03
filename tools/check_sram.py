#!/usr/bin/env python3
"""Check a technology-neutral SRAM adapter against an independent macro model."""
import argparse
import json
import os
from pathlib import Path
import subprocess
from build_board import yosys
from build_standalone_gate_sim import build
from prepare_standalone import ROOT,digest


CONFIGURATIONS=((131072,1),(131072,2),(131072,3),(80,8),(16,1))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--mapped',action='store_true');args=parser.parse_args()
    source=ROOT/'soc/asic/wasmetal_sram_memory.sv';harness=ROOT/'tests/memory/sram.cpp';top='wasmetal_sram_memory'
    inputs=[source,harness,Path(__file__).resolve(),ROOT/'tools/upstream.lock.json']
    hashes={str(path.relative_to(ROOT)):digest(path) for path in inputs};results=[]
    for size,latency in CONFIGURATIONS:
        directory=ROOT/f'build/sram-{size}-{latency}';directory.mkdir(parents=True,exist_ok=True)
        native=directory/'native';native.mkdir(exist_ok=True)
        flags=f' -DTEST_BYTES={size} -DTEST_LATENCY={latency}'
        command=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL','--assert',
            '-DWASMETAL_ASSERTIONS',f'-GRAM_BYTES={size}',f'-GREAD_LATENCY={latency}',
            '--top-module',top,'--cc','--exe','--build','-j','2','--Mdir',str(native),
            '-CFLAGS','-std=c++17 -O2 -Wall -Wextra -Werror '+flags,str(source),str(harness)]
        with (directory/'native.log').open('w') as log:
            result=subprocess.run(command,cwd=ROOT,env=dict(os.environ,
                VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),stdout=log,stderr=subprocess.STDOUT)
        if result.returncode:print((directory/'native.log').read_text()[-9000:]);result.check_returncode()
        binaries={'rtl':native/('V'+top)}
        if args.mapped:
            netlist=directory/'adapter.json'
            yosys(f'read_verilog -sv {source}\nchparam -set RAM_BYTES {size} -set READ_LATENCY {latency} {top}\n'
                f'synth_ecp5 -top {top} -json {netlist}\ncheck -assert\n','synthesis',directory)
            netlist.with_suffix('.manifest.json').write_text(json.dumps({'inputs':hashes,'netlist_sha256':digest(netlist)},indent=2)+'\n')
            binaries['mapped']=build(netlist,directory/'mapped',top=top,harness=harness,cflags=flags)
        tests={};mapped_identity=None
        for backend,binary in binaries.items():
            run=subprocess.run([str(binary)],cwd=ROOT,capture_output=True,text=True,timeout=180)
            if run.returncode:raise RuntimeError(run.stdout+run.stderr)
            rejected=[]
            for control in ('--corrupt-read','--ignore-masks'):
                negative=subprocess.run([str(binary),control],cwd=ROOT,capture_output=True,text=True,timeout=30)
                if negative.returncode==0 or 'SRAM read differs from independent byte oracle' not in negative.stderr:
                    raise ValueError('SRAM oracle did not reject '+control)
                rejected.append(control)
            tests[backend]={'results':json.loads(run.stdout),'binary_sha256':digest(binary),'negative_controls_rejected':rejected}
            if backend=='mapped':mapped_identity=json.loads(Path(str(binary)+'.build.json').read_text())
        if args.mapped and tests['rtl']['results']!=tests['mapped']['results']:
            raise ValueError('SRAM adapter RTL and mapped observations differ')
        results.append({'ram_bytes':size,'read_latency':latency,'tests':tests,'mapped_build':mapped_identity})
        print(f'PASS SRAM adapter {size} bytes, latency {latency}: '+str(tests['rtl']['results']['transactions'])+' transactions',flush=True)
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise ValueError('SRAM verification inputs changed')
    report={'status':'passed','scope':'adapter RTL and functional ECP5 mapping; independent behavioral SRAM, no foundry macro',
        'configurations':results,'all_65536_write_masks_checked_per_configuration':True,'inputs':hashes,
        'physical_hardware_tested':False,'connected_to_cpu':False}
    (ROOT/'reports').mkdir(exist_ok=True)
    (ROOT/'reports'/('sram-mapped.json' if args.mapped else 'sram-rtl.json')).write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
