// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsky130_sram_tb.h for the primary calling header

#include "Vsky130_sram_tb__pch.h"
#include "Vsky130_sram_tb___024root.h"

VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__0(Vsky130_sram_tb___024root* vlSelf);
VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__1(Vsky130_sram_tb___024root* vlSelf);
VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__2(Vsky130_sram_tb___024root* vlSelf);
VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__3(Vsky130_sram_tb___024root* vlSelf);
VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__4(Vsky130_sram_tb___024root* vlSelf);
VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__5(Vsky130_sram_tb___024root* vlSelf);
VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__6(Vsky130_sram_tb___024root* vlSelf);
VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__7(Vsky130_sram_tb___024root* vlSelf);
VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__8(Vsky130_sram_tb___024root* vlSelf);
VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__9(Vsky130_sram_tb___024root* vlSelf);
VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__10(Vsky130_sram_tb___024root* vlSelf);

void Vsky130_sram_tb___024root___eval_initial(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_initial\n"); );
    // Body
    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__0(vlSelf);
    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__1(vlSelf);
    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__2(vlSelf);
    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__3(vlSelf);
    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__4(vlSelf);
    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__5(vlSelf);
    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__6(vlSelf);
    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__7(vlSelf);
    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__8(vlSelf);
    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__9(vlSelf);
    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__10(vlSelf);
    vlSelf->__Vtrigprevexpr___TOP__sky130_sram_tb__DOT__clk__0 
        = vlSelf->sky130_sram_tb__DOT__clk;
}

VL_INLINE_OPT VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__2(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__2\n"); );
    // Body
    while (1U) {
        co_await vlSelf->__VdlySched.delay(0x2710ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           25);
        vlSelf->sky130_sram_tb__DOT__clk = (1U & (~ (IData)(vlSelf->sky130_sram_tb__DOT__clk)));
    }
}

VL_INLINE_OPT VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__3(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__3\n"); );
    // Body
    while (1U) {
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/.cache/sky130-sram/sky130_sram_2kbyte_1rw1r_32x512_8/sky130_sram_2kbyte_1rw1r_32x512_8.v", 
                                                           50);
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__csb0_reg 
            = (1U & (~ ((IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT____VdfgTmp_hcbda1b31__0) 
                        & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__sram_write)) 
                           | (0U != (0xfU & ((IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__mask_q) 
                                             >> 0xcU)))))));
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__web0_reg 
            = (1U & (~ (IData)(vlSelf->sky130_sram_tb__DOT__sram_write)));
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__wmask0_reg 
            = (0xfU & ((IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__mask_q) 
                       >> 0xcU));
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__addr0_reg 
            = vlSelf->sky130_sram_tb__DOT__adapter__DOT__address_q;
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__din0_reg 
            = vlSelf->sky130_sram_tb__DOT__adapter__DOT__data_q[3U];
        co_await vlSelf->__VdlySched.delay(0x3e8ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/.cache/sky130-sram/sky130_sram_2kbyte_1rw1r_32x512_8/sky130_sram_2kbyte_1rw1r_32x512_8.v", 
                                           57);
        vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__dout0 = 0U;
    }
}

VL_INLINE_OPT VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__4(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__4\n"); );
    // Body
    while (1U) {
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/.cache/sky130-sram/sky130_sram_2kbyte_1rw1r_32x512_8/sky130_sram_2kbyte_1rw1r_32x512_8.v", 
                                                           50);
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__csb0_reg 
            = (1U & (~ ((IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT____VdfgTmp_hcbda1b31__0) 
                        & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__sram_write)) 
                           | (0U != (0xfU & ((IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__mask_q) 
                                             >> 8U)))))));
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__web0_reg 
            = (1U & (~ (IData)(vlSelf->sky130_sram_tb__DOT__sram_write)));
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__wmask0_reg 
            = (0xfU & ((IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__mask_q) 
                       >> 8U));
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__addr0_reg 
            = vlSelf->sky130_sram_tb__DOT__adapter__DOT__address_q;
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__din0_reg 
            = vlSelf->sky130_sram_tb__DOT__adapter__DOT__data_q[2U];
        co_await vlSelf->__VdlySched.delay(0x3e8ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/.cache/sky130-sram/sky130_sram_2kbyte_1rw1r_32x512_8/sky130_sram_2kbyte_1rw1r_32x512_8.v", 
                                           57);
        vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__dout0 = 0U;
    }
}

