#!/usr/bin/env python3
"""Build the RTL reference with the exact parameters of the 7-series estimate."""
import argparse
import json
import os
from pathlib import Path
import subprocess

from build_gate_sim import compilation
from prepare_standalone import ROOT, digest, load_profile
from program_upload import profile_tag


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=2)
    args=parser.parse_args()
    if args.jobs<1:parser.error('--jobs must be positive')
    estimate=ROOT/'reports/xc7-system-estimate.json'
    reference=json.loads(estimate.read_text())
    if reference['status']!='synthesized_and_structurally_checked' or reference['top']!='wasmetal_loadable':
        raise ValueError('need the complete checked 7-series system estimate')
    if reference['profile']!=load_profile():raise ValueError('estimate profile changed')
    for name,value in reference['inputs'].items():
        if digest(ROOT/name)!=value:raise ValueError('stale estimate input: '+name)
    top=reference['top'];params=reference['parameters'];profile=reference['profile']
    source=[ROOT/'rtl/vendor.vlt']+[ROOT/name for name in reference['inputs']
        if name.startswith(('rtl/','soc/','fpga/','third_party/hardfloat/source/'))
        and Path(name).suffix in ('.sv','.v')]
    if len(source)<10:raise ValueError('incomplete RTL source inventory')
    harness=ROOT/'tests/standalone/loadable.cpp'
    directory=ROOT/'build/xc7-native-sim';obj=directory/'obj';directory.mkdir(parents=True,exist_ok=True)
    binary=obj/('V'+top);receipt=Path(str(binary)+'.build.json');receipt.unlink(missing_ok=True)
    extra=[Path(__file__).resolve(),estimate,harness,ROOT/'rtl/vendor.vlt',ROOT/'tools/build_gate_sim.py',
        ROOT/'tools/prepare_standalone.py',ROOT/'tools/program_upload.py',
        ROOT/'.cache/tools/usr/bin/verilator',ROOT/'.cache/tools/usr/bin/verilator_bin']
    inputs={**reference['inputs'],**{str(p.relative_to(ROOT)):digest(p) for p in extra}}
    options=compilation(True,True)
    flags=options['cflags']+f" -DBIT_TICKS={params['UART_TICKS']} -DCLOCK_SCALE=1 -DUPLOAD_TIMEOUT={params['UPLOAD_TIMEOUT_CYCLES']}"
    vendor=ROOT/'third_party/hardfloat/source'
    command=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL',
        '--unroll-count','512','--assert','-DWASMETAL_ASSERTIONS','--top-module',top,
        '-I'+str(vendor),'-I'+str(vendor/'RISCV'),
        '--cc','--exe','--output-split','10000','--output-split-cfuncs','10000',
        '--Mdir',str(obj),'-CFLAGS',flags,*[f'-G{k}={v}' for k,v in params.items()],
        *map(str,source),str(harness)]
    make=['make','-C',str(obj),'-f','V'+top+'.mk','-j',str(args.jobs),
        'CXX='+options['compiler'],'LINK='+options['compiler'],'VM_USER_CFLAGS='+flags,
        'OPT_FAST=-O3','OPT_SLOW=-O3','OPT_GLOBAL=-O3']
    env=dict(os.environ,VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator'))
    with (directory/'build.log').open('w') as log:
        subprocess.run(command,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
        # Verilator intentionally uses bitwise operations on Boolean expressions.
        # Keep style exceptions confined to generated C++, with handwritten code strict.
        for path in obj.glob('V*.cpp'):
            body=path.read_text()
            path.write_text(''.join(f'#pragma GCC diagnostic ignored "-{rule}"\n' for rule in
                ['Wbool-operation','Wbitwise-instead-of-logical','Wint-in-bool-context','Wparentheses-equality'])+body)
        subprocess.run(make,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
    for name,value in inputs.items():
        if digest(ROOT/name)!=value:raise ValueError('RTL simulator input changed: '+name)
    if digest(Path(options['compiler']))!=options['compiler_sha256']:raise ValueError('compiler changed')
    receipt.write_text(json.dumps({'backend':'loadable-xc7-rtl','top':top,'inputs':inputs,
        'profile':profile,'profile_tag':profile_tag(profile).hex(),'parameters':params,
        'uart_ticks':params['UART_TICKS'],'clock_scale':1,'upload_timeout':params['UPLOAD_TIMEOUT_CYCLES'],
        'binary_sha256':digest(binary),'compilation':options,'commands':[command,make],
        'build_log_sha256':digest(directory/'build.log'),'physical_hardware_tested':False},indent=2)+'\n')
    print(binary)


if __name__=='__main__':main()
