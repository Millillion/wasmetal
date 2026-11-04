// SPDX-License-Identifier: MIT
// Independent macro-port sequence oracle, SRAM storage and read-latency model.
#include "Vwasmetal_bist_sram.h"
#include "verilated.h"
#include <array>
#include <cstdint>
#include <deque>
#include <iostream>
#include <limits>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>
#ifndef TEST_BYTES
#define TEST_BYTES 131072
#endif
#ifndef TEST_LATENCY
#define TEST_LATENCY 1
#endif
#ifndef TEST_TIMEOUT
#define TEST_TIMEOUT 1024
#endif
using Value=std::array<uint8_t,16>;
static void require(bool condition,const char* message){if(!condition)throw std::runtime_error(message);}
template<class Wide> static Value unpack(const Wide& input){
    Value value{};for(unsigned n=0;n<16;++n)value[n]=uint8_t(input[n/4]>>((n%4)*8));return value;
}
template<class Wide> static void pack(Wide& output,const Value& value){
    for(unsigned n=0;n<4;++n){output[n]=0;for(unsigned b=0;b<4;++b)output[n]|=uint32_t(value[n*4+b])<<(8*b);}
}
struct Operation {bool write;unsigned word;Value data;};
static std::vector<Operation> operations(){
    std::vector<Operation> result;
    for(unsigned background=0;background<8;++background){
        Value data{},inverse{};
        for(unsigned bit=0;bit<128;++bit)if(background<7 && ((bit>>background)&1U))data[bit/8]|=uint8_t(1U<<(bit%8));
        for(unsigned n=0;n<16;++n)inverse[n]=uint8_t(~data[n]);
        for(unsigned word=0;word<TEST_BYTES/16;++word)result.push_back({true,word,data});
        for(bool descending:{false,true})for(bool complemented:{false,true}){
            for(unsigned index=0;index<TEST_BYTES/16;++index){
                const unsigned word=descending ? TEST_BYTES/16-1-index : index;
                result.push_back({false,word,complemented ? inverse : data});
                result.push_back({true,word,complemented ? data : inverse});
            }
        }
        for(unsigned word=0;word<TEST_BYTES/16;++word)result.push_back({false,word,data});
    }
    return result;
}
class Test {
    Vwasmetal_bist_sram dut;
    const std::vector<Operation> sequence=operations();
    std::vector<uint8_t> memory=std::vector<uint8_t>(TEST_BYTES);
    struct Pending {unsigned delay;Value value;uint64_t epoch;};
    std::deque<Pending> pipeline;
    size_t position=0;
    int64_t poison=-1;
    Value poisoned{};
    bool corrupt_all;
    uint64_t epoch=0;
    void mix(uint64_t value){trace^=value;trace*=1099511628211ULL;}
public:
    uint64_t cycles=0,commands=0,reads=0,writes=0,resets=0,campaigns=0,detected=0,
        resets_with_pending_reads=0,old_reads_after_reset=0,held_start_cycles=0,
        trace=1469598103934665603ULL;
    explicit Test(bool corrupt):corrupt_all(corrupt){
        for(unsigned n=0;n<TEST_BYTES;++n)memory[n]=uint8_t(0xa7+37*n+(n>>8));
    }
    void tick(){
        dut.clk=0;dut.eval();
        const bool enabled=dut.sram_enable,writing=dut.sram_write;
        Value incoming{};bool issued_read=false;
        if(enabled){
            require(!dut.reset,"BIST SRAM command during reset");
            require(position<sequence.size(),"BIST SRAM extra macro command");
            const auto& expected=sequence.at(position);
            require(dut.sram_address==expected.word,"BIST SRAM wrong macro address or order");
            require(writing==expected.write,"BIST SRAM wrong macro operation");
            require(dut.sram_byte_enable==0xffff,"BIST SRAM incomplete macro byte enables");
            const unsigned address=unsigned(dut.sram_address)*16;
            require(uint64_t(address)+16<=TEST_BYTES,"BIST SRAM macro address out of range");
            mix(position);mix(address);mix(writing);++commands;
            if(writing){
                const Value value=unpack(dut.sram_wdata);
                require(value==expected.data,"BIST SRAM write differs from March oracle");
                for(unsigned n=0;n<16;++n){memory.at(address+n)=value[n];mix(value[n]);}++writes;
            } else {
                for(unsigned n=0;n<16;++n)incoming[n]=memory.at(address+n);
                if(corrupt_all || int64_t(position)==poison){
                    incoming[position%16]^=uint8_t(1U<<(position%8));poisoned=incoming;
                }
                for(auto value:incoming)mix(value);
                issued_read=true;++reads;
            }
            ++position;
        }
        dut.clk=1;dut.eval();++cycles;
        Value output{};for(unsigned n=0;n<16;++n)output[n]=uint8_t(0xc3+cycles+17*n);
        for(auto& pending:pipeline)--pending.delay;
        if(!pipeline.empty() && pipeline.front().delay==0){
            output=pipeline.front().value;
            if(pipeline.front().epoch!=epoch)++old_reads_after_reset;
            pipeline.pop_front();
        }
        if(issued_read){
            if(TEST_LATENCY==1)output=incoming;
            else pipeline.push_back({TEST_LATENCY-1,incoming,epoch});
        }
        pack(dut.sram_rdata,output);dut.eval();dut.clk=0;dut.eval();
        mix(dut.done);mix(dut.failed);mix(dut.busy);mix(dut.error_code);mix(dut.completed_operations);
    }
    void reset(){
        if(!pipeline.empty())++resets_with_pending_reads;
        ++epoch;dut.start=0;dut.reset=1;dut.eval();
        require(!dut.sram_enable && !dut.sram_write,"BIST SRAM reset did not isolate macro strobes");
        const auto before=memory;const uint64_t old_commands=commands;
        tick();tick();
        require(commands==old_commands && memory==before,"BIST SRAM reset modified retained memory");
        require(!dut.done && !dut.failed && !dut.busy && dut.completed_operations==0,
                "BIST SRAM reset retained test status");
        dut.reset=0;tick();++resets;
        // Neither SRAM contents nor the outstanding read pipeline is cleared.
    }
    void begin(int64_t corrupt=-1,bool hold=false){
        position=0;poison=corrupt;poisoned={};dut.start=1;tick();
        require(dut.busy && !dut.done && !dut.failed,"BIST SRAM start was not accepted");
        if(!hold){dut.start=0;dut.eval();}
    }
    uint64_t run(int64_t corrupt=-1,bool hold=false){
        const uint64_t start=cycles;begin(corrupt,hold);
        const uint64_t limit=sequence.size()*(TEST_LATENCY+12ULL)+32;
        while(!dut.done && cycles-start<limit)tick();
        require(dut.done && !dut.busy,"BIST SRAM campaign did not drain and complete");
        const int64_t timeout_at=TEST_TIMEOUT<3 ? 0 :
            (TEST_TIMEOUT<TEST_LATENCY+3 ? TEST_BYTES/16 : -1);
        const int64_t failure=timeout_at>=0 ? timeout_at : corrupt;
        if(failure<0){
            require(!dut.failed && dut.error_code==0,"BIST SRAM unexpected failure");
            require(position==sequence.size() && dut.completed_operations==sequence.size(),
                    "BIST SRAM missing commands or completions");
            require(unpack(dut.expected_data)==Value{} && unpack(dut.observed_data)==Value{},
                    "BIST SRAM healthy run retained error diagnostics");
            for(auto byte:memory)require(byte==0,"BIST SRAM successful test left nonzero contents");
        } else {
            const auto& expected=sequence.at(size_t(failure));
            require(dut.failed && dut.error_code==(timeout_at>=0 ? 3U : 1U),"BIST SRAM missing or wrong failure");
            require(position==size_t(failure+1) && dut.completed_operations==uint64_t(failure+1),
                    "BIST SRAM failure did not stop after draining one access");
            require(dut.error_address==expected.word*16 && unpack(dut.expected_data)==expected.data,
                    "BIST SRAM wrong first-failure address or expected data");
            require(unpack(dut.observed_data)==(timeout_at>=0 ? Value{} : poisoned),
                    "BIST SRAM wrong first-failure observed data");
            ++detected;
        }
        const uint64_t finished=cycles-start,old_commands=commands;
        for(unsigned n=0;n<7;++n){tick();require(dut.done && !dut.busy && commands==old_commands,
            "BIST SRAM completion repeated an access");if(hold)++held_start_cycles;}
        ++campaigns;return finished;
    }
    void exercise(){
        reset();const uint64_t length=run(-1,true);reset();run();
        if(TEST_TIMEOUT>=TEST_LATENCY+3){
            if(TEST_BYTES<=80){
                // Corrupt every individual read position; each must stop at the
                // exact macro access and retain the returned bad data.
                for(size_t n=0;n<sequence.size();++n)if(!sequence[n].write){reset();run(int64_t(n));}
                // Reset at every clock of the full healthy command sequence.
                // Delayed old reads remain live across the shared reset.
                for(uint64_t offset=0;offset<length;++offset){
                    reset();begin();for(uint64_t n=0;n<offset;++n)tick();reset();run();
                }
                if(TEST_LATENCY>1)require(resets_with_pending_reads>0 && old_reads_after_reset>0,
                    "BIST SRAM reset campaign did not exercise old read completions");
            } else {
                for(size_t n: {size_t(TEST_BYTES/16),sequence.size()-1}){reset();run(int64_t(n));}
                for(unsigned offset: {0U,1U,2U,3U,TEST_LATENCY+2U,TEST_LATENCY+4U}){
                    reset();begin();for(unsigned n=0;n<offset;++n)tick();reset();run();
                }
            }
        } else {
            for(unsigned offset=0;offset<unsigned(TEST_LATENCY+6);++offset){
                reset();begin();for(unsigned n=0;n<offset;++n)tick();reset();run();
            }
        }
    }
};
int main(int argc,char** argv){
    Verilated::commandArgs(argc,argv);bool corrupt=false;
    for(int n=1;n<argc;++n){const std::string argument=argv[n];
        if(argument=="--corrupt-read")corrupt=true;else throw std::runtime_error("unknown BIST SRAM argument");}
    try{
        auto test=std::make_unique<Test>(corrupt);test->exercise();
        std::cout<<"{\"status\":\"passed\",\"campaigns\":"<<test->campaigns<<",\"cycles\":"<<test->cycles
            <<",\"macro_commands\":"<<test->commands<<",\"reads\":"<<test->reads<<",\"writes\":"<<test->writes
            <<",\"resets\":"<<test->resets<<",\"detected_errors\":"<<test->detected
            <<",\"resets_with_pending_reads\":"<<test->resets_with_pending_reads
            <<",\"old_reads_after_reset\":"<<test->old_reads_after_reset
            <<",\"held_start_cycles\":"<<test->held_start_cycles<<",\"trace\":"<<test->trace<<"}\n";
    }catch(const std::exception& error){std::cerr<<error.what()<<'\n';return 1;}
}
