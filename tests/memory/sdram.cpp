// SPDX-License-Identifier: MIT
#include "Vwasmetal_sdram_memory.h"
#include "sdram_device.hpp"

struct Observation {bool ready,fault;Word data;};
struct Test {
    Vwasmetal_sdram_memory dut;
    Request request;
    Sdram memory;
    std::unordered_map<uint32_t,uint8_t> oracle;
    uint64_t transactions=0,resets=0,rejections=0,digest=1469598103934665603ULL;
    uint64_t stimulus=1469598103934665603ULL;
    uint64_t reset_reads=0,reset_writes=0,reset_open=0,reset_refresh=0;
    explicit Test(const std::string& mutation):memory(request,mutation) {
        dut.clk=0;dut.reset=1;dut.bus_reset=1;dut.valid=1;dut.write=0;dut.address=0;dut.mask=0;
        for(unsigned n=0;n<4;++n)dut.wdata[n]=0;
        for(unsigned n=0;n<3;++n)tick();
        dut.reset=0;
        for(unsigned n=0;!dut.initialized;++n) {require(n<TEST_POWERUP+100,"SDRAM initialization timed out");tick();}
        require(memory.mode && memory.initial_refreshes==2,"initialization did not program SDRAM");
        for(unsigned n=0;n<8;++n)tick();
        dut.bus_reset=0;dut.valid=0;tick();tick();
    }
    uint8_t expected(uint32_t address)const {
        auto found=oracle.find(address);return found==oracle.end() ? initial_byte(address) : found->second;
    }
    void mix(uint64_t value) {digest^=value;digest*=1099511628211ULL;}
    Observation tick() {
        dut.clk=0;dut.sdram_dq_in=memory.drive;dut.eval();
        Observation observation{bool(dut.ready),bool(dut.fault),{}};
        for(unsigned n=0;n<16;++n)observation.data[n]=uint8_t(dut.rdata[n/4]>>(8*(n%4)));
        require(!(dut.bus_reset && observation.ready),"response escaped a warm reset");
        Pins pins(dut);
        mix(pins.command()|(uint64_t(pins.address)<<3)|(uint64_t(pins.bank)<<16)|
            (uint64_t(pins.dqm)<<18)|(uint64_t(pins.oe)<<20));
        if(pins.oe)mix(pins.data);
        if(observation.ready) {mix(observation.fault);for(auto byte:observation.data)mix(byte);}
        memory.step(pins);
        dut.clk=1;dut.eval(); // still the old DQ value; the device changes after this edge
        dut.sdram_dq_in=memory.drive;dut.eval();
        return observation;
    }
    void begin(bool write,uint32_t address,uint16_t mask,const Word& value) {
        require(!request.active,"test overlaps requests");
        for(uint64_t item:{uint64_t(write),uint64_t(address),uint64_t(mask)}) {
            stimulus^=item;stimulus*=1099511628211ULL;
        }
        for(uint8_t byte:value) {stimulus^=byte;stimulus*=1099511628211ULL;}
        request={true,write,address%16==0 && mask!=0 && uint64_t(address)+16<=TEST_BYTES,false,address,mask,value};
        dut.valid=1;dut.write=write;dut.address=address;dut.mask=mask;
        for(unsigned n=0;n<4;++n) {
            uint32_t packed=0;for(unsigned b=0;b<4;++b)packed|=uint32_t(value[4*n+b])<<(8*b);
            dut.wdata[n]=packed;
        }
    }
    void account_write() {
        for(unsigned n=0;n<16;++n)if(request.mask&(1u<<n))oracle[request.address+n]=request.data[n];
        for(unsigned n=0;n<16;++n) {
            uint8_t actual=uint8_t(memory.load((request.address+n)/2)>>(8*((request.address+n)%2)));
            require(actual==expected(request.address+n),"SDRAM bytes differ from independent byte oracle");
        }
    }
    void transfer(bool write,uint32_t address,uint16_t mask,const Word& value={},unsigned hold=0) {
        begin(write,address,mask,value);
        Observation result{};unsigned waited=0;
        do {result=tick();require(++waited<TEST_REFRESH+300,"SDRAM transaction timed out");}while(!result.ready);
        if(result.fault==request.legal)throw std::runtime_error(
            "SDRAM fault disagrees with address/mask oracle: write="+std::to_string(write)+
            " address="+std::to_string(address)+" mask="+std::to_string(mask)+
            " fault="+std::to_string(result.fault)+" cycle="+std::to_string(memory.cycles));
        if(request.legal && write) {require(request.saw_write,"write acknowledged without a burst");account_write();}
        for(unsigned n=0;n<16;++n) {
            uint8_t value_expected=request.legal && !write ? expected(address+n) : 0;
            require(result.data[n]==value_expected,"SDRAM read differs from independent byte oracle");
        }
        if(!request.legal)++rejections;
        ++transactions;request.active=false;
        for(unsigned n=0;n<hold;++n)require(!tick().ready,"held request was acknowledged twice");
        dut.valid=0;tick();tick();
    }
    void warm_abort(bool write,unsigned delay,unsigned hold) {
        uint32_t address=(random_value()%(TEST_BYTES/16))*16;
        uint16_t mask=uint16_t(random_value()|1);
        Word data=random_word();
        begin(write,address,mask,data);
        for(unsigned n=0;n<delay;++n) {
            Observation seen=tick();
            if(seen.ready)break;
        }
        reset_reads+=memory.read_running;reset_writes+=memory.write_running;
        reset_open+=!memory.closed();
        reset_refresh+=int64_t(memory.cycles)<memory.blocked_until;
        dut.bus_reset=1;dut.valid=0;
        for(unsigned n=0;n<hold;++n)require(!tick().ready,"reset transaction produced a response");
        // Accepted writes may finish during reset, before any new request.
        if(request.saw_write)account_write();
        request.active=false;dut.bus_reset=0;
        for(unsigned n=0;n<4;++n)require(!tick().ready,"late response after warm reset");
        require(memory.closed() && !memory.read_running && !memory.write_running,"warm reset did not drain operations");
        require(dut.initialized,"warm reset reinitialized SDRAM");
        ++resets;
        transfer(false,address,0xffff);
    }
    void reset_at_refresh() {
        dut.valid=0;
        unsigned waited=0;
        while(Pins(dut).command()!=1) {tick();require(++waited<TEST_REFRESH+100,"refresh was never scheduled");}
        uint64_t prior=memory.refreshes;
        dut.bus_reset=1;tick();
        require(memory.refreshes==prior+1,"warm reset interrupted a refresh command");
        for(unsigned n=0;n<TEST_REFRESH*2;++n)require(!tick().ready,"response during refresh reset");
        dut.bus_reset=0;tick();tick();++resets;++reset_refresh;
    }
    void run() {
        transfer(false,0,0xffff,{},TEST_REFRESH*3);
        transfer(false,TEST_BYTES-16,0xffff);
        for(uint32_t mask=1;mask<=65535;++mask) {
            transfer(true,0,uint16_t(mask),random_word());
            transfer(false,0,0xffff);
        }
        for(unsigned n=0;n<4096;++n) {
            uint32_t address=(random_value()%(TEST_BYTES/16))*16;
            uint16_t mask=uint16_t(random_value()|1);
            Word data=random_word();
            transfer(true,address,mask,data);
            transfer(false,address,uint16_t(random_value()|1));
        }
        for(unsigned bank=0;bank<4;++bank)for(unsigned edge=0;edge<2;++edge) {
            uint32_t address=(bank*(2u<<TEST_COLUMNS))+(edge ? ((2u<<TEST_COLUMNS)-16) : 0);
            if(address<TEST_BYTES) {transfer(true,address,0xa55a,random_word());transfer(false,address,0xffff);}
        }
        for(unsigned byte=1;byte<16;++byte)transfer(true,byte,0xffff,random_word());
        transfer(false,0,0);transfer(true,0,0,random_word());
        transfer(true,TEST_BYTES,0xffff,random_word());
        transfer(false,0xfffffff0u,0xffff);transfer(true,0xfffffff8u,0xffff,random_word());
        for(unsigned delay=0;delay<64;++delay)for(bool write:{false,true})
            warm_abort(write,delay,TEST_REFRESH*2+100);
        reset_at_refresh();
        dut.bus_reset=1;
        for(unsigned n=0;n<TEST_REFRESH*10;++n)tick();
        dut.bus_reset=0;tick();transfer(false,TEST_BYTES-16,0xffff);
        require(reset_reads>0 && reset_writes>0 && reset_open>0 && reset_refresh>0,
            "reset did not cover active pin operations");
        std::cout<<"{\"transactions\":"<<transactions<<",\"warm_resets\":"<<resets
            <<",\"invalid_requests\":"<<rejections<<",\"cycles\":"<<memory.cycles
            <<",\"activations\":"<<memory.activations<<",\"read_bursts\":"<<memory.reads
            <<",\"write_bursts\":"<<memory.writes<<",\"read_beats\":"<<memory.read_beats
            <<",\"write_beats\":"<<memory.write_beats<<",\"written_bytes\":"<<memory.write_byte_count
            <<",\"refreshes\":"<<memory.refreshes<<",\"largest_refresh_gap\":"<<memory.refresh_max_gap
            <<",\"reset_during_read\":"<<reset_reads<<",\"reset_during_write\":"<<reset_writes
            <<",\"reset_with_open_bank\":"<<reset_open<<",\"reset_during_refresh\":"<<reset_refresh
            <<",\"stimulus_hash\":"<<stimulus
            <<",\"observation_hash\":"<<digest<<"}\n";
    }
};

int main(int argc,char** argv) {
    Verilated::commandArgs(argc,argv);
    try {Test test(argc>1 ? argv[1] : "");test.run();return 0;}
    catch(const std::exception& error) {std::cerr<<error.what()<<'\n';return 1;}
}
