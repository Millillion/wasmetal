#pragma GCC diagnostic ignored "-Wint-in-bool-context"
#pragma GCC diagnostic ignored "-Wbool-operation"
#pragma GCC diagnostic ignored "-Wbitwise-instead-of-logical"
// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vwasmetal_core.h for the primary calling header

#include "Vwasmetal_core__pch.h"
#include "Vwasmetal_core__Syms.h"
#include "Vwasmetal_core___024root.h"

void Vwasmetal_core___024root___ctor_var_reset(Vwasmetal_core___024root* vlSelf);

Vwasmetal_core___024root::Vwasmetal_core___024root(Vwasmetal_core__Syms* symsp, const char* v__name)
    : VerilatedModule{v__name}
    , vlSymsp{symsp}
 {
    // Reset structure values
    Vwasmetal_core___024root___ctor_var_reset(this);
}

void Vwasmetal_core___024root::__Vconfigure(bool first) {
    if (false && first) {}  // Prevent unused
}

Vwasmetal_core___024root::~Vwasmetal_core___024root() {
}
