#!/usr/bin/env python3
"""Check independent UART rates and phases with the actual board divider."""
import json
from pathlib import Path
import subprocess
import time
from check_loadable import parse_frames
from check_standalone import check_expected
from prepare_standalone import ROOT,prepare,digest
from program_upload import encode
from standalone_support import verify_simulator


def main():
    binary=ROOT/'build/loadable-board-sim/Vwasmetal_loadable_ulx3s';identity=verify_simulator(binary)
    if identity['backend']!='loadable-board-rtl' or identity['clock_scale']!=32 or identity['uart_ticks']!=81:
        raise ValueError('production board divider and UART parameters required')
    directory=ROOT/'build/loadable-board-rates';directory.mkdir(parents=True,exist_ok=True)
    source=ROOT/'examples/standalone/answer.wat';prepare(source,directory/'image')
    packet=directory/'answer.wmu';packet.write_bytes(encode(directory/'image',0x574d524154455301).bytes())
    paths=[Path(__file__).resolve(),source,ROOT/'tools/check_loadable.py',ROOT/'tools/check_standalone.py',
        ROOT/'tools/prepare_standalone.py',ROOT/'tools/program_upload.py',ROOT/'tools/standalone_support.py',packet]
    inputs={str(path.relative_to(ROOT)):digest(path) for path in paths};results=[];started=time.monotonic()
    report=ROOT/'reports/loadable-board-rates.json'
    def save(status):
        report.write_text(json.dumps({'status':status,'model':identity,'inputs':inputs,'cases':results,
            'elapsed_seconds':time.monotonic()-started,'physical_hardware_tested':False},indent=2)+'\n')
    save('running')
    try:
        for period in (980,1005,1020):
            run=subprocess.run([str(binary),'--period-permille',str(period),'--upload',str(packet)],
                cwd=ROOT,capture_output=True,text=True,check=True,timeout=1800)
            observations=[json.loads(line) for line in run.stdout.splitlines()]
            if len(observations)!=1:raise ValueError('missing board-rate completion')
            replies,frames=parse_frames(observations[0]['uart'])
            if [reply['status'] for reply in replies]!=['ready','committed'] or len(frames)!=1:
                raise ValueError('bad board-rate protocol response')
            check_expected(frames[0],[42])
            results.append({'period_permille':period,'uart':observations[0],'result':frames[0]})
            save('running');print(f'PASS board upload at {period}/1000 bit period',flush=True)
        verify_simulator(binary)
        if any(digest(ROOT/name)!=value for name,value in inputs.items()):raise ValueError('board rate inputs changed')
        save('passed')
    except BaseException:
        save('failed');raise


if __name__=='__main__':main()
