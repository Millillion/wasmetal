// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsky130_sram_tb.h for the primary calling header

#include "Vsky130_sram_tb__pch.h"
#include "Vsky130_sram_tb___024root.h"

VL_ATTR_COLD void Vsky130_sram_tb___024root___eval_static__TOP(Vsky130_sram_tb___024root* vlSelf);

VL_ATTR_COLD void Vsky130_sram_tb___024root___eval_static(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_static\n"); );
    // Body
    Vsky130_sram_tb___024root___eval_static__TOP(vlSelf);
}

VL_ATTR_COLD void Vsky130_sram_tb___024root___eval_static__TOP(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_static__TOP\n"); );
    // Body
    vlSelf->sky130_sram_tb__DOT__clk = 0U;
    vlSelf->sky130_sram_tb__DOT__reset = 1U;
    vlSelf->sky130_sram_tb__DOT__valid = 0U;
    vlSelf->sky130_sram_tb__DOT__write = 0U;
    vlSelf->sky130_sram_tb__DOT__address = 0U;
    vlSelf->sky130_sram_tb__DOT__mask = 0U;
    vlSelf->sky130_sram_tb__DOT__wdata[0U] = 0U;
    vlSelf->sky130_sram_tb__DOT__wdata[1U] = 0U;
    vlSelf->sky130_sram_tb__DOT__wdata[2U] = 0U;
    vlSelf->sky130_sram_tb__DOT__wdata[3U] = 0U;
    vlSelf->sky130_sram_tb__DOT__transactions = 0U;
    vlSelf->sky130_sram_tb__DOT__commands = 0U;
    vlSelf->sky130_sram_tb__DOT__resets = 0U;
}

VL_ATTR_COLD void Vsky130_sram_tb___024root___eval_final(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_final\n"); );
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vsky130_sram_tb___024root___dump_triggers__stl(Vsky130_sram_tb___024root* vlSelf);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vsky130_sram_tb___024root___eval_phase__stl(Vsky130_sram_tb___024root* vlSelf);

VL_ATTR_COLD void Vsky130_sram_tb___024root___eval_settle(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_settle\n"); );
    // Init
    IData/*31:0*/ __VstlIterCount;
    CData/*0:0*/ __VstlContinue;
    // Body
    __VstlIterCount = 0U;
    vlSelf->__VstlFirstIteration = 1U;
    __VstlContinue = 1U;
    while (__VstlContinue) {
        if (VL_UNLIKELY((0x64U < __VstlIterCount))) {
#ifdef VL_DEBUG
            Vsky130_sram_tb___024root___dump_triggers__stl(vlSelf);
#endif
            VL_FATAL_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 3, "", "Settle region did not converge.");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        __VstlContinue = 0U;
        if (Vsky130_sram_tb___024root___eval_phase__stl(vlSelf)) {
            __VstlContinue = 1U;
        }
        vlSelf->__VstlFirstIteration = 0U;
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vsky130_sram_tb___024root___dump_triggers__stl(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(vlSelf->__VstlTriggered.any())))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelf->__VstlTriggered.word(0U))) {
        VL_DBG_MSGF("         'stl' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vsky130_sram_tb___024root___stl_sequent__TOP__0(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___stl_sequent__TOP__0\n"); );
    // Body
    vlSelf->sky130_sram_tb__DOT__adapter__DOT__legal 
        = ((0U == (0xfU & vlSelf->sky130_sram_tb__DOT__address)) 
           & ((0x2000ULL >= (0x1ffffffffULL & (0x10ULL 
                                               + (QData)((IData)(vlSelf->sky130_sram_tb__DOT__address))))) 
              & (0U != (IData)(vlSelf->sky130_sram_tb__DOT__mask))));
    vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data[0U][0U] 
        = vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__dout0;
    vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data[0U][1U] 
        = vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__dout0;
    vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data[0U][2U] 
        = vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__dout0;
    vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data[0U][3U] 
        = vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__dout0;
    vlSelf->sky130_sram_tb__DOT__sram_enable = ((~ (IData)(vlSelf->sky130_sram_tb__DOT__reset)) 
                                                & (1U 
                                                   == (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state)));
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
    vlSelf->sky130_sram_tb__DOT__sram_write = ((IData)(vlSelf->sky130_sram_tb__DOT__sram_enable) 
                                               & (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__write_q));
    vlSelf->sky130_sram_tb__DOT__storage__DOT____VdfgTmp_hcbda1b31__0 
        = ((IData)(vlSelf->sky130_sram_tb__DOT__sram_enable) 
           & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__reset)) 
              & (0U == VL_SHIFTR_III(32,32,32, (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__address_q), 9U))));
}

