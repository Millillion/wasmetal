#!/usr/bin/env python3
"""Prove binary mux/inverter behavior and enumerate their four-state models."""
import hashlib
import itertools
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

from check_xc7_luts import extract, run
from prepare_standalone import ROOT, digest


def oracle(kind, pins, vendor):
    if kind == 'INV':
        return '1' if pins == '0' else '0' if pins == '1' else 'x'
    selector, one, zero = pins
    if vendor:
        return one if selector == '1' else zero
    return one if selector == '1' else zero if selector == '0' else one if one == zero else 'x'


def ports(kind, flip=False):
    first = '~pins[0]' if flip else 'pins[0]'
    return f'.I({first})' if kind == 'INV' else f'.I0({first}),.I1(pins[1]),.S(pins[2])'


def bench(kind, trace, count, vendor=False, flip=False):
    width = 1 if kind == 'INV' else 3
    return f'''`timescale 1ps/1ps
module bench;
reg [{width-1}:0] pins,next_pins;
reg expected_yosys,expected_vendor;
wire value;
wire observed={'!value' if flip else 'value'};
{kind} dut(.O(value),{ports(kind)});
integer fd,n,j,extra;
initial begin
 fd=$fopen("{trace}","r");if(fd==0)$fatal(1,"MUX_TRACE_OPEN_FAILED");
 for(j=0;j<{count};j=j+1)begin
  n=$fscanf(fd,"%b %b %b",next_pins,expected_yosys,expected_vendor);
  if(n!=3)$fatal(1,"MUX_TRACE_TRUNCATED_OR_MALFORMED");
  pins=next_pins; #1000;
  if(observed!=={'expected_vendor' if vendor else 'expected_yosys'})
   $fatal(1,"MUX_ORACLE_MISMATCH pins=%b observed=%b yosys=%b vendor=%b",pins,observed,expected_yosys,expected_vendor);
 end
 n=$fscanf(fd,"%s",extra);
 if(n!=-1 && !(n==0 && $feof(fd)))$fatal(1,"MUX_TRACE_EXTRA_DATA");
 $fclose(fd);$display("PASS {count} logic oracle comparisons");$finish;
end
endmodule
'''


