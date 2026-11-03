#!/usr/bin/env python3
"""Compare observable UART and clock behavior of RTL and the mapped board."""
import json
from pathlib import Path
import subprocess
import time

from check_standalone import decode, check_expected, reset_schedule, SELFTEST_VALUES
from prepare_standalone import ROOT, digest
from standalone_support import verify_image, verify_simulator


def main():
    binaries={'rtl':ROOT/'build/standalone-board-sim/Vwasmetal_standalone_ulx3s',
              'mapped':ROOT/'build/standalone-gate-sim/obj/Vwasmetal_standalone_ulx3s'}
    identities={name:verify_simulator(binary) for name,binary in binaries.items()}
    image=verify_image(ROOT/'build/standalone-image')
    if image['source_sha256']!=digest(ROOT/'examples/standalone/selftest.wat') or image['arguments'] or image['export']!='main':
        raise ValueError('mapped comparison requires the committed standalone selftest image')
    mapped=json.loads((ROOT/'build/standalone-ulx3s/design.manifest.json').read_text())
    if mapped['image']!=image: raise ValueError('mapped circuit contains a different image')
    scenarios=[('power-on-and-restart',['--power-on','--reboots','2']),
               ('external-reset',[]),
               ('reset-during-execution',None),('reset-during-uart',None)]
    report={'status':'running','scope':'fixed selftest image on the full standalone board circuit',
            'netlist_sha256':identities['mapped']['netlist_sha256'],'image':image,
            'builds':identities,'cases':[],'physical_hardware_tested':False}
    path=ROOT/'reports/standalone-mapped.json'; started=time.monotonic()
    inputs={str(p.relative_to(ROOT)):digest(p) for p in [Path(__file__).resolve(),ROOT/'tools/check_standalone.py']}
    report['test_inputs']=inputs
    def save():
        report['elapsed_seconds']=time.monotonic()-started
        path.write_text(json.dumps(report,indent=2)+'\n')
    save()
    try:
        for name,flags in scenarios:
            if flags is None:
                reference=report['cases'][0]['frames'][0]
                flags=['--power-on','--reset-at',str(reset_schedule(reference,name.removeprefix('reset-during-'),True))]
            observed={}
            for backend,binary in binaries.items():
                result=subprocess.run([str(binary),*flags],cwd=ROOT,capture_output=True,text=True,timeout=900)
                if result.returncode: raise RuntimeError(result.stdout+result.stderr)
                frames=[json.loads(line) for line in result.stdout.splitlines()]
                if len(frames)!=(2 if '--reboots' in flags else 1): raise AssertionError('missing serial frame')
                for entry in frames:
                    check_expected(decode(entry['uart']),SELFTEST_VALUES)
                    if entry['reset_injected']!=('--reset-at' in flags): raise AssertionError('reset coverage mismatch')
                observed[backend]=frames
            if observed['rtl']!=observed['mapped']:
                raise AssertionError('mapped UART bytes or completion clocks differ from RTL')
            report['cases'].append({'name':name,'rtl_and_mapped_identical':True,'frames':observed['mapped']})
            save(); print(name+': identical RTL and mapped results/clocks',flush=True)
        for binary in binaries.values(): verify_simulator(binary)
        for name,value in inputs.items():
            if digest(ROOT/name)!=value: raise ValueError('mapped checker changed during execution')
        report['status']='passed';save()
    except Exception as e:
        report['status']='failed';report['failure']=str(e);save();raise
    print(path)


if __name__=='__main__': main()
