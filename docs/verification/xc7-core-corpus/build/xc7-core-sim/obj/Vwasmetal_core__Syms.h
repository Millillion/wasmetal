// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VWASMETAL_CORE__SYMS_H_
#define VERILATED_VWASMETAL_CORE__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vwasmetal_core.h"

// INCLUDE MODULE CLASSES
#include "Vwasmetal_core___024root.h"
#include "Vwasmetal_core_DSP48E1__pi1.h"
#include "Vwasmetal_core_DSP48E1__pi2.h"
#include "Vwasmetal_core_RAMB36E1__pi4.h"
#include "Vwasmetal_core_RAMB36E1__pi5.h"
#include "Vwasmetal_core_RAMB18E1__pi6.h"

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES)Vwasmetal_core__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vwasmetal_core* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vwasmetal_core___024root       TOP;
    Vwasmetal_core_DSP48E1__pi1    TOP__wasmetal_core__DOT___134220_;
    Vwasmetal_core_DSP48E1__pi2    TOP__wasmetal_core__DOT___134221_;
    Vwasmetal_core_DSP48E1__pi1    TOP__wasmetal_core__DOT___134222_;
    Vwasmetal_core_DSP48E1__pi2    TOP__wasmetal_core__DOT___134223_;
    Vwasmetal_core_DSP48E1__pi2    TOP__wasmetal_core__DOT___134224_;
    Vwasmetal_core_DSP48E1__pi1    TOP__wasmetal_core__DOT___134225_;
    Vwasmetal_core_DSP48E1__pi2    TOP__wasmetal_core__DOT___134226_;
    Vwasmetal_core_DSP48E1__pi2    TOP__wasmetal_core__DOT___134227_;
    Vwasmetal_core_DSP48E1__pi1    TOP__wasmetal_core__DOT___134228_;
    Vwasmetal_core_DSP48E1__pi2    TOP__wasmetal_core__DOT___134229_;
    Vwasmetal_core_DSP48E1__pi1    TOP__wasmetal_core__DOT___134230_;
    Vwasmetal_core_DSP48E1__pi2    TOP__wasmetal_core__DOT___134231_;
    Vwasmetal_core_DSP48E1__pi1    TOP__wasmetal_core__DOT___134232_;
    Vwasmetal_core_DSP48E1__pi2    TOP__wasmetal_core__DOT___135064_;
    Vwasmetal_core_DSP48E1__pi1    TOP__wasmetal_core__DOT___135065_;
    Vwasmetal_core_DSP48E1__pi2    TOP__wasmetal_core__DOT___135066_;
    Vwasmetal_core_DSP48E1__pi2    TOP__wasmetal_core__DOT___135067_;
    Vwasmetal_core_DSP48E1__pi2    TOP__wasmetal_core__DOT___135068_;
    Vwasmetal_core_DSP48E1__pi1    TOP__wasmetal_core__DOT___135069_;
    Vwasmetal_core_DSP48E1__pi2    TOP__wasmetal_core__DOT___135070_;
    Vwasmetal_core_DSP48E1__pi2    TOP__wasmetal_core__DOT___135071_;
    Vwasmetal_core_DSP48E1__pi2    TOP__wasmetal_core__DOT___135072_;
    Vwasmetal_core_DSP48E1__pi1    TOP__wasmetal_core__DOT___135073_;
    Vwasmetal_core_DSP48E1__pi2    TOP__wasmetal_core__DOT___135074_;
    Vwasmetal_core_DSP48E1__pi2    TOP__wasmetal_core__DOT___135075_;
    Vwasmetal_core_DSP48E1__pi1    TOP__wasmetal_core__DOT___135195_;
    Vwasmetal_core_DSP48E1__pi1    TOP__wasmetal_core__DOT___135196_;
    Vwasmetal_core_DSP48E1__pi1    TOP__wasmetal_core__DOT___135426_;
    Vwasmetal_core_RAMB36E1__pi4   TOP__wasmetal_core__DOT__data_sizes__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB36E1__pi4   TOP__wasmetal_core__DOT__element_sizes__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB36E1__pi4   TOP__wasmetal_core__DOT__frames_memory__02e0__02e0;
    Vwasmetal_core_RAMB36E1__pi4   TOP__wasmetal_core__DOT__frames_memory__02e0__02e1;
    Vwasmetal_core_RAMB36E1__pi5   TOP__wasmetal_core__DOT__labels_memory__02e0__02e0;
    Vwasmetal_core_RAMB36E1__pi5   TOP__wasmetal_core__DOT__labels_memory__02e0__02e1;
    Vwasmetal_core_RAMB36E1__pi5   TOP__wasmetal_core__DOT__labels_memory__02e0__02e2;
    Vwasmetal_core_RAMB36E1__pi5   TOP__wasmetal_core__DOT__labels_memory__02e0__02e3;
    Vwasmetal_core_RAMB36E1__pi5   TOP__wasmetal_core__DOT__labels_memory__02e0__02e4;
    Vwasmetal_core_RAMB36E1__pi5   TOP__wasmetal_core__DOT__labels_memory__02e0__02e5;
    Vwasmetal_core_RAMB36E1__pi5   TOP__wasmetal_core__DOT__labels_memory__02e0__02e6;
    Vwasmetal_core_RAMB36E1__pi5   TOP__wasmetal_core__DOT__labels_memory__02e0__02e7;
    Vwasmetal_core_RAMB36E1__pi5   TOP__wasmetal_core__DOT__labels_memory__02e0__02e8;
    Vwasmetal_core_RAMB36E1__pi4   TOP__wasmetal_core__DOT__memory_bounds__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB36E1__pi4   TOP__wasmetal_core__DOT__memory_sizes__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB36E1__pi4   TOP__wasmetal_core__DOT__memory_sizes__02ewords__02e1__02e0;
    Vwasmetal_core_RAMB36E1__pi4   TOP__wasmetal_core__DOT__table_bounds__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB36E1__pi4   TOP__wasmetal_core__DOT__table_sizes__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB36E1__pi4   TOP__wasmetal_core__DOT__table_sizes__02ewords__02e1__02e0;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e1;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e10;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e11;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e12;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e13;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e14;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e2;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e3;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e4;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e5;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e6;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e7;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e8;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e9;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e1;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e10;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e11;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e12;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e13;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e14;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e2;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e3;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e4;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e5;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e6;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e7;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e8;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e9;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e1;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e10;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e11;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e12;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e13;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e14;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e2;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e3;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e4;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e5;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e6;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e7;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e8;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e9;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e1;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e10;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e11;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e12;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e13;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e14;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e2;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e3;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e4;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e5;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e6;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e7;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e8;
    Vwasmetal_core_RAMB18E1__pi6   TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e9;

    // SCOPE NAMES
    VerilatedScope __Vscope_wasmetal_core__data_sizes__02ewords__02e0__02e0__memory;
    VerilatedScope __Vscope_wasmetal_core__element_sizes__02ewords__02e0__02e0__memory;
    VerilatedScope __Vscope_wasmetal_core__frames_memory__02e0__02e0__memory;
    VerilatedScope __Vscope_wasmetal_core__frames_memory__02e0__02e1__memory;
    VerilatedScope __Vscope_wasmetal_core__memory_bounds__02ewords__02e0__02e0__memory;
    VerilatedScope __Vscope_wasmetal_core__memory_sizes__02ewords__02e0__02e0__memory;
    VerilatedScope __Vscope_wasmetal_core__memory_sizes__02ewords__02e1__02e0__memory;
    VerilatedScope __Vscope_wasmetal_core__table_bounds__02ewords__02e0__02e0__memory;
    VerilatedScope __Vscope_wasmetal_core__table_sizes__02ewords__02e0__02e0__memory;
    VerilatedScope __Vscope_wasmetal_core__table_sizes__02ewords__02e1__02e0__memory;

    // CONSTRUCTORS
    Vwasmetal_core__Syms(VerilatedContext* contextp, const char* namep, Vwasmetal_core* modelp);
    ~Vwasmetal_core__Syms();

    // METHODS
    const char* name() { return TOP.name(); }
};

#endif  // guard