VL_INLINE_OPT VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__5(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__5\n"); );
    // Body
    while (1U) {
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/.cache/sky130-sram/sky130_sram_2kbyte_1rw1r_32x512_8/sky130_sram_2kbyte_1rw1r_32x512_8.v", 
                                                           50);
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__csb0_reg 
            = (1U & (~ ((IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT____VdfgTmp_hcbda1b31__0) 
                        & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__sram_write)) 
                           | (0U != (0xfU & ((IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__mask_q) 
                                             >> 4U)))))));
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__web0_reg 
            = (1U & (~ (IData)(vlSelf->sky130_sram_tb__DOT__sram_write)));
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__wmask0_reg 
            = (0xfU & ((IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__mask_q) 
                       >> 4U));
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__addr0_reg 
            = vlSelf->sky130_sram_tb__DOT__adapter__DOT__address_q;
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__din0_reg 
            = vlSelf->sky130_sram_tb__DOT__adapter__DOT__data_q[1U];
        co_await vlSelf->__VdlySched.delay(0x3e8ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/.cache/sky130-sram/sky130_sram_2kbyte_1rw1r_32x512_8/sky130_sram_2kbyte_1rw1r_32x512_8.v", 
                                           57);
        vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__dout0 = 0U;
    }
}

VL_INLINE_OPT VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__6(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__6\n"); );
    // Body
    while (1U) {
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/.cache/sky130-sram/sky130_sram_2kbyte_1rw1r_32x512_8/sky130_sram_2kbyte_1rw1r_32x512_8.v", 
                                                           50);
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__csb0_reg 
            = (1U & (~ ((IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT____VdfgTmp_hcbda1b31__0) 
                        & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__sram_write)) 
                           | (0U != (0xfU & (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__mask_q)))))));
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__web0_reg 
            = (1U & (~ (IData)(vlSelf->sky130_sram_tb__DOT__sram_write)));
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__wmask0_reg 
            = (0xfU & (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__mask_q));
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__addr0_reg 
            = vlSelf->sky130_sram_tb__DOT__adapter__DOT__address_q;
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__din0_reg 
            = vlSelf->sky130_sram_tb__DOT__adapter__DOT__data_q[0U];
        co_await vlSelf->__VdlySched.delay(0x3e8ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/.cache/sky130-sram/sky130_sram_2kbyte_1rw1r_32x512_8/sky130_sram_2kbyte_1rw1r_32x512_8.v", 
                                           57);
        vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__dout0 = 0U;
    }
}

VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__7____Vfork_4__1(Vsky130_sram_tb___024root* vlSelf, IData/*31:0*/ __Vintraval_h1c213051__0);

VL_INLINE_OPT VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__7(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__7\n"); );
    // Body
    while (1U) {
        co_await vlSelf->__VtrigSched_h2f20d2d8__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(negedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/.cache/sky130-sram/sky130_sram_2kbyte_1rw1r_32x512_8/sky130_sram_2kbyte_1rw1r_32x512_8.v", 
                                                           100);
        if (((~ (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__csb0_reg)) 
             & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__web0_reg))) {
            vlSelf->__Vintraval_h1c213051__0 = vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__mem
                [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__addr0_reg];
            Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__7____Vfork_4__1(vlSelf, vlSelf->__Vintraval_h1c213051__0);
        }
    }
}

VL_INLINE_OPT VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__7____Vfork_4__1(Vsky130_sram_tb___024root* vlSelf, IData/*31:0*/ __Vintraval_h1c213051__0) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__7____Vfork_4__1\n"); );
    // Body
    co_await vlSelf->__VdlySched.delay(0x2328ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/.cache/sky130-sram/sky130_sram_2kbyte_1rw1r_32x512_8/sky130_sram_2kbyte_1rw1r_32x512_8.v", 
                                       103);
    vlSelf->__Vdlyvval__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__dout0__v0 
        = __Vintraval_h1c213051__0;
    vlSelf->__Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__dout0__v0 = 1U;
}

VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__8____Vfork_3__1(Vsky130_sram_tb___024root* vlSelf, IData/*31:0*/ __Vintraval_hac5192ed__0);

VL_INLINE_OPT VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__8(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__8\n"); );
    // Body
    while (1U) {
        co_await vlSelf->__VtrigSched_h2f20d2d8__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(negedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/.cache/sky130-sram/sky130_sram_2kbyte_1rw1r_32x512_8/sky130_sram_2kbyte_1rw1r_32x512_8.v", 
                                                           100);
        if (((~ (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__csb0_reg)) 
             & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__web0_reg))) {
            vlSelf->__Vintraval_hac5192ed__0 = vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__mem
                [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__addr0_reg];
            Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__8____Vfork_3__1(vlSelf, vlSelf->__Vintraval_hac5192ed__0);
        }
    }
}

