#!/usr/bin/env python3
"""Execute UART-uploaded programs with initially unknown storage in Icarus."""
import json
from pathlib import Path
import re
import subprocess
import time

from build_standalone_sim import sources
from check_loadable import parse_frames
from check_standalone import SELFTEST_VALUES, check_expected
from prepare_standalone import ROOT, prepare, load_profile, digest
from program_upload import encode, profile_tag
from standalone_support import generate_parameters, parameters, verify_image, verify_simulator

BUILD=ROOT/'build/loadable-four-state'
BENCH=ROOT/'tests/standalone/loadable_four_state.sv'
TOOLS=ROOT/'.cache/tools/usr'
PASS='PASS complete programmable four-state: 2 images, 1 interrupted upload'
SECOND='''(module (memory 1 1)
 (func (export "main") (result i32 f32 f64 f32 f64 f32 f64 v128 v128 f64)
  i32.const 32 i32.load
  f32.const -0.5 f32.nearest
  f64.const 1.5 f64.nearest
  f32.const -0.25 f32.ceil
  f64.const -0.25 f64.floor
  f32.const 1.875 f32.trunc
  f64.const 0.25 f64.ceil
  v128.const f32x4 -0.5 1.5 -0.25 2.75 f32x4.nearest
  v128.const f64x2 -0.25 2.75 f64x2.floor
  f64.const nan:0x1 f64.trunc))
'''
SECOND_VALUES=[0,0x80000000,0x4000000000000000,0x80000000,0xbff0000000000000,
    0x3f800000,0x3ff0000000000000,
    sum(v<<(32*i) for i,v in enumerate((0x80000000,0x40000000,0x80000000,0x40400000))),
    0xbff0000000000000 | (0x4000000000000000<<64),0x7ff8000000000000]


def checked(command,log,timeout=1800):
    with log.open('w') as out:
        result=subprocess.run(command,cwd=ROOT,stdout=out,stderr=subprocess.STDOUT,timeout=timeout)
    return result,log.read_text()


def compile_model(label,source,includes,defines=()):
    executable=BUILD/(label+'.vvp');log=BUILD/(label+'-compile.log')
    vendor=ROOT/'third_party/hardfloat/source'
    command=[str(TOOLS/'bin/iverilog'),'-B'+str(TOOLS/'lib/x86_64-linux-gnu/ivl'),
        '-g2012','-DWASMETAL_ASSERTIONS',*['-D'+name for name in defines],'-s','loadable_four_state',
        '-I'+str(vendor),'-I'+str(vendor/'RISCV'),'-I'+str(BUILD),'-I'+str(ROOT/'build'),
        '-o',str(executable),*map(str,source),str(BENCH)]
    identities={str(p.relative_to(ROOT)):digest(p) for p in source+[BENCH,*includes]}
    result,_=checked(command,log,timeout=300)
    if result.returncode:raise RuntimeError('Icarus compilation failed: '+str(log))
    if any(digest(ROOT/p)!=h for p,h in identities.items()):raise RuntimeError('four-state compilation input changed')
    return executable,{'inputs':identities,'command':command,'compile_log_sha256':digest(log),
        'executable_sha256':digest(executable)}


