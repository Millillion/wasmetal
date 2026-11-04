#!/usr/bin/env python3
"""Check every DSP configuration in the current 7-series system against integer arithmetic."""
import collections
import copy
import fcntl
import hashlib
import json
from pathlib import Path
import random
import re
import shutil
import subprocess
import time

from check_xc7_memory_mapping import TOOLS, VENDOR, identities, verify_vendor
from check_xc7_ram_models import outcome, run
from prepare_standalone import ROOT, digest
from xc7_dsp_model import split_carries

BUILD = ROOT/'build/xc7-dsp'
BENCH = ROOT/'tests/xc7/dsp.sv'
LIBRARY = TOOLS/'share/yosys/xilinx/cells_sim.v'
GROUPS = {('DIRECT','DIRECT',5):9, ('CASCADE','DIRECT',85):16,
          ('DIRECT','DIRECT',21):1, ('DIRECT','CASCADE',85):1, ('DIRECT','DIRECT',53):2}
REGISTERS = ['ACASCREG','ADREG','ALUMODEREG','AREG','BCASCREG','BREG','CARRYINREG',
             'CARRYINSELREG','CREG','DREG','INMODEREG','MREG','OPMODEREG','PREG']


def verify_dsp_vendor():
    verify_vendor()
    pin = json.loads((VENDOR/'DSP48E1.UPSTREAM.json').read_text())
    data = (VENDOR/'DSP48E1.v').read_bytes()
    blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if blob != pin['git_blob_sha'] or digest(VENDOR/'DSP48E1.v') != pin['sha256']:
        raise ValueError('DSP vendor source changed')


def audit(module):
    cells = module['cells']
    consumed = {bit for cell in cells.values() for port, bits in cell['connections'].items()
        if cell['port_directions'][port]=='input' for bit in bits}
    consumed.update(bit for port in module['ports'].values() if port['direction']=='output'
        for bit in port['bits'])
    groups = collections.Counter()
    for name, cell in cells.items():
        if cell['type'] != 'DSP48E1':
            continue
        p = cell['parameters']; pins = cell['connections']
        for port, bits in pins.items():
            if cell['port_directions'][port]=='output' and port not in {'P','PCOUT','ACOUT','BCOUT'} and \
                    any(isinstance(bit,int) and bit in consumed for bit in bits):
                raise ValueError('unverified DSP output is consumed: '+name+'.'+port)
        fixed = {k:'0'*32 for k in REGISTERS}
        fixed.update(USE_DPORT='FALSE', USE_MULT='MULTIPLY', USE_SIMD='ONE48',
                     A_INPUT=p.get('A_INPUT'), B_INPUT=p.get('B_INPUT'))
        if p != fixed:
            raise ValueError('unreviewed DSP parameters: '+name)
        for key, width in [('ALUMODE',4),('CARRYIN',1),('CARRYINSEL',3),('INMODE',5)]:
            if pins.get(key) != ['0']*width:
                raise ValueError('unreviewed DSP control: '+name+'.'+key)
        op = pins.get('OPMODE',[])
        if len(op)!=7 or set(op)-{'0','1'}:
            raise ValueError('unreviewed variable DSP operation: '+name)
        group = (p['A_INPUT'],p['B_INPUT'],int(''.join(reversed(op)),2))
        if group not in GROUPS:
            raise ValueError('unreviewed DSP arithmetic mode: '+name)
        groups[group] += 1
    if groups != GROUPS:
        raise ValueError('DSP inventory changed; review complete configuration coverage')
    return groups


