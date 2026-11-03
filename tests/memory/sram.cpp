// SPDX-License-Identifier: MIT
// Independent byte-addressed SRAM model; only the adapter's public pins are used.
#include "Vwasmetal_sram_memory.h"
#include "verilated.h"
#include <array>
#include <cstdint>
#include <deque>
#include <iostream>
#include <memory>
#include <random>
#include <stdexcept>
#include <string>
#ifndef TEST_BYTES
#define TEST_BYTES 131072
#endif
#ifndef TEST_LATENCY
#define TEST_LATENCY 1
#endif
using Value=std::array<uint8_t,16>;
static void require(bool condition,const char* message){if(!condition)throw std::runtime_error(message);}
template<class Wide> static Value unpack(const Wide& input){
    Value value{};for(unsigned n=0;n<16;++n)value[n]=uint8_t(input[n/4]>>((n%4)*8));return value;
}
template<class Wide> static void pack(Wide& output,const Value& value){
    for(unsigned n=0;n<4;++n){output[n]=0;for(unsigned b=0;b<4;++b)output[n]|=uint32_t(value[n*4+b])<<(8*b);}
}
class Test {
    Vwasmetal_sram_memory dut;
    std::array<uint8_t,TEST_BYTES> memory{},oracle{};
    struct Pending {unsigned delay;Value value;};
    std::deque<Pending> pipeline;
    bool corrupt_read,ignore_masks;
public:
    uint64_t cycles=0,transactions=0,commands=0,reads=0,writes=0,resets=0,held_cycles=0;
    Test(bool corrupt,bool masks):corrupt_read(corrupt),ignore_masks(masks){memory.fill(0xa5);}
    void tick(){
        dut.clk=0;dut.eval();
        const bool enable=dut.sram_enable,write=dut.sram_write;
        Value incoming{};bool issued_read=false;
        if(enable){
            const uint64_t address=uint64_t(dut.sram_address)*16;
            require(address+16<=TEST_BYTES,"macro address escaped the memory");
            require(dut.sram_byte_enable!=0,"macro received zero byte enables");
            ++commands;
            if(write){
                const Value data=unpack(dut.sram_wdata);++writes;
                for(unsigned n=0;n<16;++n)if(ignore_masks || (dut.sram_byte_enable&(1U<<n)))memory.at(address+n)=data[n];
            } else {
                ++reads;issued_read=true;
                for(unsigned n=0;n<16;++n)incoming[n]=memory.at(address+n);
                if(corrupt_read)incoming[0]^=1;
            }
        }
        dut.clk=1;dut.eval();++cycles;
        // Invalid sampling cycles carry changing garbage, so early or late
        // capture cannot accidentally pass by seeing a retained old read.
        Value output{};for(unsigned n=0;n<16;++n)output[n]=uint8_t(0xc3+cycles+17*n);
        for(auto& pending:pipeline)--pending.delay;
        if(!pipeline.empty() && pipeline.front().delay==0){output=pipeline.front().value;pipeline.pop_front();}
        if(issued_read){
            if(TEST_LATENCY==1)output=incoming;
            else pipeline.push_back({TEST_LATENCY-1,incoming});
        }
        pack(dut.sram_rdata,output);dut.eval();dut.clk=0;dut.eval();
    }
    void reset(){
        dut.reset=1;dut.eval();require(!dut.sram_enable && !dut.sram_write,"reset did not suppress macro strobes");
        const uint64_t before=commands;tick();tick();require(commands==before,"reset accessed SRAM");
        dut.valid=0;dut.reset=0;tick();++resets;
    }
    void inputs(uint32_t address,uint16_t mask,bool write,const Value& data){
        dut.address=address;dut.mask=mask;dut.write=write;pack(dut.wdata,data);dut.valid=1;
    }
    void request(uint32_t address,uint16_t mask,bool write,Value data={}){
        const bool legal=mask!=0 && address%16==0 && uint64_t(address)+16<=TEST_BYTES;
        if(legal && write)for(unsigned n=0;n<16;++n)if(mask&(1U<<n))oracle.at(address+n)=data[n];
        inputs(address,mask,write,data);const uint64_t before=commands,start=cycles;
        unsigned limit=TEST_LATENCY+10;while(!dut.ready && limit--)tick();
        require(dut.ready && bool(dut.fault)!=legal,"incorrect SRAM completion");
        require(cycles-start==(legal ? (write ? 2U : TEST_LATENCY+2U) : 1U),"incorrect SRAM completion latency");
        require(commands-before==unsigned(legal),"missing or duplicated macro command");
        const Value actual=unpack(dut.rdata);
        if(legal && !write){
            for(unsigned n=0;n<16;++n)require(actual[n]==oracle.at(address+n),"SRAM read differs from independent byte oracle");
        } else for(uint8_t byte:actual)require(byte==0,"write/fault response leaked old read data");
        tick();
        Value poison{};poison.fill(0x71);inputs(0,0xffff,true,poison);
        for(unsigned n=0;n<3;++n){tick();++held_cycles;require(!dut.ready && commands==before+unsigned(legal),"held valid repeated a command");}
        dut.valid=0;tick();tick();++transactions;
    }
    void interrupt(bool write,unsigned after){
        Value data{};for(unsigned n=0;n<16;++n)data[n]=uint8_t(0x31+after+19*n);
        inputs(0,0xa581,write,data);const uint64_t before=commands;
        for(unsigned n=0;n<after;++n)tick();
        require(commands-before==unsigned(after>=2),"unexpected command before interrupt");
        if(write && after>=2)for(unsigned n=0;n<16;++n)if(0xa581&(1U<<n))oracle[n]=data[n];
        reset();
        // Do not clear the SRAM model or its delayed read pipeline on reset.
        request(TEST_BYTES-16,0xffff,false);request(0,0xffff,false);
    }
};
int main(int argc,char** argv){
    Verilated::commandArgs(argc,argv);
    bool corrupt=false,masks=false;
    for(int n=1;n<argc;++n){
        const std::string argument=argv[n];
        if(argument=="--corrupt-read")corrupt=true;
        else if(argument=="--ignore-masks")masks=true;
        else throw std::runtime_error("unknown SRAM test argument");
    }
    try {
        auto test=std::make_unique<Test>(corrupt,masks);test->reset();std::mt19937 random(0x5352414d);Value data{};
        for(uint32_t address=0;address<TEST_BYTES;address+=16){
            for(auto& byte:data)byte=uint8_t(random());
            test->request(address,0xffff,true,data);
        }
        // Exhaust every mask, checking adjacent byte preservation each time.
        for(unsigned mask=0;mask<65536;++mask){
            const uint32_t address=(random()%(TEST_BYTES/16))*16;
            for(auto& byte:data)byte=uint8_t(random());
            test->request(address,uint16_t(mask),true,data);
            test->request(address,0xffff,false);
        }
        for(unsigned n=0;n<3000;++n){
            const uint32_t address=(random()%(TEST_BYTES/16))*16;
            for(auto& byte:data)byte=uint8_t(random());
            const uint16_t mask=uint16_t(random());const bool write=bool(random()&1);
            test->request(address,mask,write,data);
        }
        for(uint32_t address:{0U,1U,uint32_t(TEST_BYTES-16),uint32_t(TEST_BYTES-1),uint32_t(TEST_BYTES),0xfffffff0U})
            for(uint16_t mask:{uint16_t(0),uint16_t(1),uint16_t(0x8000),uint16_t(0xffff)})
                for(bool write:{false,true})test->request(address,mask,write,data);
        for(bool write:{false,true})for(unsigned offset=0;offset<TEST_LATENCY+5;++offset)test->interrupt(write,offset);
        test->reset();for(uint32_t address=0;address<TEST_BYTES;address+=16)test->request(address,0xffff,false);
        std::cout<<"{\"status\":\"passed\",\"transactions\":"<<test->transactions<<",\"cycles\":"<<test->cycles
            <<",\"macro_commands\":"<<test->commands<<",\"reads\":"<<test->reads<<",\"writes\":"<<test->writes
            <<",\"resets\":"<<test->resets<<",\"held_valid_cycles\":"<<test->held_cycles<<"}\n";
    } catch(const std::exception& error){std::cerr<<error.what()<<'\n';return 1;}
}
