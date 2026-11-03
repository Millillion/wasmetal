#!/usr/bin/env python3
"""Upload independent Wasm cases over UART and verify execution and recovery."""
import argparse
import json
import os
from pathlib import Path
import selectors
import subprocess
import tempfile
import time
from check_standalone import cases,decode,check_expected,reference_check
from prepare_standalone import ROOT,prepare,digest,load_profile
from program_upload import encode,decode_reply
from standalone_support import verify_simulator,verify_image


def extra_cases():
    yield {'name':'program-address-boundaries','expected':[119],
        'wat':'(module (func $padding '+'nop '*520+') '+
        ' '.join(f'(func $f{n} (result i32) i32.const {n})' for n in range(120))+
        ' (func (export "main") (result i32) call $f119))'}
    types=' '.join(f'(type $t{n} (struct '+ '(field i32) '*n+'))' for n in range(60))
    types+='(type $base (sub (struct '+ '(field i32) '*60+')))'
    for name,expected in [('type-address-boundaries',[42]),('type-boundary-rejection',[])]:
        child='(type $child '+('(sub $base (struct '+'(field i32) '*61+')))' if expected else '(struct '+'(field i32) '*61+'))')
        target='$base'
        case={'name':name,'expected':expected,'wat':'(module '+types+child+
            ' (func (export "main") (result i32) '+ 'i32.const 42 '*61+
            f' struct.new $child ref.cast (ref {target}) struct.get {target} 0))'}
        if not expected:case.update(status=1,trap=10)
        yield case
    data=bytes(n%256 for n in range(3500))
    yield {'name':'boot-address-boundaries','expected':[int.from_bytes(data[-4:],'little')],
        'wat':'(module (memory 1 1) (data (i32.const 0) "'+''.join(f'\\{byte:02x}' for byte in data)+
              '") (func (export "main") (result i32) i32.const 3496 i32.load))'}
    yield {'name':'segment-address-boundaries','expected':[80],
        'wat':'(module (memory 1 1) '+ ' '.join(f'(data $d{n} "{chr(65+n)}")' for n in range(16))+
            ' (func (export "main") (result i32) i32.const 3 i32.const 0 i32.const 1 memory.init $d15 i32.const 3 i32.load8_u))'}