def inventory_controls(module):
    name=next(n for n,c in module['cells'].items() if c['type']=='DSP48E1')
    results=[]
    for label in ['registered-input','nonzero-carry','variable-opmode','unsupported-opmode',
                  'unsupported-a-source','extra-parameter','missing-dsp','unverified-output']:
        mutant=dict(module);mutant['cells']=dict(module['cells'])
        cell=copy.deepcopy(module['cells'][name]);mutant['cells'][name]=cell
        if label=='registered-input':cell['parameters']['AREG']='0'*31+'1'
        elif label=='nonzero-carry':cell['connections']['CARRYIN']=['1']
        elif label=='variable-opmode':cell['connections']['OPMODE'][0]=999999
        elif label=='unsupported-opmode':cell['connections']['OPMODE']=['0']*7
        elif label=='unsupported-a-source':cell['parameters']['A_INPUT']='UNREVIEWED'
        elif label=='extra-parameter':cell['parameters']['IS_CARRYIN_INVERTED']='1'
        elif label=='missing-dsp':del mutant['cells'][name]
        else:
            cell['connections']['CARRYOUT']=[999999];cell['port_directions']['CARRYOUT']='output'
            mutant['ports']=dict(module['ports'])
            mutant['ports']['unverified']={'direction':'output','bits':[999999]}
        try:audit(mutant)
        except ValueError as error:results.append({'name':label,'diagnostic':str(error)})
        else:raise ValueError('DSP inventory mutation accepted: '+label)
    return results


def fixture(group, mutation=None):
    aa, bb, op = group
    if mutation=='wrong-a-cascade':aa='DIRECT'
    if mutation=='wrong-b-cascade':bb='DIRECT'
    if mutation=='unshifted-cascade':op=21
    params=[f'.{key}(0)' for key in REGISTERS]
    params += [f'.A_INPUT("{aa}")',f'.B_INPUT("{bb}")',
               '.USE_DPORT("FALSE")','.USE_MULT("MULTIPLY")','.USE_SIMD("ONE48")']
    enables=['CEA1','CEA2','CEAD','CEALUMODE','CEB1','CEB2','CEC','CECARRYIN','CECTRL','CED','CEINMODE','CEM','CEP']
    resets=['RSTA','RSTALLCARRYIN','RSTALUMODE','RSTB','RSTC','RSTCTRL','RSTD','RSTINMODE','RSTM','RSTP']
    pins=['.A(a)','.ACIN(acin)','.B(b)','.BCIN(bcin)','.C(c)',".D(25'b0)",'.PCIN(pcin)',
          '.CLK(clk)',f".OPMODE(7'd{op})",".ALUMODE(4'b0)",".INMODE(5'b0)",".CARRYINSEL(3'b0)",
          f".CARRYIN(1'b{int(mutation=='wrong-carry')})",".CARRYCASCIN(1'b0)",".MULTSIGNIN(1'b0)",
          '.P(raw_p)','.PCOUT(raw_pc)','.ACOUT(acout)','.BCOUT(bcout)']
    pins += [f'.{key}(enable)' for key in enables]+[f'.{key}(reset)' for key in resets]
    return '''module dsp_fixture(input clk,enable,reset,
input [29:0] a,acin,input [17:0] b,bcin,input [47:0] c,pcin,
output [47:0] p,pcout,output [29:0] acout,output [17:0] bcout);
wire [47:0] raw_p,raw_pc;
'''+'DSP48E1 #('+','.join(params)+') cell_under_test('+','.join(pins)+');\n'+\
        f"assign p=raw_p ^ 48'd{int(mutation=='flipped-product')};\n"+\
        ("assign pcout=48'b0;\n" if mutation=='lost-cascade-output' else 'assign pcout=raw_pc;\n')+'endmodule\n'


