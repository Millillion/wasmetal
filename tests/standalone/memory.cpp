// SPDX-License-Identifier: MIT
// Independent byte-array oracle for region translation and transaction atomicity.
#include "Vwasmetal_local_memory.h"
#include "verilated.h"
#include <array>
#include <cstdint>
#include <iostream>
#include <memory>
#include <random>
#include <stdexcept>

using Value=std::array<uint8_t,16>;
struct Region { uint32_t base,size; };
static constexpr Region regions[6][2]={{{0,64},{64,16}},{{80,16},{0,0}},
    {{96,32},{0,0}},{{128,16},{0,0}},{{144,16},{0,0}},{{160,96},{0,0}}};
class Test {
    Vwasmetal_local_memory dut;
    std::array<uint8_t,256> bytes{};
public:
    unsigned checks=0;
    void tick() { dut.clk=0; dut.eval(); dut.clk=1; dut.eval(); dut.clk=0; dut.eval(); }
    void reset() {
        dut.reset=1; dut.valid=0; tick(); tick(); dut.reset=0;
        unsigned remaining=300;
        while(!dut.initialized && remaining--) tick();
        if(!dut.initialized) throw std::runtime_error("RAM clear timed out");
        bytes.fill(0);
    }
    void setup(unsigned kind,uint32_t index,uint64_t address,unsigned size,bool write,Value value,bool init) {
        dut.kind=kind; dut.index=index; dut.address=address; dut.bytes=size;
        dut.write=write; dut.initialize=init;
        for(unsigned w=0;w<4;w++) {
            dut.wdata[w]=0;
            for(unsigned b=0;b<4;b++) dut.wdata[w]|=uint32_t(value[w*4+b])<<(8*b);
        }
        dut.valid=1;
    }
    void request(unsigned kind,uint32_t index,uint64_t address,unsigned size,bool write,Value value={},bool init=false) {
        bool legal=size>=1 && size<=16;
        uint64_t translated=address;
        if(init) legal=legal && write && address<=bytes.size() && size<=bytes.size()-address;
        else if(kind>=6 || index>=2) legal=false;
        else {
            const auto region=regions[kind][index];
            const bool slots=kind==1 || kind==2 || kind==4 || kind==5;
            if(slots) {
                legal=legal && size==16 && address<=UINT64_MAX/16;
                if(address<=UINT64_MAX/16) translated=address*16;
            }
            legal=legal && translated<=region.size && size<=region.size-translated &&
                !(write && (kind==3 || kind==4));
            translated+=region.base;
        }
        Value expected{};
        if(legal) for(unsigned n=0;n<size;n++) {
            if(write) bytes.at(static_cast<size_t>(translated+n))=value[n];
            else expected[n]=bytes.at(static_cast<size_t>(translated+n));
        }
        setup(kind,index,address,size,write,value,init);
        unsigned remaining=100;
        while(!dut.ready && remaining--) tick();
        if(!dut.ready || bool(dut.fault)==legal) throw std::runtime_error("incorrect response or fault");
        if(legal && !write) for(unsigned n=0;n<16;n++) {
            uint8_t actual=uint8_t(dut.rdata[n/4]>>((n%4)*8));
            if(actual!=expected[n]) throw std::runtime_error("local RAM differs from byte-array oracle");
        }
        tick(); dut.valid=0; tick();
        if(dut.ready) throw std::runtime_error("duplicate response");
        ++checks;
    }
    void interrupted(unsigned after) {
        Value ones; ones.fill(255);
        setup(0,0,0,16,true,ones,false);
        for(unsigned n=0;n<after;n++) tick();
        reset();
        for(unsigned offset=0;offset<64;offset+=16) request(0,0,offset,16,false);
    }
};

int main(int argc,char** argv) {
    Verilated::commandArgs(argc,argv);
    try {
        auto t=std::make_unique<Test>(); t->reset();
        std::mt19937 rng(0x5741534d);
        Value pattern{}; for(unsigned n=0;n<16;n++) pattern[n]=uint8_t(n+1);
        for(unsigned addr=0;addr<256;addr+=16) t->request(0,0,addr,16,true,pattern,true);
        for(unsigned size=1;size<=16;size++) for(unsigned offset=0;offset<16;offset++) {
            t->request(0,0,offset,size,true,pattern);
            t->request(0,0,offset,size,false);
        }
        for(unsigned kind=0;kind<8;kind++) for(unsigned index:{0U,1U,2U,0xffffffffU}) {
            for(uint64_t address:{uint64_t(0),uint64_t(1),uint64_t(63),uint64_t(64),
                                  uint64_t(1)<<32,uint64_t(1)<<63,UINT64_MAX}) {
                for(unsigned size:{0U,1U,16U,17U,31U}) {
                    t->request(kind,index,address,size,true,pattern);
                    t->request(kind,index,address,size,false);
                }
            }
        }
        // Recheck every physical byte after the invalid-write attempts.
        for(unsigned kind=0;kind<6;kind++) for(unsigned index=0;index<2;index++) {
            const unsigned unit=(kind==0 || kind==3) ? 1 : 16;
            for(unsigned offset=0;offset<regions[kind][index].size;offset+=16)
                t->request(kind,index,offset/unit,16,false);
        }
        for(unsigned n=0;n<2000;n++) {
            unsigned kind=rng()%6,index=rng()%2,size=(kind==0 || kind==3) ? 1+rng()%16 : 16;
            uint64_t address=rng()%(kind==0 || kind==3 ? 80 : 4);
            for(auto& v:pattern) v=uint8_t(rng());
            t->request(kind,index,address,size,(rng()&1)!=0,pattern);
        }
        for(unsigned offset:{0U,240U,255U,256U}) for(unsigned size:{0U,1U,16U,17U}) {
            t->request(0,0,offset,size,true,pattern,true);
            t->request(0,0,offset,size,false,pattern,true);
        }
        for(unsigned after:{1U,2U,3U,8U,17U}) t->interrupted(after);
        std::cout<<"{\"status\":\"passed\",\"transactions\":"<<t->checks<<"}\n";
    } catch(const std::exception& e) {
        std::cerr<<e.what()<<'\n'; return 1;
    }
    return 0;
}
