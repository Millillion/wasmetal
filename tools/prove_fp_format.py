#!/usr/bin/env python3
"""Prove every format-unit output after integrating direct integral rounding."""
import json
from pathlib import Path
import time
from check_fp_round import ROOT,BUILD,CANDIDATE,REFERENCE,VENDOR,YOSYS,digest,read_reference,yosys,ORIGINAL_SHA256

FORMAT=ROOT/'rtl/wasmetal_fp_format.sv'


def prove(exp,sig,negative=False):
    n=exp+sig;label=f'format-{n}'+('-wrong-mode' if negative else '')
    source=FORMAT
    if negative:
        body=FORMAT.read_text();before="operation[1:0]-2'd2"
        if body.count(before)!=1:raise ValueError('review format integration mutation')
        source=BUILD/(label+'-source.sv');source.write_text(body.replace(before,"operation[1:0]-2'd1"))
    inputs=[('operation',6),('a',n),('b',n),('integer_signed',1),('result_signed',1),
        ('integer_input',64),('arithmetic_result',n),('arithmetic_done',1)]
    outputs=[('result',n),('div_result',n),('integer_float',n),('div_done',1),
        ('int32_result',32),('int64_result',64),('int32_flags',3),('int64_flags',3),
        ('rec_a',n+1),('rec_b',n+1),('is_nan',1)]
    declaration=lambda name,width:f'wire [{width-1}:0] {name}'
    text='module format_miter('+','.join('input '+declaration(k,w) for k,w in inputs)+',output wire equal);\n'
    for prefix,module in [('expected','wasmetal_fp_round_reference'),('actual','wasmetal_fp_format')]:
        text+='\n'.join(declaration(prefix+'_'+k,w)+';' for k,w in outputs)+'\n'
        pins=[f'.{k}({k})' for k,_ in inputs]+[f'.{k}({prefix}_{k})' for k,_ in outputs]
        text+=f'{module} #(.EXP({exp}),.SIG({sig})) {prefix}_format('+','.join(pins)+');\n'
    bundle=lambda prefix:'{'+','.join(prefix+'_'+k for k,_ in outputs)+'}'
    text+=f'assign equal={bundle("expected")}=={bundle("actual")};\nendmodule\n'
    top=BUILD/(label+'.sv');top.write_text(text)
    identities={str(p.relative_to(ROOT)):digest(p) for p in [source,top,CANDIDATE]}
    script=read_reference()+f'read_verilog -sv {CANDIDATE} {source} {top}\n'
    script+='prep -top format_miter -flatten\nopt -full\nwreduce\nopt -full\ncheck -assert\nscc -expect 0\n'
    script+='sat -set-def-inputs -enable_undef -prove equal 1 '+('' if negative else '-verify ')+'-show-inputs -show-outputs\n'
    result=yosys(script,label,negative)
    if not negative and 'SAT proof finished - no model found: SUCCESS!' not in (BUILD/(label+'.log')).read_text():
        raise ValueError('missing integrated format proof')
    if any(digest(ROOT/p)!=h for p,h in identities.items()):raise ValueError('format proof input changed')
    result.update(inputs=identities,compared_output_bits=sum(w for _,w in outputs))
    return result


def main():
    started=time.monotonic();BUILD.mkdir(parents=True,exist_ok=True)
    report_path=ROOT/'reports/fp-format-proof.json';report_path.unlink(missing_ok=True)
    restored=REFERENCE.read_text().replace('module wasmetal_fp_round_reference #(','module wasmetal_fp_format #(')
    import hashlib
    if hashlib.sha256(restored.encode()).hexdigest()!=ORIGINAL_SHA256:raise ValueError('frozen format reference changed')
    paths=[FORMAT,CANDIDATE,REFERENCE,Path(__file__).resolve(),ROOT/'tools/check_fp_round.py',YOSYS,
        ROOT/'tools/upstream.lock.json',*sorted(VENDOR.rglob('*.v')),*sorted(VENDOR.rglob('*.vi'))]
    inputs={str(p.relative_to(ROOT)):digest(p) for p in paths}
    results=[]
    for exp,sig in [(8,24),(11,53)]:
        results.append({'precision_bits':exp+sig,'equivalence':prove(exp,sig),
            'incorrect_mode_mapping_rejected':prove(exp,sig,True)})
        print(f'PASS binary{exp+sig} complete format interface and rejected incorrect mode mapping',flush=True)
    if any(digest(ROOT/p)!=h for p,h in inputs.items()):raise ValueError('format verification source changed')
    report={'status':'passed','scope':'all format-unit outputs for every binary input, including all 64 operation encodings',
        'reference_origin_sha256':ORIGINAL_SHA256,'inputs':inputs,'results':results,
        'elapsed_seconds':time.monotonic()-started,'physical_hardware_tested':False}
    report_path.parent.mkdir(exist_ok=True);report_path.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