def vectors(group, path):
    rng = random.Random(0xD548E1)
    widths=[30,30,18,18,48,48]
    mask=(1<<48)-1
    rows=[]
    def signed(value,width):return (value&((1<<(width-1))-1))-(value&(1<<(width-1)))
    def emit(values):
        a,ac,b,bc,c,pc=values
        av=a if group[0]=='DIRECT' else ac
        bv=b if group[1]=='DIRECT' else bc
        z={5:0,21:signed(pc,48),53:signed(c,48),85:signed(pc,48)>>17}[group[2]]
        p=(signed(av,25)*signed(bv,18)+z)&mask
        rows.append(' '.join(f'{v:x}' for v in [*values,p,av,bv])+'\n')
    ca=[0,1,2,(1<<24)-1,1<<24,(1<<25)-1,0x1555555,0xaaaaaa]
    cb=[0,1,2,(1<<17)-1,1<<17,(1<<18)-1,0x15555,0x2aaaa]
    cz=[0,1,mask,1<<47,(1<<47)-1,1<<16,1<<17,(1<<17)-1,0x555555555555,0xaaaaaaaaaaaa]
    for a in ca:
        for b in cb:
            for z in cz:
                emit([a|(0x15<<25),((1<<30)-1)^a,b,((1<<18)-1)^b,z,mask^z])
    for field,width in enumerate(widths):
        for bit in range(width):
            for invert in [False,True]:
                values=[rng.getrandbits(w) for w in widths]
                values[field]=((1<<width)-1)^(1<<bit) if invert else 1<<bit
                emit(values)
    for _ in range(16384):emit([rng.getrandbits(w) for w in widths])
    path.write_text(''.join(rows))
    if len(rows)!=17408:raise ValueError('incomplete DSP vector plan')
    return len(rows)


def simulate(directory, label, wrapper, model, trace, count, verilator=False, failure=None):
    sources=[wrapper,model,BENCH,VENDOR/'glbl.v']
    inputs=identities([*sources,trace])
    if verilator:
        obj=directory/(label+'-obj')
        command=[TOOLS/'bin/verilator','--binary','--timing','--assert','-j','2','-Wno-fatal',
                 '--top-module','xc7_dsp','--Mdir',obj,*sources]
        binary=obj/'Vxc7_dsp'
    else:
        binary=directory/(label+'.vvp')
        command=[TOOLS/'bin/iverilog','-B'+str(TOOLS/'lib/x86_64-linux-gnu/ivl'),'-g2012',
                 '-s','xc7_dsp','-s','glbl','-o',binary,*sources]
    compile_log=directory/(label+'-compile.log')
    code,_=run(command,compile_log,timeout=600)
    if code:raise RuntimeError('DSP compilation failed: '+str(compile_log))
    log=directory/(label+'.log')
    invoke=([binary] if verilator else [TOOLS/'bin/vvp',binary])+['+VECTORS='+str(trace),'+COUNT='+str(count)]
    code,text=run(invoke,log)
    outcome(code,text,f'PASS XC7_DSP vectors={count}',failure,verilator)
    if identities([ROOT/n for n in inputs])!=inputs:raise ValueError('DSP test inputs changed')
    return {'inputs':inputs,'command':list(map(str,command)),'returncode':code,
            'expected_failure':failure,'observations':text.splitlines(),
            'artifacts':identities([binary,compile_log,log])}