VL_INLINE_OPT VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__8____Vfork_3__1(Vsky130_sram_tb___024root* vlSelf, IData/*31:0*/ __Vintraval_hac5192ed__0) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__8____Vfork_3__1\n"); );
    // Body
    co_await vlSelf->__VdlySched.delay(0x2328ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/.cache/sky130-sram/sky130_sram_2kbyte_1rw1r_32x512_8/sky130_sram_2kbyte_1rw1r_32x512_8.v", 
                                       103);
    vlSelf->__Vdlyvval__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__dout0__v0 
        = __Vintraval_hac5192ed__0;
    vlSelf->__Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__dout0__v0 = 1U;
}

VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__9____Vfork_2__1(Vsky130_sram_tb___024root* vlSelf, IData/*31:0*/ __Vintraval_h36210009__0);

VL_INLINE_OPT VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__9(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__9\n"); );
    // Body
    while (1U) {
        co_await vlSelf->__VtrigSched_h2f20d2d8__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(negedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/.cache/sky130-sram/sky130_sram_2kbyte_1rw1r_32x512_8/sky130_sram_2kbyte_1rw1r_32x512_8.v", 
                                                           100);
        if (((~ (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__csb0_reg)) 
             & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__web0_reg))) {
            vlSelf->__Vintraval_h36210009__0 = vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__mem
                [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__addr0_reg];
            Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__9____Vfork_2__1(vlSelf, vlSelf->__Vintraval_h36210009__0);
        }
    }
}

VL_INLINE_OPT VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__9____Vfork_2__1(Vsky130_sram_tb___024root* vlSelf, IData/*31:0*/ __Vintraval_h36210009__0) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__9____Vfork_2__1\n"); );
    // Body
    co_await vlSelf->__VdlySched.delay(0x2328ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/.cache/sky130-sram/sky130_sram_2kbyte_1rw1r_32x512_8/sky130_sram_2kbyte_1rw1r_32x512_8.v", 
                                       103);
    vlSelf->__Vdlyvval__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__dout0__v0 
        = __Vintraval_h36210009__0;
    vlSelf->__Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__dout0__v0 = 1U;
}

VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__10____Vfork_1__1(Vsky130_sram_tb___024root* vlSelf, IData/*31:0*/ __Vintraval_h7f9437f7__0);

VL_INLINE_OPT VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__10(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__10\n"); );
    // Body
    while (1U) {
        co_await vlSelf->__VtrigSched_h2f20d2d8__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(negedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/.cache/sky130-sram/sky130_sram_2kbyte_1rw1r_32x512_8/sky130_sram_2kbyte_1rw1r_32x512_8.v", 
                                                           100);
        if (((~ (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__csb0_reg)) 
             & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__web0_reg))) {
            vlSelf->__Vintraval_h7f9437f7__0 = vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__mem
                [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__addr0_reg];
            Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__10____Vfork_1__1(vlSelf, vlSelf->__Vintraval_h7f9437f7__0);
        }
    }
}

VL_INLINE_OPT VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__10____Vfork_1__1(Vsky130_sram_tb___024root* vlSelf, IData/*31:0*/ __Vintraval_h7f9437f7__0) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__10____Vfork_1__1\n"); );
    // Body
    co_await vlSelf->__VdlySched.delay(0x2328ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/.cache/sky130-sram/sky130_sram_2kbyte_1rw1r_32x512_8/sky130_sram_2kbyte_1rw1r_32x512_8.v", 
                                       103);
    vlSelf->__Vdlyvval__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__dout0__v0 
        = __Vintraval_h7f9437f7__0;
    vlSelf->__Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__dout0__v0 = 1U;
}

VL_INLINE_OPT void Vsky130_sram_tb___024root___act_comb__TOP__0(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___act_comb__TOP__0\n"); );
    // Body
    vlSelf->sky130_sram_tb__DOT__adapter__DOT__legal 
        = ((0U == (0xfU & vlSelf->sky130_sram_tb__DOT__address)) 
           & ((0x2000ULL >= (0x1ffffffffULL & (0x10ULL 
                                               + (QData)((IData)(vlSelf->sky130_sram_tb__DOT__address))))) 
              & (0U != (IData)(vlSelf->sky130_sram_tb__DOT__mask))));
    vlSelf->sky130_sram_tb__DOT__sram_enable = ((~ (IData)(vlSelf->sky130_sram_tb__DOT__reset)) 
                                                & (1U 
                                                   == (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state)));
    vlSelf->sky130_sram_tb__DOT__sram_write = ((IData)(vlSelf->sky130_sram_tb__DOT__sram_enable) 
                                               & (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__write_q));
    vlSelf->sky130_sram_tb__DOT__storage__DOT____VdfgTmp_hcbda1b31__0 
        = ((IData)(vlSelf->sky130_sram_tb__DOT__sram_enable) 
           & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__reset)) 
              & (0U == VL_SHIFTR_III(32,32,32, (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__address_q), 9U))));
}