def main():
    started = time.monotonic(); directory = ROOT/'build/xc7-muxes'; directory.mkdir(exist_ok=True)
    report = ROOT/'reports/xc7-muxes.json'; report.unlink(missing_ok=True)
    library = ROOT/'.cache/tools/usr/share/yosys/xilinx/cells_sim.v'
    vendor_dir = ROOT/'third_party/xilinx-unisim'; kinds = ('MUXF7','MUXF8','INV')
    dependencies = [Path(__file__).resolve(),ROOT/'tools/check_xc7_luts.py',ROOT/'tools/prepare_standalone.py',
                    library,vendor_dir/'LICENSE',vendor_dir/'UPSTREAM.json']
    for kind in kinds:
        source = vendor_dir/(kind+'.v'); pin_path = vendor_dir/(kind+'.UPSTREAM.json')
        pin = json.loads(pin_path.read_text()); data = source.read_bytes()
        if digest(source) != pin['sha256'] or len(data) != pin['bytes'] or hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() != pin['git_blob_sha']:
            raise ValueError('vendor logic source changed: '+kind)
        dependencies += [source,pin_path]
    dependencies += [ROOT/'.cache/tools/usr/bin'/n for n in ('yosys','iverilog','vvp','verilator','verilator_bin')]
    dependencies += [p for p in sorted((ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl').glob('*')) if p.is_file()]
    dependencies += [p for p in sorted((ROOT/'.cache/tools/usr/share/verilator/include').rglob('*')) if p.is_file()]
    inputs = {str(p.relative_to(ROOT)):digest(p) for p in dependencies}
    compiler = Path(shutil.which('g++')).resolve()
    compiler_identity = {'path':str(compiler),'sha256':digest(compiler),
                         'version':subprocess.check_output([str(compiler),'--version'],text=True).splitlines()[0]}
    text = library.read_text(); notice = text[:re.search(r'^module\b',text,re.M).start()]
    generated = set(); checks = []; controls = []; differences = []; fixtures = {}
    def write(path, body):
        path.write_text(body); generated.add(path)
    def execute(command, log, **kwargs):
        run(command,log,**kwargs); generated.add(log)
    def simulate(fixture, source, log, failure=False, marker=None):
        binary = log.with_suffix('.vvp')
        command = [str(ROOT/'.cache/tools/usr/bin/iverilog'),'-B',str(ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl'),
                   '-g2012','-s','bench','-o',str(binary),str(source),str(fixture)]
        execute(command,log.with_name(log.stem+'-compile.log')); generated.add(binary)
        execute([str(ROOT/'.cache/tools/usr/bin/vvp'),str(binary)],log,expect_failure=failure,marker=marker)
        return {'command':command,'binary_sha256':digest(binary),'log':str(log.relative_to(ROOT))}
    for kind in kinds:
        target = directory/kind; target.mkdir(exist_ok=True)
        model = target/'yosys.v'; write(model,notice+'`timescale 1ps/1ps\n'+extract(text,kind)+'\n')
        vendor = vendor_dir/(kind+'.v')
        renamed = re.sub(r'\bmodule\s+'+kind+r'\b','module VENDOR_'+kind,vendor.read_text(),count=1)
        width = 1 if kind == 'INV' else 3
        for bad in (False,True):
            label = 'wrong-input-proof' if bad else 'equivalence'
            proof = target/(label+'.sv')
            write(proof,model.read_text()+'\n'+renamed+f'''
module proof(input [{width-1}:0] pins,output mismatch);
wire a,b;
{kind} u0(.O(a),{ports(kind)});
VENDOR_{kind} u1(.O(b),{ports(kind,bad)});
assign mismatch=a^b;
endmodule
''')
            script = target/(label+'.ys')
            write(script,f'read_verilog -sv {proof}\nprep -top proof\nflatten\nopt\nsat -verify -prove mismatch 0 -show-inputs\n')
            execute([str(ROOT/'.cache/tools/usr/bin/yosys'),'-s',str(script)],script.with_suffix('.log'),
                    expect_failure=bad,marker='proof did fail' if bad else 'SUCCESS!')
            if bad:controls.append(kind+'-wrong-input-proof')
        for four_state in (False,True):
            label = 'four-state' if four_state else 'known'; symbols = '01xz' if four_state else '01'
            rows = []; differing = 0; examples = []
            for pins in itertools.product(symbols,repeat=width):
                pins = ''.join(pins); y = oracle(kind,pins,False); v = oracle(kind,pins,True)
                rows.append(pins+' '+y+' '+v)
                if y != v:
                    differing += 1; examples.append({'pins_msb_to_lsb':pins,'yosys':y,'vendor':v})
            if not four_state and differing:raise ValueError('binary logic oracles disagree')
            if four_state:differences.append({'kind':kind,'cases':len(rows),'differing_cases':differing,'examples':examples[:8]})
            trace = target/(label+'.txt'); write(trace,'\n'.join(rows)+'\n')
            for is_vendor in (False,True):
                name = 'vendor' if is_vendor else 'yosys'
                fixture = target/(label+'-'+name+'.sv'); write(fixture,bench(kind,trace,len(rows),is_vendor))
                info = simulate(fixture,vendor if is_vendor else model,fixture.with_suffix('.log'),
                                marker=f'PASS {len(rows)} logic oracle comparisons')
                checks.append({'kind':kind,'model':name,'four_state':four_state,'cases':len(rows),**info})
                if not is_vendor:fixtures[(kind,four_state)] = (fixture,model,trace,len(rows))
            if not four_state:
                fixture = fixtures[(kind,False)][0]; obj = target/'obj'
                command = [str(ROOT/'.cache/tools/usr/bin/verilator'),'--binary','--timing','--assert','-j','1',
                           '-Wall','-Wno-DECLFILENAME','-Wno-UNUSEDSIGNAL','--top-module','bench',
                           '-MAKEFLAGS',f'CXX={compiler} LINK={compiler}','--Mdir',str(obj),str(model),str(fixture)]
                execute(command,target/'verilator-compile.log',env=dict(os.environ,VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')))
                execute([str(obj/'Vbench')],target/'verilator.log',marker=f'PASS {len(rows)} logic oracle comparisons')
                checks.append({'kind':kind,'model':'yosys-verilator','four_state':False,'cases':len(rows),
                               'command':command,'binary_sha256':digest(obj/'Vbench'),'log':str((target/'verilator.log').relative_to(ROOT))})
                wrong = target/'flipped-output.sv'; write(wrong,bench(kind,trace,len(rows),flip=True))
                simulate(wrong,model,wrong.with_suffix('.log'),True,'MUX_ORACLE_MISMATCH')
                controls.append(kind+'-flipped-output')
            elif kind != 'INV':
                wrong = target/'false-four-state-equivalence.sv'; write(wrong,bench(kind,trace,len(rows),vendor=True))
                simulate(wrong,model,wrong.with_suffix('.log'),True,'MUX_ORACLE_MISMATCH')
                controls.append(kind+'-false-four-state-equivalence')
        print('PASS',kind,'binary proof and all four-state combinations',flush=True)
    fixture,model,trace,count = fixtures[('MUXF7',False)]; lines = trace.read_text().splitlines()
    for name,data,marker in [
        ('truncated-trace','\n'.join(lines[:-1])+'\n','MUX_TRACE_TRUNCATED_OR_MALFORMED'),
        ('extra-trace',trace.read_text()+'000 0 0\n','MUX_TRACE_EXTRA_DATA'),
        ('malformed-trace','invalid\n'+'\n'.join(lines[1:])+'\n','MUX_TRACE_TRUNCATED_OR_MALFORMED')]:
        wrong_trace = directory/(name+'.txt'); write(wrong_trace,data)
        wrong = directory/(name+'.sv'); write(wrong,bench('MUXF7',wrong_trace,count))
        simulate(wrong,model,wrong.with_suffix('.log'),True,marker); controls.append(name)
    for name,value in inputs.items():
        if digest(ROOT/name) != value:raise ValueError('logic verification input changed: '+name)
    if digest(compiler) != compiler_identity['sha256']:raise ValueError('compiler changed')
    result = {'status':'passed','scope':'binary equivalence proofs and independent complete truth tables for MUXF7, MUXF8 and INV',
              'inputs':inputs,'compiler':compiler_identity,'binary_equivalence_proven':True,'checks':checks,
              'four_state_vendor_equivalent':False,'four_state_differences':differences,
              'negative_controls_rejected':len(controls),'negative_controls':controls,
              'artifacts':{str(p.relative_to(ROOT)):digest(p) for p in sorted(generated)},
              'elapsed_seconds':time.monotonic()-started,'physical_hardware_tested':False}
    report.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS three logic proofs and',len(controls),'negative controls')


if __name__ == '__main__':
    main()
