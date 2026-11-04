#pragma once
// SPDX-License-Identifier: MIT
// Independent pin-level SDR SDRAM model and flat byte-addressed request oracle.
// No controller hierarchy, state encoding, or internal counters are inspected.
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
    template<class Model> explicit Pins(const Model& d):
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

