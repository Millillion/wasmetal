#pragma GCC diagnostic ignored "-Wint-in-bool-context"
#pragma GCC diagnostic ignored "-Wbool-operation"
#pragma GCC diagnostic ignored "-Wbitwise-instead-of-logical"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vwasmetal_core.h for the primary calling header

#include "Vwasmetal_core__pch.h"
#include "Vwasmetal_core_DSP48E1__pi2.h"

VL_ATTR_COLD void Vwasmetal_core_DSP48E1__pi2___eval_static__TOP__wasmetal_core__DOT___134221_(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___eval_static__TOP__wasmetal_core__DOT___134221_\n"); );
    // Body
    vlSelf->__PVT__Mr = 0ULL;
}

VL_ATTR_COLD void Vwasmetal_core_DSP48E1__pi2___ctor_var_reset(Vwasmetal_core_DSP48E1__pi2* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vwasmetal_core__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vwasmetal_core_DSP48E1__pi2___ctor_var_reset\n"); );
    // Body
    vlSelf->ACOUT = VL_RAND_RESET_I(30);
    vlSelf->__PVT__BCOUT = VL_RAND_RESET_I(18);
    vlSelf->__PVT__CARRYCASCOUT = VL_RAND_RESET_I(1);
    vlSelf->__PVT__CARRYOUT = VL_RAND_RESET_I(4);
    vlSelf->__PVT__MULTSIGNOUT = VL_RAND_RESET_I(1);
    vlSelf->__PVT__OVERFLOW = VL_RAND_RESET_I(1);
    vlSelf->P = VL_RAND_RESET_Q(48);
    vlSelf->__PVT__PATTERNBDETECT = VL_RAND_RESET_I(1);
    vlSelf->__PVT__PATTERNDETECT = VL_RAND_RESET_I(1);
    vlSelf->PCOUT = VL_RAND_RESET_Q(48);
    vlSelf->__PVT__UNDERFLOW = VL_RAND_RESET_I(1);
    vlSelf->A = VL_RAND_RESET_I(30);
    vlSelf->ACIN = VL_RAND_RESET_I(30);
    vlSelf->ALUMODE = VL_RAND_RESET_I(4);
    vlSelf->B = VL_RAND_RESET_I(18);
    vlSelf->BCIN = VL_RAND_RESET_I(18);
    vlSelf->C = VL_RAND_RESET_Q(48);
    vlSelf->__PVT__CARRYCASCIN = VL_RAND_RESET_I(1);
    vlSelf->CARRYIN = VL_RAND_RESET_I(1);
    vlSelf->CARRYINSEL = VL_RAND_RESET_I(3);
    vlSelf->__PVT__CEA1 = VL_RAND_RESET_I(1);
    vlSelf->__PVT__CEA2 = VL_RAND_RESET_I(1);
    vlSelf->__PVT__CEAD = VL_RAND_RESET_I(1);
    vlSelf->__PVT__CEALUMODE = VL_RAND_RESET_I(1);
    vlSelf->__PVT__CEB1 = VL_RAND_RESET_I(1);
    vlSelf->__PVT__CEB2 = VL_RAND_RESET_I(1);
    vlSelf->__PVT__CEC = VL_RAND_RESET_I(1);
    vlSelf->__PVT__CECARRYIN = VL_RAND_RESET_I(1);
    vlSelf->__PVT__CECTRL = VL_RAND_RESET_I(1);
    vlSelf->__PVT__CED = VL_RAND_RESET_I(1);
    vlSelf->__PVT__CEINMODE = VL_RAND_RESET_I(1);
    vlSelf->__PVT__CEM = VL_RAND_RESET_I(1);
    vlSelf->__PVT__CEP = VL_RAND_RESET_I(1);
    vlSelf->__PVT__CLK = VL_RAND_RESET_I(1);
    vlSelf->D = VL_RAND_RESET_I(25);
    vlSelf->INMODE = VL_RAND_RESET_I(5);
    vlSelf->__PVT__MULTSIGNIN = VL_RAND_RESET_I(1);
    vlSelf->OPMODE = VL_RAND_RESET_I(7);
    vlSelf->PCIN = VL_RAND_RESET_Q(48);
    vlSelf->__PVT__RSTA = VL_RAND_RESET_I(1);
    vlSelf->__PVT__RSTALLCARRYIN = VL_RAND_RESET_I(1);
    vlSelf->__PVT__RSTALUMODE = VL_RAND_RESET_I(1);
    vlSelf->__PVT__RSTB = VL_RAND_RESET_I(1);
    vlSelf->__PVT__RSTC = VL_RAND_RESET_I(1);
    vlSelf->__PVT__RSTCTRL = VL_RAND_RESET_I(1);
    vlSelf->__PVT__RSTD = VL_RAND_RESET_I(1);
    vlSelf->__PVT__RSTINMODE = VL_RAND_RESET_I(1);
    vlSelf->__PVT__RSTM = VL_RAND_RESET_I(1);
    vlSelf->__PVT__RSTP = VL_RAND_RESET_I(1);
    vlSelf->__PVT__Mr = VL_RAND_RESET_Q(43);
    vlSelf->__PVT__maj_xyz = VL_RAND_RESET_Q(48);
    vlSelf->__PVT__xor_xyz_muxed = VL_RAND_RESET_Q(48);
    vlSelf->__PVT__alu_sum = VL_RAND_RESET_Q(48);
    vlSelf->__VdfgTmp_h4c2f98f1__0 = 0;
    vlSelf->__VdfgTmp_ha5045b21__0 = 0;
}
