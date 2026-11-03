#!/usr/bin/env python3
"""Prove the binary lookup identity and check the original X/Z behavior."""
import argparse
import json
from pathlib import Path
import re
import subprocess

from build_gate_sim import ROOT, digest, fast_lut_model


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--core-netlist',type=Path,default=ROOT/'build/core-ecp5.json')
    parser.add_argument('--directory',type=Path,default=ROOT/'build/lut-model-check')
    parser.add_argument('--top',default='wasmetal_core')
    args=parser.parse_args()
    directory=args.directory.resolve();directory.mkdir(parents=True,exist_ok=True)
    library=ROOT/'.cache/tools/usr/share/yosys/ecp5/cells_sim.v'
    models=[]
    for width in (2,4):
        name='LUT'+str(width)
        original=re.search(r'\bmodule\s+'+name+r'\b.*?\bendmodule',library.read_text(),re.S)[0]
        original=re.sub(r'\bspecify\b.*?\bendspecify\b','',original,flags=re.S)
        for label,model in [('original',original),('candidate',fast_lut_model(original,name))]:
            # Treat INIT as an input to prove the identity for every table,
            # rather than checking only one elaborated parameter value.
            model=model.replace('module '+name,'module '+label+str(width),1)
            model=model.replace('output Z);',f'input [{(1<<width)-1}:0] INIT, output Z);')
            model,count=re.subn(r'\s*parameter \[[^]]+\] INIT = [^;]+;','',model,count=1)
            if count!=1: raise ValueError('unrecognized LUT parameter declaration')
            models.append(model)
    instances='''
wire a,b,c,d;
original4 u0(pins[0],pins[1],pins[2],pins[3],table_value,a);
candidate4 u1(pins[0],pins[1],pins[2],pins[3],table_value,b);
original2 u2(pins[0],pins[1],table_value[3:0],c);
candidate2 u3(pins[0],pins[1],table_value[3:0],d);
'''
    proof=directory/'equivalence.sv'
    proof.write_text('\n'.join(models)+'\nmodule proof(input [15:0] table_value, input [3:0] pins, output mismatch);\n'+instances+'assign mismatch=(a!=b)||(c!=d);\nendmodule\n')
    script=directory/'equivalence.ys'
    script.write_text(f'read_verilog -sv {proof}\nprep -top proof\nflatten\nopt\nsat -verify -prove mismatch 0 -show-inputs\n')
    with (directory/'equivalence.log').open('w') as log:
        subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-s',str(script)],stdout=log,stderr=subprocess.STDOUT,check=True)
    # Make sure a deliberately wrong primitive cannot pass a vacuous miter.
    wrong=re.sub(r'(module candidate4\b.*?assign Z = )(.*?);',
                 lambda m:m[1]+'~('+m[2]+');',proof.read_text(),count=1,flags=re.S)
    if wrong==proof.read_text(): raise ValueError('negative control was not injected')
    negative=directory/'negative.sv';negative.write_text(wrong)
    negative_script=directory/'negative.ys'
    negative_script.write_text(script.read_text().replace(str(proof),str(negative)))
    rejected=subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-s',str(negative_script)],text=True,capture_output=True)
    (directory/'negative.log').write_text(rejected.stdout+rejected.stderr)
    if rejected.returncode==0 or 'proof did fail' not in rejected.stdout+rejected.stderr:
        raise ValueError('equivalence checker did not reject the wrong LUT')
    netlist=json.loads(args.core_netlist.read_text())
    tables={'0'*16,'1'*16}
    for cell in netlist['modules'][args.top]['cells'].values():
        if cell['type'] in ('LUT4','CCU2C'):
            for name,value in cell.get('parameters',{}).items():
                if name in ('INIT','INIT0','INIT1'):
                    if len(value)!=16 or set(value)-set('01xz'): raise ValueError('unexpected LUT table')
                    tables.add(value)
    for bit in range(16):
        for unknown in ('x','z'):
            word=['0']*16;word[bit]=unknown;tables.add(''.join(word))
    tables=sorted(tables);count=len(tables)
    assignments='\n'.join(f"tables[{i}]=16'b{value};" for i,value in enumerate(tables))
    bench=directory/'four_state.sv'
    bench.write_text('''module bench;
reg [15:0] table_value;
reg [3:0] pins;
'''+instances+f'reg [15:0] tables[0:{count-1}];\ninteger i,j,k;\ninitial begin\n'+assignments+f'''
for(i=0;i<{count};i=i+1) begin
 table_value=tables[i];
 for(j=0;j<256;j=j+1) begin
  for(k=0;k<4;k=k+1) begin
   case((j>>(2*k))&3)
   0:pins[k]=0;1:pins[k]=1;2:pins[k]=1'bx;3:pins[k]=1'bz;
   endcase
  end
  #1;
  if(a!==b || c!==d) $fatal(1,"LUT mismatch table=%h pins=%b",table_value,pins);
 end
end
$display("PASS {count*256} four-state LUT cases");
$finish;
end
endmodule
''')
    binary=directory/'four_state.vvp'
    subprocess.run([str(ROOT/'.cache/tools/usr/bin/iverilog'),'-B',str(ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl'),
                    '-g2012','-s','bench','-o',str(binary),str(proof),str(bench)],check=True)
    result=subprocess.run([str(ROOT/'.cache/tools/usr/bin/vvp'),str(binary)],text=True,capture_output=True,check=True)
    (directory/'four_state.log').write_text(result.stdout+result.stderr)
    report={'binary_equivalence_proven':True,'negative_control_rejected':True,'binary_scope':'every 16-bit or 4-bit INIT table and every binary selector',
            'four_state_cases_passed':count*256,'four_state_scope':'every selector combination for all mapped tables plus single X/Z table-bit patterns',
            'library_sha256':digest(library),'netlist_sha256':digest(args.core_netlist),'top':args.top,
            'optimizer_source_sha256':digest(ROOT/'tools/build_gate_sim.py'),
            'checker_sha256':digest(Path(__file__).resolve()),'proof_sha256':digest(proof),
            'four_state_test_sha256':digest(bench)}
    (directory/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS exhaustive binary LUT equivalence and',count*256,'four-state cases')


if __name__=='__main__': main()