def main():
    started=time.monotonic();BUILD.mkdir(parents=True,exist_ok=True)
    report_path=ROOT/'reports/loadable-four-state.json';report_path.unlink(missing_ok=True)
    generated_parameters=generate_parameters()
    profile=load_profile();params={**parameters(profile),'UART_TICKS':4,'UPLOAD_TIMEOUT_CYCLES':4096,
        'PROFILE_TAG':f"128'h{int.from_bytes(profile_tag(profile),'little'):032x}"}
    source=[p for p in sources() if p.suffix in ('.v','.sv')]
    vendor=ROOT/'third_party/hardfloat/source'
    dependencies=[*source,*sorted(vendor.rglob('*.vi')),BENCH,Path(__file__).resolve(),
        ROOT/'soc/profile.json',ROOT/'tools/upstream.lock.json',ROOT/'tools/build_standalone_sim.py',
        ROOT/'tools/prepare_standalone.py',ROOT/'tools/standalone_support.py',ROOT/'tools/program_upload.py',
        ROOT/'tools/check_loadable.py',ROOT/'tools/check_standalone.py',
        TOOLS/'bin/iverilog',TOOLS/'bin/vvp',generated_parameters,
        ROOT/'examples/standalone/selftest.wat']
    inputs={str(p.relative_to(ROOT)):digest(p) for p in dependencies}
    instance=BUILD/'instance.svh'
    instance.write_text('wasmetal_loadable #('+','.join(f'.{k}({v})' for k,v in params.items())+
        ') dut(.clk(clk),.reset(reset),.rx(rx),.tx(tx),.finished(finished),.error(error),.image_valid(image_valid));\n')
    checks=[];words=0;bits=0
    def expect_unknown(expression,depth,width):
        nonlocal words,bits
        checks.append(f'for(integer i=0;i<{depth};i=i+1) begin\n'
            f' if({expression}[i] !== {{{width}{{1\'bx}}}}) $fatal(1,"INITIAL_MEMORY_NOT_X");\n'
            ' checked_words=checked_words+1;\nend\n')
        words+=depth;bits+=depth*width
    for name,depth,width in [('instructions',profile['instruction_depth'],288),
        ('functions',profile['function_depth'],160),('types',profile['type_depth'],profile['type_depth']),
        ('boot',profile['boot_depth'],232),('memory.regions',6*profile['regions_per_kind'],64)]:
        expect_unknown('dut.execution.'+name,depth,width)
    program_checks=len(checks)
    bank_words=min(2048,profile['ram_bytes']//16)
    for bank in range(profile['ram_bytes']//(16*bank_words)):
        for lane in range(16):
            expect_unknown(f'dut.execution.memory.ram_backend.banks[{bank}].lanes[{lane}].storage',bank_words,8)
    unknown=BUILD/'unknown_storage.svh';unknown.write_text(''.join(checks))
    unknown_ram=BUILD/'unknown_ram.svh';unknown_ram.write_text(''.join(checks[program_checks:]))
    rom_harness=BUILD/'rom_harness.sv'
    rom_params={**parameters(profile),'UART_TICKS':4,'IMAGE_DIR':json.dumps(str(BUILD/'image-0'))}
    rom_harness.write_text('module wasmetal_rom_smoke_harness(input wire clk,reset,rx, '
        'output wire tx,finished,error,image_valid);\nassign image_valid=1\'b1;\n'
        'wasmetal_standalone #('+','.join(f'.{k}({v})' for k,v in rom_params.items())+
        ') execution(.clk(clk),.reset(reset),.tx(tx),.finished(finished),.error(error),'
        '.image_write_valid(1\'b0),.image_section(3\'b0),.image_index(32\'b0),'
        f'.image_word({max(profile["type_depth"],288)}\'b0),.result_valid(),.result_byte(),.result_ready(1\'b0));\nendmodule\n')
    second=BUILD/'zero-and-rounding.wat';second.write_text(SECOND)
    programs=[ROOT/'examples/standalone/selftest.wat',second]
    expected=[SELFTEST_VALUES,SECOND_VALUES];packets=[];stimuli=[]
    for index,program in enumerate(programs):
        directory=BUILD/f'image-{index}';prepare(program,directory)
        upload=encode(directory,0x574d465300000000+index)
        packet=BUILD/f'image-{index}.wmu';packet.write_bytes(upload.bytes());packets.append(packet)
        stimulus=BUILD/f'image-{index}.hex';stimulus.write_text(''.join(f'{b:02x}\n' for b in upload.bytes()));stimuli.append(stimulus)
    manifests=[verify_image(BUILD/f'image-{i}') for i in range(2)]
    stimulus_inputs={str(p.relative_to(ROOT)):digest(p) for p in
        [instance,unknown,unknown_ram,rom_harness,second,*packets,*stimuli,
         *[BUILD/f'image-{i}/manifest.json' for i in range(2)]]}
    lengths=[p.stat().st_size for p in packets]
    if len(set(lengths))!=1:raise RuntimeError('fixed-layout images must have equal payload sizes')
    # The previous self-test wrote 0x33221111 here. The second program must
    # observe zero at the same physical location after its fresh boot clear.
    old_region=int((BUILD/'image-0/regions.hex').read_text().splitlines()[1],16)
    new_region=int((BUILD/'image-1/regions.hex').read_text().splitlines()[0],16)
    if (old_region&0xffffffff)!=(new_region&0xffffffff):raise RuntimeError('warm-clear programs do not overlap')
    binary=ROOT/'build/loadable-sim/Vwasmetal_loadable';identity=verify_simulator(binary)
    if identity['backend']!='loadable-rtl' or identity['uart_ticks']!=4 or identity['profile']!=profile:
        raise RuntimeError('matching native programmable simulator is required')
    command=[str(binary),'--upload',str(packets[0]),'--partial',str(packets[1]),'70','--upload',str(packets[1])]
    result,text=checked(command,BUILD/'native.log')
    if result.returncode:raise RuntimeError('native reference failed')
    native=[json.loads(line) for line in text.splitlines()]
    if len(native)!=3:raise RuntimeError('native reference omitted a transaction')
    for i,values in ((0,expected[0]),(2,expected[1])):
        replies,frames=parse_frames(native[i]['uart'])
        if [r['status'] for r in replies]!=['ready','committed'] or len(frames)!=1:raise RuntimeError('native UART framing differs')
        check_expected(frames[0],values)
    # The native reset deliberately clears its receiver, including the ready
    # acknowledgment. The Icarus observer preserves that pre-reset transcript.
    if native[1]['uart'] or not native[1]['interrupted']:raise RuntimeError('partial native upload did not reset')
    arguments=[f'+image{i}={p}' for i,p in enumerate(stimuli)]+[f'+length={lengths[0]}']+[
        f'+expected{i}={40+12+16*len(v)}' for i,v in enumerate(expected)]
    # Exercise the production ROM configuration first: it reaches CPU execution
    # without the millions of serial-upload clocks in the full campaign.
    rom_model,rom_identity=compile_model('rom',source+[rom_harness],[unknown_ram,generated_parameters],
        defines=['WASMETAL_ROM_SMOKE'])
    rom_log=BUILD/'rom.log';result,text=checked([str(TOOLS/'bin/vvp'),'-i',str(rom_model),*arguments],rom_log)
    rom_uart=re.findall(r'^UART 0 ([0-9a-f]+)$',text,re.M)
    if (result.returncode or 'PASS complete ROM four-state boot' not in text or
        re.search(r'\b(?:ERROR|FATAL):',text) or rom_uart!=[native[0]['uart'][80:]] or
        f'UNKNOWN_STORAGE {profile["ram_bytes"]}\n' not in text):
        raise RuntimeError('four-state ROM smoke failed: '+str(rom_log))
    print('PASS production ROM four-state boot and exact native result frame',flush=True)
    executable,model=compile_model('complete',source,[instance,unknown,generated_parameters])
    log=BUILD/'complete.log';result,text=checked([str(TOOLS/'bin/vvp'),'-i',str(executable),*arguments],log,timeout=14400)
    if result.returncode or PASS not in text or re.search(r'\b(?:ERROR|FATAL):',text):
        raise RuntimeError('four-state execution failed: '+str(log))
    if f'UNKNOWN_STORAGE {words}\n' not in text:raise RuntimeError('initial unknown storage was not fully checked')
    observed=re.findall(r'^UART ([0-2]) ([0-9a-f]+)$',text,re.M)
    if [i for i,_ in observed]!=['0','1','2']:raise RuntimeError('four-state transaction coverage differs')
    for (i,uart),reference in zip(observed,native):
        if i!='1' and uart!=reference['uart']:raise RuntimeError('Icarus/native UART or invocation cycles differ: '+i)
        replies,frames=parse_frames(uart)
        if i=='1' and ([r['status'] for r in replies]!=['ready'] or frames):
            raise RuntimeError('partial four-state upload executed')
        if frames:
            values=expected[0 if i=='0' else 1];check_expected(frames[0],values)
            wrong=dict(frames[0],values=[values[0]^1,*values[1:]])
            try:check_expected(wrong,values)
            except AssertionError:pass
            else:raise RuntimeError('independent result oracle accepted corruption')
    negatives={}
    for name,extra in [('known-initial-word',['+known-initial-word'])]:
        neg_log=BUILD/(name+'.log');run,output=checked([str(TOOLS/'bin/vvp'),str(executable),*arguments,*extra],neg_log)
        if run.returncode==0 or 'INITIAL_MEMORY_NOT_X' not in output:raise RuntimeError('zero-initialization assumption was not rejected')
        negatives[name]={'rejected':True,'log_sha256':digest(neg_log)}
    wrapper=ROOT/'soc/loader/wasmetal_loadable.sv';body=wrapper.read_text();needle='.reset(reset || !image_valid)'
    if body.count(needle)!=1:raise RuntimeError('review boot-gating mutation')
    mutation=BUILD/'uncommitted.sv';mutation.write_text(body.replace(needle,'.reset(reset)'))
    bad_model,bad_identity=compile_model('uncommitted',[mutation if p==wrapper else p for p in source],
        [instance,unknown,generated_parameters])
    neg_log=BUILD/'uncommitted.log';run,output=checked([str(TOOLS/'bin/vvp'),str(bad_model),*arguments,'+boot-gating-negative'],neg_log)
    if run.returncode==0 or 'BOOT_BEFORE_COMMIT' not in output:raise RuntimeError('uncommitted boot was not rejected')
    negatives['boot-before-commit']={'rejected':True,'model':bad_identity,'log_sha256':digest(neg_log)}
    if verify_simulator(binary)!=identity:raise RuntimeError('native reference changed')
    if any(digest(ROOT/p)!=h for p,h in inputs.items()):raise RuntimeError('four-state source changed')
    if any(digest(ROOT/p)!=h for p,h in stimulus_inputs.items()):raise RuntimeError('four-state stimulus changed')
    if [verify_image(BUILD/f'image-{i}') for i in range(2)]!=manifests:raise RuntimeError('prepared images changed')
    if digest(executable)!=model['executable_sha256']:raise RuntimeError('four-state model changed')
    if digest(rom_model)!=rom_identity['executable_sha256']:raise RuntimeError('four-state ROM model changed')
    report={'status':'passed','scope':'complete programmable RTL in Icarus, production capacities, accelerated UART; no analog or physical-board claim',
        'inputs':inputs,'model':model,'rom_model':rom_identity,'native_model':identity,'profile':profile,
        'rom_smoke_matches_native_result_frame':True,
        'initially_unknown_words_checked':words,'initially_unknown_bits_checked':bits,
        'unknown_scope':'all five program stores and every backing-RAM byte before upload; other CPU state uses ordinary four-state semantics',
        'native_transactions':native,'four_state_uart_transactions':dict(observed),'images':manifests,
        'completed_upload_uart_and_invocation_cycles_match_native':True,
        'warm_clear_physical_address':(old_region&0xffffffff)+32,'expected_results':expected,
        'negative_controls':negatives,'corrupt_result_oracle_rejected':True,
        'artifacts':{**stimulus_inputs,**{str(p.relative_to(ROOT)):digest(p) for p in [log,rom_log,BUILD/'native.log']}},
        'elapsed_seconds':time.monotonic()-started,'physical_hardware_tested':False}
    report_path.parent.mkdir(exist_ok=True);report_path.write_text(json.dumps(report,indent=2)+'\n')
    print(f'PASS complete four-state programmable CPU; {words} initially unknown words, two images, interrupted upload and two rejected mutations')


if __name__=='__main__':main()
