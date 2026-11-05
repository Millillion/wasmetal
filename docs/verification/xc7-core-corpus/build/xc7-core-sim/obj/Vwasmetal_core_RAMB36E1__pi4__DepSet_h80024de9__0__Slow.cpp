#pragma GCC diagnostic ignored "-Wint-in-bool-context"
#pragma GCC diagnostic ignored "-Wbool-operation"
#pragma GCC diagnostic ignored "-Wbitwise-instead-of-logical"
// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vwasmetal_core.h for the primary calling header

#include "Vwasmetal_core__pch.h"
#include "Vwasmetal_core_RAMB36E1__pi4.h"
#include "Vwasmetal_core__Syms.h"

VL_ATTR_COLD void Vwasmetal_core_RAMB36E1__pi4___stl_sequent__TOP__wasmetal_core__DOT__data_sizes__02ewords__02e0__02e0__0(Vwasmetal_core_RAMB36E1__pi4* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB36E1__pi4___stl_sequent__TOP__wasmetal_core__DOT__data_sizes__02ewords__02e0__02e0__0\n"); );
    // Body
    vlSelf->__PVT__parity = 0U;
    vlSelf->__PVT__parity = ((0xf8U & (IData)(vlSelf->__PVT__parity)) 
                             | ((4U & (vlSelf->__PVT__memory__DOT__q[0U] 
                                       >> 0x18U)) | 
                                ((2U & (vlSelf->__PVT__memory__DOT__q[0U] 
                                        >> 0x10U)) 
                                 | (1U & (vlSelf->__PVT__memory__DOT__q[0U] 
                                          >> 8U)))));
    vlSelf->__PVT__parity = ((0xc7U & (IData)(vlSelf->__PVT__parity)) 
                             | ((0x20U & (vlSelf->__PVT__memory__DOT__q[1U] 
                                          >> 0x10U)) 
                                | ((0x10U & (vlSelf->__PVT__memory__DOT__q[1U] 
                                             >> 8U)) 
                                   | (8U & vlSelf->__PVT__memory__DOT__q[1U]))));
    vlSelf->__PVT__parity = ((0x3fU & (IData)(vlSelf->__PVT__parity)) 
                             | ((0x80U & vlSelf->__PVT__memory__DOT__q[2U]) 
                                | (0x40U & (vlSelf->__PVT__memory__DOT__q[1U] 
                                            >> 0x18U))));
    vlSelf->__PVT__data = 0ULL;
    vlSelf->__PVT__data = ((0xffffffffff000000ULL & vlSelf->__PVT__data) 
                           | (IData)((IData)(((0xff0000U 
                                               & (vlSelf->__PVT__memory__DOT__q[0U] 
                                                  >> 2U)) 
                                              | ((0xff00U 
                                                  & (vlSelf->__PVT__memory__DOT__q[0U] 
                                                     >> 1U)) 
                                                 | (0xffU 
                                                    & vlSelf->__PVT__memory__DOT__q[0U]))))));
    vlSelf->__PVT__data = ((0xffff000000ffffffULL & vlSelf->__PVT__data) 
                           | ((QData)((IData)(((0xff0000U 
                                                & (vlSelf->__PVT__memory__DOT__q[1U] 
                                                   << 3U)) 
                                               | ((0xff00U 
                                                   & (vlSelf->__PVT__memory__DOT__q[1U] 
                                                      << 4U)) 
                                                  | (0xffU 
                                                     & ((vlSelf->__PVT__memory__DOT__q[1U] 
                                                         << 5U) 
                                                        | (vlSelf->__PVT__memory__DOT__q[0U] 
                                                           >> 0x1bU))))))) 
                              << 0x18U));
    vlSelf->__PVT__data = ((0xffffffffffffULL & vlSelf->__PVT__data) 
                           | ((QData)((IData)(((0xff00U 
                                                & ((vlSelf->__PVT__memory__DOT__q[2U] 
                                                    << 9U) 
                                                   | (0x100U 
                                                      & (vlSelf->__PVT__memory__DOT__q[1U] 
                                                         >> 0x17U)))) 
                                               | (0xffU 
                                                  & (vlSelf->__PVT__memory__DOT__q[1U] 
                                                     >> 0x16U))))) 
                              << 0x30U));
    vlSelf->__Vcellinp__memory__wparity = (((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__data_sizes__02ewords__02e0__02e0__DIPBDIP) 
                                            << 4U) 
                                           | (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__data_sizes__02ewords__02e0__02e0__DIPADIP));
    vlSelf->__Vcellinp__memory__wdata = (((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__data_sizes__02ewords__02e0__02e0__DIBDI)) 
                                          << 0x20U) 
                                         | (QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__data_sizes__02ewords__02e0__02e0__DIADI)));
}

