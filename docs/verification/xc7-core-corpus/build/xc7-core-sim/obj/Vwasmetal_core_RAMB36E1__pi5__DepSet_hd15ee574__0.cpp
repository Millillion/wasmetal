#pragma GCC diagnostic ignored "-Wint-in-bool-context"
#pragma GCC diagnostic ignored "-Wbool-operation"
#pragma GCC diagnostic ignored "-Wbitwise-instead-of-logical"
// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vwasmetal_core.h for the primary calling header

#include "Vwasmetal_core__pch.h"
#include "Vwasmetal_core_RAMB36E1__pi5.h"
#include "Vwasmetal_core__Syms.h"

VL_INLINE_OPT void Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e0__0(Vwasmetal_core_RAMB36E1__pi5* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e0__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    CData/*4:0*/ __Vdlyvlsb__memory__DOT__words__v0;
    __Vdlyvlsb__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v1;
    __Vdlyvdim0__memory__DOT__words__v1 = 0;
    CData/*4:0*/ __Vdlyvlsb__memory__DOT__words__v1;
    __Vdlyvlsb__memory__DOT__words__v1 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v1;
    __Vdlyvval__memory__DOT__words__v1 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v1;
    __Vdlyvset__memory__DOT__words__v1 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    __Vdlyvset__memory__DOT__words__v1 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000130_))))) {
        vlSelf->memory__DOT____Vlvbound_h252618a2__0 
            = ((0x100U & (((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___134153___O) 
                           << 8U) | (0x200U & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___134155___O) 
                                               << 8U)))) 
               | (0xffU & (IData)((QData)((IData)((
                                                   (0x8000U 
                                                    & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___134155___O) 
                                                       << 0xfU)) 
                                                   | (((((IData)(vlSymsp->TOP.wasmetal_core__DOT___036762_) 
                                                         << 0xeU) 
                                                        | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036761_) 
                                                            << 0xdU) 
                                                           | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036760_) 
                                                               << 0xcU) 
                                                              | ((IData)(vlSymsp->TOP.wasmetal_core__DOT___036759_) 
                                                                 << 0xbU)))) 
                                                       ^ 
                                                       (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134154___DOT__CO__BRA__2__KET__) 
                                                         << 0xeU) 
                                                        | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134154___DOT__CO__BRA__1__KET__) 
                                                            << 0xdU) 
                                                           | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134154___DOT__CO__BRA__0__KET__) 
                                                               << 0xcU) 
                                                              | ((IData)(vlSymsp->TOP.wasmetal_core__DOT___036726_) 
                                                                 << 0xbU))))) 
                                                      | ((0x700U 
                                                          & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___134153___O) 
                                                             << 7U)) 
                                                         | (((((IData)(vlSymsp->TOP.wasmetal_core__DOT___036785_) 
                                                               << 7U) 
                                                              | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036784_) 
                                                                  << 6U) 
                                                                 | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036783_) 
                                                                     << 5U) 
                                                                    | ((IData)(vlSymsp->TOP.wasmetal_core__DOT___036782_) 
                                                                       << 4U)))) 
                                                             ^ 
                                                             (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134152___DOT__CO__BRA__2__KET__) 
                                                               << 7U) 
                                                              | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134152___DOT__CO__BRA__1__KET__) 
                                                                  << 6U) 
                                                                 | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134152___DOT__CO__BRA__0__KET__) 
                                                                     << 5U) 
                                                                    | ((IData)(vlSymsp->TOP.wasmetal_core__DOT___036749_) 
                                                                       << 4U))))) 
                                                            | ((((IData)(vlSymsp->TOP.wasmetal_core__DOT___036781_) 
                                                                 << 3U) 
                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036778_) 
                                                                    << 2U) 
                                                                   | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036767_) 
                                                                       << 1U) 
                                                                      | (1U 
                                                                         & (~ (IData)(vlSymsp->TOP.wasmetal_core__DOT___036595_)))))) 
                                                               ^ 
                                                               (3U 
                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134151___DOT__CO__BRA__2__KET__) 
                                                                    << 3U) 
                                                                   | ((IData)(vlSymsp->TOP.wasmetal_core__DOT___134151___DOT__CO__BRA__1__KET__) 
                                                                      << 2U)))))))))))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h252618a2__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvlsb__memory__DOT__words__v0 = 0U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRARDADDR) 
                                                  >> 4U));
    }
    if ((2U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000130_))))) {
        vlSelf->memory__DOT____Vlvbound_h252618a2__0 
            = ((0x100U & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___134155___O) 
                          << 7U)) | (0xffU & (IData)(
                                                     ((QData)((IData)(
                                                                      ((0x8000U 
                                                                        & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___134155___O) 
                                                                           << 0xfU)) 
                                                                       | (((((IData)(vlSymsp->TOP.wasmetal_core__DOT___036762_) 
                                                                             << 0xeU) 
                                                                            | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036761_) 
                                                                                << 0xdU) 
                                                                               | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036760_) 
                                                                                << 0xcU) 
                                                                                | ((IData)(vlSymsp->TOP.wasmetal_core__DOT___036759_) 
                                                                                << 0xbU)))) 
                                                                           ^ 
                                                                           (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134154___DOT__CO__BRA__2__KET__) 
                                                                             << 0xeU) 
                                                                            | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134154___DOT__CO__BRA__1__KET__) 
                                                                                << 0xdU) 
                                                                               | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134154___DOT__CO__BRA__0__KET__) 
                                                                                << 0xcU) 
                                                                                | ((IData)(vlSymsp->TOP.wasmetal_core__DOT___036726_) 
                                                                                << 0xbU))))) 
                                                                          | ((0x700U 
                                                                              & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___134153___O) 
                                                                                << 7U)) 
                                                                             | (((((IData)(vlSymsp->TOP.wasmetal_core__DOT___036785_) 
                                                                                << 7U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036784_) 
                                                                                << 6U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036783_) 
                                                                                << 5U) 
                                                                                | ((IData)(vlSymsp->TOP.wasmetal_core__DOT___036782_) 
                                                                                << 4U)))) 
                                                                                ^ 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134152___DOT__CO__BRA__2__KET__) 
                                                                                << 7U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134152___DOT__CO__BRA__1__KET__) 
                                                                                << 6U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134152___DOT__CO__BRA__0__KET__) 
                                                                                << 5U) 
                                                                                | ((IData)(vlSymsp->TOP.wasmetal_core__DOT___036749_) 
                                                                                << 4U))))) 
                                                                                | ((((IData)(vlSymsp->TOP.wasmetal_core__DOT___036781_) 
                                                                                << 3U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036778_) 
                                                                                << 2U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036767_) 
                                                                                << 1U) 
                                                                                | (1U 
                                                                                & (~ (IData)(vlSymsp->TOP.wasmetal_core__DOT___036595_)))))) 
                                                                                ^ 
                                                                                (3U 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134151___DOT__CO__BRA__2__KET__) 
                                                                                << 3U) 
                                                                                | ((IData)(vlSymsp->TOP.wasmetal_core__DOT___134151___DOT__CO__BRA__1__KET__) 
                                                                                << 2U)))))))))) 
                                                      >> 8U))));
        __Vdlyvval__memory__DOT__words__v1 = vlSelf->memory__DOT____Vlvbound_h252618a2__0;
        __Vdlyvset__memory__DOT__words__v1 = 1U;
        __Vdlyvlsb__memory__DOT__words__v1 = 9U;
        __Vdlyvdim0__memory__DOT__words__v1 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRARDADDR) 
                                                  >> 4U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = (((~ ((IData)(0x1ffU) << (IData)(__Vdlyvlsb__memory__DOT__words__v0))) 
                & vlSelf->__PVT__memory__DOT__words
                [__Vdlyvdim0__memory__DOT__words__v0]) 
               | (0x3ffffU & ((IData)(__Vdlyvval__memory__DOT__words__v0) 
                              << (IData)(__Vdlyvlsb__memory__DOT__words__v0))));
    }
    if (__Vdlyvset__memory__DOT__words__v1) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v1] 
            = (((~ ((IData)(0x1ffU) << (IData)(__Vdlyvlsb__memory__DOT__words__v1))) 
                & vlSelf->__PVT__memory__DOT__words
                [__Vdlyvdim0__memory__DOT__words__v1]) 
               | (0x3ffffU & ((IData)(__Vdlyvval__memory__DOT__words__v1) 
                              << (IData)(__Vdlyvlsb__memory__DOT__words__v1))));
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e0__1(Vwasmetal_core_RAMB36E1__pi5* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e0__1\n"); );
    // Body
    vlSelf->__PVT__memory__DOT__q = vlSelf->__PVT__memory__DOT__words
        [(0x7ffU & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRBWRADDR) 
                    >> 4U))];
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

