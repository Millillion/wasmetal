#pragma GCC diagnostic ignored "-Wint-in-bool-context"
#pragma GCC diagnostic ignored "-Wbool-operation"
#pragma GCC diagnostic ignored "-Wbitwise-instead-of-logical"
// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vwasmetal_core.h for the primary calling header

#include "Vwasmetal_core__pch.h"
#include "Vwasmetal_core_RAMB36E1__pi5.h"

extern const VlWide<128>/*4095:0*/ Vwasmetal_core__ConstPool__CONST_h6e0f3f36_0;
extern const VlWide<1024>/*32767:0*/ Vwasmetal_core__ConstPool__CONST_hbc03216d_0;

VL_ATTR_COLD void Vwasmetal_core_RAMB36E1__pi5___eval_initial__TOP__wasmetal_core__DOT__labels_memory__02e0__02e0(Vwasmetal_core_RAMB36E1__pi5* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB36E1__pi5___eval_initial__TOP__wasmetal_core__DOT__labels_memory__02e0__02e0\n"); );
    // Init
    IData/*31:0*/ __PVT__memory__DOT__unnamedblk1__DOT__word_index;
    __PVT__memory__DOT__unnamedblk1__DOT__word_index = 0;
    // Body
    __PVT__memory__DOT__unnamedblk1__DOT__word_index = 0U;
    while (VL_GTS_III(32, 0x800U, __PVT__memory__DOT__unnamedblk1__DOT__word_index)) {
        vlSelf->memory__DOT____Vlvbound_h5aa9bc41__0 
            = ((0x100U & ((Vwasmetal_core__ConstPool__CONST_h6e0f3f36_0[
                           (0x7fU & (VL_MULS_III(32, (IData)(2U), __PVT__memory__DOT__unnamedblk1__DOT__word_index) 
                                     >> 5U))] >> (0x1fU 
                                                  & VL_MULS_III(32, (IData)(2U), __PVT__memory__DOT__unnamedblk1__DOT__word_index))) 
                          << 8U)) | (0xffU & (((0U 
                                                == 
                                                (0x1fU 
                                                 & VL_MULS_III(32, (IData)(0x10U), __PVT__memory__DOT__unnamedblk1__DOT__word_index)))
                                                ? 0U
                                                : (
                                                   Vwasmetal_core__ConstPool__CONST_hbc03216d_0[
                                                   (((IData)(7U) 
                                                     + 
                                                     (0x7fffU 
                                                      & VL_MULS_III(32, (IData)(0x10U), __PVT__memory__DOT__unnamedblk1__DOT__word_index))) 
                                                    >> 5U)] 
                                                   << 
                                                   ((IData)(0x20U) 
                                                    - 
                                                    (0x1fU 
                                                     & VL_MULS_III(32, (IData)(0x10U), __PVT__memory__DOT__unnamedblk1__DOT__word_index))))) 
                                              | (Vwasmetal_core__ConstPool__CONST_hbc03216d_0[
                                                 (0x3ffU 
                                                  & (VL_MULS_III(32, (IData)(0x10U), __PVT__memory__DOT__unnamedblk1__DOT__word_index) 
                                                     >> 5U))] 
                                                 >> 
                                                 (0x1fU 
                                                  & VL_MULS_III(32, (IData)(0x10U), __PVT__memory__DOT__unnamedblk1__DOT__word_index))))));
        vlSelf->__PVT__memory__DOT__words[(0x7ffU & __PVT__memory__DOT__unnamedblk1__DOT__word_index)] 
            = ((0x3fe00U & vlSelf->__PVT__memory__DOT__words
                [(0x7ffU & __PVT__memory__DOT__unnamedblk1__DOT__word_index)]) 
               | (IData)(vlSelf->memory__DOT____Vlvbound_h5aa9bc41__0));
        vlSelf->memory__DOT____Vlvbound_h5aa9bc41__0 
            = ((0x100U & ((Vwasmetal_core__ConstPool__CONST_h6e0f3f36_0[
                           (0x7fU & (((IData)(1U) + 
                                      VL_MULS_III(32, (IData)(2U), __PVT__memory__DOT__unnamedblk1__DOT__word_index)) 
                                     >> 5U))] >> (0x1fU 
                                                  & ((IData)(1U) 
                                                     + 
                                                     VL_MULS_III(32, (IData)(2U), __PVT__memory__DOT__unnamedblk1__DOT__word_index)))) 
                          << 8U)) | (0xffU & (((0U 
                                                == 
                                                (0x1fU 
                                                 & VL_MULS_III(32, (IData)(8U), 
                                                               ((IData)(1U) 
                                                                + 
                                                                VL_MULS_III(32, (IData)(2U), __PVT__memory__DOT__unnamedblk1__DOT__word_index)))))
                                                ? 0U
                                                : (
                                                   Vwasmetal_core__ConstPool__CONST_hbc03216d_0[
                                                   (((IData)(7U) 
                                                     + 
                                                     (0x7fffU 
                                                      & VL_MULS_III(32, (IData)(8U), 
                                                                    ((IData)(1U) 
                                                                     + 
                                                                     VL_MULS_III(32, (IData)(2U), __PVT__memory__DOT__unnamedblk1__DOT__word_index))))) 
                                                    >> 5U)] 
                                                   << 
                                                   ((IData)(0x20U) 
                                                    - 
                                                    (0x1fU 
                                                     & VL_MULS_III(32, (IData)(8U), 
                                                                   ((IData)(1U) 
                                                                    + 
                                                                    VL_MULS_III(32, (IData)(2U), __PVT__memory__DOT__unnamedblk1__DOT__word_index))))))) 
                                              | (Vwasmetal_core__ConstPool__CONST_hbc03216d_0[
                                                 (0x3ffU 
                                                  & (VL_MULS_III(32, (IData)(8U), 
                                                                 ((IData)(1U) 
                                                                  + 
                                                                  VL_MULS_III(32, (IData)(2U), __PVT__memory__DOT__unnamedblk1__DOT__word_index))) 
                                                     >> 5U))] 
                                                 >> 
                                                 (0x1fU 
                                                  & VL_MULS_III(32, (IData)(8U), 
                                                                ((IData)(1U) 
                                                                 + 
                                                                 VL_MULS_III(32, (IData)(2U), __PVT__memory__DOT__unnamedblk1__DOT__word_index))))))));
        vlSelf->__PVT__memory__DOT__words[(0x7ffU & __PVT__memory__DOT__unnamedblk1__DOT__word_index)] 
            = ((0x1ffU & vlSelf->__PVT__memory__DOT__words
                [(0x7ffU & __PVT__memory__DOT__unnamedblk1__DOT__word_index)]) 
               | ((IData)(vlSelf->memory__DOT____Vlvbound_h5aa9bc41__0) 
                  << 9U));
        __PVT__memory__DOT__unnamedblk1__DOT__word_index 
            = ((IData)(1U) + __PVT__memory__DOT__unnamedblk1__DOT__word_index);
    }
    vlSelf->__PVT__memory__DOT__q = 0U;
}

