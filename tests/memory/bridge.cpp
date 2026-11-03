// SPDX-License-Identifier: MIT
// Byte-array oracle, independently scheduled memory responses, and fault tests.
#include "Vwasmetal_memory_bridge.h"
#include "verilated.h"
#include <array>
#include <cstdint>
#include <iostream>
#include <memory>
#include <random>
#include <stdexcept>
#include <vector>

using Value=std::array<uint8_t,16>;
struct Region { unsigned base,size; };
static constexpr Region regions[6][2]={{{13,64},{64,16}},{{80,16},{249,16}},
    {{101,32},{0,0}},{{128,16},{0,0}},{{144,16},{0,0}},{{160,96},{0,0}}};
struct Request {
    bool write;uint32_t address;uint16_t mask;Value data;
    bool operator==(const Request& b) const {return write==b.write && address==b.address && mask==b.mask && data==b.data;}
};
static void require(bool v,const char* message) {if(!v)throw std::runtime_error(message);}
template<class T> static Value unpack(const T& data) {
    Value value{};for(unsigned n=0;n<16;n++)value[n]=uint8_t(data[n/4]>>((n%4)*8));return value;
}
template<class T> static void pack(T& target,const Value& bytes) {
    for(unsigned n=0;n<4;n++){target[n]=0;for(unsigned b=0;b<4;b++)target[n]|=uint32_t(bytes[n*4+b])<<(8*b);}
}

class Test {
public:
    Vwasmetal_memory_bridge dut;
    std::array<uint8_t,256> storage{},oracle{};
    std::mt19937 random{0x574d4255};
    std::vector<Request> expected;
    Request pending{};
    bool active=false,clearing=false,checking=false,stall=false,late_response=false;
    int delay=0,fail_after=-1;
    unsigned checks=0,beats=0,expected_index=0,clear_index=0,cycles=0;

    Request request_on_bus() {return {bool(dut.bus_write),dut.bus_address,dut.bus_mask,unpack(dut.bus_wdata)};}
    void tick() {
        dut.clk=0;dut.eval();dut.bus_ready=0;dut.bus_fault=0;
        if(dut.reset){active=false;dut.region=0;}
        else {
            if(active && !dut.bus_valid){require(stall,"request disappeared before completion");active=false;}
            if(dut.bus_valid && !active) {
                pending=request_on_bus();active=true;delay=int(random()%8);
                require(pending.address%16==0 && pending.address<=240 && pending.mask!=0,"invalid physical request");
                if(clearing) {
                    require(pending.write && pending.address==clear_index && pending.mask==0xffff && pending.data==Value{},"incorrect RAM clear");
                    clear_index+=16;
                } else if(checking) {
                    require(expected_index<expected.size(),"unexpected extra bus request");
                    const auto& e=expected[expected_index++];
                    require(pending.write==e.write && pending.address==e.address && pending.mask==e.mask,"wrong address/mask/operation");
                    if(e.write) require(pending.data==e.data,"wrong shifted write payload");
                }
            }
            if(active) {
                require(request_on_bus()==pending,"request changed while stalled");
                if(!stall && delay--==0) {
                    dut.bus_ready=1;dut.bus_fault=fail_after==0;
                    if(fail_after>=0)--fail_after;
                    Value read{};
                    for(unsigned n=0;n<16;n++)read[n]=storage[pending.address+n];
                    pack(dut.bus_rdata,read);
                    if(!dut.bus_fault && pending.write) for(unsigned n=0;n<16;n++)
                        if(pending.mask&(1U<<n))storage[pending.address+n]=pending.data[n];
                    active=false;++beats;
                }
            }
        }
        if(late_response) {
            require(!active,"late response overlaps an issued request");
            dut.bus_ready=1;dut.bus_fault=0;Value stale{};stale.fill(0xaa);pack(dut.bus_rdata,stale);
            late_response=false;
        }
        const Region region=dut.kind<6 && dut.index<2 ? regions[dut.kind][dut.index] : regions[0][0];
        dut.clk=1;dut.eval();
        // Match a synchronous lookup, not a combinational shortcut.
        dut.region=uint64_t(region.base)|(uint64_t(region.size)<<32);
        dut.eval();dut.clk=0;dut.eval();++cycles;
    }
    void start_reset() {
        checking=false;clearing=true;clear_index=0;stall=false;fail_after=-1;late_response=false;
        dut.reset=1;dut.valid=0;tick();tick();dut.reset=0;
    }
    void reset() {
        start_reset();unsigned timeout=2000;
        while(!dut.initialized && !dut.initialization_failed && timeout--)tick();
        require(dut.initialized && !dut.initialization_failed,"clear did not complete");
        require(clear_index==256 && storage==std::array<uint8_t,256>{},"clear skipped memory");
        oracle.fill(0);clearing=false;checking=true;
    }
    void setup(unsigned kind,uint32_t index,uint64_t address,unsigned size,bool write,const Value& value,bool init=false) {
        dut.kind=kind;dut.index=index;dut.address=address;dut.bytes=size;
        dut.write=write;dut.initialize=init;pack(dut.wdata,value);dut.valid=1;
    }
    void finish(bool fault) {
        require(dut.ready && bool(dut.fault)==fault,"incorrect response status");
        tick();dut.valid=0;tick();require(!dut.ready,"duplicate response");
    }
    void transfer(unsigned kind,uint32_t index,uint64_t address,unsigned size,bool write,Value value={},bool init=false) {
        bool legal=size>=1 && size<=16;
        __uint128_t physical=address;
        if(init)legal=legal && write && physical+size<=storage.size();
        else if(kind>=6 || index>=2)legal=false;
        else {
            const auto region=regions[kind][index];
            const bool slots=kind==1 || kind==2 || kind==4 || kind==5;
            if(slots){physical*=16;legal=legal && size==16;}
            legal=legal && physical+size<=region.size && !(write && (kind==3 || kind==4));
            physical+=region.base;legal=legal && physical+size<=storage.size();
        }
        Value result{};expected.clear();expected_index=0;
        if(legal) {
            for(unsigned n=0;n<size;n++) {
                const auto a=unsigned(physical)+n;
                if(write)oracle.at(a)=value[n];else result[n]=oracle.at(a);
                if(expected.empty() || expected.back().address!=a/16*16)expected.push_back({write,a/16*16,0,{}});
                auto& e=expected.back();e.mask|=uint16_t(1U<<(a%16));e.data[a%16]=value[n];
            }
        }
        const auto before=beats;setup(kind,index,address,size,write,value,init);
        unsigned timeout=200;tick();
        while(!dut.ready && timeout--) {
            // The transaction must use its captured request despite input noise.
            if((random()%7)==0){dut.kind=random()%8;dut.index=random();dut.address=random();pack(dut.wdata,{});}
            tick();
        }
        require(beats-before==expected.size() && expected_index==expected.size(),"unexpected beat count");
        if(legal && !write)require(unpack(dut.rdata)==result,"read differs from byte oracle");
        if(!legal)require(unpack(dut.rdata)==Value{},"fault leaked stale read data");
        require(storage==oracle,"write corruption or out-of-bounds partial write");
        finish(!legal);++checks;
    }
    void clear_failure(bool timeout) {
        start_reset();if(timeout)stall=true;else fail_after=2;
        unsigned limit=2000;while(!dut.initialization_failed && limit--)tick();
        require(dut.initialization_failed && !dut.initialized,"startup failure not reported");
        for(unsigned n=0;n<80;n++){tick();require(!dut.bus_valid && !dut.initialized,"startup failure resumed");}
        ++checks;reset();
    }
    void bus_failure(bool timeout,bool write,int failing_beat) {
        reset();checking=false;Value value{};value.fill(0x6d);
        setup(0,0,0,16,write,value);fail_after=timeout ? -1 : failing_beat;stall=timeout;
        unsigned remaining=200;while(!dut.ready && remaining--)tick();
        require(unpack(dut.rdata)==Value{},"backend failure leaked partial read");finish(true);
        // Failed second beats may follow a committed first write; bounds faults
        // never issue any beat. A hardware fault poisons the bus until reset.
        if(!timeout && write && failing_beat==1) {
            require(storage[13]==0x6d && storage[15]==0x6d && storage[16]==0,"wrong partial hardware-fault effect");
        }
        const auto before=beats;stall=false;active=false;late_response=timeout;
        setup(0,0,0,1,false,{});remaining=20;
        while(!dut.ready && remaining--)tick();
        finish(true);
        require(beats==before,"poisoned backend was reused");
        ++checks;reset();
    }
    void interrupted(unsigned after) {
        reset();checking=false;Value value{};value.fill(0xf1);setup(0,0,0,16,true,value);
        for(unsigned n=0;n<after;n++)tick();
        reset();++checks;
    }
};