def parse_frames(hexadecimal):
    data=bytes.fromhex(hexadecimal);replies=[];results=[]
    while data:
        if data[:4]==b'WMLR' and len(data)>=20:
            replies.append(decode_reply(data[:20]));data=data[20:]
        elif data[:3]==b'WM\x01' and len(data)>=6:
            length=12+16*data[5];results.append(decode(data[:length].hex()));data=data[length:]
        else:raise ValueError('unexpected or truncated serial data: '+data[:20].hex())
    return replies,results


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary',type=Path,default=ROOT/'build/loadable-sim/Vwasmetal_loadable')
    parser.add_argument('--board',action='store_true');parser.add_argument('--case',action='append',default=[])
    parser.add_argument('--report',type=Path);parser.add_argument('--no-recovery',action='store_true')
    args=parser.parse_args();binary=args.binary.resolve();identity=verify_simulator(binary)
    scale=identity['clock_scale'];bit_ticks=identity['uart_ticks']*scale
    if args.board!=(scale==32):parser.error('--board must match the simulator clock configuration')
    source=Path(__file__).resolve();source_hash=digest(source);started=time.monotonic();results=[]
    inputs=[source,ROOT/'tools/check_standalone.py',ROOT/'tools/program_upload.py',ROOT/'tools/prepare_standalone.py',
        ROOT/'tools/standalone_support.py',ROOT/'tests/standalone/loadable.cpp']
    hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs}
    report=args.report or ROOT/'reports/loadable-rtl.json'
    selected=[case for case in cases() if 'reset_at' not in case and 'reset_phase' not in case and 'corrupt' not in case]
    selected+=list(extra_cases());case_numbers={case['name']:n for n,case in enumerate(selected)}
    if args.case:
        if set(args.case)-{case['name'] for case in selected}:parser.error('unknown loadable case')
        selected=[case for case in selected if case['name'] in args.case]
    elif args.board:selected=[case for case in selected if case['name'] in ('answer','selftest')]
    packets={};expectations={}
    def save(status):
        report.parent.mkdir(parents=True,exist_ok=True)
        report.write_text(json.dumps({'status':status,'scope':'complete programmable CPU using UART pins only',
            'model':identity,'clock_scale':scale,'uart_ticks':bit_ticks//scale,'cases':results,'inputs':hashes,
            'elapsed_seconds':time.monotonic()-started,'physical_hardware_tested':False},indent=2)+'\n')
    def execute(flags,on_result=None):
        # A mapped watchdog case executes over 19 million circuit clocks.
        # Bound each operation, rather than the total duration of a batch, and
        # preserve completed cases if a later operation fails or is interrupted.
        runs=[];pending=b''
        with tempfile.TemporaryFile() as errors:
            process=subprocess.Popen([str(binary),*flags],cwd=ROOT,stdout=subprocess.PIPE,stderr=errors)
            try:
                with selectors.DefaultSelector() as selector:
                    selector.register(process.stdout,selectors.EVENT_READ);deadline=time.monotonic()+3600
                    while True:
                        if not selector.select(max(0,deadline-time.monotonic())):
                            raise TimeoutError('programmable simulator operation exceeded one hour')
                        chunk=os.read(process.stdout.fileno(),65536)
                        if not chunk:break
                        pending+=chunk
                        if len(pending)>1048576:raise ValueError('oversized simulator response')
                        while b'\n' in pending:
                            line,pending=pending.split(b'\n',1)
                            run=json.loads(line);runs.append(run);deadline=time.monotonic()+3600
                            if on_result:on_result(run)
                    if pending:raise ValueError('truncated simulator response')
                    process.wait(timeout=max(0.1,deadline-time.monotonic()))
                if process.returncode:
                    errors.seek(0);raise RuntimeError(errors.read().decode(errors='replace'))
                return runs
            finally:
                if process.poll() is None:
                    process.terminate()
                    try:process.wait(timeout=10)
                    except subprocess.TimeoutExpired:process.kill();process.wait(timeout=10)
                process.stdout.close()
    save('running')
    try:
        for case in selected:
            number=case_numbers[case['name']]
            directory=ROOT/'build/loadable-cases'/identity['backend']/case['name'];directory.mkdir(parents=True,exist_ok=True)
            wat=case.get('source',directory/'program.wat')
            if 'wat' in case:wat.write_text(case['wat'])
            image=directory/'image';prepare(wat,image,arguments=case.get('args',[]));verify_image(image)
            if case.get('reference',True):reference_check(image,case)
            packet=encode(image,0x574d000000000000+number);path=directory/'program.wmu';path.write_bytes(packet.bytes())
            packets[case['name']]=path;expectations[case['name']]=case
        # All programs reuse the same running simulator and physical store.
        # The next upload must erase the previous execution's state and data.
        commands=[part for case in selected for part in ('--upload',str(packets[case['name']]))]
        def completed(run):
            if len(results)>=len(selected):raise ValueError('unexpected extra upload execution')
            case=selected[len(results)]
            acknowledgments,frames=parse_frames(run['uart'])
            if [reply['status'] for reply in acknowledgments]!=['ready','committed'] or len(frames)!=1:
                raise ValueError('missing acknowledgment or result')
            check_expected(frames[0],case['expected'],case.get('status',0),case.get('trap',0))
            result={'name':case['name'],'packet_sha256':digest(packets[case['name']]),'uart':run,'result':frames[0]}
            results.append(result);save('running');print('PASS uploaded '+case['name'],flush=True)
        runs=execute(commands,completed)
        if len(runs)!=len(selected):raise ValueError('missing upload executions')
        if not args.no_recovery and 'answer' in packets:
            path=str(packets['answer'])
            recovery=execute(['--bad-profile',path,'--bad-crc',path,'--partial',path,'35',
                '--timeout',path,'37','--break',path,'36','--upload',path])
            if len(recovery)!=6:raise ValueError('missing recovery cases')
            for name,run in zip(('profile-rejection','crc-rejection','partial-reset','receive-timeout','break-abort','recovery-upload'),recovery):
                acknowledgments,frames=parse_frames(run['uart'])
                if name=='recovery-upload':
                    if len(frames)!=1:raise ValueError('missing recovered result')
                    check_expected(frames[0],[42])
                elif frames:raise ValueError('failed upload produced an execution result')
                results.append({'name':name,'uart':run,'replies':acknowledgments,'results':frames});save('running')
            for permille in (980,1020):
                run=execute(['--period-permille',str(permille),'--upload',path])[0]
                acknowledgments,frames=parse_frames(run['uart'])
                if len(frames)!=1:raise ValueError('missing result at independent serial rate')
                check_expected(frames[0],[42])
                results.append({'name':f'serial-period-{permille}','uart':run,'result':frames[0]});save('running')
            for phase,target in [('execution','selftest'),('result','answer')]:
                if target not in packets:continue
                reference=next(result for result in results if result['name']==target)
                first=reference['uart']['first_result_clock'];commit=reference['uart']['commit_clock']
                cycles=reference['result']['cycles']
                if phase=='execution':
                    offset=first-commit-(cycles//2+4)*scale
                    if cycles<64 or not first-(cycles-8)*scale<commit+offset<first-8*scale:
                        raise ValueError('reset is outside measured invocation')
                else:offset=first-commit+35*bit_ticks
                interrupted,recovered=execute(['--interrupt',str(packets[target]),str(offset),'--upload',path])
                if not interrupted['interrupted']:raise ValueError('reset did not occur')
                _,frames=parse_frames(recovered['uart'])
                if len(frames)!=1:raise ValueError('missing result after interrupted execution')
                check_expected(frames[0],[42])
                results.append({'name':'reset-during-'+phase,'offset_after_commit':offset,'interrupted':interrupted,
                    'recovered':recovered,'result':frames[0]});save('running')
        # Ensure the independent value checker would reject an incorrect CPU result.
        try:check_expected({'status':0,'trap':0,'cycles':53,'values':[41]},[42])
        except AssertionError:pass
        else:raise ValueError('result oracle accepted an incorrect value')
        if digest(source)!=source_hash or any(digest(ROOT/name)!=value for name,value in hashes.items()):
            raise ValueError('loadable verification inputs changed')
        verify_simulator(binary);save('passed')
    except BaseException:
        save('failed');raise


if __name__=='__main__':main()
