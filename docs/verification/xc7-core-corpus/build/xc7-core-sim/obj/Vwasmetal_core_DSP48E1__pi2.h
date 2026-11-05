// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vwasmetal_core.h for the primary calling header

#ifndef VERILATED_VWASMETAL_CORE_DSP48E1__PI2_H_
#define VERILATED_VWASMETAL_CORE_DSP48E1__PI2_H_  // guard

#include "verilated.h"


class Vwasmetal_core__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vwasmetal_core_DSP48E1__pi2 final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    VL_OUT8(__PVT__CARRYCASCOUT,0,0);
    VL_OUT8(__PVT__CARRYOUT,3,0);
    VL_OUT8(__PVT__MULTSIGNOUT,0,0);
    VL_OUT8(__PVT__OVERFLOW,0,0);
    VL_OUT8(__PVT__PATTERNBDETECT,0,0);
    VL_OUT8(__PVT__PATTERNDETECT,0,0);
    VL_OUT8(__PVT__UNDERFLOW,0,0);
    VL_IN8(ALUMODE,3,0);
    VL_IN8(__PVT__CARRYCASCIN,0,0);
    VL_IN8(CARRYIN,0,0);
    VL_IN8(CARRYINSEL,2,0);
    VL_IN8(__PVT__CEA1,0,0);
    VL_IN8(__PVT__CEA2,0,0);
    VL_IN8(__PVT__CEAD,0,0);
    VL_IN8(__PVT__CEALUMODE,0,0);
    VL_IN8(__PVT__CEB1,0,0);
    VL_IN8(__PVT__CEB2,0,0);
    VL_IN8(__PVT__CEC,0,0);
    VL_IN8(__PVT__CECARRYIN,0,0);
    VL_IN8(__PVT__CECTRL,0,0);
    VL_IN8(__PVT__CED,0,0);
    VL_IN8(__PVT__CEINMODE,0,0);
    VL_IN8(__PVT__CEM,0,0);
    VL_IN8(__PVT__CEP,0,0);
    VL_IN8(__PVT__CLK,0,0);
    VL_IN8(INMODE,4,0);
    VL_IN8(__PVT__MULTSIGNIN,0,0);
    VL_IN8(OPMODE,6,0);
    VL_IN8(__PVT__RSTA,0,0);
    VL_IN8(__PVT__RSTALLCARRYIN,0,0);
    VL_IN8(__PVT__RSTALUMODE,0,0);
    VL_IN8(__PVT__RSTB,0,0);
    VL_IN8(__PVT__RSTC,0,0);
    VL_IN8(__PVT__RSTCTRL,0,0);
    VL_IN8(__PVT__RSTD,0,0);
    VL_IN8(__PVT__RSTINMODE,0,0);
    VL_IN8(__PVT__RSTM,0,0);
    VL_IN8(__PVT__RSTP,0,0);
    SData/*12:0*/ __VdfgTmp_h4c2f98f1__0;
    SData/*12:0*/ __VdfgTmp_ha5045b21__0;
    VL_OUT(ACOUT,29,0);
    VL_OUT(__PVT__BCOUT,17,0);
    VL_IN(A,29,0);
    VL_IN(ACIN,29,0);
    VL_IN(B,17,0);
    VL_IN(BCIN,17,0);
    VL_IN(D,24,0);
    VL_OUT64(P,47,0);
    VL_OUT64(PCOUT,47,0);
    VL_IN64(C,47,0);
    VL_IN64(PCIN,47,0);
    QData/*42:0*/ __PVT__Mr;
    QData/*47:0*/ __PVT__maj_xyz;
    QData/*47:0*/ __PVT__xor_xyz_muxed;
    QData/*47:0*/ __PVT__alu_sum;

    // INTERNAL VARIABLES
    Vwasmetal_core__Syms* const vlSymsp;

    // CONSTRUCTORS
    Vwasmetal_core_DSP48E1__pi2(Vwasmetal_core__Syms* symsp, const char* v__name);
    ~Vwasmetal_core_DSP48E1__pi2();
    VL_UNCOPYABLE(Vwasmetal_core_DSP48E1__pi2);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
