// SPDX-License-Identifier: MIT
// Memory/clock adapter only. No Wasm instruction is executed in C++.
#include "Vwasmetal_core.h"
#include "verilated.h"
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

using Value = std::array<uint32_t,4>;
struct Instruction { uint32_t op=0,x=0,y=0,z=0,w=0; Value imm{}; };
struct Function { uint32_t entry=0,params=0,locals=0,results=0,type=0; };
static Value parse_value(const std::string& s) {
    Value out{}; size_t end=s.size();
    for (size_t i=0;i<4 && end;i++) {
        size_t begin=end>8?end-8:0;
        out[i]=static_cast<uint32_t>(std::stoul(s.substr(begin,end-begin),nullptr,16)); end=begin;
    }
    if (end) throw std::runtime_error("value wider than 128 bits");
    return out;
}
static std::string hex_value(const Value& v) {
    std::ostringstream o; o << std::hex;
    for (int i=3;i>=0;i--) { o.width(8); o.fill('0'); o << v[static_cast<size_t>(i)]; }
    return o.str();
}
template<class T> static void put(T& dst,const Value& v) { for(int i=0;i<4;i++) dst[i]=v[static_cast<size_t>(i)]; }
template<class T> static Value get(const T& src) { return {src[0],src[1],src[2],src[3]}; }

class Simulator {
public:
    Vwasmetal_core dut;
    std::vector<Instruction> code;
    std::vector<Function> functions;
    std::map<std::pair<uint32_t,uint64_t>,uint8_t> bytes;
    std::map<uint32_t,Value> globals;
    std::map<std::pair<uint32_t,uint64_t>,Value> tables;
    uint64_t cycles=0;
    unsigned wait_states=0;
    unsigned memory_wait=0;
    bool transaction_seen=false;
    void drive() {
        dut.insn_valid=dut.pc<code.size();
        Instruction i=dut.insn_valid?code[dut.pc]:Instruction{};
        dut.insn_op=i.op; dut.insn_x=i.x; dut.insn_y=i.y; dut.insn_z=i.z; dut.insn_w=i.w; put(dut.insn_imm,i.imm);
        dut.function_valid=dut.function_index<functions.size();
        Function f=dut.function_valid?functions[dut.function_index]:Function{};
        dut.function_entry=f.entry; dut.function_params=f.params; dut.function_locals=f.locals;
        dut.function_results=f.results; dut.function_type=f.type;
        dut.mem_ready=0; dut.mem_fault=0; put(dut.mem_rdata,Value{});
        if (!dut.mem_valid) { transaction_seen=false; memory_wait=0; return; }
        if (!transaction_seen) { transaction_seen=true; memory_wait=wait_states; }
        if (memory_wait) return;
        dut.mem_ready=1;
        Value data{};
        if (dut.mem_kind==1) data=globals[dut.mem_index];
        else if(dut.mem_kind==2) data=tables[{dut.mem_index,dut.mem_address}];
        else if (dut.mem_kind==0) {
            if (dut.mem_bytes==0 || dut.mem_bytes>16) { dut.mem_fault=1; return; }
            for(unsigned n=0;n<dut.mem_bytes;n++) {
                auto p=bytes.find({dut.mem_index,dut.mem_address+n});
                if(p!=bytes.end()) data[n/4] |= uint32_t(p->second) << ((n%4)*8);
            }
        } else { dut.mem_fault=1; return; }
        put(dut.mem_rdata,data);
    }
    void tick() {
        dut.clk=0; drive(); dut.eval(); drive(); dut.eval();
        bool transfer=dut.mem_valid && dut.mem_ready && !dut.mem_fault;
        if (transfer && dut.mem_write) {
            Value v=get(dut.mem_wdata);
            if(dut.mem_kind==1) globals[dut.mem_index]=v;
            else if(dut.mem_kind==2) tables[{dut.mem_index,dut.mem_address}]=v;
            else for(unsigned n=0;n<dut.mem_bytes;n++) {
                auto key=std::make_pair(dut.mem_index,dut.mem_address+n);
                uint8_t b=static_cast<uint8_t>(v[n/4] >> ((n%4)*8));
                if(b) bytes[key]=b; else bytes.erase(key);
            }
        }
        dut.clk=1; dut.eval(); cycles++;
        if(memory_wait) memory_wait--;
    }
    void reset() {
        code.clear(); functions.clear(); bytes.clear(); globals.clear(); tables.clear(); cycles=0;
        transaction_seen=false; memory_wait=0;
        dut.cmd_valid=0; dut.result_index=0; dut.reset=1; tick(); tick(); dut.reset=0; tick();
    }
    void command(unsigned kind,uint32_t index,Value data={},uint64_t aux=0) {
        if(dut.busy) throw std::runtime_error("command during execution");
        dut.cmd_kind=kind; dut.cmd_index=index; put(dut.cmd_data,data); dut.cmd_aux=aux;
        dut.cmd_valid=1; tick(); dut.cmd_valid=0;
    }
    void run(uint32_t index,unsigned argc,uint64_t limit) {
        uint64_t begin=cycles;
        command(0,index,{},argc);
        while(!dut.done && cycles-begin<limit) tick();
        if(!dut.done) { std::cout << "TIMEOUT " << dut.pc << ' ' << cycles-begin << '\n'; }
        else if(dut.trap) { std::cout << "TRAP " << unsigned(dut.trap) << ' ' << dut.pc << ' ' << cycles-begin << '\n'; }
        else {
            std::cout << "OK " << dut.result_count;
            for(uint32_t n=0;n<dut.result_count;n++) { dut.result_index=n; dut.eval(); std::cout << ' ' << hex_value(get(dut.result_data)); }
            std::cout << ' ' << cycles-begin << '\n';
        }
        std::cout.flush();
    }
};

