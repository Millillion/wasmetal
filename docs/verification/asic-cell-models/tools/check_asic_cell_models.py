#!/usr/bin/env python3
"""Cross-check Liberty-derived cells against pinned upstream Verilog in Icarus."""
import argparse
import json
from pathlib import Path
import posixpath
import re
import subprocess
import time
import urllib.request

from asic_cells import filter_library, inputs, require, verify_bytes
from check_memory_startup import CONFIGURATIONS, TOP
from prepare_standalone import ROOT, digest


LOCK = ROOT / 'tools/asic_cell_models.lock.json'
CACHE = ROOT / '.cache/sky130hd-vendor'
BASE = ROOT / 'build/asic-cell-models'


def upstream():
    lock = json.loads(LOCK.read_text())
    require(lock['schema_version'] == 1 and re.fullmatch('[0-9a-f]{40}', lock['revision']),
            'unpinned upstream cell models')
    names = [record['path'] for record in lock['files']]
    require(len(names) == len(set(names)), 'duplicate upstream model file')
    types = lock['cell_types']
    require(types == sorted(set(types)) and all(re.fullmatch(r'sky130_fd_sc_hd__[a-z0-9_]+_[0-9]+', n) for n in types),
            'invalid or duplicate upstream cell type')
    required = {'cells/' + name.split('__')[1].rsplit('_', 1)[0] + '/' + name + '.functional.v' for name in types}
    require({name for name in names if name.startswith('cells/')} == required and 'LICENSE' in names,
            'cell source/license inventory is incomplete or unexpected')
    for record in lock['files']:
        relative = Path(record['path'])
        require(not relative.is_absolute() and '..' not in relative.parts, 'unsafe model source path')
        path = CACHE / relative
        if not path.exists():
            url = 'https://raw.githubusercontent.com/' + '/'.join([lock['repository'], lock['revision'], record['path']])
            with urllib.request.urlopen(url, timeout=60) as response:
                data = response.read(record['bytes'] + 1)
            verify_bytes(data, record)
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary = path.with_name(path.name + '.download')
            temporary.write_bytes(data)
            temporary.replace(path)
        verify_bytes(path.read_bytes(), record)
        require(not re.search(r'\$(system|fopen|readmem[hb]|fwrite|fdisplay)\b', path.read_text()),
                'unexpected executable/file operation in a functional cell model')
        text = path.read_text()
        for include in re.findall(r'^`include "([^"]+)"', text, re.M):
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(record['path']), include))
            if include.endswith('.blackbox.v'):
                require('`ifdef NO_PRIMITIVES\n`include "' + include + '"' in text,
                        'unguarded primitive black-box include')
            else:
                require(resolved in names, 'unbound transitive model include: ' + resolved)
    return lock


def execute(command, log, accepted_failure=False):
    with log.open('w') as stream:
        run = subprocess.run(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, timeout=120)
    require(accepted_failure or run.returncode == 0, 'cell-model check failed; see ' + str(log))
    return run.returncode


def module_bodies(text, prefix=''):
    pattern = r'\bmodule\s+(' + re.escape(prefix) + r'sky130_fd_sc_hd__[A-Za-z0-9_]+)\s*\(.*?\bendmodule\b'
    records = {}
    for match in re.finditer(pattern, text, re.S):
        name = match.group(1)
        require(name not in records, 'duplicate cell model declaration')
        records[name] = match.group()
    return records


