#!/usr/bin/env python3
"""Check counter sizing and the final transaction around 32-bit capacity boundaries."""
import json
from pathlib import Path
import subprocess
from prepare_standalone import ROOT,digest

CAPACITIES=(16,80,131072,429496736,858993456,858993472,2147483632)


def main():
    directory=ROOT/'build/memory-bist-widths';directory.mkdir(parents=True,exist_ok=True)
    output=ROOT/'reports/memory-bist-widths.json';output.unlink(missing_ok=True)
    source=ROOT/'soc/asic/wasmetal_memory_bist.sv';yosys=ROOT/'.cache/tools/usr/bin/yosys'
    inputs={str(p.relative_to(ROOT)):digest(p) for p in [source,Path(__file__).resolve(),yosys,ROOT/'tools/upstream.lock.json']}
    def execute(path,size,label):
        words=size//16;limit=words*80;target=directory/label;target.mkdir(exist_ok=True)
        script=target/'boundary.ys';netlist=target/'elaborated.json';logfile=target/'boundary.log'
        script.write_text(f'read_verilog -formal -sv {path}\n'+
            f'chparam -set RAM_BYTES {size} wasmetal_memory_bist\n'+
            f'prep -top wasmetal_memory_bist -flatten\nwrite_json {netlist}\n'+
            'sat -seq 3 -set-def-inputs -enable_undef -set-init-zero '+
            '-set reset 0 -set start 0 -set ready 1 -set fault 0 -set rdata 0 '+
            '-set-init state 1 -set-init phase 5 -set-init background_index 7 '+
            f"-set-init word_index 32'd{words-1} -set-init operation_count 64'd{limit-1} "+
            f"-prove completed_operations 64'd{limit} -prove done 1 -prove failed 0 -prove busy 0 "+
            '-prove-skip 2 -verify\n')
        with logfile.open('w') as log:
            run=subprocess.run([str(yosys),'-Q','-T','-s',str(script)],cwd=ROOT,
                               stdout=log,stderr=subprocess.STDOUT,timeout=90)
        return run,netlist,logfile,script
    checks=[]
    for size in CAPACITIES:
        run,netlist,log,script=execute(source,size,str(size));run.check_returncode()
        if 'SAT proof finished - no model found: SUCCESS!' not in log.read_text():raise ValueError('missing counter-boundary proof')
        module=json.loads(netlist.read_text())['modules']['wasmetal_memory_bist']
        bits=module['netnames']['operation_count']['bits'];width=(80*(size//16)).bit_length()
        if len(bits)!=width:raise ValueError('incorrect counter width')
        if module['ports']['completed_operations']['bits']!=bits+['0']*(64-width):
            raise ValueError('counter output is not the required zero extension')
        checks.append({'ram_bytes':size,'operation_limit':80*(size//16),'counter_bits':width,
                       'final_increment_proven':True,'netlist_sha256':digest(netlist),
                       'script_sha256':digest(script),'log_sha256':digest(log)})
        print('PASS capacity boundary',size,'bytes;',width,'counter bits',flush=True)
    controls=[];text=source.read_text()
    for name,old,new,size in [
        ('truncated-capacity','localparam logic [63:0] OPERATION_LIMIT=',
         'localparam logic [31:0] OPERATION_LIMIT=',2147483632),
        ('counter-too-narrow','CW=OPERATION_LIMIT>0 ? $clog2(OPERATION_LIMIT+1) : 1;',
         'CW=OPERATION_LIMIT>0 ? $clog2(OPERATION_LIMIT+1)-1 : 1;',16)]:
        if text.count(old)!=1:raise ValueError('ambiguous width fault: '+name)
        mutant=directory/(name+'.sv');mutant.write_text(text.replace(old,new))
        run,netlist,log,script=execute(mutant,size,name)
        if run.returncode==0 or 'proof did fail' not in log.read_text():raise ValueError('counter fault not rejected: '+name)
        controls.append({'name':name,'ram_bytes':size,'source_sha256':digest(mutant),
                         'script_sha256':digest(script),'log_sha256':digest(log)})
        print('REJECTED',name,flush=True)
    for name,sha in inputs.items():
        if digest(ROOT/name)!=sha:raise ValueError('counter-boundary input changed: '+name)
    report={'status':'passed','scope':'elaborated counter widths and final completion at selected capacity boundaries',
        'inputs':inputs,'checks':checks,'negative_controls':controls,'negative_controls_rejected':len(controls),
        'assumptions':'The boundary proof starts immediately before the final successful read with corresponding phase, word and count values; memory responds with zero.',
        'limitations':['The large-capacity fixtures do not execute full memory sweeps or prove reachability of their seeded boundary state.',
            'Unbounded safety and full simulated campaigns are recorded separately.',
            'No large SRAM allocation, physical implementation or hardware test is implied.'],
        'physical_hardware_tested':False}
    output.parent.mkdir(exist_ok=True);output.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
