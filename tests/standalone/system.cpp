// SPDX-License-Identifier: MIT
// Clock/reset and a UART receiver only. No CPU ports or backing memory access.
#include "verilated.h"
#ifdef WASMETAL_BOARD
#include "Vwasmetal_standalone_ulx3s.h"
using Model=Vwasmetal_standalone_ulx3s;
static constexpr unsigned bit_ticks=81*32;
#else
#include "Vwasmetal_standalone.h"
using Model=Vwasmetal_standalone;
static constexpr unsigned bit_ticks=4;
#endif
#include <cstdint>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

class Receiver {
    unsigned state=0,remaining=0,bit=0,value=0;
public:
    std::vector<uint8_t> bytes;
    void sample(bool high) {
        if(state==0) {
            if(!high) { state=1; remaining=bit_ticks+bit_ticks/2-1; bit=0; value=0; }
        } else if(remaining) --remaining;
        else if(state==1) {
            if(high) value|=1U<<bit;
            remaining=bit_ticks-1;
            if(++bit==8) state=2;
        } else {
            if(!high) throw std::runtime_error("UART framing error");
            bytes.push_back(static_cast<uint8_t>(value)); state=0;
        }
    }
};

static void set_reset(Model& m,bool reset) {
#ifdef WASMETAL_BOARD
    m.btn_n=!reset;
#else
    m.reset=reset;
#endif
}
static void tick(Model& m) {
#ifdef WASMETAL_BOARD
    m.clk_25mhz=0; m.eval(); m.clk_25mhz=1; m.eval(); m.clk_25mhz=0; m.eval();
#else
    m.clk=0; m.eval(); m.clk=1; m.eval(); m.clk=0; m.eval();
#endif
}
static bool finished(Model& m) {
#ifdef WASMETAL_BOARD
    return !m.led_busy;
#else
    return m.finished;
#endif
}
static bool serial(Model& m) {
#ifdef WASMETAL_BOARD
    return m.ftdi_rxd;
#else
    return m.tx;
#endif
}

int main(int argc,char** argv) {
    Verilated::commandArgs(argc,argv);
    try {
        uint64_t limit=20000000,reset_at=0;
        unsigned reboots=1;
        bool power_on=false,reset_requested=false;
        for(int n=1;n<argc;n++) {
            const std::string arg=argv[n];
            if(arg=="--power-on") power_on=true;
            else if(n+1<argc && arg=="--limit") limit=std::stoull(argv[++n]);
            else if(n+1<argc && arg=="--reset-at") { reset_at=std::stoull(argv[++n]); reset_requested=true; }
            else if(n+1<argc && arg=="--reboots") reboots=static_cast<unsigned>(std::stoul(argv[++n]));
            else throw std::runtime_error("unknown driver argument");
        }
        auto m=std::make_unique<Model>();
        for(unsigned attempt=0;attempt<reboots;attempt++) {
            if(!power_on || attempt) {
                set_reset(*m,true); for(unsigned n=0;n<128;n++) tick(*m);
            }
            set_reset(*m,false);
            Receiver receiver;
            uint64_t clocks=0,first_uart_clock=0;
            bool reset_injected=false;
            for(;clocks<limit;clocks++) {
                if(reset_requested && !reset_injected && clocks==reset_at) {
                    set_reset(*m,true); for(unsigned n=0;n<128;n++) tick(*m);
                    clocks+=128; reset_injected=true; first_uart_clock=0;
                    receiver=Receiver{}; set_reset(*m,false);
                }
                tick(*m); receiver.sample(serial(*m));
                if(!serial(*m) && !first_uart_clock) first_uart_clock=clocks+1;
                if(finished(*m)) break;
            }
            if(clocks>=limit) throw std::runtime_error("standalone system did not finish");
            if(reset_requested && !reset_injected) throw std::runtime_error("scheduled reset never occurred");
            std::cout<<"{\"clocks\":"<<clocks+1<<",\"first_uart_clock\":"<<first_uart_clock
                     <<",\"reset_injected\":"<<(reset_injected ? "true" : "false")
                     <<",\"reset_at\":"<<(reset_injected ? reset_at : 0)<<",\"uart\":\"";
            const char* hex="0123456789abcdef";
            for(uint8_t b:receiver.bytes) std::cout<<hex[b>>4]<<hex[b&15];
            std::cout<<"\"}\n";
        }
        m->final();
    } catch(const std::exception& e) {
        std::cerr<<e.what()<<'\n'; return 1;
    }
    return 0;
}