VL_ATTR_COLD void Vwasmetal_core_RAMB36E1__pi4___stl_sequent__TOP__wasmetal_core__DOT__frames_memory__02e0__02e1__0(Vwasmetal_core_RAMB36E1__pi4* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB36E1__pi4___stl_sequent__TOP__wasmetal_core__DOT__frames_memory__02e0__02e1__0\n"); );
    // Body
    vlSelf->__PVT__data = 0ULL;
    vlSelf->__PVT__data = ((0xffffffffff000000ULL & vlSelf->__PVT__data) 
                           | (IData)((IData)(((0xff0000U 
                                               & (vlSelf->__PVT__memory__DOT__q[0U] 
                                                  >> 2U)) 
                                              | ((0xff00U 
                                                  & (vlSelf->__PVT__memory__DOT__q[0U] 
                                                     >> 1U)) 
                                                 | (0xffU 
                                                    & vlSelf->__PVT__memory__DOT__q[0U]))))));
    vlSelf->__PVT__data = ((0xffff000000ffffffULL & vlSelf->__PVT__data) 
                           | ((QData)((IData)(((0xff0000U 
                                                & (vlSelf->__PVT__memory__DOT__q[1U] 
                                                   << 3U)) 
                                               | ((0xff00U 
                                                   & (vlSelf->__PVT__memory__DOT__q[1U] 
                                                      << 4U)) 
                                                  | (0xffU 
                                                     & ((vlSelf->__PVT__memory__DOT__q[1U] 
                                                         << 5U) 
                                                        | (vlSelf->__PVT__memory__DOT__q[0U] 
                                                           >> 0x1bU))))))) 
                              << 0x18U));
    vlSelf->__PVT__data = ((0xffffffffffffULL & vlSelf->__PVT__data) 
                           | ((QData)((IData)(((0xff00U 
                                                & ((vlSelf->__PVT__memory__DOT__q[2U] 
                                                    << 9U) 
                                                   | (0x100U 
                                                      & (vlSelf->__PVT__memory__DOT__q[1U] 
                                                         >> 0x17U)))) 
                                               | (0xffU 
                                                  & (vlSelf->__PVT__memory__DOT__q[1U] 
                                                     >> 0x16U))))) 
                              << 0x30U));
    vlSelf->__PVT__parity = 0U;
    vlSelf->__PVT__parity = ((0xf8U & (IData)(vlSelf->__PVT__parity)) 
                             | ((4U & (vlSelf->__PVT__memory__DOT__q[0U] 
                                       >> 0x18U)) | 
                                ((2U & (vlSelf->__PVT__memory__DOT__q[0U] 
                                        >> 0x10U)) 
                                 | (1U & (vlSelf->__PVT__memory__DOT__q[0U] 
                                          >> 8U)))));
    vlSelf->__PVT__parity = ((0xc7U & (IData)(vlSelf->__PVT__parity)) 
                             | ((0x20U & (vlSelf->__PVT__memory__DOT__q[1U] 
                                          >> 0x10U)) 
                                | ((0x10U & (vlSelf->__PVT__memory__DOT__q[1U] 
                                             >> 8U)) 
                                   | (8U & vlSelf->__PVT__memory__DOT__q[1U]))));
    vlSelf->__PVT__parity = ((0x3fU & (IData)(vlSelf->__PVT__parity)) 
                             | ((0x80U & vlSelf->__PVT__memory__DOT__q[2U]) 
                                | (0x40U & (vlSelf->__PVT__memory__DOT__q[1U] 
                                            >> 0x18U))));
    vlSelf->__Vcellinp__memory__wparity = ((((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b29__05d) 
                                             << 5U) 
                                            | ((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b20__05d) 
                                               << 4U)) 
                                           | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b11__05d) 
                                               << 3U) 
                                              | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b2__05d) 
                                                  << 2U) 
                                                 | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b25__05d) 
                                                     << 1U) 
                                                    | (IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b16__05d)))));
    vlSelf->__Vcellinp__memory__wdata = (((QData)((IData)(
                                                          (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b31__05d) 
                                                            << 0x11U) 
                                                           | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b30__05d) 
                                                               << 0x10U) 
                                                              | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b28__05d) 
                                                                  << 0xfU) 
                                                                 | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b27__05d) 
                                                                     << 0xeU) 
                                                                    | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b26__05d) 
                                                                        << 0xdU) 
                                                                       | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b25__05d) 
                                                                           << 0xcU) 
                                                                          | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b24__05d) 
                                                                              << 0xbU) 
                                                                             | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b23__05d) 
                                                                                << 0xaU) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b22__05d) 
                                                                                << 9U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b21__05d) 
                                                                                << 8U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b19__05d) 
                                                                                << 7U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b18__05d) 
                                                                                << 6U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b17__05d) 
                                                                                << 5U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b16__05d) 
                                                                                << 4U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b15__05d) 
                                                                                << 3U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b14__05d) 
                                                                                << 2U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b13__05d) 
                                                                                << 1U) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b12__05d)))))))))))))))))))) 
                                          << 0x20U) 
                                         | (QData)((IData)(
                                                           (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b10__05d) 
                                                             << 0x1fU) 
                                                            | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b9__05d) 
                                                                << 0x1eU) 
                                                               | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b8__05d) 
                                                                   << 0x1dU) 
                                                                  | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b7__05d) 
                                                                      << 0x1cU) 
                                                                     | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b6__05d) 
                                                                         << 0x1bU) 
                                                                        | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b5__05d) 
                                                                            << 0x1aU) 
                                                                           | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b4__05d) 
                                                                               << 0x19U) 
                                                                              | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b3__05d) 
                                                                                << 0x18U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b1__05d) 
                                                                                << 0x17U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__result_arity__05b0__05d) 
                                                                                << 0x16U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b31__05d) 
                                                                                << 0x15U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b30__05d) 
                                                                                << 0x14U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b29__05d) 
                                                                                << 0x13U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b28__05d) 
                                                                                << 0x12U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b27__05d) 
                                                                                << 0x11U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b26__05d) 
                                                                                << 0x10U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b24__05d) 
                                                                                << 0xfU) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b23__05d) 
                                                                                << 0xeU) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b22__05d) 
                                                                                << 0xdU) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b21__05d) 
                                                                                << 0xcU) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b20__05d) 
                                                                                << 0xbU) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b19__05d) 
                                                                                << 0xaU) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b18__05d) 
                                                                                << 9U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b17__05d) 
                                                                                << 8U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b15__05d) 
                                                                                << 7U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b14__05d) 
                                                                                << 6U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b13__05d) 
                                                                                << 5U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b12__05d) 
                                                                                << 4U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b11__05d) 
                                                                                << 3U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b10__05d) 
                                                                                << 2U) 
                                                                                | (((IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b9__05d) 
                                                                                << 1U) 
                                                                                | (IData)(vlSymsp->TOP.wasmetal_core__DOT__control_base__05b8__05d)))))))))))))))))))))))))))))))))));
}