def mapped_models(path, types):
    report = json.loads(path.read_text())
    require(report['status'] == 'passed' and report['backend'] == 'mapped-sky130hd-functional',
            'completed SKY130 mapping report required')
    configurations = [(c['ram_bytes'], c['read_latency'], c['response_timeout']) for c in report['checks']]
    require(len(configurations) == len(CONFIGURATIONS) and set(configurations) == set(CONFIGURATIONS),
            'complete ASIC configuration matrix required')
    models, paths = {}, [path.resolve()]
    for check in report['checks']:
        size, latency, timeout = check['ram_bytes'], check['read_latency'], check['response_timeout']
        directory = ROOT / 'build/asic-startup' / f'{size}-{latency}-{timeout}'
        netlist, source = directory / 'mapped.json', directory / 'cells.v'
        require(digest(netlist) == check['netlist_sha256'] and digest(source) == check['functional_models_sha256'],
                'changed mapped circuit or functional model source')
        module = json.loads(netlist.read_text())['modules'][TOP]
        selected = {c['type'] for c in module['cells'].values()}
        bodies = module_bodies(source.read_text())
        require(selected == set(check['standard_cells']) == set(bodies), 'mapped cell-model inventory mismatch')
        require(selected <= set(types), 'mapped circuit uses an unverified vendor cell type')
        for name, body in bodies.items():
            require(name not in models or models[name] == body, 'inconsistent cell definitions across ASIC configurations')
            models[name] = body
        paths.extend([source, netlist])
    return models, paths


def bench(types, library, directory):
    sources, chunks, vectors = [], ['`timescale 1ns/1ps\n'], 0
    require(types == sorted(set(types)), 'cell model inventory must be unique and sorted')
    for index, kind in enumerate(types):
        family = kind.split('__')[1].rsplit('_', 1)[0]
        source = CACHE / 'cells' / family / (kind + '.functional.v')
        text = source.read_text()
        sources.append(source)
        module = library[kind]
        ports = module['ports']
        declared = {name: direction for direction, name in re.findall(
            r'^\s*(input|output)\s+wire\s+(\w+)\s*;', text, re.M)}
        require(declared == {name: p['direction'] for name, p in ports.items()}, 'vendor port inventory mismatch: ' + kind)
        require(all(len(p['bits']) == 1 for p in ports.values()), 'unsupported multibit standard-cell port')
        sequential = [c['type'] for c in module['cells'].values()
                      if 'dff' in c['type'].lower() or 'latch' in c['type'].lower()]
        head = f'module cell_check_{index}(output reg done);\n'
        if kind == 'sky130_fd_sc_hd__dfxtp_1':
            require(sequential == ['$_DFF_P_'], 'unexpected Liberty flip-flop model')
            chunks.append(head + f'''reg d=0,clk=0;wire vendor_q,derived_q;reg expected;integer seed,prior,following;
{kind} vendor(.D(d),.CLK(clk),.Q(vendor_q));
derived__{kind} derived(.D(d),.CLK(clk),.Q(derived_q));
initial begin
 done=0;
 for(seed=0;seed<2;seed=seed+1) for(prior=0;prior<4;prior=prior+1) for(following=0;following<4;following=following+1) begin
  clk=0;d=seed[0];#1;clk=1;#1;
  if(vendor_q!==seed[0] || derived_q!==seed[0]) $fatal(1,"DFF seed mismatch");
  d=prior[0];clk=prior[1];#1;
  if(vendor_q!==seed[0] || derived_q!==seed[0]) $fatal(1,"DFF pretransition hold mismatch");
  d=following[0];clk=following[1];#1;
  expected=(!prior[1] && following[1]) ? following[0] : seed[0];
  if(vendor_q!==expected || derived_q!==expected) $fatal(1,"DFF binary transition mismatch");
 end
 done=1;
end
endmodule
''')
            continue
        require(not sequential, 'unsupported stateful standard cell: ' + kind)
        ins = sorted(name for name, p in ports.items() if p['direction'] == 'input')
        outs = sorted(name for name, p in ports.items() if p['direction'] == 'output')
        require(outs and len(ins) <= 12, 'unexpected combinational cell interface')
        vectors += 2 ** len(ins)
        vendor = [f'.{pin}(stimulus[{i}])' for i, pin in enumerate(ins)]
        derived = vendor.copy()
        vendor += [f'.{pin}(vendor_q[{i}])' for i, pin in enumerate(outs)]
        derived += [f'.{pin}(derived_q[{i}])' for i, pin in enumerate(outs)]
        chunks.append(head + f'reg [{max(len(ins),1)-1}:0] stimulus=0;wire [{len(outs)-1}:0] vendor_q,derived_q;integer pattern;\n' +
                      kind + ' vendor(' + ','.join(vendor) + ');\n' +
                      'derived__' + kind + ' derived(' + ','.join(derived) + ');\n' + f'''initial begin
 done=0;
 for(pattern=0;pattern<{2**len(ins)};pattern=pattern+1) begin
  stimulus=pattern;#1;
  if((^vendor_q===1'bx) || (^derived_q===1'bx) || vendor_q!==derived_q) $fatal(1,"{kind} binary truth table mismatch at %0d",pattern);
 end
 done=1;
end
endmodule
''')
    require('sky130_fd_sc_hd__dfxtp_1' in types, 'missing sequential-cell coverage')
    chunks.append(f'module testbench;wire [{len(types)-1}:0] done;\n')
    chunks.extend(f'cell_check_{n} check_{n}(.done(done[{n}]));\n' for n in range(len(types)))
    marker = f'PASS {len(types)} cell types; {vectors} combinational vectors; 32 binary DFF transitions; 64 seed/hold checks'
    chunks.append(f'initial begin wait(&done);#1;$display("{marker}");$finish;end\n' +
                  'initial begin #10000;$fatal(1,"vendor comparison timeout");end\nendmodule\n')
    (directory / 'testbench.sv').write_text(''.join(chunks))
    return sources, vectors, marker