VL_INLINE_OPT void Vsky130_sram_tb___024root___act_comb__TOP__1(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___act_comb__TOP__1\n"); );
    // Body
    vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data[0U][0U] 
        = vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__dout0;
    vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data[0U][1U] 
        = vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__dout0;
    vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data[0U][2U] 
        = vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__dout0;
    vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data[0U][3U] 
        = vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__dout0;
    if ((0U >= (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__selected))) {
        vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[0U] 
            = vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data
            [vlSelf->sky130_sram_tb__DOT__storage__DOT__selected][0U];
        vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[1U] 
            = vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data
            [vlSelf->sky130_sram_tb__DOT__storage__DOT__selected][1U];
        vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[2U] 
            = vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data
            [vlSelf->sky130_sram_tb__DOT__storage__DOT__selected][2U];
        vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[3U] 
            = vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data
            [vlSelf->sky130_sram_tb__DOT__storage__DOT__selected][3U];
    } else {
        vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[0U] = 0U;
        vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[1U] = 0U;
        vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[2U] = 0U;
        vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[3U] = 0U;
    }
}

void Vsky130_sram_tb___024root___eval_act(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_act\n"); );
    // Body
    if ((0xbULL & vlSelf->__VactTriggered.word(0U))) {
        Vsky130_sram_tb___024root___act_comb__TOP__0(vlSelf);
    }
    if ((9ULL & vlSelf->__VactTriggered.word(0U))) {
        Vsky130_sram_tb___024root___act_comb__TOP__1(vlSelf);
    }
}

