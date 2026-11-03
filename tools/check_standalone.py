#!/usr/bin/env python3
"""Check standalone execution through UART alone, with independent expectations."""
import argparse
import binascii
import json
from pathlib import Path
import subprocess
import time

from prepare_standalone import ROOT, prepare, digest, load_profile, record
from standalone_support import verify_image, verify_simulator
from run_spec import RTL, Trap
from wasm_image import Module


def decode(packet):
    raw = bytes.fromhex(packet)
    if len(raw) < 12 or raw[:3] != b'WM\x01':
        raise ValueError('bad standalone frame header')
    count = raw[5]
    if len(raw) != 12 + 16 * count:
        raise ValueError('bad standalone frame length')
    if binascii.crc_hqx(raw[2:-2], 0xffff) != int.from_bytes(raw[-2:], 'little'):
        raise ValueError('bad standalone frame checksum')
    if raw[3] > 4 or (raw[3] != 0 and count) or (raw[3] == 0 and raw[4]):
        raise ValueError('inconsistent standalone status')
    return {'status': raw[3], 'trap': raw[4], 'cycles': int.from_bytes(raw[6:10], 'little'),
            'values': [int.from_bytes(raw[n:n+16], 'little') for n in range(10, len(raw)-2, 16)]}


def check_expected(frame, expected, status=0, trap=0):
    if (frame['status'], frame['trap'], frame['values']) != (status, trap, expected):
        raise AssertionError(f'UART result differs from independent expectation: {frame}')


SELFTEST_VALUES = [42,42,2,39,0x40700000,0x4008000000000000,
                  sum((11*(n+1)) << (16*n) for n in range(8)),42,0x33221111,0xa5a5,20,99]


