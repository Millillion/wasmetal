// SPDX-License-Identifier: MIT
// Independent AXI subordinate and byte oracle; channel handshakes are sampled
// separately. No RTL internals or implementation-state names are accessed.
#include "Vwasmetal_axi_memory.h"
#include "verilated.h"
#include <array>
#include <cstdint>
#include <iostream>
#include <memory>
#include <random>
#include <stdexcept>
#include <string>

using Word=std::array<uint8_t,16>;
static constexpr uint32_t base=4096,size=8192;
static uint64_t transactions=0,clocks=0,aw_first=0,w_first=0,together=0;
static bool corrupt_read=false;
static void require(bool value,const char* message) { if(!value) throw std::runtime_error(message); }
template<class T> static Word unpack(const T& data) {
    Word result{};for(unsigned n=0;n<16;n++) result[n]=uint8_t(data[n/4]>>(8*(n%4)));return result;
}
template<class T> static void pack(T& data,const Word& value) {
    for(unsigned w=0;w<4;w++) {data[w]=0;for(unsigned b=0;b<4;b++) data[w]|=uint32_t(value[w*4+b])<<(8*b);}
}

class Test {
public:
    Vwasmetal_axi_memory dut;
    std::array<uint8_t,size> actual{},expected{};
    std::mt19937 rng{0x41584934};
    unsigned order=0,response=0,response_id=0;
    bool last=true,blocked=false;
    uint64_t accepted=0;
private:
    bool have_aw=false,have_w=false,pending_b=false,pending_r=false;
    uint32_t saved_aw=0;
    uint16_t saved_mask=0;
    Word saved_data{},read_word{};
    unsigned b_delay=0,r_delay=0,read_response=0,write_response=0;
    bool held_aw=false,held_w=false,held_ar=false;
    uint32_t old_aw=0,old_ar=0;
    uint16_t old_mask=0;
    Word old_data{};
public:
    void tick() {
        if(dut.reset) {
            have_aw=have_w=pending_b=pending_r=false;
            held_aw=held_w=held_ar=false;
        }
        dut.awready=!blocked && !have_aw && !pending_b && (order!=1 || have_w) && (order==2 || rng()%3!=0);
        dut.wready=!blocked && !have_w && !pending_b && (order!=0 || have_aw) && (order==2 || rng()%3!=0);
        dut.arready=!blocked && !pending_r && (rng()%3!=0);
        dut.bvalid=pending_b && b_delay==0;dut.bresp=write_response;dut.bid=response_id;
        dut.rvalid=pending_r && r_delay==0;dut.rresp=read_response;dut.rid=response_id;dut.rlast=last;
        Word data=read_word;if(corrupt_read) data[0]^=1;pack(dut.read_data,data);
        dut.clk=0;dut.eval();
        if(!dut.reset) {
            if(held_aw) require(dut.awvalid && dut.awaddr==old_aw,"AW changed during a stall");
            if(held_w) require(dut.wvalid && dut.wstrb==old_mask && unpack(dut.write_data)==old_data,"W changed during a stall");
            if(held_ar) require(dut.arvalid && dut.araddr==old_ar,"AR changed during a stall");
            require(!(dut.arvalid && (dut.awvalid || dut.wvalid)),"overlapping read and write");
            if(dut.awvalid || dut.arvalid) {
                require(dut.awid==0 && dut.arid==0 && dut.awlen==0 && dut.arlen==0 &&
                    dut.awsize==4 && dut.arsize==4 && dut.awburst==1 && dut.arburst==1 &&
                    dut.awlock==0 && dut.arlock==0 && dut.awcache==0 && dut.arcache==0 &&
                    dut.awprot==0 && dut.arprot==0 && dut.awqos==0 && dut.arqos==0,"wrong AXI attributes");
            }
            if(dut.bready) require(have_aw && have_w,"B accepted before AW and W");
            if(dut.rready) require(pending_r,"R accepted before AR");
            const bool take_aw=dut.awvalid && dut.awready,take_w=dut.wvalid && dut.wready;
            if(take_aw) {
                require(!have_aw && !pending_b && (dut.awaddr&15)==0,"duplicate or unaligned AW");
                saved_aw=dut.awaddr;have_aw=true;++accepted;
                if(!have_w && !take_w) ++aw_first;
            }
            if(take_w) {
                require(!have_w && !pending_b && dut.wlast && dut.wstrb,"duplicate or malformed W");
                saved_mask=dut.wstrb;saved_data=unpack(dut.write_data);have_w=true;++accepted;
                if(!take_aw && !have_aw) ++w_first;
            }
            if(take_aw && take_w) ++together;
            if(dut.arvalid && dut.arready) {
                require(!pending_r && (dut.araddr&15)==0,"duplicate or unaligned AR");
                const bool in_range=dut.araddr>=base && uint64_t(dut.araddr)+16<=uint64_t(base)+size;
                read_word.fill(0);
                if(in_range) for(unsigned n=0;n<16;n++) read_word[n]=actual[dut.araddr-base+n];
                read_response=in_range ? response : 3;r_delay=rng()%12;pending_r=true;++accepted;
            }
            if(dut.bvalid && dut.bready) {pending_b=false;have_aw=have_w=false;}
            if(dut.rvalid && dut.rready) pending_r=false;
            if(have_aw && have_w && !pending_b) {
                const bool in_range=saved_aw>=base && uint64_t(saved_aw)+16<=uint64_t(base)+size;
                if(in_range) for(unsigned n=0;n<16;n++) if(saved_mask>>n&1) actual[saved_aw-base+n]=saved_data[n];
                write_response=in_range ? response : 3;b_delay=rng()%12;pending_b=true;
            }
            if(b_delay) --b_delay;
            if(r_delay) --r_delay;
            held_aw=dut.awvalid && !dut.awready;held_w=dut.wvalid && !dut.wready;held_ar=dut.arvalid && !dut.arready;
            old_aw=dut.awaddr;old_ar=dut.araddr;old_mask=dut.wstrb;old_data=unpack(dut.write_data);
        }
        dut.clk=1;dut.eval();dut.clk=0;dut.eval();++clocks;
    }
    void reset() {
        dut.valid=0;dut.reset=1;tick();tick();dut.reset=0;
        for(unsigned n=0;n<4;n++) {tick();require(!dut.ready && !dut.awvalid && !dut.wvalid && !dut.arvalid,"phantom transaction after reset");}
    }
    void start(uint32_t address,bool write,uint16_t mask,const Word& data) {
        dut.address=address;dut.write=write;dut.mask=mask;pack(dut.wdata,data);dut.valid=1;
    }
    void request(uint32_t address,bool write,uint16_t mask,const Word& data={},bool error=false,unsigned hold=0) {
        const bool legal=(address&15)==0 && mask && uint64_t(base)+address+16<=(uint64_t(1)<<32);
        const uint64_t before=accepted;
        start(address,write,mask,data);tick();
        unsigned count=0;
        while(!dut.ready && count++<200) {
            // Accepted requests must use the captured payload even if upstream
            // address/data wires change while the downstream channels stall.
            dut.address=rng();dut.mask=uint16_t(rng());dut.write=!write;
            for(unsigned n=0;n<4;n++) dut.wdata[n]=rng();
            tick();
        }
        require(dut.ready,"AXI request did not complete");
        require(bool(dut.fault)==(!legal || error),"wrong AXI completion status");
        if(!legal) require(accepted==before,"invalid address/mask reached AXI");
        if(!legal || error) require(unpack(dut.rdata)==Word{},"fault returned untrusted data");
        else {
            require(accepted-before==(write ? 2U : 1U),"wrong AXI transaction count");
            require(address+16<=size,"test oracle address overflow");
            if(write) {for(unsigned n=0;n<16;n++) if(mask>>n&1) expected[address+n]=data[n];}
            else {
                Word want{};for(unsigned n=0;n<16;n++) want[n]=expected[address+n];
                require(unpack(dut.rdata)==want,"read data differs from independent byte oracle");
            }
        }
        const auto completed=accepted;
        for(unsigned n=0;n<hold;n++) {
            tick();require(!dut.ready && accepted==completed,"held request executed twice");
        }
        dut.valid=0;tick();tick();
        require(!dut.ready,"duplicate local completion");++transactions;
    }
};