def simulation(source, label, vendor, marker, failure=None):
    binary = BASE / (label + '.vvp')
    command = [str(ROOT / '.cache/tools/usr/bin/iverilog'),
        '-B' + str(ROOT / '.cache/tools/usr/lib/x86_64-linux-gnu/ivl'),
        '-g2012', '-grelative-include', '-DUNIT_DELAY=', '-s', 'testbench', '-o', str(binary),
        str(BASE / 'testbench.sv'), str(source), *map(str, vendor)]
    execute(command, BASE / (label + '-compile.log'))
    logfile = BASE / (label + '.log')
    result = execute([str(ROOT / '.cache/tools/usr/bin/vvp'), str(binary)], logfile, accepted_failure=bool(failure))
    text = logfile.read_text()
    require((result != 0 and failure in text and marker not in text) if failure else (result == 0 and marker in text),
            'unexpected vendor-model comparison outcome: ' + label)
    return {'binary_sha256': digest(binary), 'source_sha256': digest(source),
            'log_sha256': digest(logfile), 'compile_command': command}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--asic-report', type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    BASE.mkdir(parents=True, exist_ok=True)
    output = ROOT / 'reports/asic-cell-models.json'
    output.parent.mkdir(exist_ok=True)
    output.unlink(missing_ok=True)
    lock = upstream()
    library_files = inputs()
    library, filtering = filter_library(library_files, BASE / 'filtered')
    types = lock['cell_types']
    paths = [LOCK, ROOT / 'tools/asic_cells.lock.json', Path(__file__).resolve(), ROOT / 'tools/asic_cells.py',
             ROOT / 'tools/prepare_standalone.py', ROOT / 'tools/check_memory_startup.py',
             ROOT / 'tools/upstream.lock.json', *library_files.values(),
             library, BASE / 'filtered/filter.json',
             *[CACHE / record['path'] for record in lock['files']],
             *[ROOT / '.cache/tools/usr/bin' / name for name in ('yosys', 'iverilog', 'vvp')],
             *[ROOT / '.cache/tools/usr/lib/x86_64-linux-gnu/ivl' / name for name in ('ivl', 'ivlpp')]]
    actual_models = {}
    if args.asic_report:
        actual_models, actual_paths = mapped_models(args.asic_report, types)
        paths.extend(actual_paths)
    bound = {str(path.relative_to(ROOT)): digest(path) for path in paths}
    script = f'read_liberty -ignore_miss_func -ignore_miss_dir -ignore_miss_data_latch {library}\n'
    script += f'write_json {BASE}/library.json\n'
    script += ''.join(f'rename {kind} derived__{kind}\n' for kind in types)
    script += 'select -clear\nselect ' + ' '.join('derived__' + kind for kind in types)
    script += f'\nwrite_verilog -selected -noattr {BASE}/derived.v\n'
    (BASE / 'models.ys').write_text(script)
    execute([str(ROOT / '.cache/tools/usr/bin/yosys'), '-Q', '-T', '-s', str(BASE / 'models.ys')], BASE / 'models.log')
    library = json.loads((BASE / 'library.json').read_text())['modules']
    vendor, vectors, marker = bench(types, library, BASE)
    source = BASE / 'derived.v'
    if actual_models:
        # Replace each used cell with the exact definition from the mapped
        # simulator. Only its module name changes to avoid colliding with the
        # independent upstream definition. No logic or signal names are edited.
        fresh = module_bodies(source.read_text(), 'derived__')
        require(set(fresh) == {'derived__' + name for name in types}, 'derived cell inventory mismatch')
        for name, body in actual_models.items():
            changed, count = re.subn(r'\bmodule\s+' + re.escape(name) + r'\b', 'module derived__' + name, body)
            require(count == 1, 'ambiguous mapped cell-model rename')
            fresh['derived__' + name] = changed
        source.write_text('/* Actual mapped definitions: module names alone are prefixed. */\n' +
                          '\n\n'.join(fresh['derived__' + name] for name in types) + '\n')
    positive = simulation(source, 'positive', vendor, marker)
    controls = []
    original = source.read_text()
    for label, old, new, failure in [
        ('wrong-tie-high', "assign HI = 1'h1;", "assign HI = 1'h0;", 'sky130_fd_sc_hd__conb_1 binary truth table mismatch'),
        ('wrong-clock-edge', 'always @(posedge CLK)', 'always @(negedge CLK)', 'DFF')]:
        require(original.count(old) == 1, 'ambiguous standard-cell mutation: ' + label)
        mutant = BASE / (label + '.v')
        mutant.write_text(original.replace(old, new))
        controls.append({'name': label, **simulation(mutant, label, vendor, marker, failure)})
    match = re.search(r'(module derived__sky130_fd_sc_hd__and2_0\b.*?endmodule)', original, re.S)
    require(match is not None, 'missing AND-cell fault target')
    body, count = re.subn(r'(assign X\s*=\s*)([^;]+)(;)', r'\1~(\2)\3', match.group(), count=1)
    require(count == 1, 'ambiguous AND-cell output')
    mutant = BASE / 'wrong-and-output.v'
    mutant.write_text(original[:match.start()] + body + original[match.end():])
    controls.append({'name': 'wrong-and-output', **simulation(mutant, 'wrong-and-output', vendor, marker,
                     'sky130_fd_sc_hd__and2_0 binary truth table mismatch')})
    for name, sha in bound.items():
        require(digest(ROOT / name) == sha, 'cell-model verification input changed: ' + name)
    result = {'status': 'passed', 'scope': 'binary functional cell behavior only', 'cell_types': types,
              'cell_type_count': len(types), 'combinational_vectors': vectors, 'flip_flop_transitions': 32,
              'flip_flop_seed_and_hold_checks': 64, 'upstream_repository': lock['repository'],
              'upstream_revision': lock['revision'], 'inputs': bound, 'positive': positive,
              'library_filter': filtering,
              'testbench_sha256': digest(BASE / 'testbench.sv'), 'negative_controls': controls,
              'negative_controls_rejected': len(controls), 'mapped_types_checked': sorted(actual_models),
              'elapsed_seconds': time.monotonic() - started,
              'limitations': ['No timing, analog, power-pin or unknown-clock/data equivalence is claimed.',
                  'The flip-flop is seeded by a clock edge; no power-on state is assumed.',
                  'The upstream primitive tables are enabled; no black-box cell models are used.']}
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(marker + f'; {len(controls)} deliberate model faults rejected')


if __name__ == '__main__':
    main()
