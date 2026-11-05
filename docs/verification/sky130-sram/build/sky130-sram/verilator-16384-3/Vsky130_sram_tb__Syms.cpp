// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vsky130_sram_tb__pch.h"
#include "Vsky130_sram_tb.h"
#include "Vsky130_sram_tb___024root.h"

// FUNCTIONS
Vsky130_sram_tb__Syms::~Vsky130_sram_tb__Syms()
{
}

Vsky130_sram_tb__Syms::Vsky130_sram_tb__Syms(VerilatedContext* contextp, const char* namep, Vsky130_sram_tb* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup module instances
    , TOP{this, namep}
{
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscope_sky130_sram_tb.configure(this, name(), "sky130_sram_tb", "sky130_sram_tb", -9, VerilatedScope::SCOPE_OTHER);
    __Vscope_sky130_sram_tb__request.configure(this, name(), "sky130_sram_tb.request", "request", -9, VerilatedScope::SCOPE_OTHER);
    __Vscope_sky130_sram_tb__unnamedblk7.configure(this, name(), "sky130_sram_tb.unnamedblk7", "unnamedblk7", -9, VerilatedScope::SCOPE_OTHER);
}
