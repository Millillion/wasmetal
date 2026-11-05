#pragma GCC diagnostic ignored "-Wint-in-bool-context"
#pragma GCC diagnostic ignored "-Wbool-operation"
#pragma GCC diagnostic ignored "-Wbitwise-instead-of-logical"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vwasmetal_core.h for the primary calling header

#include "Vwasmetal_core__pch.h"
#include "Vwasmetal_core_DSP48E1__pi1.h"
#include "Vwasmetal_core__Syms.h"

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___134220___0(Vwasmetal_core_DSP48E1__pi1* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___134220___0\n"); );
    // Init
    QData/*42:0*/ __PVT__Mr;
    __PVT__Mr = 0;
    QData/*47:0*/ __PVT__X;
    __PVT__X = 0;
    QData/*47:0*/ __PVT__xor_xyz_muxed;
    __PVT__xor_xyz_muxed = 0;
    SData/*12:0*/ __VdfgTmp_h4c2f98f1__0;
    __VdfgTmp_h4c2f98f1__0 = 0;
    SData/*12:0*/ __VdfgTmp_ha5045b21__0;
    __VdfgTmp_ha5045b21__0 = 0;
    // Body
    __PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,25, 
                                                                 (0x1ffffffU 
                                                                  & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134220___A))), 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134220___B))));
    __PVT__X = (0xffffffffffffULL & VL_EXTENDS_QQ(48,43, __PVT__Mr));
    __PVT__xor_xyz_muxed = __PVT__X;
    __VdfgTmp_ha5045b21__0 = (0xfffU & (IData)(__PVT__xor_xyz_muxed));
    __VdfgTmp_h4c2f98f1__0 = (0x1fffU & ((0xfffU & (IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0xcU))) 
                                         + VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_ha5045b21__0), 0xcU)));
    vlSelf->__PVT__alu_sum = (((QData)((IData)((0xfffU 
                                                & ((IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0x24U)) 
                                                   + 
                                                   (1U 
                                                    & (((0xfffU 
                                                         & (IData)(
                                                                   (__PVT__xor_xyz_muxed 
                                                                    >> 0x18U))) 
                                                        + 
                                                        VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_h4c2f98f1__0), 0xcU)) 
                                                       >> 0xcU)))))) 
                               << 0x24U) | (((QData)((IData)(
                                                             (0xfffU 
                                                              & ((IData)(
                                                                         (__PVT__xor_xyz_muxed 
                                                                          >> 0x18U)) 
                                                                 + 
                                                                 (1U 
                                                                  & ((IData)(__VdfgTmp_h4c2f98f1__0) 
                                                                     >> 0xcU)))))) 
                                             << 0x18U) 
                                            | (QData)((IData)(
                                                              ((0xfff000U 
                                                                & (((IData)(
                                                                            (__PVT__xor_xyz_muxed 
                                                                             >> 0xcU)) 
                                                                    + 
                                                                    (1U 
                                                                     & ((IData)(__VdfgTmp_ha5045b21__0) 
                                                                        >> 0xcU))) 
                                                                   << 0xcU)) 
                                                               | (0xfffU 
                                                                  & (IData)(__PVT__xor_xyz_muxed)))))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___134222___0(Vwasmetal_core_DSP48E1__pi1* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___134222___0\n"); );
    // Init
    QData/*42:0*/ __PVT__Mr;
    __PVT__Mr = 0;
    QData/*47:0*/ __PVT__X;
    __PVT__X = 0;
    QData/*47:0*/ __PVT__xor_xyz_muxed;
    __PVT__xor_xyz_muxed = 0;
    SData/*12:0*/ __VdfgTmp_h4c2f98f1__0;
    __VdfgTmp_h4c2f98f1__0 = 0;
    SData/*12:0*/ __VdfgTmp_ha5045b21__0;
    __VdfgTmp_ha5045b21__0 = 0;
    // Body
    __PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,25, 
                                                                 (0x1ffffffU 
                                                                  & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134222___A))), 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134220___B))));
    __PVT__X = (0xffffffffffffULL & VL_EXTENDS_QQ(48,43, __PVT__Mr));
    __PVT__xor_xyz_muxed = __PVT__X;
    __VdfgTmp_ha5045b21__0 = (0xfffU & (IData)(__PVT__xor_xyz_muxed));
    __VdfgTmp_h4c2f98f1__0 = (0x1fffU & ((0xfffU & (IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0xcU))) 
                                         + VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_ha5045b21__0), 0xcU)));
    vlSelf->__PVT__alu_sum = (((QData)((IData)((0xfffU 
                                                & ((IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0x24U)) 
                                                   + 
                                                   (1U 
                                                    & (((0xfffU 
                                                         & (IData)(
                                                                   (__PVT__xor_xyz_muxed 
                                                                    >> 0x18U))) 
                                                        + 
                                                        VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_h4c2f98f1__0), 0xcU)) 
                                                       >> 0xcU)))))) 
                               << 0x24U) | (((QData)((IData)(
                                                             (0xfffU 
                                                              & ((IData)(
                                                                         (__PVT__xor_xyz_muxed 
                                                                          >> 0x18U)) 
                                                                 + 
                                                                 (1U 
                                                                  & ((IData)(__VdfgTmp_h4c2f98f1__0) 
                                                                     >> 0xcU)))))) 
                                             << 0x18U) 
                                            | (QData)((IData)(
                                                              ((0xfff000U 
                                                                & (((IData)(
                                                                            (__PVT__xor_xyz_muxed 
                                                                             >> 0xcU)) 
                                                                    + 
                                                                    (1U 
                                                                     & ((IData)(__VdfgTmp_ha5045b21__0) 
                                                                        >> 0xcU))) 
                                                                   << 0xcU)) 
                                                               | (0xfffU 
                                                                  & (IData)(__PVT__xor_xyz_muxed)))))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___134225___0(Vwasmetal_core_DSP48E1__pi1* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___134225___0\n"); );
    // Init
    QData/*42:0*/ __PVT__Mr;
    __PVT__Mr = 0;
    QData/*47:0*/ __PVT__X;
    __PVT__X = 0;
    QData/*47:0*/ __PVT__xor_xyz_muxed;
    __PVT__xor_xyz_muxed = 0;
    SData/*12:0*/ __VdfgTmp_h4c2f98f1__0;
    __VdfgTmp_h4c2f98f1__0 = 0;
    SData/*12:0*/ __VdfgTmp_ha5045b21__0;
    __VdfgTmp_ha5045b21__0 = 0;
    // Body
    __PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,25, 
                                                                 (0x1ffffffU 
                                                                  & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134225___A))), 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134220___B))));
    __PVT__X = (0xffffffffffffULL & VL_EXTENDS_QQ(48,43, __PVT__Mr));
    __PVT__xor_xyz_muxed = __PVT__X;
    __VdfgTmp_ha5045b21__0 = (0xfffU & (IData)(__PVT__xor_xyz_muxed));
    __VdfgTmp_h4c2f98f1__0 = (0x1fffU & ((0xfffU & (IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0xcU))) 
                                         + VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_ha5045b21__0), 0xcU)));
    vlSelf->__PVT__alu_sum = (((QData)((IData)((0xfffU 
                                                & ((IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0x24U)) 
                                                   + 
                                                   (1U 
                                                    & (((0xfffU 
                                                         & (IData)(
                                                                   (__PVT__xor_xyz_muxed 
                                                                    >> 0x18U))) 
                                                        + 
                                                        VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_h4c2f98f1__0), 0xcU)) 
                                                       >> 0xcU)))))) 
                               << 0x24U) | (((QData)((IData)(
                                                             (0xfffU 
                                                              & ((IData)(
                                                                         (__PVT__xor_xyz_muxed 
                                                                          >> 0x18U)) 
                                                                 + 
                                                                 (1U 
                                                                  & ((IData)(__VdfgTmp_h4c2f98f1__0) 
                                                                     >> 0xcU)))))) 
                                             << 0x18U) 
                                            | (QData)((IData)(
                                                              ((0xfff000U 
                                                                & (((IData)(
                                                                            (__PVT__xor_xyz_muxed 
                                                                             >> 0xcU)) 
                                                                    + 
                                                                    (1U 
                                                                     & ((IData)(__VdfgTmp_ha5045b21__0) 
                                                                        >> 0xcU))) 
                                                                   << 0xcU)) 
                                                               | (0xfffU 
                                                                  & (IData)(__PVT__xor_xyz_muxed)))))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___134228___0(Vwasmetal_core_DSP48E1__pi1* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___134228___0\n"); );
    // Init
    QData/*42:0*/ __PVT__Mr;
    __PVT__Mr = 0;
    QData/*47:0*/ __PVT__X;
    __PVT__X = 0;
    QData/*47:0*/ __PVT__xor_xyz_muxed;
    __PVT__xor_xyz_muxed = 0;
    SData/*12:0*/ __VdfgTmp_h4c2f98f1__0;
    __VdfgTmp_h4c2f98f1__0 = 0;
    SData/*12:0*/ __VdfgTmp_ha5045b21__0;
    __VdfgTmp_ha5045b21__0 = 0;
    // Body
    __PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,25, 
                                                                 (0x1ffffffU 
                                                                  & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134228___A))), 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134220___B))));
    __PVT__X = (0xffffffffffffULL & VL_EXTENDS_QQ(48,43, __PVT__Mr));
    __PVT__xor_xyz_muxed = __PVT__X;
    __VdfgTmp_ha5045b21__0 = (0xfffU & (IData)(__PVT__xor_xyz_muxed));
    __VdfgTmp_h4c2f98f1__0 = (0x1fffU & ((0xfffU & (IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0xcU))) 
                                         + VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_ha5045b21__0), 0xcU)));
    vlSelf->__PVT__alu_sum = (((QData)((IData)((0xfffU 
                                                & ((IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0x24U)) 
                                                   + 
                                                   (1U 
                                                    & (((0xfffU 
                                                         & (IData)(
                                                                   (__PVT__xor_xyz_muxed 
                                                                    >> 0x18U))) 
                                                        + 
                                                        VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_h4c2f98f1__0), 0xcU)) 
                                                       >> 0xcU)))))) 
                               << 0x24U) | (((QData)((IData)(
                                                             (0xfffU 
                                                              & ((IData)(
                                                                         (__PVT__xor_xyz_muxed 
                                                                          >> 0x18U)) 
                                                                 + 
                                                                 (1U 
                                                                  & ((IData)(__VdfgTmp_h4c2f98f1__0) 
                                                                     >> 0xcU)))))) 
                                             << 0x18U) 
                                            | (QData)((IData)(
                                                              ((0xfff000U 
                                                                & (((IData)(
                                                                            (__PVT__xor_xyz_muxed 
                                                                             >> 0xcU)) 
                                                                    + 
                                                                    (1U 
                                                                     & ((IData)(__VdfgTmp_ha5045b21__0) 
                                                                        >> 0xcU))) 
                                                                   << 0xcU)) 
                                                               | (0xfffU 
                                                                  & (IData)(__PVT__xor_xyz_muxed)))))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___134230___0(Vwasmetal_core_DSP48E1__pi1* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___134230___0\n"); );
    // Body
    vlSelf->__PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,25, 
                                                                         (0x1ffffffU 
                                                                          & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134230___A))), 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134230___B))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___134230___1(Vwasmetal_core_DSP48E1__pi1* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___134230___1\n"); );
    // Init
    QData/*47:0*/ __PVT__X;
    __PVT__X = 0;
    QData/*47:0*/ __PVT__Z;
    __PVT__Z = 0;
    QData/*47:0*/ __PVT__maj_xyz;
    __PVT__maj_xyz = 0;
    QData/*47:0*/ __PVT__xor_xyz_muxed;
    __PVT__xor_xyz_muxed = 0;
    SData/*12:0*/ __VdfgTmp_h4c2f98f1__0;
    __VdfgTmp_h4c2f98f1__0 = 0;
    SData/*12:0*/ __VdfgTmp_ha5045b21__0;
    __VdfgTmp_ha5045b21__0 = 0;
    // Body
    __PVT__X = (0xffffffffffffULL & VL_EXTENDS_QQ(48,43, vlSelf->__PVT__Mr));
    __PVT__Z = (((QData)((IData)((0xfffU & ((IData)(
                                                    (vlSymsp->TOP__wasmetal_core__DOT___134231_.__PVT__maj_xyz 
                                                     >> 0x23U)) 
                                            + ((IData)(
                                                       (vlSymsp->TOP__wasmetal_core__DOT___134231_.__PVT__xor_xyz_muxed 
                                                        >> 0x24U)) 
                                               + (1U 
                                                  & (((0xfffU 
                                                       & (IData)(
                                                                 (vlSymsp->TOP__wasmetal_core__DOT___134231_.__PVT__maj_xyz 
                                                                  >> 0x17U))) 
                                                      + 
                                                      ((0xfffU 
                                                        & (IData)(
                                                                  (vlSymsp->TOP__wasmetal_core__DOT___134231_.__PVT__xor_xyz_muxed 
                                                                   >> 0x18U))) 
                                                       + 
                                                       VL_SHIFTR_III(13,13,32, (IData)(vlSymsp->TOP__wasmetal_core__DOT___134231_.__VdfgTmp_h4c2f98f1__0), 0xcU))) 
                                                     >> 0xcU))))))) 
                 << 0x24U) | (((QData)((IData)((0xfffU 
                                                & ((IData)(
                                                           (vlSymsp->TOP__wasmetal_core__DOT___134231_.__PVT__maj_xyz 
                                                            >> 0x17U)) 
                                                   + 
                                                   ((IData)(
                                                            (vlSymsp->TOP__wasmetal_core__DOT___134231_.__PVT__xor_xyz_muxed 
                                                             >> 0x18U)) 
                                                    + 
                                                    (1U 
                                                     & ((IData)(vlSymsp->TOP__wasmetal_core__DOT___134231_.__VdfgTmp_h4c2f98f1__0) 
                                                        >> 0xcU))))))) 
                               << 0x18U) | (QData)((IData)(
                                                           ((0xfff000U 
                                                             & (((IData)(
                                                                         (vlSymsp->TOP__wasmetal_core__DOT___134231_.__PVT__maj_xyz 
                                                                          >> 0xbU)) 
                                                                 + 
                                                                 ((IData)(
                                                                          (vlSymsp->TOP__wasmetal_core__DOT___134231_.__PVT__xor_xyz_muxed 
                                                                           >> 0xcU)) 
                                                                  + 
                                                                  (1U 
                                                                   & ((IData)(vlSymsp->TOP__wasmetal_core__DOT___134231_.__VdfgTmp_ha5045b21__0) 
                                                                      >> 0xcU)))) 
                                                                << 0xcU)) 
                                                            | (0xfffU 
                                                               & ((0xffeU 
                                                                   & ((IData)(vlSymsp->TOP__wasmetal_core__DOT___134231_.__PVT__maj_xyz) 
                                                                      << 1U)) 
                                                                  + (IData)(vlSymsp->TOP__wasmetal_core__DOT___134231_.__PVT__xor_xyz_muxed))))))));
    __PVT__maj_xyz = (__PVT__X & __PVT__Z);
    __PVT__xor_xyz_muxed = (__PVT__X ^ __PVT__Z);
    __VdfgTmp_ha5045b21__0 = (0x1fffU & ((0xffeU & 
                                          ((IData)(__PVT__maj_xyz) 
                                           << 1U)) 
                                         + (0xfffU 
                                            & (IData)(__PVT__xor_xyz_muxed))));
    __VdfgTmp_h4c2f98f1__0 = (0x1fffU & ((0xfffU & (IData)(
                                                           (__PVT__maj_xyz 
                                                            >> 0xbU))) 
                                         + ((0xfffU 
                                             & (IData)(
                                                       (__PVT__xor_xyz_muxed 
                                                        >> 0xcU))) 
                                            + VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_ha5045b21__0), 0xcU))));
    vlSelf->__PVT__alu_sum = (((QData)((IData)((0xfffU 
                                                & ((IData)(
                                                           (__PVT__maj_xyz 
                                                            >> 0x23U)) 
                                                   + 
                                                   ((IData)(
                                                            (__PVT__xor_xyz_muxed 
                                                             >> 0x24U)) 
                                                    + 
                                                    (1U 
                                                     & (((0xfffU 
                                                          & (IData)(
                                                                    (__PVT__maj_xyz 
                                                                     >> 0x17U))) 
                                                         + 
                                                         ((0xfffU 
                                                           & (IData)(
                                                                     (__PVT__xor_xyz_muxed 
                                                                      >> 0x18U))) 
                                                          + 
                                                          VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_h4c2f98f1__0), 0xcU))) 
                                                        >> 0xcU))))))) 
                               << 0x24U) | (((QData)((IData)(
                                                             (0xfffU 
                                                              & ((IData)(
                                                                         (__PVT__maj_xyz 
                                                                          >> 0x17U)) 
                                                                 + 
                                                                 ((IData)(
                                                                          (__PVT__xor_xyz_muxed 
                                                                           >> 0x18U)) 
                                                                  + 
                                                                  (1U 
                                                                   & ((IData)(__VdfgTmp_h4c2f98f1__0) 
                                                                      >> 0xcU))))))) 
                                             << 0x18U) 
                                            | (QData)((IData)(
                                                              ((0xfff000U 
                                                                & (((IData)(
                                                                            (__PVT__maj_xyz 
                                                                             >> 0xbU)) 
                                                                    + 
                                                                    ((IData)(
                                                                             (__PVT__xor_xyz_muxed 
                                                                              >> 0xcU)) 
                                                                     + 
                                                                     (1U 
                                                                      & ((IData)(__VdfgTmp_ha5045b21__0) 
                                                                         >> 0xcU)))) 
                                                                   << 0xcU)) 
                                                               | (0xfffU 
                                                                  & ((0xffeU 
                                                                      & ((IData)(__PVT__maj_xyz) 
                                                                         << 1U)) 
                                                                     + (IData)(__PVT__xor_xyz_muxed))))))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___134232___0(Vwasmetal_core_DSP48E1__pi1* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___134232___0\n"); );
    // Init
    QData/*42:0*/ __PVT__Mr;
    __PVT__Mr = 0;
    QData/*47:0*/ __PVT__X;
    __PVT__X = 0;
    QData/*47:0*/ __PVT__xor_xyz_muxed;
    __PVT__xor_xyz_muxed = 0;
    SData/*12:0*/ __VdfgTmp_h4c2f98f1__0;
    __VdfgTmp_h4c2f98f1__0 = 0;
    SData/*12:0*/ __VdfgTmp_ha5045b21__0;
    __VdfgTmp_ha5045b21__0 = 0;
    // Body
    __PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,25, 
                                                                 (0x1ffffffU 
                                                                  & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134232___A))), 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134230___B))));
    __PVT__X = (0xffffffffffffULL & VL_EXTENDS_QQ(48,43, __PVT__Mr));
    __PVT__xor_xyz_muxed = __PVT__X;
    __VdfgTmp_ha5045b21__0 = (0xfffU & (IData)(__PVT__xor_xyz_muxed));
    __VdfgTmp_h4c2f98f1__0 = (0x1fffU & ((0xfffU & (IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0xcU))) 
                                         + VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_ha5045b21__0), 0xcU)));
    vlSelf->__PVT__alu_sum = (((QData)((IData)((0xfffU 
                                                & ((IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0x24U)) 
                                                   + 
                                                   (1U 
                                                    & (((0xfffU 
                                                         & (IData)(
                                                                   (__PVT__xor_xyz_muxed 
                                                                    >> 0x18U))) 
                                                        + 
                                                        VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_h4c2f98f1__0), 0xcU)) 
                                                       >> 0xcU)))))) 
                               << 0x24U) | (((QData)((IData)(
                                                             (0xfffU 
                                                              & ((IData)(
                                                                         (__PVT__xor_xyz_muxed 
                                                                          >> 0x18U)) 
                                                                 + 
                                                                 (1U 
                                                                  & ((IData)(__VdfgTmp_h4c2f98f1__0) 
                                                                     >> 0xcU)))))) 
                                             << 0x18U) 
                                            | (QData)((IData)(
                                                              ((0xfff000U 
                                                                & (((IData)(
                                                                            (__PVT__xor_xyz_muxed 
                                                                             >> 0xcU)) 
                                                                    + 
                                                                    (1U 
                                                                     & ((IData)(__VdfgTmp_ha5045b21__0) 
                                                                        >> 0xcU))) 
                                                                   << 0xcU)) 
                                                               | (0xfffU 
                                                                  & (IData)(__PVT__xor_xyz_muxed)))))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___135065___0(Vwasmetal_core_DSP48E1__pi1* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___135065___0\n"); );
    // Init
    QData/*42:0*/ __PVT__Mr;
    __PVT__Mr = 0;
    QData/*47:0*/ __PVT__X;
    __PVT__X = 0;
    QData/*47:0*/ __PVT__xor_xyz_muxed;
    __PVT__xor_xyz_muxed = 0;
    SData/*12:0*/ __VdfgTmp_h4c2f98f1__0;
    __VdfgTmp_h4c2f98f1__0 = 0;
    SData/*12:0*/ __VdfgTmp_ha5045b21__0;
    __VdfgTmp_ha5045b21__0 = 0;
    // Body
    __PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,25, 
                                                                 (0x1ffffffU 
                                                                  & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135065___A))), 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135065___B))));
    __PVT__X = (0xffffffffffffULL & VL_EXTENDS_QQ(48,43, __PVT__Mr));
    __PVT__xor_xyz_muxed = __PVT__X;
    __VdfgTmp_ha5045b21__0 = (0xfffU & (IData)(__PVT__xor_xyz_muxed));
    __VdfgTmp_h4c2f98f1__0 = (0x1fffU & ((0xfffU & (IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0xcU))) 
                                         + VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_ha5045b21__0), 0xcU)));
    vlSelf->__PVT__alu_sum = (((QData)((IData)((0xfffU 
                                                & ((IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0x24U)) 
                                                   + 
                                                   (1U 
                                                    & (((0xfffU 
                                                         & (IData)(
                                                                   (__PVT__xor_xyz_muxed 
                                                                    >> 0x18U))) 
                                                        + 
                                                        VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_h4c2f98f1__0), 0xcU)) 
                                                       >> 0xcU)))))) 
                               << 0x24U) | (((QData)((IData)(
                                                             (0xfffU 
                                                              & ((IData)(
                                                                         (__PVT__xor_xyz_muxed 
                                                                          >> 0x18U)) 
                                                                 + 
                                                                 (1U 
                                                                  & ((IData)(__VdfgTmp_h4c2f98f1__0) 
                                                                     >> 0xcU)))))) 
                                             << 0x18U) 
                                            | (QData)((IData)(
                                                              ((0xfff000U 
                                                                & (((IData)(
                                                                            (__PVT__xor_xyz_muxed 
                                                                             >> 0xcU)) 
                                                                    + 
                                                                    (1U 
                                                                     & ((IData)(__VdfgTmp_ha5045b21__0) 
                                                                        >> 0xcU))) 
                                                                   << 0xcU)) 
                                                               | (0xfffU 
                                                                  & (IData)(__PVT__xor_xyz_muxed)))))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___135069___0(Vwasmetal_core_DSP48E1__pi1* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___135069___0\n"); );
    // Init
    QData/*42:0*/ __PVT__Mr;
    __PVT__Mr = 0;
    QData/*47:0*/ __PVT__X;
    __PVT__X = 0;
    QData/*47:0*/ __PVT__xor_xyz_muxed;
    __PVT__xor_xyz_muxed = 0;
    SData/*12:0*/ __VdfgTmp_h4c2f98f1__0;
    __VdfgTmp_h4c2f98f1__0 = 0;
    SData/*12:0*/ __VdfgTmp_ha5045b21__0;
    __VdfgTmp_ha5045b21__0 = 0;
    // Body
    __PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,25, 
                                                                 (0x1ffffffU 
                                                                  & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135069___A))), 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135065___B))));
    __PVT__X = (0xffffffffffffULL & VL_EXTENDS_QQ(48,43, __PVT__Mr));
    __PVT__xor_xyz_muxed = __PVT__X;
    __VdfgTmp_ha5045b21__0 = (0xfffU & (IData)(__PVT__xor_xyz_muxed));
    __VdfgTmp_h4c2f98f1__0 = (0x1fffU & ((0xfffU & (IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0xcU))) 
                                         + VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_ha5045b21__0), 0xcU)));
    vlSelf->__PVT__alu_sum = (((QData)((IData)((0xfffU 
                                                & ((IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0x24U)) 
                                                   + 
                                                   (1U 
                                                    & (((0xfffU 
                                                         & (IData)(
                                                                   (__PVT__xor_xyz_muxed 
                                                                    >> 0x18U))) 
                                                        + 
                                                        VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_h4c2f98f1__0), 0xcU)) 
                                                       >> 0xcU)))))) 
                               << 0x24U) | (((QData)((IData)(
                                                             (0xfffU 
                                                              & ((IData)(
                                                                         (__PVT__xor_xyz_muxed 
                                                                          >> 0x18U)) 
                                                                 + 
                                                                 (1U 
                                                                  & ((IData)(__VdfgTmp_h4c2f98f1__0) 
                                                                     >> 0xcU)))))) 
                                             << 0x18U) 
                                            | (QData)((IData)(
                                                              ((0xfff000U 
                                                                & (((IData)(
                                                                            (__PVT__xor_xyz_muxed 
                                                                             >> 0xcU)) 
                                                                    + 
                                                                    (1U 
                                                                     & ((IData)(__VdfgTmp_ha5045b21__0) 
                                                                        >> 0xcU))) 
                                                                   << 0xcU)) 
                                                               | (0xfffU 
                                                                  & (IData)(__PVT__xor_xyz_muxed)))))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___135073___0(Vwasmetal_core_DSP48E1__pi1* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___135073___0\n"); );
    // Init
    QData/*42:0*/ __PVT__Mr;
    __PVT__Mr = 0;
    QData/*47:0*/ __PVT__X;
    __PVT__X = 0;
    QData/*47:0*/ __PVT__xor_xyz_muxed;
    __PVT__xor_xyz_muxed = 0;
    SData/*12:0*/ __VdfgTmp_h4c2f98f1__0;
    __VdfgTmp_h4c2f98f1__0 = 0;
    SData/*12:0*/ __VdfgTmp_ha5045b21__0;
    __VdfgTmp_ha5045b21__0 = 0;
    // Body
    __PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,25, 
                                                                 (0x1ffffffU 
                                                                  & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135073___A))), 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135065___B))));
    __PVT__X = (0xffffffffffffULL & VL_EXTENDS_QQ(48,43, __PVT__Mr));
    __PVT__xor_xyz_muxed = __PVT__X;
    __VdfgTmp_ha5045b21__0 = (0xfffU & (IData)(__PVT__xor_xyz_muxed));
    __VdfgTmp_h4c2f98f1__0 = (0x1fffU & ((0xfffU & (IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0xcU))) 
                                         + VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_ha5045b21__0), 0xcU)));
    vlSelf->__PVT__alu_sum = (((QData)((IData)((0xfffU 
                                                & ((IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0x24U)) 
                                                   + 
                                                   (1U 
                                                    & (((0xfffU 
                                                         & (IData)(
                                                                   (__PVT__xor_xyz_muxed 
                                                                    >> 0x18U))) 
                                                        + 
                                                        VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_h4c2f98f1__0), 0xcU)) 
                                                       >> 0xcU)))))) 
                               << 0x24U) | (((QData)((IData)(
                                                             (0xfffU 
                                                              & ((IData)(
                                                                         (__PVT__xor_xyz_muxed 
                                                                          >> 0x18U)) 
                                                                 + 
                                                                 (1U 
                                                                  & ((IData)(__VdfgTmp_h4c2f98f1__0) 
                                                                     >> 0xcU)))))) 
                                             << 0x18U) 
                                            | (QData)((IData)(
                                                              ((0xfff000U 
                                                                & (((IData)(
                                                                            (__PVT__xor_xyz_muxed 
                                                                             >> 0xcU)) 
                                                                    + 
                                                                    (1U 
                                                                     & ((IData)(__VdfgTmp_ha5045b21__0) 
                                                                        >> 0xcU))) 
                                                                   << 0xcU)) 
                                                               | (0xfffU 
                                                                  & (IData)(__PVT__xor_xyz_muxed)))))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___135195___0(Vwasmetal_core_DSP48E1__pi1* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___135195___0\n"); );
    // Body
    vlSelf->__PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,25, 
                                                                         (0x1ffffffU 
                                                                          & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135195___A))), 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135195___B))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___135195___1(Vwasmetal_core_DSP48E1__pi1* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___135195___1\n"); );
    // Init
    QData/*47:0*/ __PVT__X;
    __PVT__X = 0;
    QData/*47:0*/ __PVT__Z;
    __PVT__Z = 0;
    QData/*47:0*/ __PVT__maj_xyz;
    __PVT__maj_xyz = 0;
    QData/*47:0*/ __PVT__xor_xyz_muxed;
    __PVT__xor_xyz_muxed = 0;
    SData/*12:0*/ __VdfgTmp_h4c2f98f1__0;
    __VdfgTmp_h4c2f98f1__0 = 0;
    SData/*12:0*/ __VdfgTmp_ha5045b21__0;
    __VdfgTmp_ha5045b21__0 = 0;
    // Body
    __PVT__X = (0xffffffffffffULL & VL_EXTENDS_QQ(48,43, vlSelf->__PVT__Mr));
    __PVT__Z = (((QData)((IData)((0x7fffU & (- (IData)(
                                                       (1U 
                                                        & (IData)(
                                                                  (vlSymsp->TOP__wasmetal_core__DOT___134230_.__PVT__alu_sum 
                                                                   >> 0x10U)))))))) 
                 << 0x21U) | (((QData)((IData)((0xffffU 
                                                & (IData)(vlSymsp->TOP__wasmetal_core__DOT___134230_.__PVT__alu_sum)))) 
                               << 0x11U) | (QData)((IData)(
                                                           (0x1ffffU 
                                                            & (IData)(vlSymsp->TOP__wasmetal_core__DOT___134232_.__PVT__alu_sum))))));
    __PVT__maj_xyz = (__PVT__X & __PVT__Z);
    __PVT__xor_xyz_muxed = (__PVT__X ^ __PVT__Z);
    __VdfgTmp_ha5045b21__0 = (0x1fffU & ((0xffeU & 
                                          ((IData)(__PVT__maj_xyz) 
                                           << 1U)) 
                                         + (0xfffU 
                                            & (IData)(__PVT__xor_xyz_muxed))));
    __VdfgTmp_h4c2f98f1__0 = (0x1fffU & ((0xfffU & (IData)(
                                                           (__PVT__maj_xyz 
                                                            >> 0xbU))) 
                                         + ((0xfffU 
                                             & (IData)(
                                                       (__PVT__xor_xyz_muxed 
                                                        >> 0xcU))) 
                                            + VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_ha5045b21__0), 0xcU))));
    vlSelf->__PVT__alu_sum = (((QData)((IData)((0xfffU 
                                                & ((IData)(
                                                           (__PVT__maj_xyz 
                                                            >> 0x23U)) 
                                                   + 
                                                   ((IData)(
                                                            (__PVT__xor_xyz_muxed 
                                                             >> 0x24U)) 
                                                    + 
                                                    (1U 
                                                     & (((0xfffU 
                                                          & (IData)(
                                                                    (__PVT__maj_xyz 
                                                                     >> 0x17U))) 
                                                         + 
                                                         ((0xfffU 
                                                           & (IData)(
                                                                     (__PVT__xor_xyz_muxed 
                                                                      >> 0x18U))) 
                                                          + 
                                                          VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_h4c2f98f1__0), 0xcU))) 
                                                        >> 0xcU))))))) 
                               << 0x24U) | (((QData)((IData)(
                                                             (0xfffU 
                                                              & ((IData)(
                                                                         (__PVT__maj_xyz 
                                                                          >> 0x17U)) 
                                                                 + 
                                                                 ((IData)(
                                                                          (__PVT__xor_xyz_muxed 
                                                                           >> 0x18U)) 
                                                                  + 
                                                                  (1U 
                                                                   & ((IData)(__VdfgTmp_h4c2f98f1__0) 
                                                                      >> 0xcU))))))) 
                                             << 0x18U) 
                                            | (QData)((IData)(
                                                              ((0xfff000U 
                                                                & (((IData)(
                                                                            (__PVT__maj_xyz 
                                                                             >> 0xbU)) 
                                                                    + 
                                                                    ((IData)(
                                                                             (__PVT__xor_xyz_muxed 
                                                                              >> 0xcU)) 
                                                                     + 
                                                                     (1U 
                                                                      & ((IData)(__VdfgTmp_ha5045b21__0) 
                                                                         >> 0xcU)))) 
                                                                   << 0xcU)) 
                                                               | (0xfffU 
                                                                  & ((0xffeU 
                                                                      & ((IData)(__PVT__maj_xyz) 
                                                                         << 1U)) 
                                                                     + (IData)(__PVT__xor_xyz_muxed))))))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___135196___0(Vwasmetal_core_DSP48E1__pi1* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___135196___0\n"); );
    // Init
    QData/*42:0*/ __PVT__Mr;
    __PVT__Mr = 0;
    QData/*47:0*/ __PVT__X;
    __PVT__X = 0;
    QData/*47:0*/ __PVT__xor_xyz_muxed;
    __PVT__xor_xyz_muxed = 0;
    SData/*12:0*/ __VdfgTmp_h4c2f98f1__0;
    __VdfgTmp_h4c2f98f1__0 = 0;
    SData/*12:0*/ __VdfgTmp_ha5045b21__0;
    __VdfgTmp_ha5045b21__0 = 0;
    // Body
    __PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,25, 
                                                                 (0x1ffffffU 
                                                                  & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135196___A))), 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135196___B))));
    __PVT__X = (0xffffffffffffULL & VL_EXTENDS_QQ(48,43, __PVT__Mr));
    __PVT__xor_xyz_muxed = __PVT__X;
    __VdfgTmp_ha5045b21__0 = (0xfffU & (IData)(__PVT__xor_xyz_muxed));
    __VdfgTmp_h4c2f98f1__0 = (0x1fffU & ((0xfffU & (IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0xcU))) 
                                         + VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_ha5045b21__0), 0xcU)));
    vlSelf->__PVT__alu_sum = (((QData)((IData)((0xfffU 
                                                & ((IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0x24U)) 
                                                   + 
                                                   (1U 
                                                    & (((0xfffU 
                                                         & (IData)(
                                                                   (__PVT__xor_xyz_muxed 
                                                                    >> 0x18U))) 
                                                        + 
                                                        VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_h4c2f98f1__0), 0xcU)) 
                                                       >> 0xcU)))))) 
                               << 0x24U) | (((QData)((IData)(
                                                             (0xfffU 
                                                              & ((IData)(
                                                                         (__PVT__xor_xyz_muxed 
                                                                          >> 0x18U)) 
                                                                 + 
                                                                 (1U 
                                                                  & ((IData)(__VdfgTmp_h4c2f98f1__0) 
                                                                     >> 0xcU)))))) 
                                             << 0x18U) 
                                            | (QData)((IData)(
                                                              ((0xfff000U 
                                                                & (((IData)(
                                                                            (__PVT__xor_xyz_muxed 
                                                                             >> 0xcU)) 
                                                                    + 
                                                                    (1U 
                                                                     & ((IData)(__VdfgTmp_ha5045b21__0) 
                                                                        >> 0xcU))) 
                                                                   << 0xcU)) 
                                                               | (0xfffU 
                                                                  & (IData)(__PVT__xor_xyz_muxed)))))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___135426___0(Vwasmetal_core_DSP48E1__pi1* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi1___ico_sequent__TOP__wasmetal_core__DOT___135426___0\n"); );
    // Init
    QData/*42:0*/ __PVT__Mr;
    __PVT__Mr = 0;
    QData/*47:0*/ __PVT__X;
    __PVT__X = 0;
    QData/*47:0*/ __PVT__xor_xyz_muxed;
    __PVT__xor_xyz_muxed = 0;
    SData/*12:0*/ __VdfgTmp_h4c2f98f1__0;
    __VdfgTmp_h4c2f98f1__0 = 0;
    SData/*12:0*/ __VdfgTmp_ha5045b21__0;
    __VdfgTmp_ha5045b21__0 = 0;
    // Body
    __PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,25, 
                                                                 (0x1ffffU 
                                                                  & vlSymsp->TOP.insn_y))), 
                                                (0x7ffffffffffULL 
                                                 & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135426___B))));
    __PVT__X = (0xffffffffffffULL & VL_EXTENDS_QQ(48,43, __PVT__Mr));
    __PVT__xor_xyz_muxed = __PVT__X;
    __VdfgTmp_ha5045b21__0 = (0xfffU & (IData)(__PVT__xor_xyz_muxed));
    __VdfgTmp_h4c2f98f1__0 = (0x1fffU & ((0xfffU & (IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0xcU))) 
                                         + VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_ha5045b21__0), 0xcU)));
    vlSelf->__PVT__alu_sum = (((QData)((IData)((0xfffU 
                                                & ((IData)(
                                                           (__PVT__xor_xyz_muxed 
                                                            >> 0x24U)) 
                                                   + 
                                                   (1U 
                                                    & (((0xfffU 
                                                         & (IData)(
                                                                   (__PVT__xor_xyz_muxed 
                                                                    >> 0x18U))) 
                                                        + 
                                                        VL_SHIFTR_III(13,13,32, (IData)(__VdfgTmp_h4c2f98f1__0), 0xcU)) 
                                                       >> 0xcU)))))) 
                               << 0x24U) | (((QData)((IData)(
                                                             (0xfffU 
                                                              & ((IData)(
                                                                         (__PVT__xor_xyz_muxed 
                                                                          >> 0x18U)) 
                                                                 + 
                                                                 (1U 
                                                                  & ((IData)(__VdfgTmp_h4c2f98f1__0) 
                                                                     >> 0xcU)))))) 
                                             << 0x18U) 
                                            | (QData)((IData)(
                                                              ((0xfff000U 
                                                                & (((IData)(
                                                                            (__PVT__xor_xyz_muxed 
                                                                             >> 0xcU)) 
                                                                    + 
                                                                    (1U 
                                                                     & ((IData)(__VdfgTmp_ha5045b21__0) 
                                                                        >> 0xcU))) 
                                                                   << 0xcU)) 
                                                               | (0xfffU 
                                                                  & (IData)(__PVT__xor_xyz_muxed)))))));
}
