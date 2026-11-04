// SPDX-License-Identifier: MIT
// Independent March oracle, CPU transaction scoreboard and synchronous SRAM.
#include "Vwasmetal_startup_sram.h"
#include "verilated.h"
#include <array>
#include <cstdint>
#include <deque>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>
#ifndef TEST_BYTES
#define TEST_BYTES 131072
#endif
#ifndef TEST_LATENCY
#define TEST_LATENCY 3
#endif
#ifndef TEST_TIMEOUT
#define TEST_TIMEOUT 11
#endif
using Value=std::array<uint8_t,16>;
static void require(bool ok,const char* message){if(!ok)throw std::runtime_error(message);}
template<class W> static Value unpack(const W& input){Value v{};for(unsigned n=0;n<16;++n)v[n]=uint8_t(input[n/4]>>(8*(n%4)));return v;}
template<class W> static void pack(W& output,const Value& v){for(unsigned n=0;n<4;++n){output[n]=0;for(unsigned b=0;b<4;++b)output[n]|=uint32_t(v[n*4+b])<<(8*b);}}
struct Operation{bool write;unsigned word;Value data;};
static std::vector<Operation> sequence(){
    std::vector<Operation> result;
    for(unsigned background=0;background<8;++background){
        Value value{},inverse{};
        for(unsigned bit=0;bit<128;++bit)if(background<7 && ((bit>>background)&1U))value[bit/8]|=uint8_t(1U<<(bit%8));
        for(unsigned b=0;b<16;++b)inverse[b]=uint8_t(~value[b]);
        for(unsigned w=0;w<TEST_BYTES/16;++w)result.push_back({true,w,value});
        for(bool down:{false,true})for(bool complement:{false,true})for(unsigned n=0;n<TEST_BYTES/16;++n){
            const unsigned w=down ? TEST_BYTES/16-1-n : n;
            result.push_back({false,w,complement ? inverse : value});
            result.push_back({true,w,complement ? value : inverse});
        }
        for(unsigned w=0;w<TEST_BYTES/16;++w)result.push_back({false,w,value});
    }
    return result;
}
class Test{
    Vwasmetal_startup_sram dut;
    const std::vector<Operation> march=sequence();
    std::vector<uint8_t> memory=std::vector<uint8_t>(TEST_BYTES);
    struct Pending{unsigned delay;Value data;uint64_t epoch;};
    std::deque<Pending> pipeline;
    struct Request{bool active=false,issued=false,complete=false,write=false,legal=false;
        uint32_t address=0;uint16_t mask=0;Value data{},expected{};} request;
    size_t position=0;
    int64_t poison=-1;
    Value poisoned{};
    bool granted=false,corrupt_model=false;
    uint64_t epoch=0,random=0x8142a593;
    uint32_t next(){random^=random<<13;random^=random>>7;random^=random<<17;return uint32_t(random);}
    void mix(uint64_t v){trace^=v;trace*=1099511628211ULL;}
    void status(){
        if(dut.reset){require(!dut.cpu_enabled && !dut.cpu_ready && !dut.cpu_fault && !dut.sram_enable && !dut.sram_write,
            "startup reset did not isolate access");return;}
        if(dut.cpu_enabled){
            require(dut.test_done && !dut.test_failed && !dut.test_busy && position==march.size()
                && dut.completed_operations==march.size(),"startup enabled CPU before full test");
            if(!granted){for(auto v:memory)require(v==0,"startup handoff retained untested data");granted=true;++boots;}
        } else {
            require(!granted,"startup revoked successful ownership without reset");
            require(!dut.cpu_ready && !dut.cpu_fault && unpack(dut.cpu_rdata)==Value{},
                    "startup exposed CPU response before handoff");
        }
    }
public:
    uint64_t cycles=0,commands=0,test_commands=0,cpu_commands=0,cpu_responses=0,cpu_faults=0,
        boots=0,failures=0,resets=0,resets_with_pending_reads=0,old_reads_after_reset=0,
        held_valid_cycles=0,trace=1469598103934665603ULL;
    explicit Test(bool corrupt):corrupt_model(corrupt){for(unsigned n=0;n<TEST_BYTES;++n)memory[n]=uint8_t(0xa7+37*n+(n>>8));}
    void tick(){
        dut.clk=0;dut.eval();status();
        Value incoming{};bool issued_read=false;
        if(dut.cpu_ready){
            require(request.active && !request.complete,"startup duplicate or unsolicited CPU response");
            require(bool(dut.cpu_fault)==!request.legal,"startup CPU fault differs from address oracle");
            require(request.issued==request.legal,"startup response lacks exactly one legal macro command");
            require(unpack(dut.cpu_rdata)==request.expected,"startup CPU response data differs from SRAM oracle");
            request.complete=true;++cpu_responses;if(dut.cpu_fault)++cpu_faults;
            mix(0xcafe);mix(dut.cpu_fault);for(auto v:unpack(dut.cpu_rdata))mix(v);
        }
        if(dut.sram_enable){
            require(!dut.reset,"startup macro command during reset");
            const bool write=dut.sram_write;const unsigned address=unsigned(dut.sram_address)*16;
            require(uint64_t(address)+16<=TEST_BYTES,"startup macro address outside SRAM");
            const Value data=unpack(dut.sram_wdata);const uint16_t mask=dut.sram_byte_enable;
            if(dut.cpu_enabled){
                require(request.active && !request.complete && !request.issued && request.legal,
                        "startup unsolicited or duplicate CPU macro command");
                require(address==request.address && write==request.write,"startup CPU macro operation mismatch");
                require(mask==request.mask,"startup CPU macro byte mask mismatch");
                require(data==request.data,"startup CPU macro write data mismatch");
                request.issued=true;++cpu_commands;
                if(!write)for(unsigned n=0;n<16;++n)request.expected[n]=memory.at(address+n);
            } else {
                require(position<march.size(),"startup repeated a completed memory test");
                const auto& expected=march.at(position);
                require(address==expected.word*16 && write==expected.write,"startup March command order mismatch");
                require(mask==0xffff,"startup March byte mask mismatch");
                if(write)require(data==expected.data,"startup March data mismatch");
                ++test_commands;
            }
            ++commands;mix(address);mix(write);mix(mask);
            if(write){for(unsigned n=0;n<16;++n){if(mask&(1U<<n))memory.at(address+n)=data[n];mix(data[n]);}}
            else {
                for(unsigned n=0;n<16;++n)incoming[n]=memory.at(address+n);
                if(corrupt_model || (!dut.cpu_enabled && int64_t(position)==poison)){
                    incoming[position%16]^=uint8_t(1U<<(position%8));poisoned=incoming;
                }
                for(auto v:incoming){mix(v);}issued_read=true;
            }
            if(!dut.cpu_enabled)++position;
        }
        dut.clk=1;dut.eval();++cycles;
        Value output{};for(unsigned n=0;n<16;++n)output[n]=uint8_t(0xc3+cycles+17*n);
        for(auto& item:pipeline)--item.delay;
        if(!pipeline.empty() && pipeline.front().delay==0){output=pipeline.front().data;
            if(pipeline.front().epoch!=epoch){++old_reads_after_reset;}pipeline.pop_front();}
        if(issued_read){if(TEST_LATENCY==1)output=incoming;else pipeline.push_back({TEST_LATENCY-1,incoming,epoch});}
        pack(dut.sram_rdata,output);dut.eval();dut.clk=0;dut.eval();status();
        mix(dut.cpu_enabled);mix(dut.test_done);mix(dut.test_failed);mix(dut.completed_operations);
    }
    void queue(bool write,uint32_t address,uint16_t mask,const Value& data){
        require(!request.active,"startup test double CPU submission");
        request={};request.active=true;request.write=write;request.address=address;request.mask=mask;request.data=data;
        request.legal=address%16==0 && uint64_t(address)+16<=TEST_BYTES && mask!=0;
        dut.cpu_valid=1;dut.cpu_write=write;dut.cpu_address=address;dut.cpu_mask=mask;pack(dut.cpu_wdata,data);dut.eval();
    }
    void begin(int64_t corrupt=-1){
        if(!pipeline.empty())++resets_with_pending_reads;
        ++epoch;++resets;dut.reset=1;dut.cpu_valid=0;dut.eval();status();
        const auto saved=memory;const auto count=commands;request={};granted=false;position=0;poison=corrupt;poisoned={};
        tick();tick();require(memory==saved && commands==count,"startup reset changed retained SRAM");
        require(!dut.test_done && !dut.test_failed && dut.completed_operations==0,"startup reset retained test status");
        dut.reset=0;
        Value value{};for(unsigned n=0;n<16;++n)value[n]=uint8_t(0x93+n*11);
        // Queue a write before the first startup clock. It must stay blocked
        // throughout the destructive test and execute exactly once afterwards.
        queue(true,TEST_BYTES-16,0xa55a,value);
    }
    void finish_cpu(unsigned hold=0){
        const auto start=cycles;
        while(!request.complete && cycles-start<TEST_LATENCY+16ULL)tick();
        require(request.complete,"startup CPU request did not complete");
        const auto before=commands;
        for(unsigned n=0;n<hold;++n){tick();++held_valid_cycles;require(commands==before,"startup repeated held-valid CPU request");}
        dut.cpu_valid=0;tick();tick();request={};
    }
    uint64_t finish_boot(int64_t corrupt=-1){
        const auto start=cycles;const auto limit=march.size()*(TEST_LATENCY+12ULL)+32;
        while(!dut.test_done && cycles-start<limit)tick();
        require(dut.test_done && !dut.test_busy,"startup memory test did not complete");
        const int64_t timeout=TEST_TIMEOUT<3 ? 0 : (TEST_TIMEOUT<TEST_LATENCY+3 ? TEST_BYTES/16 : -1);
        const int64_t failure=timeout>=0 ? timeout : corrupt;
        if(failure<0){require(dut.cpu_enabled && !dut.test_failed,"startup healthy memory did not grant CPU");finish_cpu(7);}
        else {
            const auto& expected=march.at(size_t(failure));
            require(dut.test_failed && !dut.cpu_enabled && dut.error_code==(timeout>=0 ? 3U : 1U),"startup failed test did not block CPU");
            require(position==size_t(failure+1) && dut.completed_operations==uint64_t(failure+1),"startup failed test did not drain exactly one access");
            require(dut.error_address==expected.word*16 && unpack(dut.expected_data)==expected.data,
                    "startup wrong first-failure diagnostic");
            require(unpack(dut.observed_data)==(timeout>=0 ? Value{} : poisoned),"startup wrong failed-read observation");
            const auto before=commands;
            for(unsigned n=0;n<17;++n){tick();require(commands==before && !dut.cpu_enabled && !dut.cpu_ready,"startup failed memory accepted CPU request");}
            ++failures;
        }
        return cycles-start;
    }
    void cpu_suite(unsigned count){
        for(unsigned n=0;n<count;++n){
            Value data{};for(auto& v:data)v=uint8_t(next());
            const bool write=(next()&1)!=0;uint32_t address=16*(next()%(TEST_BYTES/16));uint16_t mask=uint16_t(next());
            if(n%13==0)mask=uint16_t(1U<<(n%16));
            if(n%29==0)mask=0xffff;
            if(n%41==0)address=TEST_BYTES;
            if(n%43==0)address|=1;
            if(n%47==0)mask=0;
            if(n%53==0)address=0xfffffff0U;
            queue(write,address,mask,data);finish_cpu(n%5);
        }
    }
    void exercise(){
        begin();const auto boot_length=finish_boot();
        if(TEST_TIMEOUT<TEST_LATENCY+3){
            for(unsigned offset=0;offset<TEST_LATENCY+7U;++offset){begin();for(unsigned n=0;n<offset;++n)tick();begin();finish_boot();}
            return;
        }
        cpu_suite(2048);begin();finish_boot();cpu_suite(64);
        if(TEST_BYTES<=80){
            for(size_t n=0;n<march.size();++n)if(!march[n].write){begin(int64_t(n));finish_boot(int64_t(n));}
            // Cover reset at every startup and handoff clock; memory and old
            // read responses survive reset, while ownership is revoked.
            for(uint64_t offset=0;offset<boot_length;++offset){begin();for(uint64_t n=0;n<offset;++n)tick();begin();finish_boot();}
        } else {
            for(size_t n:{size_t(TEST_BYTES/16),march.size()-1}){begin(int64_t(n));finish_boot(int64_t(n));}
            for(unsigned offset:{0U,3U,TEST_LATENCY+3U}){begin();for(unsigned n=0;n<offset;++n)tick();begin();finish_boot();}
        }
        // Interrupt both normal CPU reads and writes at every pipeline age.
        const unsigned maximum=TEST_BYTES<=272 ? TEST_LATENCY+7 : 2;
        for(bool write:{false,true})for(unsigned age=0;age<maximum;++age){
            begin();finish_boot();Value data{};data.fill(0x6d);queue(write,0,0xffff,data);
            for(unsigned n=0;n<age;++n){tick();}begin();finish_boot();
        }
        if(TEST_LATENCY>1 && TEST_BYTES<=80)require(resets_with_pending_reads && old_reads_after_reset,
            "startup reset checks did not deliver stale macro reads");
    }
};
int main(int argc,char** argv){
    Verilated::commandArgs(argc,argv);bool corrupt=false;
    for(int n=1;n<argc;++n){if(std::string(argv[n])=="--corrupt-read")corrupt=true;else throw std::runtime_error("unknown startup argument");}
    try{auto test=std::make_unique<Test>(corrupt);test->exercise();
        std::cout<<"{\"status\":\"passed\",\"cycles\":"<<test->cycles<<",\"macro_commands\":"<<test->commands
            <<",\"test_commands\":"<<test->test_commands<<",\"cpu_commands\":"<<test->cpu_commands
            <<",\"cpu_responses\":"<<test->cpu_responses<<",\"cpu_faults\":"<<test->cpu_faults
            <<",\"successful_boots\":"<<test->boots<<",\"failed_boots\":"<<test->failures<<",\"resets\":"<<test->resets
            <<",\"resets_with_pending_reads\":"<<test->resets_with_pending_reads<<",\"old_reads_after_reset\":"<<test->old_reads_after_reset
            <<",\"held_valid_cycles\":"<<test->held_valid_cycles<<",\"trace\":"<<test->trace<<"}\n";
    }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}
}
