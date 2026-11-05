// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vwasmetal_core.h for the primary calling header

#ifndef VERILATED_VWASMETAL_CORE_RAMB18E1__PI6_H_
#define VERILATED_VWASMETAL_CORE_RAMB18E1__PI6_H_  // guard

#include "verilated.h"


class Vwasmetal_core__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vwasmetal_core_RAMB18E1__pi6 final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    VL_IN8(CLKARDCLK,0,0);
    VL_IN8(CLKBWRCLK,0,0);
    VL_OUT8(__PVT__DOPADOP,1,0);
    VL_OUT8(DOPBDOP,1,0);
    VL_IN8(ENARDEN,0,0);
    VL_IN8(ENBWREN,0,0);
    VL_IN8(REGCEAREGCE,0,0);
    VL_IN8(REGCEB,0,0);
    VL_IN8(RSTRAMARSTRAM,0,0);
    VL_IN8(RSTRAMB,0,0);
    VL_IN8(RSTREGARSTREG,0,0);
    VL_IN8(RSTREGB,0,0);
    VL_IN8(DIPADIP,1,0);
    VL_IN8(DIPBDIP,1,0);
    VL_IN8(WEA,1,0);
    VL_IN8(WEBWE,3,0);
    CData/*7:0*/ __PVT__parity;
    VL_OUT16(__PVT__DOADO,15,0);
    VL_OUT16(DOBDO,15,0);
    VL_IN16(ADDRARDADDR,13,0);
    VL_IN16(ADDRBWRADDR,13,0);
    VL_IN16(DIADI,15,0);
    VL_IN16(DIBDI,15,0);
    SData/*8:0*/ __PVT__memory__DOT__q;
    SData/*8:0*/ memory__DOT____Vlvbound_h79136b5e__0;
    SData/*8:0*/ memory__DOT____Vlvbound_h26c55382__0;
    QData/*63:0*/ __PVT__data;
    VlUnpacked<SData/*8:0*/, 2048> __PVT__memory__DOT__words;

    // INTERNAL VARIABLES
    Vwasmetal_core__Syms* const vlSymsp;

    // CONSTRUCTORS
    Vwasmetal_core_RAMB18E1__pi6(Vwasmetal_core__Syms* symsp, const char* v__name);
    ~Vwasmetal_core_RAMB18E1__pi6();
    VL_UNCOPYABLE(Vwasmetal_core_RAMB18E1__pi6);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
