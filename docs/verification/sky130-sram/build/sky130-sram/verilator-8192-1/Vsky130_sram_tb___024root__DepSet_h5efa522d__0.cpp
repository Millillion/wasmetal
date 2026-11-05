// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsky130_sram_tb.h for the primary calling header

#include "Vsky130_sram_tb__pch.h"
#include "Vsky130_sram_tb__Syms.h"
#include "Vsky130_sram_tb___024root.h"

VL_INLINE_OPT VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__0(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__0\n"); );
    // Body
    co_await vlSelf->__VdlySched.delay(0x174876e800ULL, 
                                       nullptr, "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       27);
    VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:27: Assertion failed in %Nsky130_sram_tb: macro test watchdog\n",
              64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
    VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 27, "");
}

VL_INLINE_OPT VlCoroutine Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__1(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_initial__TOP__Vtiming__1\n"); );
    // Init
    IData/*31:0*/ sky130_sram_tb__DOT__unnamedblk3__DOT__i;
    sky130_sram_tb__DOT__unnamedblk3__DOT__i = 0;
    IData/*31:0*/ sky130_sram_tb__DOT__unnamedblk4__DOT__i;
    sky130_sram_tb__DOT__unnamedblk4__DOT__i = 0;
    IData/*31:0*/ sky130_sram_tb__DOT__unnamedblk5__DOT__i;
    sky130_sram_tb__DOT__unnamedblk5__DOT__i = 0;
    IData/*31:0*/ sky130_sram_tb__DOT__unnamedblk6__DOT__i;
    sky130_sram_tb__DOT__unnamedblk6__DOT__i = 0;
    CData/*0:0*/ __Vtask_sky130_sram_tb__DOT__request__3__wr;
    __Vtask_sky130_sram_tb__DOT__request__3__wr = 0;
    IData/*31:0*/ __Vtask_sky130_sram_tb__DOT__request__3__addr;
    __Vtask_sky130_sram_tb__DOT__request__3__addr = 0;
    SData/*15:0*/ __Vtask_sky130_sram_tb__DOT__request__3__lanes;
    __Vtask_sky130_sram_tb__DOT__request__3__lanes = 0;
    VlWide<4>/*127:0*/ __Vtask_sky130_sram_tb__DOT__request__3__value;
    VL_ZERO_W(128, __Vtask_sky130_sram_tb__DOT__request__3__value);
    VlWide<4>/*127:0*/ __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout;
    VL_ZERO_W(128, __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout);
    IData/*31:0*/ __Vfunc_sky130_sram_tb__DOT__pattern__4__a;
    __Vfunc_sky130_sram_tb__DOT__pattern__4__a = 0;
    IData/*31:0*/ __Vfunc_sky130_sram_tb__DOT__pattern__4__seed;
    __Vfunc_sky130_sram_tb__DOT__pattern__4__seed = 0;
    CData/*0:0*/ __Vtask_sky130_sram_tb__DOT__request__11__wr;
    __Vtask_sky130_sram_tb__DOT__request__11__wr = 0;
    IData/*31:0*/ __Vtask_sky130_sram_tb__DOT__request__11__addr;
    __Vtask_sky130_sram_tb__DOT__request__11__addr = 0;
    SData/*15:0*/ __Vtask_sky130_sram_tb__DOT__request__11__lanes;
    __Vtask_sky130_sram_tb__DOT__request__11__lanes = 0;
    VlWide<4>/*127:0*/ __Vtask_sky130_sram_tb__DOT__request__11__value;
    VL_ZERO_W(128, __Vtask_sky130_sram_tb__DOT__request__11__value);
    CData/*0:0*/ __Vtask_sky130_sram_tb__DOT__request__18__wr;
    __Vtask_sky130_sram_tb__DOT__request__18__wr = 0;
    IData/*31:0*/ __Vtask_sky130_sram_tb__DOT__request__18__addr;
    __Vtask_sky130_sram_tb__DOT__request__18__addr = 0;
    SData/*15:0*/ __Vtask_sky130_sram_tb__DOT__request__18__lanes;
    __Vtask_sky130_sram_tb__DOT__request__18__lanes = 0;
    VlWide<4>/*127:0*/ __Vtask_sky130_sram_tb__DOT__request__18__value;
    VL_ZERO_W(128, __Vtask_sky130_sram_tb__DOT__request__18__value);
    VlWide<4>/*127:0*/ __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout;
    VL_ZERO_W(128, __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout);
    IData/*31:0*/ __Vfunc_sky130_sram_tb__DOT__pattern__19__a;
    __Vfunc_sky130_sram_tb__DOT__pattern__19__a = 0;
    IData/*31:0*/ __Vfunc_sky130_sram_tb__DOT__pattern__19__seed;
    __Vfunc_sky130_sram_tb__DOT__pattern__19__seed = 0;
    CData/*0:0*/ __Vtask_sky130_sram_tb__DOT__request__26__wr;
    __Vtask_sky130_sram_tb__DOT__request__26__wr = 0;
    IData/*31:0*/ __Vtask_sky130_sram_tb__DOT__request__26__addr;
    __Vtask_sky130_sram_tb__DOT__request__26__addr = 0;
    SData/*15:0*/ __Vtask_sky130_sram_tb__DOT__request__26__lanes;
    __Vtask_sky130_sram_tb__DOT__request__26__lanes = 0;
    VlWide<4>/*127:0*/ __Vtask_sky130_sram_tb__DOT__request__26__value;
    VL_ZERO_W(128, __Vtask_sky130_sram_tb__DOT__request__26__value);
    CData/*0:0*/ __Vtask_sky130_sram_tb__DOT__request__33__wr;
    __Vtask_sky130_sram_tb__DOT__request__33__wr = 0;
    IData/*31:0*/ __Vtask_sky130_sram_tb__DOT__request__33__addr;
    __Vtask_sky130_sram_tb__DOT__request__33__addr = 0;
    SData/*15:0*/ __Vtask_sky130_sram_tb__DOT__request__33__lanes;
    __Vtask_sky130_sram_tb__DOT__request__33__lanes = 0;
    VlWide<4>/*127:0*/ __Vtask_sky130_sram_tb__DOT__request__33__value;
    VL_ZERO_W(128, __Vtask_sky130_sram_tb__DOT__request__33__value);
    CData/*0:0*/ __Vtask_sky130_sram_tb__DOT__request__40__wr;
    __Vtask_sky130_sram_tb__DOT__request__40__wr = 0;
    IData/*31:0*/ __Vtask_sky130_sram_tb__DOT__request__40__addr;
    __Vtask_sky130_sram_tb__DOT__request__40__addr = 0;
    SData/*15:0*/ __Vtask_sky130_sram_tb__DOT__request__40__lanes;
    __Vtask_sky130_sram_tb__DOT__request__40__lanes = 0;
    VlWide<4>/*127:0*/ __Vtask_sky130_sram_tb__DOT__request__40__value;
    VL_ZERO_W(128, __Vtask_sky130_sram_tb__DOT__request__40__value);
    CData/*0:0*/ __Vtask_sky130_sram_tb__DOT__request__47__wr;
    __Vtask_sky130_sram_tb__DOT__request__47__wr = 0;
    IData/*31:0*/ __Vtask_sky130_sram_tb__DOT__request__47__addr;
    __Vtask_sky130_sram_tb__DOT__request__47__addr = 0;
    SData/*15:0*/ __Vtask_sky130_sram_tb__DOT__request__47__lanes;
    __Vtask_sky130_sram_tb__DOT__request__47__lanes = 0;
    VlWide<4>/*127:0*/ __Vtask_sky130_sram_tb__DOT__request__47__value;
    VL_ZERO_W(128, __Vtask_sky130_sram_tb__DOT__request__47__value);
    CData/*0:0*/ __Vtask_sky130_sram_tb__DOT__request__54__wr;
    __Vtask_sky130_sram_tb__DOT__request__54__wr = 0;
    IData/*31:0*/ __Vtask_sky130_sram_tb__DOT__request__54__addr;
    __Vtask_sky130_sram_tb__DOT__request__54__addr = 0;
    SData/*15:0*/ __Vtask_sky130_sram_tb__DOT__request__54__lanes;
    __Vtask_sky130_sram_tb__DOT__request__54__lanes = 0;
    VlWide<4>/*127:0*/ __Vtask_sky130_sram_tb__DOT__request__54__value;
    VL_ZERO_W(128, __Vtask_sky130_sram_tb__DOT__request__54__value);
    CData/*0:0*/ __Vtask_sky130_sram_tb__DOT__request__65__wr;
    __Vtask_sky130_sram_tb__DOT__request__65__wr = 0;
    IData/*31:0*/ __Vtask_sky130_sram_tb__DOT__request__65__addr;
    __Vtask_sky130_sram_tb__DOT__request__65__addr = 0;
    SData/*15:0*/ __Vtask_sky130_sram_tb__DOT__request__65__lanes;
    __Vtask_sky130_sram_tb__DOT__request__65__lanes = 0;
    VlWide<4>/*127:0*/ __Vtask_sky130_sram_tb__DOT__request__65__value;
    VL_ZERO_W(128, __Vtask_sky130_sram_tb__DOT__request__65__value);
    CData/*0:0*/ __Vtask_sky130_sram_tb__DOT__request__79__wr;
    __Vtask_sky130_sram_tb__DOT__request__79__wr = 0;
    IData/*31:0*/ __Vtask_sky130_sram_tb__DOT__request__79__addr;
    __Vtask_sky130_sram_tb__DOT__request__79__addr = 0;
    SData/*15:0*/ __Vtask_sky130_sram_tb__DOT__request__79__lanes;
    __Vtask_sky130_sram_tb__DOT__request__79__lanes = 0;
    VlWide<4>/*127:0*/ __Vtask_sky130_sram_tb__DOT__request__79__value;
    VL_ZERO_W(128, __Vtask_sky130_sram_tb__DOT__request__79__value);
    // Body
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    vlSelf->sky130_sram_tb__DOT__reset = 0U;
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    sky130_sram_tb__DOT__unnamedblk3__DOT__i = 0U;
    while (VL_GTS_III(32, 0x200U, sky130_sram_tb__DOT__unnamedblk3__DOT__i)) {
        __Vfunc_sky130_sram_tb__DOT__pattern__4__seed = 1U;
        __Vfunc_sky130_sram_tb__DOT__pattern__4__a 
            = sky130_sram_tb__DOT__unnamedblk3__DOT__i;
        __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[0U] 
            = ((0xffffff00U & __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[0U]) 
               | (0xffU & ((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__4__a) 
                            ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__4__seed)) 
                           ^ (__Vfunc_sky130_sram_tb__DOT__pattern__4__a 
                              >> 8U))));
        __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[0U] 
            = ((0xffff00ffU & __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[0U]) 
               | (0xff00U & (0x1300U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__4__a) 
                                          ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__4__seed)) 
                                         << 8U) ^ (0xffffff00U 
                                                   & __Vfunc_sky130_sram_tb__DOT__pattern__4__a)))));
        __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[0U] 
            = ((0xff00ffffU & __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[0U]) 
               | (0xff0000U & (0x260000U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__4__a) 
                                              ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__4__seed)) 
                                             << 0x10U) 
                                            ^ (0xffff0000U 
                                               & (__Vfunc_sky130_sram_tb__DOT__pattern__4__a 
                                                  << 8U))))));
        __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[0U] 
            = ((0xffffffU & __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[0U]) 
               | (0xff000000U & (0x39000000U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__4__a) 
                                                  ^ 
                                                  VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__4__seed)) 
                                                 << 0x18U) 
                                                ^ (0xff000000U 
                                                   & (__Vfunc_sky130_sram_tb__DOT__pattern__4__a 
                                                      << 0x10U))))));
        __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[1U] 
            = ((0xffffff00U & __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[1U]) 
               | (0xffU & (0x4cU ^ ((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__4__a) 
                                     ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__4__seed)) 
                                    ^ (__Vfunc_sky130_sram_tb__DOT__pattern__4__a 
                                       >> 8U)))));
        __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[1U] 
            = ((0xffff00ffU & __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[1U]) 
               | (0xff00U & (0x5f00U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__4__a) 
                                          ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__4__seed)) 
                                         << 8U) ^ (0xffffff00U 
                                                   & __Vfunc_sky130_sram_tb__DOT__pattern__4__a)))));
        __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[1U] 
            = ((0xff00ffffU & __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[1U]) 
               | (0xff0000U & (0x720000U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__4__a) 
                                              ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__4__seed)) 
                                             << 0x10U) 
                                            ^ (0xffff0000U 
                                               & (__Vfunc_sky130_sram_tb__DOT__pattern__4__a 
                                                  << 8U))))));
        __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[1U] 
            = ((0xffffffU & __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[1U]) 
               | (0xff000000U & (0x85000000U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__4__a) 
                                                  ^ 
                                                  VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__4__seed)) 
                                                 << 0x18U) 
                                                ^ (0xff000000U 
                                                   & (__Vfunc_sky130_sram_tb__DOT__pattern__4__a 
                                                      << 0x10U))))));
        __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[2U] 
            = ((0xffffff00U & __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[2U]) 
               | (0xffU & (0x98U ^ ((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__4__a) 
                                     ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__4__seed)) 
                                    ^ (__Vfunc_sky130_sram_tb__DOT__pattern__4__a 
                                       >> 8U)))));
        __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[2U] 
            = ((0xffff00ffU & __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[2U]) 
               | (0xff00U & (0xab00U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__4__a) 
                                          ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__4__seed)) 
                                         << 8U) ^ (0xffffff00U 
                                                   & __Vfunc_sky130_sram_tb__DOT__pattern__4__a)))));
        __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[2U] 
            = ((0xff00ffffU & __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[2U]) 
               | (0xff0000U & (0xbe0000U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__4__a) 
                                              ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__4__seed)) 
                                             << 0x10U) 
                                            ^ (0xffff0000U 
                                               & (__Vfunc_sky130_sram_tb__DOT__pattern__4__a 
                                                  << 8U))))));
        __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[2U] 
            = ((0xffffffU & __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[2U]) 
               | (0xff000000U & (0xd1000000U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__4__a) 
                                                  ^ 
                                                  VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__4__seed)) 
                                                 << 0x18U) 
                                                ^ (0xff000000U 
                                                   & (__Vfunc_sky130_sram_tb__DOT__pattern__4__a 
                                                      << 0x10U))))));
        __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[3U] 
            = ((0xffffff00U & __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[3U]) 
               | (0xffU & (0xe4U ^ ((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__4__a) 
                                     ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__4__seed)) 
                                    ^ (__Vfunc_sky130_sram_tb__DOT__pattern__4__a 
                                       >> 8U)))));
        __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[3U] 
            = ((0xffff00ffU & __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[3U]) 
               | (0xff00U & (0xf700U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__4__a) 
                                          ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__4__seed)) 
                                         << 8U) ^ (0xffffff00U 
                                                   & __Vfunc_sky130_sram_tb__DOT__pattern__4__a)))));
        __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[3U] 
            = ((0xff00ffffU & __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[3U]) 
               | (0xff0000U & (0xa0000U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__4__a) 
                                             ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__4__seed)) 
                                            << 0x10U) 
                                           ^ (0xffff0000U 
                                              & (__Vfunc_sky130_sram_tb__DOT__pattern__4__a 
                                                 << 8U))))));
        __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[3U] 
            = ((0xffffffU & __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[3U]) 
               | (0xff000000U & (0x1d000000U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__4__a) 
                                                  ^ 
                                                  VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__4__seed)) 
                                                 << 0x18U) 
                                                ^ (0xff000000U 
                                                   & (__Vfunc_sky130_sram_tb__DOT__pattern__4__a 
                                                      << 0x10U))))));
        __Vtask_sky130_sram_tb__DOT__request__3__value[0U] 
            = __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[0U];
        __Vtask_sky130_sram_tb__DOT__request__3__value[1U] 
            = __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[1U];
        __Vtask_sky130_sram_tb__DOT__request__3__value[2U] 
            = __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[2U];
        __Vtask_sky130_sram_tb__DOT__request__3__value[3U] 
            = __Vfunc_sky130_sram_tb__DOT__pattern__4__Vfuncout[3U];
        __Vtask_sky130_sram_tb__DOT__request__3__lanes = 0xffffU;
        __Vtask_sky130_sram_tb__DOT__request__3__addr 
            = VL_MULS_III(32, (IData)(0x10U), sky130_sram_tb__DOT__unnamedblk3__DOT__i);
        __Vtask_sky130_sram_tb__DOT__request__3__wr = 1U;
        co_await vlSelf->__VtrigSched_h2f20d2d8__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(negedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           36);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           36);
        vlSelf->sky130_sram_tb__DOT__write = __Vtask_sky130_sram_tb__DOT__request__3__wr;
        vlSelf->sky130_sram_tb__DOT__address = __Vtask_sky130_sram_tb__DOT__request__3__addr;
        vlSelf->sky130_sram_tb__DOT__mask = __Vtask_sky130_sram_tb__DOT__request__3__lanes;
        vlSelf->sky130_sram_tb__DOT__wdata[0U] = __Vtask_sky130_sram_tb__DOT__request__3__value[0U];
        vlSelf->sky130_sram_tb__DOT__wdata[1U] = __Vtask_sky130_sram_tb__DOT__request__3__value[1U];
        vlSelf->sky130_sram_tb__DOT__wdata[2U] = __Vtask_sky130_sram_tb__DOT__request__3__value[2U];
        vlSelf->sky130_sram_tb__DOT__wdata[3U] = __Vtask_sky130_sram_tb__DOT__request__3__value[3U];
        vlSelf->sky130_sram_tb__DOT__valid = 1U;
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands 
            = vlSelf->sky130_sram_tb__DOT__commands;
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__age = 0U;
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
            = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
        if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
        }
        while ((3U != (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state))) {
            co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                               nullptr, 
                                                               "@(posedge sky130_sram_tb.clk)", 
                                                               "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                               28);
            co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                               nullptr, 
                                               "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                               28);
            vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
                = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
            if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
                VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                          64,VL_TIME_UNITED_Q(1000),
                          -9,vlSymsp->name());
                VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
            }
        }
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal 
            = (((0x2000U > __Vtask_sky130_sram_tb__DOT__request__3__addr) 
                & (0U == (0xfU & __Vtask_sky130_sram_tb__DOT__request__3__addr))) 
               & (0U != (IData)(__Vtask_sky130_sram_tb__DOT__request__3__lanes)));
        if (VL_UNLIKELY((vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
                         != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                              ? ((IData)(__Vtask_sky130_sram_tb__DOT__request__3__wr)
                                  ? 2U : 3U) : 1U)))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:41: Assertion failed in %Nsky130_sram_tb.request: incorrect response timing\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 41, "");
        }
        if (VL_UNLIKELY(((IData)(vlSelf->sky130_sram_tb__DOT__fault) 
                         != (1U & (~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)))))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:42: Assertion failed in %Nsky130_sram_tb.request: unexpected fault addr=%x\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name(),32,__Vtask_sky130_sram_tb__DOT__request__3__addr);
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 42, "");
        }
        if (VL_UNLIKELY(((vlSelf->sky130_sram_tb__DOT__commands 
                          - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                         != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                              ? 1U : 0U)))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:43: Assertion failed in %Nsky130_sram_tb.request: wrong number of macro commands\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 43, "");
        }
        if ((1U & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)) 
                   | (IData)(__Vtask_sky130_sram_tb__DOT__request__3__wr)))) {
            if (VL_UNLIKELY((0U != (((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                      | vlSelf->sky130_sram_tb__DOT__rdata[1U]) 
                                     | vlSelf->sky130_sram_tb__DOT__rdata[2U]) 
                                    | vlSelf->sky130_sram_tb__DOT__rdata[3U])))) {
                VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:45: Assertion failed in %Nsky130_sram_tb.request: write/fault data not zero\n",
                          64,VL_TIME_UNITED_Q(1000),
                          -9,vlSymsp->name());
                VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 45, "");
            }
        } else if (VL_UNLIKELY((0U != ((((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                          ^ vlSelf->sky130_sram_tb__DOT__oracle
                                          [(0x1ffU 
                                            & (__Vtask_sky130_sram_tb__DOT__request__3__addr 
                                               >> 4U))][0U]) 
                                         | (vlSelf->sky130_sram_tb__DOT__rdata[1U] 
                                            ^ vlSelf->sky130_sram_tb__DOT__oracle
                                            [(0x1ffU 
                                              & (__Vtask_sky130_sram_tb__DOT__request__3__addr 
                                                 >> 4U))][1U])) 
                                        | (vlSelf->sky130_sram_tb__DOT__rdata[2U] 
                                           ^ vlSelf->sky130_sram_tb__DOT__oracle
                                           [(0x1ffU 
                                             & (__Vtask_sky130_sram_tb__DOT__request__3__addr 
                                                >> 4U))][2U])) 
                                       | (vlSelf->sky130_sram_tb__DOT__rdata[3U] 
                                          ^ vlSelf->sky130_sram_tb__DOT__oracle
                                          [(0x1ffU 
                                            & (__Vtask_sky130_sram_tb__DOT__request__3__addr 
                                               >> 4U))][3U]))))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:46: Assertion failed in %Nsky130_sram_tb.request: read differs addr=%x got=%x want=%x\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name(),32,__Vtask_sky130_sram_tb__DOT__request__3__addr,
                      128,vlSelf->sky130_sram_tb__DOT__rdata.data(),
                      128,vlSelf->sky130_sram_tb__DOT__oracle
                      [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__3__addr 
                                  >> 4U))].data());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 46, "");
        }
        if (((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal) 
             & (IData)(__Vtask_sky130_sram_tb__DOT__request__3__wr))) {
            vlSelf->sky130_sram_tb__DOT__request__Vstatic__index 
                = VL_SHIFTR_III(32,32,32, __Vtask_sky130_sram_tb__DOT__request__3__addr, 4U);
            if ((1U & (IData)(__Vtask_sky130_sram_tb__DOT__request__3__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__3__value[0U]));
            }
            if ((2U & (IData)(__Vtask_sky130_sram_tb__DOT__request__3__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__3__value[0U]));
            }
            if ((4U & (IData)(__Vtask_sky130_sram_tb__DOT__request__3__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__3__value[0U]));
            }
            if ((8U & (IData)(__Vtask_sky130_sram_tb__DOT__request__3__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__3__value[0U]));
            }
            if ((0x10U & (IData)(__Vtask_sky130_sram_tb__DOT__request__3__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__3__value[1U]));
            }
            if ((0x20U & (IData)(__Vtask_sky130_sram_tb__DOT__request__3__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__3__value[1U]));
            }
            if ((0x40U & (IData)(__Vtask_sky130_sram_tb__DOT__request__3__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__3__value[1U]));
            }
            if ((0x80U & (IData)(__Vtask_sky130_sram_tb__DOT__request__3__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__3__value[1U]));
            }
            if ((0x100U & (IData)(__Vtask_sky130_sram_tb__DOT__request__3__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__3__value[2U]));
            }
            if ((0x200U & (IData)(__Vtask_sky130_sram_tb__DOT__request__3__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__3__value[2U]));
            }
            if ((0x400U & (IData)(__Vtask_sky130_sram_tb__DOT__request__3__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__3__value[2U]));
            }
            if ((0x800U & (IData)(__Vtask_sky130_sram_tb__DOT__request__3__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__3__value[2U]));
            }
            if ((0x1000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__3__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__3__value[3U]));
            }
            if ((0x2000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__3__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__3__value[3U]));
            }
            if ((0x4000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__3__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__3__value[3U]));
            }
            if ((0x8000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__3__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__3__value[3U]));
            }
        }
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        if (VL_UNLIKELY((((3U == (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state)) 
                          | (IData)(vlSelf->sky130_sram_tb__DOT__sram_enable)) 
                         | ((vlSelf->sky130_sram_tb__DOT__commands 
                             - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                            != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                                 ? 1U : 0U))))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:52: Assertion failed in %Nsky130_sram_tb.request: held request repeated\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 52, "");
        }
        vlSelf->sky130_sram_tb__DOT__valid = 0U;
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        vlSelf->sky130_sram_tb__DOT__transactions = 
            ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__transactions);
        sky130_sram_tb__DOT__unnamedblk3__DOT__i = 
            ((IData)(1U) + sky130_sram_tb__DOT__unnamedblk3__DOT__i);
    }
    sky130_sram_tb__DOT__unnamedblk4__DOT__i = 0U;
    while (VL_GTS_III(32, 0x200U, sky130_sram_tb__DOT__unnamedblk4__DOT__i)) {
        __Vtask_sky130_sram_tb__DOT__request__11__value[0U] = 0U;
        __Vtask_sky130_sram_tb__DOT__request__11__value[1U] = 0U;
        __Vtask_sky130_sram_tb__DOT__request__11__value[2U] = 0U;
        __Vtask_sky130_sram_tb__DOT__request__11__value[3U] = 0U;
        __Vtask_sky130_sram_tb__DOT__request__11__lanes = 0xffffU;
        __Vtask_sky130_sram_tb__DOT__request__11__addr 
            = VL_MULS_III(32, (IData)(0x10U), sky130_sram_tb__DOT__unnamedblk4__DOT__i);
        __Vtask_sky130_sram_tb__DOT__request__11__wr = 0U;
        co_await vlSelf->__VtrigSched_h2f20d2d8__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(negedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           36);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           36);
        vlSelf->sky130_sram_tb__DOT__write = __Vtask_sky130_sram_tb__DOT__request__11__wr;
        vlSelf->sky130_sram_tb__DOT__address = __Vtask_sky130_sram_tb__DOT__request__11__addr;
        vlSelf->sky130_sram_tb__DOT__mask = __Vtask_sky130_sram_tb__DOT__request__11__lanes;
        vlSelf->sky130_sram_tb__DOT__wdata[0U] = __Vtask_sky130_sram_tb__DOT__request__11__value[0U];
        vlSelf->sky130_sram_tb__DOT__wdata[1U] = __Vtask_sky130_sram_tb__DOT__request__11__value[1U];
        vlSelf->sky130_sram_tb__DOT__wdata[2U] = __Vtask_sky130_sram_tb__DOT__request__11__value[2U];
        vlSelf->sky130_sram_tb__DOT__wdata[3U] = __Vtask_sky130_sram_tb__DOT__request__11__value[3U];
        vlSelf->sky130_sram_tb__DOT__valid = 1U;
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands 
            = vlSelf->sky130_sram_tb__DOT__commands;
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__age = 0U;
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
            = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
        if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
        }
        while ((3U != (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state))) {
            co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                               nullptr, 
                                                               "@(posedge sky130_sram_tb.clk)", 
                                                               "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                               28);
            co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                               nullptr, 
                                               "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                               28);
            vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
                = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
            if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
                VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                          64,VL_TIME_UNITED_Q(1000),
                          -9,vlSymsp->name());
                VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
            }
        }
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal 
            = (((0x2000U > __Vtask_sky130_sram_tb__DOT__request__11__addr) 
                & (0U == (0xfU & __Vtask_sky130_sram_tb__DOT__request__11__addr))) 
               & (0U != (IData)(__Vtask_sky130_sram_tb__DOT__request__11__lanes)));
        if (VL_UNLIKELY((vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
                         != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                              ? ((IData)(__Vtask_sky130_sram_tb__DOT__request__11__wr)
                                  ? 2U : 3U) : 1U)))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:41: Assertion failed in %Nsky130_sram_tb.request: incorrect response timing\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 41, "");
        }
        if (VL_UNLIKELY(((IData)(vlSelf->sky130_sram_tb__DOT__fault) 
                         != (1U & (~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)))))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:42: Assertion failed in %Nsky130_sram_tb.request: unexpected fault addr=%x\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name(),32,__Vtask_sky130_sram_tb__DOT__request__11__addr);
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 42, "");
        }
        if (VL_UNLIKELY(((vlSelf->sky130_sram_tb__DOT__commands 
                          - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                         != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                              ? 1U : 0U)))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:43: Assertion failed in %Nsky130_sram_tb.request: wrong number of macro commands\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 43, "");
        }
        if ((1U & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)) 
                   | (IData)(__Vtask_sky130_sram_tb__DOT__request__11__wr)))) {
            if (VL_UNLIKELY((0U != (((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                      | vlSelf->sky130_sram_tb__DOT__rdata[1U]) 
                                     | vlSelf->sky130_sram_tb__DOT__rdata[2U]) 
                                    | vlSelf->sky130_sram_tb__DOT__rdata[3U])))) {
                VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:45: Assertion failed in %Nsky130_sram_tb.request: write/fault data not zero\n",
                          64,VL_TIME_UNITED_Q(1000),
                          -9,vlSymsp->name());
                VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 45, "");
            }
        } else if (VL_UNLIKELY((0U != ((((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                          ^ vlSelf->sky130_sram_tb__DOT__oracle
                                          [(0x1ffU 
                                            & (__Vtask_sky130_sram_tb__DOT__request__11__addr 
                                               >> 4U))][0U]) 
                                         | (vlSelf->sky130_sram_tb__DOT__rdata[1U] 
                                            ^ vlSelf->sky130_sram_tb__DOT__oracle
                                            [(0x1ffU 
                                              & (__Vtask_sky130_sram_tb__DOT__request__11__addr 
                                                 >> 4U))][1U])) 
                                        | (vlSelf->sky130_sram_tb__DOT__rdata[2U] 
                                           ^ vlSelf->sky130_sram_tb__DOT__oracle
                                           [(0x1ffU 
                                             & (__Vtask_sky130_sram_tb__DOT__request__11__addr 
                                                >> 4U))][2U])) 
                                       | (vlSelf->sky130_sram_tb__DOT__rdata[3U] 
                                          ^ vlSelf->sky130_sram_tb__DOT__oracle
                                          [(0x1ffU 
                                            & (__Vtask_sky130_sram_tb__DOT__request__11__addr 
                                               >> 4U))][3U]))))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:46: Assertion failed in %Nsky130_sram_tb.request: read differs addr=%x got=%x want=%x\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name(),32,__Vtask_sky130_sram_tb__DOT__request__11__addr,
                      128,vlSelf->sky130_sram_tb__DOT__rdata.data(),
                      128,vlSelf->sky130_sram_tb__DOT__oracle
                      [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__11__addr 
                                  >> 4U))].data());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 46, "");
        }
        if (((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal) 
             & (IData)(__Vtask_sky130_sram_tb__DOT__request__11__wr))) {
            vlSelf->sky130_sram_tb__DOT__request__Vstatic__index 
                = VL_SHIFTR_III(32,32,32, __Vtask_sky130_sram_tb__DOT__request__11__addr, 4U);
            if ((1U & (IData)(__Vtask_sky130_sram_tb__DOT__request__11__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__11__value[0U]));
            }
            if ((2U & (IData)(__Vtask_sky130_sram_tb__DOT__request__11__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__11__value[0U]));
            }
            if ((4U & (IData)(__Vtask_sky130_sram_tb__DOT__request__11__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__11__value[0U]));
            }
            if ((8U & (IData)(__Vtask_sky130_sram_tb__DOT__request__11__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__11__value[0U]));
            }
            if ((0x10U & (IData)(__Vtask_sky130_sram_tb__DOT__request__11__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__11__value[1U]));
            }
            if ((0x20U & (IData)(__Vtask_sky130_sram_tb__DOT__request__11__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__11__value[1U]));
            }
            if ((0x40U & (IData)(__Vtask_sky130_sram_tb__DOT__request__11__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__11__value[1U]));
            }
            if ((0x80U & (IData)(__Vtask_sky130_sram_tb__DOT__request__11__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__11__value[1U]));
            }
            if ((0x100U & (IData)(__Vtask_sky130_sram_tb__DOT__request__11__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__11__value[2U]));
            }
            if ((0x200U & (IData)(__Vtask_sky130_sram_tb__DOT__request__11__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__11__value[2U]));
            }
            if ((0x400U & (IData)(__Vtask_sky130_sram_tb__DOT__request__11__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__11__value[2U]));
            }
            if ((0x800U & (IData)(__Vtask_sky130_sram_tb__DOT__request__11__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__11__value[2U]));
            }
            if ((0x1000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__11__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__11__value[3U]));
            }
            if ((0x2000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__11__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__11__value[3U]));
            }
            if ((0x4000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__11__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__11__value[3U]));
            }
            if ((0x8000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__11__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__11__value[3U]));
            }
        }
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        if (VL_UNLIKELY((((3U == (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state)) 
                          | (IData)(vlSelf->sky130_sram_tb__DOT__sram_enable)) 
                         | ((vlSelf->sky130_sram_tb__DOT__commands 
                             - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                            != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                                 ? 1U : 0U))))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:52: Assertion failed in %Nsky130_sram_tb.request: held request repeated\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 52, "");
        }
        vlSelf->sky130_sram_tb__DOT__valid = 0U;
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        vlSelf->sky130_sram_tb__DOT__transactions = 
            ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__transactions);
        sky130_sram_tb__DOT__unnamedblk4__DOT__i = 
            ((IData)(1U) + sky130_sram_tb__DOT__unnamedblk4__DOT__i);
    }
    sky130_sram_tb__DOT__unnamedblk5__DOT__i = 1U;
    while (VL_GTES_III(32, 0xffffU, sky130_sram_tb__DOT__unnamedblk5__DOT__i)) {
        __Vfunc_sky130_sram_tb__DOT__pattern__19__seed = 2U;
        __Vfunc_sky130_sram_tb__DOT__pattern__19__a 
            = sky130_sram_tb__DOT__unnamedblk5__DOT__i;
        __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[0U] 
            = ((0xffffff00U & __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[0U]) 
               | (0xffU & ((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__19__a) 
                            ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__19__seed)) 
                           ^ (__Vfunc_sky130_sram_tb__DOT__pattern__19__a 
                              >> 8U))));
        __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[0U] 
            = ((0xffff00ffU & __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[0U]) 
               | (0xff00U & (0x1300U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__19__a) 
                                          ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__19__seed)) 
                                         << 8U) ^ (0xffffff00U 
                                                   & __Vfunc_sky130_sram_tb__DOT__pattern__19__a)))));
        __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[0U] 
            = ((0xff00ffffU & __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[0U]) 
               | (0xff0000U & (0x260000U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__19__a) 
                                              ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__19__seed)) 
                                             << 0x10U) 
                                            ^ (0xffff0000U 
                                               & (__Vfunc_sky130_sram_tb__DOT__pattern__19__a 
                                                  << 8U))))));
        __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[0U] 
            = ((0xffffffU & __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[0U]) 
               | (0xff000000U & (0x39000000U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__19__a) 
                                                  ^ 
                                                  VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__19__seed)) 
                                                 << 0x18U) 
                                                ^ (0xff000000U 
                                                   & (__Vfunc_sky130_sram_tb__DOT__pattern__19__a 
                                                      << 0x10U))))));
        __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[1U] 
            = ((0xffffff00U & __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[1U]) 
               | (0xffU & (0x4cU ^ ((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__19__a) 
                                     ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__19__seed)) 
                                    ^ (__Vfunc_sky130_sram_tb__DOT__pattern__19__a 
                                       >> 8U)))));
        __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[1U] 
            = ((0xffff00ffU & __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[1U]) 
               | (0xff00U & (0x5f00U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__19__a) 
                                          ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__19__seed)) 
                                         << 8U) ^ (0xffffff00U 
                                                   & __Vfunc_sky130_sram_tb__DOT__pattern__19__a)))));
        __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[1U] 
            = ((0xff00ffffU & __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[1U]) 
               | (0xff0000U & (0x720000U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__19__a) 
                                              ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__19__seed)) 
                                             << 0x10U) 
                                            ^ (0xffff0000U 
                                               & (__Vfunc_sky130_sram_tb__DOT__pattern__19__a 
                                                  << 8U))))));
        __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[1U] 
            = ((0xffffffU & __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[1U]) 
               | (0xff000000U & (0x85000000U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__19__a) 
                                                  ^ 
                                                  VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__19__seed)) 
                                                 << 0x18U) 
                                                ^ (0xff000000U 
                                                   & (__Vfunc_sky130_sram_tb__DOT__pattern__19__a 
                                                      << 0x10U))))));
        __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[2U] 
            = ((0xffffff00U & __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[2U]) 
               | (0xffU & (0x98U ^ ((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__19__a) 
                                     ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__19__seed)) 
                                    ^ (__Vfunc_sky130_sram_tb__DOT__pattern__19__a 
                                       >> 8U)))));
        __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[2U] 
            = ((0xffff00ffU & __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[2U]) 
               | (0xff00U & (0xab00U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__19__a) 
                                          ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__19__seed)) 
                                         << 8U) ^ (0xffffff00U 
                                                   & __Vfunc_sky130_sram_tb__DOT__pattern__19__a)))));
        __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[2U] 
            = ((0xff00ffffU & __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[2U]) 
               | (0xff0000U & (0xbe0000U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__19__a) 
                                              ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__19__seed)) 
                                             << 0x10U) 
                                            ^ (0xffff0000U 
                                               & (__Vfunc_sky130_sram_tb__DOT__pattern__19__a 
                                                  << 8U))))));
        __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[2U] 
            = ((0xffffffU & __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[2U]) 
               | (0xff000000U & (0xd1000000U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__19__a) 
                                                  ^ 
                                                  VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__19__seed)) 
                                                 << 0x18U) 
                                                ^ (0xff000000U 
                                                   & (__Vfunc_sky130_sram_tb__DOT__pattern__19__a 
                                                      << 0x10U))))));
        __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[3U] 
            = ((0xffffff00U & __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[3U]) 
               | (0xffU & (0xe4U ^ ((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__19__a) 
                                     ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__19__seed)) 
                                    ^ (__Vfunc_sky130_sram_tb__DOT__pattern__19__a 
                                       >> 8U)))));
        __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[3U] 
            = ((0xffff00ffU & __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[3U]) 
               | (0xff00U & (0xf700U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__19__a) 
                                          ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__19__seed)) 
                                         << 8U) ^ (0xffffff00U 
                                                   & __Vfunc_sky130_sram_tb__DOT__pattern__19__a)))));
        __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[3U] 
            = ((0xff00ffffU & __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[3U]) 
               | (0xff0000U & (0xa0000U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__19__a) 
                                             ^ VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__19__seed)) 
                                            << 0x10U) 
                                           ^ (0xffff0000U 
                                              & (__Vfunc_sky130_sram_tb__DOT__pattern__19__a 
                                                 << 8U))))));
        __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[3U] 
            = ((0xffffffU & __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[3U]) 
               | (0xff000000U & (0x1d000000U ^ (((VL_MULS_III(32, (IData)(0x49U), __Vfunc_sky130_sram_tb__DOT__pattern__19__a) 
                                                  ^ 
                                                  VL_MULS_III(32, (IData)(0x1fU), __Vfunc_sky130_sram_tb__DOT__pattern__19__seed)) 
                                                 << 0x18U) 
                                                ^ (0xff000000U 
                                                   & (__Vfunc_sky130_sram_tb__DOT__pattern__19__a 
                                                      << 0x10U))))));
        __Vtask_sky130_sram_tb__DOT__request__18__value[0U] 
            = __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[0U];
        __Vtask_sky130_sram_tb__DOT__request__18__value[1U] 
            = __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[1U];
        __Vtask_sky130_sram_tb__DOT__request__18__value[2U] 
            = __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[2U];
        __Vtask_sky130_sram_tb__DOT__request__18__value[3U] 
            = __Vfunc_sky130_sram_tb__DOT__pattern__19__Vfuncout[3U];
        __Vtask_sky130_sram_tb__DOT__request__18__lanes 
            = (0xffffU & sky130_sram_tb__DOT__unnamedblk5__DOT__i);
        __Vtask_sky130_sram_tb__DOT__request__18__addr 
            = VL_MULS_III(32, (IData)(0x10U), VL_MODDIVS_III(32, 
                                                             VL_MULS_III(32, (IData)(0x61U), sky130_sram_tb__DOT__unnamedblk5__DOT__i), (IData)(0x200U)));
        __Vtask_sky130_sram_tb__DOT__request__18__wr = 1U;
        co_await vlSelf->__VtrigSched_h2f20d2d8__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(negedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           36);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           36);
        vlSelf->sky130_sram_tb__DOT__write = __Vtask_sky130_sram_tb__DOT__request__18__wr;
        vlSelf->sky130_sram_tb__DOT__address = __Vtask_sky130_sram_tb__DOT__request__18__addr;
        vlSelf->sky130_sram_tb__DOT__mask = __Vtask_sky130_sram_tb__DOT__request__18__lanes;
        vlSelf->sky130_sram_tb__DOT__wdata[0U] = __Vtask_sky130_sram_tb__DOT__request__18__value[0U];
        vlSelf->sky130_sram_tb__DOT__wdata[1U] = __Vtask_sky130_sram_tb__DOT__request__18__value[1U];
        vlSelf->sky130_sram_tb__DOT__wdata[2U] = __Vtask_sky130_sram_tb__DOT__request__18__value[2U];
        vlSelf->sky130_sram_tb__DOT__wdata[3U] = __Vtask_sky130_sram_tb__DOT__request__18__value[3U];
        vlSelf->sky130_sram_tb__DOT__valid = 1U;
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands 
            = vlSelf->sky130_sram_tb__DOT__commands;
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__age = 0U;
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
            = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
        if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
        }
        while ((3U != (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state))) {
            co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                               nullptr, 
                                                               "@(posedge sky130_sram_tb.clk)", 
                                                               "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                               28);
            co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                               nullptr, 
                                               "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                               28);
            vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
                = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
            if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
                VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                          64,VL_TIME_UNITED_Q(1000),
                          -9,vlSymsp->name());
                VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
            }
        }
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal 
            = (((0x2000U > __Vtask_sky130_sram_tb__DOT__request__18__addr) 
                & (0U == (0xfU & __Vtask_sky130_sram_tb__DOT__request__18__addr))) 
               & (0U != (IData)(__Vtask_sky130_sram_tb__DOT__request__18__lanes)));
        if (VL_UNLIKELY((vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
                         != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                              ? ((IData)(__Vtask_sky130_sram_tb__DOT__request__18__wr)
                                  ? 2U : 3U) : 1U)))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:41: Assertion failed in %Nsky130_sram_tb.request: incorrect response timing\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 41, "");
        }
        if (VL_UNLIKELY(((IData)(vlSelf->sky130_sram_tb__DOT__fault) 
                         != (1U & (~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)))))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:42: Assertion failed in %Nsky130_sram_tb.request: unexpected fault addr=%x\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name(),32,__Vtask_sky130_sram_tb__DOT__request__18__addr);
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 42, "");
        }
        if (VL_UNLIKELY(((vlSelf->sky130_sram_tb__DOT__commands 
                          - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                         != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                              ? 1U : 0U)))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:43: Assertion failed in %Nsky130_sram_tb.request: wrong number of macro commands\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 43, "");
        }
        if ((1U & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)) 
                   | (IData)(__Vtask_sky130_sram_tb__DOT__request__18__wr)))) {
            if (VL_UNLIKELY((0U != (((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                      | vlSelf->sky130_sram_tb__DOT__rdata[1U]) 
                                     | vlSelf->sky130_sram_tb__DOT__rdata[2U]) 
                                    | vlSelf->sky130_sram_tb__DOT__rdata[3U])))) {
                VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:45: Assertion failed in %Nsky130_sram_tb.request: write/fault data not zero\n",
                          64,VL_TIME_UNITED_Q(1000),
                          -9,vlSymsp->name());
                VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 45, "");
            }
        } else if (VL_UNLIKELY((0U != ((((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                          ^ vlSelf->sky130_sram_tb__DOT__oracle
                                          [(0x1ffU 
                                            & (__Vtask_sky130_sram_tb__DOT__request__18__addr 
                                               >> 4U))][0U]) 
                                         | (vlSelf->sky130_sram_tb__DOT__rdata[1U] 
                                            ^ vlSelf->sky130_sram_tb__DOT__oracle
                                            [(0x1ffU 
                                              & (__Vtask_sky130_sram_tb__DOT__request__18__addr 
                                                 >> 4U))][1U])) 
                                        | (vlSelf->sky130_sram_tb__DOT__rdata[2U] 
                                           ^ vlSelf->sky130_sram_tb__DOT__oracle
                                           [(0x1ffU 
                                             & (__Vtask_sky130_sram_tb__DOT__request__18__addr 
                                                >> 4U))][2U])) 
                                       | (vlSelf->sky130_sram_tb__DOT__rdata[3U] 
                                          ^ vlSelf->sky130_sram_tb__DOT__oracle
                                          [(0x1ffU 
                                            & (__Vtask_sky130_sram_tb__DOT__request__18__addr 
                                               >> 4U))][3U]))))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:46: Assertion failed in %Nsky130_sram_tb.request: read differs addr=%x got=%x want=%x\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name(),32,__Vtask_sky130_sram_tb__DOT__request__18__addr,
                      128,vlSelf->sky130_sram_tb__DOT__rdata.data(),
                      128,vlSelf->sky130_sram_tb__DOT__oracle
                      [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__18__addr 
                                  >> 4U))].data());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 46, "");
        }
        if (((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal) 
             & (IData)(__Vtask_sky130_sram_tb__DOT__request__18__wr))) {
            vlSelf->sky130_sram_tb__DOT__request__Vstatic__index 
                = VL_SHIFTR_III(32,32,32, __Vtask_sky130_sram_tb__DOT__request__18__addr, 4U);
            if ((1U & (IData)(__Vtask_sky130_sram_tb__DOT__request__18__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__18__value[0U]));
            }
            if ((2U & (IData)(__Vtask_sky130_sram_tb__DOT__request__18__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__18__value[0U]));
            }
            if ((4U & (IData)(__Vtask_sky130_sram_tb__DOT__request__18__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__18__value[0U]));
            }
            if ((8U & (IData)(__Vtask_sky130_sram_tb__DOT__request__18__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__18__value[0U]));
            }
            if ((0x10U & (IData)(__Vtask_sky130_sram_tb__DOT__request__18__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__18__value[1U]));
            }
            if ((0x20U & (IData)(__Vtask_sky130_sram_tb__DOT__request__18__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__18__value[1U]));
            }
            if ((0x40U & (IData)(__Vtask_sky130_sram_tb__DOT__request__18__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__18__value[1U]));
            }
            if ((0x80U & (IData)(__Vtask_sky130_sram_tb__DOT__request__18__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__18__value[1U]));
            }
            if ((0x100U & (IData)(__Vtask_sky130_sram_tb__DOT__request__18__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__18__value[2U]));
            }
            if ((0x200U & (IData)(__Vtask_sky130_sram_tb__DOT__request__18__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__18__value[2U]));
            }
            if ((0x400U & (IData)(__Vtask_sky130_sram_tb__DOT__request__18__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__18__value[2U]));
            }
            if ((0x800U & (IData)(__Vtask_sky130_sram_tb__DOT__request__18__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__18__value[2U]));
            }
            if ((0x1000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__18__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__18__value[3U]));
            }
            if ((0x2000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__18__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__18__value[3U]));
            }
            if ((0x4000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__18__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__18__value[3U]));
            }
            if ((0x8000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__18__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__18__value[3U]));
            }
        }
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        if (VL_UNLIKELY((((3U == (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state)) 
                          | (IData)(vlSelf->sky130_sram_tb__DOT__sram_enable)) 
                         | ((vlSelf->sky130_sram_tb__DOT__commands 
                             - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                            != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                                 ? 1U : 0U))))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:52: Assertion failed in %Nsky130_sram_tb.request: held request repeated\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 52, "");
        }
        vlSelf->sky130_sram_tb__DOT__valid = 0U;
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        vlSelf->sky130_sram_tb__DOT__transactions = 
            ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__transactions);
        __Vtask_sky130_sram_tb__DOT__request__26__value[0U] = 0U;
        __Vtask_sky130_sram_tb__DOT__request__26__value[1U] = 0U;
        __Vtask_sky130_sram_tb__DOT__request__26__value[2U] = 0U;
        __Vtask_sky130_sram_tb__DOT__request__26__value[3U] = 0U;
        __Vtask_sky130_sram_tb__DOT__request__26__lanes = 0xffffU;
        __Vtask_sky130_sram_tb__DOT__request__26__addr 
            = VL_MULS_III(32, (IData)(0x10U), VL_MODDIVS_III(32, 
                                                             VL_MULS_III(32, (IData)(0x61U), sky130_sram_tb__DOT__unnamedblk5__DOT__i), (IData)(0x200U)));
        __Vtask_sky130_sram_tb__DOT__request__26__wr = 0U;
        co_await vlSelf->__VtrigSched_h2f20d2d8__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(negedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           36);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           36);
        vlSelf->sky130_sram_tb__DOT__write = __Vtask_sky130_sram_tb__DOT__request__26__wr;
        vlSelf->sky130_sram_tb__DOT__address = __Vtask_sky130_sram_tb__DOT__request__26__addr;
        vlSelf->sky130_sram_tb__DOT__mask = __Vtask_sky130_sram_tb__DOT__request__26__lanes;
        vlSelf->sky130_sram_tb__DOT__wdata[0U] = __Vtask_sky130_sram_tb__DOT__request__26__value[0U];
        vlSelf->sky130_sram_tb__DOT__wdata[1U] = __Vtask_sky130_sram_tb__DOT__request__26__value[1U];
        vlSelf->sky130_sram_tb__DOT__wdata[2U] = __Vtask_sky130_sram_tb__DOT__request__26__value[2U];
        vlSelf->sky130_sram_tb__DOT__wdata[3U] = __Vtask_sky130_sram_tb__DOT__request__26__value[3U];
        vlSelf->sky130_sram_tb__DOT__valid = 1U;
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands 
            = vlSelf->sky130_sram_tb__DOT__commands;
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__age = 0U;
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
            = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
        if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
        }
        while ((3U != (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state))) {
            co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                               nullptr, 
                                                               "@(posedge sky130_sram_tb.clk)", 
                                                               "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                               28);
            co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                               nullptr, 
                                               "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                               28);
            vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
                = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
            if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
                VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                          64,VL_TIME_UNITED_Q(1000),
                          -9,vlSymsp->name());
                VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
            }
        }
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal 
            = (((0x2000U > __Vtask_sky130_sram_tb__DOT__request__26__addr) 
                & (0U == (0xfU & __Vtask_sky130_sram_tb__DOT__request__26__addr))) 
               & (0U != (IData)(__Vtask_sky130_sram_tb__DOT__request__26__lanes)));
        if (VL_UNLIKELY((vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
                         != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                              ? ((IData)(__Vtask_sky130_sram_tb__DOT__request__26__wr)
                                  ? 2U : 3U) : 1U)))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:41: Assertion failed in %Nsky130_sram_tb.request: incorrect response timing\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 41, "");
        }
        if (VL_UNLIKELY(((IData)(vlSelf->sky130_sram_tb__DOT__fault) 
                         != (1U & (~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)))))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:42: Assertion failed in %Nsky130_sram_tb.request: unexpected fault addr=%x\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name(),32,__Vtask_sky130_sram_tb__DOT__request__26__addr);
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 42, "");
        }
        if (VL_UNLIKELY(((vlSelf->sky130_sram_tb__DOT__commands 
                          - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                         != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                              ? 1U : 0U)))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:43: Assertion failed in %Nsky130_sram_tb.request: wrong number of macro commands\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 43, "");
        }
        if ((1U & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)) 
                   | (IData)(__Vtask_sky130_sram_tb__DOT__request__26__wr)))) {
            if (VL_UNLIKELY((0U != (((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                      | vlSelf->sky130_sram_tb__DOT__rdata[1U]) 
                                     | vlSelf->sky130_sram_tb__DOT__rdata[2U]) 
                                    | vlSelf->sky130_sram_tb__DOT__rdata[3U])))) {
                VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:45: Assertion failed in %Nsky130_sram_tb.request: write/fault data not zero\n",
                          64,VL_TIME_UNITED_Q(1000),
                          -9,vlSymsp->name());
                VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 45, "");
            }
        } else if (VL_UNLIKELY((0U != ((((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                          ^ vlSelf->sky130_sram_tb__DOT__oracle
                                          [(0x1ffU 
                                            & (__Vtask_sky130_sram_tb__DOT__request__26__addr 
                                               >> 4U))][0U]) 
                                         | (vlSelf->sky130_sram_tb__DOT__rdata[1U] 
                                            ^ vlSelf->sky130_sram_tb__DOT__oracle
                                            [(0x1ffU 
                                              & (__Vtask_sky130_sram_tb__DOT__request__26__addr 
                                                 >> 4U))][1U])) 
                                        | (vlSelf->sky130_sram_tb__DOT__rdata[2U] 
                                           ^ vlSelf->sky130_sram_tb__DOT__oracle
                                           [(0x1ffU 
                                             & (__Vtask_sky130_sram_tb__DOT__request__26__addr 
                                                >> 4U))][2U])) 
                                       | (vlSelf->sky130_sram_tb__DOT__rdata[3U] 
                                          ^ vlSelf->sky130_sram_tb__DOT__oracle
                                          [(0x1ffU 
                                            & (__Vtask_sky130_sram_tb__DOT__request__26__addr 
                                               >> 4U))][3U]))))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:46: Assertion failed in %Nsky130_sram_tb.request: read differs addr=%x got=%x want=%x\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name(),32,__Vtask_sky130_sram_tb__DOT__request__26__addr,
                      128,vlSelf->sky130_sram_tb__DOT__rdata.data(),
                      128,vlSelf->sky130_sram_tb__DOT__oracle
                      [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__26__addr 
                                  >> 4U))].data());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 46, "");
        }
        if (((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal) 
             & (IData)(__Vtask_sky130_sram_tb__DOT__request__26__wr))) {
            vlSelf->sky130_sram_tb__DOT__request__Vstatic__index 
                = VL_SHIFTR_III(32,32,32, __Vtask_sky130_sram_tb__DOT__request__26__addr, 4U);
            if ((1U & (IData)(__Vtask_sky130_sram_tb__DOT__request__26__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__26__value[0U]));
            }
            if ((2U & (IData)(__Vtask_sky130_sram_tb__DOT__request__26__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__26__value[0U]));
            }
            if ((4U & (IData)(__Vtask_sky130_sram_tb__DOT__request__26__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__26__value[0U]));
            }
            if ((8U & (IData)(__Vtask_sky130_sram_tb__DOT__request__26__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__26__value[0U]));
            }
            if ((0x10U & (IData)(__Vtask_sky130_sram_tb__DOT__request__26__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__26__value[1U]));
            }
            if ((0x20U & (IData)(__Vtask_sky130_sram_tb__DOT__request__26__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__26__value[1U]));
            }
            if ((0x40U & (IData)(__Vtask_sky130_sram_tb__DOT__request__26__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__26__value[1U]));
            }
            if ((0x80U & (IData)(__Vtask_sky130_sram_tb__DOT__request__26__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__26__value[1U]));
            }
            if ((0x100U & (IData)(__Vtask_sky130_sram_tb__DOT__request__26__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__26__value[2U]));
            }
            if ((0x200U & (IData)(__Vtask_sky130_sram_tb__DOT__request__26__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__26__value[2U]));
            }
            if ((0x400U & (IData)(__Vtask_sky130_sram_tb__DOT__request__26__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__26__value[2U]));
            }
            if ((0x800U & (IData)(__Vtask_sky130_sram_tb__DOT__request__26__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__26__value[2U]));
            }
            if ((0x1000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__26__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__26__value[3U]));
            }
            if ((0x2000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__26__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__26__value[3U]));
            }
            if ((0x4000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__26__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__26__value[3U]));
            }
            if ((0x8000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__26__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__26__value[3U]));
            }
        }
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        if (VL_UNLIKELY((((3U == (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state)) 
                          | (IData)(vlSelf->sky130_sram_tb__DOT__sram_enable)) 
                         | ((vlSelf->sky130_sram_tb__DOT__commands 
                             - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                            != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                                 ? 1U : 0U))))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:52: Assertion failed in %Nsky130_sram_tb.request: held request repeated\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 52, "");
        }
        vlSelf->sky130_sram_tb__DOT__valid = 0U;
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        vlSelf->sky130_sram_tb__DOT__transactions = 
            ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__transactions);
        sky130_sram_tb__DOT__unnamedblk5__DOT__i = 
            ((IData)(1U) + sky130_sram_tb__DOT__unnamedblk5__DOT__i);
    }
    __Vtask_sky130_sram_tb__DOT__request__33__value[0U] = 0U;
    __Vtask_sky130_sram_tb__DOT__request__33__value[1U] = 0U;
    __Vtask_sky130_sram_tb__DOT__request__33__value[2U] = 0U;
    __Vtask_sky130_sram_tb__DOT__request__33__value[3U] = 0U;
    __Vtask_sky130_sram_tb__DOT__request__33__lanes = 0U;
    __Vtask_sky130_sram_tb__DOT__request__33__addr = 0U;
    __Vtask_sky130_sram_tb__DOT__request__33__wr = 0U;
    co_await vlSelf->__VtrigSched_h2f20d2d8__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(negedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       36);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       36);
    vlSelf->sky130_sram_tb__DOT__write = __Vtask_sky130_sram_tb__DOT__request__33__wr;
    vlSelf->sky130_sram_tb__DOT__address = __Vtask_sky130_sram_tb__DOT__request__33__addr;
    vlSelf->sky130_sram_tb__DOT__mask = __Vtask_sky130_sram_tb__DOT__request__33__lanes;
    vlSelf->sky130_sram_tb__DOT__wdata[0U] = __Vtask_sky130_sram_tb__DOT__request__33__value[0U];
    vlSelf->sky130_sram_tb__DOT__wdata[1U] = __Vtask_sky130_sram_tb__DOT__request__33__value[1U];
    vlSelf->sky130_sram_tb__DOT__wdata[2U] = __Vtask_sky130_sram_tb__DOT__request__33__value[2U];
    vlSelf->sky130_sram_tb__DOT__wdata[3U] = __Vtask_sky130_sram_tb__DOT__request__33__value[3U];
    vlSelf->sky130_sram_tb__DOT__valid = 1U;
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands 
        = vlSelf->sky130_sram_tb__DOT__commands;
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__age = 0U;
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
        = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
    if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
    }
    while ((3U != (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state))) {
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
            = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
        if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
        }
    }
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal 
        = (((0x2000U > __Vtask_sky130_sram_tb__DOT__request__33__addr) 
            & (0U == (0xfU & __Vtask_sky130_sram_tb__DOT__request__33__addr))) 
           & (0U != (IData)(__Vtask_sky130_sram_tb__DOT__request__33__lanes)));
    if (VL_UNLIKELY((vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
                     != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                          ? ((IData)(__Vtask_sky130_sram_tb__DOT__request__33__wr)
                              ? 2U : 3U) : 1U)))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:41: Assertion failed in %Nsky130_sram_tb.request: incorrect response timing\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 41, "");
    }
    if (VL_UNLIKELY(((IData)(vlSelf->sky130_sram_tb__DOT__fault) 
                     != (1U & (~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)))))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:42: Assertion failed in %Nsky130_sram_tb.request: unexpected fault addr=%x\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name(),
                  32,__Vtask_sky130_sram_tb__DOT__request__33__addr);
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 42, "");
    }
    if (VL_UNLIKELY(((vlSelf->sky130_sram_tb__DOT__commands 
                      - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                     != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                          ? 1U : 0U)))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:43: Assertion failed in %Nsky130_sram_tb.request: wrong number of macro commands\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 43, "");
    }
    if ((1U & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)) 
               | (IData)(__Vtask_sky130_sram_tb__DOT__request__33__wr)))) {
        if (VL_UNLIKELY((0U != (((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                  | vlSelf->sky130_sram_tb__DOT__rdata[1U]) 
                                 | vlSelf->sky130_sram_tb__DOT__rdata[2U]) 
                                | vlSelf->sky130_sram_tb__DOT__rdata[3U])))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:45: Assertion failed in %Nsky130_sram_tb.request: write/fault data not zero\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 45, "");
        }
    } else if (VL_UNLIKELY((0U != ((((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                      ^ vlSelf->sky130_sram_tb__DOT__oracle
                                      [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__33__addr 
                                                  >> 4U))][0U]) 
                                     | (vlSelf->sky130_sram_tb__DOT__rdata[1U] 
                                        ^ vlSelf->sky130_sram_tb__DOT__oracle
                                        [(0x1ffU & 
                                          (__Vtask_sky130_sram_tb__DOT__request__33__addr 
                                           >> 4U))][1U])) 
                                    | (vlSelf->sky130_sram_tb__DOT__rdata[2U] 
                                       ^ vlSelf->sky130_sram_tb__DOT__oracle
                                       [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__33__addr 
                                                   >> 4U))][2U])) 
                                   | (vlSelf->sky130_sram_tb__DOT__rdata[3U] 
                                      ^ vlSelf->sky130_sram_tb__DOT__oracle
                                      [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__33__addr 
                                                  >> 4U))][3U]))))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:46: Assertion failed in %Nsky130_sram_tb.request: read differs addr=%x got=%x want=%x\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name(),
                  32,__Vtask_sky130_sram_tb__DOT__request__33__addr,
                  128,vlSelf->sky130_sram_tb__DOT__rdata.data(),
                  128,vlSelf->sky130_sram_tb__DOT__oracle
                  [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__33__addr 
                              >> 4U))].data());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 46, "");
    }
    if (((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal) 
         & (IData)(__Vtask_sky130_sram_tb__DOT__request__33__wr))) {
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__index 
            = VL_SHIFTR_III(32,32,32, __Vtask_sky130_sram_tb__DOT__request__33__addr, 4U);
        if ((1U & (IData)(__Vtask_sky130_sram_tb__DOT__request__33__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__33__value[0U]));
        }
        if ((2U & (IData)(__Vtask_sky130_sram_tb__DOT__request__33__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__33__value[0U]));
        }
        if ((4U & (IData)(__Vtask_sky130_sram_tb__DOT__request__33__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__33__value[0U]));
        }
        if ((8U & (IData)(__Vtask_sky130_sram_tb__DOT__request__33__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__33__value[0U]));
        }
        if ((0x10U & (IData)(__Vtask_sky130_sram_tb__DOT__request__33__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__33__value[1U]));
        }
        if ((0x20U & (IData)(__Vtask_sky130_sram_tb__DOT__request__33__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__33__value[1U]));
        }
        if ((0x40U & (IData)(__Vtask_sky130_sram_tb__DOT__request__33__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__33__value[1U]));
        }
        if ((0x80U & (IData)(__Vtask_sky130_sram_tb__DOT__request__33__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__33__value[1U]));
        }
        if ((0x100U & (IData)(__Vtask_sky130_sram_tb__DOT__request__33__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__33__value[2U]));
        }
        if ((0x200U & (IData)(__Vtask_sky130_sram_tb__DOT__request__33__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__33__value[2U]));
        }
        if ((0x400U & (IData)(__Vtask_sky130_sram_tb__DOT__request__33__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__33__value[2U]));
        }
        if ((0x800U & (IData)(__Vtask_sky130_sram_tb__DOT__request__33__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__33__value[2U]));
        }
        if ((0x1000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__33__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__33__value[3U]));
        }
        if ((0x2000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__33__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__33__value[3U]));
        }
        if ((0x4000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__33__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__33__value[3U]));
        }
        if ((0x8000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__33__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__33__value[3U]));
        }
    }
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    if (VL_UNLIKELY((((3U == (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state)) 
                      | (IData)(vlSelf->sky130_sram_tb__DOT__sram_enable)) 
                     | ((vlSelf->sky130_sram_tb__DOT__commands 
                         - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                        != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                             ? 1U : 0U))))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:52: Assertion failed in %Nsky130_sram_tb.request: held request repeated\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 52, "");
    }
    vlSelf->sky130_sram_tb__DOT__valid = 0U;
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    vlSelf->sky130_sram_tb__DOT__transactions = ((IData)(1U) 
                                                 + vlSelf->sky130_sram_tb__DOT__transactions);
    __Vtask_sky130_sram_tb__DOT__request__40__value[0U] = 0xffffffffU;
    __Vtask_sky130_sram_tb__DOT__request__40__value[1U] = 0xffffffffU;
    __Vtask_sky130_sram_tb__DOT__request__40__value[2U] = 0xffffffffU;
    __Vtask_sky130_sram_tb__DOT__request__40__value[3U] = 0xffffffffU;
    __Vtask_sky130_sram_tb__DOT__request__40__lanes = 0xffffU;
    __Vtask_sky130_sram_tb__DOT__request__40__addr = 1U;
    __Vtask_sky130_sram_tb__DOT__request__40__wr = 1U;
    co_await vlSelf->__VtrigSched_h2f20d2d8__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(negedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       36);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       36);
    vlSelf->sky130_sram_tb__DOT__write = __Vtask_sky130_sram_tb__DOT__request__40__wr;
    vlSelf->sky130_sram_tb__DOT__address = __Vtask_sky130_sram_tb__DOT__request__40__addr;
    vlSelf->sky130_sram_tb__DOT__mask = __Vtask_sky130_sram_tb__DOT__request__40__lanes;
    vlSelf->sky130_sram_tb__DOT__wdata[0U] = __Vtask_sky130_sram_tb__DOT__request__40__value[0U];
    vlSelf->sky130_sram_tb__DOT__wdata[1U] = __Vtask_sky130_sram_tb__DOT__request__40__value[1U];
    vlSelf->sky130_sram_tb__DOT__wdata[2U] = __Vtask_sky130_sram_tb__DOT__request__40__value[2U];
    vlSelf->sky130_sram_tb__DOT__wdata[3U] = __Vtask_sky130_sram_tb__DOT__request__40__value[3U];
    vlSelf->sky130_sram_tb__DOT__valid = 1U;
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands 
        = vlSelf->sky130_sram_tb__DOT__commands;
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__age = 0U;
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
        = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
    if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
    }
    while ((3U != (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state))) {
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
            = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
        if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
        }
    }
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal 
        = (((0x2000U > __Vtask_sky130_sram_tb__DOT__request__40__addr) 
            & (0U == (0xfU & __Vtask_sky130_sram_tb__DOT__request__40__addr))) 
           & (0U != (IData)(__Vtask_sky130_sram_tb__DOT__request__40__lanes)));
    if (VL_UNLIKELY((vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
                     != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                          ? ((IData)(__Vtask_sky130_sram_tb__DOT__request__40__wr)
                              ? 2U : 3U) : 1U)))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:41: Assertion failed in %Nsky130_sram_tb.request: incorrect response timing\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 41, "");
    }
    if (VL_UNLIKELY(((IData)(vlSelf->sky130_sram_tb__DOT__fault) 
                     != (1U & (~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)))))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:42: Assertion failed in %Nsky130_sram_tb.request: unexpected fault addr=%x\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name(),
                  32,__Vtask_sky130_sram_tb__DOT__request__40__addr);
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 42, "");
    }
    if (VL_UNLIKELY(((vlSelf->sky130_sram_tb__DOT__commands 
                      - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                     != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                          ? 1U : 0U)))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:43: Assertion failed in %Nsky130_sram_tb.request: wrong number of macro commands\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 43, "");
    }
    if ((1U & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)) 
               | (IData)(__Vtask_sky130_sram_tb__DOT__request__40__wr)))) {
        if (VL_UNLIKELY((0U != (((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                  | vlSelf->sky130_sram_tb__DOT__rdata[1U]) 
                                 | vlSelf->sky130_sram_tb__DOT__rdata[2U]) 
                                | vlSelf->sky130_sram_tb__DOT__rdata[3U])))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:45: Assertion failed in %Nsky130_sram_tb.request: write/fault data not zero\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 45, "");
        }
    } else if (VL_UNLIKELY((0U != ((((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                      ^ vlSelf->sky130_sram_tb__DOT__oracle
                                      [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__40__addr 
                                                  >> 4U))][0U]) 
                                     | (vlSelf->sky130_sram_tb__DOT__rdata[1U] 
                                        ^ vlSelf->sky130_sram_tb__DOT__oracle
                                        [(0x1ffU & 
                                          (__Vtask_sky130_sram_tb__DOT__request__40__addr 
                                           >> 4U))][1U])) 
                                    | (vlSelf->sky130_sram_tb__DOT__rdata[2U] 
                                       ^ vlSelf->sky130_sram_tb__DOT__oracle
                                       [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__40__addr 
                                                   >> 4U))][2U])) 
                                   | (vlSelf->sky130_sram_tb__DOT__rdata[3U] 
                                      ^ vlSelf->sky130_sram_tb__DOT__oracle
                                      [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__40__addr 
                                                  >> 4U))][3U]))))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:46: Assertion failed in %Nsky130_sram_tb.request: read differs addr=%x got=%x want=%x\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name(),
                  32,__Vtask_sky130_sram_tb__DOT__request__40__addr,
                  128,vlSelf->sky130_sram_tb__DOT__rdata.data(),
                  128,vlSelf->sky130_sram_tb__DOT__oracle
                  [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__40__addr 
                              >> 4U))].data());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 46, "");
    }
    if (((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal) 
         & (IData)(__Vtask_sky130_sram_tb__DOT__request__40__wr))) {
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__index 
            = VL_SHIFTR_III(32,32,32, __Vtask_sky130_sram_tb__DOT__request__40__addr, 4U);
        if ((1U & (IData)(__Vtask_sky130_sram_tb__DOT__request__40__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__40__value[0U]));
        }
        if ((2U & (IData)(__Vtask_sky130_sram_tb__DOT__request__40__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__40__value[0U]));
        }
        if ((4U & (IData)(__Vtask_sky130_sram_tb__DOT__request__40__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__40__value[0U]));
        }
        if ((8U & (IData)(__Vtask_sky130_sram_tb__DOT__request__40__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__40__value[0U]));
        }
        if ((0x10U & (IData)(__Vtask_sky130_sram_tb__DOT__request__40__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__40__value[1U]));
        }
        if ((0x20U & (IData)(__Vtask_sky130_sram_tb__DOT__request__40__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__40__value[1U]));
        }
        if ((0x40U & (IData)(__Vtask_sky130_sram_tb__DOT__request__40__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__40__value[1U]));
        }
        if ((0x80U & (IData)(__Vtask_sky130_sram_tb__DOT__request__40__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__40__value[1U]));
        }
        if ((0x100U & (IData)(__Vtask_sky130_sram_tb__DOT__request__40__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__40__value[2U]));
        }
        if ((0x200U & (IData)(__Vtask_sky130_sram_tb__DOT__request__40__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__40__value[2U]));
        }
        if ((0x400U & (IData)(__Vtask_sky130_sram_tb__DOT__request__40__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__40__value[2U]));
        }
        if ((0x800U & (IData)(__Vtask_sky130_sram_tb__DOT__request__40__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__40__value[2U]));
        }
        if ((0x1000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__40__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__40__value[3U]));
        }
        if ((0x2000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__40__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__40__value[3U]));
        }
        if ((0x4000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__40__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__40__value[3U]));
        }
        if ((0x8000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__40__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__40__value[3U]));
        }
    }
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    if (VL_UNLIKELY((((3U == (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state)) 
                      | (IData)(vlSelf->sky130_sram_tb__DOT__sram_enable)) 
                     | ((vlSelf->sky130_sram_tb__DOT__commands 
                         - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                        != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                             ? 1U : 0U))))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:52: Assertion failed in %Nsky130_sram_tb.request: held request repeated\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 52, "");
    }
    vlSelf->sky130_sram_tb__DOT__valid = 0U;
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    vlSelf->sky130_sram_tb__DOT__transactions = ((IData)(1U) 
                                                 + vlSelf->sky130_sram_tb__DOT__transactions);
    __Vtask_sky130_sram_tb__DOT__request__47__value[0U] = 0U;
    __Vtask_sky130_sram_tb__DOT__request__47__value[1U] = 0U;
    __Vtask_sky130_sram_tb__DOT__request__47__value[2U] = 0U;
    __Vtask_sky130_sram_tb__DOT__request__47__value[3U] = 0U;
    __Vtask_sky130_sram_tb__DOT__request__47__lanes = 0xffffU;
    __Vtask_sky130_sram_tb__DOT__request__47__addr = 0x2000U;
    __Vtask_sky130_sram_tb__DOT__request__47__wr = 0U;
    co_await vlSelf->__VtrigSched_h2f20d2d8__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(negedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       36);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       36);
    vlSelf->sky130_sram_tb__DOT__write = __Vtask_sky130_sram_tb__DOT__request__47__wr;
    vlSelf->sky130_sram_tb__DOT__address = __Vtask_sky130_sram_tb__DOT__request__47__addr;
    vlSelf->sky130_sram_tb__DOT__mask = __Vtask_sky130_sram_tb__DOT__request__47__lanes;
    vlSelf->sky130_sram_tb__DOT__wdata[0U] = __Vtask_sky130_sram_tb__DOT__request__47__value[0U];
    vlSelf->sky130_sram_tb__DOT__wdata[1U] = __Vtask_sky130_sram_tb__DOT__request__47__value[1U];
    vlSelf->sky130_sram_tb__DOT__wdata[2U] = __Vtask_sky130_sram_tb__DOT__request__47__value[2U];
    vlSelf->sky130_sram_tb__DOT__wdata[3U] = __Vtask_sky130_sram_tb__DOT__request__47__value[3U];
    vlSelf->sky130_sram_tb__DOT__valid = 1U;
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands 
        = vlSelf->sky130_sram_tb__DOT__commands;
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__age = 0U;
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
        = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
    if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
    }
    while ((3U != (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state))) {
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
            = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
        if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
        }
    }
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal 
        = (((0x2000U > __Vtask_sky130_sram_tb__DOT__request__47__addr) 
            & (0U == (0xfU & __Vtask_sky130_sram_tb__DOT__request__47__addr))) 
           & (0U != (IData)(__Vtask_sky130_sram_tb__DOT__request__47__lanes)));
    if (VL_UNLIKELY((vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
                     != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                          ? ((IData)(__Vtask_sky130_sram_tb__DOT__request__47__wr)
                              ? 2U : 3U) : 1U)))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:41: Assertion failed in %Nsky130_sram_tb.request: incorrect response timing\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 41, "");
    }
    if (VL_UNLIKELY(((IData)(vlSelf->sky130_sram_tb__DOT__fault) 
                     != (1U & (~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)))))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:42: Assertion failed in %Nsky130_sram_tb.request: unexpected fault addr=%x\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name(),
                  32,__Vtask_sky130_sram_tb__DOT__request__47__addr);
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 42, "");
    }
    if (VL_UNLIKELY(((vlSelf->sky130_sram_tb__DOT__commands 
                      - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                     != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                          ? 1U : 0U)))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:43: Assertion failed in %Nsky130_sram_tb.request: wrong number of macro commands\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 43, "");
    }
    if ((1U & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)) 
               | (IData)(__Vtask_sky130_sram_tb__DOT__request__47__wr)))) {
        if (VL_UNLIKELY((0U != (((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                  | vlSelf->sky130_sram_tb__DOT__rdata[1U]) 
                                 | vlSelf->sky130_sram_tb__DOT__rdata[2U]) 
                                | vlSelf->sky130_sram_tb__DOT__rdata[3U])))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:45: Assertion failed in %Nsky130_sram_tb.request: write/fault data not zero\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 45, "");
        }
    } else if (VL_UNLIKELY((0U != ((((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                      ^ vlSelf->sky130_sram_tb__DOT__oracle
                                      [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__47__addr 
                                                  >> 4U))][0U]) 
                                     | (vlSelf->sky130_sram_tb__DOT__rdata[1U] 
                                        ^ vlSelf->sky130_sram_tb__DOT__oracle
                                        [(0x1ffU & 
                                          (__Vtask_sky130_sram_tb__DOT__request__47__addr 
                                           >> 4U))][1U])) 
                                    | (vlSelf->sky130_sram_tb__DOT__rdata[2U] 
                                       ^ vlSelf->sky130_sram_tb__DOT__oracle
                                       [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__47__addr 
                                                   >> 4U))][2U])) 
                                   | (vlSelf->sky130_sram_tb__DOT__rdata[3U] 
                                      ^ vlSelf->sky130_sram_tb__DOT__oracle
                                      [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__47__addr 
                                                  >> 4U))][3U]))))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:46: Assertion failed in %Nsky130_sram_tb.request: read differs addr=%x got=%x want=%x\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name(),
                  32,__Vtask_sky130_sram_tb__DOT__request__47__addr,
                  128,vlSelf->sky130_sram_tb__DOT__rdata.data(),
                  128,vlSelf->sky130_sram_tb__DOT__oracle
                  [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__47__addr 
                              >> 4U))].data());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 46, "");
    }
    if (((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal) 
         & (IData)(__Vtask_sky130_sram_tb__DOT__request__47__wr))) {
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__index 
            = VL_SHIFTR_III(32,32,32, __Vtask_sky130_sram_tb__DOT__request__47__addr, 4U);
        if ((1U & (IData)(__Vtask_sky130_sram_tb__DOT__request__47__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__47__value[0U]));
        }
        if ((2U & (IData)(__Vtask_sky130_sram_tb__DOT__request__47__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__47__value[0U]));
        }
        if ((4U & (IData)(__Vtask_sky130_sram_tb__DOT__request__47__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__47__value[0U]));
        }
        if ((8U & (IData)(__Vtask_sky130_sram_tb__DOT__request__47__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__47__value[0U]));
        }
        if ((0x10U & (IData)(__Vtask_sky130_sram_tb__DOT__request__47__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__47__value[1U]));
        }
        if ((0x20U & (IData)(__Vtask_sky130_sram_tb__DOT__request__47__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__47__value[1U]));
        }
        if ((0x40U & (IData)(__Vtask_sky130_sram_tb__DOT__request__47__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__47__value[1U]));
        }
        if ((0x80U & (IData)(__Vtask_sky130_sram_tb__DOT__request__47__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__47__value[1U]));
        }
        if ((0x100U & (IData)(__Vtask_sky130_sram_tb__DOT__request__47__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__47__value[2U]));
        }
        if ((0x200U & (IData)(__Vtask_sky130_sram_tb__DOT__request__47__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__47__value[2U]));
        }
        if ((0x400U & (IData)(__Vtask_sky130_sram_tb__DOT__request__47__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__47__value[2U]));
        }
        if ((0x800U & (IData)(__Vtask_sky130_sram_tb__DOT__request__47__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__47__value[2U]));
        }
        if ((0x1000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__47__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__47__value[3U]));
        }
        if ((0x2000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__47__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__47__value[3U]));
        }
        if ((0x4000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__47__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__47__value[3U]));
        }
        if ((0x8000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__47__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__47__value[3U]));
        }
    }
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    if (VL_UNLIKELY((((3U == (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state)) 
                      | (IData)(vlSelf->sky130_sram_tb__DOT__sram_enable)) 
                     | ((vlSelf->sky130_sram_tb__DOT__commands 
                         - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                        != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                             ? 1U : 0U))))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:52: Assertion failed in %Nsky130_sram_tb.request: held request repeated\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 52, "");
    }
    vlSelf->sky130_sram_tb__DOT__valid = 0U;
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    vlSelf->sky130_sram_tb__DOT__transactions = ((IData)(1U) 
                                                 + vlSelf->sky130_sram_tb__DOT__transactions);
    __Vtask_sky130_sram_tb__DOT__request__54__value[0U] = 0xffffffffU;
    __Vtask_sky130_sram_tb__DOT__request__54__value[1U] = 0xffffffffU;
    __Vtask_sky130_sram_tb__DOT__request__54__value[2U] = 0xffffffffU;
    __Vtask_sky130_sram_tb__DOT__request__54__value[3U] = 0xffffffffU;
    __Vtask_sky130_sram_tb__DOT__request__54__lanes = 0xffffU;
    __Vtask_sky130_sram_tb__DOT__request__54__addr = 0xfffffff0U;
    __Vtask_sky130_sram_tb__DOT__request__54__wr = 1U;
    co_await vlSelf->__VtrigSched_h2f20d2d8__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(negedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       36);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       36);
    vlSelf->sky130_sram_tb__DOT__write = __Vtask_sky130_sram_tb__DOT__request__54__wr;
    vlSelf->sky130_sram_tb__DOT__address = __Vtask_sky130_sram_tb__DOT__request__54__addr;
    vlSelf->sky130_sram_tb__DOT__mask = __Vtask_sky130_sram_tb__DOT__request__54__lanes;
    vlSelf->sky130_sram_tb__DOT__wdata[0U] = __Vtask_sky130_sram_tb__DOT__request__54__value[0U];
    vlSelf->sky130_sram_tb__DOT__wdata[1U] = __Vtask_sky130_sram_tb__DOT__request__54__value[1U];
    vlSelf->sky130_sram_tb__DOT__wdata[2U] = __Vtask_sky130_sram_tb__DOT__request__54__value[2U];
    vlSelf->sky130_sram_tb__DOT__wdata[3U] = __Vtask_sky130_sram_tb__DOT__request__54__value[3U];
    vlSelf->sky130_sram_tb__DOT__valid = 1U;
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands 
        = vlSelf->sky130_sram_tb__DOT__commands;
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__age = 0U;
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
        = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
    if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
    }
    while ((3U != (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state))) {
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
            = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
        if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
        }
    }
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal 
        = (((0x2000U > __Vtask_sky130_sram_tb__DOT__request__54__addr) 
            & (0U == (0xfU & __Vtask_sky130_sram_tb__DOT__request__54__addr))) 
           & (0U != (IData)(__Vtask_sky130_sram_tb__DOT__request__54__lanes)));
    if (VL_UNLIKELY((vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
                     != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                          ? ((IData)(__Vtask_sky130_sram_tb__DOT__request__54__wr)
                              ? 2U : 3U) : 1U)))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:41: Assertion failed in %Nsky130_sram_tb.request: incorrect response timing\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 41, "");
    }
    if (VL_UNLIKELY(((IData)(vlSelf->sky130_sram_tb__DOT__fault) 
                     != (1U & (~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)))))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:42: Assertion failed in %Nsky130_sram_tb.request: unexpected fault addr=%x\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name(),
                  32,__Vtask_sky130_sram_tb__DOT__request__54__addr);
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 42, "");
    }
    if (VL_UNLIKELY(((vlSelf->sky130_sram_tb__DOT__commands 
                      - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                     != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                          ? 1U : 0U)))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:43: Assertion failed in %Nsky130_sram_tb.request: wrong number of macro commands\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 43, "");
    }
    if ((1U & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)) 
               | (IData)(__Vtask_sky130_sram_tb__DOT__request__54__wr)))) {
        if (VL_UNLIKELY((0U != (((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                  | vlSelf->sky130_sram_tb__DOT__rdata[1U]) 
                                 | vlSelf->sky130_sram_tb__DOT__rdata[2U]) 
                                | vlSelf->sky130_sram_tb__DOT__rdata[3U])))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:45: Assertion failed in %Nsky130_sram_tb.request: write/fault data not zero\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 45, "");
        }
    } else if (VL_UNLIKELY((0U != ((((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                      ^ vlSelf->sky130_sram_tb__DOT__oracle
                                      [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__54__addr 
                                                  >> 4U))][0U]) 
                                     | (vlSelf->sky130_sram_tb__DOT__rdata[1U] 
                                        ^ vlSelf->sky130_sram_tb__DOT__oracle
                                        [(0x1ffU & 
                                          (__Vtask_sky130_sram_tb__DOT__request__54__addr 
                                           >> 4U))][1U])) 
                                    | (vlSelf->sky130_sram_tb__DOT__rdata[2U] 
                                       ^ vlSelf->sky130_sram_tb__DOT__oracle
                                       [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__54__addr 
                                                   >> 4U))][2U])) 
                                   | (vlSelf->sky130_sram_tb__DOT__rdata[3U] 
                                      ^ vlSelf->sky130_sram_tb__DOT__oracle
                                      [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__54__addr 
                                                  >> 4U))][3U]))))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:46: Assertion failed in %Nsky130_sram_tb.request: read differs addr=%x got=%x want=%x\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name(),
                  32,__Vtask_sky130_sram_tb__DOT__request__54__addr,
                  128,vlSelf->sky130_sram_tb__DOT__rdata.data(),
                  128,vlSelf->sky130_sram_tb__DOT__oracle
                  [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__54__addr 
                              >> 4U))].data());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 46, "");
    }
    if (((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal) 
         & (IData)(__Vtask_sky130_sram_tb__DOT__request__54__wr))) {
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__index 
            = VL_SHIFTR_III(32,32,32, __Vtask_sky130_sram_tb__DOT__request__54__addr, 4U);
        if ((1U & (IData)(__Vtask_sky130_sram_tb__DOT__request__54__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__54__value[0U]));
        }
        if ((2U & (IData)(__Vtask_sky130_sram_tb__DOT__request__54__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__54__value[0U]));
        }
        if ((4U & (IData)(__Vtask_sky130_sram_tb__DOT__request__54__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__54__value[0U]));
        }
        if ((8U & (IData)(__Vtask_sky130_sram_tb__DOT__request__54__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__54__value[0U]));
        }
        if ((0x10U & (IData)(__Vtask_sky130_sram_tb__DOT__request__54__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__54__value[1U]));
        }
        if ((0x20U & (IData)(__Vtask_sky130_sram_tb__DOT__request__54__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__54__value[1U]));
        }
        if ((0x40U & (IData)(__Vtask_sky130_sram_tb__DOT__request__54__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__54__value[1U]));
        }
        if ((0x80U & (IData)(__Vtask_sky130_sram_tb__DOT__request__54__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__54__value[1U]));
        }
        if ((0x100U & (IData)(__Vtask_sky130_sram_tb__DOT__request__54__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__54__value[2U]));
        }
        if ((0x200U & (IData)(__Vtask_sky130_sram_tb__DOT__request__54__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__54__value[2U]));
        }
        if ((0x400U & (IData)(__Vtask_sky130_sram_tb__DOT__request__54__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__54__value[2U]));
        }
        if ((0x800U & (IData)(__Vtask_sky130_sram_tb__DOT__request__54__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__54__value[2U]));
        }
        if ((0x1000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__54__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__54__value[3U]));
        }
        if ((0x2000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__54__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__54__value[3U]));
        }
        if ((0x4000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__54__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__54__value[3U]));
        }
        if ((0x8000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__54__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__54__value[3U]));
        }
    }
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    if (VL_UNLIKELY((((3U == (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state)) 
                      | (IData)(vlSelf->sky130_sram_tb__DOT__sram_enable)) 
                     | ((vlSelf->sky130_sram_tb__DOT__commands 
                         - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                        != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                             ? 1U : 0U))))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:52: Assertion failed in %Nsky130_sram_tb.request: held request repeated\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 52, "");
    }
    vlSelf->sky130_sram_tb__DOT__valid = 0U;
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    vlSelf->sky130_sram_tb__DOT__transactions = ((IData)(1U) 
                                                 + vlSelf->sky130_sram_tb__DOT__transactions);
    co_await vlSelf->__VtrigSched_h2f20d2d8__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(negedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       57);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       57);
    vlSelf->sky130_sram_tb__DOT__reset = 1U;
    vlSelf->sky130_sram_tb__DOT__valid = 0U;
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    vlSelf->sky130_sram_tb__DOT__reset = 0U;
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    vlSelf->sky130_sram_tb__DOT__resets = ((IData)(1U) 
                                           + vlSelf->sky130_sram_tb__DOT__resets);
    sky130_sram_tb__DOT__unnamedblk6__DOT__i = 0U;
    while (VL_GTS_III(32, 0x200U, sky130_sram_tb__DOT__unnamedblk6__DOT__i)) {
        __Vtask_sky130_sram_tb__DOT__request__65__value[0U] = 0U;
        __Vtask_sky130_sram_tb__DOT__request__65__value[1U] = 0U;
        __Vtask_sky130_sram_tb__DOT__request__65__value[2U] = 0U;
        __Vtask_sky130_sram_tb__DOT__request__65__value[3U] = 0U;
        __Vtask_sky130_sram_tb__DOT__request__65__lanes = 0xffffU;
        __Vtask_sky130_sram_tb__DOT__request__65__addr 
            = VL_MULS_III(32, (IData)(0x10U), sky130_sram_tb__DOT__unnamedblk6__DOT__i);
        __Vtask_sky130_sram_tb__DOT__request__65__wr = 0U;
        co_await vlSelf->__VtrigSched_h2f20d2d8__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(negedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           36);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           36);
        vlSelf->sky130_sram_tb__DOT__write = __Vtask_sky130_sram_tb__DOT__request__65__wr;
        vlSelf->sky130_sram_tb__DOT__address = __Vtask_sky130_sram_tb__DOT__request__65__addr;
        vlSelf->sky130_sram_tb__DOT__mask = __Vtask_sky130_sram_tb__DOT__request__65__lanes;
        vlSelf->sky130_sram_tb__DOT__wdata[0U] = __Vtask_sky130_sram_tb__DOT__request__65__value[0U];
        vlSelf->sky130_sram_tb__DOT__wdata[1U] = __Vtask_sky130_sram_tb__DOT__request__65__value[1U];
        vlSelf->sky130_sram_tb__DOT__wdata[2U] = __Vtask_sky130_sram_tb__DOT__request__65__value[2U];
        vlSelf->sky130_sram_tb__DOT__wdata[3U] = __Vtask_sky130_sram_tb__DOT__request__65__value[3U];
        vlSelf->sky130_sram_tb__DOT__valid = 1U;
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands 
            = vlSelf->sky130_sram_tb__DOT__commands;
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__age = 0U;
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
            = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
        if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
        }
        while ((3U != (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state))) {
            co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                               nullptr, 
                                                               "@(posedge sky130_sram_tb.clk)", 
                                                               "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                               28);
            co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                               nullptr, 
                                               "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                               28);
            vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
                = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
            if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
                VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                          64,VL_TIME_UNITED_Q(1000),
                          -9,vlSymsp->name());
                VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
            }
        }
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal 
            = (((0x2000U > __Vtask_sky130_sram_tb__DOT__request__65__addr) 
                & (0U == (0xfU & __Vtask_sky130_sram_tb__DOT__request__65__addr))) 
               & (0U != (IData)(__Vtask_sky130_sram_tb__DOT__request__65__lanes)));
        if (VL_UNLIKELY((vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
                         != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                              ? ((IData)(__Vtask_sky130_sram_tb__DOT__request__65__wr)
                                  ? 2U : 3U) : 1U)))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:41: Assertion failed in %Nsky130_sram_tb.request: incorrect response timing\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 41, "");
        }
        if (VL_UNLIKELY(((IData)(vlSelf->sky130_sram_tb__DOT__fault) 
                         != (1U & (~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)))))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:42: Assertion failed in %Nsky130_sram_tb.request: unexpected fault addr=%x\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name(),32,__Vtask_sky130_sram_tb__DOT__request__65__addr);
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 42, "");
        }
        if (VL_UNLIKELY(((vlSelf->sky130_sram_tb__DOT__commands 
                          - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                         != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                              ? 1U : 0U)))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:43: Assertion failed in %Nsky130_sram_tb.request: wrong number of macro commands\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 43, "");
        }
        if ((1U & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)) 
                   | (IData)(__Vtask_sky130_sram_tb__DOT__request__65__wr)))) {
            if (VL_UNLIKELY((0U != (((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                      | vlSelf->sky130_sram_tb__DOT__rdata[1U]) 
                                     | vlSelf->sky130_sram_tb__DOT__rdata[2U]) 
                                    | vlSelf->sky130_sram_tb__DOT__rdata[3U])))) {
                VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:45: Assertion failed in %Nsky130_sram_tb.request: write/fault data not zero\n",
                          64,VL_TIME_UNITED_Q(1000),
                          -9,vlSymsp->name());
                VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 45, "");
            }
        } else if (VL_UNLIKELY((0U != ((((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                          ^ vlSelf->sky130_sram_tb__DOT__oracle
                                          [(0x1ffU 
                                            & (__Vtask_sky130_sram_tb__DOT__request__65__addr 
                                               >> 4U))][0U]) 
                                         | (vlSelf->sky130_sram_tb__DOT__rdata[1U] 
                                            ^ vlSelf->sky130_sram_tb__DOT__oracle
                                            [(0x1ffU 
                                              & (__Vtask_sky130_sram_tb__DOT__request__65__addr 
                                                 >> 4U))][1U])) 
                                        | (vlSelf->sky130_sram_tb__DOT__rdata[2U] 
                                           ^ vlSelf->sky130_sram_tb__DOT__oracle
                                           [(0x1ffU 
                                             & (__Vtask_sky130_sram_tb__DOT__request__65__addr 
                                                >> 4U))][2U])) 
                                       | (vlSelf->sky130_sram_tb__DOT__rdata[3U] 
                                          ^ vlSelf->sky130_sram_tb__DOT__oracle
                                          [(0x1ffU 
                                            & (__Vtask_sky130_sram_tb__DOT__request__65__addr 
                                               >> 4U))][3U]))))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:46: Assertion failed in %Nsky130_sram_tb.request: read differs addr=%x got=%x want=%x\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name(),32,__Vtask_sky130_sram_tb__DOT__request__65__addr,
                      128,vlSelf->sky130_sram_tb__DOT__rdata.data(),
                      128,vlSelf->sky130_sram_tb__DOT__oracle
                      [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__65__addr 
                                  >> 4U))].data());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 46, "");
        }
        if (((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal) 
             & (IData)(__Vtask_sky130_sram_tb__DOT__request__65__wr))) {
            vlSelf->sky130_sram_tb__DOT__request__Vstatic__index 
                = VL_SHIFTR_III(32,32,32, __Vtask_sky130_sram_tb__DOT__request__65__addr, 4U);
            if ((1U & (IData)(__Vtask_sky130_sram_tb__DOT__request__65__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__65__value[0U]));
            }
            if ((2U & (IData)(__Vtask_sky130_sram_tb__DOT__request__65__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__65__value[0U]));
            }
            if ((4U & (IData)(__Vtask_sky130_sram_tb__DOT__request__65__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__65__value[0U]));
            }
            if ((8U & (IData)(__Vtask_sky130_sram_tb__DOT__request__65__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__65__value[0U]));
            }
            if ((0x10U & (IData)(__Vtask_sky130_sram_tb__DOT__request__65__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__65__value[1U]));
            }
            if ((0x20U & (IData)(__Vtask_sky130_sram_tb__DOT__request__65__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__65__value[1U]));
            }
            if ((0x40U & (IData)(__Vtask_sky130_sram_tb__DOT__request__65__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__65__value[1U]));
            }
            if ((0x80U & (IData)(__Vtask_sky130_sram_tb__DOT__request__65__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__65__value[1U]));
            }
            if ((0x100U & (IData)(__Vtask_sky130_sram_tb__DOT__request__65__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__65__value[2U]));
            }
            if ((0x200U & (IData)(__Vtask_sky130_sram_tb__DOT__request__65__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__65__value[2U]));
            }
            if ((0x400U & (IData)(__Vtask_sky130_sram_tb__DOT__request__65__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__65__value[2U]));
            }
            if ((0x800U & (IData)(__Vtask_sky130_sram_tb__DOT__request__65__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__65__value[2U]));
            }
            if ((0x1000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__65__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xffU & __Vtask_sky130_sram_tb__DOT__request__65__value[3U]));
            }
            if ((0x2000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__65__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__65__value[3U]));
            }
            if ((0x4000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__65__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__65__value[3U]));
            }
            if ((0x8000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__65__lanes))) {
                vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                     & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                    = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                        [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                       | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__65__value[3U]));
            }
        }
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        if (VL_UNLIKELY((((3U == (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state)) 
                          | (IData)(vlSelf->sky130_sram_tb__DOT__sram_enable)) 
                         | ((vlSelf->sky130_sram_tb__DOT__commands 
                             - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                            != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                                 ? 1U : 0U))))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:52: Assertion failed in %Nsky130_sram_tb.request: held request repeated\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 52, "");
        }
        vlSelf->sky130_sram_tb__DOT__valid = 0U;
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        vlSelf->sky130_sram_tb__DOT__transactions = 
            ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__transactions);
        sky130_sram_tb__DOT__unnamedblk6__DOT__i = 
            ((IData)(1U) + sky130_sram_tb__DOT__unnamedblk6__DOT__i);
    }
    co_await vlSelf->__VtrigSched_h2f20d2d8__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(negedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       77);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       77);
    vlSelf->sky130_sram_tb__DOT__valid = 1U;
    vlSelf->sky130_sram_tb__DOT__write = 0U;
    vlSelf->sky130_sram_tb__DOT__address = 0U;
    vlSelf->sky130_sram_tb__DOT__mask = 0xffffU;
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    co_await vlSelf->__VtrigSched_h2f20d2d8__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(negedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       57);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       57);
    vlSelf->sky130_sram_tb__DOT__reset = 1U;
    vlSelf->sky130_sram_tb__DOT__valid = 0U;
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    vlSelf->sky130_sram_tb__DOT__reset = 0U;
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    vlSelf->sky130_sram_tb__DOT__resets = ((IData)(1U) 
                                           + vlSelf->sky130_sram_tb__DOT__resets);
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    if (VL_UNLIKELY((3U == (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state)))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:79: Assertion failed in %Nsky130_sram_tb.unnamedblk7: stale post-reset read response\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 79, "");
    }
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    if (VL_UNLIKELY((3U == (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state)))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:79: Assertion failed in %Nsky130_sram_tb.unnamedblk7: stale post-reset read response\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 79, "");
    }
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    if (VL_UNLIKELY((3U == (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state)))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:79: Assertion failed in %Nsky130_sram_tb.unnamedblk7: stale post-reset read response\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 79, "");
    }
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    if (VL_UNLIKELY((3U == (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state)))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:79: Assertion failed in %Nsky130_sram_tb.unnamedblk7: stale post-reset read response\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 79, "");
    }
    __Vtask_sky130_sram_tb__DOT__request__79__value[0U] = 0U;
    __Vtask_sky130_sram_tb__DOT__request__79__value[1U] = 0U;
    __Vtask_sky130_sram_tb__DOT__request__79__value[2U] = 0U;
    __Vtask_sky130_sram_tb__DOT__request__79__value[3U] = 0U;
    __Vtask_sky130_sram_tb__DOT__request__79__lanes = 0xffffU;
    __Vtask_sky130_sram_tb__DOT__request__79__addr = 0U;
    __Vtask_sky130_sram_tb__DOT__request__79__wr = 0U;
    co_await vlSelf->__VtrigSched_h2f20d2d8__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(negedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       36);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       36);
    vlSelf->sky130_sram_tb__DOT__write = __Vtask_sky130_sram_tb__DOT__request__79__wr;
    vlSelf->sky130_sram_tb__DOT__address = __Vtask_sky130_sram_tb__DOT__request__79__addr;
    vlSelf->sky130_sram_tb__DOT__mask = __Vtask_sky130_sram_tb__DOT__request__79__lanes;
    vlSelf->sky130_sram_tb__DOT__wdata[0U] = __Vtask_sky130_sram_tb__DOT__request__79__value[0U];
    vlSelf->sky130_sram_tb__DOT__wdata[1U] = __Vtask_sky130_sram_tb__DOT__request__79__value[1U];
    vlSelf->sky130_sram_tb__DOT__wdata[2U] = __Vtask_sky130_sram_tb__DOT__request__79__value[2U];
    vlSelf->sky130_sram_tb__DOT__wdata[3U] = __Vtask_sky130_sram_tb__DOT__request__79__value[3U];
    vlSelf->sky130_sram_tb__DOT__valid = 1U;
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands 
        = vlSelf->sky130_sram_tb__DOT__commands;
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__age = 0U;
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
        = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
    if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
    }
    while ((3U != (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state))) {
        co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                           nullptr, 
                                                           "@(posedge sky130_sram_tb.clk)", 
                                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                           28);
        co_await vlSelf->__VdlySched.delay(0x7d0ULL, 
                                           nullptr, 
                                           "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                           28);
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
            = ((IData)(1U) + vlSelf->sky130_sram_tb__DOT__request__Vstatic__age);
        if (VL_UNLIKELY(VL_LTS_III(32, 9U, vlSelf->sky130_sram_tb__DOT__request__Vstatic__age))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:39: Assertion failed in %Nsky130_sram_tb.request: no bounded response\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 39, "");
        }
    }
    vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal 
        = (((0x2000U > __Vtask_sky130_sram_tb__DOT__request__79__addr) 
            & (0U == (0xfU & __Vtask_sky130_sram_tb__DOT__request__79__addr))) 
           & (0U != (IData)(__Vtask_sky130_sram_tb__DOT__request__79__lanes)));
    if (VL_UNLIKELY((vlSelf->sky130_sram_tb__DOT__request__Vstatic__age 
                     != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                          ? ((IData)(__Vtask_sky130_sram_tb__DOT__request__79__wr)
                              ? 2U : 3U) : 1U)))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:41: Assertion failed in %Nsky130_sram_tb.request: incorrect response timing\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 41, "");
    }
    if (VL_UNLIKELY(((IData)(vlSelf->sky130_sram_tb__DOT__fault) 
                     != (1U & (~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)))))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:42: Assertion failed in %Nsky130_sram_tb.request: unexpected fault addr=%x\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name(),
                  32,__Vtask_sky130_sram_tb__DOT__request__79__addr);
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 42, "");
    }
    if (VL_UNLIKELY(((vlSelf->sky130_sram_tb__DOT__commands 
                      - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                     != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                          ? 1U : 0U)))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:43: Assertion failed in %Nsky130_sram_tb.request: wrong number of macro commands\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 43, "");
    }
    if ((1U & ((~ (IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)) 
               | (IData)(__Vtask_sky130_sram_tb__DOT__request__79__wr)))) {
        if (VL_UNLIKELY((0U != (((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                  | vlSelf->sky130_sram_tb__DOT__rdata[1U]) 
                                 | vlSelf->sky130_sram_tb__DOT__rdata[2U]) 
                                | vlSelf->sky130_sram_tb__DOT__rdata[3U])))) {
            VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:45: Assertion failed in %Nsky130_sram_tb.request: write/fault data not zero\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      vlSymsp->name());
            VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 45, "");
        }
    } else if (VL_UNLIKELY((0U != ((((vlSelf->sky130_sram_tb__DOT__rdata[0U] 
                                      ^ vlSelf->sky130_sram_tb__DOT__oracle
                                      [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__79__addr 
                                                  >> 4U))][0U]) 
                                     | (vlSelf->sky130_sram_tb__DOT__rdata[1U] 
                                        ^ vlSelf->sky130_sram_tb__DOT__oracle
                                        [(0x1ffU & 
                                          (__Vtask_sky130_sram_tb__DOT__request__79__addr 
                                           >> 4U))][1U])) 
                                    | (vlSelf->sky130_sram_tb__DOT__rdata[2U] 
                                       ^ vlSelf->sky130_sram_tb__DOT__oracle
                                       [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__79__addr 
                                                   >> 4U))][2U])) 
                                   | (vlSelf->sky130_sram_tb__DOT__rdata[3U] 
                                      ^ vlSelf->sky130_sram_tb__DOT__oracle
                                      [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__79__addr 
                                                  >> 4U))][3U]))))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:46: Assertion failed in %Nsky130_sram_tb.request: read differs addr=%x got=%x want=%x\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name(),
                  32,__Vtask_sky130_sram_tb__DOT__request__79__addr,
                  128,vlSelf->sky130_sram_tb__DOT__rdata.data(),
                  128,vlSelf->sky130_sram_tb__DOT__oracle
                  [(0x1ffU & (__Vtask_sky130_sram_tb__DOT__request__79__addr 
                              >> 4U))].data());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 46, "");
    }
    if (((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal) 
         & (IData)(__Vtask_sky130_sram_tb__DOT__request__79__wr))) {
        vlSelf->sky130_sram_tb__DOT__request__Vstatic__index 
            = VL_SHIFTR_III(32,32,32, __Vtask_sky130_sram_tb__DOT__request__79__addr, 4U);
        if ((1U & (IData)(__Vtask_sky130_sram_tb__DOT__request__79__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__79__value[0U]));
        }
        if ((2U & (IData)(__Vtask_sky130_sram_tb__DOT__request__79__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__79__value[0U]));
        }
        if ((4U & (IData)(__Vtask_sky130_sram_tb__DOT__request__79__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__79__value[0U]));
        }
        if ((8U & (IData)(__Vtask_sky130_sram_tb__DOT__request__79__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][0U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__79__value[0U]));
        }
        if ((0x10U & (IData)(__Vtask_sky130_sram_tb__DOT__request__79__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__79__value[1U]));
        }
        if ((0x20U & (IData)(__Vtask_sky130_sram_tb__DOT__request__79__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__79__value[1U]));
        }
        if ((0x40U & (IData)(__Vtask_sky130_sram_tb__DOT__request__79__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__79__value[1U]));
        }
        if ((0x80U & (IData)(__Vtask_sky130_sram_tb__DOT__request__79__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][1U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__79__value[1U]));
        }
        if ((0x100U & (IData)(__Vtask_sky130_sram_tb__DOT__request__79__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__79__value[2U]));
        }
        if ((0x200U & (IData)(__Vtask_sky130_sram_tb__DOT__request__79__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__79__value[2U]));
        }
        if ((0x400U & (IData)(__Vtask_sky130_sram_tb__DOT__request__79__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__79__value[2U]));
        }
        if ((0x800U & (IData)(__Vtask_sky130_sram_tb__DOT__request__79__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][2U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__79__value[2U]));
        }
        if ((0x1000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__79__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xffffff00U & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xffU & __Vtask_sky130_sram_tb__DOT__request__79__value[3U]));
        }
        if ((0x2000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__79__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xffff00ffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xff00U & __Vtask_sky130_sram_tb__DOT__request__79__value[3U]));
        }
        if ((0x4000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__79__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xff00ffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xff0000U & __Vtask_sky130_sram_tb__DOT__request__79__value[3U]));
        }
        if ((0x8000U & (IData)(__Vtask_sky130_sram_tb__DOT__request__79__lanes))) {
            vlSelf->sky130_sram_tb__DOT__oracle[(0x1ffU 
                                                 & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U] 
                = ((0xffffffU & vlSelf->sky130_sram_tb__DOT__oracle
                    [(0x1ffU & vlSelf->sky130_sram_tb__DOT__request__Vstatic__index)][3U]) 
                   | (0xff000000U & __Vtask_sky130_sram_tb__DOT__request__79__value[3U]));
        }
    }
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    if (VL_UNLIKELY((((3U == (IData)(vlSelf->sky130_sram_tb__DOT__adapter__DOT__state)) 
                      | (IData)(vlSelf->sky130_sram_tb__DOT__sram_enable)) 
                     | ((vlSelf->sky130_sram_tb__DOT__commands 
                         - vlSelf->sky130_sram_tb__DOT__request__Vstatic__before_commands) 
                        != ((IData)(vlSelf->sky130_sram_tb__DOT__request__Vstatic__legal)
                             ? 1U : 0U))))) {
        VL_WRITEF("[%0t] %%Fatal: sky130_sram.sv:52: Assertion failed in %Nsky130_sram_tb.request: held request repeated\n",
                  64,VL_TIME_UNITED_Q(1000),-9,vlSymsp->name());
        VL_STOP_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 52, "");
    }
    vlSelf->sky130_sram_tb__DOT__valid = 0U;
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    co_await vlSelf->__VtrigSched_h2f20d209__0.trigger(0U, 
                                                       nullptr, 
                                                       "@(posedge sky130_sram_tb.clk)", 
                                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                                       28);
    co_await vlSelf->__VdlySched.delay(0x7d0ULL, nullptr, 
                                       "/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 
                                       28);
    vlSelf->sky130_sram_tb__DOT__transactions = ((IData)(1U) 
                                                 + vlSelf->sky130_sram_tb__DOT__transactions);
    VL_WRITEF("PASS vendor SRAM adapter bytes=8192 latency=1 masks=65535 transactions=%0d commands=%0d resets=%0d\n",
              32,vlSelf->sky130_sram_tb__DOT__transactions,
              32,vlSelf->sky130_sram_tb__DOT__commands,
              32,vlSelf->sky130_sram_tb__DOT__resets);
    VL_FINISH_MT("/tmp/wasmetal-xc7-core/tests/memory/sky130_sram.sv", 82, "");
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vsky130_sram_tb___024root___dump_triggers__act(Vsky130_sram_tb___024root* vlSelf);
#endif  // VL_DEBUG

