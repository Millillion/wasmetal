#!/usr/bin/env python3
"""Measure deterministic workloads through standalone UART with independent answers."""
import json
from pathlib import Path
import subprocess
import time
import zlib
from check_standalone import decode,check_expected,reference_check
from prepare_standalone import ROOT,prepare,digest,load_profile
from standalone_support import verify_image,verify_simulator


def main():
    binary=ROOT/'build/standalone-sim/Vwasmetal_standalone';identity=verify_simulator(binary)
    if identity['backend']!='standalone-rtl':raise ValueError('standalone RTL benchmark required')
    vectors=sum((n-32)*(n*3%11-5) for n in range(64));selected=[]
    for length in (0,256,1024):
        selected.append(('crc32',length,[zlib.crc32(bytes(n%256 for n in range(length)))],length))
    for kernel in ('dot-scalar','dot-simd'):
        for passes in (1,16):selected.append((kernel,passes,[vectors*passes&0xffffffff],64*passes))
    inputs=[Path(__file__).resolve(),ROOT/'tools/check_standalone.py',ROOT/'tools/prepare_standalone.py',
        ROOT/'tools/standalone_support.py',*sorted((ROOT/'examples/benchmarks').glob('*.wat'))]
    hashes={str(path.relative_to(ROOT)):digest(path) for path in inputs};started=time.monotonic();results=[]
    report=ROOT/'reports/benchmarks.json'
    def save(status):
        report.write_text(json.dumps({'status':status,'backend':identity,'inputs':hashes,'profile':load_profile(),
            'cases':results,'elapsed_seconds':time.monotonic()-started,'physical_hardware_tested':False,
            'timing_scope':'core invocation cycles; excludes image preparation, upload, memory clear, initialization and UART result transfer'},indent=2)+'\n')
    save('running')
    try:
        for kernel,argument,expected,units in selected:
            source=ROOT/f'examples/benchmarks/{kernel}.wat';name=f'{kernel}-{argument}'
            cwd=ROOT/'build/benchmarks'/name;image=cwd/'build/standalone-image'
            manifest=prepare(source,image,arguments=[argument]);verify_image(image)
            reference_check(image,{'args':[argument],'expected':expected})
            process=subprocess.run([str(binary),'--reboots','2'],cwd=cwd,capture_output=True,text=True,check=True,timeout=300)
            runs=[json.loads(line) for line in process.stdout.splitlines()]
            if len(runs)!=2:raise ValueError('benchmark did not restart')
            frames=[decode(run['uart']) for run in runs]
            for frame in frames:check_expected(frame,expected)
            if frames[0]!=frames[1]:raise ValueError('benchmark changed after restart')
            cycles=frames[0]['cycles']
            results.append({'name':name,'argument':argument,'expected':expected,'cycles':cycles,'work_units':units,
                'unit':'byte' if kernel=='crc32' else 'integer multiply-accumulate',
                'cycles_per_unit':cycles/units if units else None,'runs':runs,
                'image_counts':manifest['counts'],'allocated_ram_bytes':manifest['allocated_ram_bytes'],
                'image_manifest_sha256':digest(image/'manifest.json'),'image_files':manifest['files']})
            save('running');print(f'{name}: {cycles} cycles, {units} work units',flush=True)
        scalar=next(row['cycles'] for row in results if row['name']=='dot-scalar-16')
        simd=next(row['cycles'] for row in results if row['name']=='dot-simd-16')
        if scalar<=0 or simd<=0:raise ValueError('invalid benchmark cycle count')
        verify_simulator(binary)
        if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise ValueError('benchmark input changed')
        save('passed');print(f'Scalar / SIMD invocation cycles: {scalar/simd:.3f}')
    except BaseException:
        save('failed');raise


if __name__=='__main__':main()
