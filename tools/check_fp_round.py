#!/usr/bin/env python3
"""Prove and check the isolated binary32/binary64 integral-rounding experiment."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent.parent
BUILD=ROOT/'build/fp-round'
CANDIDATE=ROOT/'experiments/rounding/wasmetal_fp_round.sv'
REFERENCE=ROOT/'tests/rtl/wasmetal_fp_round_reference.sv'
BENCH=ROOT/'tests/rtl/fp_round_four_state.sv'
ORIGINAL_SHA256='499d39b768aa21aedeb707cb479f673f24d2d8932820382eb7f3c635413198fe'
VENDOR=ROOT/'third_party/hardfloat/source'
LIBRARY=ROOT/'.cache/tools/usr/share/yosys/ecp5/cells_sim.v'
YOSYS=ROOT/'.cache/tools/usr/bin/yosys'
IVERILOG=ROOT/'.cache/tools/usr/bin/iverilog'
VVP=ROOT/'.cache/tools/usr/bin/vvp'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def yosys(body,label,negative=False):
    script=BUILD/(label+'.ys');log=BUILD/(label+'.log')
    script.write_text(body)
    with log.open('w') as out:
        run=subprocess.run([str(YOSYS),'-Q','-T','-s',str(script)],cwd=ROOT,
            stdout=out,stderr=subprocess.STDOUT,timeout=600)
    text=log.read_text()
    if negative:
        if run.returncode!=0 or 'SAT proof finished - model found: FAIL!' not in text:
            raise ValueError('rounding proof did not reject its mutation: '+label)
    elif run.returncode:
        raise ValueError('rounding tool failed: '+str(log))
    return {'log_sha256':digest(log),'script_sha256':digest(script)}


def reference_instance(n,exp,sig,result='expected'):
    return (f"wasmetal_fp_round_reference #(.EXP({exp}),.SIG({sig})) reference_round("
        f".operation({{4'b0,mode}}+6'd2),.a(a),.b({n}'d0),.integer_signed(1'b0),"
        f".result_signed(1'b0),.integer_input(64'd0),.arithmetic_result({n}'d0),"
        f".arithmetic_done(1'b0),.result({result}));\n")


def read_reference():
    paths=sorted(VENDOR.glob('*.v'))+[VENDOR/'RISCV/HardFloat_specialize.v',REFERENCE]
    return f'read_verilog -sv -I{VENDOR} -I{VENDOR}/RISCV '+ ' '.join(map(str,paths))+'\n'


def proof(exp,sig,candidate,label,mapped=None,negative=False):
    n=exp+sig;top=BUILD/(label+'.sv')
    expected=(reference_instance(n,exp,sig) if mapped is None else
        f'wasmetal_fp_round #(.EXP({exp}),.SIG({sig})) expected_round(a,mode,expected);\n')
    actual=(f'wasmetal_fp_round #(.EXP({exp}),.SIG({sig})) actual_round(a,mode,actual);\n'
        if mapped is None else 'mapped_round_component actual_round(.a(a),.mode(mode),.result(actual));\n')
    actual_expression='(actual ^ 1)' if mapped is not None and negative else 'actual'
    top.write_text(f'module rounding_miter(input wire [{n-1}:0] a,input wire [1:0] mode,output wire equal);\n'
        f'wire [{n-1}:0] expected,actual;\n'+expected+actual+
        f'assign equal=expected=={actual_expression};\nendmodule\n')
    consumed=[candidate,top]+([mapped] if mapped is not None else [])
    identities={str(p.relative_to(ROOT)):digest(p) for p in consumed}
    script=read_reference() if mapped is None else f'read_verilog -sv {LIBRARY} {mapped}\n'
    script+=f'read_verilog -sv {candidate} {top}\n'
    script+='prep -top rounding_miter -flatten\nopt -full\nwreduce\nopt -full\ncheck -assert\nscc -expect 0\n'
    script+='sat -set-def-inputs -enable_undef -prove equal 1 '+('' if negative else '-verify ')+ '-show-inputs -show-outputs\n'
    result=yosys(script,label,negative)
    if not negative and 'SAT proof finished - no model found: SUCCESS!' not in (BUILD/(label+'.log')).read_text():
        raise ValueError('missing rounding proof success')
    if any(digest(ROOT/p)!=sha for p,sha in identities.items()):raise ValueError('rounding proof input changed')
    result['inputs']=identities
    return result


def mapping(exp,sig,variant):
    n=exp+sig;label=f'{variant}-{n}';top=BUILD/(label+'.sv')
    instance=(reference_instance(n,exp,sig,'result') if variant=='reference' else
        f'wasmetal_fp_round #(.EXP({exp}),.SIG({sig})) implementation(a,mode,result);\n')
    top.write_text(f'module round_component(input wire [{n-1}:0] a,input wire [1:0] mode,output wire [{n-1}:0] result);\n'
        +instance+'endmodule\n')
    net=BUILD/(label+'.json');verilog=BUILD/(label+'-mapped.v')
    script=(read_reference() if variant=='reference' else '')+f'read_verilog -sv {CANDIDATE} {top}\n'
    script+=f'synth_ecp5 -abc9 -top round_component -json {net}\ncheck -assert\nscc -expect 0\n'
    script+=f'rename round_component mapped_round_component\nwrite_verilog -noattr {verilog}\n'
    result=yosys(script,label)
    cells=Counter(c['type'] for c in json.loads(net.read_text())['modules']['round_component']['cells'].values())
    result.update(cells=dict(cells),netlist_sha256=digest(net),verilog_sha256=digest(verilog))
    return result,verilog


@lru_cache(maxsize=None)
def oracle(bits,mode,exp,sig):
    """Decode an exact rational, round numerically, then encode the exact integer."""
    n=exp+sig;p=sig-1;bias=(1<<(exp-1))-1
    sign=bits>>(n-1);exponent=(bits>>p)&((1<<exp)-1);fraction=bits&((1<<p)-1)
    if exponent==(1<<exp)-1:
        return (((1<<exp)-1)<<p)|(1<<(p-1)) if fraction else bits
    significand=fraction if exponent==0 else (1<<p)|fraction
    power=(1 if exponent==0 else exponent)-bias-p
    value=Fraction(significand<<max(power,0),1<<max(-power,0))
    if sign:value=-value
    rounded=(math.ceil,math.floor,int,round)[mode](value)
    if rounded==0:return sign<<(n-1)
    negative=int(rounded<0);magnitude=abs(rounded);leading=magnitude.bit_length()-1
    shift=leading-p
    if shift>0:
        if magnitude&((1<<shift)-1):raise ValueError('oracle integer is not exactly representable')
        encoded=magnitude>>shift
    else:encoded=magnitude<<-shift
    return (negative<<(n-1))|((leading+bias)<<p)|(encoded&((1<<p)-1))


def vectors(exp,sig):
    n=exp+sig;p=sig-1;bias=(1<<(exp-1))-1;all_bits=(1<<n)-1
    path=BUILD/f'vectors-{n}.txt';count=0;binary_count=0
    def possible(word,operation):
        joined=word+operation;positions=[i for i,c in enumerate(joined) if c in 'xz']
        if len(positions)>2:raise ValueError('enumeration requires at most two uncertain bits')
        values=[]
        for choices in itertools.product('01',repeat=len(positions)):
            concrete=list(joined)
            for i,c in zip(positions,choices):concrete[i]=c
            values.append(oracle(int(''.join(concrete[:n]),2),int(''.join(concrete[n:]),2),exp,sig))
        union=0;intersection=all_bits
        for v in values:union|=v;intersection&=v
        return union,intersection
    with path.open('w') as output:
        def emit(word,operation,known_bounds=None):
            nonlocal count,binary_count
            union,intersection=known_bounds if known_bounds is not None else possible(word,operation)
            output.write(f'{word} {operation} {union:x} {intersection:x}\n')
            count+=1;binary_count+=int(not any(c in 'xz' for c in word+operation))
        # Place concrete X-optimism regressions before the larger corpus.
        for unknown in 'xz':
            emit(f'{(bias-2)<<p:0{n}b}','0'+unknown)
            infinity=f'{((1<<exp)-1)<<p:0{n}b}'
            emit(infinity[:-1]+unknown,'00')
        exponents=sorted({0,1,bias-2,bias-1,bias,bias+1,bias+p-1,bias+p,(1<<exp)-2,(1<<exp)-1})
        fractions=sorted({0,1,(1<<(p-1))-1,1<<(p-1),(1<<(p-1))+1,(1<<p)-1})
        directed=[(sign<<(n-1))|(e<<p)|f for sign in range(2) for e in exponents for f in fractions]
        # One X or Z at every data/control position across edge magnitudes.
        for bits in directed:
            for mode in range(4):
                joined=f'{bits:0{n}b}{mode:02b}'
                for i in range(n+2):
                    for unknown in 'xz':
                        changed=joined[:i]+unknown+joined[i+1:]
                        emit(changed[:n],changed[n:])
        rng=random.Random(0x574d524f554e44+n)
        for _ in range(2048):
            joined=f'{rng.getrandbits(n):0{n}b}{rng.randrange(4):02b}'
            changed=list(joined)
            for i in rng.sample(range(n+2),2):changed[i]=rng.choice('xz')
            emit(''.join(changed[:n]),''.join(changed[n:]))
        # Every result bit can be either value: zero clears them all, while
        # representable integers supply witnesses with each bit set. Integers
        # are fixed points of every rounding mode, including unknown modes.
        for unknown in 'xz':
            for mode in range(4):emit(unknown*n,f'{mode:02b}',(all_bits,0))
            emit(unknown*n,unknown*2,(all_bits,0))
        # Every exponent, both signs, all modes, zero/extreme/half fractions.
        for sign in range(2):
            for exponent in range(1<<exp):
                for fraction in (0,1,1<<(p-1),(1<<p)-1):
                    bits=(sign<<(n-1))|(exponent<<p)|fraction
                    for mode in range(4):emit(f'{bits:0{n}b}',f'{mode:02b}')
    return path,{'vectors':count,'binary_vectors':binary_count,'unknown_vectors':count-binary_count,
        'sha256':digest(path),'oracle':'exact Python Fraction arithmetic; all completions of up to two X/Z bits'}


def four_state(exp,sig,candidate,mapped,vector_file,label,negative=False,counts=None):
    executable=BUILD/(label+'.vvp');compile_log=BUILD/(label+'-compile.log');log=BUILD/(label+'.log')
    identities={str(p.relative_to(ROOT)):digest(p) for p in [candidate,mapped,vector_file,BENCH]}
    command=[str(IVERILOG),'-B'+str(ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl'),'-g2012','-Wall','-s','fp_round_four_state',
        '-I'+str(LIBRARY.parent),
        f'-Pfp_round_four_state.EXP={exp}',f'-Pfp_round_four_state.SIG={sig}',
        '-o',str(executable),str(LIBRARY),str(candidate),str(mapped),str(BENCH)]
    with compile_log.open('w') as out:subprocess.run(command,stdout=out,stderr=subprocess.STDOUT,check=True,cwd=ROOT)
    run=subprocess.run([str(VVP),str(executable),'+vectors='+str(vector_file)],cwd=ROOT,
        capture_output=True,text=True,timeout=600)
    log.write_text(run.stdout+run.stderr)
    if negative:
        if run.returncode==0 or 'optimistic native rounded bit' not in log.read_text():
            raise ValueError('four-state checker did not reject its mutation: '+label)
    elif run.returncode or not run.stdout.startswith('PASS '):
        raise ValueError('rounding four-state check failed: '+str(log))
    elif run.stdout.splitlines()[0]!=f'PASS {counts["vectors"]} rounding vectors; {counts["binary_vectors"]} binary':
        raise ValueError('rounding simulation did not consume the complete oracle corpus')
    if any(digest(ROOT/p)!=sha for p,sha in identities.items()):raise ValueError('rounding simulation input changed')
    return {'log_sha256':digest(log),'executable_sha256':digest(executable),
        'compile_log_sha256':digest(compile_log),'command':command,'output':run.stdout.strip(),'inputs':identities}


def main():
    started=time.monotonic();BUILD.mkdir(parents=True,exist_ok=True)
    report_path=ROOT/'reports/fp-round-experiment.json';report_path.unlink(missing_ok=True)
    reconstructed=REFERENCE.read_text().replace('module wasmetal_fp_round_reference #(','module wasmetal_fp_format #(')
    if hashlib.sha256(reconstructed.encode()).hexdigest()!=ORIGINAL_SHA256:
        raise ValueError('frozen rounding reference differs from the recorded CPU source')
    inputs={str(p.relative_to(ROOT)):digest(p) for p in [CANDIDATE,REFERENCE,BENCH,Path(__file__).resolve(),
        ROOT/'tools/upstream.lock.json',*sorted(VENDOR.rglob('*.v')),*sorted(VENDOR.rglob('*.vi')),
        *sorted(LIBRARY.parent.glob('*.vh')),LIBRARY,YOSYS,IVERILOG,VVP]}
    results=[]
    for exp,sig in [(8,24),(11,53)]:
        n=exp+sig;item={'bits':n,'reference_origin_sha256':ORIGINAL_SHA256}
        item['binary_equivalence']=proof(exp,sig,CANDIDATE,f'equivalence-{n}')
        item['negative_controls']={}
        mutations={
            'ties-away':(' || odd)'," || 1'b1)"),
            'lost-negative-zero':('small_result={sign,',"small_result={1'b0,"),
        }
        for name,(before,after) in mutations.items():
            body=CANDIDATE.read_text()
            if body.count(before)!=1:raise ValueError('review rounding mutation '+name)
            mutant=BUILD/(name+'.sv');mutant.write_text(body.replace(before,after))
            item['negative_controls'][name]=proof(exp,sig,mutant,f'{name}-{n}',negative=True)
        item['reference_mapping'],_=mapping(exp,sig,'reference')
        item['candidate_mapping'],mapped=mapping(exp,sig,'candidate')
        item['mapped_equivalence']=proof(exp,sig,CANDIDATE,f'mapped-equivalence-{n}',mapped=mapped)
        item['negative_controls']['mapped-bit-inversion']=proof(exp,sig,CANDIDATE,
            f'mapped-bit-inversion-{n}',mapped=mapped,negative=True)
        vector_file,item['vectors']=vectors(exp,sig)
        item['four_state']=four_state(exp,sig,CANDIDATE,mapped,vector_file,f'four-state-{n}',counts=item['vectors'])
        for name,before,after,count in [
            ('unknown-mode-as-false','mode==0 ?','mode===0 ?',2),
            ('unknown-nan-as-false','result=nan ?',"result=(nan===1'b1) ?",1)]:
            body=CANDIDATE.read_text()
            if body.count(before)!=count:raise ValueError('review four-state mutation '+name)
            mutant=BUILD/(name+'.sv');mutant.write_text(body.replace(before,after))
            item['negative_controls'][name]=four_state(exp,sig,mutant,mapped,vector_file,f'{name}-{n}',negative=True)
        if digest(vector_file)!=item['vectors']['sha256']:raise ValueError('rounding vectors changed')
        results.append(item)
        print(f'PASS binary{n}: all binary inputs, mapped equivalence, {item["vectors"]["vectors"]} oracle vectors and five rejected mutations',flush=True)
    if any(digest(ROOT/name)!=value for name,value in inputs.items()):raise ValueError('rounding verification inputs changed')
    report={'status':'passed','scope':'isolated experimental rounding component; not integrated into CPU',
        'inputs':inputs,'reference_origin':'rtl/wasmetal_fp_format.sv at 2ffd29d; frozen copy differs only in module name',
        'results':results,'python_version':sys.version,'elapsed_seconds':time.monotonic()-started,
        'physical_hardware_tested':False,'whole_cpu_area_or_timing_measured':False}
    report_path.parent.mkdir(exist_ok=True);report_path.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
