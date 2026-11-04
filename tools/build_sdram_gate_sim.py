#!/usr/bin/env python3
"""Compile SDR controller pins after checking the mapped combinational graph."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from build_board import yosys
from build_gate_sim import compilation
from build_standalone_gate_sim import models,normalize
from prepare_standalone import ROOT,digest


def build(netlist,directory,harness,cflags):
    top='wasmetal_sdram_memory';directory.mkdir(parents=True,exist_ok=True)
    receipt=directory/'obj'/('V'+top+'.build.json');receipt.unlink(missing_ok=True)
    manifest_path=netlist.with_suffix('.manifest.json');manifest=json.loads(manifest_path.read_text())
    if digest(netlist)!=manifest['netlist_sha256']:raise ValueError('SDRAM circuit identity mismatch')
    library=ROOT/'.cache/tools/usr/share/yosys/ecp5/cells_sim.v'
    paths=[netlist,manifest_path,harness,library,Path(__file__).resolve(),ROOT/'tools/build_board.py',
        ROOT/'tools/build_gate_sim.py',ROOT/'tools/build_standalone_gate_sim.py',ROOT/'tools/prepare_standalone.py',
        ROOT/'tools/ecp5_ram.py',ROOT/'tools/ecp5_standalone_ram.py',ROOT/'tools/ecp5_loadable_ram.py',
        ROOT/'tools/check_ecp5_luts.py',ROOT/'tools/upstream.lock.json']
    hashes={**manifest['inputs'],**{str(p.relative_to(ROOT)):digest(p) for p in paths}}
    for name,value in hashes.items():
        if digest(ROOT/name)!=value:raise ValueError('stale SDRAM input: '+name)
    source=json.loads(netlist.read_text())
    if normalize(source,top):raise ValueError('SDRAM controller unexpectedly contains embedded RAM')
    normalized=directory/'normalized.json';normalized.write_text(json.dumps(source))
    yosys(f'read_json {normalized}\nsplitnets\nclean -purge\ncheck -assert\n'
        f'write_verilog -noattr {directory}/circuit.v\n','export',directory)
    subprocess.run([sys.executable,str(ROOT/'tools/check_ecp5_luts.py'),'--top',top,
        '--core-netlist',str(netlist),'--directory',str(directory/'lut-proof')],check=True)
    (directory/'cells.v').write_text(models(library))
    # A shared output bit can feed another bit of the same public port vector.
    # Check the bit-level graph before permitting this one vector-scheduling
    # warning; Verilator 5.020 cannot split a public port with split_var.
    yosys(f'read_verilog -sv {directory}/cells.v {directory}/circuit.v\n'
        f'hierarchy -top {top}\nproc\nflatten\nopt\nscc -expect 0\ncheck -assert\n','acyclic',directory)
    config='`verilator_config\n'+''.join(
        f'lint_off -rule {rule} -file "{directory}/{name}"\n'
        for name,rules in [('circuit.v',['DECLFILENAME','PINCONNECTEMPTY']),
            ('cells.v',['DECLFILENAME','INITIALDLY','GENUNNAMED','UNUSEDPARAM','WIDTHEXPAND','SYNCASYNCNET'])]
        for rule in rules)
    probe=directory/'cycle-probe.sv'
    probe.write_text('module cycle_probe(input wire toggle,output wire result);\n'
        'wire feedback;assign feedback=result;assign result=feedback^toggle;\nendmodule\n')
    probe_script=directory/'cycle-probe.ys';probe_log=directory/'cycle-probe.log'
    probe_script.write_text(f'read_verilog {probe}\nprep -top cycle_probe\nscc -expect 0\n')
    with probe_log.open('w') as log:
        negative=subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-Q','-T','-s',str(probe_script)],
            stdout=log,stderr=subprocess.STDOUT)
    if negative.returncode==0 or 'Found 1 SCCs but expected 0' not in probe_log.read_text():
        raise ValueError('combinational-cycle audit did not reject its negative control')
    config+=f'lint_off -rule UNOPTFLAT -file "{directory}/circuit.v" '+\
        '-match "*Circular combinational logic: \'sdram_address\'*"\n'
    (directory/'vendor.vlt').write_text(config)
    options=compilation(True,True);flags=options['cflags']+' '+cflags
    obj=directory/'obj';binary=obj/('V'+top)
    command=[str(ROOT/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL',
        '--top-module',top,'--cc','--exe','--output-split','10000','--output-split-cfuncs','10000',
        '--Mdir',str(obj),'-CFLAGS',flags,str(directory/'vendor.vlt'),str(directory/'cells.v'),
        str(directory/'circuit.v'),str(harness)]
    env=dict(os.environ,VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator'))
    make=['make','-C',str(obj),'-f','V'+top+'.mk','-j','2','CXX='+options['compiler'],
        'LINK='+options['compiler'],'VM_USER_CFLAGS='+flags,'OPT_FAST=-O3','OPT_SLOW=-O3','OPT_GLOBAL=-O3']
    with (directory/'build.log').open('w') as log:
        subprocess.run(command,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
        for p in obj.glob('V*.cpp'):
            old=p.read_text()
            body=re.sub(r'^(?:#pragma GCC diagnostic ignored "-(?:Wint-in-bool-context|Wbool-operation)"\n)+','',old)
            text='#pragma GCC diagnostic ignored "-Wint-in-bool-context"\n#pragma GCC diagnostic ignored "-Wbool-operation"\n'+body
            if text!=old:p.write_text(text)
        subprocess.run(make,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
    for name,value in hashes.items():
        if digest(ROOT/name)!=value:raise ValueError('SDRAM model input changed: '+name)
    hashes.update({str(p.relative_to(ROOT)):digest(p) for p in [directory/'circuit.v',directory/'cells.v',
        directory/'vendor.vlt',directory/'acyclic.ys',directory/'acyclic.log',directory/'lut-proof/report.json',
        normalized,probe,probe_script,probe_log]})
    record={'backend':'sdram-mapped-ecp5-functional','top':top,'inputs':hashes,
        'binary_sha256':digest(binary),'netlist_sha256':digest(netlist),'compilation':options,
        'verilator_command':command,'compiler_command':make,'combinational_cycles':0,
        'cyclic_negative_control_rejected':True,
        'warning_waiver':{'rule':'UNOPTFLAT','signal':'sdram_address',
            'basis':'zero bit-level combinational cycles; public-vector scheduling only'},
        'physical_hardware_tested':False}
    receipt.write_text(json.dumps(record,indent=2)+'\n')
    return binary
