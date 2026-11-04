#!/usr/bin/env python3
"""Check all carry-chain inputs and make vendor/Yosys X/Z differences explicit."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

from check_xc7_luts import extract, run
from prepare_standalone import ROOT, digest


def logic_and(a, b):
    return '0' if '0' in (a,b) else '1' if a == b == '1' else 'x'


def logic_or(a, b):
    return '1' if '1' in (a,b) else '0' if a == b == '0' else 'x'


def expected(pins, vendor):
    ci, cy = pins[:2]
    if vendor:
        ci = '0' if ci == 'z' else ci
        cy = '0' if cy == 'z' else cy
    previous = logic_or(ci, cy); carries = []; sums = []
    for data, selector in zip(pins[2:6], pins[6:10]):
        sums.append(str(int(selector) ^ int(previous)) if selector in '01' and previous in '01' else 'x')
        if vendor:
            inverted = '1' if selector == '0' else '0' if selector == '1' else 'x'
            carry = logic_or(logic_and(selector, previous), logic_and(inverted, data))
        else:
            carry = (previous if selector == '1' else data if selector == '0' else
                     previous if previous == data else 'x')
        carries.append(carry); previous = carry
    return ''.join(reversed(carries))+''.join(reversed(sums))


def vectors(path, four_state):
    radix = 4 if four_state else 2; count = radix**10; differences = 0; examples = []
    with path.open('w') as stream:
        for value in range(count):
            pins = ['01xz'[(value >> ((2 if four_state else 1)*i)) & (radix-1)] for i in range(10)]
            yosys = expected(pins, False); vendor = expected(pins, True)
            stream.write(yosys+' '+vendor+'\n')
            if yosys != vendor:
                differences += 1
                if len(examples) < 8:
                    examples.append({'inputs_msb_to_lsb': ''.join(reversed(pins)),
                                     'yosys_co_o': yosys, 'vendor_co_o': vendor})
    return count, differences, examples


def bench(trace, count, four_state, vendor=False, flip=0):
    select = ("case ((j >> (2*k)) & 3)\n0:pins[k]=0;1:pins[k]=1;2:pins[k]=1'bx;3:pins[k]=1'bz;endcase"
              if four_state else '')
    drive = f'for(k=0;k<10;k=k+1)begin {select} end' if four_state else 'pins=j[9:0];'
    observed = f'{{co,o}} ^ 8\'h{flip:02x}' if flip else '{co,o}'
    return f'''module bench;
reg [9:0] pins;
reg [7:0] expected_yosys,expected_vendor;
wire [3:0] co,o;
wire [7:0] observed={observed};
CARRY4 dut(.CO(co),.O(o),.CI(pins[0]),.CYINIT(pins[1]),.DI(pins[5:2]),.S(pins[9:6]));
integer fd,j,k,n,extra;
initial begin
 fd=$fopen("{trace}","r");if(fd==0)$fatal(1,"CARRY_TRACE_OPEN_FAILED");
 for(j=0;j<{count};j=j+1)begin
  n=$fscanf(fd,"%b %b",expected_yosys,expected_vendor);
  if(n!=2)$fatal(1,"CARRY_TRACE_TRUNCATED");
  {drive}
  #1;
  if(observed!=={'expected_vendor' if vendor else 'expected_yosys'})
   $fatal(1,"CARRY_ORACLE_MISMATCH pins=%b observed=%b yosys=%b vendor=%b",pins,observed,expected_yosys,expected_vendor);
 end
 n=$fscanf(fd,"%s",extra);
 if(n!=-1 && !(n==0 && $feof(fd)))$fatal(1,"CARRY_TRACE_EXTRA_DATA");
 $fclose(fd);$display("PASS {count} carry oracle comparisons");$finish;
end
endmodule
'''


def main():
    directory = ROOT/'build/xc7-carry-check'; directory.mkdir(parents=True, exist_ok=True)
    report = ROOT/'reports/xc7-carry.json'; report.unlink(missing_ok=True); started = time.monotonic()
    vendor = ROOT/'third_party/xilinx-unisim/CARRY4.v'
    pin_path = vendor.with_name('CARRY4.UPSTREAM.json'); pin = json.loads(pin_path.read_text())
    data = vendor.read_bytes()
    if digest(vendor) != pin['sha256'] or len(data) != pin['bytes'] or \
            hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() != pin['git_blob_sha']:
        raise ValueError('vendor carry source differs from its upstream pin')
    library = ROOT/'.cache/tools/usr/share/yosys/xilinx/cells_sim.v'
    dependencies = [Path(__file__).resolve(), ROOT/'tools/check_xc7_luts.py', ROOT/'tools/prepare_standalone.py',
                    ROOT/'tests/xc7/carry.cpp',
                    vendor, pin_path, vendor.with_name('LICENSE'), vendor.with_name('UPSTREAM.json'), library,
                    *[ROOT/'.cache/tools/usr/bin'/n for n in ('yosys','iverilog','vvp','verilator','verilator_bin')]]
    dependencies += [p for p in sorted((ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl').glob('*')) if p.is_file()]
    dependencies += [p for p in sorted((ROOT/'.cache/tools/usr/share/verilator/include').rglob('*')) if p.is_file()]
    inputs = {str(p.relative_to(ROOT)): digest(p) for p in dependencies}
    compiler = Path(shutil.which('g++')).resolve()
    compiler_identity = {'path': str(compiler), 'sha256': digest(compiler),
                        'version': subprocess.check_output([str(compiler), '--version'], text=True).splitlines()[0]}
    original = extract(library.read_text(), 'CARRY4')
    model = directory/'yosys.v'; model.write_text(original+'\n')
    renamed = re.sub(r'\bmodule CARRY4\b', 'module VENDOR_CARRY4', vendor.read_text(), count=1)
    proof = directory/'equivalence.sv'
    proof.write_text(original+'\n'+renamed+'''
module proof(input [9:0] pins,output mismatch);
wire [7:0] a,b;
CARRY4 u0(.CO(a[7:4]),.O(a[3:0]),.CI(pins[0]),.CYINIT(pins[1]),.DI(pins[5:2]),.S(pins[9:6]));
VENDOR_CARRY4 u1(.CO(b[7:4]),.O(b[3:0]),.CI(pins[0]),.CYINIT(pins[1]),.DI(pins[5:2]),.S(pins[9:6]));
assign mismatch=|(a^b);
endmodule
''')
    ys = directory/'equivalence.ys'
    ys.write_text(f'read_verilog -sv -DXIL_XECLIB {proof}\nprep -top proof\nflatten\nopt\nsat -verify -prove mismatch 0 -show-inputs\n')
    run([str(ROOT/'.cache/tools/usr/bin/yosys'), '-s', str(ys)], directory/'equivalence.log', marker='SUCCESS!')
    if proof.read_text().count('CI | CYINIT') != 2:
        raise ValueError('unrecognized carry proof fixture')
    wrong_proof = directory/'wrong-equivalence.sv'
    wrong_proof.write_text(proof.read_text().replace('CI | CYINIT', 'CI & CYINIT'))
    wrong_ys = directory/'wrong-equivalence.ys'
    wrong_ys.write_text(ys.read_text().replace(str(proof), str(wrong_proof)))
    run([str(ROOT/'.cache/tools/usr/bin/yosys'), '-s', str(wrong_ys)], directory/'wrong-equivalence.log',
        expect_failure=True, marker='proof did fail')
    controls = ['wrong-carry-merge-proof']; checks = []; differences = None
    for four_state in (False, True):
        label = 'four-state' if four_state else 'known'
        trace = directory/(label+'.txt'); count, differing, examples = vectors(trace, four_state)
        if not four_state and differing != 0:
            raise ValueError('binary carry oracles disagree')
        if four_state:
            if differing == 0:
                raise ValueError('known vendor/Yosys X/Z differences were not exercised')
            differences = {'vectors': differing, 'examples': examples,
                           'inputs_msb_to_lsb': 'S[3:0], DI[3:0], CYINIT, CI', 'outputs_msb_to_lsb': 'CO[3:0], O[3:0]'}
        for name, source in [('yosys',model), ('vendor',vendor)]:
            fixture = directory/(label+'-'+name+'.sv'); fixture.write_text(bench(trace,count,four_state,name=='vendor'))
            binary = fixture.with_suffix('.vvp')
            command = [str(ROOT/'.cache/tools/usr/bin/iverilog'), '-B', str(ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl'),
                       '-g2012', '-DXIL_XECLIB', '-s', 'bench', '-o', str(binary), str(source), str(fixture)]
            run(command, fixture.with_suffix('.compile.log'))
            run([str(ROOT/'.cache/tools/usr/bin/vvp'), str(binary)], fixture.with_suffix('.log'),
                marker=f'PASS {count} carry oracle comparisons')
            checks.append({'model': name, 'mode': label, 'cases': count, 'command': command,
                           'log': str(fixture.with_suffix('.log').relative_to(ROOT)), 'binary_sha256': digest(binary)})
            print('PASS', name, label, count, flush=True)
            if name == 'yosys' and not four_state:
                config = directory/'carry.vlt'; config.write_text('`verilator_config\nsplit_var -module "CARRY4" -var "CO"\n')
                obj = directory/'obj'
                compile_command = [str(ROOT/'.cache/tools/usr/bin/verilator'), '--binary', '--timing', '--assert',
                    '-Wall', '-Wno-DECLFILENAME', '-Wno-UNUSEDSIGNAL', '--top-module', 'bench',
                    '-MAKEFLAGS', f'CXX={compiler} LINK={compiler}', '--Mdir', str(obj), str(config), str(model), str(fixture)]
                run(compile_command, directory/'verilator-compile.log',
                    env=dict(os.environ, VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')))
                run([str(obj/'Vbench')], directory/'verilator.log', marker=f'PASS {count} carry oracle comparisons')
                checks.append({'model': 'yosys-verilator-split-carry', 'mode': label, 'cases': count,
                               'command': compile_command, 'binary_sha256': digest(obj/'Vbench'),
                               'log': str((directory/'verilator.log').relative_to(ROOT))})
                for bit in range(8):
                    wrong = directory/f'flipped-output-{bit}.sv'; wrong.write_text(bench(trace,count,False,flip=1 << bit))
                    bad_binary = wrong.with_suffix('.vvp')
                    invoke = [str(wrong) if p == str(fixture) else str(bad_binary) if p == str(binary) else p for p in command]
                    run(invoke, wrong.with_suffix('.compile.log'))
                    run([str(ROOT/'.cache/tools/usr/bin/vvp'), str(bad_binary)], wrong.with_suffix('.log'),
                        expect_failure=True, marker='CARRY_ORACLE_MISMATCH')
                    controls.append('flipped-output-'+str(bit))
                if original.count('CI | CYINIT') != 2:
                    raise ValueError('unrecognized carry merge model')
                bad_model = directory/'wrong-carry-merge.v'; bad_model.write_text(original.replace('CI | CYINIT','CI & CYINIT')+'\n')
                bad_binary = directory/'wrong-carry-merge.vvp'
                invoke = [str(bad_model) if p == str(model) else str(bad_binary) if p == str(binary) else p for p in command]
                run(invoke, directory/'wrong-carry-merge-compile.log')
                run([str(ROOT/'.cache/tools/usr/bin/vvp'),str(bad_binary)], directory/'wrong-carry-merge.log',
                    expect_failure=True, marker='CARRY_ORACLE_MISMATCH')
                controls.append('wrong-carry-merge')
                ports = directory/'ports.sv'
                ports.write_text('module carry_ports(input [9:0] pins,output [7:0] observed);\n'+
                    'CARRY4 dut(.CO(observed[7:4]),.O(observed[3:0]),.CI(pins[0]),.CYINIT(pins[1]),.DI(pins[5:2]),.S(pins[9:6]));\nendmodule\n')
                for variant, circuit in [('ports', model), ('ports-wrong-merge', bad_model)]:
                    obj = directory/(variant+'-obj')
                    command = [str(ROOT/'.cache/tools/usr/bin/verilator'), '--cc', '--exe', '--build', '-j', '2',
                        '-Wall', '-Wno-DECLFILENAME', '-Wno-UNUSEDSIGNAL', '--top-module', 'carry_ports',
                        '-MAKEFLAGS', f'CXX={compiler} LINK={compiler}', '-CFLAGS', '-std=c++17 -Wall -Wextra -Werror',
                        '--Mdir', str(obj), str(config), str(circuit), str(ports), str(ROOT/'tests/xc7/carry.cpp')]
                    run(command, directory/(variant+'-compile.log'),
                        env=dict(os.environ, VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')))
                    run([str(obj/'Vcarry_ports'), str(trace)], directory/(variant+'.log'),
                        expect_failure=variant!='ports', marker='CARRY_ORACLE_MISMATCH' if variant!='ports' else
                        'PASS 11264 CARRY4 C++ input transitions')
                    if variant == 'ports':
                        checks.append({'model': 'yosys-verilator-cpp-ports', 'mode': label, 'cases': 11264,
                                       'command': command, 'binary_sha256': digest(obj/'Vcarry_ports'),
                                       'log': str((directory/'ports.log').relative_to(ROOT))})
                    else:
                        controls.append('wrong-carry-merge-cpp-ports')
    for name, value in inputs.items():
        if digest(ROOT/name) != value:
            raise ValueError('carry verification input changed: '+name)
    if digest(compiler) != compiler_identity['sha256']:
        raise ValueError('carry test compiler changed')
    artifacts = {str(p.relative_to(ROOT)):digest(p) for p in directory.rglob('*') if p.is_file()
                 and p.suffix in ('.sv','.v','.vlt','.ys','.txt','.log','.vvp')}
    report.write_text(json.dumps({'status': 'passed', 'inputs': inputs, 'artifacts': artifacts, 'compiler': compiler_identity,
        'binary_vendor_equivalence_proven': True, 'checks': checks, 'negative_controls_rejected': len(controls),
        'negative_controls': controls, 'four_state_vendor_equivalent': False, 'four_state_differences': differences,
        'limitations': ['Untimed functional primitive checks only.',
                        'Yosys ternary carry logic preserves some X/Z consensus that vendor gate logic does not.',
                        'Vendor CI/CYINIT inputs model pull-downs on Z; Yosys does not.'],
        'elapsed_seconds': time.monotonic()-started, 'physical_hardware_tested': False}, indent=2)+'\n')
    print('PASS carry checks; vendor/Yosys four-state differences explicitly retained')


if __name__ == '__main__':
    main()
