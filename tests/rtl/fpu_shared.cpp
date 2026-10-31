// SPDX-License-Identifier: MIT
#include "Vfpu_shared_tb.h"
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
#include <string>

static uint64_t state=0x5741534d4554414cULL;
static uint64_t random_bits() {
    state^=state>>12; state^=state<<25; state^=state>>27;
    return state*0x2545f4914f6cdd1dULL;
}
static void tick(Vfpu_shared_tb &dut) {
    dut.clk=1; dut.eval(); dut.clk=0; dut.eval();
}
static uint64_t count=0;
static bool corrupt_value=false,corrupt_trap=false;
static void check(Vfpu_shared_tb &dut, bool, unsigned operation, uint64_t a,uint64_t b) {
    dut.op=operation;dut.a=a;dut.b=b;dut.start=0;dut.eval();
    if(!dut.actual_supported || dut.actual_supported!=dut.expected_supported || dut.actual_unary!=dut.expected_unary) {
        std::cerr<<"FP decode mismatch op="<<operation<<"\n";std::exit(1);
    }
    uint64_t actual=0,expected=0;unsigned actual_trap=0,expected_trap=0;
    dut.start=1;tick(dut);dut.start=0;dut.eval();
    bool have_actual=false,have_expected=false;
    for(unsigned cycle=0;cycle<130;cycle++) {
        if(dut.actual_done) {actual=dut.actual;actual_trap=dut.actual_trap;have_actual=true;}
        if(dut.expected_done) {expected=dut.expected;expected_trap=dut.expected_trap;have_expected=true;}
        if(have_actual && have_expected) break;
        tick(dut);
    }
    if(!have_actual || !have_expected) {
        std::cerr<<"Floating-point unit timeout op="<<operation<<"\n";std::exit(1);
    }
    tick(dut);
    if(corrupt_value) actual^=1;
    if(corrupt_trap) actual_trap^=1;
    // Trap results have no architectural value. Compare their trap class.
    if(actual_trap!=expected_trap || (actual_trap==0 && actual!=expected)) {
        std::cerr<<"FPU mismatch op="<<std::hex<<operation
                 <<" a="<<a<<" b="<<b<<" actual="<<actual<<" expected="<<expected
                 <<" traps="<<actual_trap<<","<<expected_trap<<"\n";
        std::exit(1);
    }
    ++count;
}
int main(int argc,char **argv) {
    Verilated::commandArgs(argc,argv);
    corrupt_value=argc==2 && std::string(argv[1])=="--negative-value";
    corrupt_trap=argc==2 && std::string(argv[1])=="--negative-trap";
    Vfpu_shared_tb dut;
    dut.reset=1;dut.start=0;tick(dut);dut.reset=0;tick(dut);
    const std::array<uint64_t,32> edge32={0,0x80000000,1,0x80000001,0x007fffff,0x807fffff,
        0x00800000,0x80800000,0x7f7fffff,0xff7fffff,0x7f800000,0xff800000,
        0x7fc00000,0xffc00000,0x7f800001,0xff800001,0x3f800000,0xbf800000,
        0x3f800001,0x3f7fffff,0x40000000,0xc0000000,0x33800000,0x33800001,0x4f000000,0xcf000000,0x4f800000,0x5f000000,0xdf000000,0x5f800000,0x4affffff,0x4b000000};
    const std::array<uint64_t,32> edge64={0,0x8000000000000000ULL,1,0x8000000000000001ULL,
        0x000fffffffffffffULL,0x800fffffffffffffULL,0x0010000000000000ULL,0x8010000000000000ULL,
        0x7fefffffffffffffULL,0xffefffffffffffffULL,0x7ff0000000000000ULL,0xfff0000000000000ULL,
        0x7ff8000000000000ULL,0xfff8000000000000ULL,0x7ff0000000000001ULL,0xfff0000000000001ULL,
        0x3ff0000000000000ULL,0xbff0000000000000ULL,0x3ff0000000000001ULL,0x3fefffffffffffffULL,
        0x4000000000000000ULL,0xc000000000000000ULL,0x3ca0000000000000ULL,0x3ca0000000000001ULL,0x41e0000000000000ULL,0xc1e0000000000000ULL,0x41f0000000000000ULL,0x43e0000000000000ULL,0xc3e0000000000000ULL,0x43f0000000000000ULL,0x432fffffffffffffULL,0x4330000000000000ULL};
    std::vector<unsigned> operations;
    for(unsigned op=0x5b;op<=0x66;op++) operations.push_back(op);
    for(unsigned op=0x8b;op<=0xa6;op++) operations.push_back(op);
    for(unsigned op=0xa8;op<=0xab;op++) operations.push_back(op);
    for(unsigned op=0xae;op<=0xbb;op++) operations.push_back(op);
    for(unsigned op=0xfc0000;op<=0xfc0007;op++) operations.push_back(op);
    for(unsigned operation:operations) {
        bool wide=(operation>=0x61 && operation<=0x66) || (operation>=0x99 && operation<=0xa6) ||
            operation==0xaa || operation==0xab || operation==0xb0 || operation==0xb1 ||
            (operation>=0xb6 && operation<=0xba) || (operation>=0xfc0000 && (operation&2));
        const auto &edges=wide ? edge64 : edge32;
        for(auto a:edges) for(auto b:edges) check(dut,wide,operation,a,b);
        for(unsigned i=0;i<10000;i++) {
            uint64_t a=random_bits(),b=random_bits();
            if(i%3==1) {
                // Nearby finite exponents emphasize alignment, cancellation and rounding.
                unsigned exponent=unsigned(random_bits()%80)+(wide ? 983 : 87);
                unsigned other=exponent+unsigned(random_bits()%31)-15;
                if(wide) {
                    a=(a&0x800fffffffffffffULL)|(uint64_t(exponent)<<52);
                    b=(b&0x800fffffffffffffULL)|(uint64_t(other)<<52);
                } else {
                    a=(a&0x807fffffULL)|(uint64_t(exponent)<<23);
                    b=(b&0x807fffffULL)|(uint64_t(other)<<23);
                }
            } else if(i%3==2) b=edges[random_bits()%edges.size()];
            check(dut,wide,operation,a,b);
        }
    }
    for(unsigned i=0;i<1000;i++) {
        bool wide=(i&1)!=0;
        unsigned op=wide ? ((i&2) ? 0xa3 : 0x9f) : ((i&2) ? 0x95 : 0x91);
        check(dut,wide,op,wide ? 0x4000000000000000ULL : 0x40000000ULL,
              wide ? 0x4008000000000000ULL : 0x40400000ULL);
    }
    for(unsigned op:{0x91,0x95,0x9f,0xa3}) for(unsigned phase:{0,1,2,7,23,40}) {
        bool wide=op>=0x99;
        dut.op=op;dut.a=wide ? 0x4000000000000000ULL : 0x40000000ULL;
        dut.b=wide ? 0x4008000000000000ULL : 0x40400000ULL;
        dut.start=1;tick(dut);dut.start=0;
        for(unsigned i=0;i<phase;i++) tick(dut);
        dut.reset=1;tick(dut);
        if(dut.actual_done || dut.expected_done || dut.actual || dut.expected || dut.actual_trap || dut.expected_trap) {
            std::cerr<<"FPU reset did not clear outputs\n";std::exit(1);
        }
        dut.reset=0;tick(dut);
        if(dut.actual_done || dut.expected_done) {
            std::cerr<<"FPU stale completion after reset\n";std::exit(1);
        }
        check(dut,wide,op,dut.a,dut.b);
    }
    std::cout<<"PASS "<<count<<" complete FPU comparisons including conversions, traps and NaN bit operations\n";
}