VL_ATTR_COLD void Vwasmetal_core_RAMB36E1__pi4___stl_sequent__TOP__wasmetal_core__DOT__memory_bounds__02ewords__02e0__02e0__0(Vwasmetal_core_RAMB36E1__pi4* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_RAMB36E1__pi4___stl_sequent__TOP__wasmetal_core__DOT__memory_bounds__02ewords__02e0__02e0__0\n"); );
    // Body
    vlSelf->__PVT__parity = 0U;
    vlSelf->__PVT__parity = ((0xf8U & (IData)(vlSelf->__PVT__parity)) 
                             | ((4U & (vlSelf->__PVT__memory__DOT__q[0U] 
                                       >> 0x18U)) | 
                                ((2U & (vlSelf->__PVT__memory__DOT__q[0U] 
                                        >> 0x10U)) 
                                 | (1U & (vlSelf->__PVT__memory__DOT__q[0U] 
                                          >> 8U)))));
    vlSelf->__PVT__parity = ((0xc7U & (IData)(vlSelf->__PVT__parity)) 
                             | ((0x20U & (vlSelf->__PVT__memory__DOT__q[1U] 
                                          >> 0x10U)) 
                                | ((0x10U & (vlSelf->__PVT__memory__DOT__q[1U] 
                                             >> 8U)) 
                                   | (8U & vlSelf->__PVT__memory__DOT__q[1U]))));
    vlSelf->__PVT__parity = ((0x3fU & (IData)(vlSelf->__PVT__parity)) 
                             | ((0x80U & vlSelf->__PVT__memory__DOT__q[2U]) 
                                | (0x40U & (vlSelf->__PVT__memory__DOT__q[1U] 
                                            >> 0x18U))));
    vlSelf->__PVT__data = 0ULL;
    vlSelf->__PVT__data = ((0xffffffffff000000ULL & vlSelf->__PVT__data) 
                           | (IData)((IData)(((0xff0000U 
                                               & (vlSelf->__PVT__memory__DOT__q[0U] 
                                                  >> 2U)) 
                                              | ((0xff00U 
                                                  & (vlSelf->__PVT__memory__DOT__q[0U] 
                                                     >> 1U)) 
                                                 | (0xffU 
                                                    & vlSelf->__PVT__memory__DOT__q[0U]))))));
    vlSelf->__PVT__data = ((0xffff000000ffffffULL & vlSelf->__PVT__data) 
                           | ((QData)((IData)(((0xff0000U 
                                                & (vlSelf->__PVT__memory__DOT__q[1U] 
                                                   << 3U)) 
                                               | ((0xff00U 
                                                   & (vlSelf->__PVT__memory__DOT__q[1U] 
                                                      << 4U)) 
                                                  | (0xffU 
                                                     & ((vlSelf->__PVT__memory__DOT__q[1U] 
                                                         << 5U) 
                                                        | (vlSelf->__PVT__memory__DOT__q[0U] 
                                                           >> 0x1bU))))))) 
                              << 0x18U));
    vlSelf->__PVT__data = ((0xffffffffffffULL & vlSelf->__PVT__data) 
                           | ((QData)((IData)(((0xff00U 
                                                & ((vlSelf->__PVT__memory__DOT__q[2U] 
                                                    << 9U) 
                                                   | (0x100U 
                                                      & (vlSelf->__PVT__memory__DOT__q[1U] 
                                                         >> 0x17U)))) 
                                               | (0xffU 
                                                  & (vlSelf->__PVT__memory__DOT__q[1U] 
                                                     >> 0x16U))))) 
                              << 0x30U));
    vlSelf->__Vcellinp__memory__wparity = (((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__memory_bounds__02ewords__02e0__02e0__DIPBDIP) 
                                            << 4U) 
                                           | (IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__memory_bounds__02ewords__02e0__02e0__DIPADIP));
    vlSelf->__Vcellinp__memory__wdata = (((QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__memory_bounds__02ewords__02e0__02e0__DIBDI)) 
                                          << 0x20U) 
                                         | (QData)((IData)(vlSymsp->TOP.wasmetal_core__DOT____Vcellinp__memory_bounds__02ewords__02e0__02e0__DIADI)));
}
