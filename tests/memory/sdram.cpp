// SPDX-License-Identifier: MIT
// Independent pin-level SDR SDRAM model and flat byte-addressed request oracle.
// No controller hierarchy, state encoding, or internal counters are inspected.
#include "Vwasmetal_sdram_memory.h"
#include "verilated.h"
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>

#ifndef TEST_BYTES
#define TEST_BYTES 33554432
#define TEST_ROWS 13
#define TEST_COLUMNS 9
#define TEST_POWERUP 5000
#define TEST_REFRESH 195
#define TEST_CAS 2
#define TEST_RCD 1
#define TEST_RP 1
#define TEST_RFC 2
#define TEST_RAS 2
#define TEST_WR 2
#define TEST_RC 2
#define TEST_MRD 2
#endif

using Word=std::array<uint8_t,16>;
static uint8_t initial_byte(uint32_t address) {
    return uint8_t((address*73u)^(address>>8)^(address>>16)^0x9du);
}
static uint64_t random_state=0x6ad592f01b38c47eULL;
static uint32_t random_value() {
    random_state^=random_state<<13;random_state^=random_state>>7;random_state^=random_state<<17;
    return uint32_t(random_state>>16);
}
static Word random_word() {Word value{};for(auto& byte:value)byte=uint8_t(random_value());return value;}
static void require(bool condition,const char* message) {
    if(!condition)throw std::runtime_error(message);
}
struct Request {
    bool active=false,write=false,legal=false,saw_write=false;
    uint32_t address=0;
    uint16_t mask=0;
    Word data{};
    bool activated=false,burst_started=false;
};
struct Pins {
    bool cke,cs,ras,cas,we,oe;
    uint16_t address,data;
    uint8_t bank,dqm;
    explicit Pins(const Vwasmetal_sdram_memory& d):
        cke(d.sdram_cke),cs(d.sdram_cs_n),ras(d.sdram_ras_n),cas(d.sdram_cas_n),we(d.sdram_we_n),oe(d.sdram_dq_oe),
        address(d.sdram_address),data(d.sdram_dq_out),bank(d.sdram_bank),dqm(d.sdram_dqm) {}
    unsigned command()const{return cs ? 7u : ((unsigned(ras)<<2)|(unsigned(cas)<<1)|unsigned(we));}
};