VL_INLINE_OPT void Vsky130_sram_tb___024root___nba_sequent__TOP__0(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___nba_sequent__TOP__0\n"); );
    // Init
    CData/*2:0*/ __Vdly__sky130_sram_tb__DOT__adapter__DOT__state;
    __Vdly__sky130_sram_tb__DOT__adapter__DOT__state = 0;
    CData/*0:0*/ __Vdly__sky130_sram_tb__DOT__adapter__DOT__write_q;
    __Vdly__sky130_sram_tb__DOT__adapter__DOT__write_q = 0;
    CData/*0:0*/ __Vdly__sky130_sram_tb__DOT__adapter__DOT__remaining;
    __Vdly__sky130_sram_tb__DOT__adapter__DOT__remaining = 0;
    // Body
    __Vdly__sky130_sram_tb__DOT__adapter__DOT__remaining 
        = vlSelf->sky130_sram_tb__DOT__adapter__DOT__remaining;
    __Vdly__sky130_sram_tb__DOT__adapter__DOT__write_q 
        = vlSelf->sky130_sram_tb__DOT__adapter__DOT__write_q;
    __Vdly__sky130_sram_tb__DOT__adapter__DOT__state 
        = vlSelf->sky130_sram_tb__DOT__adapter__DOT__state;
    if (vlSelf->sky130_sram_tb__DOT__sram_enable) {
        vlSelf->sky130_sram_tb__DOT__commands = ((IData)(1U) 
                                                 + vlSelf->sky130_sram_tb__DOT__commands);
    }
    if (vlSelf->sky130_sram_tb__DOT__reset) {
        vlSelf->sky130_sram_tb__DOT__storage__DOT__selected = 0U;
        __Vdly__sky130_sram_tb__DOT__adapter__DOT__state = 0U;
        __Vdly__sky130_sram_tb__DOT__adapter__DOT__write_q = 0U;
        vlSelf->sky130_sram_tb__DOT__adapter__DOT__address_q = 0U;
        vlSelf->sky130_sram_tb__DOT__adapter__DOT__mask_q = 0U;
        vlSelf->sky130_sram_tb__DOT__adapter__DOT__data_q[0U] = 0U;
        vlSelf->sky130_sram_tb__DOT__adapter__DOT__data_q[1U] = 0U;
        vlSelf->sky130_sram_tb__DOT__adapter__DOT__data_q[2U] = 0U;
        vlSelf->sky130_sram_tb__DOT__adapter__DOT__data_q[3U] = 0U;
        __Vdly__sky130_sram_tb__DOT__adapter__DOT__remaining = 0U;
        vlSelf->sky130_sram_tb__DOT__fault = 0U;
        vlSelf->sky130_sram_tb__DOT__rdata[0U] = 0U;
        vlSelf->sky130_sram_tb__DOT__rdata[1U] = 0U;
        vlSelf->sky130_sram_tb__DOT__rdata[2U] = 0U;
        vlSelf->sky130_sram_tb__DOT__rdata[3U] = 0U;
        vlSelf->sky130_sram_tb__DOT__storage__DOT__held[0U] = 0U;
        vlSelf->sky130_sram_tb__DOT__storage__DOT__held[1U] = 0U;
        vlSelf->sky130_sram_tb__DOT__storage__DOT__held[2U] = 0U;
        vlSelf->sky130_sram_tb__DOT__storage__DOT__held[3U] = 0U;
    } else {
        if (((IData)(vlSelf->sky130_sram_tb__DOT__sram_enable) 
             & (~ (IData)(vlSelf->sky130_sram_tb__DOT__sram_write)))) {
            vlSelf->sky130_sram_tb__DOT__storage__DOT__selected 
                = (1U & ((IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__address_q) 
                         >> 9U));
        }
        if ((4U & (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state))) {
            if ((2U & (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state))) {
                vlSelf->sky130_sram_tb__DOT__fault = 1U;
                vlSelf->sky130_sram_tb__DOT__rdata[0U] = 0U;
                vlSelf->sky130_sram_tb__DOT__rdata[1U] = 0U;
                vlSelf->sky130_sram_tb__DOT__rdata[2U] = 0U;
                vlSelf->sky130_sram_tb__DOT__rdata[3U] = 0U;
                __Vdly__sky130_sram_tb__DOT__adapter__DOT__state = 3U;
            } else if ((1U & (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state))) {
                vlSelf->sky130_sram_tb__DOT__fault = 1U;
                vlSelf->sky130_sram_tb__DOT__rdata[0U] = 0U;
                vlSelf->sky130_sram_tb__DOT__rdata[1U] = 0U;
                vlSelf->sky130_sram_tb__DOT__rdata[2U] = 0U;
                vlSelf->sky130_sram_tb__DOT__rdata[3U] = 0U;
                __Vdly__sky130_sram_tb__DOT__adapter__DOT__state = 3U;
            } else if ((1U & (~ (IData)(vlSelf->sky130_sram_tb__DOT__valid)))) {
                __Vdly__sky130_sram_tb__DOT__adapter__DOT__state = 0U;
            }
        } else if ((2U & (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state))) {
            if ((1U & (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state))) {
                __Vdly__sky130_sram_tb__DOT__adapter__DOT__state = 4U;
            } else if (vlSelf->sky130_sram_tb__DOT__adapter__DOT__remaining) {
                if (vlSelf->sky130_sram_tb__DOT__storage__DOT__pending) {
                    vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                        = vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[0U];
                    vlSelf->sky130_sram_tb__DOT__rdata[1U] 
                        = vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[1U];
                    vlSelf->sky130_sram_tb__DOT__rdata[2U] 
                        = vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[2U];
                    vlSelf->sky130_sram_tb__DOT__rdata[3U] 
                        = vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[3U];
                } else {
                    vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                        = vlSelf->sky130_sram_tb__DOT__storage__DOT__held[0U];
                    vlSelf->sky130_sram_tb__DOT__rdata[1U] 
                        = vlSelf->sky130_sram_tb__DOT__storage__DOT__held[1U];
                    vlSelf->sky130_sram_tb__DOT__rdata[2U] 
                        = vlSelf->sky130_sram_tb__DOT__storage__DOT__held[2U];
                    vlSelf->sky130_sram_tb__DOT__rdata[3U] 
                        = vlSelf->sky130_sram_tb__DOT__storage__DOT__held[3U];
                }
                __Vdly__sky130_sram_tb__DOT__adapter__DOT__remaining = 0U;
                __Vdly__sky130_sram_tb__DOT__adapter__DOT__state = 3U;
            } else {
                __Vdly__sky130_sram_tb__DOT__adapter__DOT__remaining 
                    = (1U & ((IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__remaining) 
                             - (IData)(1U)));
            }
        } else if ((1U & (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state))) {
            if (vlSelf->sky130_sram_tb__DOT__adapter__DOT__write_q) {
                __Vdly__sky130_sram_tb__DOT__adapter__DOT__state = 3U;
            } else {
                __Vdly__sky130_sram_tb__DOT__adapter__DOT__remaining = 1U;
                __Vdly__sky130_sram_tb__DOT__adapter__DOT__state = 2U;
            }
        } else if (vlSelf->sky130_sram_tb__DOT__valid) {
            __Vdly__sky130_sram_tb__DOT__adapter__DOT__write_q 
                = vlSelf->sky130_sram_tb__DOT__write;
            vlSelf->sky130_sram_tb__DOT__adapter__DOT__address_q 
                = (0x1ffU & (vlSelf->sky130_sram_tb__DOT__address 
                             >> 4U));
            vlSelf->sky130_sram_tb__DOT__adapter__DOT__mask_q 
                = vlSelf->sky130_sram_tb__DOT__mask;
            vlSelf->sky130_sram_tb__DOT__adapter__DOT__data_q[0U] 
                = vlSelf->sky130_sram_tb__DOT__wdata[0U];
            vlSelf->sky130_sram_tb__DOT__adapter__DOT__data_q[1U] 
                = vlSelf->sky130_sram_tb__DOT__wdata[1U];
            vlSelf->sky130_sram_tb__DOT__adapter__DOT__data_q[2U] 
                = vlSelf->sky130_sram_tb__DOT__wdata[2U];
            vlSelf->sky130_sram_tb__DOT__adapter__DOT__data_q[3U] 
                = vlSelf->sky130_sram_tb__DOT__wdata[3U];
            vlSelf->sky130_sram_tb__DOT__rdata[0U] = 0U;
            vlSelf->sky130_sram_tb__DOT__rdata[1U] = 0U;
            vlSelf->sky130_sram_tb__DOT__rdata[2U] = 0U;
            vlSelf->sky130_sram_tb__DOT__rdata[3U] = 0U;
            vlSelf->sky130_sram_tb__DOT__fault = (1U 
                                                  & (~ (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__legal)));
            __Vdly__sky130_sram_tb__DOT__adapter__DOT__remaining = 0U;
            __Vdly__sky130_sram_tb__DOT__adapter__DOT__state 
                = ((IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__legal)
                    ? 1U : 3U);
        }
        if (vlSelf->sky130_sram_tb__DOT__storage__DOT__pending) {
            vlSelf->sky130_sram_tb__DOT__storage__DOT__held[0U] 
                = vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[0U];
            vlSelf->sky130_sram_tb__DOT__storage__DOT__held[1U] 
                = vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[1U];
            vlSelf->sky130_sram_tb__DOT__storage__DOT__held[2U] 
                = vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[2U];
            vlSelf->sky130_sram_tb__DOT__storage__DOT__held[3U] 
                = vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[3U];
        }
    }
    vlSelf->sky130_sram_tb__DOT__adapter__DOT__remaining 
        = __Vdly__sky130_sram_tb__DOT__adapter__DOT__remaining;
    vlSelf->sky130_sram_tb__DOT__adapter__DOT__write_q 
        = __Vdly__sky130_sram_tb__DOT__adapter__DOT__write_q;
    vlSelf->sky130_sram_tb__DOT__adapter__DOT__state 
        = __Vdly__sky130_sram_tb__DOT__adapter__DOT__state;
    vlSelf->sky130_sram_tb__DOT__storage__DOT__pending 
        = ((1U & (~ (IData)(vlSelf->sky130_sram_tb__DOT__reset))) 
           && ((IData)(vlSelf->sky130_sram_tb__DOT__sram_enable) 
               & (~ (IData)(vlSelf->sky130_sram_tb__DOT__sram_write))));
}

