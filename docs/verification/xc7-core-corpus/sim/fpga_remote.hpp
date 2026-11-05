// SPDX-License-Identifier: MIT
#pragma once
#include "fpga_ports.hpp"
#include <cerrno>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <stdexcept>
#include <string>
#include <tuple>
#ifdef WASMETAL_UART_MODEL
#include "Vwasmetal_ulx3s.h"
#include "verilated.h"
#else
#include <fcntl.h>
#include <poll.h>
#include <sys/file.h>
#include <termios.h>
#include <unistd.h>
#endif

// CCITT-FALSE: polynomial 0x1021, initial value 0xffff, no reflection/xorout.
inline uint16_t fpga_crc(const std::vector<uint8_t>& bytes,size_t first,size_t end) {
    uint16_t crc=0xffff;
    for(size_t n=first;n<end;n++) {
        crc^=uint16_t(bytes[n])<<8;
        for(unsigned bit=0;bit<8;bit++) crc=uint16_t((crc<<1)^((crc&0x8000)?0x1021:0));
    }
    return crc;
}

#ifdef WASMETAL_UART_MODEL
class FpgaTransport {
    Vwasmetal_ulx3s board;
    std::deque<uint8_t> received;
    int sample_bit=-1, sample_count=0;
    uint8_t sample_value=0;
    void tick() {
        board.clk_25mhz=0; board.eval(); board.clk_25mhz=1; board.eval();
        if(sample_bit<0) {
            if(!board.ftdi_rxd) { sample_bit=0; sample_count=74; sample_value=0; }
        } else if(sample_count) sample_count--;
        else if(sample_bit<8) {
            sample_value|=uint8_t(board.ftdi_rxd<<sample_bit); sample_bit++; sample_count=49;
        } else {
            if(!board.ftdi_rxd) throw std::runtime_error("FPGA model UART framing error");
            received.push_back(sample_value); sample_bit=-1;
        }
    }
    void bit(unsigned value) { board.ftdi_txd=value; for(unsigned n=0;n<50;n++) tick(); }
public:
    FpgaTransport() {
        board.ftdi_txd=1; board.btn_n=0;
        for(unsigned n=0;n<20;n++) tick();
        board.btn_n=1; for(unsigned n=0;n<20;n++) tick();
    }
    void abandon_prefix(const std::vector<uint8_t>& prefix) {
        for(auto byte:prefix) {
            bit(0); for(unsigned n=0;n<8;n++) bit((byte>>n)&1U); bit(1);
        }
        for(unsigned n=0;n<5000000;n++) tick();
        if(!received.empty()) throw std::runtime_error("FPGA responded to an incomplete frame");
    }
    std::vector<uint8_t> exchange(const std::vector<uint8_t>& request,size_t response_size) {
        for(auto byte:request) {
            bit(0); for(unsigned n=0;n<8;n++) bit((byte>>n)&1U); bit(1);
        }
        unsigned budget=unsigned(response_size*600+20000);
        while(received.size()<response_size && budget) { tick(); budget--; }
        if(received.size()!=response_size) throw std::runtime_error("FPGA model UART response timeout/length error");
        std::vector<uint8_t> response(received.begin(),received.end()); received.clear(); return response;
    }
};
#else
class FpgaTransport {
    int fd=-1;
    void wait(short events) {
        pollfd descriptor{fd,events,0};
        int status;
        do { status=::poll(&descriptor,1,5000); } while(status<0 && errno==EINTR);
        if(status<=0 || !(descriptor.revents&events)) throw std::runtime_error("FPGA serial timeout/disconnect; reset the session before retrying");
    }
public:
    FpgaTransport() {
        const char* device=std::getenv("WASMETAL_SERIAL");
        if(!device || !*device) throw std::runtime_error("Set WASMETAL_SERIAL to the FPGA's serial device");
        fd=::open(device,O_RDWR|O_NOCTTY|O_CLOEXEC|O_NONBLOCK);
        if(fd<0) throw std::runtime_error("cannot open FPGA serial device: "+std::string(std::strerror(errno)));
        try {
            if(::flock(fd,LOCK_EX|LOCK_NB)<0) throw std::runtime_error("FPGA serial device already in use");
            termios settings{};
            if(::tcgetattr(fd,&settings)<0) throw std::runtime_error("cannot read serial settings");
            ::cfmakeraw(&settings); settings.c_cflag&=~(CRTSCTS|CSTOPB|PARENB|CSIZE);
            settings.c_cflag|=CLOCAL|CREAD|CS8; settings.c_iflag&=~(IXON|IXOFF|IXANY);
            if(::cfsetispeed(&settings,B500000)<0 || ::cfsetospeed(&settings,B500000)<0 || ::tcsetattr(fd,TCSANOW,&settings)<0)
                throw std::runtime_error("cannot configure 500 kbaud serial link");
            // Let the bridge's 100 ms receive watchdog discard an abandoned frame.
            ::usleep(120000); ::tcflush(fd,TCIOFLUSH);
        } catch(...) { ::close(fd); fd=-1; throw; }
    }
    ~FpgaTransport() { if(fd>=0) ::close(fd); }
    FpgaTransport(const FpgaTransport&)=delete;
    FpgaTransport& operator=(const FpgaTransport&)=delete;
    void abandon_prefix(const std::vector<uint8_t>& prefix) {
        size_t offset=0;
        while(offset<prefix.size()) {
            wait(POLLOUT); auto n=::write(fd,prefix.data()+offset,prefix.size()-offset);
            if(n<0 && (errno==EINTR || errno==EAGAIN)) continue;
            if(n<=0) throw std::runtime_error("FPGA serial write failed");
            offset+=size_t(n);
        }
        ::usleep(200000);
    }
    std::vector<uint8_t> exchange(const std::vector<uint8_t>& request,size_t response_size) {
        size_t offset=0;
        while(offset<request.size()) {
            wait(POLLOUT); auto n=::write(fd,request.data()+offset,request.size()-offset);
            if(n<0 && (errno==EINTR || errno==EAGAIN)) continue;
            if(n<=0) throw std::runtime_error("FPGA serial write failed");
            offset+=size_t(n);
        }
        std::vector<uint8_t> response(response_size); offset=0;
        while(offset<response_size) {
            wait(POLLIN); auto n=::read(fd,response.data()+offset,response_size-offset);
            if(n<0 && (errno==EINTR || errno==EAGAIN)) continue;
            if(n<=0) throw std::runtime_error("FPGA serial read failed");
            offset+=size_t(n);
        }
        return response;
    }
};
#endif

