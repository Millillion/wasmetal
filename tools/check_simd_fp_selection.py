#!/usr/bin/env python3
"""Prove the CPU's SIMD floating-point selectors and check unknown controls."""
import argparse
import json
from pathlib import Path
import subprocess

from prepare_standalone import ROOT, digest


PORTS = '''(
    input wire [127:0] top,below,third,simd_accum,
    input wire [63:0] fp_result,
    input wire [2:0] simd_lane,simd_arity,simd_mode,
    input wire simd_source_wide,simd_result_wide,
    output logic [63:0] simd_a_lane,simd_b_lane,simd_c_lane,simd_result_lane,
    output logic [127:0] simd_assembled
);
    logic [127:0] simd_a,simd_b;
'''
INPUTS = ['top','below','third','simd_accum','fp_result','simd_lane',
          'simd_arity','simd_mode','simd_source_wide','simd_result_wide']
OUTPUTS = ['simd_a_lane','simd_b_lane','simd_c_lane','simd_result_lane','simd_assembled']


def extract(source):
    """Use the actual CPU block and helper, never a second optimized copy."""
    start_marker='    always_comb begin\n        simd_a ='
    end_marker='\n    always_comb begin\n        decoded_table'
    helper_marker='    function automatic [63:0] extract_simd_fp_lane('
    if any(source.count(marker)!=1 for marker in [start_marker,end_marker,helper_marker]):
        raise ValueError('CPU selection boundaries changed; review proof extraction')
    start=source.index(start_marker);end=source.index(end_marker,start)
    helper_start=source.index(helper_marker)
    helper_end=source.index('endfunction',helper_start)+len('endfunction')
    helper=source[helper_start:helper_end]+'\n'
    if source[start:end].count('extract_simd_fp_lane(')!=3:
        raise ValueError('CPU must use the helper for all three operands')
    return 'module simd_fp_selection_candidate'+PORTS+helper+source[start:end]+'\nendmodule\n'


def miter():
    header=PORTS.split('    output logic')[0].rstrip().rstrip(',')+',\n    output wire ok\n);\n'
    body='wire [63:0] '+','.join(prefix+'_'+name for prefix in ['ref','dut'] for name in OUTPUTS[:4])+';\n'
    body+='wire [127:0] ref_simd_assembled,dut_simd_assembled;\n'
    for module,prefix in [('simd_fp_selection_reference','ref'),('simd_fp_selection_candidate','dut')]:
        connections=[f'.{name}({name})' for name in INPUTS]
        connections += [f'.{name}({prefix}_{name})' for name in OUTPUTS]
        body+=f'{module} {prefix}('+','.join(connections)+');\n'
    body+='assign ok={'+','.join('ref_'+name for name in OUTPUTS)+'}=={'+','.join('dut_'+name for name in OUTPUTS)+'};\n'
    return 'module selector_proof '+header+body+'endmodule\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--core',type=Path,default=ROOT/'rtl/wasmetal_core.sv')
    parser.add_argument('--build-directory',type=Path,default=ROOT/'build/simd-fp-selection')
    parser.add_argument('--report',type=Path,default=ROOT/'reports/simd-fp-selection.json')
    args=parser.parse_args()
    args.report.unlink(missing_ok=True)
    core=args.core.resolve();directory=args.build_directory.resolve();directory.mkdir(parents=True,exist_ok=True)
    reference=ROOT/'tests/rtl/simd_fp_selection_reference.sv'
    bench=ROOT/'tests/rtl/simd_fp_selection_four_state.sv'
    paths=[core,reference,bench,Path(__file__).resolve(),ROOT/'tools/prepare_standalone.py',ROOT/'tools/upstream.lock.json']
    hashes={str(p.relative_to(ROOT)):digest(p) for p in paths}
    candidate=directory/'candidate.sv';candidate.write_text(extract(core.read_text()))
    proof=directory/'proof.sv';proof.write_text(miter())
    outcomes={}
    for name,negative in [('binary-equivalence',False),('corrupted-lane',True)]:
        source=candidate
        if negative:
            source=directory/'corrupted-lane.sv'
            needle='simd_a_lane = extract_simd_fp_lane(simd_a,simd_lane,simd_source_wide);'
            if candidate.read_text().count(needle)!=1:raise ValueError('missing corruption point')
            source.write_text(candidate.read_text().replace(needle,needle[:-1]+" ^ 64'd1;"))
        script=directory/(name+'.ys');logfile=directory/(name+'.log')
        script.write_text(f'read_verilog -sv {reference} {source} {proof}\n'
            'prep -top selector_proof -flatten\nsat -verify -prove ok 1 -show-inputs -show-outputs\n')
        with logfile.open('w') as log:
            result=subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-Q','-T','-s',str(script)],
                cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=180)
        marker='proof did fail' if negative else 'SUCCESS!'
        if bool(result.returncode)!=negative or marker not in logfile.read_text():
            raise RuntimeError('unexpected proof outcome: '+name)
        outcomes[name]={'outcome':'rejected' if negative else 'proven','log_sha256':digest(logfile)}
    # Coercing an unknown width to false is unsafe: the binary input might
    # select wide lanes. The independent four-state oracle must detect it.
    old=',simd_source_wide);';bad=",(simd_source_wide===1'b1));"
    if candidate.read_text().count(old)!=3:raise ValueError('missing unknown-control mutation points')
    optimistic=directory/'optimistic-control.sv';optimistic.write_text(candidate.read_text().replace(old,bad))
    for name,source,negative in [('four-state',candidate,False),('optimistic-control',optimistic,True)]:
        binary=directory/(name+'.vvp');compile_log=directory/(name+'-compile.log')
        with compile_log.open('w') as log:
            subprocess.run([str(ROOT/'.cache/tools/usr/bin/iverilog'),
                '-B'+str(ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl'),'-g2012',
                '-s','simd_fp_selection_four_state','-o',str(binary),str(source),str(bench)],
                stdout=log,stderr=subprocess.STDOUT,check=True,timeout=60)
        result=subprocess.run([str(ROOT/'.cache/tools/usr/bin/vvp'),str(binary)],capture_output=True,text=True,timeout=120)
        logfile=directory/(name+'.log');logfile.write_text(result.stdout+result.stderr)
        marker='unjustified known bit' if negative else 'PASS 12288 four-state selector patterns'
        if bool(result.returncode)!=negative or marker not in logfile.read_text():
            raise RuntimeError('unexpected four-state outcome: '+name)
        outcomes[name]={'outcome':'rejected' if negative else 'passed','log_sha256':digest(logfile)}
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):
        raise RuntimeError('selection proof inputs changed during verification')
    report={'status':'passed','scope':'actual extracted CPU combinational block; not whole-CPU sequential equivalence',
        'binary_equivalence':'all operands, lane indices including out-of-range values, arities, modes and widths; all three selected operands, result selection and assembly',
        'four_state_patterns':12288,'four_state_scope':'three operands, 16 data patterns including X/Z bits, three arities and every 4-state assignment of lane/width controls; known output bits must agree with all compatible binary inputs; conservative unknown outputs permitted',
        'negative_controls_rejected':True,'checks':outcomes,'inputs':hashes,
        'generated_sources':{str(p.relative_to(ROOT)):digest(p) for p in [candidate,proof]},
        'physical_hardware_tested':False}
    args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS all-input SIMD selection proof, 12288 four-state patterns and both negative controls')


if __name__=='__main__':main()