VL_ATTR_COLD void Vwasmetal_core_RAMB36E1__pi5___stl_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e0__0(Vwasmetal_core_RAMB36E1__pi5* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB36E1__pi5___stl_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e0__0\n"); );
    // Body
    vlSelf->__PVT__parity = 0U;
    vlSelf->__PVT__parity = ((0xfcU & (IData)(vlSelf->__PVT__parity)) 
                             | ((2U & (vlSelf->__PVT__memory__DOT__q 
                                       >> 0x10U)) | 
                                (1U & (vlSelf->__PVT__memory__DOT__q 
                                       >> 8U))));
    vlSelf->__PVT__data = 0ULL;
    vlSelf->__PVT__data = ((0xffffffffffff0000ULL & vlSelf->__PVT__data) 
                           | (IData)((IData)(((0xff00U 
                                               & (vlSelf->__PVT__memory__DOT__q 
                                                  >> 1U)) 
                                              | (0xffU 
                                                 & vlSelf->__PVT__memory__DOT__q)))));
}

VL_ATTR_COLD void Vwasmetal_core_RAMB36E1__pi5___stl_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e2__0(Vwasmetal_core_RAMB36E1__pi5* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB36E1__pi5___stl_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e2__0\n"); );
    // Body
    vlSelf->__PVT__data = 0ULL;
    vlSelf->__PVT__data = ((0xffffffffffff0000ULL & vlSelf->__PVT__data) 
                           | (IData)((IData)(((0xff00U 
                                               & (vlSelf->__PVT__memory__DOT__q 
                                                  >> 1U)) 
                                              | (0xffU 
                                                 & vlSelf->__PVT__memory__DOT__q)))));
    vlSelf->__PVT__parity = 0U;
    vlSelf->__PVT__parity = ((0xfcU & (IData)(vlSelf->__PVT__parity)) 
                             | ((2U & (vlSelf->__PVT__memory__DOT__q 
                                       >> 0x10U)) | 
                                (1U & (vlSelf->__PVT__memory__DOT__q 
                                       >> 8U))));
}

