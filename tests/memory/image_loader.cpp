// SPDX-License-Identifier: MIT
// Independent byte/word oracle. No hierarchical DUT access or state mutation.
#include "Vwasmetal_image_loader.h"
#include "verilated.h"
#include <array>
#include <cstdlib>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <memory>
#include <random>
#include <stdexcept>
#include <vector>

#ifndef INSTRUCTIONS
#define INSTRUCTIONS 4
#define FUNCTIONS 2
#define TYPES 8
#define BOOT 4
#define REGIONS 2
#endif
#ifndef TAG_LOW
#define TAG_LOW 0x0706050403020100ULL
#define TAG_HIGH 0x0f0e0d0c0b0a0908ULL
#endif
static constexpr std::array<unsigned,5> rows{INSTRUCTIONS,FUNCTIONS,TYPES,6*REGIONS,BOOT};
static constexpr std::array<unsigned,5> widths{36,20,(TYPES+7)/8,8,29};
static bool corrupt_reply=false,corrupt_word=false;
static void require(bool ok,const char*why) {if(!ok)throw std::runtime_error(why);}
static uint32_t crc32(const std::vector<uint8_t>& data) {
    uint32_t crc=~0u;
    for(uint8_t byte:data) for(unsigned bit=0;bit<8;bit++) {
        bool parity=(crc^uint32_t(byte>>bit))&1;crc>>=1;if(parity)crc^=0xedb88320u;
    }
    return ~crc;
}
static uint16_t crc16(const std::vector<uint8_t>& data) {
    uint16_t crc=0xffff;
    for(uint8_t byte:data) for(unsigned bit=0;bit<8;bit++) {
        bool parity=((crc>>15)^(byte>>(7-bit)))&1;crc=uint16_t(crc<<1);if(parity)crc^=0x1021;
    }
    return crc;
}
static void append(std::vector<uint8_t>& data,uint64_t value,unsigned bytes) {
    for(unsigned n=0;n<bytes;n++)data.push_back(uint8_t(value>>(n*8)));
}
static uint64_t integer(const std::vector<uint8_t>& data,unsigned at,unsigned bytes) {
    uint64_t value=0;for(unsigned n=0;n<bytes;n++)value|=uint64_t(data.at(at+n))<<(8*n);return value;
}
static unsigned payload_size() {unsigned total=0;for(unsigned n=0;n<5;n++)total+=rows[n]*widths[n];return total;}
class Test {
public:
    Vwasmetal_image_loader dut;
    std::mt19937 random{0xc01dc0de};
    uint64_t clocks=0,words=0,replies=0,commits=0,resets=0;
    unsigned expected_word=0;
    bool stalled=false;
    std::vector<uint8_t> expected,reply_bytes;
    // Per-row oracle: the bytes each store row must receive, written once.
    std::array<std::vector<std::vector<uint8_t>>,5> row_data;
    std::array<std::vector<bool>,5> written;
    void expect_full(const std::vector<uint8_t>& payload) {
        unsigned offset=0;
        for(unsigned s=0;s<5;s++) {
            row_data[s].assign(rows[s],{});written[s].assign(rows[s],false);
            for(unsigned i=0;i<rows[s];i++,offset+=widths[s])
                row_data[s][i].assign(payload.begin()+offset,payload.begin()+offset+widths[s]);
        }
    }
    Test(){dut.clk=0;dut.rx_valid=0;dut.abort_load=0;reset();}
    void tick() {
        dut.tx_ready=stalled ? 0 : random()%4!=0;dut.eval();
        if(dut.word_valid) {
            require(!dut.image_valid,"image executable during a store write");
            unsigned section=dut.word_section,index=dut.word_index;
            require(section<5 && index<rows[section] && !row_data[section].empty(),"out of bounds image write");
            require(!written[section][index],"duplicate image write");
            for(unsigned n=0;n<widths[section];n++) {
                uint8_t byte=uint8_t(dut.word_data[n/4]>>((n%4)*8));
                if(corrupt_word && n==0)byte^=1;
                require(byte==row_data[section][index][n],"image write differs from independent byte oracle");
            }
            written[section][index]=true;expected_word++;words++;
        }
        if(dut.tx_valid && dut.tx_ready) {
            uint8_t byte=dut.tx_data;
            if(corrupt_reply && reply_bytes.size()==18)byte^=1;
            reply_bytes.push_back(byte);
        }
        dut.clk=1;dut.eval();dut.clk=0;dut.eval();clocks++;
    }
    void reset() {
        dut.reset=1;dut.rx_valid=0;dut.abort_load=0;tick();tick();dut.reset=0;
        reply_bytes.clear();expected_word=0;resets++;tick();require(!dut.image_valid,"reset preserved commit permission");
    }
    void send(uint8_t byte,unsigned gap=0) {
        dut.rx_valid=0;for(unsigned n=0;n<gap;n++)tick();
        dut.rx_valid=1;dut.rx_data=byte;tick();dut.rx_valid=0;
    }
    std::vector<uint8_t> header(uint64_t nonce,int mutation=0) {
        std::vector<uint8_t> bytes{0x57,0x4d,0x4c,0x44,1};append(bytes,nonce,8);
        append(bytes,TAG_LOW,8);append(bytes,TAG_HIGH,8);
        append(bytes,payload_size(),4);
        if(mutation==2)bytes[4]=3;
        if(mutation==3)bytes[13]^=1;
        if(mutation==4)bytes[29]^=1;
        expected.resize(payload_size());for(auto&byte:expected)byte=uint8_t(random());expected_word=0;
        expect_full(expected);
        for(uint8_t byte:bytes)send(byte,random()%3);
        require(!dut.image_valid,"new header did not invalidate previous image");
        return bytes;
    }
    void reply(unsigned status,uint64_t nonce,uint32_t image_crc=0) {
        for(unsigned n=0;reply_bytes.size()<20 && n<1000;n++)tick();
        require(reply_bytes.size()==20,"missing or oversized loader reply");
        std::vector<uint8_t> expected_reply{0x57,0x4d,0x4c,0x52,1,uint8_t(status)};
        append(expected_reply,nonce,8);append(expected_reply,image_crc,4);
        append(expected_reply,crc16(std::vector<uint8_t>(expected_reply.begin()+4,expected_reply.end())),2);
        if(reply_bytes!=expected_reply && std::getenv("LOADER_DEBUG")) {
            std::cerr<<"expected status "<<status<<" got "<<unsigned(reply_bytes[5])<<" nonce "<<nonce<<"\n";
        }
        require(reply_bytes==expected_reply,"loader reply differs from independent oracle");
        replies++;reply_bytes.clear();
        if(status==1){require(dut.image_valid,"complete image was not committed");commits++;}
        else require(!dut.image_valid,"invalid or incomplete image was committed");
    }
    // Version 2: five row counts, those rows, then zero rows written by the loader.
    void compact(uint64_t nonce,std::array<unsigned,5> counts,int mutation=0,bool gaps=false) {
        std::vector<uint8_t> payload;
        for(unsigned s=0;s<5;s++)append(payload,counts[s],4);
        for(unsigned s=0;s<5;s++) {
            row_data[s].assign(rows[s],std::vector<uint8_t>(widths[s],0));written[s].assign(rows[s],false);
            for(unsigned i=0;i<counts[s] && i<rows[s];i++)
                for(auto&byte:row_data[s][i]){byte=uint8_t(random());payload.push_back(byte);}
        }
        uint32_t length=uint32_t(payload.size());
        if(mutation==1)length++;
        std::vector<uint8_t> bytes{0x57,0x4d,0x4c,0x44,2};append(bytes,nonce,8);
        append(bytes,TAG_LOW,8);append(bytes,TAG_HIGH,8);append(bytes,length,4);
        expected_word=0;for(uint8_t byte:bytes)send(byte,random()%3);
        require(!dut.image_valid,"new header did not invalidate previous image");
        reply(0,nonce);
        bool oversized=false;for(unsigned s=0;s<5;s++)oversized|=counts[s]>rows[s];
        if(mutation==1 || oversized) {
            for(unsigned n=0;n<20;n++)send(payload[n]);
            reply(4,nonce);require(expected_word==0,"rejected compact layout wrote a row");return;
        }
        std::vector<uint8_t> body(bytes.begin()+4,bytes.end());body.insert(body.end(),payload.begin(),payload.end());
        uint32_t checksum=crc32(body);
        for(uint8_t byte:payload)send(byte,gaps ? random()%8 : 0);
        std::vector<uint8_t> trailer;append(trailer,mutation==2 ? checksum^1 : checksum,4);
        stalled=true;for(uint8_t byte:trailer)send(byte);
        unsigned total=0;for(unsigned count:rows)total+=count;
        for(unsigned n=0;n<total+100;n++){tick();require(!dut.image_valid,"commit before acknowledgment was accepted");}
        unsigned sent=0;for(unsigned s=0;s<5;s++)sent+=counts[s];
        require(expected_word==(mutation==2 ? sent : total),"compact image did not write every row exactly once");
        stalled=false;reply(mutation==2 ? 5 : 1,nonce,checksum);
    }
    void upload(uint64_t nonce,bool bad_crc=false,bool gaps=false) {
        auto bytes=header(nonce);reply(0,nonce);std::vector<uint8_t> body(bytes.begin()+4,bytes.end());
        body.insert(body.end(),expected.begin(),expected.end());uint32_t checksum=crc32(body);
        for(uint8_t byte:expected)send(byte,gaps ? random()%8 : 0);
        unsigned total=0;for(unsigned count:rows)total+=count;
        std::vector<uint8_t> trailer;append(trailer,bad_crc ? checksum^1 : checksum,4);
        stalled=true;for(uint8_t byte:trailer)send(byte);
        for(unsigned n=0;n<100;n++){tick();require(!dut.image_valid,"commit before acknowledgment was accepted");}
        require(expected_word==total,"image did not fill every store row");
        stalled=false;reply(bad_crc ? 5 : 1,nonce,checksum);
    }
};
int main(int argc,char**argv) {
    try {
        Verilated::commandArgs(argc,argv);
        if(argc==2 && std::string(argv[1])=="--corrupt-reply")corrupt_reply=true;
        if(argc==2 && std::string(argv[1])=="--corrupt-word")corrupt_word=true;
        std::vector<uint8_t> check{'1','2','3','4','5','6','7','8','9'};
        require(crc32(check)==0xcbf43926 && crc16(check)==0x29b1,"CRC oracle known vector failed");
        auto t=std::make_unique<Test>();
        if(argc==3 && std::string(argv[1])=="--packet") {
            std::ifstream file(argv[2],std::ios::binary);require(bool(file),"cannot open encoded image");
            std::vector<uint8_t> packet((std::istreambuf_iterator<char>(file)),std::istreambuf_iterator<char>());
            require(packet.size()==33+payload_size()+4,"wrong encoded image size");
            uint64_t nonce=integer(packet,5,8);uint32_t checksum=uint32_t(integer(packet,unsigned(packet.size()-4),4));
            require(crc32(std::vector<uint8_t>(packet.begin()+4,packet.end()-4))==checksum,"Python and C++ CRC oracles disagree");
            t->expected.assign(packet.begin()+33,packet.end()-4);
            t->expect_full(t->expected);
            for(unsigned n=0;n<33;n++)t->send(packet[n]);
            t->reply(0,nonce);
            for(size_t n=33;n<packet.size();n++)t->send(packet[n]);
            t->reply(1,nonce,checksum);
            std::cout<<"{\"status\":\"passed\",\"words\":"<<t->words<<",\"checksum\":"<<checksum<<"}\n";
            return 0;
        }
        for(uint64_t n=0;n<30;n++)t->upload(0x0123456789abcdefULL+n,n%7==0,n%3==0);
        // Compact uploads: random, empty and full sections, gaps and bad CRCs.
        for(uint64_t n=0;n<60;n++) {
            std::array<unsigned,5> counts{};
            for(unsigned s=0;s<5;s++)counts[s]=n%5==s ? rows[s] : n%4==0 ? 0 : t->random()%(rows[s]+1);
            t->compact(0x5700000000000000ULL+n,counts,n%9==8 ? 2 : 0,n%2==1);
        }
        t->compact(0x5710000000000000ULL,{0,0,0,0,0});
        t->compact(0x5720000000000000ULL,{rows[0],rows[1],rows[2],rows[3],rows[4]});
        // Inconsistent declared length and counts beyond each store are rejected.
        t->compact(0x5730000000000000ULL,{1,1,1,1,1},1);
        for(unsigned s=0;s<5;s++) {
            std::array<unsigned,5> counts{};counts[s]=rows[s]+1;
            t->compact(0x5740000000000000ULL+s,counts);
        }
        for(unsigned status=2;status<=4;status++){t->header(100+status,status);t->reply(status,100+status);}
        // Timeout in header, payload and each partial checksum length.
        t->send(0x57);t->send(0x4d);t->send(0x4c);t->send(0x44);t->reply(6,0);
        for(unsigned missing=0;missing<5;missing++) {
            t->header(200+missing);t->reply(0,200+missing);
            if(missing) {
                for(uint8_t byte:t->expected)t->send(byte);
                for(unsigned n=0;n<missing-1;n++)t->send(0);
            }
            t->reply(6,200+missing);
        }
        // Interrupted partial words at every byte position, then a clean retry.
        for(unsigned offset=0;offset<40;offset++) {
            t->header(300+offset);t->reply(0,300+offset);
            for(unsigned n=0;n<offset;n++)t->send(t->expected[n]);
            if(offset&1) {t->dut.abort_load=1;t->tick();t->dut.abort_load=0;t->reply(7,300+offset);}
            else t->reset();
        }
        unsigned boundary=0;
        for(unsigned section=0;section<5;section++) {
            boundary+=rows[section]*widths[section];
            for(unsigned offset:{boundary-1,boundary}) {
                t->header(500+offset);t->reply(0,500+offset);
                for(unsigned n=0;n<offset;n++)t->send(t->expected[n]);
                t->dut.abort_load=1;t->tick();t->dut.abort_load=0;t->reply(7,500+offset);
            }
        }
        // Even a verified CRC cannot authorize execution through a reset before
        // the transmitter has accepted the complete commit acknowledgment.
        auto header=t->header(600);t->reply(0,600);
        std::vector<uint8_t> body(header.begin()+4,header.end());body.insert(body.end(),t->expected.begin(),t->expected.end());
        for(uint8_t byte:t->expected)t->send(byte);
        std::vector<uint8_t> trailer;append(trailer,crc32(body),4);
        t->stalled=true;for(uint8_t byte:trailer)t->send(byte);
        for(unsigned n=0;n<10;n++){t->tick();require(!t->dut.image_valid,"verified CRC bypassed acknowledgment");}
        t->reset();t->stalled=false;
        // Reset while reply is backpressured, including after a verified image.
        t->stalled=true;t->header(400);t->reset();t->stalled=false;
        t->upload(401);t->reset();
        // Partial magic expires; overlapping prefixes still resynchronize.
        t->send(0x57);t->send(0x4d);for(unsigned n=0;n<70;n++)t->tick();t->send(0x4c);t->send(0x44);
        for(unsigned n=0;n<70;n++)t->tick();
        require(t->reply_bytes.empty(),"expired magic was accepted");
        t->send(0x57);t->send(0x57);t->upload(402);
        std::cout<<"{\"status\":\"passed\",\"payload_bytes\":"<<payload_size()<<",\"cycles\":"<<t->clocks
            <<",\"words\":"<<t->words<<",\"replies\":"<<t->replies<<",\"commits\":"<<t->commits
            <<",\"resets\":"<<t->resets<<"}\n";
    } catch(const std::exception&e) {std::cerr<<e.what()<<"\n";return 1;}
}