VL_INLINE_OPT void Vsky130_sram_tb___024root___nba_sequent__TOP__1(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___nba_sequent__TOP__1\n"); );
    // Body
    if ((1U & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__csb0_reg)) 
               & (~ (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__web0_reg))))) {
        if ((1U & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__wmask0_reg))) {
            vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__mem[vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__addr0_reg] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__mem
                    [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__addr0_reg]) 
                   | (0xffU & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__din0_reg));
        }
        if ((2U & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__wmask0_reg))) {
            vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__mem[vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__addr0_reg] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__mem
                    [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__addr0_reg]) 
                   | (0xff00U & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__din0_reg));
        }
        if ((4U & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__wmask0_reg))) {
            vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__mem[vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__addr0_reg] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__mem
                    [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__addr0_reg]) 
                   | (0xff0000U & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__din0_reg));
        }
        if ((8U & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__wmask0_reg))) {
            vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__mem[vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__addr0_reg] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__mem
                    [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__addr0_reg]) 
                   | (0xff000000U & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__din0_reg));
        }
    }
    if ((1U & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__csb0_reg)) 
               & (~ (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__web0_reg))))) {
        if ((1U & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__wmask0_reg))) {
            vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__mem[vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__addr0_reg] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__mem
                    [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__addr0_reg]) 
                   | (0xffU & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__din0_reg));
        }
        if ((2U & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__wmask0_reg))) {
            vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__mem[vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__addr0_reg] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__mem
                    [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__addr0_reg]) 
                   | (0xff00U & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__din0_reg));
        }
        if ((4U & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__wmask0_reg))) {
            vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__mem[vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__addr0_reg] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__mem
                    [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__addr0_reg]) 
                   | (0xff0000U & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__din0_reg));
        }
        if ((8U & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__wmask0_reg))) {
            vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__mem[vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__addr0_reg] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__mem
                    [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__addr0_reg]) 
                   | (0xff000000U & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__din0_reg));
        }
    }
    if ((1U & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__csb0_reg)) 
               & (~ (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__web0_reg))))) {
        if ((1U & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__wmask0_reg))) {
            vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__mem[vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__addr0_reg] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__mem
                    [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__addr0_reg]) 
                   | (0xffU & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__din0_reg));
        }
        if ((2U & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__wmask0_reg))) {
            vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__mem[vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__addr0_reg] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__mem
                    [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__addr0_reg]) 
                   | (0xff00U & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__din0_reg));
        }
        if ((4U & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__wmask0_reg))) {
            vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__mem[vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__addr0_reg] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__mem
                    [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__addr0_reg]) 
                   | (0xff0000U & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__din0_reg));
        }
        if ((8U & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__wmask0_reg))) {
            vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__mem[vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__addr0_reg] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__mem
                    [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__addr0_reg]) 
                   | (0xff000000U & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__din0_reg));
        }
    }
    if ((1U & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__csb0_reg)) 
               & (~ (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__web0_reg))))) {
        if ((1U & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__wmask0_reg))) {
            vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__mem[vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__addr0_reg] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__mem
                    [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__addr0_reg]) 
                   | (0xffU & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__din0_reg));
        }
        if ((2U & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__wmask0_reg))) {
            vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__mem[vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__addr0_reg] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__mem
                    [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__addr0_reg]) 
                   | (0xff00U & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__din0_reg));
        }
        if ((4U & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__wmask0_reg))) {
            vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__mem[vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__addr0_reg] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__mem
                    [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__addr0_reg]) 
                   | (0xff0000U & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__din0_reg));
        }
        if ((8U & (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__wmask0_reg))) {
            vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__mem[vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__addr0_reg] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__mem
                    [vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__addr0_reg]) 
                   | (0xff000000U & vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__din0_reg));
        }
    }
}