def main():
    started=time.monotonic(); report=ROOT/'reports/xc7-dsp.json';report.unlink(missing_ok=True)
    verify_dsp_vendor()
    estimate=ROOT/'reports/xc7-system-estimate.json';netlist=ROOT/'build/xc7-system/mapped.json'
    reference=json.loads(estimate.read_text())
    if reference['netlist_sha256']!=digest(netlist):raise ValueError('stale DSP inventory')
    for name,h in reference['inputs'].items():
        if digest(ROOT/name)!=h:raise ValueError('stale synthesis input: '+name)
    module=json.loads(netlist.read_text())['modules'][reference['top']]
    groups=audit(module);inventory_negative=inventory_controls(module)
    compiler=Path(shutil.which('g++')).resolve()
    compiler_identity={'path':str(compiler),'sha256':digest(compiler),
        'version':subprocess.check_output([str(compiler),'--version'],text=True).splitlines()[0]}
    inputs=identities([Path(__file__).resolve(),BENCH,LIBRARY,estimate,netlist,
        ROOT/'tools/check_xc7_memory_mapping.py',ROOT/'tools/check_xc7_ram_models.py',ROOT/'tools/prepare_standalone.py',
        ROOT/'tools/xc7_dsp_model.py',
        *[VENDOR/n for n in ['DSP48E1.v','DSP48E1.UPSTREAM.json','UPSTREAM.json','LICENSE','glbl.v']],
        TOOLS/'bin/iverilog',TOOLS/'bin/vvp',TOOLS/'bin/verilator',TOOLS/'bin/verilator_bin'])
    extracted=re.findall(r'\bmodule\s+DSP48E1\b.*?\bendmodule',LIBRARY.read_text(),re.S)
    if len(extracted)!=1:raise ValueError('ambiguous standard DSP model')
    model=BUILD/'yosys-dsp.v';model.write_text(extracted[0]+'\n')
    split_model=BUILD/'yosys-dsp-split.v';split_model.write_text(split_carries(extracted[0])+'\n')
    checks=[];negative=[]
    for index,(group,instances) in enumerate(sorted(groups.items())):
        directory=BUILD/f'configuration-{index}';directory.mkdir(exist_ok=True)
        wrapper=directory/'fixture.sv';wrapper.write_text(fixture(group))
        trace=directory/'vectors.txt';count=vectors(group,trace)
        vendor=simulate(directory,'vendor',wrapper,VENDOR/'DSP48E1.v',trace,count)
        standard=simulate(directory,'yosys',wrapper,model,trace,count)
        split=simulate(directory,'split-icarus',wrapper,split_model,trace,count)
        compiled=simulate(directory,'verilator',wrapper,split_model,trace,count,verilator=True)
        mutations=[]
        if group==('DIRECT','DIRECT',5):mutations+=['wrong-carry','flipped-product','lost-cascade-output']
        if group[0]=='CASCADE':mutations+=['wrong-a-cascade','unshifted-cascade']
        if group[1]=='CASCADE':mutations+=['wrong-b-cascade']
        for mutation in mutations:
            changed=directory/(mutation+'.sv');changed.write_text(fixture(group,mutation))
            negative.append(simulate(directory,mutation,changed,split_model,trace,count,failure='DSP_DATA_MISMATCH'))
        checks.append({'a_input':group[0],'b_input':group[1],'opmode':group[2],
                       'instances':instances,'vectors_per_model':count,'vendor':vendor,'yosys':standard,
                       'split_icarus':split,'verilator':compiled})
        print(f'PASS DSP {group}: {count} integer-oracle vectors in vendor, original Yosys and split-carry models',flush=True)
    if len(negative)!=6:raise ValueError('missing DSP fault controls')
    if identities([ROOT/n for n in inputs])!=inputs:raise ValueError('DSP verification inputs changed')
    if digest(compiler)!=compiler_identity['sha256']:raise ValueError('DSP test compiler changed')
    verify_dsp_vendor()
    report.write_text(json.dumps({'status':'passed','inputs':inputs,'checks':checks,'compiler':compiler_identity,
        'instances_covered':sum(groups.values()),'vectors_per_model':sum(c['vectors_per_model'] for c in checks),
        'negative_controls':negative,'negative_controls_rejected':len(negative),
        'inventory_negative_controls':inventory_negative,'inventory_controls_rejected':len(inventory_negative),
        'scope':'Used unregistered multiplier/cascade configurations and all consumed output types; independent signed-integer oracle',
        'limitations':['Known input data only; no four-state equivalence claim.','No registered DSP modes, physical timing or silicon validation.'],
        'physical_hardware_tested':False,'elapsed_seconds':time.monotonic()-started},indent=2)+'\n')


if __name__=='__main__':
    BUILD.mkdir(parents=True,exist_ok=True)
    with (BUILD/'.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        main()
