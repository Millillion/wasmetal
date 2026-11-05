// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vsky130_sram_tb__pch.h"

//============================================================
// Constructors

Vsky130_sram_tb::Vsky130_sram_tb(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vsky130_sram_tb__Syms(contextp(), _vcname__, this)}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vsky130_sram_tb::Vsky130_sram_tb(const char* _vcname__)
    : Vsky130_sram_tb(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vsky130_sram_tb::~Vsky130_sram_tb() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vsky130_sram_tb___024root___eval_debug_assertions(Vsky130_sram_tb___024root* vlSelf);
#endif  // VL_DEBUG
void Vsky130_sram_tb___024root___eval_static(Vsky130_sram_tb___024root* vlSelf);
void Vsky130_sram_tb___024root___eval_initial(Vsky130_sram_tb___024root* vlSelf);
void Vsky130_sram_tb___024root___eval_settle(Vsky130_sram_tb___024root* vlSelf);
void Vsky130_sram_tb___024root___eval(Vsky130_sram_tb___024root* vlSelf);

void Vsky130_sram_tb::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vsky130_sram_tb::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vsky130_sram_tb___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        vlSymsp->__Vm_didInit = true;
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vsky130_sram_tb___024root___eval_static(&(vlSymsp->TOP));
        Vsky130_sram_tb___024root___eval_initial(&(vlSymsp->TOP));
        Vsky130_sram_tb___024root___eval_settle(&(vlSymsp->TOP));
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vsky130_sram_tb___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vsky130_sram_tb::eventsPending() { return !vlSymsp->TOP.__VdlySched.empty(); }

uint64_t Vsky130_sram_tb::nextTimeSlot() { return vlSymsp->TOP.__VdlySched.nextTimeSlot(); }

//============================================================
// Utilities

const char* Vsky130_sram_tb::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vsky130_sram_tb___024root___eval_final(Vsky130_sram_tb___024root* vlSelf);

VL_ATTR_COLD void Vsky130_sram_tb::final() {
    Vsky130_sram_tb___024root___eval_final(&(vlSymsp->TOP));
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vsky130_sram_tb::hierName() const { return vlSymsp->name(); }
const char* Vsky130_sram_tb::modelName() const { return "Vsky130_sram_tb"; }
unsigned Vsky130_sram_tb::threads() const { return 1; }
void Vsky130_sram_tb::prepareClone() const { contextp()->prepareClone(); }
void Vsky130_sram_tb::atClone() const {
    contextp()->threadPoolpOnClone();
}

//============================================================
// Trace configuration

VL_ATTR_COLD void Vsky130_sram_tb::trace(VerilatedVcdC* tfp, int levels, int options) {
    vl_fatal(__FILE__, __LINE__, __FILE__,"'Vsky130_sram_tb::trace()' called on model that was Verilated without --trace option");
}