VL_INLINE_OPT void Vsky130_sram_tb___024root___nba_sequent__TOP__2(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___nba_sequent__TOP__2\n"); );
    // Body
    if (vlSelf->__Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__dout0__v0) {
        vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__dout0 
            = vlSelf->__Vdlyvval__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__dout0__v0;
        vlSelf->__Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__dout0__v0 = 0U;
    }
    if (vlSelf->__Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__dout0__v0) {
        vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__dout0 
            = vlSelf->__Vdlyvval__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__dout0__v0;
        vlSelf->__Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__dout0__v0 = 0U;
    }
    if (vlSelf->__Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__dout0__v0) {
        vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__dout0 
            = vlSelf->__Vdlyvval__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__dout0__v0;
        vlSelf->__Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__dout0__v0 = 0U;
    }
    if (vlSelf->__Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__dout0__v0) {
        vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__dout0 
            = vlSelf->__Vdlyvval__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__dout0__v0;
        vlSelf->__Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__dout0__v0 = 0U;
    }
}

VL_INLINE_OPT void Vsky130_sram_tb___024root___nba_comb__TOP__1(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___nba_comb__TOP__1\n"); );
    // Body
    vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data[0U][3U] 
        = vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__dout0;
    vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data[0U][2U] 
        = vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__dout0;
    vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data[0U][1U] 
        = vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__dout0;
    vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data[0U][0U] 
        = vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__dout0;
    if ((0U >= (IData)(vlSelf->sky130_sram_tb__DOT__storage__DOT__selected))) {
        vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[0U] 
            = vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data
            [vlSelf->sky130_sram_tb__DOT__storage__DOT__selected][0U];
        vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[1U] 
            = vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data
            [vlSelf->sky130_sram_tb__DOT__storage__DOT__selected][1U];
        vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[2U] 
            = vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data
            [vlSelf->sky130_sram_tb__DOT__storage__DOT__selected][2U];
        vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[3U] 
            = vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data
            [vlSelf->sky130_sram_tb__DOT__storage__DOT__selected][3U];
    } else {
        vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[0U] = 0U;
        vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[1U] = 0U;
        vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[2U] = 0U;
        vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled[3U] = 0U;
    }
}

void Vsky130_sram_tb___024root___eval_nba(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_nba\n"); );
    // Body
    if ((1ULL & vlSelf->__VnbaTriggered.word(0U))) {
        Vsky130_sram_tb___024root___nba_sequent__TOP__0(vlSelf);
    }
    if ((2ULL & vlSelf->__VnbaTriggered.word(0U))) {
        Vsky130_sram_tb___024root___nba_sequent__TOP__1(vlSelf);
    }
    if ((4ULL & vlSelf->__VnbaTriggered.word(0U))) {
        Vsky130_sram_tb___024root___nba_sequent__TOP__2(vlSelf);
    }
    if ((0xbULL & vlSelf->__VnbaTriggered.word(0U))) {
        Vsky130_sram_tb___024root___act_comb__TOP__0(vlSelf);
    }
    if ((0xdULL & vlSelf->__VnbaTriggered.word(0U))) {
        Vsky130_sram_tb___024root___nba_comb__TOP__1(vlSelf);
    }
}

