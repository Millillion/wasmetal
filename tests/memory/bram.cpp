// SPDX-License-Identifier: MIT
#include "Vwasmetal_bram.h"
#include "verilated.h"
#include <array>
#include <cstdint>
#include <iostream>
#include <memory>
#include <random>
#include <stdexcept>
#ifndef TEST_BYTES
#define TEST_BYTES 131072
#endif
using Value=std::array<uint8_t,16>;
static void require(bool x,const char* message){if(!x)throw std::runtime_error(message);}
class Test {
    Vwasmetal_bram dut;
    std::array<uint8_t,TEST_BYTES> oracle{};
public:
    unsigned checks=0,cycles=0;
    void tick(){dut.clk=0;dut.eval();dut.clk=1;dut.eval();dut.clk=0;dut.eval();++cycles;}
    void reset(){dut.valid=0;dut.reset=1;tick();tick();dut.reset=0;tick();}
    void request(uint32_t address,uint16_t mask,bool write,Value data={}) {
        const bool legal=mask && address%16==0 && uint64_t(address)+16<=TEST_BYTES;
        if(legal && write)for(unsigned n=0;n<16;n++)if(mask&(1U<<n))oracle.at(address+n)=data[n];
        dut.address=address;dut.mask=mask;dut.write=write;dut.valid=1;
        for(unsigned n=0;n<4;n++){dut.wdata[n]=0;for(unsigned b=0;b<4;b++)dut.wdata[n]|=uint32_t(data[n*4+b])<<(b*8);}
        unsigned timeout=10;while(!dut.ready && timeout--)tick();
        require(dut.ready && bool(dut.fault)!=legal,"incorrect BRAM response");
        if(legal && !write)for(unsigned n=0;n<16;n++)
            require(uint8_t(dut.rdata[n/4]>>((n%4)*8))==oracle.at(address+n),"BRAM read differs from byte oracle");
        tick();
        // Holding valid or changing fields must not execute the request again.
        dut.address=0;dut.mask=0xffff;dut.write=1;
        for(unsigned n=0;n<4;n++)dut.wdata[n]=0xdeadbeef;
        for(unsigned n=0;n<3;n++){tick();require(!dut.ready,"duplicate BRAM response");}
        dut.valid=0;tick();tick();++checks;
    }
};
int main(int argc,char** argv) {
    Verilated::commandArgs(argc,argv);
    try {
        auto test=std::make_unique<Test>();test->reset();std::mt19937 random(0x4252414d);Value data{};
        for(unsigned address=0;address<TEST_BYTES;address+=16) {
            for(auto& b:data)b=uint8_t(random());
            test->request(address,0xffff,true,data);
        }
        for(unsigned n=0;n<10000;n++) {
            const uint32_t address=(random()%(TEST_BYTES/16))*16;
            for(auto& b:data)b=uint8_t(random());
            test->request(address,uint16_t(random()),true,data);test->request(address,0xffff,false);
        }
        for(uint32_t address:{0U,1U,uint32_t(TEST_BYTES-16),uint32_t(TEST_BYTES-1),uint32_t(TEST_BYTES),0xfffffff0U})
            for(uint16_t mask:{uint16_t(0),uint16_t(1),uint16_t(0x8000),uint16_t(0xffff)})
                for(bool write:{false,true})test->request(address,mask,write,data);
        test->reset(); // backend reset must preserve data; the bridge owns zeroing.
        for(unsigned address=0;address<TEST_BYTES;address+=16)test->request(address,0xffff,false);
        std::cout<<"{\"status\":\"passed\",\"transactions\":"<<test->checks<<",\"cycles\":"<<test->cycles<<"}\n";
    } catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}
}
