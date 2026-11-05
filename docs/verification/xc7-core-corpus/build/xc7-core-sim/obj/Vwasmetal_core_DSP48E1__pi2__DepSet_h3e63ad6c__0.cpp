#pragma GCC diagnostic ignored "-Wint-in-bool-context"
#pragma GCC diagnostic ignored "-Wbool-operation"
#pragma GCC diagnostic ignored "-Wbitwise-instead-of-logical"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vwasmetal_core.h for the primary calling header

#include "Vwasmetal_core__pch.h"
#include "Vwasmetal_core_DSP48E1__pi2.h"
#include "Vwasmetal_core__Syms.h"

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134221___0(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134221___0\n"); );
    // Body
    vlSelf->__PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,25, 
                                                                         (0x1ffffffU 
                                                                          & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134222___A))), 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134221___B))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134221___1(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134221___1\n"); );
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
    __PVT__Z = (0xffffffffffffULL & VL_EXTENDS_QI(48,31, 
                                                  (0x7fffffffU 
                                                   & (IData)(
                                                             (vlSymsp->TOP__wasmetal_core__DOT___134224_.__PVT__alu_sum 
                                                              >> 0x11U)))));
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

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134223___0(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134223___0\n"); );
    // Body
    vlSelf->__PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,25, 
                                                                         (0x1ffffffU 
                                                                          & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134222___A))), 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134223___B))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134223___1(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134223___1\n"); );
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
    __PVT__Z = (0xffffffffffffULL & VL_EXTENDS_QI(48,31, 
                                                  (0x7fffffffU 
                                                   & (IData)(
                                                             (vlSymsp->TOP__wasmetal_core__DOT___134222_.__PVT__alu_sum 
                                                              >> 0x11U)))));
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

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134224___0(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134224___0\n"); );
    // Body
    vlSelf->__PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,25, 
                                                                         (0x1ffffffU 
                                                                          & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134222___A))), 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134224___B))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134224___1(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134224___1\n"); );
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
    __PVT__Z = (0xffffffffffffULL & VL_EXTENDS_QI(48,31, 
                                                  (0x7fffffffU 
                                                   & (IData)(
                                                             (vlSymsp->TOP__wasmetal_core__DOT___134223_.__PVT__alu_sum 
                                                              >> 0x11U)))));
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

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134226___0(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134226___0\n"); );
    // Body
    vlSelf->__PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,25, 
                                                                         (0x1ffffffU 
                                                                          & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134225___A))), 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134223___B))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134226___1(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134226___1\n"); );
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
    __PVT__Z = (0xffffffffffffULL & VL_EXTENDS_QI(48,31, 
                                                  (0x7fffffffU 
                                                   & (IData)(
                                                             (vlSymsp->TOP__wasmetal_core__DOT___134225_.__PVT__alu_sum 
                                                              >> 0x11U)))));
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

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134227___0(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134227___0\n"); );
    // Body
    vlSelf->__PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,25, 
                                                                         (0x1ffffffU 
                                                                          & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134225___A))), 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134224___B))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134227___1(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134227___1\n"); );
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
    __PVT__Z = (0xffffffffffffULL & VL_EXTENDS_QI(48,31, 
                                                  (0x7fffffffU 
                                                   & (IData)(
                                                             (vlSymsp->TOP__wasmetal_core__DOT___134226_.__PVT__alu_sum 
                                                              >> 0x11U)))));
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

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134229___0(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134229___0\n"); );
    // Body
    vlSelf->__PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,25, 
                                                                         (0x1ffffffU 
                                                                          & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134228___A))), 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134223___B))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134229___1(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134229___1\n"); );
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
    __PVT__Z = (0xffffffffffffULL & VL_EXTENDS_QI(48,31, 
                                                  (0x7fffffffU 
                                                   & (IData)(
                                                             (vlSymsp->TOP__wasmetal_core__DOT___134228_.__PVT__alu_sum 
                                                              >> 0x11U)))));
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

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134231___0(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134231___0\n"); );
    // Body
    vlSelf->__PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,25, 
                                                                         (0x1ffffffU 
                                                                          & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134232___A))), 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___134231___B))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134231___1(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___134231___1\n"); );
    // Init
    QData/*47:0*/ __PVT__X;
    __PVT__X = 0;
    QData/*47:0*/ __PVT__Z;
    __PVT__Z = 0;
    // Body
    __PVT__X = (0xffffffffffffULL & VL_EXTENDS_QQ(48,43, vlSelf->__PVT__Mr));
    __PVT__Z = (0xffffffffffffULL & VL_EXTENDS_QI(48,31, 
                                                  (0x7fffffffU 
                                                   & (IData)(
                                                             (vlSymsp->TOP__wasmetal_core__DOT___134232_.__PVT__alu_sum 
                                                              >> 0x11U)))));
    vlSelf->__PVT__maj_xyz = (__PVT__X & __PVT__Z);
    vlSelf->__PVT__xor_xyz_muxed = (__PVT__X ^ __PVT__Z);
    vlSelf->__VdfgTmp_ha5045b21__0 = (0x1fffU & ((0xffeU 
                                                  & ((IData)(vlSelf->__PVT__maj_xyz) 
                                                     << 1U)) 
                                                 + 
                                                 (0xfffU 
                                                  & (IData)(vlSelf->__PVT__xor_xyz_muxed))));
    vlSelf->__VdfgTmp_h4c2f98f1__0 = (0x1fffU & ((0xfffU 
                                                  & (IData)(
                                                            (vlSelf->__PVT__maj_xyz 
                                                             >> 0xbU))) 
                                                 + 
                                                 ((0xfffU 
                                                   & (IData)(
                                                             (vlSelf->__PVT__xor_xyz_muxed 
                                                              >> 0xcU))) 
                                                  + 
                                                  VL_SHIFTR_III(13,13,32, (IData)(vlSelf->__VdfgTmp_ha5045b21__0), 0xcU))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135064___0(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135064___0\n"); );
    // Body
    vlSelf->__PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,25, 
                                                                         (0x1ffffffU 
                                                                          & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135065___A))), 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135064___B))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135064___1(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135064___1\n"); );
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
    __PVT__Z = (0xffffffffffffULL & VL_EXTENDS_QI(48,31, 
                                                  (0x7fffffffU 
                                                   & (IData)(
                                                             (vlSymsp->TOP__wasmetal_core__DOT___135067_.__PVT__alu_sum 
                                                              >> 0x11U)))));
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

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135066___0(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135066___0\n"); );
    // Body
    vlSelf->__PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,25, 
                                                                         (0x1ffffffU 
                                                                          & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135065___A))), 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135066___B))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135066___1(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135066___1\n"); );
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
    __PVT__Z = (0xffffffffffffULL & VL_EXTENDS_QI(48,31, 
                                                  (0x7fffffffU 
                                                   & (IData)(
                                                             (vlSymsp->TOP__wasmetal_core__DOT___135065_.__PVT__alu_sum 
                                                              >> 0x11U)))));
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

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135067___0(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135067___0\n"); );
    // Body
    vlSelf->__PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,25, 
                                                                         (0x1ffffffU 
                                                                          & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135065___A))), 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135067___B))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135067___1(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135067___1\n"); );
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
    __PVT__Z = (0xffffffffffffULL & VL_EXTENDS_QI(48,31, 
                                                  (0x7fffffffU 
                                                   & (IData)(
                                                             (vlSymsp->TOP__wasmetal_core__DOT___135066_.__PVT__alu_sum 
                                                              >> 0x11U)))));
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

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135068___0(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135068___0\n"); );
    // Body
    vlSelf->__PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,25, 
                                                                         (0x1ffffffU 
                                                                          & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135069___A))), 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135064___B))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135068___1(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135068___1\n"); );
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
    __PVT__Z = (0xffffffffffffULL & VL_EXTENDS_QI(48,31, 
                                                  (0x7fffffffU 
                                                   & (IData)(
                                                             (vlSymsp->TOP__wasmetal_core__DOT___135071_.__PVT__alu_sum 
                                                              >> 0x11U)))));
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

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135070___0(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135070___0\n"); );
    // Body
    vlSelf->__PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,25, 
                                                                         (0x1ffffffU 
                                                                          & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135069___A))), 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135066___B))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135070___1(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135070___1\n"); );
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
    __PVT__Z = (0xffffffffffffULL & VL_EXTENDS_QI(48,31, 
                                                  (0x7fffffffU 
                                                   & (IData)(
                                                             (vlSymsp->TOP__wasmetal_core__DOT___135069_.__PVT__alu_sum 
                                                              >> 0x11U)))));
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

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135071___0(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135071___0\n"); );
    // Body
    vlSelf->__PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,25, 
                                                                         (0x1ffffffU 
                                                                          & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135069___A))), 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135067___B))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135071___1(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135071___1\n"); );
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
    __PVT__Z = (0xffffffffffffULL & VL_EXTENDS_QI(48,31, 
                                                  (0x7fffffffU 
                                                   & (IData)(
                                                             (vlSymsp->TOP__wasmetal_core__DOT___135070_.__PVT__alu_sum 
                                                              >> 0x11U)))));
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

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135072___0(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135072___0\n"); );
    // Body
    vlSelf->__PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,25, 
                                                                         (0x1ffffffU 
                                                                          & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135073___A))), 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135064___B))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135072___1(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135072___1\n"); );
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
    __PVT__Z = (0xffffffffffffULL & VL_EXTENDS_QI(48,31, 
                                                  (0x7fffffffU 
                                                   & (IData)(
                                                             (vlSymsp->TOP__wasmetal_core__DOT___135075_.__PVT__alu_sum 
                                                              >> 0x11U)))));
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

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135074___0(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135074___0\n"); );
    // Body
    vlSelf->__PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,25, 
                                                                         (0x1ffffffU 
                                                                          & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135073___A))), 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135066___B))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135074___1(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135074___1\n"); );
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
    __PVT__Z = (0xffffffffffffULL & VL_EXTENDS_QI(48,31, 
                                                  (0x7fffffffU 
                                                   & (IData)(
                                                             (vlSymsp->TOP__wasmetal_core__DOT___135073_.__PVT__alu_sum 
                                                              >> 0x11U)))));
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

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135075___0(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135075___0\n"); );
    // Body
    vlSelf->__PVT__Mr = (0x7ffffffffffULL & VL_MULS_QQQ(43, 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,25, 
                                                                         (0x1ffffffU 
                                                                          & vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135073___A))), 
                                                        (0x7ffffffffffULL 
                                                         & VL_EXTENDS_QI(43,18, vlSymsp->TOP.wasmetal_core__DOT____Vcellinp___135067___B))));
}

VL_INLINE_OPT void Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135075___1(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ico_sequent__TOP__wasmetal_core__DOT___135075___1\n"); );
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
    __PVT__Z = (0xffffffffffffULL & VL_EXTENDS_QI(48,31, 
                                                  (0x7fffffffU 
                                                   & (IData)(
                                                             (vlSymsp->TOP__wasmetal_core__DOT___135074_.__PVT__alu_sum 
                                                              >> 0x11U)))));
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
