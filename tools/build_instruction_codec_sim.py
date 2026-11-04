#!/usr/bin/env python3
"""Build the complete native CPU with RTL instruction coding and a loaded-row audit.

The CPU receives decoded instruction fields. The C++ adapter also checks every
loaded row, including unreachable instructions, without advancing the clock.
"""
import json
import os
from pathlib import Path
import subprocess
from build_identity import begin,finish
from prepare_standalone import ROOT,digest


def main():
    root=ROOT
    d=root/'build/instruction-codec-sim';d.mkdir(parents=True,exist_ok=True)
    original=(root/'rtl/wasmetal_core.sv').read_text()
    inner=d/'wasmetal_unpacked_core.sv';inner.write_text(original.replace('module wasmetal_core #(','module wasmetal_unpacked_core #(',1))
    header=original.split(');\n',1)[0]
    header+=',\n    output wire [287:0] codec_word,\n    output wire codec_valid,\n    output wire [1:0] codec_layout\n);\n'
    params=['VALUE_DEPTH','CONTROL_DEPTH','CALL_DEPTH','MEMORY_COUNT','HEAP_SLOTS']
    layout=json.loads((root/'fpga/ports.json').read_text())
    ports=['clk']+[p['name'] for direction in ['input','output'] for p in layout[direction]]
    substitution={'insn_op':'codec_word[31:0]','insn_x':'codec_word[63:32]',
        'insn_y':'codec_word[95:64]','insn_z':'codec_word[127:96]',
        'insn_w':'codec_word[159:128]','insn_imm':'codec_word[287:160]'}
    wrapper=header+'''
    wire [287:0] original_word={insn_imm,insn_w,insn_z,insn_y,insn_x,insn_op};
    wire [193:0] encoded_word;
    wasmetal_instruction_encode encoder(original_word,encoded_word,codec_valid);
    wasmetal_instruction_decode decoder(encoded_word,codec_word);
    assign codec_layout=encoded_word[193:192];
    always @(posedge clk) if(!reset && insn_valid) begin
        assert(codec_valid);
        assert(codec_word==original_word);
    end
'''
    wrapper+='wasmetal_unpacked_core #('+','.join('.'+p+'('+p+')' for p in params)+') engine(\n'+',\n'.join('.'+p+'('+substitution.get(p,p)+')' for p in ports)+');\nendmodule\n'
    wrapped=d/'wasmetal_core.sv';wrapped.write_text(wrapper)
    cpp=(root/'sim/main.cpp').read_text()
    cpp=cpp.replace('#include <array>','#include <array>\n#include <fstream>\n#include <cstdlib>\n#include <unistd.h>')
    needle='    CoreModel dut;'
    assert cpp.count(needle)==1
    cpp=cpp.replace(needle,'''    CoreModel dut;
    uint64_t codec_rows_checked=0;
    std::array<uint64_t,4> codec_layouts{};
    std::set<uint32_t> codec_opcodes;
    void audit_instruction(const Instruction& i) {
        if(dut.clk!=0) throw std::runtime_error("instruction audit requires settled low clock");
        dut.insn_op=i.op;dut.insn_x=i.x;dut.insn_y=i.y;dut.insn_z=i.z;dut.insn_w=i.w;
        put(dut.insn_imm,i.imm);dut.eval();
        std::array<uint32_t,9> expected={i.op,i.x,i.y,i.z,i.w,i.imm[0],i.imm[1],i.imm[2],i.imm[3]};
        if(!dut.codec_valid) throw std::runtime_error("instruction is not losslessly encodable");
        for(unsigned n=0;n<9;n++) if(dut.codec_word[n]!=expected[n])
            throw std::runtime_error("instruction codec changed a loaded field");
        codec_rows_checked++;codec_layouts[dut.codec_layout]++;codec_opcodes.insert(i.op);
    }
    ~Simulator() {
        const char* directory=std::getenv("WASMETAL_CODEC_COVERAGE");
        if(!directory) return;
        std::ofstream out(std::string(directory)+"/"+std::to_string(getpid())+".jsonl",std::ios::app);
        if(!out) std::abort();
        out<<"{\\"rows_checked\\":"<<codec_rows_checked<<",\\"layouts\\":[";
        for(unsigned n=0;n<4;n++)out<<(n ? "," : "")<<codec_layouts[n];
        out<<"],\\"opcodes\\":[";bool first=true;
        for(auto op:codec_opcodes) {out<<(first ? "" : ",")<<op;first=false;}
        out<<"]}\\n";
    }''')
    needle='                sim->code[index]=i;';assert cpp.count(needle)==1
    cpp=cpp.replace(needle,needle+'\n                sim->audit_instruction(i);')
    harness=d/'main.cpp';harness.write_text(cpp)
    vendor=root/'third_party/hardfloat/source'
    sources=[root/'rtl/vendor.vlt',*[p for p in sorted((root/'rtl').glob('*.sv')) if p.name!='wasmetal_core.sv'],
        *sorted(vendor.glob('*.v')),vendor/'RISCV/HardFloat_specialize.v',inner,wrapped,
        root/'soc/loader/wasmetal_instruction_encode.sv',
        root/'soc/loader/wasmetal_instruction_decode.sv']
    binary=d/'obj/Vwasmetal_core';begin(binary,'native')
    p=Path(str(binary)+'.inputs.json');snapshot=json.loads(p.read_text())
    extra=[Path(__file__).resolve(),root/'fpga/ports.json',root/'tools/prepare_standalone.py',inner,wrapped,harness,*sources[-2:]]
    snapshot['extra_inputs']={str(p.relative_to(root)):digest(p) for p in extra}
    snapshot['variant']='complete CPU RTL with hardware instruction codec and every-loaded-row round-trip audit'
    p.write_text(json.dumps(snapshot,indent=2)+'\n')
    command=[str(root/'.cache/tools/usr/bin/verilator'),'-Wall','-Wno-UNUSEDSIGNAL',
        '--unroll-count','512','--assert','-DWASMETAL_ASSERTIONS','--top-module','wasmetal_core',
        '-I'+str(vendor),'-I'+str(vendor/'RISCV'),'--cc','--exe','--build','-j','4',
        '--Mdir',str(binary.parent),'-MAKEFLAGS','OPT_FAST=-O3','-CFLAGS',
        '-std=c++17 -O3 -Wall -Wextra -Werror -I'+str(root/'sim'),*map(str,sources),str(harness)]
    with (d/'build.log').open('w') as log:
        subprocess.run(command,cwd=root,env=dict(os.environ,VERILATOR_ROOT=str(root/'.cache/tools/usr/share/verilator')),
            stdout=log,stderr=subprocess.STDOUT,check=True)
    finish(binary);print(binary)


if __name__=="__main__":main()
