// SPDX-License-Identifier: MIT
// Pins only: independent UART sender/receiver, reset, and completion indicators.
#include "verilated.h"
#ifdef WASMETAL_BOARD
#include "Vwasmetal_loadable_ulx3s.h"
using Model=Vwasmetal_loadable_ulx3s;
#else
#include "Vwasmetal_loadable.h"
using Model=Vwasmetal_loadable;
#endif
#include <cstdint>
#include <fstream>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>
#ifndef BIT_TICKS
#define BIT_TICKS 16
#define CLOCK_SCALE 1
#define UPLOAD_TIMEOUT 4096
#endif
static void require(bool value,const char*why){if(!value)throw std::runtime_error(why);}
static uint64_t integer(const std::vector<uint8_t>& bytes,size_t at,unsigned width) {
    uint64_t value=0;for(unsigned n=0;n<width;n++)value|=uint64_t(bytes.at(at+n))<<(n*8);return value;
}
static uint16_t crc16(const std::vector<uint8_t>& bytes,size_t at,size_t end) {
    uint16_t crc=0xffff;
    for(;at<end;at++)for(unsigned n=0;n<8;n++) {
        bool parity=((crc>>15)^(bytes[at]>>(7-n)))&1;crc=uint16_t(crc<<1);if(parity)crc^=0x1021;
    }
    return crc;
}
class Receiver {
    unsigned state=0,count=0,bit=0,value=0;
public:
    std::vector<uint8_t> bytes;
    void sample(bool high) {
        if(state==0){if(!high){state=1;count=BIT_TICKS+BIT_TICKS/2-1;bit=0;value=0;}}
        else if(count)count--;
        else if(state==1){if(high)value|=1u<<bit;count=BIT_TICKS-1;if(++bit==8)state=2;}
        else {require(high,"loadable UART framing error");bytes.push_back(uint8_t(value));state=0;}
    }
};
class Test {
public:
    Model dut;
    Receiver receiver;
    uint64_t clocks=0,first_result=0;
    unsigned period_permille=1000;
    bool record_result=false;
    uint64_t fractional_time=0;
    size_t reply_cursor=0;
    bool serial() {
#ifdef WASMETAL_BOARD
        return dut.ftdi_rxd;
#else
        return dut.tx;
#endif
    }
    bool finished() {
#ifdef WASMETAL_BOARD
        return !dut.led_busy;
#else
        return dut.finished;
#endif
    }
    void rx(bool value) {
#ifdef WASMETAL_BOARD
        dut.ftdi_txd=value;
#else
        dut.rx=value;
#endif
    }
    void tick(bool capture=true) {
#ifdef WASMETAL_BOARD
        dut.clk_25mhz=0;dut.eval();dut.clk_25mhz=1;dut.eval();dut.clk_25mhz=0;dut.eval();
#else
        dut.clk=0;dut.eval();dut.clk=1;dut.eval();dut.clk=0;dut.eval();
#endif
        clocks++;
        if(capture){receiver.sample(serial());if(record_result && !serial() && !first_result)first_result=clocks;}
    }
    void reset() {
        rx(true);
#ifdef WASMETAL_BOARD
        dut.btn_n=0;
#else
        dut.reset=1;
#endif
        for(unsigned n=0;n<128;n++)tick(false);
#ifdef WASMETAL_BOARD
        dut.btn_n=1;
#else
        dut.reset=0;
#endif
        receiver=Receiver{};reply_cursor=0;record_result=false;first_result=0;
        for(unsigned n=0;n<128;n++)tick();
        require(!finished(),"reset did not revoke execution permission");
    }
    void bit(bool high) {
        rx(high);fractional_time+=uint64_t(BIT_TICKS)*period_permille;
        unsigned count=unsigned(fractional_time/1000);fractional_time%=1000;
        for(unsigned n=0;n<count;n++)tick();
    }
    void send(uint8_t byte) {bit(false);for(unsigned n=0;n<8;n++)bit((byte>>n)&1);bit(true);}
    void unloaded() {
#ifndef WASMETAL_BOARD
        require(!dut.image_valid,"failed upload authorized CPU execution");
#endif
        require(!finished(),"failed upload completed execution");
    }
    void reply(uint64_t nonce,unsigned expected,uint32_t checksum=0) {
        const uint64_t deadline=clocks+UPLOAD_TIMEOUT+25*10*BIT_TICKS+4096*CLOCK_SCALE;
        for(;clocks<deadline;tick()) {
            while(receiver.bytes.size()-reply_cursor>=20) {
                size_t at=reply_cursor++;const auto&b=receiver.bytes;
                if(b[at]!=0x57 || b[at+1]!=0x4d || b[at+2]!=0x4c || b[at+3]!=0x52 || b[at+4]!=1)continue;
                if(crc16(b,at+4,at+18)!=integer(b,at+18,2) || integer(b,at+6,8)!=nonce)continue;
                require(b[at+5]==expected,"unexpected image-loader reply status");
                if(expected==1)require(integer(b,at+14,4)==checksum,"committed CRC differs from encoded image");
                reply_cursor=at+20;return;
            }
        }
        throw std::runtime_error("no valid upload acknowledgment");
    }
    void operation(const std::string&kind,const std::string&path,uint64_t offset) {
        std::ifstream file(path,std::ios::binary);require(bool(file),"cannot open upload packet");
        std::vector<uint8_t> bytes((std::istreambuf_iterator<char>(file)),std::istreambuf_iterator<char>());
        require(bytes.size()>=37 && integer(bytes,29,4)+37==bytes.size(),"invalid packet length");
        const uint64_t nonce=integer(bytes,5,8);const uint32_t checksum=uint32_t(integer(bytes,bytes.size()-4,4));
        receiver=Receiver{};reply_cursor=0;record_result=false;first_result=0;
        const uint64_t start=clocks;uint64_t commit_clock=0;bool interrupted=false;
        if(kind=="bad-profile")bytes[13]^=1;
        if(kind=="bad-crc")bytes.back()^=1;
        for(size_t n=0;n<33;n++)send(bytes[n]);
        if(kind=="bad-profile"){reply(nonce,3);unloaded();}
        else {
            reply(nonce,0);
            if(kind=="partial" || kind=="timeout" || kind=="break") {
                require(offset<=bytes.size()-37,"partial upload exceeds payload");
                for(size_t n=0;n<offset;n++)send(bytes[33+n]);
                if(kind=="partial"){reset();interrupted=true;}
                else if(kind=="timeout"){rx(true);reply(nonce,6);}
                else {for(unsigned n=0;n<12;n++)bit(false);bit(true);reply(nonce,7);}
                unloaded();
            } else {
                for(size_t n=33;n<bytes.size();n++)send(bytes[n]);
                reply(nonce,kind=="bad-crc" ? 5 : 1,checksum);commit_clock=clocks;
                if(kind=="bad-crc")unloaded();
                else {
                    record_result=true;
                    const uint64_t deadline=clocks+12000000ULL*CLOCK_SCALE;
                    while(!finished() && clocks<deadline) {
                        if(kind=="interrupt" && clocks-commit_clock==offset){reset();interrupted=true;break;}
                        tick();
                    }
                    if(kind=="interrupt"){require(interrupted,"scheduled upload-system reset never occurred");unloaded();}
                    else require(finished(),"uploaded program did not finish");
                }
            }
        }
        std::cout<<"{\"operation\":\""<<kind<<"\",\"clocks\":"<<clocks-start
            <<",\"commit_clock\":"<<(commit_clock ? commit_clock-start : 0)
            <<",\"first_result_clock\":"<<(first_result ? first_result-start : 0)
            <<",\"interrupted\":"<<(interrupted ? "true" : "false")<<",\"uart\":\"";
        const char*hex="0123456789abcdef";for(uint8_t byte:receiver.bytes)std::cout<<hex[byte>>4]<<hex[byte&15];
        std::cout<<"\"}\n"<<std::flush;
    }
};
int main(int argc,char**argv) {
    try {
        Verilated::commandArgs(argc,argv);auto test=std::make_unique<Test>();test->rx(true);test->reset();
        for(int n=1;n<argc;n++) {
            std::string flag=argv[n];
            if(flag=="--period-permille" && n+1<argc){test->period_permille=unsigned(std::stoul(argv[++n]));continue;}
            require(n+1<argc,"missing upload file");std::string path=argv[++n];uint64_t offset=0;
            require(flag=="--upload" || flag=="--bad-crc" || flag=="--bad-profile" || flag=="--partial" ||
                flag=="--timeout" || flag=="--break" || flag=="--interrupt","unknown loadable driver option");
            if(flag=="--partial" || flag=="--timeout" || flag=="--break" || flag=="--interrupt") {
                require(n+1<argc,"missing interruption offset");offset=std::stoull(argv[++n]);
            }
            test->operation(flag.substr(2),path,offset);
        }
    } catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}
}
