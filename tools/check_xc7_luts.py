#!/usr/bin/env python3
"""Prove every binary LUT table and check all X/Z selectors against an oracle."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

from prepare_standalone import ROOT, digest
from xc7_lut_model import fast_lut


def extract(text, name):
    matches = re.findall(r'\bmodule\s+'+name+r'\b.*?\bendmodule', text, re.S)
    if len(matches) != 1:
        raise ValueError('ambiguous LUT declaration: '+name)
    return re.sub(r'\bspecify\b.*?\bendspecify\b', '', matches[0], flags=re.S)


def variable_table(model, width, label):
    # Move only the constant parameter into a port so the proof quantifies over
    # every table. All original combinational expressions remain unchanged.
    model = model.replace('module LUT'+str(width), 'module '+label+str(width), 1)
    model = model.replace(');', f', input [{(1 << width)-1}:0] INIT);', 1)
    model, count = re.subn(r'parameter \['+str((1 << width)-1)+r':0\] INIT = 0;', '', model)
    if count != 1:
        raise ValueError('unrecognized LUT parameter declaration')
    return model


def possible_addresses(width, four_state):
    masks = []
    for selector in range((4 if four_state else 2)**width):
        if not four_state:
            masks.append(1 << selector)
            continue
        fixed = [(selector >> (2*i)) & 3 for i in range(width)]
        masks.append(sum(1 << address for address in range(1 << width)
                         if all(pin >= 2 or ((address >> i) & 1) == pin for i, pin in enumerate(fixed))))
    return masks


def oracle(table, masks):
    # All possible known addresses must agree on the same four-state symbol.
    symbols = {symbol: sum(1 << i for i, value in enumerate(reversed(table)) if value == symbol)
               for symbol in '01z'}
    return ''.join(next((symbol for symbol, bits in symbols.items() if mask & bits == mask), 'x')
                   for mask in reversed(masks))


def run(command, log, *, expect_failure=False, marker=None, env=None):
    with log.open('w') as stream:
        result = subprocess.run(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, env=env, timeout=1200)
    text = log.read_text()
    if (result.returncode == 0) == expect_failure or marker is not None and marker not in text:
        raise ValueError('unexpected verification outcome: '+str(log))


def bench(width, tables, four_state, vectors):
    count = (4 if four_state else 2)**width
    connections = ','.join(f'.I{i}(pins[{i}])' for i in range(width))
    select = ("case ((j >> (2*k)) & 3)\n0:pins[k]=0;1:pins[k]=1;2:pins[k]=1'bx;3:pins[k]=1'bz;endcase"
              if four_state else 'pins[k]=j[k];')
    return f'''module bench;
reg [{(1 << width)-1}:0] scan_table, table_value;
reg [{count-1}:0] expected;
reg [{width-1}:0] pins;
wire original_value,candidate_value;
original{width} u0(.O(original_value),{connections},.INIT(table_value));
candidate{width} u1(.O(candidate_value),{connections},.INIT(table_value));
integer fd,i,j,k,n,extra;
initial begin
 fd=$fopen("{vectors}","r");
 if(fd==0)$fatal(1,"LUT_TRACE_OPEN_FAILED");
 for(i=0;i<{len(tables)};i=i+1)begin
  n=$fscanf(fd,"%b %b",scan_table,expected);
  if(n!=2)$fatal(1,"LUT_TRACE_TRUNCATED");
  table_value=scan_table;
  for(j=0;j<{count};j=j+1)begin
   for(k=0;k<{width};k=k+1)begin {select} end
   #1;
   if(original_value!==expected[j] || candidate_value!==expected[j])
    $fatal(1,"LUT_ORACLE_MISMATCH table=%b pins=%b expected=%b original=%b candidate=%b",table_value,pins,expected[j],original_value,candidate_value);
  end
 end
 n=$fscanf(fd,"%s",extra);
 if(n!=-1 && !(n==0 && $feof(fd)))$fatal(1,"LUT_TRACE_EXTRA_DATA");
 $fclose(fd);
 $display("PASS {len(tables)*count} LUT{width} oracle comparisons per model");
 $finish;
end
endmodule
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--netlist', action='append', type=Path)
    parser.add_argument('--top', choices=['wasmetal_loadable','wasmetal_core'], default='wasmetal_loadable')
    parser.add_argument('--directory', type=Path, default=ROOT/'build/xc7-lut-check')
    parser.add_argument('--report', type=Path, default=ROOT/'reports/xc7-luts.json')
    args = parser.parse_args()
    netlists = args.netlist or [ROOT/'build/xc7-system/mapped.json']
    directory = args.directory.resolve();report = args.report.resolve()
    if ROOT/'build' not in directory.parents or ROOT/'reports' not in report.parents:
        parser.error('use a build subdirectory and a report inside reports/')
    if any(directory in path.resolve().parents or report==path.resolve() for path in netlists):
        parser.error('verification outputs must be separate from input netlists')
    directory.mkdir(parents=True, exist_ok=True);report.parent.mkdir(parents=True,exist_ok=True)
    report.unlink(missing_ok=True)
    started = time.monotonic()
    library = ROOT/'.cache/tools/usr/share/yosys/xilinx/cells_sim.v'
    yosys = ROOT/'.cache/tools/usr/bin/yosys'
    iverilog = ROOT/'.cache/tools/usr/bin/iverilog'
    vvp = ROOT/'.cache/tools/usr/bin/vvp'
    verilator = ROOT/'.cache/tools/usr/bin/verilator'
    dependencies = [Path(__file__).resolve(), ROOT/'tools/xc7_lut_model.py', ROOT/'tools/prepare_standalone.py',
                    library, yosys, iverilog, vvp, verilator, ROOT/'.cache/tools/usr/bin/verilator_bin', *netlists]
    dependencies += [p for p in sorted((ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl').glob('*')) if p.is_file()]
    dependencies += [p for p in sorted((ROOT/'.cache/tools/usr/share/verilator/include').rglob('*')) if p.is_file()]
    compiler = Path(shutil.which('g++')).resolve()
    compiler_identity = {'path': str(compiler), 'sha256': digest(compiler),
                        'version': subprocess.check_output([str(compiler), '--version'], text=True).splitlines()[0]}
    inputs = {str(p.resolve().relative_to(ROOT) if not p.is_symlink() and ROOT in p.resolve().parents
                  else p.relative_to(ROOT)): digest(p) for p in dependencies}
    source = library.read_text(); models = []; tables = {n: set() for n in range(1,7)}; inventories = []
    for path in netlists:
        cells = json.loads(path.read_text())['modules'][args.top]['cells']
        counts = {}
        for cell in cells.values():
            if re.fullmatch('LUT[1-6]', cell['type']) is None:
                continue
            width = int(cell['type'][-1]); value = cell['parameters']['INIT']
            if len(value) != 1 << width or set(value)-set('01'):
                raise ValueError('unexpected mapped LUT initialization')
            tables[width].add(value); counts[cell['type']] = counts.get(cell['type'], 0)+1
        if set(counts) != {'LUT'+str(n) for n in range(1,7)}:
            raise ValueError('incomplete whole-system LUT inventory')
        inventories.append({'path': str(path), 'sha256': digest(path), 'counts': counts})
    original_models = {}
    for width in range(1,7):
        name = 'LUT'+str(width); original = extract(source, name); original_models[width] = original
        models += [variable_table(original, width, 'original'),
                   variable_table(fast_lut(original, name), width, 'candidate')]
    model_path = directory/'models.sv'; model_path.write_text('\n'.join(models)+'\n')
    proof = directory/'equivalence.sv'
    body = ['module proof(input [63:0] table_value,input [5:0] pins,output mismatch);',
            'wire [5:0] a,b;']
    for width in range(1,7):
        pins = ','.join(f'.I{i}(pins[{i}])' for i in range(width))
        for label, value in [('original','a'), ('candidate','b')]:
            body.append(f'{label}{width} u_{label}{width}(.O({value}[{width-1}]),{pins},.INIT(table_value[{(1 << width)-1}:0]));')
    body += ['assign mismatch = |(a ^ b);', 'endmodule']
    proof.write_text(model_path.read_text()+'\n'.join(body)+'\n')
    script = directory/'equivalence.ys'
    script.write_text(f'read_verilog -sv {proof}\nprep -top proof\nflatten\nopt\nsat -verify -prove mismatch 0 -show-inputs\n')
    run([str(yosys), '-s', str(script)], directory/'equivalence.log', marker='SUCCESS!')
    controls = []
    for width in range(1,7):
        wrong, count = re.subn(r'(module candidate'+str(width)+r'\b.*?assign O = )(.*?);',
            lambda m: m[1]+'~('+m[2]+');', proof.read_text(), count=1, flags=re.S)
        if count != 1:
            raise ValueError('failed to inject LUT proof fault')
        negative = directory/f'negative-{width}.sv'; negative.write_text(wrong)
        ys = directory/f'negative-{width}.ys'; ys.write_text(script.read_text().replace(str(proof), str(negative)))
        run([str(yosys), '-s', str(ys)], directory/f'negative-{width}.log', expect_failure=True, marker='proof did fail')
        controls.append('inverted-LUT'+str(width))
    results = []
    for width in range(1,7):
        bits = 1 << width
        known = set(tables[width]) | {'0'*bits, '1'*bits}
        four = set(known) | {'x'*bits, 'z'*bits}
        for bit in range(bits):
            for background in '01':
                for symbol in 'xz':
                    value = list(background*bits); value[bit] = symbol; four.add(''.join(value))
        for label, values, four_state in [('known', sorted(known), False), ('four-state', sorted(four), True)]:
            case = directory/f'lut{width}-{label}'; case.mkdir(exist_ok=True)
            masks = possible_addresses(width, four_state)
            vectors = case/'oracle.txt'
            with vectors.open('w') as stream:
                for value in values:
                    stream.write(value+' '+oracle(value, masks)+'\n')
            fixture = case/'bench.sv'; fixture.write_text(bench(width, values, four_state, vectors))
            local_models = case/'models.sv'
            local_models.write_text('\n'.join([variable_table(original_models[width], width, 'original'),
                variable_table(fast_lut(original_models[width], 'LUT'+str(width)), width, 'candidate')])+'\n')
            binary = case/'bench.vvp'
            compile_command = [str(iverilog), '-B', str(ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl'),
                               '-g2012', '-s', 'bench', '-o', str(binary), str(local_models), str(fixture)]
            run(compile_command, case/'compile.log')
            marker = f'PASS {len(values)*len(masks)} LUT{width} oracle comparisons per model'
            run([str(vvp), str(binary)], case/'icarus.log', marker=marker)
            record = {'width': width, 'mode': label, 'tables': len(values), 'cases_per_model': len(values)*len(masks),
                      'icarus_passed': True, 'commands': [compile_command]}
            if not four_state:
                obj = case/'obj'
                command = [str(verilator), '--binary', '--timing', '--assert', '--top-module', 'bench',
                           '-Wall', '-Wno-DECLFILENAME', '-Wno-UNUSEDSIGNAL',
                           '-MAKEFLAGS', f'CXX={compiler} LINK={compiler}',
                           '--Mdir', str(obj), str(local_models), str(fixture)]
                run(command, case/'verilator-compile.log', env=dict(os.environ, VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')))
                run([str(obj/'Vbench')], case/'verilator.log', marker=marker)
                record['verilator_passed'] = True; record['commands'].append(command)
                record['verilator_binary_sha256'] = digest(obj/'Vbench')
            results.append(record)
            print('PASS', width, label, record['cases_per_model'], flush=True)
            if width == 2 and four_state:
                faulty, changed = re.subn(r'(module candidate2\b.*?assign O = )(.*?);',
                    lambda m: m[1]+'INIT[{I1,I0}];', local_models.read_text(), count=1, flags=re.S)
                if changed != 1:
                    raise ValueError('failed to inject unknown-selector fault')
                wrong_model = case/'unsafe-model.sv'; wrong_model.write_text(faulty)
                wrong_binary = case/'unsafe-model.vvp'
                command = [str(wrong_binary) if p == str(binary) else
                           str(wrong_model) if p == str(local_models) else p for p in compile_command]
                run(command, case/'unsafe-model-compile.log')
                run([str(vvp), str(wrong_binary)], case/'unsafe-model.log',
                    expect_failure=True, marker='LUT_ORACLE_MISMATCH')
                controls.append('unsafe-lookup-with-XZ-selectors')
                lines = vectors.read_text().splitlines(keepends=True)
                first = lines[0].rstrip('\n')
                mutations = [
                    ('wrong-oracle', first[:-1]+('1' if first[-1]=='0' else '0')+'\n'+''.join(lines[1:]), 'LUT_ORACLE_MISMATCH'),
                    ('truncated-trace', ''.join(lines[:-1]), 'LUT_TRACE_TRUNCATED'),
                    ('extra-trace', ''.join(lines)+'extra\n', 'LUT_TRACE_EXTRA_DATA'),
                    ('malformed-trace', 'invalid\n'+''.join(lines[1:]), 'LUT_TRACE_TRUNCATED')]
                for name, content, diagnostic in mutations:
                    wrong_vectors = case/(name+'.txt'); wrong_vectors.write_text(content)
                    wrong_fixture = case/(name+'.sv')
                    wrong_fixture.write_text(fixture.read_text().replace(str(vectors), str(wrong_vectors)))
                    wrong_binary = case/(name+'.vvp')
                    command = [str(wrong_binary) if p == str(binary) else
                               str(wrong_fixture) if p == str(fixture) else p for p in compile_command]
                    run(command, case/(name+'-compile.log'))
                    run([str(vvp), str(wrong_binary)], case/(name+'.log'), expect_failure=True, marker=diagnostic)
                    controls.append(name)
    for name, value in inputs.items():
        if digest(ROOT/name) != value:
            raise ValueError('LUT verification input changed: '+name)
    if digest(compiler) != compiler_identity['sha256']:
        raise ValueError('LUT test compiler changed')
    artifacts = {str(p.relative_to(ROOT)): digest(p) for p in directory.rglob('*') if p.is_file()
                 and p.suffix in ('.sv', '.ys', '.log', '.txt', '.vvp')}
    report.write_text(json.dumps({'status': 'passed', 'inputs': inputs, 'artifacts': artifacts, 'compiler': compiler_identity,
        'netlists': inventories, 'binary_equivalence_proven': True,
        'binary_proof_scope': 'All known INIT bits and selectors for LUT1 through LUT6',
        'negative_controls_rejected': len(controls), 'negative_controls': controls, 'checks': results,
        'known_cases_per_model': sum(x['cases_per_model'] for x in results if x['mode']=='known'),
        'four_state_cases_per_model': sum(x['cases_per_model'] for x in results if x['mode']=='four-state'),
        'four_state_scope': 'Every X/Z selector combination, all mapped tables, constant tables and single X/Z table bits',
        'elapsed_seconds': time.monotonic()-started, 'physical_hardware_tested': False}, indent=2)+'\n')
    print('PASS six LUT proofs and complete oracle regressions')


if __name__ == '__main__':
    main()
