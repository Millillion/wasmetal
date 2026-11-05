#pragma GCC diagnostic ignored "-Wint-in-bool-context"
#pragma GCC diagnostic ignored "-Wbool-operation"
#pragma GCC diagnostic ignored "-Wbitwise-instead-of-logical"
// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vwasmetal_core.h for the primary calling header

#include "Vwasmetal_core__pch.h"
#include "Vwasmetal_core_RAMB18E1__pi6.h"
#include "Vwasmetal_core__Syms.h"

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021739_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b8__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__1(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__1\n"); );
    // Body
    vlSelf->__PVT__memory__DOT__q = vlSelf->__PVT__memory__DOT__words
        [(0x7ffU & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRBWRADDR) 
                    >> 3U))];
    vlSelf->__PVT__parity = 0U;
    vlSelf->__PVT__parity = ((0xfeU & (IData)(vlSelf->__PVT__parity)) 
                             | (1U & ((IData)(vlSelf->__PVT__memory__DOT__q) 
                                      >> 8U)));
    vlSelf->__PVT__data = 0ULL;
    vlSelf->__PVT__data = ((0xffffffffffffff00ULL & vlSelf->__PVT__data) 
                           | (IData)((IData)((0xffU 
                                              & (IData)(vlSelf->__PVT__memory__DOT__q)))));
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e1__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e1__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021739_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b17__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e1__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e10__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e10__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021739_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b98__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e10__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e11__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e11__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021739_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b107__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e11__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e12__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e12__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021739_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b116__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e12__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e13__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e13__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021739_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b125__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e13__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e14__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e14__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021739_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e14__DIADI))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e14__1(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e14__1\n"); );
    // Body
    vlSelf->__PVT__memory__DOT__q = vlSelf->__PVT__memory__DOT__words
        [(0x7ffU & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRBWRADDR) 
                    >> 3U))];
    vlSelf->__PVT__data = 0ULL;
    vlSelf->__PVT__data = ((0xffffffffffffff00ULL & vlSelf->__PVT__data) 
                           | (IData)((IData)((0xffU 
                                              & (IData)(vlSelf->__PVT__memory__DOT__q)))));
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e2__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e2__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021739_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b26__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e2__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e3__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e3__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021739_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b35__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e3__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e4__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e4__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021739_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b44__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e4__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e5__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e5__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021739_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b53__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e5__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e6__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e6__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021739_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b62__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e6__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e7__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e7__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021739_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b71__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e7__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e8__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e8__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021739_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b80__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e8__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e9__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e9__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021739_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b89__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e9__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e0__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e0__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021740_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b8__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e0__1(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e0__1\n"); );
    // Body
    vlSelf->__PVT__memory__DOT__q = vlSelf->__PVT__memory__DOT__words
        [(0x7ffU & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b1__05d__02ewords__02e0__02e0__ADDRBWRADDR) 
                    >> 3U))];
    vlSelf->__PVT__parity = 0U;
    vlSelf->__PVT__parity = ((0xfeU & (IData)(vlSelf->__PVT__parity)) 
                             | (1U & ((IData)(vlSelf->__PVT__memory__DOT__q) 
                                      >> 8U)));
    vlSelf->__PVT__data = 0ULL;
    vlSelf->__PVT__data = ((0xffffffffffffff00ULL & vlSelf->__PVT__data) 
                           | (IData)((IData)((0xffU 
                                              & (IData)(vlSelf->__PVT__memory__DOT__q)))));
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e1__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e1__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021740_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b17__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e1__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e10__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e10__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021740_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b98__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e10__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e11__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e11__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021740_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b107__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e11__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e12__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e12__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021740_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b116__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e12__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e13__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e13__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021740_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b125__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e13__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e14__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e14__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021740_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e14__DIADI))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e14__1(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e14__1\n"); );
    // Body
    vlSelf->__PVT__memory__DOT__q = vlSelf->__PVT__memory__DOT__words
        [(0x7ffU & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b1__05d__02ewords__02e0__02e0__ADDRBWRADDR) 
                    >> 3U))];
    vlSelf->__PVT__data = 0ULL;
    vlSelf->__PVT__data = ((0xffffffffffffff00ULL & vlSelf->__PVT__data) 
                           | (IData)((IData)((0xffU 
                                              & (IData)(vlSelf->__PVT__memory__DOT__q)))));
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e2__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e2__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021740_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b26__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e2__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e3__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e3__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021740_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b35__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e3__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e4__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e4__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021740_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b44__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e4__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e5__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e5__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021740_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b53__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e5__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e6__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e6__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021740_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b62__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e6__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e7__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e7__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021740_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b71__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e7__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e8__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e8__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021740_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b80__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e8__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e9__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e9__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021740_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b89__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e9__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e0__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e0__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000209_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b8__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e0__1(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e0__1\n"); );
    // Body
    vlSelf->__PVT__memory__DOT__q = vlSelf->__PVT__memory__DOT__words
        [(0x7ffU & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b2__05d__02ewords__02e0__02e0__ADDRBWRADDR) 
                    >> 3U))];
    vlSelf->__PVT__parity = 0U;
    vlSelf->__PVT__parity = ((0xfeU & (IData)(vlSelf->__PVT__parity)) 
                             | (1U & ((IData)(vlSelf->__PVT__memory__DOT__q) 
                                      >> 8U)));
    vlSelf->__PVT__data = 0ULL;
    vlSelf->__PVT__data = ((0xffffffffffffff00ULL & vlSelf->__PVT__data) 
                           | (IData)((IData)((0xffU 
                                              & (IData)(vlSelf->__PVT__memory__DOT__q)))));
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e1__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e1__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000209_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b17__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e1__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e10__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e10__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000209_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b98__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e10__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e11__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e11__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000209_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b107__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e11__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e12__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e12__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000209_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b116__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e12__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e13__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e13__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000209_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b125__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e13__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e14__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e14__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000209_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e14__DIADI))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e14__1(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e14__1\n"); );
    // Body
    vlSelf->__PVT__memory__DOT__q = vlSelf->__PVT__memory__DOT__words
        [(0x7ffU & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b2__05d__02ewords__02e0__02e0__ADDRBWRADDR) 
                    >> 3U))];
    vlSelf->__PVT__data = 0ULL;
    vlSelf->__PVT__data = ((0xffffffffffffff00ULL & vlSelf->__PVT__data) 
                           | (IData)((IData)((0xffU 
                                              & (IData)(vlSelf->__PVT__memory__DOT__q)))));
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e2__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e2__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000209_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b26__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e2__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e3__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e3__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000209_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b35__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e3__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e4__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e4__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000209_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b44__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e4__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e5__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e5__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000209_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b53__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e5__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e6__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e6__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000209_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b62__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e6__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e7__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e7__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000209_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b71__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e7__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e8__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e8__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000209_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b80__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e8__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e9__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e9__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000209_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b89__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e9__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e0__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e0__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021741_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b8__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e0__1(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e0__1\n"); );
    // Body
    vlSelf->__PVT__memory__DOT__q = vlSelf->__PVT__memory__DOT__words
        [(0x7ffU & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b3__05d__02ewords__02e0__02e0__ADDRBWRADDR) 
                    >> 3U))];
    vlSelf->__PVT__parity = 0U;
    vlSelf->__PVT__parity = ((0xfeU & (IData)(vlSelf->__PVT__parity)) 
                             | (1U & ((IData)(vlSelf->__PVT__memory__DOT__q) 
                                      >> 8U)));
    vlSelf->__PVT__data = 0ULL;
    vlSelf->__PVT__data = ((0xffffffffffffff00ULL & vlSelf->__PVT__data) 
                           | (IData)((IData)((0xffU 
                                              & (IData)(vlSelf->__PVT__memory__DOT__q)))));
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e1__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e1__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021741_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b17__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e1__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e10__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e10__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021741_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b98__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e10__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e11__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e11__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021741_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b107__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e11__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e12__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e12__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021741_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b116__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e12__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e13__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e13__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021741_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b125__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e13__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e14__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e14__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021741_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e14__DIADI))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e14__1(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e14__1\n"); );
    // Body
    vlSelf->__PVT__memory__DOT__q = vlSelf->__PVT__memory__DOT__words
        [(0x7ffU & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b3__05d__02ewords__02e0__02e0__ADDRBWRADDR) 
                    >> 3U))];
    vlSelf->__PVT__data = 0ULL;
    vlSelf->__PVT__data = ((0xffffffffffffff00ULL & vlSelf->__PVT__data) 
                           | (IData)((IData)((0xffU 
                                              & (IData)(vlSelf->__PVT__memory__DOT__q)))));
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e2__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e2__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021741_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b26__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e2__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e3__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e3__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021741_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b35__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e3__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e4__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e4__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021741_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b44__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e4__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e5__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e5__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021741_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b53__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e5__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e6__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e6__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021741_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b62__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e6__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e7__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e7__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021741_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b71__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e7__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e8__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e8__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021741_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b80__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e8__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e9__0(Vwasmetal_core_RAMB18E1__pi6* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB18E1__pi6___nba_sequent__TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e9__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___021741_))))) {
        vlSelf->memory__DOT____Vlvbound_h26c55382__0 
            = (((IData)(vlSymsp->TOP.wasmetal_core__DOT__value_file__02ewrite_data__05b89__05d) 
                << 8U) | (0xffU & (IData)((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e9__DIADI)))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h26c55382__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0__ADDRARDADDR) 
                                                  >> 3U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = __Vdlyvval__memory__DOT__words__v0;
    }
}