VL_INLINE_OPT void Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e1__0(Vwasmetal_core_RAMB36E1__pi5* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e1__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    CData/*4:0*/ __Vdlyvlsb__memory__DOT__words__v0;
    __Vdlyvlsb__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v1;
    __Vdlyvdim0__memory__DOT__words__v1 = 0;
    CData/*4:0*/ __Vdlyvlsb__memory__DOT__words__v1;
    __Vdlyvlsb__memory__DOT__words__v1 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v1;
    __Vdlyvval__memory__DOT__words__v1 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v1;
    __Vdlyvset__memory__DOT__words__v1 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    __Vdlyvset__memory__DOT__words__v1 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000130_))))) {
        vlSelf->memory__DOT____Vlvbound_h252618a2__0 
            = (((1U & (((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___134157___O) 
                        >> 2U) | (2U & ((0xcaU >> (
                                                   ((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                    << 2U) 
                                                   | ((2U 
                                                       & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127994___O) 
                                                          >> 2U)) 
                                                      | (1U 
                                                         & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128026___O) 
                                                            >> 3U))))) 
                                        << 1U)))) << 8U) 
               | (0xffU & (IData)((QData)((IData)((
                                                   (0x8000U 
                                                    & ((0xcaU 
                                                        >> 
                                                        (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                          << 2U) 
                                                         | ((2U 
                                                             & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127994___O) 
                                                                >> 1U)) 
                                                            | (1U 
                                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128026___O) 
                                                                  >> 2U))))) 
                                                       << 0xfU)) 
                                                   | ((0x4000U 
                                                       & ((0xcaU 
                                                           >> 
                                                           (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                             << 2U) 
                                                            | ((2U 
                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127994___O)) 
                                                               | (1U 
                                                                  & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128026___O) 
                                                                     >> 1U))))) 
                                                          << 0xeU)) 
                                                      | ((0x2000U 
                                                          & ((0xcaU 
                                                              >> 
                                                              (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                << 2U) 
                                                               | ((2U 
                                                                   & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127994___O) 
                                                                      << 1U)) 
                                                                  | (1U 
                                                                     & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128026___O))))) 
                                                             << 0xdU)) 
                                                         | (((((IData)(vlSymsp->TOP.wasmetal_core__DOT___036780_) 
                                                               << 0xcU) 
                                                              | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036779_) 
                                                                  << 0xbU) 
                                                                 | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036777_) 
                                                                     << 0xaU) 
                                                                    | ((IData)(vlSymsp->TOP.wasmetal_core__DOT___036776_) 
                                                                       << 9U)))) 
                                                             ^ 
                                                             ((0x1000U 
                                                               & (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036779_)
                                                                    ? (IData)(vlSymsp->TOP.wasmetal_core__DOT___134158___DOT__CO__BRA__1__KET__)
                                                                    : 
                                                                   (6U 
                                                                    >> (IData)(vlSymsp->TOP.__VdfgTmp_hf9e7c209__0))) 
                                                                  << 0xcU)) 
                                                              | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134158___DOT__CO__BRA__1__KET__) 
                                                                  << 0xbU) 
                                                                 | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134158___DOT__CO__BRA__0__KET__) 
                                                                     << 0xaU) 
                                                                    | ((IData)(vlSymsp->TOP.wasmetal_core__DOT___036743_) 
                                                                       << 9U))))) 
                                                            | ((0x100U 
                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___134157___O) 
                                                                   << 5U)) 
                                                               | ((0xc0U 
                                                                   & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___134157___O) 
                                                                      << 6U)) 
                                                                  | (((((IData)(vlSymsp->TOP.wasmetal_core__DOT___036771_) 
                                                                        << 5U) 
                                                                       | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036770_) 
                                                                           << 4U) 
                                                                          | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036769_) 
                                                                              << 3U) 
                                                                             | ((IData)(vlSymsp->TOP.wasmetal_core__DOT___036768_) 
                                                                                << 2U)))) 
                                                                      ^ 
                                                                      (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134156___DOT__CO__BRA__2__KET__) 
                                                                        << 5U) 
                                                                       | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134156___DOT__CO__BRA__1__KET__) 
                                                                           << 4U) 
                                                                          | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134156___DOT__CO__BRA__0__KET__) 
                                                                              << 3U) 
                                                                             | ((IData)(vlSymsp->TOP.wasmetal_core__DOT___036734_) 
                                                                                << 2U))))) 
                                                                     | (3U 
                                                                        & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___134155___O) 
                                                                           >> 2U))))))))))))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h252618a2__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvlsb__memory__DOT__words__v0 = 0U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRARDADDR) 
                                                  >> 4U));
    }
    if ((2U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000130_))))) {
        vlSelf->memory__DOT____Vlvbound_h252618a2__0 
            = ((0x100U & ((0xcaU >> (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                      << 2U) | ((2U 
                                                 & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127994___O) 
                                                    >> 2U)) 
                                                | (1U 
                                                   & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128026___O) 
                                                      >> 3U))))) 
                          << 8U)) | (0xffU & (IData)(
                                                     ((QData)((IData)(
                                                                      ((0x8000U 
                                                                        & ((0xcaU 
                                                                            >> 
                                                                            (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                              << 2U) 
                                                                             | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127994___O) 
                                                                                >> 1U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128026___O) 
                                                                                >> 2U))))) 
                                                                           << 0xfU)) 
                                                                       | ((0x4000U 
                                                                           & ((0xcaU 
                                                                               >> 
                                                                               (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127994___O)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128026___O) 
                                                                                >> 1U))))) 
                                                                              << 0xeU)) 
                                                                          | ((0x2000U 
                                                                              & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127994___O) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128026___O))))) 
                                                                                << 0xdU)) 
                                                                             | (((((IData)(vlSymsp->TOP.wasmetal_core__DOT___036780_) 
                                                                                << 0xcU) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036779_) 
                                                                                << 0xbU) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036777_) 
                                                                                << 0xaU) 
                                                                                | ((IData)(vlSymsp->TOP.wasmetal_core__DOT___036776_) 
                                                                                << 9U)))) 
                                                                                ^ 
                                                                                ((0x1000U 
                                                                                & (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036779_)
                                                                                 ? (IData)(vlSymsp->TOP.wasmetal_core__DOT___134158___DOT__CO__BRA__1__KET__)
                                                                                 : 
                                                                                (6U 
                                                                                >> (IData)(vlSymsp->TOP.__VdfgTmp_hf9e7c209__0))) 
                                                                                << 0xcU)) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134158___DOT__CO__BRA__1__KET__) 
                                                                                << 0xbU) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134158___DOT__CO__BRA__0__KET__) 
                                                                                << 0xaU) 
                                                                                | ((IData)(vlSymsp->TOP.wasmetal_core__DOT___036743_) 
                                                                                << 9U))))) 
                                                                                | ((0x100U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___134157___O) 
                                                                                << 5U)) 
                                                                                | ((0xc0U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___134157___O) 
                                                                                << 6U)) 
                                                                                | (((((IData)(vlSymsp->TOP.wasmetal_core__DOT___036771_) 
                                                                                << 5U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036770_) 
                                                                                << 4U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___036769_) 
                                                                                << 3U) 
                                                                                | ((IData)(vlSymsp->TOP.wasmetal_core__DOT___036768_) 
                                                                                << 2U)))) 
                                                                                ^ 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134156___DOT__CO__BRA__2__KET__) 
                                                                                << 5U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134156___DOT__CO__BRA__1__KET__) 
                                                                                << 4U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___134156___DOT__CO__BRA__0__KET__) 
                                                                                << 3U) 
                                                                                | ((IData)(vlSymsp->TOP.wasmetal_core__DOT___036734_) 
                                                                                << 2U))))) 
                                                                                | (3U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___134155___O) 
                                                                                >> 2U))))))))))) 
                                                      >> 8U))));
        __Vdlyvval__memory__DOT__words__v1 = vlSelf->memory__DOT____Vlvbound_h252618a2__0;
        __Vdlyvset__memory__DOT__words__v1 = 1U;
        __Vdlyvlsb__memory__DOT__words__v1 = 9U;
        __Vdlyvdim0__memory__DOT__words__v1 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRARDADDR) 
                                                  >> 4U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = (((~ ((IData)(0x1ffU) << (IData)(__Vdlyvlsb__memory__DOT__words__v0))) 
                & vlSelf->__PVT__memory__DOT__words
                [__Vdlyvdim0__memory__DOT__words__v0]) 
               | (0x3ffffU & ((IData)(__Vdlyvval__memory__DOT__words__v0) 
                              << (IData)(__Vdlyvlsb__memory__DOT__words__v0))));
    }
    if (__Vdlyvset__memory__DOT__words__v1) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v1] 
            = (((~ ((IData)(0x1ffU) << (IData)(__Vdlyvlsb__memory__DOT__words__v1))) 
                & vlSelf->__PVT__memory__DOT__words
                [__Vdlyvdim0__memory__DOT__words__v1]) 
               | (0x3ffffU & ((IData)(__Vdlyvval__memory__DOT__words__v1) 
                              << (IData)(__Vdlyvlsb__memory__DOT__words__v1))));
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e2__0(Vwasmetal_core_RAMB36E1__pi5* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e2__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    CData/*4:0*/ __Vdlyvlsb__memory__DOT__words__v0;
    __Vdlyvlsb__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v1;
    __Vdlyvdim0__memory__DOT__words__v1 = 0;
    CData/*4:0*/ __Vdlyvlsb__memory__DOT__words__v1;
    __Vdlyvlsb__memory__DOT__words__v1 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v1;
    __Vdlyvval__memory__DOT__words__v1 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v1;
    __Vdlyvset__memory__DOT__words__v1 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    __Vdlyvset__memory__DOT__words__v1 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000130_))))) {
        vlSelf->memory__DOT____Vlvbound_h252618a2__0 
            = ((0x100U & ((0x200U & ((0xcaU >> (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                 << 2U) 
                                                | ((2U 
                                                    & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127999___O)) 
                                                   | (1U 
                                                      & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128031___O) 
                                                         >> 1U))))) 
                                     << 9U)) | (0x100U 
                                                & ((0xcaU 
                                                    >> 
                                                    (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                      << 2U) 
                                                     | ((2U 
                                                         & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127997___O) 
                                                            << 1U)) 
                                                        | (1U 
                                                           & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128029___O))))) 
                                                   << 8U)))) 
               | (0xffU & (IData)((QData)((IData)((
                                                   (0x8000U 
                                                    & ((0xcaU 
                                                        >> 
                                                        (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                          << 2U) 
                                                         | ((2U 
                                                             & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127999___O) 
                                                                << 1U)) 
                                                            | (1U 
                                                               & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128031___O))))) 
                                                       << 0xfU)) 
                                                   | ((0x4000U 
                                                       & ((0xcaU 
                                                           >> 
                                                           (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                             << 2U) 
                                                            | ((2U 
                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127998___O) 
                                                                   >> 2U)) 
                                                               | (1U 
                                                                  & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128030___O) 
                                                                     >> 3U))))) 
                                                          << 0xeU)) 
                                                      | ((0x2000U 
                                                          & ((0xcaU 
                                                              >> 
                                                              (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                << 2U) 
                                                               | ((2U 
                                                                   & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127998___O) 
                                                                      >> 1U)) 
                                                                  | (1U 
                                                                     & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128030___O) 
                                                                        >> 2U))))) 
                                                             << 0xdU)) 
                                                         | ((0x1000U 
                                                             & ((0xcaU 
                                                                 >> 
                                                                 (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                   << 2U) 
                                                                  | ((2U 
                                                                      & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127998___O)) 
                                                                     | (1U 
                                                                        & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128030___O) 
                                                                           >> 1U))))) 
                                                                << 0xcU)) 
                                                            | ((0x800U 
                                                                & ((0xcaU 
                                                                    >> 
                                                                    (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                      << 2U) 
                                                                     | ((2U 
                                                                         & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127998___O) 
                                                                            << 1U)) 
                                                                        | (1U 
                                                                           & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128030___O))))) 
                                                                   << 0xbU)) 
                                                               | ((0x400U 
                                                                   & ((0xcaU 
                                                                       >> 
                                                                       (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                         << 2U) 
                                                                        | ((2U 
                                                                            & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127997___O) 
                                                                               >> 2U)) 
                                                                           | (1U 
                                                                              & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128029___O) 
                                                                                >> 3U))))) 
                                                                      << 0xaU)) 
                                                                  | ((0x200U 
                                                                      & ((0xcaU 
                                                                          >> 
                                                                          (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                            << 2U) 
                                                                           | ((2U 
                                                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127997___O) 
                                                                                >> 1U)) 
                                                                              | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128029___O) 
                                                                                >> 2U))))) 
                                                                         << 9U)) 
                                                                     | ((0x100U 
                                                                         & ((0xcaU 
                                                                             >> 
                                                                             (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                               << 2U) 
                                                                              | ((2U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127997___O)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128029___O) 
                                                                                >> 1U))))) 
                                                                            << 8U)) 
                                                                        | ((0x80U 
                                                                            & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127996___O) 
                                                                                >> 2U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128028___O) 
                                                                                >> 3U))))) 
                                                                               << 7U)) 
                                                                           | ((0x40U 
                                                                               & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127996___O) 
                                                                                >> 1U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128028___O) 
                                                                                >> 2U))))) 
                                                                                << 6U)) 
                                                                              | ((0x20U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127996___O)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128028___O) 
                                                                                >> 1U))))) 
                                                                                << 5U)) 
                                                                                | ((0x10U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127996___O) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128028___O))))) 
                                                                                << 4U)) 
                                                                                | ((8U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127995___O) 
                                                                                >> 2U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128027___O) 
                                                                                >> 3U))))) 
                                                                                << 3U)) 
                                                                                | ((4U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127995___O) 
                                                                                >> 1U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128027___O) 
                                                                                >> 2U))))) 
                                                                                << 2U)) 
                                                                                | ((2U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127995___O)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128027___O) 
                                                                                >> 1U))))) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127995___O) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128027___O))))))))))))))))))))))))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h252618a2__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvlsb__memory__DOT__words__v0 = 0U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRARDADDR) 
                                                  >> 4U));
    }
    if ((2U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000130_))))) {
        vlSelf->memory__DOT____Vlvbound_h252618a2__0 
            = ((0x100U & ((0xcaU >> (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                      << 2U) | ((2U 
                                                 & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127999___O)) 
                                                | (1U 
                                                   & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128031___O) 
                                                      >> 1U))))) 
                          << 8U)) | (0xffU & (IData)(
                                                     ((QData)((IData)(
                                                                      ((0x8000U 
                                                                        & ((0xcaU 
                                                                            >> 
                                                                            (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                              << 2U) 
                                                                             | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127999___O) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128031___O))))) 
                                                                           << 0xfU)) 
                                                                       | ((0x4000U 
                                                                           & ((0xcaU 
                                                                               >> 
                                                                               (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127998___O) 
                                                                                >> 2U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128030___O) 
                                                                                >> 3U))))) 
                                                                              << 0xeU)) 
                                                                          | ((0x2000U 
                                                                              & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127998___O) 
                                                                                >> 1U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128030___O) 
                                                                                >> 2U))))) 
                                                                                << 0xdU)) 
                                                                             | ((0x1000U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127998___O)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128030___O) 
                                                                                >> 1U))))) 
                                                                                << 0xcU)) 
                                                                                | ((0x800U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127998___O) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128030___O))))) 
                                                                                << 0xbU)) 
                                                                                | ((0x400U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127997___O) 
                                                                                >> 2U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128029___O) 
                                                                                >> 3U))))) 
                                                                                << 0xaU)) 
                                                                                | ((0x200U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127997___O) 
                                                                                >> 1U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128029___O) 
                                                                                >> 2U))))) 
                                                                                << 9U)) 
                                                                                | ((0x100U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127997___O)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128029___O) 
                                                                                >> 1U))))) 
                                                                                << 8U)) 
                                                                                | ((0x80U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127996___O) 
                                                                                >> 2U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128028___O) 
                                                                                >> 3U))))) 
                                                                                << 7U)) 
                                                                                | ((0x40U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127996___O) 
                                                                                >> 1U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128028___O) 
                                                                                >> 2U))))) 
                                                                                << 6U)) 
                                                                                | ((0x20U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127996___O)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128028___O) 
                                                                                >> 1U))))) 
                                                                                << 5U)) 
                                                                                | ((0x10U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127996___O) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128028___O))))) 
                                                                                << 4U)) 
                                                                                | ((8U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127995___O) 
                                                                                >> 2U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128027___O) 
                                                                                >> 3U))))) 
                                                                                << 3U)) 
                                                                                | ((4U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127995___O) 
                                                                                >> 1U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128027___O) 
                                                                                >> 2U))))) 
                                                                                << 2U)) 
                                                                                | ((2U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127995___O)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128027___O) 
                                                                                >> 1U))))) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127995___O) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128027___O))))))))))))))))))))))) 
                                                      >> 8U))));
        __Vdlyvval__memory__DOT__words__v1 = vlSelf->memory__DOT____Vlvbound_h252618a2__0;
        __Vdlyvset__memory__DOT__words__v1 = 1U;
        __Vdlyvlsb__memory__DOT__words__v1 = 9U;
        __Vdlyvdim0__memory__DOT__words__v1 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRARDADDR) 
                                                  >> 4U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = (((~ ((IData)(0x1ffU) << (IData)(__Vdlyvlsb__memory__DOT__words__v0))) 
                & vlSelf->__PVT__memory__DOT__words
                [__Vdlyvdim0__memory__DOT__words__v0]) 
               | (0x3ffffU & ((IData)(__Vdlyvval__memory__DOT__words__v0) 
                              << (IData)(__Vdlyvlsb__memory__DOT__words__v0))));
    }
    if (__Vdlyvset__memory__DOT__words__v1) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v1] 
            = (((~ ((IData)(0x1ffU) << (IData)(__Vdlyvlsb__memory__DOT__words__v1))) 
                & vlSelf->__PVT__memory__DOT__words
                [__Vdlyvdim0__memory__DOT__words__v1]) 
               | (0x3ffffU & ((IData)(__Vdlyvval__memory__DOT__words__v1) 
                              << (IData)(__Vdlyvlsb__memory__DOT__words__v1))));
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e2__1(Vwasmetal_core_RAMB36E1__pi5* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e2__1\n"); );
    // Body
    vlSelf->__PVT__memory__DOT__q = vlSelf->__PVT__memory__DOT__words
        [(0x7ffU & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRBWRADDR) 
                    >> 4U))];
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

