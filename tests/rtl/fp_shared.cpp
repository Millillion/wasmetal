// SPDX-License-Identifier: MIT
#include "Vfp_shared_tb.h"
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>

static uint64_t state=0x5741534d4554414cULL;
static uint64_t random_bits() {
    state^=state>>12; state^=state<<25; state^=state>>27;
    return state*0x2545f4914f6cdd1dULL;
}
static void tick(Vfp_shared_tb &dut) {
    dut.clk=1; dut.eval(); dut.clk=0; dut.eval();
}
static uint64_t count=0;
static void check(Vfp_shared_tb &dut, bool wide, unsigned operation, uint64_t a,uint64_t b) {
    dut.wide=wide;dut.operation=operation;dut.a=a;dut.b=b;dut.start=0;dut.eval();
    uint64_t actual=dut.actual,expected=dut.expected;
    if(operation==6 || operation==10) {
        dut.start=1;tick(dut);dut.start=0;dut.eval();
        bool have_actual=false,have_expected=false;
        for(unsigned cycle=0;cycle<130;cycle++) {
            if(dut.actual_done) {actual=dut.actual;have_actual=true;}
            if(dut.expected_done) {expected=dut.expected;have_expected=true;}
            if(have_actual && have_expected) break;
            tick(dut);
        }
        if(!have_actual || !have_expected) {
            std::cerr<<"Floating-point unit timeout\n";std::exit(1);
        }
        tick(dut);
    }
    if(actual!=expected) {
        std::cerr<<"FP mismatch wide="<<wide<<" op="<<operation<<std::hex
                 <<" a="<<a<<" b="<<b<<" actual="<<actual<<" expected="<<expected<<"\n";
        std::exit(1);
    }
    ++count;
}
int main(int argc,char **argv) {
    Verilated::commandArgs(argc,argv);
    Vfp_shared_tb dut;
    dut.reset=1;dut.start=0;tick(dut);dut.reset=0;tick(dut);
    const std::array<uint64_t,24> edge32={0,0x80000000,1,0x80000001,0x007fffff,0x807fffff,
        0x00800000,0x80800000,0x7f7fffff,0xff7fffff,0x7f800000,0xff800000,
        0x7fc00000,0xffc00000,0x7f800001,0xff800001,0x3f800000,0xbf800000,
        0x3f800001,0x3f7fffff,0x40000000,0xc0000000,0x33800000,0x33800001};
    const std::array<uint64_t,24> edge64={0,0x8000000000000000ULL,1,0x8000000000000001ULL,
        0x000fffffffffffffULL,0x800fffffffffffffULL,0x0010000000000000ULL,0x8010000000000000ULL,
        0x7fefffffffffffffULL,0xffefffffffffffffULL,0x7ff0000000000000ULL,0xfff0000000000000ULL,
        0x7ff8000000000000ULL,0xfff8000000000000ULL,0x7ff0000000000001ULL,0xfff0000000000001ULL,
        0x3ff0000000000000ULL,0xbff0000000000000ULL,0x3ff0000000000001ULL,0x3fefffffffffffffULL,
        0x4000000000000000ULL,0xc000000000000000ULL,0x3ca0000000000000ULL,0x3ca0000000000001ULL};
    for(bool wide:{false,true}) for(unsigned operation:{6,7,8,9,10}) {
        const auto &edges=wide ? edge64 : edge32;
        for(auto a:edges) for(auto b:edges) check(dut,wide,operation,a,b);
        for(unsigned i=0;i<100000;i++) {
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
    std::cout<<"PASS "<<count<<" shared floating-point comparisons against separate precision units\n";
}