void Vsky130_sram_tb___024root___timing_resume(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___timing_resume\n"); );
    // Body
    if ((1ULL & vlSelf->__VactTriggered.word(0U))) {
        vlSelf->__VtrigSched_h2f20d209__0.resume("@(posedge sky130_sram_tb.clk)");
    }
    if ((2ULL & vlSelf->__VactTriggered.word(0U))) {
        vlSelf->__VtrigSched_h2f20d2d8__0.resume("@(negedge sky130_sram_tb.clk)");
    }
    if ((8ULL & vlSelf->__VactTriggered.word(0U))) {
        vlSelf->__VdlySched.resume();
    }
}

void Vsky130_sram_tb___024root___timing_commit(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___timing_commit\n"); );
    // Body
    if ((! (1ULL & vlSelf->__VactTriggered.word(0U)))) {
        vlSelf->__VtrigSched_h2f20d209__0.commit("@(posedge sky130_sram_tb.clk)");
    }
    if ((! (2ULL & vlSelf->__VactTriggered.word(0U)))) {
        vlSelf->__VtrigSched_h2f20d2d8__0.commit("@(negedge sky130_sram_tb.clk)");
    }
}

void Vsky130_sram_tb___024root___eval_triggers__act(Vsky130_sram_tb___024root* vlSelf);

bool Vsky130_sram_tb___024root___eval_phase__act(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_phase__act\n"); );
    // Init
    VlTriggerVec<4> __VpreTriggered;
    CData/*0:0*/ __VactExecute;
    // Body
    Vsky130_sram_tb___024root___eval_triggers__act(vlSelf);
    Vsky130_sram_tb___024root___timing_commit(vlSelf);
    __VactExecute = vlSelf->__VactTriggered.any();
    if (__VactExecute) {
        __VpreTriggered.andNot(vlSelf->__VactTriggered, vlSelf->__VnbaTriggered);
        vlSelf->__VnbaTriggered.thisOr(vlSelf->__VactTriggered);
        Vsky130_sram_tb___024root___timing_resume(vlSelf);
        Vsky130_sram_tb___024root___eval_act(vlSelf);
    }
    return (__VactExecute);
}

bool Vsky130_sram_tb___024root___eval_phase__nba(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_phase__nba\n"); );
    // Init
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = vlSelf->__VnbaTriggered.any();
    if (__VnbaExecute) {
        Vsky130_sram_tb___024root___eval_nba(vlSelf);
        vlSelf->__VnbaTriggered.clear();
    }
    return (__VnbaExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vsky130_sram_tb___024root___dump_triggers__nba(Vsky130_sram_tb___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void Vsky130_sram_tb___024root___dump_triggers__act(Vsky130_sram_tb___024root* vlSelf);
#endif  // VL_DEBUG

void Vsky130_sram_tb___024root___eval(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval\n"); );
    // Init
    IData/*31:0*/ __VnbaIterCount;
    CData/*0:0*/ __VnbaContinue;
    // Body
    __VnbaIterCount = 0U;
    __VnbaContinue = 1U;
    while (__VnbaContinue) {
        if (VL_UNLIKELY((0x64U < __VnbaIterCount))) {
#ifdef VL_DEBUG
            Vsky130_sram_tb___024root___dump_triggers__nba(vlSelf);
#endif
            VL_FATAL_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 3, "", "NBA region did not converge.");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        __VnbaContinue = 0U;
        vlSelf->__VactIterCount = 0U;
        vlSelf->__VactContinue = 1U;
        while (vlSelf->__VactContinue) {
            if (VL_UNLIKELY((0x64U < vlSelf->__VactIterCount))) {
#ifdef VL_DEBUG
                Vsky130_sram_tb___024root___dump_triggers__act(vlSelf);
#endif
                VL_FATAL_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 3, "", "Active region did not converge.");
            }
            vlSelf->__VactIterCount = ((IData)(1U) 
                                       + vlSelf->__VactIterCount);
            vlSelf->__VactContinue = 0U;
            if (Vsky130_sram_tb___024root___eval_phase__act(vlSelf)) {
                vlSelf->__VactContinue = 1U;
            }
        }
        if (Vsky130_sram_tb___024root___eval_phase__nba(vlSelf)) {
            __VnbaContinue = 1U;
        }
    }
}

#ifdef VL_DEBUG
void Vsky130_sram_tb___024root___eval_debug_assertions(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_debug_assertions\n"); );
}
#endif  // VL_DEBUG