int main(int argc,char** argv) {
    Verilated::commandArgs(argc,argv);
    try {
        auto t=std::make_unique<Test>();t->storage.fill(0xa5);t->reset();Value value{};
        for(unsigned n=0;n<16;n++)value[n]=uint8_t(n*13+3);
        for(unsigned a=0;a<256;a+=16)t->transfer(0,0,a,16,true,value,true);
        for(unsigned size=1;size<=16;size++)for(unsigned offset=0;offset<32;offset++) {
            t->transfer(0,0,offset,size,true,value);t->transfer(0,0,offset,size,false);
        }
        for(unsigned kind=0;kind<8;kind++)for(unsigned index:{0U,1U,2U,0xffffffffU})
            for(uint64_t address:{uint64_t(0),uint64_t(1),uint64_t(63),uint64_t(64),uint64_t(1)<<32,uint64_t(1)<<63,UINT64_MAX})
                for(unsigned size:{0U,1U,16U,17U,31U}) {
                    t->transfer(kind,index,address,size,true,value);t->transfer(kind,index,address,size,false);
                }
        for(unsigned n=0;n<10000;n++) {
            const unsigned kind=t->random()%6,index=t->random()%2,size=(kind==0 || kind==3) ? 1+t->random()%16 : 16;
            const uint64_t address=t->random()%(kind==0 || kind==3 ? 80 : 8);
            for(auto& b:value)b=uint8_t(t->random());
            t->transfer(kind,index,address,size,(t->random()&1)!=0,value);
        }
        for(unsigned a:{0U,240U,255U,256U})for(unsigned n:{0U,1U,16U,17U}) {
            t->transfer(0,0,a,n,true,value,true);t->transfer(0,0,a,n,false,value,true);
        }
        for(bool timeout:{false,true})t->clear_failure(timeout);
        for(bool timeout:{false,true})for(bool write:{false,true})for(int beat:{0,1})t->bus_failure(timeout,write,beat);
        for(unsigned after:{1U,2U,3U,8U,17U})t->interrupted(after);
        std::cout<<"{\"status\":\"passed\",\"transactions\":"<<t->checks<<",\"bus_completions\":"<<t->beats<<",\"cycles\":"<<t->cycles<<"}\n";
    } catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}
    return 0;
}
