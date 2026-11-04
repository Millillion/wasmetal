#!/usr/bin/env python3
"""Verify the used distributed RAM with state proofs and independent memory oracles."""
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


def audit(module):
    count = 0
    required = {'ADDRA','ADDRB','ADDRC','ADDRD','DIA','DIB','DIC','DOA','DOB','DOC','WCLK','WE'}
    for cell in module['cells'].values():
        if cell['type'] != 'RAM64M':continue
        for name,value in cell['parameters'].items():
            if name not in {'INIT_A','INIT_B','INIT_C','INIT_D','IS_WCLK_INVERTED'} or int(value,2) != 0:
                raise ValueError('unreviewed distributed-RAM parameter: '+name)
        pins = set(cell['connections'])
        if not required <= pins or pins-required-{'DID','DOD'}:
            raise ValueError('unreviewed distributed-RAM ports')
        if any(len(bits) != (6 if name.startswith('ADDR') else 1) for name,bits in cell['connections'].items()):
            raise ValueError('unreviewed distributed-RAM port width')
        count += 1
    if not count:raise ValueError('missing distributed-RAM inventory')
    return count


def initial_state(module):
    storage = {bit for cell in module['cells'].values() if cell['type'] in ('$dff','$dffe') for bit in cell['connections']['Q']}
    banks = set()
    for name in ('mem_a','mem_b','mem_c','mem_d'):
        memory = module['netnames'][name]
        if len(memory['bits']) != 64 or memory['attributes'].get('init') != '0'*64:
            raise ValueError('RAM proof initial state differs from the actual zero-initialized configuration')
        banks.update(memory['bits'])
    if len(banks) != 256 or banks != storage:
        raise ValueError('RAM proof does not cover every state bit')
    return {'state_bits':256,'banks':4,'initial_values':'all zero'}


def vectors(path, initial, four_state):
    memories = [[list(reversed(bank)) for bank in initial] for _ in range(2)]
    old_clock = '0'; count = 0; differences = 0; examples = []
    symbols = '01xz' if four_state else '01'; rng = random.Random(0x64D157)
    with path.open('w') as stream:
        def emit(clock, enable, data, addresses):
            nonlocal old_clock,count,differences
            observed = []
            for vendor in (False,True):
                memory = memories[int(vendor)]
                if old_clock == '0' and clock == '1' and (enable == '1' or vendor and enable == 'z'):
                    if set(addresses[3]) <= {'0','1'}:
                        address = int(addresses[3],2)
                        for bank in range(4):memory[bank][address] = data[3-bank]
                outputs = [memory[bank][int(addresses[bank],2)] if set(addresses[bank]) <= {'0','1'} else 'x' for bank in range(4)]
                observed.append(''.join(reversed(outputs)))
            pins = clock+enable+data+''.join(addresses)
            stream.write(pins+' '+observed[0]+' '+observed[1]+'\n')
            if observed[0] != observed[1]:
                differences += 1
                if len(examples)<8:examples.append({'pins':pins,'yosys':observed[0],'vendor':observed[1]})
            old_clock = clock; count += 1
        def operation(address, data, enable='1'):
            addresses = [f'{address:06b}']*4
            emit('0',enable,data,addresses);emit('1',enable,data,addresses)
            changed = ''.join('1' if x=='0' else '0' for x in data)
            emit('1',enable,changed,addresses);emit('0',enable,changed,addresses)
        for address in range(64):emit('0','0','0000',[f'{address:06b}']*4)
        for address in range(64):
            for bits in itertools.product(symbols,repeat=4):operation(address,''.join(bits))
            for value in range(16):operation(address,f'{value:04b}','0')
        if four_state:
            for address in (0,1,31,32,63):
                for enable in symbols:
                    for bits in itertools.product(symbols,repeat=4):operation(address,''.join(bits),enable)
        # Distinct, nonuniform bank contents make every address/port pairing
        # sensitive to aliases and exchanged read ports.
        for address in range(64):operation(address,f'{rng.randrange(16):04b}')
        for left,right in itertools.combinations(range(4),2):
            for a in range(64):
                for b in range(64):
                    addresses = [f'{(a+7*b+13*i)&63:06b}' for i in range(4)]
                    addresses[left]=f'{a:06b}';addresses[right]=f'{b:06b}'
                    emit('0','0','0000',addresses)
        if four_state:
            # Every four-state six-bit read address on every port.
            for port in range(4):
                for bits in itertools.product('01xz',repeat=6):
                    addresses = [f'{(11*i+23)&63:06b}' for i in range(4)];addresses[port]=''.join(bits)
                    emit('0','0','0000',addresses)
            # Invalid-address writes leave the simulation arrays unchanged.
            # This is a model-semantic check, not a physical corruption bound.
            for bits in itertools.product('01xz',repeat=6):
                addresses = ['000000','011111','111111',''.join(bits)]
                emit('0','1','1010',addresses);emit('1','1','1010',addresses)
            for address in range(64):emit('0','0','0000',[f'{address:06b}']*4)
        for _ in range(2048):
            addresses = [f'{rng.randrange(64):06b}' for _ in range(4)]
            data = ''.join(rng.choice(symbols) for _ in range(4));enable = rng.choice(symbols)
            emit('0',enable,data,addresses);emit('1',enable,data,addresses)
    if not four_state and differences:raise ValueError('binary RAM oracles disagree')
    return count,differences,examples


