// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vwasmetal_core.h for the primary calling header

#ifndef VERILATED_VWASMETAL_CORE_RAMB36E1__PI4_H_
#define VERILATED_VWASMETAL_CORE_RAMB36E1__PI4_H_  // guard

#include "verilated.h"


class Vwasmetal_core__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vwasmetal_core_RAMB36E1__pi4 final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    VL_IN8(CLKARDCLK,0,0);
    VL_IN8(CLKBWRCLK,0,0);
    VL_OUT8(DOPADOP,3,0);
    VL_OUT8(DOPBDOP,3,0);
    VL_IN8(ENARDEN,0,0);
    VL_IN8(ENBWREN,0,0);
    VL_IN8(REGCEAREGCE,0,0);
    VL_IN8(REGCEB,0,0);
    VL_IN8(RSTRAMARSTRAM,0,0);
    VL_IN8(RSTRAMB,0,0);
    VL_IN8(RSTREGARSTREG,0,0);
    VL_IN8(RSTREGB,0,0);
    VL_IN8(DIPADIP,3,0);
    VL_IN8(DIPBDIP,3,0);
    VL_IN8(WEA,3,0);
    VL_IN8(WEBWE,7,0);
    VL_IN8(__PVT__CASCADEINA,0,0);
    VL_IN8(__PVT__CASCADEINB,0,0);
    VL_IN8(__PVT__INJECTDBITERR,0,0);
    VL_IN8(__PVT__INJECTSBITERR,0,0);
    VL_OUT8(__PVT__CASCADEOUTA,0,0);
    VL_OUT8(__PVT__CASCADEOUTB,0,0);
    VL_OUT8(__PVT__DBITERR,0,0);
    VL_OUT8(__PVT__SBITERR,0,0);
    VL_OUT8(__PVT__ECCPARITY,7,0);
    CData/*7:0*/ __PVT__parity;
    CData/*7:0*/ __Vcellinp__memory__wparity;
    VL_IN16(ADDRARDADDR,15,0);
    VL_IN16(ADDRBWRADDR,15,0);
    VL_OUT16(__PVT__RDADDRECC,8,0);
    SData/*8:0*/ memory__DOT____Vlvbound_hb773fe31__0;
    SData/*8:0*/ memory__DOT____Vlvbound_h903ea74b__0;
    VL_OUT(DOADO,31,0);
    VL_OUT(DOBDO,31,0);
    VL_IN(DIADI,31,0);
    VL_IN(DIBDI,31,0);
    VlWide<3>/*71:0*/ __PVT__memory__DOT__q;
    QData/*63:0*/ __PVT__data;
    QData/*63:0*/ __Vcellinp__memory__wdata;
    VlUnpacked<VlWide<3>/*71:0*/, 512> __PVT__memory__DOT__words;

    // INTERNAL VARIABLES
    Vwasmetal_core__Syms* const vlSymsp;

    // CONSTRUCTORS
    Vwasmetal_core_RAMB36E1__pi4(Vwasmetal_core__Syms* symsp, const char* v__name);
    ~Vwasmetal_core_RAMB36E1__pi4();
    VL_UNCOPYABLE(Vwasmetal_core_RAMB36E1__pi4);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