def cases():
    yield {'name':'answer', 'source':ROOT/'examples/standalone/answer.wat', 'expected':[42]}
    yield {'name':'selftest', 'source':ROOT/'examples/standalone/selftest.wat', 'expected':SELFTEST_VALUES}
    yield {'name':'arguments', 'args':[7,35], 'expected':[42], 'wat':'''(module
      (func (export "main") (param i32 i32) (result i32)
        local.get 0 local.get 1 i32.add))'''}
    yield {'name':'memory64', 'expected':[0,0x1122334455667788,0xffffffffffffffff], 'wat':'''(module
      (memory i64 0 1)
      (func (export "main") (result i64 i64 i64)
        i64.const 1 memory.grow
        i64.const 65527 i64.const 0x1122334455667788 i64.store
        i64.const 65527 i64.load
        i64.const 1 memory.grow))'''}
    yield {'name':'unaligned-simd', 'expected':[(1<<128)-1], 'wat':'''(module
      (memory 1 1)
      (func (export "main") (result v128)
        i32.const 65519 v128.const i32x4 -1 -1 -1 -1 v128.store
        i32.const 65519 v128.load))'''}
    yield {'name':'subtype-cast', 'expected':[42], 'wat':'''(module
      (type $base (sub (struct (field i32))))
      (type $child (sub $base (struct (field i32))))
      (func (export "main") (result i32)
        i32.const 42 struct.new $child ref.cast (ref $base) struct.get $base 0))'''}
    yield {'name':'tail-reference', 'expected':[42], 'wat':'''(module
      (type $t (func (param i32) (result i32)))
      (elem declare func $target)
      (func $target (type $t) local.get 0 i32.const 1 i32.add)
      (func $caller (type $t) local.get 0 ref.func $target return_call_ref $t)
      (func (export "main") (result i32) i32.const 41 call $caller))'''}
    yield {'name':'branches', 'expected':[5050,42], 'wat':'''(module
      (func (export "main") (result i32 i32) (local $n i32) (local $sum i32)
        i32.const 100 local.set $n
        block $exit loop $again
          local.get $n i32.eqz br_if $exit
          local.get $sum local.get $n i32.add local.set $sum
          local.get $n i32.const 1 i32.sub local.set $n br $again
        end end
        local.get $sum
        block $selected (result i32)
          i32.const 42 i32.const 0 br_table $selected $selected
        end))'''}
    yield {'name':'sixteen-results', 'expected':list(range(16)), 'wat':
           '(module (func (export "main") (result '+ ' '.join(['i32']*16) + ') '+
           ' '.join('i32.const '+str(n) for n in range(16))+'))'}
    yield {'name':'no-results', 'expected':[], 'wat':'(module (func (export "main") nop))'}
    traps = {
        'unreachable': (1, '(module (func (export "main") unreachable))'),
        'divide-zero': (2, '(module (func (export "main") (result i32) i32.const 1 i32.const 0 i32.div_u))'),
        'memory-oob': (4, '(module (memory 1 1) (func (export "main") (result i32) i32.const 65535 i32.load))'),
        'memory64-wrap': (4, '(module (memory i64 1 1) (func (export "main") (result i32) i64.const -1 i32.load))'),
        'table-oob': (5, '(module (table 1 1 funcref) (func (export "main") (result funcref) i32.const 1 table.get))'),
        'null-call': (6, '(module (type $t (func)) (func (export "main") ref.null $t call_ref $t))'),
        'bad-cast': (10, '(module (type $s (struct)) (func (export "main") ref.null $s ref.cast (ref $s) drop))'),
        'uncaught': (13, '(module (tag $e) (func (export "main") throw $e))'),
    }
    for name,(trap,wat) in traps.items():
        yield {'name':name,'wat':wat,'status':1,'trap':trap,'expected':[]}
    yield {'name':'heap-exhaustion','expected':[],'status':1,'trap':12,'reference':False,'wat':'''(module
      (type $s (struct (field i32)))
      (func (export "main") (local $n i32)
        loop $again
          i32.const 42 struct.new $s drop
          local.get $n i32.const 1 i32.add local.tee $n i32.const 1100 i32.lt_u br_if $again
        end))'''}
    yield {'name':'watchdog','expected':[],'status':3,'trap':0,'reference':False,
           'wat':'(module (func (export "main") (loop $forever br $forever)))'}
    for name,at,source,expected in [
        ('reset-during-clear',50,'answer', [42]),
        ('reset-during-execution',132000,'selftest',SELFTEST_VALUES),
        ('reset-during-uart',131500,'answer',[42])]:
        yield {'name':name,'source':ROOT/f'examples/standalone/{source}.wat',
               'reset_at':at,'expected':expected}
    for name,status,trap in [('bad-header',2,254),('bad-command',2,254),
                            ('bad-init-range',2,254),('missing-end',2,254),
                            ('damaged-instruction',1,1),('boot-initializer-trap',4,1)]:
        yield {'name':name,'source':ROOT/'examples/standalone/answer.wat',
               'corrupt':name,'expected':[],'status':status,'trap':trap,'reference':False}


def inject_corruption(image, name):
    """Deliberately bypass preflight to exercise hardware error reporting."""
    path=image/'boot.hex'
    words=[int(x,16) for x in path.read_text().splitlines()]
    width=58
    if name=='bad-header': words[0]^=1
    elif name=='bad-command': words[1]=record(14)
    elif name=='bad-init-range': words[1]=record(2,index=load_profile()['ram_bytes']-1,aux=16,data=0xff)
    elif name=='missing-end': words[((words[0]>>96)&0xffffffff)-1]=record(1,1)
    else:
        trace=(image/'initialization.txt').read_text().splitlines()
        op='Z' if name=='damaged-instruction' else 'R'
        fid=int(next(line for line in trace if line.startswith(op+' ')).split()[1])
        functions=[int(x,16) for x in (image/'functions.hex').read_text().splitlines()]
        entry=functions[fid]&0xffffffff
        path=image/'code.hex';width=72
        words=[int(x,16) for x in path.read_text().splitlines()]
        words[entry]=0  # A real unreachable instruction, not a fabricated result.
    path.write_text(''.join(f'{word:0{width}x}\n' for word in words))
    try: verify_image(image)
    except ValueError: return
    raise AssertionError('corrupt image escaped the preflight hash check')