VL_ATTR_COLD void Vwasmetal_core_RAMB36E1__pi5___ctor_var_reset(Vwasmetal_core_RAMB36E1__pi5* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB36E1__pi5___ctor_var_reset\n"); );
    // Body
    vlSelf->__PVT__DOADO = VL_RAND_RESET_I(32);
    vlSelf->DOBDO = VL_RAND_RESET_I(32);
    vlSelf->__PVT__DOPADOP = VL_RAND_RESET_I(4);
    vlSelf->DOPBDOP = VL_RAND_RESET_I(4);
    vlSelf->ADDRARDADDR = VL_RAND_RESET_I(16);
    vlSelf->ADDRBWRADDR = VL_RAND_RESET_I(16);
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
    vlSelf->DIADI = VL_RAND_RESET_I(32);
    vlSelf->DIBDI = VL_RAND_RESET_I(32);
    vlSelf->DIPADIP = VL_RAND_RESET_I(4);
    vlSelf->DIPBDIP = VL_RAND_RESET_I(4);
    vlSelf->WEA = VL_RAND_RESET_I(4);
    vlSelf->WEBWE = VL_RAND_RESET_I(8);
    vlSelf->__PVT__CASCADEINA = VL_RAND_RESET_I(1);
    vlSelf->__PVT__CASCADEINB = VL_RAND_RESET_I(1);
    vlSelf->__PVT__INJECTDBITERR = VL_RAND_RESET_I(1);
    vlSelf->__PVT__INJECTSBITERR = VL_RAND_RESET_I(1);
    vlSelf->__PVT__CASCADEOUTA = VL_RAND_RESET_I(1);
    vlSelf->__PVT__CASCADEOUTB = VL_RAND_RESET_I(1);
    vlSelf->__PVT__DBITERR = VL_RAND_RESET_I(1);
    vlSelf->__PVT__SBITERR = VL_RAND_RESET_I(1);
    vlSelf->__PVT__ECCPARITY = VL_RAND_RESET_I(8);
    vlSelf->__PVT__RDADDRECC = VL_RAND_RESET_I(9);
    vlSelf->__PVT__data = VL_RAND_RESET_Q(64);
    vlSelf->__PVT__parity = VL_RAND_RESET_I(8);
    for (int __Vi0 = 0; __Vi0 < 2048; ++__Vi0) {
        vlSelf->__PVT__memory__DOT__words[__Vi0] = VL_RAND_RESET_I(18);
    }
    vlSelf->__PVT__memory__DOT__q = VL_RAND_RESET_I(18);
    vlSelf->memory__DOT____Vlvbound_h5aa9bc41__0 = VL_RAND_RESET_I(9);
    vlSelf->memory__DOT____Vlvbound_h252618a2__0 = VL_RAND_RESET_I(9);
}
