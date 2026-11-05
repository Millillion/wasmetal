// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vsky130_sram_tb.h for the primary calling header

#ifndef VERILATED_VSKY130_SRAM_TB___024ROOT_H_
#define VERILATED_VSKY130_SRAM_TB___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_timing.h"


class Vsky130_sram_tb__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vsky130_sram_tb___024root final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    // Anonymous structures to workaround compiler member-count bugs
    struct {
        CData/*0:0*/ sky130_sram_tb__DOT__clk;
        CData/*0:0*/ sky130_sram_tb__DOT__reset;
        CData/*0:0*/ sky130_sram_tb__DOT__valid;
        CData/*0:0*/ sky130_sram_tb__DOT__write;
        CData/*0:0*/ sky130_sram_tb__DOT__fault;
        CData/*0:0*/ sky130_sram_tb__DOT__sram_enable;
        CData/*0:0*/ sky130_sram_tb__DOT__sram_write;
        CData/*0:0*/ sky130_sram_tb__DOT__request__Vstatic__legal;
        CData/*2:0*/ sky130_sram_tb__DOT__adapter__DOT__state;
        CData/*0:0*/ sky130_sram_tb__DOT__adapter__DOT__write_q;
        CData/*0:0*/ sky130_sram_tb__DOT__adapter__DOT__remaining;
        CData/*0:0*/ sky130_sram_tb__DOT__adapter__DOT__legal;
        CData/*0:0*/ sky130_sram_tb__DOT__storage__DOT__pending;
        CData/*0:0*/ sky130_sram_tb__DOT__storage__DOT__selected;
        CData/*0:0*/ sky130_sram_tb__DOT__storage__DOT____VdfgTmp_hcbda1b31__0;
        CData/*0:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__csb0_reg;
        CData/*0:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__web0_reg;
        CData/*3:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__wmask0_reg;
        CData/*0:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__csb0_reg;
        CData/*0:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__web0_reg;
        CData/*3:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__wmask0_reg;
        CData/*0:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__csb0_reg;
        CData/*0:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__web0_reg;
        CData/*3:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__wmask0_reg;
        CData/*0:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__csb0_reg;
        CData/*0:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__web0_reg;
        CData/*3:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__wmask0_reg;
        CData/*0:0*/ __Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__dout0__v0;
        CData/*0:0*/ __Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__dout0__v0;
        CData/*0:0*/ __Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__dout0__v0;
        CData/*0:0*/ __Vdlyvset__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__dout0__v0;
        CData/*0:0*/ __VstlFirstIteration;
        CData/*0:0*/ __Vtrigprevexpr___TOP__sky130_sram_tb__DOT__clk__0;
        CData/*0:0*/ __VactContinue;
        SData/*15:0*/ sky130_sram_tb__DOT__mask;
        SData/*8:0*/ sky130_sram_tb__DOT__adapter__DOT__address_q;
        SData/*15:0*/ sky130_sram_tb__DOT__adapter__DOT__mask_q;
        SData/*8:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__addr0_reg;
        SData/*8:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__addr0_reg;
        SData/*8:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__addr0_reg;
        SData/*8:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__addr0_reg;
        IData/*31:0*/ sky130_sram_tb__DOT__address;
        VlWide<4>/*127:0*/ sky130_sram_tb__DOT__wdata;
        VlWide<4>/*127:0*/ sky130_sram_tb__DOT__rdata;
        IData/*31:0*/ sky130_sram_tb__DOT__transactions;
        IData/*31:0*/ sky130_sram_tb__DOT__commands;
        IData/*31:0*/ sky130_sram_tb__DOT__resets;
        IData/*31:0*/ sky130_sram_tb__DOT__request__Vstatic__age;
        IData/*31:0*/ sky130_sram_tb__DOT__request__Vstatic__before_commands;
        IData/*31:0*/ sky130_sram_tb__DOT__request__Vstatic__index;
        VlWide<4>/*127:0*/ sky130_sram_tb__DOT__adapter__DOT__data_q;
        VlWide<4>/*127:0*/ sky130_sram_tb__DOT__storage__DOT__held;
        VlWide<4>/*127:0*/ sky130_sram_tb__DOT__storage__DOT__sampled;
        IData/*31:0*/ sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__dout0;
        IData/*31:0*/ sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__dout0;
        IData/*31:0*/ sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__dout0;
        IData/*31:0*/ sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__dout0;
        IData/*31:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__din0_reg;
        IData/*31:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__din0_reg;
        IData/*31:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__din0_reg;
        IData/*31:0*/ sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__din0_reg;
        IData/*31:0*/ __Vintraval_h7f9437f7__0;
        IData/*31:0*/ __Vintraval_h36210009__0;
        IData/*31:0*/ __Vintraval_hac5192ed__0;
    };
    struct {
        IData/*31:0*/ __Vintraval_h1c213051__0;
        IData/*31:0*/ __Vdlyvval__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__dout0__v0;
        IData/*31:0*/ __Vdlyvval__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__dout0__v0;
        IData/*31:0*/ __Vdlyvval__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__dout0__v0;
        IData/*31:0*/ __Vdlyvval__sky130_sram_tb__DOT__storage__DOT____Vcellout__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__dout0__v0;
        IData/*31:0*/ __VactIterCount;
        VlUnpacked<VlWide<4>/*127:0*/, 512> sky130_sram_tb__DOT__oracle;
        VlUnpacked<VlWide<4>/*127:0*/, 1> sky130_sram_tb__DOT__storage__DOT__bank_data;
        VlUnpacked<IData/*31:0*/, 512> sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__0__KET____DOT__memory__DOT__mem;
        VlUnpacked<IData/*31:0*/, 512> sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__1__KET____DOT__memory__DOT__mem;
        VlUnpacked<IData/*31:0*/, 512> sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__2__KET____DOT__memory__DOT__mem;
        VlUnpacked<IData/*31:0*/, 512> sky130_sram_tb__DOT__storage__DOT__banks__BRA__0__KET____DOT__lanes__BRA__3__KET____DOT__memory__DOT__mem;
    };
    VlDelayScheduler __VdlySched;
    VlTriggerScheduler __VtrigSched_h2f20d209__0;
    VlTriggerScheduler __VtrigSched_h2f20d2d8__0;
    VlTriggerVec<1> __VstlTriggered;
    VlTriggerVec<4> __VactTriggered;
    VlTriggerVec<4> __VnbaTriggered;

    // INTERNAL VARIABLES
    Vsky130_sram_tb__Syms* const vlSymsp;

    // CONSTRUCTORS
    Vsky130_sram_tb___024root(Vsky130_sram_tb__Syms* symsp, const char* v__name);
    ~Vsky130_sram_tb___024root();
    VL_UNCOPYABLE(Vsky130_sram_tb___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
