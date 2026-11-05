#!/usr/bin/env python3
"""Check used 7-series flip-flops against independent event/state oracles."""
import argparse
from copy import deepcopy
import hashlib
import itertools
import json
import os
from pathlib import Path
import random
import re
import shutil
import subprocess
import time

from check_xc7_luts import extract, run
from prepare_standalone import ROOT, digest

KINDS = ('FDRE', 'FDRE_1', 'FDSE', 'FDCE')


def audit(module):
    counts = {kind:0 for kind in KINDS}
    for cell in module['cells'].values():
        kind = cell['type']
        if kind not in counts:
            continue
        control = 'CLR' if kind == 'FDCE' else 'S' if kind == 'FDSE' else 'R'
        allowed = {'INIT'} if kind == 'FDRE_1' else {'INIT','IS_C_INVERTED','IS_D_INVERTED','IS_'+control+'_INVERTED'}
        for name, value in cell['parameters'].items():
            if name not in allowed or (name == 'INIT' and value not in ('0','1','x')) or (name != 'INIT' and int(value,2) != 0):
                raise ValueError('unreviewed flip-flop parameter: '+kind+'.'+name)
        pins = {'C','CE','D',control,'Q'}
        if set(cell['connections']) != pins or any(len(v) != 1 for v in cell['connections'].values()):
            raise ValueError('unreviewed flip-flop ports: '+kind)
        counts[kind] += 1
    if not all(counts.values()):
        raise ValueError('incomplete mapped flip-flop inventory')
    return counts


def posedge(old, new):
    return old == '0' and new in '1xz' or old in 'xz' and new == '1'


def transition(kind, state, old, new, vendor):
    clock, control, enable, data = new
    active_edge = old[0] == ('1' if kind == 'FDRE_1' else '0') and clock == ('0' if kind == 'FDRE_1' else '1')
    sampled = data if kind == 'FDRE_1' and not vendor else data if data in '01' else 'x'
    enabled = enable == '1' or vendor and enable == 'z'
    if kind == 'FDCE':
        if vendor:
            # The vendor model continuously forces Q while CLR is one or X.
            # Z is treated as a deasserted clear. Clock inputs stay binary.
            if control == '1': return '0'
            if control == 'x': return 'x'
            event = active_edge
        else:
            event = active_edge or posedge(old[1], control)
        if event:
            if control == '1': return '0'
            if enabled: return sampled
    elif active_edge:
        reset_value = '1' if kind == 'FDSE' else '0'
        if control == '1' or vendor and control == 'x' and state == reset_value:
            return reset_value
        if enabled: return sampled
    return state


def vectors(path, kind, initial, four_state, known_clear=False):
    symbols = '01xz' if four_state else '01'
    clear_symbols = '01' if known_clear else symbols
    vendor_supported = not (kind == 'FDCE' and four_state and not known_clear)
    old = '0000'; states = [initial,initial]; count = 0; differences = 0; examples = []
    idle = '1' if kind == 'FDRE_1' else '0'; active = '0' if idle == '1' else '1'
    with path.open('w') as stream:
        def emit(clock, control, enable, data):
            nonlocal old, states, count, differences
            new = clock+control+enable+data
            previous = list(states)
            states = [transition(kind,states[0],old,new,False),
                      transition(kind,states[1],old,new,True) if vendor_supported else 'x']
            stream.write(new+' '+states[0]+' '+states[1]+'\n')
            if vendor_supported and states[0] != states[1]:
                differences += 1
                if len(examples) < 8:
                    examples.append({'old_pins':old,'pins':new,'old_states':previous,'states':list(states)})
            old = new; count += 1

        # Establish each prior data state through real pins, then cover every
        # old/new binary clock and every control/enable/data combination.
        for prior, old_clock, new_clock, control, enable, data in itertools.product(symbols,'01','01',clear_symbols,symbols,symbols):
            emit(idle,'0','1',prior); emit(active,'0','1',prior)
            emit(old_clock,'0','0','0')
            emit(old_clock,control,enable,data)
            emit(new_clock,control,enable,data)
        rng = random.Random(0xFDCED00D)
        for _ in range(2048):
            clock = rng.choice('01'); controls = [rng.choice(clear_symbols),rng.choice(symbols),rng.choice(symbols)]
            # Settle data/control aliases before changing the clock. This is
            # an untimed state check, not a setup/hold violation experiment.
            emit(old[0],*controls)
            emit(clock,*controls)
    if not four_state and differences:
        raise ValueError('binary flip-flop oracles disagree')
    return count, differences, examples


