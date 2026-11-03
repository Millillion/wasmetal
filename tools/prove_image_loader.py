#!/usr/bin/env python3
"""Prove image-store bounds and that partial/unverified uploads cannot execute."""
import json
from pathlib import Path
import subprocess
from prepare_standalone import ROOT,digest,load_profile

HARNESS='''
reg formal_started=0;
always @(posedge clk) begin
    if(!formal_started) assume(reset);
    formal_started<=1;
end
function automatic [31:0] formal_prefix(input [2:0] part);
    case(part)
        0: formal_prefix=0;
        1: formal_prefix=INSTRUCTION_DEPTH;
        2: formal_prefix=INSTRUCTION_DEPTH+FUNCTION_DEPTH;
        3: formal_prefix=INSTRUCTION_DEPTH+FUNCTION_DEPTH+TYPE_DEPTH;
        4: formal_prefix=INSTRUCTION_DEPTH+FUNCTION_DEPTH+TYPE_DEPTH+6*REGIONS_PER_KIND;
        default: formal_prefix=0;
    endcase
endfunction
always @* if(formal_started) begin
    assert((^{state,magic_index,checksum_index,header_index,reply_index,header_data,nonce,crc,
        received_crc,reply_image_crc,cursor,words_sent,reply_crc,reply_status,section,byte_index,
        idle_cycles,write_pending,checksum_verified,image_valid,word_section,word_index,word_data})!==1'bx);
    assert(state<=CHECKSUM && words_sent<=TOTAL_WORDS);
    if(state==HEADER) assert(section==0 && cursor==0 && byte_index==0 && words_sent==0);
    if(state==PAYLOAD) begin
        assert(section<5 && cursor<section_words(section) && 32'(byte_index)<section_bytes(section));
        assert(words_sent==formal_prefix(section)+cursor);
    end
    if(state==CHECKSUM) assert(words_sent==TOTAL_WORDS);
    if(state==REPLY && reply_status==0) assert(section==0 && cursor==0 && byte_index==0 && words_sent==0);
    if(state==REPLY && reply_status==1) assert(checksum_verified && words_sent==TOTAL_WORDS);
    if(checksum_verified) begin
        assert(received_crc==~crc);
        assert((state==REPLY && reply_status==1) || (state==SEARCH && image_valid));
    end
    if(image_valid) assert(checksum_verified && words_sent==TOTAL_WORDS && state==SEARCH);
    if(write_pending) assert(!image_valid && word_section<5 && word_index<section_words(word_section));
end
'''


def main():
    directory=ROOT/'build/formal-image-loader';directory.mkdir(parents=True,exist_ok=True)
    original=ROOT/'soc/loader/wasmetal_image_loader.sv'
    source=directory/'loader.sv';text=original.read_text();assert text.count('endmodule')==1
    source.write_text(text.replace('endmodule',HARNESS+'\nendmodule'))
    inputs=[original,Path(__file__).resolve(),source,ROOT/'soc/profile.json']
    hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs};results=[]
    profile=load_profile()
    small={'INSTRUCTION_DEPTH':4,'FUNCTION_DEPTH':2,'TYPE_DEPTH':8,'BOOT_DEPTH':4,'REGIONS_PER_KIND':2,'TIMEOUT_CYCLES':64}
    production={key.upper():profile[key] for key in ('instruction_depth','function_depth','type_depth','boot_depth','regions_per_kind')}
    production['TIMEOUT_CYCLES']=2000000
    def execute(path,name,params,depth=None):
        script=directory/f'{name}.ys';logfile=directory/f'{name}.log'
        proof='-seq 1 -tempinduct -maxsteps 12' if depth is None else f'-seq {depth}'
        script.write_text(f'''read_verilog -formal -sv -DWASMETAL_ASSERTIONS {path}
chparam -set PROFILE_TAG 128'h0f0e0d0c0b0a09080706050403020100 '''+
            ' '.join(f'-set {key} {value}' for key,value in params.items())+f''' wasmetal_image_loader
prep -top wasmetal_image_loader -flatten
sat {proof} -set-assumes -set-def-inputs -set-init-undef -enable_undef -prove-asserts -verify
''')
        with logfile.open('w') as log:
            result=subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-Q','-T','-s',str(script)],
                cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=180)
        return result,logfile.read_text()
    for name,params in [('small',small),('production',production)]:
        result,log=execute(source,name,params);result.check_returncode()
        if 'Induction step proven: SUCCESS!' not in log:raise ValueError('missing unbounded proof')
        results.append({'name':name,'parameters':params,'status':'proven'})
        print('PASS '+name+' loader safety induction',flush=True)
    rejected=[]
    for name,old,new,depth in [
        ('missing-word-reset','word_index<=0;word_data<=0;','word_index<=0;',3),
        ('commit-before-payload','nonce<=0;crc<=32\'hffffffff;image_valid<=0;checksum_verified<=0;',
         'nonce<=0;crc<=32\'hffffffff;image_valid<=1;checksum_verified<=0;',6),
    ]:
        text=source.read_text();assert text.count(old)==1
        negative=directory/f'{name}.sv';negative.write_text(text.replace(old,new))
        result,log=execute(negative,name,small,depth)
        if result.returncode==0 or 'proof did fail' not in log:raise ValueError('bad negative control: '+name)
        rejected.append(name)
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise RuntimeError('proof inputs changed')
    report={'status':'passed','scope':'unbounded upload authorization, write bounds and initialization safety; not complete CRC/data equivalence or CPU integration',
        'configurations':results,'environment':'initial reset; arbitrary binary bytes, RX strobes, aborts, TX backpressure and later resets',
        'properties':['no store write to an executable image','store writes stay within every section',
            'execution permission requires complete word count and verified checksum state','all state registers remain defined'],
        'reachable_state_lemmas':'proven jointly, not assumed','negative_controls_rejected':rejected,'inputs':hashes,
        'physical_hardware_tested':False}
    (ROOT/'reports/image-loader-proof.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