struct Sdram {
    struct Bank {bool open=false;uint32_t row=0;int64_t active=-1000000,precharged=-1000000,written=-1000000;};
    std::array<Bank,4> banks{};
    std::unordered_map<uint32_t,uint16_t> words;
    Request& request;
    uint64_t cycles=0,activations=0,reads=0,writes=0,refreshes=0,write_beats=0,read_beats=0;
    uint64_t refresh_max_gap=0,write_byte_count=0;
    int64_t first_clock=-1,last_refresh=-1,blocked_until=0,last_activation=-1000000;
    bool precharged=false,mode=false,write_running=false,read_running=false;
    unsigned initial_refreshes=0,write_index=0;
    uint32_t burst_word=0;
    uint8_t burst_bank=0,drive_mask=0;
    uint16_t drive=0;
    int64_t read_start=0;
    std::array<uint8_t,2> mask_history{{3,3}};
    std::string mutation;
    explicit Sdram(Request& r,const std::string& m):request(r),mutation(m){}
    void check(bool ok,const char* message)const {
        if(!ok)throw std::runtime_error("SDRAM protocol violation at cycle "+std::to_string(cycles)+": "+message);
    }
    uint16_t load(uint32_t word)const {
        auto found=words.find(word);
        return found!=words.end() ? found->second : uint16_t(initial_byte(word*2)|(uint16_t(initial_byte(word*2+1))<<8));
    }
    bool closed()const{for(const auto& bank:banks)if(bank.open)return false;return true;}
    void expected_command()const {
        check(request.active && request.legal,"memory command without a legal request");
    }
    void store_beat(const Pins& p,int64_t now) {
        check(write_index<8,"write burst exceeded eight words");
        uint32_t word=burst_word+write_index;
        uint32_t byte_address=word*2;
        check(request.active && request.write && request.legal,"write without an accepted request");
        check(byte_address==request.address+2*write_index,"write address differs from request");
        uint8_t expected_mask=uint8_t((request.mask>>(2*write_index))&3);
        check(p.dqm==uint8_t(expected_mask^3),"write byte mask differs from request");
        if(expected_mask)check(p.oe,"write data bus is not driven");
        for(unsigned byte=0;byte<2;++byte)if(expected_mask&(1u<<byte))
            check(uint8_t(p.data>>(8*byte))==request.data[2*write_index+byte],"write data differs from request");
        uint16_t old=load(word);
        uint8_t applied=mutation=="--ignore-masks" ? 3 : expected_mask;
        for(unsigned byte=0;byte<2;++byte)if(applied&(1u<<byte)) {
            uint16_t bitmask=uint16_t(255u<<(8*byte));
            old=uint16_t((old&~bitmask)|(p.data&bitmask));++write_byte_count;
        }
        words[word]=old;banks[burst_bank].written=now;
        ++write_beats;++write_index;if(write_index==8)write_running=false;
    }
    void step(Pins p) {
        int64_t now=int64_t(cycles++);
        unsigned command=p.command();
        if(mode && mutation=="--mask-read-data" && request.active && !request.write)p.dqm=3;
        if(mode && mutation=="--omit-refresh" && command==1)command=7;
        if(mode && mutation=="--early-command" && now<blocked_until && command==7)command=3;
        check(!(p.oe && drive_mask),"DQ bus contention");
        drive_mask=0;drive=uint16_t(0xa50fu^uint16_t(now*319));
        uint8_t read_mask=mask_history[0];mask_history[0]=mask_history[1];mask_history[1]=p.dqm;
        if(!p.cke) {check(!mode && command==7 && !p.oe,"unexpected clock suspension");return;}
        if(first_clock<0)first_clock=now;
        if(command!=7)check(now-first_clock>=TEST_POWERUP,"command before power-up delay");
        if(command!=7)check(now>=blocked_until,"command before timing recovery");
        if(mode) {
            check(last_refresh>=0 && now-last_refresh<=TEST_REFRESH,"refresh deadline missed");
            refresh_max_gap=std::max(refresh_max_gap,uint64_t(now-last_refresh));
        }
        for(const auto& bank:banks)if(bank.open)check(now-bank.active<3000,"row remained active too long");
        bool continuation=write_running;
        if(continuation)check(command==7,"write burst interrupted");
        if(command==2) {
            check(!write_running && !read_running,"precharge interrupted a burst");
            bool all=(p.address&1024)!=0;
            check(all || banks[p.bank].open,"precharge of an idle bank");
            for(unsigned b=0;b<4;++b)if(all || b==p.bank) {
                check(!banks[b].open || now-banks[b].active>=TEST_RAS,"tRAS violated");
                check(now-banks[b].written>=TEST_WR,"write recovery violated");
                banks[b].open=false;banks[b].precharged=now;
            }
            precharged=true;
        } else if(command==1) {
            check(precharged && closed() && !read_running && !write_running,"refresh while a bank is active");
            for(const auto& bank:banks)check(now-bank.precharged>=TEST_RP,"refresh before tRP");
            blocked_until=now+TEST_RFC;last_refresh=now;++refreshes;
            if(!mode)++initial_refreshes;
        } else if(command==0) {
            check(!mode && initial_refreshes>=2 && closed(),"invalid initialization sequence");
            check(p.bank==0 && p.address==TEST_CAS*16+3,"incorrect mode register");
            blocked_until=now+TEST_MRD;mode=true;
        } else if(command==3) {
            expected_command();check(mode,"activate before mode programming");
            check(!request.activated,"request activated twice");request.activated=true;
            auto& bank=banks[p.bank];
            check(!bank.open && now-bank.precharged>=TEST_RP,"activate before precharge completion");
            check(now-bank.active>=TEST_RC && now-last_activation>=TEST_RC,"tRC violated");
            check(p.address<(1u<<TEST_ROWS),"row address exceeds geometry");
            check(p.bank==(request.address/(2u<<TEST_COLUMNS))%4,"bank address differs from request");
            check(p.address==request.address/(8u<<TEST_COLUMNS),"row address differs from request");
            bank.open=true;bank.row=p.address;bank.active=now;last_activation=now;++activations;
        } else if(command==4 || command==5) {
            expected_command();check(mode,"access before mode programming");
            check(request.activated && !request.burst_started,"duplicate or unactivated request burst");
            request.burst_started=true;
            const auto& bank=banks[p.bank];
            check(bank.open && now-bank.active>=TEST_RCD,"access before tRCD");
            check(!read_running && !write_running,"overlapping bursts");
            check(p.address<(1u<<TEST_COLUMNS) && (p.address&7)==0,"invalid burst column");
            check((command==4)==request.write,"read/write direction differs from request");
            burst_word=((bank.row*4+p.bank)<<TEST_COLUMNS)+p.address;burst_bank=p.bank;
            check(burst_word*2==request.address,"column address differs from request");
            if(command==4) {
                ++writes;request.saw_write=true;write_index=0;write_running=true;
            } else {
                ++reads;read_running=true;read_start=now+TEST_CAS;
                if(mutation=="--wrong-read-latency")--read_start;
            }
        } else check(command==7,"unsupported command");
        if(write_running)store_beat(p,now);
        else if(!continuation)check(!p.oe,"DQ driven outside a write burst");
        if(read_running && now>=read_start) {
            unsigned index=unsigned(now-read_start);
            if(index>=8)read_running=false;
            else {
                drive=load(burst_word+index);drive_mask=uint8_t((read_mask^3)&3);
                if(mutation=="--corrupt-read")drive^=1;
                for(unsigned byte=0;byte<2;++byte)if(!(drive_mask&(1u<<byte))) {
                    uint16_t mask=uint16_t(255u<<(8*byte));
                    uint16_t poison=uint16_t(0xa50fu^uint16_t(now*319));
                    drive=uint16_t((drive&~mask)|(poison&mask));
                }
                ++read_beats;
            }
        }
    }
};

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
