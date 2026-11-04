#!/usr/bin/env python3
"""Exercise SDRAM pins, refresh deadlines and warm resets in RTL and ECP5 models."""
import argparse
import json
import os
from pathlib import Path
import subprocess

from build_board import yosys
from build_sdram_gate_sim import build
from prepare_standalone import ROOT,digest


PROFILES={
    '25mhz-full':dict(RAM_BYTES=33554432,ROW_BITS=13,COLUMN_BITS=9,POWERUP_CYCLES=5000,
        REFRESH_CYCLES=195,CAS_LATENCY=2,T_RCD=1,T_RP=1,T_RFC=2,T_RAS=2,T_WR=2,T_RC=2,T_MRD=2),
    '25mhz-prefix':dict(RAM_BYTES=131072,ROW_BITS=13,COLUMN_BITS=9,POWERUP_CYCLES=5000,
        REFRESH_CYCLES=195,CAS_LATENCY=2,T_RCD=1,T_RP=1,T_RFC=2,T_RAS=2,T_WR=2,T_RC=2,T_MRD=2),
    '100mhz-full':dict(RAM_BYTES=33554432,ROW_BITS=13,COLUMN_BITS=9,POWERUP_CYCLES=20000,
        REFRESH_CYCLES=781,CAS_LATENCY=3,T_RCD=2,T_RP=2,T_RFC=6,T_RAS=5,T_WR=2,T_RC=6,T_MRD=2),
    'synthetic':dict(RAM_BYTES=512,ROW_BITS=3,COLUMN_BITS=3,POWERUP_CYCLES=16,
        REFRESH_CYCLES=127,CAS_LATENCY=3,T_RCD=2,T_RP=2,T_RFC=7,T_RAS=8,T_WR=3,T_RC=10,T_MRD=3),
    'synthetic-long-row':dict(RAM_BYTES=512,ROW_BITS=3,COLUMN_BITS=3,POWERUP_CYCLES=16,
        REFRESH_CYCLES=257,CAS_LATENCY=3,T_RCD=2,T_RP=2,T_RFC=7,T_RAS=32,T_WR=3,T_RC=36,T_MRD=3),
    'synthetic-minimum':dict(RAM_BYTES=128,ROW_BITS=1,COLUMN_BITS=3,POWERUP_CYCLES=2,
        REFRESH_CYCLES=63,CAS_LATENCY=2,T_RCD=1,T_RP=1,T_RFC=1,T_RAS=1,T_WR=2,T_RC=1,T_MRD=2),
}
MACROS={'RAM_BYTES':'BYTES','ROW_BITS':'ROWS','COLUMN_BITS':'COLUMNS','POWERUP_CYCLES':'POWERUP',
    'REFRESH_CYCLES':'REFRESH','CAS_LATENCY':'CAS','T_RCD':'RCD','T_RP':'RP','T_RFC':'RFC',
    'T_RAS':'RAS','T_WR':'WR','T_RC':'RC','T_MRD':'MRD'}