void Vsky130_sram_tb___024root___eval_triggers__act(Vsky130_sram_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vsky130_sram_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsky130_sram_tb___024root___eval_triggers__act\n"); );
    // Body
    vlSelf->__VactTriggered.set(0U, ((IData)(vlSelf->sky130_sram_tb__DOT__clk) 
                                     & (~ (IData)(vlSelf->__Vtrigprevexpr___TOP__sky130_sram_tb__DOT__clk__0))));
    vlSelf->__VactTriggered.set(1U, ((~ (IData)(vlSelf->sky130_sram_tb__DOT__clk)) 
                                     & (IData)(vlSelf->__Vtrigprevexpr___TOP__sky130_sram_tb__DOT__clk__0)));
    vlSelf->__VactTriggered.set(2U, (((~ (IData)(vlSelf->sky130_sram_tb__DOT__clk)) 
                                      & (IData)(vlSelf->__Vtrigprevexpr___TOP__sky130_sram_tb__DOT__clk__0)) 
                                     | vlSelf->__VdlySched.awaitingCurrentTime()));
    vlSelf->__VactTriggered.set(3U, vlSelf->__VdlySched.awaitingCurrentTime());
    vlSelf->__Vtrigprevexpr___TOP__sky130_sram_tb__DOT__clk__0 
        = vlSelf->sky130_sram_tb__DOT__clk;
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vsky130_sram_tb___024root___dump_triggers__act(vlSelf);
    }
#endif
}