def reference_check(image, case):
    rtl = RTL()
    try:
        instance = rtl.instantiate(Module((image/'program.wasm').read_bytes()))
        try:
            actual = rtl.invoke(instance.exports['main'][1], case.get('args',[]))
            if case.get('status',0) or actual != case['expected']:
                raise AssertionError('native reference differs from independent expectation')
        except Trap as e:
            if case.get('status') != 1 or e.code != case['trap']:
                raise
    finally:
        rtl.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--board',action='store_true')
    parser.add_argument('--case',action='append',default=[])
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    binary=ROOT/'build'/('standalone-board-sim/Vwasmetal_standalone_ulx3s' if args.board
                        else 'standalone-sim/Vwasmetal_standalone')
    identity=verify_simulator(binary)
    started=time.monotonic(); results=[]
    test_source_sha=digest(Path(__file__).resolve())
    controls={}
    report=args.report or ROOT/'reports'/('standalone-board.json' if args.board else 'standalone.json')
    report.parent.mkdir(exist_ok=True,parents=True)

    def save(status):
        report.write_text(json.dumps({'status':status,'backend':identity['backend'],
            'binary_sha256':identity['binary_sha256'],'profile':load_profile(),
            'test_source_sha256':test_source_sha,'build_inputs':identity['inputs'],'cases':results,
            'negative_controls':controls,
            'elapsed_seconds':time.monotonic()-started,'physical_hardware_tested':False},indent=2)+'\n')

    save('running')
    selected=list(cases())
    if args.case:
        if set(args.case)-{c['name'] for c in selected}: parser.error('unknown standalone case')
        selected=[c for c in selected if c['name'] in args.case]
    elif args.board:
        selected=[c for c in selected if c['name'] in ('answer','selftest','memory64','sixteen-results','memory-oob',
                  'reset-during-clear','reset-during-execution','reset-during-uart','bad-header')]
    try:
        for case in selected:
            cwd=ROOT/'build/standalone-cases'/identity['backend']/case['name']; cwd.mkdir(parents=True,exist_ok=True)
            source=case.get('source',cwd/'program.wat')
            if 'wat' in case: source.write_text(case['wat'])
            image=cwd/'build/standalone-image'
            manifest=prepare(source,image,arguments=case.get('args',[]))
            verify_image(image)
            if case.get('reference',True): reference_check(image,case)
            if 'corrupt' in case: inject_corruption(image,case['corrupt'])
            flags=['--power-on'] if args.board else []
            if case['name'] in ('answer','selftest'): flags+=['--reboots','2']
            if 'reset_at' in case: flags+=['--reset-at',str(case['reset_at']*(32 if args.board else 1))]
            result=subprocess.run([str(binary),*flags],cwd=cwd,capture_output=True,text=True,timeout=300)
            if result.returncode: raise RuntimeError(result.stdout+result.stderr)
            frames=[]
            for line in result.stdout.splitlines():
                entry=json.loads(line); frame=decode(entry['uart'])
                check_expected(frame,case['expected'],case.get('status',0),case.get('trap',0))
                frames.append(dict(frame,simulation_clocks=entry['clocks'],uart=entry['uart']))
            if len(frames)!=(2 if '--reboots' in flags else 1):
                raise AssertionError('missing UART completion or restart')
            results.append({'name':case['name'],'source_sha256':digest(source),
                'image_manifest_sha256':digest(image/'manifest.json'),
                'image_files':{name:digest(image/name) for name in manifest['files']},
                'reference_compared':case.get('reference',True),
                'intentional_corruption':case.get('corrupt'), 'frames':frames})
            if case['name']=='answer':
                raw=bytearray.fromhex(frames[0]['uart']);raw[10]^=1
                try: decode(raw.hex())
                except ValueError: controls['corrupt_uart_rejected']=True
                else: raise AssertionError('UART checksum negative control escaped')
                try: check_expected(frames[0],[43])
                except AssertionError: controls['wrong_expected_result_rejected']=True
                else: raise AssertionError('result oracle negative control escaped')
            save('running'); print(case['name']+': passed',flush=True)
        verify_simulator(binary)
        if digest(Path(__file__).resolve())!=test_source_sha:
            raise RuntimeError('standalone tests changed during execution')
        save('passed')
    except Exception as e:
        results.append({'failure':str(e)}); save('failed'); raise
    print(report)


if __name__=='__main__': main()
