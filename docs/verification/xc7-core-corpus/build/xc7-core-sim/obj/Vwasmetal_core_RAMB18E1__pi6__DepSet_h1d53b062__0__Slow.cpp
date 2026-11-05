#pragma GCC diagnostic ignored "-Wint-in-bool-context"
#pragma GCC diagnostic ignored "-Wbool-operation"
#pragma GCC diagnostic ignored "-Wbitwise-instead-of-logical"
// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vwasmetal_core.h for the primary calling header

#include "Vwasmetal_core__pch.h"
#include "Vwasmetal_core_RAMB18E1__pi6.h"

extern const VlWide<64>/*2047:0*/ Vwasmetal_core__ConstPool__CONST_h6be9aa18_0;
extern const VlWide<512>/*16383:0*/ Vwasmetal_core__ConstPool__CONST_h60a81158_0;

VL_ATTR_COLD void Vwasmetal_core_RAMB18E1__pi6___eval_initial__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___eval_initial__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0\n"); );
    // Init
    IData/*31:0*/ __PVT__memory__DOT__unnamedblk1__DOT__word_index;
    __PVT__memory__DOT__unnamedblk1__DOT__word_index = 0;
    // Body
    __PVT__memory__DOT__unnamedblk1__DOT__word_index = 0U;
    while (VL_GTS_III(32, 0x800U, __PVT__memory__DOT__unnamedblk1__DOT__word_index)) {
        vlSelf->memory__DOT____Vlvbound_h79136b5e__0 
            = ((0x100U & ((Vwasmetal_core__ConstPool__CONST_h6be9aa18_0[
                           (0x3fU & (__PVT__memory__DOT__unnamedblk1__DOT__word_index 
                                     >> 5U))] >> (0x1fU 
                                                  & __PVT__memory__DOT__unnamedblk1__DOT__word_index)) 
                          << 8U)) | (0xffU & (((0U 
                                                == 
                                                (0x1fU 
                                                 & VL_MULS_III(32, (IData)(8U), __PVT__memory__DOT__unnamedblk1__DOT__word_index)))
                                                ? 0U
                                                : (
                                                   Vwasmetal_core__ConstPool__CONST_h60a81158_0[
                                                   (((IData)(7U) 
                                                     + 
                                                     (0x3fffU 
                                                      & VL_MULS_III(32, (IData)(8U), __PVT__memory__DOT__unnamedblk1__DOT__word_index))) 
                                                    >> 5U)] 
                                                   << 
                                                   ((IData)(0x20U) 
                                                    - 
                                                    (0x1fU 
                                                     & VL_MULS_III(32, (IData)(8U), __PVT__memory__DOT__unnamedblk1__DOT__word_index))))) 
                                              | (Vwasmetal_core__ConstPool__CONST_h60a81158_0[
                                                 (0x1ffU 
                                                  & (VL_MULS_III(32, (IData)(8U), __PVT__memory__DOT__unnamedblk1__DOT__word_index) 
                                                     >> 5U))] 
                                                 >> 
                                                 (0x1fU 
                                                  & VL_MULS_III(32, (IData)(8U), __PVT__memory__DOT__unnamedblk1__DOT__word_index))))));
        vlSelf->__PVT__memory__DOT__words[(0x7ffU & __PVT__memory__DOT__unnamedblk1__DOT__word_index)] 
            = vlSelf->memory__DOT____Vlvbound_h79136b5e__0;
        __PVT__memory__DOT__unnamedblk1__DOT__word_index 
            = ((IData)(1U) + __PVT__memory__DOT__unnamedblk1__DOT__word_index);
    }
    vlSelf->__PVT__memory__DOT__q = 0U;
}

VL_ATTR_COLD void Vwasmetal_core_RAMB18E1__pi6___stl_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___stl_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__0\n"); );
    // Body
    vlSelf->__PVT__parity = 0U;
    vlSelf->__PVT__parity = ((0xfeU & (IData)(vlSelf->__PVT__parity)) 
                             | (1U & ((IData)(vlSelf->__PVT__memory__DOT__q) 
                                      >> 8U)));
    vlSelf->__PVT__data = 0ULL;
    vlSelf->__PVT__data = ((0xffffffffffffff00ULL & vlSelf->__PVT__data) 
                           | (IData)((IData)((0xffU 
                                              & (IData)(vlSelf->__PVT__memory__DOT__q)))));
}

VL_ATTR_COLD void Vwasmetal_core_RAMB18E1__pi6___stl_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e14__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___stl_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e14__0\n"); );
    // Body
    vlSelf->__PVT__data = 0ULL;
    vlSelf->__PVT__data = ((0xffffffffffffff00ULL & vlSelf->__PVT__data) 
                           | (IData)((IData)((0xffU 
                                              & (IData)(vlSelf->__PVT__memory__DOT__q)))));
}

VL_ATTR_COLD void Vwasmetal_core_RAMB18E1__pi6___ctor_var_reset(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___ctor_var_reset\n"); );
    // Body
    vlSelf->__PVT__DOADO = VL_RAND_RESET_I(16);
    vlSelf->DOBDO = VL_RAND_RESET_I(16);
    vlSelf->__PVT__DOPADOP = VL_RAND_RESET_I(2);
    vlSelf->DOPBDOP = VL_RAND_RESET_I(2);
    vlSelf->ADDRARDADDR = VL_RAND_RESET_I(14);
    vlSelf->ADDRBWRADDR = VL_RAND_RESET_I(14);
    vlSelf->CLKARDCLK = VL_RAND_RESET_I(1);
    vlSelf->CLKBWRCLK = VL_RAND_RESET_I(1);
    vlSelf->ENARDEN = VL_RAND_RESET_I(1);
    vlSelf->ENBWREN = VL_RAND_RESET_I(1);
    vlSelf->REGCEAREGCE = VL_RAND_RESET_I(1);
    vlSelf->REGCEB = VL_RAND_RESET_I(1);
    vlSelf->RSTRAMARSTRAM = VL_RAND_RESET_I(1);
    vlSelf->RSTRAMB = VL_RAND_RESET_I(1);
    vlSelf->RSTREGARSTREG = VL_RAND_RESET_I(1);
    vlSelf->RSTREGB = VL_RAND_RESET_I(1);
    vlSelf->DIADI = VL_RAND_RESET_I(16);
    vlSelf->DIBDI = VL_RAND_RESET_I(16);
    vlSelf->DIPADIP = VL_RAND_RESET_I(2);
    vlSelf->DIPBDIP = VL_RAND_RESET_I(2);
    vlSelf->WEA = VL_RAND_RESET_I(2);
    vlSelf->WEBWE = VL_RAND_RESET_I(4);
    vlSelf->__PVT__data = VL_RAND_RESET_Q(64);
    vlSelf->__PVT__parity = VL_RAND_RESET_I(8);
    for (int __Vi0 = 0; __Vi0 < 2048; ++__Vi0) {
        vlSelf->__PVT__memory__DOT__words[__Vi0] = VL_RAND_RESET_I(9);
    }
    vlSelf->__PVT__memory__DOT__q = VL_RAND_RESET_I(9);
    vlSelf->memory__DOT____Vlvbound_h79136b5e__0 = VL_RAND_RESET_I(9);
    vlSelf->memory__DOT____Vlvbound_h26c55382__0 = VL_RAND_RESET_I(9);
}