def bench(kind, initial, trace, count, vendor=False):
    model = 'FDRE' if vendor and kind == 'FDRE_1' else kind
    extra = ",.IS_C_INVERTED(1'b1)" if vendor and kind == 'FDRE_1' else ''
    control = 'CLR' if kind == 'FDCE' else 'S' if kind == 'FDSE' else 'R'
    return f'''`timescale 1ps/1ps
module glbl;
reg GSR=1'b0;
initial begin #100 GSR=1'b1; #1000 GSR=1'b0; end
endmodule
module bench;
reg [3:0] pins=0,next_pins;
reg expected_yosys,expected_vendor;
wire observed;
{model} #(.INIT(1'b{initial}){extra}) dut(.Q(observed),.C(pins[3]),.{control}(pins[2]),.CE(pins[1]),.D(pins[0]));
integer fd,j,n,extra;
initial begin
 #2000;
 if(observed!==1'b{initial})$fatal(1,"FLOP_INIT_MISMATCH observed=%b",observed);
 fd=$fopen("{trace}","r");if(fd==0)$fatal(1,"FLOP_TRACE_OPEN_FAILED");
 for(j=0;j<{count};j=j+1)begin
  n=$fscanf(fd,"%b %b %b",next_pins,expected_yosys,expected_vendor);
  if(n!=3)$fatal(1,"FLOP_TRACE_TRUNCATED_OR_MALFORMED");
  pins=next_pins;
  #1000;
  if(observed!=={'expected_vendor' if vendor else 'expected_yosys'})
   $fatal(1,"FLOP_ORACLE_MISMATCH row=%0d pins=%b observed=%b yosys=%b vendor=%b",j,pins,observed,expected_yosys,expected_vendor);
 end
 n=$fscanf(fd,"%s",extra);
 if(n!=-1 && !(n==0 && $feof(fd)))$fatal(1,"FLOP_TRACE_EXTRA_DATA");
 $fclose(fd);$display("PASS {count} flip-flop transitions");$finish;
end
endmodule
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--netlist',type=Path,action='append')
    parser.add_argument('--top',choices=['wasmetal_loadable','wasmetal_core'],default='wasmetal_loadable')
    args = parser.parse_args(); netlists = args.netlist or [ROOT/'build/xc7-system/mapped.json']
    netlists = [p if p.is_absolute() else ROOT/p for p in netlists]
    directory = ROOT/'build/xc7-flops'; directory.mkdir(parents=True,exist_ok=True)
    report = ROOT/'reports/xc7-flops.json'; report.unlink(missing_ok=True); started = time.monotonic()
    library = ROOT/'.cache/tools/usr/share/yosys/xilinx/cells_sim.v'
    vendor_dir = ROOT/'third_party/xilinx-unisim'; vendor_sources = {}
    dependencies = [Path(__file__).resolve(),ROOT/'tools/check_xc7_luts.py',ROOT/'tools/prepare_standalone.py',
                    library,vendor_dir/'LICENSE',vendor_dir/'UPSTREAM.json',*netlists]
    for kind in ('FDRE','FDSE','FDCE'):
        source = vendor_dir/(kind+'.v'); pin_path = vendor_dir/(kind+'.UPSTREAM.json')
        pin = json.loads(pin_path.read_text()); data = source.read_bytes()
        if digest(source) != pin['sha256'] or len(data) != pin['bytes'] or hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() != pin['git_blob_sha']:
            raise ValueError('vendor flip-flop source changed: '+kind)
        dependencies += [source,pin_path]; vendor_sources[kind] = source
    dependencies += [ROOT/'.cache/tools/usr/bin'/n for n in ('iverilog','vvp','verilator','verilator_bin')]
    dependencies += [p for p in sorted((ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl').glob('*')) if p.is_file()]
    dependencies += [p for p in sorted((ROOT/'.cache/tools/usr/share/verilator/include').rglob('*')) if p.is_file()]
    inputs = {str(p.relative_to(ROOT)):digest(p) for p in dependencies}
    compiler = Path(shutil.which('g++')).resolve()
    compiler_identity = {'path':str(compiler),'sha256':digest(compiler),
                         'version':subprocess.check_output([str(compiler),'--version'],text=True).splitlines()[0]}
    inventories = []; controls = []
    for path in netlists:
        module = json.loads(path.read_text())['modules'][args.top]
        inventories.append({'path':str(path),'sha256':digest(path),'counts':audit(module)})
        for name, change in (
            ('clock-inversion',lambda c:c['parameters'].update(IS_C_INVERTED='1')),
            ('unsupported-initial-state',lambda c:c['parameters'].update(INIT='z')),
            ('extra-parameter',lambda c:c['parameters'].update(UNREVIEWED='1')),
            ('wrong-port-width',lambda c:c['connections']['D'].append('0'))):
            wrong = {'cells':deepcopy({k:c for k,c in module['cells'].items() if c['type'] in KINDS})}
            cell = next(c for c in wrong['cells'].values() if c['type']=='FDRE'); change(cell)
            try: audit(wrong)
            except ValueError:controls.append({'name':name,'netlist':str(path),'rejected':True})
            else:raise ValueError('inventory accepted '+name)
    original = library.read_text(); notice = original[:re.search(r'^module\b',original,re.M).start()]
    checks = []; differences = []; fixtures = {}
    generated = set()
    def write(path, text):
        path.write_text(text); generated.add(path)
    def execute(command, log, **kwargs):
        run(command,log,**kwargs); generated.add(log)
    env = dict(os.environ,VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator'))
    ivl = ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl'

    def simulate(fixture, source, log, failure=False, marker=None):
        binary = log.with_suffix('.vvp')
        command = [str(ROOT/'.cache/tools/usr/bin/iverilog'),'-B',str(ivl),'-g2012','-s','bench','-s','glbl',
                   '-o',str(binary),str(source),str(fixture)]
        execute(command,log.with_name(log.stem+'-compile.log')); generated.add(binary)
        execute([str(ROOT/'.cache/tools/usr/bin/vvp'),str(binary)],log,expect_failure=failure,marker=marker)
        return {'command':command,'binary_sha256':digest(binary),'log':str(log.relative_to(ROOT))}

    for kind in KINDS:
        target = directory/kind; target.mkdir(exist_ok=True)
        model = target/'yosys.v'; body = extract(original,kind)
        write(model,notice+'`timescale 1ps/1ps\n'+body+'\n')
        variants = [('0',False,False),('1',False,False),('x',True,False)]
        if kind == 'FDCE':variants.append(('x',True,True))
        for initial,four_state,known_clear in variants:
            label = ('four-state' if four_state else 'known')+'-init-'+initial+('-known-clear' if known_clear else '')
            trace = target/(label+'.txt'); count, differing, examples = vectors(trace,kind,initial,four_state,known_clear)
            generated.add(trace)
            vendor_supported = not (kind == 'FDCE' and four_state and not known_clear)
            if four_state and vendor_supported:
                differences.append({'kind':kind,'known_async_clear':known_clear,'differing_observations':differing,'examples':examples})
            for vendor in ((False,True) if vendor_supported else (False,)):
                name = 'vendor' if vendor else 'yosys'
                fixture = target/(label+'-'+name+'.sv'); write(fixture,bench(kind,initial,trace,count,vendor))
                source = vendor_sources['FDRE' if kind=='FDRE_1' else kind] if vendor else model
                info = simulate(fixture,source,fixture.with_suffix('.log'),marker=f'PASS {count} flip-flop transitions')
                checks.append({'kind':kind,'model':name,'initial':initial,'four_state':four_state,'observations':count,
                               'known_async_clear':known_clear,'vendor_oracle_defined':vendor_supported,**info})
                if not vendor:fixtures[(kind,initial)] = (fixture,model,count,trace)
                print('PASS',kind,name,label,count,flush=True)
            if not four_state:
                fixture = fixtures[(kind,initial)][0]; obj = target/(label+'-obj')
                config = target/'model.vlt'; write(config,'`verilator_config\n'+''.join(
                    f'lint_off -rule {rule} -file "{model}"\n' for rule in ('INITIALDLY','GENUNNAMED')))
                command = [str(ROOT/'.cache/tools/usr/bin/verilator'),'--binary','--timing','--assert','-j','1',
                           '-Wall','-Wno-DECLFILENAME','-Wno-UNUSEDSIGNAL','--top-module','bench',
                           '-MAKEFLAGS',f'CXX={compiler} LINK={compiler}','--Mdir',str(obj),str(config),str(model),str(fixture)]
                execute(command,target/(label+'-verilator-compile.log'),env=env)
                log = target/(label+'-verilator.log')
                execute([str(obj/'Vbench')],log,marker=f'PASS {count} flip-flop transitions')
                checks.append({'kind':kind,'model':'yosys-verilator','initial':initial,'four_state':False,'observations':count,
                               'command':command,'binary_sha256':digest(obj/'Vbench'),'log':str(log.relative_to(ROOT))})
    # Characterize, rather than normalize away, the vendor's delta-cycle pulse
    # when CLR returns from Z to zero. This is not a physical timing oracle.
    diagnostic = directory/'vendor-unknown-clear.sv'
    write(diagnostic,'''`timescale 1ps/1ps
module glbl;
reg GSR=0; initial begin #100 GSR=1; #1000 GSR=0; end
endmodule
module bench;
reg c=0,r=0,d=1; wire q; integer unknown_pulses=0;
FDCE #(.INIT(1'b0)) dut(.C(c),.CLR(r),.D(d),.CE(1'b1),.Q(q));
always @(dut.CLR_in) if($time>2000 && dut.CLR_in===1'bx)unknown_pulses=unknown_pulses+1;
initial begin
 #2000; c=1; #1000; c=0; #1000; r=1'bz; #1000; d=0; #1000;
 if(q!==1'b1)$fatal(1,"VENDOR_DIAGNOSTIC_SETUP_FAILED");
 r=0; #1000;
 if(c!==1'b0 || q!==1'b0 || unknown_pulses==0)$fatal(1,"VENDOR_DIAGNOSTIC_CHANGED");
 $display("PASS vendor unknown-clear diagnostic: Q changed without a clock edge; internal X pulses=%0d",unknown_pulses);
 $finish;
end
endmodule
''')
    diagnostic_result = simulate(diagnostic,vendor_sources['FDCE'],diagnostic.with_suffix('.log'),
                                 marker='PASS vendor unknown-clear diagnostic')
    mutations = [
        ('wrong-clock-edge','FDRE_1','0','negedge C','posedge C','FLOP_ORACLE_MISMATCH'),
        ('synchronous-clear','FDCE','0','@(posedge C, posedge CLR)','@(posedge C)','FLOP_ORACLE_MISMATCH'),
        ('reset-gated-by-enable','FDRE','0','if (R == !IS_R_INVERTED)','if (CE && R == !IS_R_INVERTED)','FLOP_ORACLE_MISMATCH'),
        ('wrong-startup-value','FDRE','0','initial Q <= INIT;','initial Q <= ~INIT;','FLOP_INIT_MISMATCH'),
        ('zero-unknown-startup','FDRE','x','initial Q <= INIT;',"initial Q <= 1'b0;",'FLOP_INIT_MISMATCH'),
    ]
    for name,kind,initial,old,new,marker in mutations:
        fixture,model,count,trace = fixtures[(kind,initial)]; text = model.read_text()
        if old not in text:raise ValueError('mutation anchor changed: '+name)
        wrong = directory/(name+'.v'); write(wrong,text.replace(old,new))
        simulate(fixture,wrong,directory/(name+'.log'),failure=True,marker=marker)
        controls.append({'name':name,'rejected':True})
    fixture,model,count,trace = fixtures[('FDRE','0')]; lines = trace.read_text().splitlines()
    for name,data,marker in [
        ('truncated-trace','\n'.join(lines[:-1])+'\n','FLOP_TRACE_TRUNCATED_OR_MALFORMED'),
        ('extra-trace',trace.read_text()+'0000 0 0\n','FLOP_TRACE_EXTRA_DATA'),
        ('malformed-trace','invalid\n'+'\n'.join(lines[1:])+'\n','FLOP_TRACE_TRUNCATED_OR_MALFORMED')]:
        wrong_trace = directory/(name+'.txt'); write(wrong_trace,data)
        wrong_fixture = directory/(name+'.sv'); write(wrong_fixture,bench('FDRE','0',wrong_trace,count))
        simulate(wrong_fixture,model,directory/(name+'.log'),failure=True,marker=marker)
        controls.append({'name':name,'rejected':True})
    for name,value in inputs.items():
        if digest(ROOT/name) != value:raise ValueError('flip-flop verification input changed: '+name)
    if digest(compiler) != compiler_identity['sha256']:raise ValueError('compiler changed')
    artifacts = {str(p.relative_to(ROOT)):digest(p) for p in sorted(generated)}
    result = {'status':'passed','scope':'used untimed flip-flop models with binary clocks; startup, control priority and settled state transitions',
              'inputs':inputs,'netlists':inventories,'compiler':compiler_identity,'checks':checks,'artifacts':artifacts,
              'negative_controls_rejected':len(controls),'negative_controls':controls,
              'four_state_vendor_equivalent':False,'four_state_differences':differences,
              'vendor_unknown_async_clear_oracle_verified':False,
              'vendor_unknown_clear_diagnostic':diagnostic_result,
              'limitations':['No physical setup/hold or metastability model','Clock inputs stay known binary',
                             'Vendor global reset is pulsed only to establish INIT; later GSR changes are outside scope',
                             'FDCE vendor oracle keeps CLR binary; unknown CLR has delta-cycle behavior recorded separately',
                             'The full FDCE Yosys X/Z trace leaves its unused vendor expectation column undefined (X)',
                             'No sequential formal-equivalence claim; these are independent oracle simulations'],
              'elapsed_seconds':time.monotonic()-started,'physical_hardware_tested':False}
    report.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS all four used flip-flop kinds and',len(controls),'negative controls')


if __name__ == '__main__':
    main()