class FpgaRemote : public FpgaPorts {
    FpgaTransport transport;
    uint8_t sequence_number=0;
    bool previous_clock=false;
    std::vector<uint8_t> transact(uint8_t mode,bool corrupt=false) {
        auto payload=pack_inputs();
        std::vector<uint8_t> request{0x57,0x4d,mode,sequence_number};
        request.insert(request.end(),payload.begin(),payload.end());
        auto crc=fpga_crc(request,2,request.size()); if(corrupt) crc^=1;
        request.push_back(uint8_t(crc)); request.push_back(uint8_t(crc>>8));
        auto response=transport.exchange(request,OUTPUT_BYTES+6);
        if(response[0]!=0x57 || response[1]!=0x52 || response[3]!=sequence_number++)
            throw std::runtime_error("FPGA response framing/sequence mismatch");
        auto checksum=fpga_crc(response,2,response.size()-2);
        if(checksum!=(uint16_t(response[response.size()-2])|(uint16_t(response.back())<<8)))
            throw std::runtime_error("FPGA response checksum mismatch");
        return response;
    }
public:
    unsigned value_capacity=0,control_capacity=0,call_capacity=0,descriptor_capacity=0,heap_capacity=0;
    FpgaRemote() {
        auto response=transact(2);
        auto word=[&](unsigned index) { unsigned p=4+index*4; return uint32_t(response[p])|(uint32_t(response[p+1])<<8)|(uint32_t(response[p+2])<<16)|(uint32_t(response[p+3])<<24); };
        if(response[2] || word(0)!=0x574d0001 || word(6)!=INPUT_BYTES || word(7)!=OUTPUT_BYTES || word(8)!=SCHEMA_ID)
            throw std::runtime_error("FPGA image protocol/schema mismatch");
        for(unsigned n=0;n<4;n++) if(word(9+n)!=BUILD_WORDS[n])
            throw std::runtime_error("FPGA image source fingerprint mismatch; load the matching bitstream");
        value_capacity=word(1); control_capacity=word(2); call_capacity=word(3); descriptor_capacity=word(4); heap_capacity=word(5);
    }
    void eval() {
        auto response=transact(clk && !previous_clock);
        if(response[2]) throw std::runtime_error("FPGA rejected request, status="+std::to_string(response[2]));
        previous_clock=clk;
        unpack_outputs(std::vector<uint8_t>(response.begin()+4,response.end()-2));
    }
    void final() {}
    void check_corrupt_frame() {
        if(busy) throw std::runtime_error("CRC probe requires an idle core");
        auto snapshot=[&] { return std::make_tuple(busy,done,trap,pc,result_count,function_index,mem_valid); };
        auto before=snapshot();
        auto saved_valid=cmd_valid; auto saved_kind=cmd_kind;
        cmd_valid=1; cmd_kind=0; eval();
        auto response=transact(true,true);
        if(response[2]!=1) throw std::runtime_error("FPGA accepted a corrupt request");
        eval(); if(snapshot()!=before) throw std::runtime_error("Corrupt FPGA frame changed execution state");
        response=transact(3);
        if(response[2]!=2) throw std::runtime_error("FPGA accepted invalid request flags");
        eval(); if(snapshot()!=before) throw std::runtime_error("Invalid flags changed execution state");
        response=transact(2);
        if(response[2]) throw std::runtime_error("FPGA capability query failed");
        eval(); if(snapshot()!=before) throw std::runtime_error("Capability query changed execution state");
        transport.abandon_prefix({0x57,0x4d,1,sequence_number,0});
        cmd_valid=saved_valid; cmd_kind=saved_kind; eval();
        if(snapshot()!=before) throw std::runtime_error("Incomplete FPGA frame changed execution state");
    }
};
