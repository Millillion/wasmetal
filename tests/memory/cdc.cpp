// SPDX-License-Identifier: MIT
// Independently scheduled clocks and a separately timed backend. The oracle
// compares all request bits before producing an independent response payload.
#include "Vwasmetal_memory_cdc.h"
#include "verilated.h"
#include <array>
#include <cstdint>
#include <iostream>
#include <memory>
#include <random>
#include <stdexcept>
#include <string>

using Word=std::array<uint32_t,4>;
static uint64_t transfers=0,steps=0,resets=0,pauses=0;
static unsigned reset_coverage=0;
static bool corrupt_response=false;
static void require(bool ok,const char* message) {if(!ok) throw std::runtime_error(message);}
template<class T> static Word unpack(const T& value) {return {value[0],value[1],value[2],value[3]};}
template<class T> static void pack(T& to,const Word& from) {for(unsigned i=0;i<4;i++) to[i]=from[i];}

class Test {
public:
    Vwasmetal_memory_cdc dut;
    std::mt19937 rng{0x43444331};
    unsigned source_half,memory_half,phase,pause_source=0,pause_memory=0;
    uint64_t now=0;
    bool active=false,seen=false,returned=false,captured=false;
private:
    bool pending=false,finished_backend=false,reference_write=false,reference_fault=false;
    uint32_t reference_address=0;
    uint16_t reference_mask=0;
    Word reference_data{},response{};
    unsigned delay=0;
public:
    Test(unsigned s,unsigned m,unsigned p):source_half(s),memory_half(m),phase(p) {}
    void step() {
        const bool next_s=pause_source ? bool(dut.s_clk) : ((now/source_half)&1)!=0;
        const bool next_m=pause_memory ? bool(dut.m_clk) : (((now+phase)/memory_half)&1)!=0;
        if(pause_source) --pause_source;
        if(pause_memory) --pause_memory;
        dut.m_ready=pending && delay==0;dut.m_fault=reference_fault;
        Word data=response;if(corrupt_response) data[0]^=1;pack(dut.m_rdata,data);
        dut.eval();
        const bool s_rise=next_s && !dut.s_clk,m_rise=next_m && !dut.m_clk;
        if(dut.m_reset) {pending=false;seen=false;finished_backend=false;}
        if(!dut.m_reset && m_rise) {
            if(dut.m_valid) {
                require(!finished_backend,"destination request remained valid after completion");
                require(active,"phantom destination request");
                require(bool(dut.m_write)==reference_write && dut.m_address==reference_address &&
                    dut.m_mask==reference_mask && unpack(dut.m_wdata)==reference_data,"CDC request payload differs");
                if(!seen) {
                    require(!finished_backend,"CDC duplicated a destination request");
                    seen=true;pending=true;delay=rng()%32;
                } else if(dut.m_ready) {pending=false;finished_backend=true;}
            }
            if(pending && delay) --delay;
        }
        if(s_rise && !dut.s_reset) {
            if(active && dut.source_online) captured=true;
            if(dut.s_ready) {
                require(active && !returned && finished_backend,"phantom or early source completion");
                require(bool(dut.s_fault)==reference_fault,"CDC fault changed");
                require(unpack(dut.s_rdata)==(reference_fault ? Word{} : response),"CDC response payload differs");
                returned=true;++transfers;
            }
        }
        dut.s_clk=next_s;dut.m_clk=next_m;dut.eval();++now;++steps;
    }
    void idle(unsigned count) {for(unsigned n=0;n<count;n++) step();}
    void reset(bool clocks_stopped=false) {
        if(active) reset_coverage|=returned ? 8U : finished_backend ? 4U : seen ? 2U : 1U;
        active=false;returned=false;captured=false;dut.s_valid=0;
        if(clocks_stopped) {pause_source=100;pause_memory=100;}
        dut.reset=1;step();
        require(dut.s_reset && dut.m_reset && !dut.s_ready && !dut.m_valid,"asynchronous reset did not assert");
        dut.reset=0;step();
        if(clocks_stopped) {
            idle(10);require(dut.s_reset && dut.m_reset && !dut.source_online,"reset released without clock edges");
            pause_source=pause_memory=0;
        }
        unsigned count=0;while(!dut.source_online && count++<10000) step();
        require(dut.source_online,"CDC link did not leave reset");
        idle(4*(source_half+memory_half));++resets;
    }
    void start() {
        require(!active,"test has overlapping requests");
        active=true;seen=false;returned=false;captured=false;finished_backend=false;
        reference_write=(rng()&1)!=0;reference_fault=rng()%7==0;
        reference_address=rng();reference_mask=uint16_t(rng());
        for(unsigned n=0;n<4;n++) {
            reference_data[n]=rng();
            response[n]=reference_data[n]^reference_address^(uint32_t(reference_mask)<<(n+1))^
                (reference_write ? 0xa5a55a5aU : 0x12345678U)^(0x9e3779b9U*n);
        }
        dut.s_valid=1;dut.s_write=reference_write;dut.s_address=reference_address;
        dut.s_mask=reference_mask;pack(dut.s_wdata,reference_data);
    }
    void finish(unsigned pause_kind=0) {
        bool paused=false;unsigned count=0;
        while(!returned && count++<20000) {
            if(seen) {
                dut.s_address=rng();dut.s_mask=uint16_t(rng());dut.s_write=(rng()&1)!=0;
                for(unsigned n=0;n<4;n++) dut.s_wdata[n]=rng();
                if(pause_kind && !paused) {
                    if(pause_kind&1) pause_source=19+rng()%80;
                    if(pause_kind&2) pause_memory=19+rng()%80;
                    paused=true;++pauses;
                }
            }
            step();
        }
        require(returned,"CDC transaction timed out");
        idle((rng()%5+1)*2*source_half); // Hold valid after completion.
        dut.s_valid=0;idle(4*source_half+4*memory_half);active=false;
    }
};

int main(int argc,char** argv) {
    Verilated::commandArgs(argc,argv);
    try {
        if(argc==2 && std::string(argv[1])=="--corrupt-response") corrupt_response=true;
        const unsigned configurations[][3]={{2,3,0},{3,2,1},{5,7,3},{4,4,2},{32,1,0},{1,32,17},{1,1,0}};
        for(const auto& c:configurations) {
            auto t=std::make_unique<Test>(c[0],c[1],c[2]);t->reset(true);
            for(unsigned n=0;n<1000;n++) {t->start();t->finish(n%19==0 ? 1+n%3 : 0);}
            for(unsigned offset=0;offset<40;offset++) {
                t->start();t->idle(offset);t->reset(offset%2==0);
                t->start();t->finish();
            }
            // Source reset release must wait for a stopped destination clock.
            t->reset(true);t->dut.reset=1;t->step();t->dut.reset=0;t->pause_memory=200;
            t->idle(100);require(!t->dut.source_online,"offline destination was advertised ready");
            t->start();t->finish();
        }
        require(reset_coverage==15,"missing reset interruption phase coverage");
        std::cout<<"{\"status\":\"passed\",\"transfers\":"<<transfers<<",\"time_steps\":"<<steps
            <<",\"clock_configurations\":7,\"resets\":"<<resets<<",\"paused_transfers\":"<<pauses
            <<",\"reset_phase_coverage\":"<<reset_coverage<<"}\n";
    } catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 1;}
    return 0;
}