VL_ATTR_COLD void Vsky130_sram_tb___024root___eval_stl(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_stl\n"); );
    // Body
    if ((1ULL & vlSelf->__VstlTriggered.word(0U))) {
        Vsky130_sram_tb___024root___stl_sequent__TOP__0(vlSelf);
    }
}

VL_ATTR_COLD void Vsky130_sram_tb___024root___eval_triggers__stl(Vsky130_sram_tb___024root* vlSelf);

VL_ATTR_COLD bool Vsky130_sram_tb___024root___eval_phase__stl(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_phase__stl\n"); );
    // Init
    CData/*0:0*/ __VstlExecute;
    // Body
    Vsky130_sram_tb___024root___eval_triggers__stl(vlSelf);
    __VstlExecute = vlSelf->__VstlTriggered.any();
    if (__VstlExecute) {
        Vsky130_sram_tb___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vsky130_sram_tb___024root___dump_triggers__act(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(vlSelf->__VactTriggered.any())))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelf->__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 0 is active: @(posedge sky130_sram_tb.clk)\n");
    }
    if ((2ULL & vlSelf->__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 1 is active: @(negedge sky130_sram_tb.clk)\n");
    }
    if ((4ULL & vlSelf->__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 2 is active: @(negedge sky130_sram_tb.clk or [true] __VdlySched.awaitingCurrentTime())\n");
    }
    if ((8ULL & vlSelf->__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 3 is active: @([true] __VdlySched.awaitingCurrentTime())\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void Vsky130_sram_tb___024root___dump_triggers__nba(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___dump_triggers__nba\n"); );
    // Body
    if ((1U & (~ (IData)(vlSelf->__VnbaTriggered.any())))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelf->__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 0 is active: @(posedge sky130_sram_tb.clk)\n");
    }
    if ((2ULL & vlSelf->__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 1 is active: @(negedge sky130_sram_tb.clk)\n");
    }
    if ((4ULL & vlSelf->__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 2 is active: @(negedge sky130_sram_tb.clk or [true] __VdlySched.awaitingCurrentTime())\n");
    }
    if ((8ULL & vlSelf->__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 3 is active: @([true] __VdlySched.awaitingCurrentTime())\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vsky130_sram_tb___024root___ctor_var_reset(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___ctor_var_reset\n"); );
    // Body
    vlSelf->sky130_sram_tb__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->sky130_sram_tb__DOT__reset = VL_RAND_RESET_I(1);
    vlSelf->sky130_sram_tb__DOT__valid = VL_RAND_RESET_I(1);
    vlSelf->sky130_sram_tb__DOT__write = VL_RAND_RESET_I(1);
    vlSelf->sky130_sram_tb__DOT__address = VL_RAND_RESET_I(32);
    vlSelf->sky130_sram_tb__DOT__mask = VL_RAND_RESET_I(16);
    VL_RAND_RESET_W(128, vlSelf->sky130_sram_tb__DOT__wdata);
    vlSelf->sky130_sram_tb__DOT__fault = VL_RAND_RESET_I(1);
    vlSelf->sky130_sram_tb__DOT__sram_enable = VL_RAND_RESET_I(1);
    vlSelf->sky130_sram_tb__DOT__sram_write = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(128, vlSelf->sky130_sram_tb__DOT__rdata);
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        VL_RAND_RESET_W(128, vlSelf->sky130_sram_tb__DOT__oracle[__Vi0]);
    }
    vlSelf->sky130_sram_tb__DOT__transactions = VL_RAND_RESET_I(32);
    vlSelf->sky130_sram_tb__DOT__commands = VL_RAND_RESET_I(32);
    vlSelf->sky130_sram_tb__DOT__resets = VL_RAND_RESET_I(32);
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__age = VL_RAND_RESET_I(32);
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands = VL_RAND_RESET_I(32);
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__index = VL_RAND_RESET_I(32);
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal = 0;
    vlSelf->sky130_sram_tb__DOT__adapter__DOT__state = VL_RAND_RESET_I(3);
    vlSelf->sky130_sram_tb__DOT__adapter__DOT__write_q = VL_RAND_RESET_I(1);
    vlSelf->sky130_sram_tb__DOT__adapter__DOT__address_q = VL_RAND_RESET_I(9);
    vlSelf->sky130_sram_tb__DOT__adapter__DOT__mask_q = VL_RAND_RESET_I(16);
    VL_RAND_RESET_W(128, vlSelf->sky130_sram_tb__DOT__adapter__DOT__data_q);
    vlSelf->sky130_sram_tb__DOT__adapter__DOT__remaining = VL_RAND_RESET_I(1);
    vlSelf->sky130_sram_tb__DOT__adapter__DOT__legal = VL_RAND_RESET_I(1);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        VL_RAND_RESET_W(128, vlSelf->sky130_sram_tb__DOT__storage__DOT__bank_data[__Vi0]);
    }
    vlSelf->sky130_sram_tb__DOT__storage__DOT__pending = VL_RAND_RESET_I(1);
    vlSelf->sky130_sram_tb__DOT__storage__DOT__selected = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(128, vlSelf->sky130_sram_tb__DOT__storage__DOT__held);
    VL_RAND_RESET_W(128, vlSelf->sky130_sram_tb__DOT__storage__DOT__sampled);
    vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__dout0 = VL_RAND_RESET_I(32);
    vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__dout0 = VL_RAND_RESET_I(32);
    vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__dout0 = VL_RAND_RESET_I(32);
    vlSelf->sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__dout0 = VL_RAND_RESET_I(32);
    vlSelf->sky130_sram_tb__DOT__storage__DOT____VdfgTmp_hcbda1b31__0 = 0;
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__csb0_reg = VL_RAND_RESET_I(1);
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__web0_reg = VL_RAND_RESET_I(1);
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__wmask0_reg = VL_RAND_RESET_I(4);
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__addr0_reg = VL_RAND_RESET_I(9);
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__din0_reg = VL_RAND_RESET_I(32);
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__mem[__Vi0] = VL_RAND_RESET_I(32);
    }
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__csb0_reg = VL_RAND_RESET_I(1);
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__web0_reg = VL_RAND_RESET_I(1);
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__wmask0_reg = VL_RAND_RESET_I(4);
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__addr0_reg = VL_RAND_RESET_I(9);
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__din0_reg = VL_RAND_RESET_I(32);
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__mem[__Vi0] = VL_RAND_RESET_I(32);
    }
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__csb0_reg = VL_RAND_RESET_I(1);
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__web0_reg = VL_RAND_RESET_I(1);
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__wmask0_reg = VL_RAND_RESET_I(4);
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__addr0_reg = VL_RAND_RESET_I(9);
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__din0_reg = VL_RAND_RESET_I(32);
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__mem[__Vi0] = VL_RAND_RESET_I(32);
    }
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__csb0_reg = VL_RAND_RESET_I(1);
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__web0_reg = VL_RAND_RESET_I(1);
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__wmask0_reg = VL_RAND_RESET_I(4);
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__addr0_reg = VL_RAND_RESET_I(9);
    vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__din0_reg = VL_RAND_RESET_I(32);
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__mem[__Vi0] = VL_RAND_RESET_I(32);
    }
    vlSelf->__Vintraval_h7f9437f7__0 = VL_RAND_RESET_I(32);
    vlSelf->__Vintraval_h36210009__0 = VL_RAND_RESET_I(32);
    vlSelf->__Vintraval_hac5192ed__0 = VL_RAND_RESET_I(32);
    vlSelf->__Vintraval_h1c213051__0 = VL_RAND_RESET_I(32);
    vlSelf->__Vdlyvval__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__dout0__v0 = VL_RAND_RESET_I(32);
    vlSelf->__Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__dout0__v0 = 0;
    vlSelf->__Vdlyvval__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__dout0__v0 = VL_RAND_RESET_I(32);
    vlSelf->__Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__dout0__v0 = 0;
    vlSelf->__Vdlyvval__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__dout0__v0 = VL_RAND_RESET_I(32);
    vlSelf->__Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__dout0__v0 = 0;
    vlSelf->__Vdlyvval__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__dout0__v0 = VL_RAND_RESET_I(32);
    vlSelf->__Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__dout0__v0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__sky130_sram_tb__DOT__clk__0 = VL_RAND_RESET_I(1);
}