int main(int argc,char** argv) {
    Verilated::commandArgs(argc,argv);
    try {
        if(argc==2 && std::string(argv[1])=="--corrupt-read") corrupt_read=true;
        auto t=std::make_unique<Test>();t->reset();Word pattern{};
        for(unsigned address=0;address<size;address+=16) {
            for(unsigned n=0;n<16;n++) pattern[n]=uint8_t(address/16+n*19);
            t->order=(address/16)%3;t->request(address,true,65535,pattern);t->request(address,false,65535);
        }
        for(unsigned n=0;n<10000;n++) {
            const uint32_t address=(t->rng()%(size/16))*16;const uint16_t mask=uint16_t(t->rng())|1;
            for(auto& byte:pattern) byte=uint8_t(t->rng());
            t->order=n%3;
            t->request(address,true,mask,pattern,false,n%7);t->request(address,false,65535);
        }
        for(uint32_t address:{1U,15U,17U,0xfffff000U,0xfffffff0U,0xffffffffU})
            for(bool write:{false,true}) t->request(address,write,65535,pattern);
        t->request(0,true,0,pattern);t->request(0,false,0);
        for(unsigned address=0;address<size;address+=16) t->request(address,false,65535);
        // Every response error, mismatched ID and malformed final-beat flag
        // poisons the adapter. No new external transaction may follow it.
        for(bool write:{false,true}) for(unsigned fault=0;fault<5;fault++) {
            if(write && fault==4) continue;
            auto f=std::make_unique<Test>();f->reset();
            if(fault<3) f->response=fault+1;
            else if(fault==3) f->response_id=1;
            else f->last=false;
            f->request(0,write,65535,pattern,true);
            const auto before=f->accepted;
            f->request(16,false,65535,{},true);require(f->accepted==before,"poisoned adapter issued a request");
            f->response=f->response_id=0;f->last=true;f->reset();
            f->request(0,true,65535,Word{});f->request(0,false,65535);
        }
        for(unsigned after=0;after<24;after++) for(unsigned order=0;order<3;order++) {
            auto f=std::make_unique<Test>();f->reset();f->order=order;
            f->start(0,after%2!=0,65535,pattern);for(unsigned n=0;n<after;n++) f->tick();
            f->reset();f->request(0,true,65535,Word{});f->request(0,false,65535);
        }
        // Withdrawal by a timed-out frontend must not retract AXI VALID.
        for(bool write:{false,true}) {
            auto f=std::make_unique<Test>();f->reset();f->blocked=true;f->start(0,write,65535,Word{});
            for(unsigned n=0;n<40;n++) f->tick();
            f->dut.valid=0;
            for(unsigned n=0;n<40;n++) {f->tick();require(!f->dut.ready,"blocked AXI falsely completed");}
            f->blocked=false;unsigned n=0;while(!f->dut.ready && n++<200) f->tick();
            require(f->dut.ready && !f->dut.fault,"late AXI completion was lost");f->tick();f->tick();
            f->request(16,false,65535);
        }
        require(aw_first && w_first && together,"missing write-channel ordering coverage");
        std::cout<<"{\"status\":\"passed\",\"transactions\":"<<transactions<<",\"cycles\":"<<clocks
            <<",\"aw_before_w\":"<<aw_first<<",\"w_before_aw\":"<<w_first<<",\"aw_with_w\":"<<together<<"}\n";
    } catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 1;}
    return 0;
}