NEGATIVES={
    '--corrupt-read':'SDRAM read differs from independent byte oracle',
    '--ignore-masks':'SDRAM bytes differ from independent byte oracle',
    '--omit-refresh':'refresh deadline missed',
    '--early-command':'command before timing recovery',
    '--wrong-read-latency':'SDRAM read differs from independent byte oracle',
    '--mask-read-data':'SDRAM read differs from independent byte oracle',
}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mapped',action='store_true')
    parser.add_argument('--profile',action='append',choices=PROFILES)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    output=args.report or ROOT/'reports'/('sdram-mapped.json' if args.mapped else 'sdram-rtl.json')
    output.unlink(missing_ok=True)
    source=ROOT/'soc/sdram/wasmetal_sdram_memory.sv';harness=ROOT/'tests/memory/sdram.cpp'
    top='wasmetal_sdram_memory'
    paths=[source,harness,ROOT/'tests/memory/sdram_device.hpp',Path(__file__).resolve(),ROOT/'tools/prepare_standalone.py',
        ROOT/'tools/build_board.py',ROOT/'tools/build_standalone_gate_sim.py',
        ROOT/'tools/build_sdram_gate_sim.py',ROOT/'tools/upstream.lock.json']
    hashes={str(p.relative_to(ROOT)):digest(p) for p in paths}
    results=[]
    for name in args.profile or PROFILES:
        profile=PROFILES[name];directory=ROOT/'build'/('sdram-'+name);directory.mkdir(parents=True,exist_ok=True)
        native=directory/'native';native.mkdir(exist_ok=True)
        flags=' '.join(f'-DTEST_{MACROS[key]}={value}' for key,value in profile.items())
        command=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL','--assert',
            '-DWASMETAL_ASSERTIONS',*[f'-G{key}={value}' for key,value in profile.items()],
            '--top-module',top,'--cc','--exe','--build','-j','2','--Mdir',str(native),
            '-CFLAGS','-std=c++17 -O2 -Wall -Wextra -Werror '+flags,str(source),str(harness)]
        with (directory/'native-build.log').open('w') as log:
            subprocess.run(command,cwd=ROOT,env=dict(os.environ,
                VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')),
                stdout=log,stderr=subprocess.STDOUT,check=True)
        binaries={'rtl':native/('V'+top)}
        mapped_identity=None
        if args.mapped:
            netlist=directory/'controller.json'
            parameters=' '.join(f'-set {key} {value}' for key,value in profile.items())
            yosys(f'read_verilog -sv {source}\nchparam {parameters} {top}\n'
                f'synth_ecp5 -top {top} -json {netlist}\ncheck -assert\n','synthesis',directory)
            netlist.with_suffix('.manifest.json').write_text(json.dumps(
                {'inputs':hashes,'netlist_sha256':digest(netlist)},indent=2)+'\n')
            binaries['mapped']=build(netlist,directory/'mapped',harness=harness,cflags=flags)
        observations={}
        for backend,binary in binaries.items():
            positive=subprocess.run([str(binary)],cwd=ROOT,capture_output=True,text=True,timeout=600)
            (directory/(backend+'-test.log')).write_text(positive.stdout+positive.stderr)
            if positive.returncode:raise RuntimeError(positive.stdout+positive.stderr)
            observed=json.loads(positive.stdout)
            if observed['warm_resets']!=129 or observed['invalid_requests']!=20:
                raise ValueError('SDRAM coverage is incomplete')
            rejected=[]
            for mutation,message in NEGATIVES.items():
                negative=subprocess.run([str(binary),mutation],cwd=ROOT,capture_output=True,text=True,timeout=90)
                (directory/(backend+mutation+'.log')).write_text(negative.stdout+negative.stderr)
                if negative.returncode==0 or message not in negative.stderr:
                    raise ValueError('SDRAM checker did not reject '+mutation+': '+negative.stdout+negative.stderr)
                rejected.append(mutation)
            observations[backend]={'results':observed,'binary_sha256':digest(binary),
                'negative_controls_rejected':rejected}
            if backend=='mapped':mapped_identity=json.loads(Path(str(binary)+'.build.json').read_text())
        if args.mapped:
            if observations['rtl']['results']['stimulus_hash']!=observations['mapped']['results']['stimulus_hash']:
                raise ValueError('SDRAM request stimuli differ between compilers')
            if observations['rtl']['results']!=observations['mapped']['results']:
                raise ValueError('SDRAM model observations differ')
        results.append({'name':name,'parameters':profile,'native_command':command,
            'tests':observations,'mapped_build':mapped_identity})
        print(f'PASS SDRAM {name}: '+str(observations['rtl']['results']['transactions'])+' requests',flush=True)
    for name,value in hashes.items():
        if digest(ROOT/name)!=value:raise ValueError('SDRAM verification input changed: '+name)
    report={'status':'passed','scope':'controller with independent pin-level SDR model and byte oracle; no board PHY or physical timing validation',
        'profiles':results,'all_65536_write_masks_checked_per_profile':True,
        'warm_resets_per_model_per_profile':129,'inputs':hashes,
        'connected_to_cpu':False,'physical_hardware_tested':False}
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