VL_INLINE_OPT void Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e3__0(Vwasmetal_core_RAMB36E1__pi5* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e3__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    CData/*4:0*/ __Vdlyvlsb__memory__DOT__words__v0;
    __Vdlyvlsb__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v1;
    __Vdlyvdim0__memory__DOT__words__v1 = 0;
    CData/*4:0*/ __Vdlyvlsb__memory__DOT__words__v1;
    __Vdlyvlsb__memory__DOT__words__v1 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v1;
    __Vdlyvval__memory__DOT__words__v1 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v1;
    __Vdlyvset__memory__DOT__words__v1 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    __Vdlyvset__memory__DOT__words__v1 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000130_))))) {
        vlSelf->memory__DOT____Vlvbound_h252618a2__0 
            = ((0x100U & ((0x200U & ((0xcaU >> (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                 << 2U) 
                                                | (IData)(vlSymsp->TOP.__VdfgTmp_hd0f5eb35__0))) 
                                     << 9U)) | (0x100U 
                                                & ((0xcaU 
                                                    >> 
                                                    (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                      << 2U) 
                                                     | ((2U 
                                                         & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128001___O) 
                                                            >> 1U)) 
                                                        | (1U 
                                                           & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128033___O) 
                                                              >> 2U))))) 
                                                   << 8U)))) 
               | (0xffU & (IData)((QData)((IData)((
                                                   (0x8000U 
                                                    & ((0xcaU 
                                                        >> 
                                                        (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                          << 2U) 
                                                         | (IData)(vlSymsp->TOP.__VdfgTmp_hd3ff3db1__0))) 
                                                       << 0xfU)) 
                                                   | ((0x4000U 
                                                       & ((0xcaU 
                                                           >> 
                                                           (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                             << 2U) 
                                                            | (IData)(vlSymsp->TOP.__VdfgTmp_hd6f0d46f__0))) 
                                                          << 0xeU)) 
                                                      | ((0x2000U 
                                                          & ((0xcaU 
                                                              >> 
                                                              (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                << 2U) 
                                                               | (IData)(vlSymsp->TOP.__VdfgTmp_he98db662__0))) 
                                                             << 0xdU)) 
                                                         | ((0x1000U 
                                                             & ((0xcaU 
                                                                 >> 
                                                                 (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                   << 2U) 
                                                                  | (IData)(vlSymsp->TOP.__VdfgTmp_hec90fad7__0))) 
                                                                << 0xcU)) 
                                                            | ((0x800U 
                                                                & ((0xcaU 
                                                                    >> 
                                                                    (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                      << 2U) 
                                                                     | (IData)(vlSymsp->TOP.__VdfgTmp_hefae6eba__0))) 
                                                                   << 0xbU)) 
                                                               | ((0x400U 
                                                                   & ((0xcaU 
                                                                       >> 
                                                                       (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                         << 2U) 
                                                                        | (IData)(vlSymsp->TOP.__VdfgTmp_hc52368c6__0))) 
                                                                      << 0xaU)) 
                                                                  | ((0x200U 
                                                                      & ((0xcaU 
                                                                          >> 
                                                                          (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                            << 2U) 
                                                                           | (IData)(vlSymsp->TOP.__VdfgTmp_hc3828814__0))) 
                                                                         << 9U)) 
                                                                     | ((0x100U 
                                                                         & ((0xcaU 
                                                                             >> 
                                                                             (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                               << 2U) 
                                                                              | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128001___O) 
                                                                                >> 2U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128033___O) 
                                                                                >> 3U))))) 
                                                                            << 8U)) 
                                                                        | ((0x80U 
                                                                            & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128001___O)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128033___O) 
                                                                                >> 1U))))) 
                                                                               << 7U)) 
                                                                           | ((0x40U 
                                                                               & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128001___O) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128033___O))))) 
                                                                                << 6U)) 
                                                                              | ((0x20U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128000___O) 
                                                                                >> 2U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128032___O) 
                                                                                >> 3U))))) 
                                                                                << 5U)) 
                                                                                | ((0x10U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128000___O) 
                                                                                >> 1U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128032___O) 
                                                                                >> 2U))))) 
                                                                                << 4U)) 
                                                                                | ((8U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128000___O)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128032___O) 
                                                                                >> 1U))))) 
                                                                                << 3U)) 
                                                                                | ((4U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128000___O) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128032___O))))) 
                                                                                << 2U)) 
                                                                                | ((2U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127999___O) 
                                                                                >> 2U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128031___O) 
                                                                                >> 3U))))) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127999___O) 
                                                                                >> 1U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128031___O) 
                                                                                >> 2U))))))))))))))))))))))))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h252618a2__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvlsb__memory__DOT__words__v0 = 0U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRARDADDR) 
                                                  >> 4U));
    }
    if ((2U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000130_))))) {
        vlSelf->memory__DOT____Vlvbound_h252618a2__0 
            = ((0x100U & ((0xcaU >> (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                      << 2U) | (IData)(vlSymsp->TOP.__VdfgTmp_hd0f5eb35__0))) 
                          << 8U)) | (0xffU & (IData)(
                                                     ((QData)((IData)(
                                                                      ((0x8000U 
                                                                        & ((0xcaU 
                                                                            >> 
                                                                            (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                              << 2U) 
                                                                             | (IData)(vlSymsp->TOP.__VdfgTmp_hd3ff3db1__0))) 
                                                                           << 0xfU)) 
                                                                       | ((0x4000U 
                                                                           & ((0xcaU 
                                                                               >> 
                                                                               (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_hd6f0d46f__0))) 
                                                                              << 0xeU)) 
                                                                          | ((0x2000U 
                                                                              & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_he98db662__0))) 
                                                                                << 0xdU)) 
                                                                             | ((0x1000U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_hec90fad7__0))) 
                                                                                << 0xcU)) 
                                                                                | ((0x800U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_hefae6eba__0))) 
                                                                                << 0xbU)) 
                                                                                | ((0x400U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_hc52368c6__0))) 
                                                                                << 0xaU)) 
                                                                                | ((0x200U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_hc3828814__0))) 
                                                                                << 9U)) 
                                                                                | ((0x100U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128001___O) 
                                                                                >> 2U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128033___O) 
                                                                                >> 3U))))) 
                                                                                << 8U)) 
                                                                                | ((0x80U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128001___O)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128033___O) 
                                                                                >> 1U))))) 
                                                                                << 7U)) 
                                                                                | ((0x40U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128001___O) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128033___O))))) 
                                                                                << 6U)) 
                                                                                | ((0x20U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128000___O) 
                                                                                >> 2U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128032___O) 
                                                                                >> 3U))))) 
                                                                                << 5U)) 
                                                                                | ((0x10U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128000___O) 
                                                                                >> 1U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128032___O) 
                                                                                >> 2U))))) 
                                                                                << 4U)) 
                                                                                | ((8U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128000___O)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128032___O) 
                                                                                >> 1U))))) 
                                                                                << 3U)) 
                                                                                | ((4U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128000___O) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128032___O))))) 
                                                                                << 2U)) 
                                                                                | ((2U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127999___O) 
                                                                                >> 2U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128031___O) 
                                                                                >> 3U))))) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___127999___O) 
                                                                                >> 1U)) 
                                                                                | (1U 
                                                                                & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellout___128031___O) 
                                                                                >> 2U))))))))))))))))))))))) 
                                                      >> 8U))));
        __Vdlyvval__memory__DOT__words__v1 = vlSelf->memory__DOT____Vlvbound_h252618a2__0;
        __Vdlyvset__memory__DOT__words__v1 = 1U;
        __Vdlyvlsb__memory__DOT__words__v1 = 9U;
        __Vdlyvdim0__memory__DOT__words__v1 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRARDADDR) 
                                                  >> 4U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = (((~ ((IData)(0x1ffU) << (IData)(__Vdlyvlsb__memory__DOT__words__v0))) 
                & vlSelf->__PVT__memory__DOT__words
                [__Vdlyvdim0__memory__DOT__words__v0]) 
               | (0x3ffffU & ((IData)(__Vdlyvval__memory__DOT__words__v0) 
                              << (IData)(__Vdlyvlsb__memory__DOT__words__v0))));
    }
    if (__Vdlyvset__memory__DOT__words__v1) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v1] 
            = (((~ ((IData)(0x1ffU) << (IData)(__Vdlyvlsb__memory__DOT__words__v1))) 
                & vlSelf->__PVT__memory__DOT__words
                [__Vdlyvdim0__memory__DOT__words__v1]) 
               | (0x3ffffU & ((IData)(__Vdlyvval__memory__DOT__words__v1) 
                              << (IData)(__Vdlyvlsb__memory__DOT__words__v1))));
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e4__0(Vwasmetal_core_RAMB36E1__pi5* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e4__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    CData/*4:0*/ __Vdlyvlsb__memory__DOT__words__v0;
    __Vdlyvlsb__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v1;
    __Vdlyvdim0__memory__DOT__words__v1 = 0;
    CData/*4:0*/ __Vdlyvlsb__memory__DOT__words__v1;
    __Vdlyvlsb__memory__DOT__words__v1 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v1;
    __Vdlyvval__memory__DOT__words__v1 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v1;
    __Vdlyvset__memory__DOT__words__v1 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    __Vdlyvset__memory__DOT__words__v1 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000130_))))) {
        vlSelf->memory__DOT____Vlvbound_h252618a2__0 
            = ((0x100U & ((0x200U & ((0xcaU >> (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                 << 2U) 
                                                | (IData)(vlSymsp->TOP.__VdfgTmp_heb8306fa__0))) 
                                     << 9U)) | (0x100U 
                                                & ((0xcaU 
                                                    >> 
                                                    (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                      << 2U) 
                                                     | (IData)(vlSymsp->TOP.__VdfgTmp_h134dac5a__0))) 
                                                   << 8U)))) 
               | (0xffU & (IData)((QData)((IData)((
                                                   (0x8000U 
                                                    & ((0xcaU 
                                                        >> 
                                                        (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                          << 2U) 
                                                         | (IData)(vlSymsp->TOP.__VdfgTmp_he4692376__0))) 
                                                       << 0xfU)) 
                                                   | ((0x4000U 
                                                       & ((0xcaU 
                                                           >> 
                                                           (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                             << 2U) 
                                                            | (IData)(vlSymsp->TOP.__VdfgTmp_he580b887__0))) 
                                                          << 0xeU)) 
                                                      | ((0x2000U 
                                                          & ((0xcaU 
                                                              >> 
                                                              (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                << 2U) 
                                                               | (IData)(vlSymsp->TOP.__VdfgTmp_he08305af__0))) 
                                                             << 0xdU)) 
                                                         | ((0x1000U 
                                                             & ((0xcaU 
                                                                 >> 
                                                                 (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                   << 2U) 
                                                                  | (IData)(vlSymsp->TOP.__VdfgTmp_h273da3c5__0))) 
                                                                << 0xcU)) 
                                                            | ((0x800U 
                                                                & ((0xcaU 
                                                                    >> 
                                                                    (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                      << 2U) 
                                                                     | (IData)(vlSymsp->TOP.__VdfgTmp_h2660b6cc__0))) 
                                                                   << 0xbU)) 
                                                               | ((0x400U 
                                                                   & ((0xcaU 
                                                                       >> 
                                                                       (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                         << 2U) 
                                                                        | (IData)(vlSymsp->TOP.__VdfgTmp_h3d708201__0))) 
                                                                      << 0xaU)) 
                                                                  | ((0x200U 
                                                                      & ((0xcaU 
                                                                          >> 
                                                                          (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                            << 2U) 
                                                                           | (IData)(vlSymsp->TOP.__VdfgTmp_h3c4e434c__0))) 
                                                                         << 9U)) 
                                                                     | ((0x100U 
                                                                         & ((0xcaU 
                                                                             >> 
                                                                             (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                               << 2U) 
                                                                              | (IData)(vlSymsp->TOP.__VdfgTmp_he366744c__0))) 
                                                                            << 8U)) 
                                                                        | ((0x80U 
                                                                            & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h19a3d105__0))) 
                                                                               << 7U)) 
                                                                           | ((0x40U 
                                                                               & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h1a8ff62f__0))) 
                                                                                << 6U)) 
                                                                              | ((0x20U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h1fc2f2ef__0))) 
                                                                                << 5U)) 
                                                                                | ((0x10U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h10bdd4bc__0))) 
                                                                                << 4U)) 
                                                                                | ((8U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h1585cf87__0))) 
                                                                                << 3U)) 
                                                                                | ((4U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h16f85c0c__0))) 
                                                                                << 2U)) 
                                                                                | ((2U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_heb713746__0))) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_hedbed4ea__0))))))))))))))))))))))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h252618a2__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvlsb__memory__DOT__words__v0 = 0U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRARDADDR) 
                                                  >> 4U));
    }
    if ((2U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000130_))))) {
        vlSelf->memory__DOT____Vlvbound_h252618a2__0 
            = ((0x100U & ((0xcaU >> (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                      << 2U) | (IData)(vlSymsp->TOP.__VdfgTmp_heb8306fa__0))) 
                          << 8U)) | (0xffU & (IData)(
                                                     ((QData)((IData)(
                                                                      ((0x8000U 
                                                                        & ((0xcaU 
                                                                            >> 
                                                                            (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                              << 2U) 
                                                                             | (IData)(vlSymsp->TOP.__VdfgTmp_he4692376__0))) 
                                                                           << 0xfU)) 
                                                                       | ((0x4000U 
                                                                           & ((0xcaU 
                                                                               >> 
                                                                               (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_he580b887__0))) 
                                                                              << 0xeU)) 
                                                                          | ((0x2000U 
                                                                              & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_he08305af__0))) 
                                                                                << 0xdU)) 
                                                                             | ((0x1000U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h273da3c5__0))) 
                                                                                << 0xcU)) 
                                                                                | ((0x800U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h2660b6cc__0))) 
                                                                                << 0xbU)) 
                                                                                | ((0x400U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h3d708201__0))) 
                                                                                << 0xaU)) 
                                                                                | ((0x200U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h3c4e434c__0))) 
                                                                                << 9U)) 
                                                                                | ((0x100U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_he366744c__0))) 
                                                                                << 8U)) 
                                                                                | ((0x80U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h19a3d105__0))) 
                                                                                << 7U)) 
                                                                                | ((0x40U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h1a8ff62f__0))) 
                                                                                << 6U)) 
                                                                                | ((0x20U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h1fc2f2ef__0))) 
                                                                                << 5U)) 
                                                                                | ((0x10U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h10bdd4bc__0))) 
                                                                                << 4U)) 
                                                                                | ((8U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h1585cf87__0))) 
                                                                                << 3U)) 
                                                                                | ((4U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h16f85c0c__0))) 
                                                                                << 2U)) 
                                                                                | ((2U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_heb713746__0))) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_hedbed4ea__0))))))))))))))))))))) 
                                                      >> 8U))));
        __Vdlyvval__memory__DOT__words__v1 = vlSelf->memory__DOT____Vlvbound_h252618a2__0;
        __Vdlyvset__memory__DOT__words__v1 = 1U;
        __Vdlyvlsb__memory__DOT__words__v1 = 9U;
        __Vdlyvdim0__memory__DOT__words__v1 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRARDADDR) 
                                                  >> 4U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = (((~ ((IData)(0x1ffU) << (IData)(__Vdlyvlsb__memory__DOT__words__v0))) 
                & vlSelf->__PVT__memory__DOT__words
                [__Vdlyvdim0__memory__DOT__words__v0]) 
               | (0x3ffffU & ((IData)(__Vdlyvval__memory__DOT__words__v0) 
                              << (IData)(__Vdlyvlsb__memory__DOT__words__v0))));
    }
    if (__Vdlyvset__memory__DOT__words__v1) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v1] 
            = (((~ ((IData)(0x1ffU) << (IData)(__Vdlyvlsb__memory__DOT__words__v1))) 
                & vlSelf->__PVT__memory__DOT__words
                [__Vdlyvdim0__memory__DOT__words__v1]) 
               | (0x3ffffU & ((IData)(__Vdlyvval__memory__DOT__words__v1) 
                              << (IData)(__Vdlyvlsb__memory__DOT__words__v1))));
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e5__0(Vwasmetal_core_RAMB36E1__pi5* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e5__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    CData/*4:0*/ __Vdlyvlsb__memory__DOT__words__v0;
    __Vdlyvlsb__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v1;
    __Vdlyvdim0__memory__DOT__words__v1 = 0;
    CData/*4:0*/ __Vdlyvlsb__memory__DOT__words__v1;
    __Vdlyvlsb__memory__DOT__words__v1 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v1;
    __Vdlyvval__memory__DOT__words__v1 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v1;
    __Vdlyvset__memory__DOT__words__v1 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    __Vdlyvset__memory__DOT__words__v1 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000130_))))) {
        vlSelf->memory__DOT____Vlvbound_h252618a2__0 
            = ((0x100U & ((0x200U & ((8U >> ((2U & 
                                              (vlSymsp->TOP.insn_w 
                                               >> 9U)) 
                                             | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                     << 9U)) | (0x100U 
                                                & ((8U 
                                                    >> 
                                                    ((2U 
                                                      & vlSymsp->TOP.insn_w) 
                                                     | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                   << 8U)))) 
               | (0xffU & (IData)((QData)((IData)((
                                                   (0x8000U 
                                                    & ((8U 
                                                        >> 
                                                        ((2U 
                                                          & (vlSymsp->TOP.insn_w 
                                                             >> 8U)) 
                                                         | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                       << 0xfU)) 
                                                   | ((0x4000U 
                                                       & ((8U 
                                                           >> 
                                                           ((2U 
                                                             & (vlSymsp->TOP.insn_w 
                                                                >> 7U)) 
                                                            | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                          << 0xeU)) 
                                                      | ((0x2000U 
                                                          & ((8U 
                                                              >> 
                                                              ((2U 
                                                                & (vlSymsp->TOP.insn_w 
                                                                   >> 6U)) 
                                                               | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                             << 0xdU)) 
                                                         | ((0x1000U 
                                                             & ((8U 
                                                                 >> 
                                                                 ((2U 
                                                                   & (vlSymsp->TOP.insn_w 
                                                                      >> 5U)) 
                                                                  | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                << 0xcU)) 
                                                            | ((0x800U 
                                                                & ((8U 
                                                                    >> 
                                                                    ((2U 
                                                                      & (vlSymsp->TOP.insn_w 
                                                                         >> 4U)) 
                                                                     | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                   << 0xbU)) 
                                                               | ((0x400U 
                                                                   & ((8U 
                                                                       >> 
                                                                       ((2U 
                                                                         & (vlSymsp->TOP.insn_w 
                                                                            >> 3U)) 
                                                                        | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                      << 0xaU)) 
                                                                  | ((0x200U 
                                                                      & ((8U 
                                                                          >> 
                                                                          ((2U 
                                                                            & (vlSymsp->TOP.insn_w 
                                                                               >> 2U)) 
                                                                           | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                         << 9U)) 
                                                                     | ((0x100U 
                                                                         & ((8U 
                                                                             >> 
                                                                             ((2U 
                                                                               & (vlSymsp->TOP.insn_w 
                                                                                >> 1U)) 
                                                                              | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                            << 8U)) 
                                                                        | ((0x80U 
                                                                            & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                << 1U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                               << 7U)) 
                                                                           | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                               << 6U) 
                                                                              | ((0x20U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h26a9e557__0))) 
                                                                                << 5U)) 
                                                                                | ((0x10U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h265c757d__0))) 
                                                                                << 4U)) 
                                                                                | ((8U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h272aca04__0))) 
                                                                                << 3U)) 
                                                                                | ((4U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_he081d797__0))) 
                                                                                << 2U)) 
                                                                                | ((2U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_he16c95bc__0))) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h3a2be217__0))))))))))))))))))))))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h252618a2__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvlsb__memory__DOT__words__v0 = 0U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRARDADDR) 
                                                  >> 4U));
    }
    if ((2U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000130_))))) {
        vlSelf->memory__DOT____Vlvbound_h252618a2__0 
            = ((0x100U & ((8U >> ((2U & (vlSymsp->TOP.insn_w 
                                         >> 9U)) | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                          << 8U)) | (0xffU & (IData)(
                                                     ((QData)((IData)(
                                                                      ((0x8000U 
                                                                        & ((8U 
                                                                            >> 
                                                                            ((2U 
                                                                              & (vlSymsp->TOP.insn_w 
                                                                                >> 8U)) 
                                                                             | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                           << 0xfU)) 
                                                                       | ((0x4000U 
                                                                           & ((8U 
                                                                               >> 
                                                                               ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 7U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                              << 0xeU)) 
                                                                          | ((0x2000U 
                                                                              & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 6U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 0xdU)) 
                                                                             | ((0x1000U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 5U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 0xcU)) 
                                                                                | ((0x800U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 4U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 0xbU)) 
                                                                                | ((0x400U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 3U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 0xaU)) 
                                                                                | ((0x200U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 2U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 9U)) 
                                                                                | ((0x100U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 1U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 8U)) 
                                                                                | ((0x80U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                << 1U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 7U)) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 6U) 
                                                                                | ((0x20U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h26a9e557__0))) 
                                                                                << 5U)) 
                                                                                | ((0x10U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h265c757d__0))) 
                                                                                << 4U)) 
                                                                                | ((8U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h272aca04__0))) 
                                                                                << 3U)) 
                                                                                | ((4U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_he081d797__0))) 
                                                                                << 2U)) 
                                                                                | ((2U 
                                                                                & ((0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_he16c95bc__0))) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (0xcaU 
                                                                                >> 
                                                                                (((IData)(vlSymsp->TOP.wasmetal_core__DOT___000125_) 
                                                                                << 2U) 
                                                                                | (IData)(vlSymsp->TOP.__VdfgTmp_h3a2be217__0))))))))))))))))))))) 
                                                      >> 8U))));
        __Vdlyvval__memory__DOT__words__v1 = vlSelf->memory__DOT____Vlvbound_h252618a2__0;
        __Vdlyvset__memory__DOT__words__v1 = 1U;
        __Vdlyvlsb__memory__DOT__words__v1 = 9U;
        __Vdlyvdim0__memory__DOT__words__v1 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRARDADDR) 
                                                  >> 4U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = (((~ ((IData)(0x1ffU) << (IData)(__Vdlyvlsb__memory__DOT__words__v0))) 
                & vlSelf->__PVT__memory__DOT__words
                [__Vdlyvdim0__memory__DOT__words__v0]) 
               | (0x3ffffU & ((IData)(__Vdlyvval__memory__DOT__words__v0) 
                              << (IData)(__Vdlyvlsb__memory__DOT__words__v0))));
    }
    if (__Vdlyvset__memory__DOT__words__v1) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v1] 
            = (((~ ((IData)(0x1ffU) << (IData)(__Vdlyvlsb__memory__DOT__words__v1))) 
                & vlSelf->__PVT__memory__DOT__words
                [__Vdlyvdim0__memory__DOT__words__v1]) 
               | (0x3ffffU & ((IData)(__Vdlyvval__memory__DOT__words__v1) 
                              << (IData)(__Vdlyvlsb__memory__DOT__words__v1))));
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e6__0(Vwasmetal_core_RAMB36E1__pi5* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e6__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    CData/*4:0*/ __Vdlyvlsb__memory__DOT__words__v0;
    __Vdlyvlsb__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v1;
    __Vdlyvdim0__memory__DOT__words__v1 = 0;
    CData/*4:0*/ __Vdlyvlsb__memory__DOT__words__v1;
    __Vdlyvlsb__memory__DOT__words__v1 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v1;
    __Vdlyvval__memory__DOT__words__v1 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v1;
    __Vdlyvset__memory__DOT__words__v1 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    __Vdlyvset__memory__DOT__words__v1 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000130_))))) {
        vlSelf->memory__DOT____Vlvbound_h252618a2__0 
            = ((0x100U & ((0x200U & ((8U >> ((2U & 
                                              (vlSymsp->TOP.insn_w 
                                               >> 0x1bU)) 
                                             | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                     << 9U)) | (0x100U 
                                                & ((8U 
                                                    >> 
                                                    ((2U 
                                                      & (vlSymsp->TOP.insn_w 
                                                         >> 0x12U)) 
                                                     | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                   << 8U)))) 
               | (0xffU & (IData)((QData)((IData)((
                                                   (0x8000U 
                                                    & ((8U 
                                                        >> 
                                                        ((2U 
                                                          & (vlSymsp->TOP.insn_w 
                                                             >> 0x1aU)) 
                                                         | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                       << 0xfU)) 
                                                   | ((0x4000U 
                                                       & ((8U 
                                                           >> 
                                                           ((2U 
                                                             & (vlSymsp->TOP.insn_w 
                                                                >> 0x19U)) 
                                                            | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                          << 0xeU)) 
                                                      | ((0x2000U 
                                                          & ((8U 
                                                              >> 
                                                              ((2U 
                                                                & (vlSymsp->TOP.insn_w 
                                                                   >> 0x18U)) 
                                                               | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                             << 0xdU)) 
                                                         | ((0x1000U 
                                                             & ((8U 
                                                                 >> 
                                                                 ((2U 
                                                                   & (vlSymsp->TOP.insn_w 
                                                                      >> 0x17U)) 
                                                                  | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                << 0xcU)) 
                                                            | ((0x800U 
                                                                & ((8U 
                                                                    >> 
                                                                    ((2U 
                                                                      & (vlSymsp->TOP.insn_w 
                                                                         >> 0x16U)) 
                                                                     | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                   << 0xbU)) 
                                                               | ((0x400U 
                                                                   & ((8U 
                                                                       >> 
                                                                       ((2U 
                                                                         & (vlSymsp->TOP.insn_w 
                                                                            >> 0x15U)) 
                                                                        | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                      << 0xaU)) 
                                                                  | ((0x200U 
                                                                      & ((8U 
                                                                          >> 
                                                                          ((2U 
                                                                            & (vlSymsp->TOP.insn_w 
                                                                               >> 0x14U)) 
                                                                           | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                         << 9U)) 
                                                                     | ((0x100U 
                                                                         & ((8U 
                                                                             >> 
                                                                             ((2U 
                                                                               & (vlSymsp->TOP.insn_w 
                                                                                >> 0x13U)) 
                                                                              | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                            << 8U)) 
                                                                        | ((0x80U 
                                                                            & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0x11U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                               << 7U)) 
                                                                           | ((0x40U 
                                                                               & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0x10U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 6U)) 
                                                                              | ((0x20U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0xfU)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 5U)) 
                                                                                | ((0x10U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0xeU)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 4U)) 
                                                                                | ((8U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0xdU)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 3U)) 
                                                                                | ((4U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0xcU)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 2U)) 
                                                                                | ((2U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0xbU)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0xaU)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))))))))))))))))))))))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h252618a2__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvlsb__memory__DOT__words__v0 = 0U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRARDADDR) 
                                                  >> 4U));
    }
    if ((2U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000130_))))) {
        vlSelf->memory__DOT____Vlvbound_h252618a2__0 
            = ((0x100U & ((8U >> ((2U & (vlSymsp->TOP.insn_w 
                                         >> 0x1bU)) 
                                  | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                          << 8U)) | (0xffU & (IData)(
                                                     ((QData)((IData)(
                                                                      ((0x8000U 
                                                                        & ((8U 
                                                                            >> 
                                                                            ((2U 
                                                                              & (vlSymsp->TOP.insn_w 
                                                                                >> 0x1aU)) 
                                                                             | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                           << 0xfU)) 
                                                                       | ((0x4000U 
                                                                           & ((8U 
                                                                               >> 
                                                                               ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0x19U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                              << 0xeU)) 
                                                                          | ((0x2000U 
                                                                              & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0x18U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 0xdU)) 
                                                                             | ((0x1000U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0x17U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 0xcU)) 
                                                                                | ((0x800U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0x16U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 0xbU)) 
                                                                                | ((0x400U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0x15U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 0xaU)) 
                                                                                | ((0x200U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0x14U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 9U)) 
                                                                                | ((0x100U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0x13U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 8U)) 
                                                                                | ((0x80U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0x11U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 7U)) 
                                                                                | ((0x40U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0x10U)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 6U)) 
                                                                                | ((0x20U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0xfU)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 5U)) 
                                                                                | ((0x10U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0xeU)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 4U)) 
                                                                                | ((8U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0xdU)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 3U)) 
                                                                                | ((4U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0xcU)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 2U)) 
                                                                                | ((2U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0xbU)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0xaU)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))))))))))))))))))))) 
                                                      >> 8U))));
        __Vdlyvval__memory__DOT__words__v1 = vlSelf->memory__DOT____Vlvbound_h252618a2__0;
        __Vdlyvset__memory__DOT__words__v1 = 1U;
        __Vdlyvlsb__memory__DOT__words__v1 = 9U;
        __Vdlyvdim0__memory__DOT__words__v1 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRARDADDR) 
                                                  >> 4U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = (((~ ((IData)(0x1ffU) << (IData)(__Vdlyvlsb__memory__DOT__words__v0))) 
                & vlSelf->__PVT__memory__DOT__words
                [__Vdlyvdim0__memory__DOT__words__v0]) 
               | (0x3ffffU & ((IData)(__Vdlyvval__memory__DOT__words__v0) 
                              << (IData)(__Vdlyvlsb__memory__DOT__words__v0))));
    }
    if (__Vdlyvset__memory__DOT__words__v1) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v1] 
            = (((~ ((IData)(0x1ffU) << (IData)(__Vdlyvlsb__memory__DOT__words__v1))) 
                & vlSelf->__PVT__memory__DOT__words
                [__Vdlyvdim0__memory__DOT__words__v1]) 
               | (0x3ffffU & ((IData)(__Vdlyvval__memory__DOT__words__v1) 
                              << (IData)(__Vdlyvlsb__memory__DOT__words__v1))));
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e7__0(Vwasmetal_core_RAMB36E1__pi5* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e7__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    CData/*4:0*/ __Vdlyvlsb__memory__DOT__words__v0;
    __Vdlyvlsb__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v1;
    __Vdlyvdim0__memory__DOT__words__v1 = 0;
    CData/*4:0*/ __Vdlyvlsb__memory__DOT__words__v1;
    __Vdlyvlsb__memory__DOT__words__v1 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v1;
    __Vdlyvval__memory__DOT__words__v1 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v1;
    __Vdlyvset__memory__DOT__words__v1 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    __Vdlyvset__memory__DOT__words__v1 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000130_))))) {
        vlSelf->memory__DOT____Vlvbound_h252618a2__0 
            = ((0x100U & ((0xffffff00U & (vlSymsp->TOP.insn_imm[0U] 
                                          << 3U)) | 
                          (0x200U & (vlSymsp->TOP.insn_imm[0U] 
                                     >> 5U)))) | (0xffU 
                                                  & (IData)((QData)((IData)(
                                                                            ((0xff00U 
                                                                              & (vlSymsp->TOP.insn_imm[0U] 
                                                                                << 2U)) 
                                                                             | ((0xf8U 
                                                                                & (vlSymsp->TOP.insn_imm[0U] 
                                                                                << 3U)) 
                                                                                | ((4U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0x1eU)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 2U)) 
                                                                                | ((2U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0x1dU)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0x1cU)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_)))))))))))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h252618a2__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvlsb__memory__DOT__words__v0 = 0U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRARDADDR) 
                                                  >> 4U));
    }
    if ((2U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000130_))))) {
        vlSelf->memory__DOT____Vlvbound_h252618a2__0 
            = ((0x100U & (vlSymsp->TOP.insn_imm[0U] 
                          >> 6U)) | (0xffU & (IData)(
                                                     ((QData)((IData)(
                                                                      ((0xff00U 
                                                                        & (vlSymsp->TOP.insn_imm[0U] 
                                                                           << 2U)) 
                                                                       | ((0xf8U 
                                                                           & (vlSymsp->TOP.insn_imm[0U] 
                                                                              << 3U)) 
                                                                          | ((4U 
                                                                              & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0x1eU)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 2U)) 
                                                                             | ((2U 
                                                                                & ((8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0x1dU)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_))) 
                                                                                << 1U)) 
                                                                                | (1U 
                                                                                & (8U 
                                                                                >> 
                                                                                ((2U 
                                                                                & (vlSymsp->TOP.insn_w 
                                                                                >> 0x1cU)) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT___052851_)))))))))) 
                                                      >> 8U))));
        __Vdlyvval__memory__DOT__words__v1 = vlSelf->memory__DOT____Vlvbound_h252618a2__0;
        __Vdlyvset__memory__DOT__words__v1 = 1U;
        __Vdlyvlsb__memory__DOT__words__v1 = 9U;
        __Vdlyvdim0__memory__DOT__words__v1 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRARDADDR) 
                                                  >> 4U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = (((~ ((IData)(0x1ffU) << (IData)(__Vdlyvlsb__memory__DOT__words__v0))) 
                & vlSelf->__PVT__memory__DOT__words
                [__Vdlyvdim0__memory__DOT__words__v0]) 
               | (0x3ffffU & ((IData)(__Vdlyvval__memory__DOT__words__v0) 
                              << (IData)(__Vdlyvlsb__memory__DOT__words__v0))));
    }
    if (__Vdlyvset__memory__DOT__words__v1) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v1] 
            = (((~ ((IData)(0x1ffU) << (IData)(__Vdlyvlsb__memory__DOT__words__v1))) 
                & vlSelf->__PVT__memory__DOT__words
                [__Vdlyvdim0__memory__DOT__words__v1]) 
               | (0x3ffffU & ((IData)(__Vdlyvval__memory__DOT__words__v1) 
                              << (IData)(__Vdlyvlsb__memory__DOT__words__v1))));
    }
}

