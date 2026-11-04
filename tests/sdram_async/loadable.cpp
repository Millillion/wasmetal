// SPDX-License-Identifier: MIT
// Keep the existing UART driver and result oracle. Only its model's eval()
// schedules the separate memory clock, including genuinely coincident edges.
#include "Vwasmetal_loadable.h"
#include "clock_parameters.hpp"
#include <cstdint>
#include <fstream>
#include <stdexcept>

class AsyncSdramSystemModel final : public Vwasmetal_loadable {
    uint64_t now_=0,next_memory_=MEMORY_PHASE,cpu_rises_=0,memory_rises_=0,coincident_=0;
    bool previous_cpu_=false;
    void advance(uint64_t target) {
        if(target<now_) throw std::runtime_error("simulation clock moved backwards");
        contextp()->timeInc(target-now_);now_=target;
    }
    void memory_edge() {
        memory_clk=!memory_clk;
        if(memory_clk) memory_rises_++;
        next_memory_+=MEMORY_HALF_PERIOD;
    }
public:
    AsyncSdramSystemModel() { clk=0;memory_clk=0; }
    void eval() {
        const bool requested=clk;
        if(requested==previous_cpu_) { Vwasmetal_loadable::eval();return; }
        const uint64_t end=now_+CPU_HALF_PERIOD;
        clk=previous_cpu_;
        while(next_memory_<end) {
            advance(next_memory_);memory_edge();Vwasmetal_loadable::eval();
        }
        advance(end);clk=requested;
        if(next_memory_==end) { memory_edge();coincident_++; }
        if(requested) cpu_rises_++;
        previous_cpu_=requested;Vwasmetal_loadable::eval();
    }
    ~AsyncSdramSystemModel() override {
        final();
        std::ofstream out(CLOCK_COVERAGE,std::ios::app);
        out<<"{\"cpu_rising_edges\":"<<cpu_rises_<<",\"memory_rising_edges\":"<<memory_rises_
           <<",\"coincident_edges\":"<<coincident_<<",\"elapsed_ticks\":"<<now_<<"}\n";
    }
};
#define Vwasmetal_loadable AsyncSdramSystemModel
#include "../standalone/loadable.cpp"
#undef Vwasmetal_loadable