def bench(initial, trace, count, vendor=False):
    params = ','.join(f'.INIT_{name}(64\'b{value})' for name,value in zip('ABCD',initial))
    return f'''`timescale 1ps/1ps
module bench;
reg [29:0] pins=0,next_pins;
reg [3:0] expected_yosys,expected_vendor;
wire [3:0] observed;
RAM64M #({params}) dut(.WCLK(pins[29]),.WE(pins[28]),
 .DIA(pins[24]),.DIB(pins[25]),.DIC(pins[26]),.DID(pins[27]),
 .ADDRA(pins[23:18]),.ADDRB(pins[17:12]),.ADDRC(pins[11:6]),.ADDRD(pins[5:0]),
 .DOA(observed[0]),.DOB(observed[1]),.DOC(observed[2]),.DOD(observed[3]));
integer fd,n,j,extra;
initial begin
 #1000;
 fd=$fopen("{trace}","r");if(fd==0)$fatal(1,"LUTRAM_TRACE_OPEN_FAILED");
 for(j=0;j<{count};j=j+1)begin
  n=$fscanf(fd,"%b %b %b",next_pins,expected_yosys,expected_vendor);
  if(n!=3)$fatal(1,"LUTRAM_TRACE_TRUNCATED_OR_MALFORMED");
  pins=next_pins; #1000;
  if(observed!=={'expected_vendor' if vendor else 'expected_yosys'})
   $fatal(1,"LUTRAM_ORACLE_MISMATCH row=%0d pins=%b observed=%b yosys=%b vendor=%b",j,pins,observed,expected_yosys,expected_vendor);
 end
 n=$fscanf(fd,"%s",extra);
 if(n!=-1 && !(n==0 && $feof(fd)))$fatal(1,"LUTRAM_TRACE_EXTRA_DATA");
 $fclose(fd);$display("PASS {count} distributed-RAM observations");$finish;
end
endmodule
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--netlist',type=Path,action='append');args=parser.parse_args()
    netlists = [p if p.is_absolute() else ROOT/p for p in (args.netlist or [ROOT/'build/xc7-system/mapped.json'])]
    started=time.monotonic();directory=ROOT/'build/xc7-lutram';directory.mkdir(exist_ok=True)
    report=ROOT/'reports/xc7-lutram.json';report.unlink(missing_ok=True)
    library=ROOT/'.cache/tools/usr/share/yosys/xilinx/cells_sim.v';vendor=ROOT/'third_party/xilinx-unisim/RAM64M.v'
    pin_path=vendor.with_suffix('.UPSTREAM.json');pin=json.loads(pin_path.read_text());data=vendor.read_bytes()
    if digest(vendor)!=pin['sha256'] or len(data)!=pin['bytes'] or hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()!=pin['git_blob_sha']:
        raise ValueError('vendor distributed RAM differs from its upstream pin')
    dependencies=[Path(__file__).resolve(),ROOT/'tools/check_xc7_luts.py',ROOT/'tools/prepare_standalone.py',library,vendor,pin_path,
                  vendor.with_name('LICENSE'),vendor.with_name('UPSTREAM.json'),*netlists]
    dependencies += [ROOT/'.cache/tools/usr/bin'/n for n in ('yosys','iverilog','vvp','verilator','verilator_bin')]
    dependencies += [p for p in sorted((ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl').glob('*')) if p.is_file()]
    dependencies += [p for p in sorted((ROOT/'.cache/tools/usr/share/verilator/include').rglob('*')) if p.is_file()]
    inputs={str(p.relative_to(ROOT)):digest(p) for p in dependencies}
    compiler=Path(shutil.which('g++')).resolve();compiler_identity={'path':str(compiler),'sha256':digest(compiler),
        'version':subprocess.check_output([str(compiler),'--version'],text=True).splitlines()[0]}
    generated=set();checks=[];controls=[];inventories=[]
    def write(path,text):path.write_text(text);generated.add(path)
    def execute(command,log,**kwargs):run(command,log,**kwargs);generated.add(log)
    def simulate(fixture,source,log,failure=False,marker=None):
        binary=log.with_suffix('.vvp')
        command=[str(ROOT/'.cache/tools/usr/bin/iverilog'),'-B',str(ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl'),
                 '-g2012','-s','bench','-o',str(binary),str(source),str(fixture)]
        execute(command,log.with_name(log.stem+'-compile.log'));generated.add(binary)
        execute([str(ROOT/'.cache/tools/usr/bin/vvp'),str(binary)],log,expect_failure=failure,marker=marker)
        return {'command':command,'binary_sha256':digest(binary),'log':str(log.relative_to(ROOT))}
    for path in netlists:
        module=json.loads(path.read_text())['modules']['wasmetal_loadable']
        inventories.append({'path':str(path),'sha256':digest(path),'instances':audit(module)})
        small={'cells':{k:c for k,c in module['cells'].items() if c['type']=='RAM64M'}}
        for name,change in [('clock-inversion',lambda c:c['parameters'].update(IS_WCLK_INVERTED='1')),
                            ('nonzero-init',lambda c:c['parameters'].update(INIT_A='1')),
                            ('unknown-parameter',lambda c:c['parameters'].update(UNREVIEWED='1')),
                            ('address-width',lambda c:c['connections']['ADDRD'].pop())]:
            wrong=deepcopy(small);change(next(iter(wrong['cells'].values())))
            try:audit(wrong)
            except ValueError:controls.append('inventory-'+path.parent.name+'-'+name)
            else:raise ValueError('accepted RAM inventory fault: '+name)
    text=library.read_text();notice=text[:re.search(r'^module\b',text,re.M).start()]
    model=directory/'yosys.v';write(model,notice+'`timescale 1ps/1ps\n'+extract(text,'RAM64M')+'\n')
    # For known binary WE, the vendor's Z detector is identically false. Check
    # the original four-state expression exhaustively before specializing the
    # proof; the actual vendor simulation source is never modified.
    predicate=directory/'write-enable.sv'
    predicate_text='''`timescale 1ps/1ps
module bench;
reg we;wire original=(we===1'bz)||we;
initial begin
 we=0;#1000;if(original!==we)$fatal(1,"LUTRAM_WRITE_ENABLE_MISMATCH");
 we=1;#1000;if(original!==we)$fatal(1,"LUTRAM_WRITE_ENABLE_MISMATCH");
 we=1'bx;#1000;if(original!==1'bx)$fatal(1,"LUTRAM_WRITE_ENABLE_MISMATCH");
 we=1'bz;#1000;if(original!==1'b1)$fatal(1,"LUTRAM_WRITE_ENABLE_MISMATCH");
 $display("PASS all four write-enable states and complete binary specialization");$finish;
end
endmodule
'''
    write(predicate,predicate_text)
    predicate_check=simulate(predicate,model,predicate.with_suffix('.log'),marker='PASS all four write-enable states')
    bad_predicate=directory/'wrong-write-enable.sv';write(bad_predicate,predicate_text.replace("(we===1'bz)||we","(we===1'bz)&&we"))
    simulate(bad_predicate,model,bad_predicate.with_suffix('.log'),True,'LUTRAM_WRITE_ENABLE_MISMATCH');controls.append('wrong-write-enable-specialization')
    vendor_text=vendor.read_text();anchor="assign WE_in = (WE === 1'bz) || WE;"
    if vendor_text.count(anchor)!=1:raise ValueError('unrecognized vendor binary-specialization anchor')
    specialized=vendor_text.replace(anchor,'assign WE_in = WE;')
    if specialized.replace('assign WE_in = WE;',anchor)!=vendor_text:raise ValueError('unexpected vendor specialization change')
    specialized=re.sub(r'\bmodule RAM64M\b','module VENDOR_RAM64M',specialized,count=1)
    proof_vendor=directory/'binary-vendor.v';write(proof_vendor,'// Binary-input proof specialization: the WE Z detector is false for WE=0/1.\n'+specialized)
    lowered=directory/'lowered.json';script=directory/'equivalence.ys'
    script_text=f'read_verilog -sv {model} {proof_vendor}\nproc\nmemory_map\nopt\nwrite_json {lowered}\nequiv_make RAM64M VENDOR_RAM64M equiv\nhierarchy -top equiv\nequiv_simple\nequiv_induct -seq 2\nequiv_status -assert\n'
    write(script,script_text)
    execute([str(ROOT/'.cache/tools/usr/bin/yosys'),'-s',str(script)],script.with_suffix('.log'),marker='Equivalence successfully proven!');generated.add(lowered)
    proof_log=script.with_suffix('.log').read_text()
    if '260 are proven and 0 are unproven' not in proof_log:raise ValueError('unexpected RAM state/output proof coverage')
    lowered_models=json.loads(lowered.read_text())['modules'];states={name:initial_state(m) for name,m in lowered_models.items()}
    wrong=deepcopy(lowered_models['VENDOR_RAM64M']);wrong['netnames']['mem_a']['attributes']['init']='1'+'0'*63
    try:initial_state(wrong)
    except ValueError:controls.append('wrong-proof-initial-state')
    else:raise ValueError('accepted incorrect proof initial state')
    wrong_vendor=directory/'wrong-address-vendor.v';anchor='assign ADDRD_in = ADDRD;'
    if specialized.count(anchor)!=1:raise ValueError('unrecognized write-address anchor')
    write(wrong_vendor,specialized.replace(anchor,"assign ADDRD_in = {1'b0,ADDRD[4:0]};"))
    wrong_script=directory/'wrong-address-proof.ys'
    write(wrong_script,script_text.replace(str(proof_vendor),str(wrong_vendor)).replace(f'write_json {lowered}\n',''))
    execute([str(ROOT/'.cache/tools/usr/bin/yosys'),'-s',str(wrong_script)],wrong_script.with_suffix('.log'),
            expect_failure=True,marker='unproven $equiv cells');controls.append('wrong-write-address-proof')
    variants=[('zero',['0'*64]*4,False),('asymmetric',[f'{n:064b}' for n in (0x13579BDF2468ACE0,0xFEDCBA9876543210,0x5AA53CC3F00F9696,0x0123456789ABCDEF)],False),
              ('four-state',['x'*64,'z'*64,'01xz'*16,'10zx'*16],True)]
    fixtures={};differences=[]
    for label,initial,four_state in variants:
        trace=directory/(label+'.txt');count,differing,examples=vectors(trace,initial,four_state);generated.add(trace)
        if four_state:differences.append({'cases':count,'differing_observations':differing,'examples':examples})
        for is_vendor in (False,True):
            name='vendor' if is_vendor else 'yosys';fixture=directory/(label+'-'+name+'.sv')
            write(fixture,bench(initial,trace,count,is_vendor))
            info=simulate(fixture,vendor if is_vendor else model,fixture.with_suffix('.log'),marker=f'PASS {count} distributed-RAM observations')
            checks.append({'initialization':label,'model':name,'four_state':four_state,'observations':count,**info})
            if not is_vendor:fixtures[label]=(fixture,trace,count,initial)
        if not four_state:
            fixture=fixtures[label][0];obj=directory/(label+'-obj')
            command=[str(ROOT/'.cache/tools/usr/bin/verilator'),'--binary','--timing','--assert','-j','1','-Wall',
                     '-Wno-DECLFILENAME','-Wno-UNUSEDSIGNAL','--top-module','bench','-MAKEFLAGS',f'CXX={compiler} LINK={compiler}',
                     '--Mdir',str(obj),str(model),str(fixture)]
            execute(command,directory/(label+'-verilator-compile.log'),env=dict(os.environ,VERILATOR_ROOT=str(ROOT/'.cache/tools/usr/share/verilator')))
            log=directory/(label+'-verilator.log');execute([str(obj/'Vbench')],log,marker=f'PASS {count} distributed-RAM observations')
            checks.append({'initialization':label,'model':'yosys-verilator','four_state':False,'observations':count,
                           'command':command,'binary_sha256':digest(obj/'Vbench'),'log':str(log.relative_to(ROOT))})
        print('PASS distributed RAM',label,count,'observations per model',flush=True)
    mutations=[('read-port-alias','zero','assign DOA = mem_a[ADDRA];','assign DOA = mem_a[ADDRB];'),
               ('ignore-enable','zero','if (WE)',"if (1'b1)"),
               ('transparent-write','zero','always @(posedge clk)','always @*'),
               ('exchanged-data-bank','zero','mem_a[ADDRD] <= DIA;','mem_a[ADDRD] <= DIB;'),
               ('zero-unknown-init','four-state','reg [63:0] mem_a = INIT_A;',"reg [63:0] mem_a = 64'b0;"),
               ('zero-unknown-write','four-state','mem_a[ADDRD] <= DIA;',"mem_a[ADDRD] <= DIA === 1'b1;")]
    for name,label,old,new in mutations:
        source=model.read_text()
        if source.count(old)!=1:raise ValueError('unrecognized RAM mutation anchor: '+name)
        bad_model=directory/(name+'.v');write(bad_model,source.replace(old,new))
        simulate(fixtures[label][0],bad_model,directory/(name+'.log'),True,'LUTRAM_ORACLE_MISMATCH');controls.append(name)
    fixture,trace,count,initial=fixtures['zero'];lines=trace.read_text().splitlines()
    for name,data,marker in [('truncated-trace','\n'.join(lines[:-1])+'\n','LUTRAM_TRACE_TRUNCATED_OR_MALFORMED'),
                             ('extra-trace',trace.read_text()+'0 0 0\n','LUTRAM_TRACE_EXTRA_DATA'),
                             ('malformed-trace','invalid\n'+'\n'.join(lines[1:])+'\n','LUTRAM_TRACE_TRUNCATED_OR_MALFORMED')]:
        bad_trace=directory/(name+'.txt');write(bad_trace,data);bad_fixture=directory/(name+'.sv');write(bad_fixture,bench(initial,bad_trace,count))
        simulate(bad_fixture,model,bad_fixture.with_suffix('.log'),True,marker);controls.append(name)
    for name,value in inputs.items():
        if digest(ROOT/name)!=value:raise ValueError('distributed-RAM verification input changed: '+name)
    if digest(compiler)!=compiler_identity['sha256']:raise ValueError('compiler changed')
    result={'status':'passed','scope':'all used zero-initialized RAM64M instances; binary state proof and independent untimed memory oracles',
            'inputs':inputs,'netlists':inventories,'compiler':compiler_identity,'checks':checks,
            'proof':{'state_bits':256,'output_bits':4,'all_260_equivalence_points_proven':True,'initial_states':states,
                     'vendor_binary_enable_specialization':True,'specialization_truth_table':predicate_check},
            'four_state_vendor_equivalent':False,'four_state_differences':differences,
            'negative_controls_rejected':len(controls),'negative_controls':controls,
            'artifacts':{str(p.relative_to(ROOT)):digest(p) for p in sorted(generated)},
            'limitations':['The proof specializes the vendor WE Z detector under binary WE; the original expression is checked exhaustively',
                           'Vendor unit delays are ignored by the state proof; simulation samples settled values',
                           'Clock inputs remain binary; unknown addresses and enables characterize models, not physical fault containment',
                           'No X/Z sequential-equivalence or physical timing claim'],
            'elapsed_seconds':time.monotonic()-started,'physical_hardware_tested':False}
    report.write_text(json.dumps(result,indent=2)+'\n');print('PASS 260 RAM equivalence points and',len(controls),'negative controls')


if __name__=='__main__':main()