VL_INLINE_OPT void Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e8__0(Vwasmetal_core_RAMB36E1__pi5* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB36E1__pi5___nba_sequent__TOP__wasmetal_core__DOT__labels_memory__02e0__02e8__0\n"); );
    // Init
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v0;
    __Vdlyvdim0__memory__DOT__words__v0 = 0;
    CData/*4:0*/ __Vdlyvlsb__memory__DOT__words__v0;
    __Vdlyvlsb__memory__DOT__words__v0 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v0;
    __Vdlyvval__memory__DOT__words__v0 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v0;
    __Vdlyvset__memory__DOT__words__v0 = 0;
    SData/*10:0*/ __Vdlyvdim0__memory__DOT__words__v1;
    __Vdlyvdim0__memory__DOT__words__v1 = 0;
    CData/*4:0*/ __Vdlyvlsb__memory__DOT__words__v1;
    __Vdlyvlsb__memory__DOT__words__v1 = 0;
    SData/*8:0*/ __Vdlyvval__memory__DOT__words__v1;
    __Vdlyvval__memory__DOT__words__v1 = 0;
    CData/*0:0*/ __Vdlyvset__memory__DOT__words__v1;
    __Vdlyvset__memory__DOT__words__v1 = 0;
    // Body
    __Vdlyvset__memory__DOT__words__v0 = 0U;
    __Vdlyvset__memory__DOT__words__v1 = 0U;
    if ((1U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000130_))))) {
        vlSelf->memory__DOT____Vlvbound_h252618a2__0 
            = ((0x100U & (vlSymsp->TOP.insn_imm[0U] 
                          >> 0xfU)) | (0xffU & (IData)((QData)((IData)(
                                                                       ((0xff00U 
                                                                         & (vlSymsp->TOP.insn_imm[0U] 
                                                                            >> 0x10U)) 
                                                                        | (0xffU 
                                                                           & (vlSymsp->TOP.insn_imm[0U] 
                                                                              >> 0xfU))))))));
        __Vdlyvval__memory__DOT__words__v0 = vlSelf->memory__DOT____Vlvbound_h252618a2__0;
        __Vdlyvset__memory__DOT__words__v0 = 1U;
        __Vdlyvlsb__memory__DOT__words__v0 = 0U;
        __Vdlyvdim0__memory__DOT__words__v0 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRARDADDR) 
                                                  >> 4U));
    }
    if ((2U & (- (IData)((IData)(vlSymsp->TOP.wasmetal_core__DOT___000130_))))) {
        vlSelf->memory__DOT____Vlvbound_h252618a2__0 
            = (0xffU & (IData)(((QData)((IData)(((0xff00U 
                                                  & (vlSymsp->TOP.insn_imm[0U] 
                                                     >> 0x10U)) 
                                                 | (0xffU 
                                                    & (vlSymsp->TOP.insn_imm[0U] 
                                                       >> 0xfU))))) 
                                >> 8U)));
        __Vdlyvval__memory__DOT__words__v1 = vlSelf->memory__DOT____Vlvbound_h252618a2__0;
        __Vdlyvset__memory__DOT__words__v1 = 1U;
        __Vdlyvlsb__memory__DOT__words__v1 = 9U;
        __Vdlyvdim0__memory__DOT__words__v1 = (0x7ffU 
                                               & ((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__labels_memory__02e0__02e0__ADDRARDADDR) 
                                                  >> 4U));
    }
    if (__Vdlyvset__memory__DOT__words__v0) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v0] 
            = (((~ ((IData)(0x1ffU) << (IData)(__Vdlyvlsb__memory__DOT__words__v0))) 
                & vlSelf->__PVT__memory__DOT__words
                [__Vdlyvdim0__memory__DOT__words__v0]) 
               | (0x3ffffU & ((IData)(__Vdlyvval__memory__DOT__words__v0) 
                              << (IData)(__Vdlyvlsb__memory__DOT__words__v0))));
    }
    if (__Vdlyvset__memory__DOT__words__v1) {
        vlSelf->__PVT__memory__DOT__words[__Vdlyvdim0__memory__DOT__words__v1] 
            = (((~ ((IData)(0x1ffU) << (IData)(__Vdlyvlsb__memory__DOT__words__v1))) 
                & vlSelf->__PVT__memory__DOT__words
                [__Vdlyvdim0__memory__DOT__words__v1]) 
               | (0x3ffffU & ((IData)(__Vdlyvval__memory__DOT__words__v1) 
                              << (IData)(__Vdlyvlsb__memory__DOT__words__v1))));
    }
}