int main(int argc,char** argv) {
    Verilated::commandArgs(argc,argv);
    try {
        auto sim=std::make_unique<Simulator>(); sim->reset();
        std::string line;
        while(std::getline(std::cin,line)) {
            if(line.empty()) continue;
            std::istringstream in(line); char op; in>>op;
            if(op=='Q') break;
            if(op=='X') sim->reset();
            else if(op=='I') {
                uint32_t index; Instruction i; std::string hex;
                in>>index>>i.op>>i.x>>i.y>>i.z>>i.w>>hex; i.imm=parse_value(hex);
                if(index>10000000) throw std::runtime_error("instruction image too large");
                if(sim->code.size()<=index) sim->code.resize(static_cast<size_t>(index)+1);
                sim->code[index]=i;
            } else if(op=='F') {
                uint32_t index; Function f; in>>index>>f.entry>>f.params>>f.locals>>f.results>>f.type;
                if(index>1000000) throw std::runtime_error("function image too large");
                if(sim->functions.size()<=index) sim->functions.resize(static_cast<size_t>(index)+1);
                sim->functions[index]=f;
            } else if(op=='A') {
                uint32_t index; std::string v; in>>index>>v; sim->command(1,index,parse_value(v));
            } else if(op=='M' || op=='T') {
                uint32_t index; uint64_t initial,maximum; unsigned wide;
                in>>index>>initial>>maximum>>wide;
                Value v{uint32_t(initial),uint32_t(initial>>32),uint32_t(maximum),uint32_t(maximum>>32)};
                sim->command(op=='M'?2:3,index,v,wide);
            } else if(op=='E') {
                uint32_t index; uint64_t address; std::string v; in>>index>>address>>v;
                sim->tables[{index,address}]=parse_value(v);
            } else if(op=='B') {
                uint32_t index; uint64_t address; std::string hex; in>>index>>address>>hex;
                if(hex.size()%2) throw std::runtime_error("odd byte string");
                for(size_t n=0;n<hex.size()/2;n++) {
                    auto key=std::make_pair(index,address+n);
                    uint8_t b=static_cast<uint8_t>(std::stoul(hex.substr(2*n,2),nullptr,16));
                    if(b) sim->bytes[key]=b; else sim->bytes.erase(key);
                }
            } else if(op=='G') {
                uint32_t index; std::string v; in>>index>>v; sim->globals[index]=parse_value(v);
            } else if(op=='H') {
                uint32_t index; in>>index;
                std::cout<<"GLOBAL "<<hex_value(sim->globals[index])<<'\n'; std::cout.flush();
            } else if(op=='R') {
                uint32_t index; unsigned args; uint64_t limit; in>>index>>args>>limit; sim->run(index,args,limit);
            } else if(op=='W') in>>sim->wait_states;
            else throw std::runtime_error("unknown harness command");
            if(in.fail()) throw std::runtime_error("malformed harness command: "+line);
        }
        sim->dut.final();
        return 0;
    } catch(const std::exception& e) { std::cerr<<"harness: "<<e.what()<<'\n'; return 1; }
}
