#pragma GCC diagnostic ignored "-Wint-in-bool-context"
#pragma GCC diagnostic ignored "-Wbool-operation"
#pragma GCC diagnostic ignored "-Wbitwise-instead-of-logical"
// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vwasmetal_core__pch.h"
#include "Vwasmetal_core.h"
#include "Vwasmetal_core___024root.h"
#include "Vwasmetal_core_DSP48E1__pi1.h"
#include "Vwasmetal_core_DSP48E1__pi2.h"
#include "Vwasmetal_core_RAMB36E1__pi4.h"
#include "Vwasmetal_core_RAMB36E1__pi5.h"
#include "Vwasmetal_core_RAMB18E1__pi6.h"

// FUNCTIONS
Vwasmetal_core__Syms::~Vwasmetal_core__Syms()
{
}

Vwasmetal_core__Syms::Vwasmetal_core__Syms(VerilatedContext* contextp, const char* namep, Vwasmetal_core* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup module instances
    , TOP{this, namep}
    , TOP__wasmetal_core__DOT___134220_{this, Verilated::catName(namep, "wasmetal_core._134220_")}
    , TOP__wasmetal_core__DOT___134221_{this, Verilated::catName(namep, "wasmetal_core._134221_")}
    , TOP__wasmetal_core__DOT___134222_{this, Verilated::catName(namep, "wasmetal_core._134222_")}
    , TOP__wasmetal_core__DOT___134223_{this, Verilated::catName(namep, "wasmetal_core._134223_")}
    , TOP__wasmetal_core__DOT___134224_{this, Verilated::catName(namep, "wasmetal_core._134224_")}
    , TOP__wasmetal_core__DOT___134225_{this, Verilated::catName(namep, "wasmetal_core._134225_")}
    , TOP__wasmetal_core__DOT___134226_{this, Verilated::catName(namep, "wasmetal_core._134226_")}
    , TOP__wasmetal_core__DOT___134227_{this, Verilated::catName(namep, "wasmetal_core._134227_")}
    , TOP__wasmetal_core__DOT___134228_{this, Verilated::catName(namep, "wasmetal_core._134228_")}
    , TOP__wasmetal_core__DOT___134229_{this, Verilated::catName(namep, "wasmetal_core._134229_")}
    , TOP__wasmetal_core__DOT___134230_{this, Verilated::catName(namep, "wasmetal_core._134230_")}
    , TOP__wasmetal_core__DOT___134231_{this, Verilated::catName(namep, "wasmetal_core._134231_")}
    , TOP__wasmetal_core__DOT___134232_{this, Verilated::catName(namep, "wasmetal_core._134232_")}
    , TOP__wasmetal_core__DOT___135064_{this, Verilated::catName(namep, "wasmetal_core._135064_")}
    , TOP__wasmetal_core__DOT___135065_{this, Verilated::catName(namep, "wasmetal_core._135065_")}
    , TOP__wasmetal_core__DOT___135066_{this, Verilated::catName(namep, "wasmetal_core._135066_")}
    , TOP__wasmetal_core__DOT___135067_{this, Verilated::catName(namep, "wasmetal_core._135067_")}
    , TOP__wasmetal_core__DOT___135068_{this, Verilated::catName(namep, "wasmetal_core._135068_")}
    , TOP__wasmetal_core__DOT___135069_{this, Verilated::catName(namep, "wasmetal_core._135069_")}
    , TOP__wasmetal_core__DOT___135070_{this, Verilated::catName(namep, "wasmetal_core._135070_")}
    , TOP__wasmetal_core__DOT___135071_{this, Verilated::catName(namep, "wasmetal_core._135071_")}
    , TOP__wasmetal_core__DOT___135072_{this, Verilated::catName(namep, "wasmetal_core._135072_")}
    , TOP__wasmetal_core__DOT___135073_{this, Verilated::catName(namep, "wasmetal_core._135073_")}
    , TOP__wasmetal_core__DOT___135074_{this, Verilated::catName(namep, "wasmetal_core._135074_")}
    , TOP__wasmetal_core__DOT___135075_{this, Verilated::catName(namep, "wasmetal_core._135075_")}
    , TOP__wasmetal_core__DOT___135195_{this, Verilated::catName(namep, "wasmetal_core._135195_")}
    , TOP__wasmetal_core__DOT___135196_{this, Verilated::catName(namep, "wasmetal_core._135196_")}
    , TOP__wasmetal_core__DOT___135426_{this, Verilated::catName(namep, "wasmetal_core._135426_")}
    , TOP__wasmetal_core__DOT__data_sizes__02ewords__02e0__02e0{this, Verilated::catName(namep, "wasmetal_core.data_sizes.words.0.0")}
    , TOP__wasmetal_core__DOT__element_sizes__02ewords__02e0__02e0{this, Verilated::catName(namep, "wasmetal_core.element_sizes.words.0.0")}
    , TOP__wasmetal_core__DOT__frames_memory__02e0__02e0{this, Verilated::catName(namep, "wasmetal_core.frames_memory.0.0")}
    , TOP__wasmetal_core__DOT__frames_memory__02e0__02e1{this, Verilated::catName(namep, "wasmetal_core.frames_memory.0.1")}
    , TOP__wasmetal_core__DOT__labels_memory__02e0__02e0{this, Verilated::catName(namep, "wasmetal_core.labels_memory.0.0")}
    , TOP__wasmetal_core__DOT__labels_memory__02e0__02e1{this, Verilated::catName(namep, "wasmetal_core.labels_memory.0.1")}
    , TOP__wasmetal_core__DOT__labels_memory__02e0__02e2{this, Verilated::catName(namep, "wasmetal_core.labels_memory.0.2")}
    , TOP__wasmetal_core__DOT__labels_memory__02e0__02e3{this, Verilated::catName(namep, "wasmetal_core.labels_memory.0.3")}
    , TOP__wasmetal_core__DOT__labels_memory__02e0__02e4{this, Verilated::catName(namep, "wasmetal_core.labels_memory.0.4")}
    , TOP__wasmetal_core__DOT__labels_memory__02e0__02e5{this, Verilated::catName(namep, "wasmetal_core.labels_memory.0.5")}
    , TOP__wasmetal_core__DOT__labels_memory__02e0__02e6{this, Verilated::catName(namep, "wasmetal_core.labels_memory.0.6")}
    , TOP__wasmetal_core__DOT__labels_memory__02e0__02e7{this, Verilated::catName(namep, "wasmetal_core.labels_memory.0.7")}
    , TOP__wasmetal_core__DOT__labels_memory__02e0__02e8{this, Verilated::catName(namep, "wasmetal_core.labels_memory.0.8")}
    , TOP__wasmetal_core__DOT__memory_bounds__02ewords__02e0__02e0{this, Verilated::catName(namep, "wasmetal_core.memory_bounds.words.0.0")}
    , TOP__wasmetal_core__DOT__memory_sizes__02ewords__02e0__02e0{this, Verilated::catName(namep, "wasmetal_core.memory_sizes.words.0.0")}
    , TOP__wasmetal_core__DOT__memory_sizes__02ewords__02e1__02e0{this, Verilated::catName(namep, "wasmetal_core.memory_sizes.words.1.0")}
    , TOP__wasmetal_core__DOT__table_bounds__02ewords__02e0__02e0{this, Verilated::catName(namep, "wasmetal_core.table_bounds.words.0.0")}
    , TOP__wasmetal_core__DOT__table_sizes__02ewords__02e0__02e0{this, Verilated::catName(namep, "wasmetal_core.table_sizes.words.0.0")}
    , TOP__wasmetal_core__DOT__table_sizes__02ewords__02e1__02e0{this, Verilated::catName(namep, "wasmetal_core.table_sizes.words.1.0")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[0].words.0.0")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e1{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[0].words.0.1")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e10{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[0].words.0.10")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e11{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[0].words.0.11")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e12{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[0].words.0.12")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e13{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[0].words.0.13")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e14{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[0].words.0.14")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e2{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[0].words.0.2")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e3{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[0].words.0.3")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e4{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[0].words.0.4")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e5{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[0].words.0.5")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e6{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[0].words.0.6")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e7{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[0].words.0.7")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e8{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[0].words.0.8")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e9{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[0].words.0.9")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e0{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[1].words.0.0")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e1{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[1].words.0.1")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e10{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[1].words.0.10")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e11{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[1].words.0.11")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e12{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[1].words.0.12")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e13{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[1].words.0.13")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e14{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[1].words.0.14")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e2{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[1].words.0.2")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e3{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[1].words.0.3")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e4{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[1].words.0.4")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e5{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[1].words.0.5")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e6{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[1].words.0.6")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e7{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[1].words.0.7")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e8{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[1].words.0.8")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e9{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[1].words.0.9")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e0{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[2].words.0.0")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e1{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[2].words.0.1")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e10{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[2].words.0.10")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e11{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[2].words.0.11")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e12{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[2].words.0.12")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e13{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[2].words.0.13")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e14{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[2].words.0.14")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e2{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[2].words.0.2")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e3{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[2].words.0.3")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e4{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[2].words.0.4")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e5{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[2].words.0.5")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e6{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[2].words.0.6")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e7{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[2].words.0.7")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e8{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[2].words.0.8")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e9{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[2].words.0.9")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e0{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[3].words.0.0")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e1{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[3].words.0.1")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e10{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[3].words.0.10")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e11{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[3].words.0.11")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e12{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[3].words.0.12")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e13{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[3].words.0.13")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e14{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[3].words.0.14")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e2{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[3].words.0.2")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e3{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[3].words.0.3")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e4{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[3].words.0.4")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e5{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[3].words.0.5")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e6{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[3].words.0.6")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e7{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[3].words.0.7")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e8{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[3].words.0.8")}
    , TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e9{this, Verilated::catName(namep, "wasmetal_core.value_file.banks[3].words.0.9")}
{
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-12);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    TOP.__PVT__wasmetal_core__DOT___134220_ = &TOP__wasmetal_core__DOT___134220_;
    TOP.__PVT__wasmetal_core__DOT___134221_ = &TOP__wasmetal_core__DOT___134221_;
    TOP.__PVT__wasmetal_core__DOT___134222_ = &TOP__wasmetal_core__DOT___134222_;
    TOP.__PVT__wasmetal_core__DOT___134223_ = &TOP__wasmetal_core__DOT___134223_;
    TOP.__PVT__wasmetal_core__DOT___134224_ = &TOP__wasmetal_core__DOT___134224_;
    TOP.__PVT__wasmetal_core__DOT___134225_ = &TOP__wasmetal_core__DOT___134225_;
    TOP.__PVT__wasmetal_core__DOT___134226_ = &TOP__wasmetal_core__DOT___134226_;
    TOP.__PVT__wasmetal_core__DOT___134227_ = &TOP__wasmetal_core__DOT___134227_;
    TOP.__PVT__wasmetal_core__DOT___134228_ = &TOP__wasmetal_core__DOT___134228_;
    TOP.__PVT__wasmetal_core__DOT___134229_ = &TOP__wasmetal_core__DOT___134229_;
    TOP.__PVT__wasmetal_core__DOT___134230_ = &TOP__wasmetal_core__DOT___134230_;
    TOP.__PVT__wasmetal_core__DOT___134231_ = &TOP__wasmetal_core__DOT___134231_;
    TOP.__PVT__wasmetal_core__DOT___134232_ = &TOP__wasmetal_core__DOT___134232_;
    TOP.__PVT__wasmetal_core__DOT___135064_ = &TOP__wasmetal_core__DOT___135064_;
    TOP.__PVT__wasmetal_core__DOT___135065_ = &TOP__wasmetal_core__DOT___135065_;
    TOP.__PVT__wasmetal_core__DOT___135066_ = &TOP__wasmetal_core__DOT___135066_;
    TOP.__PVT__wasmetal_core__DOT___135067_ = &TOP__wasmetal_core__DOT___135067_;
    TOP.__PVT__wasmetal_core__DOT___135068_ = &TOP__wasmetal_core__DOT___135068_;
    TOP.__PVT__wasmetal_core__DOT___135069_ = &TOP__wasmetal_core__DOT___135069_;
    TOP.__PVT__wasmetal_core__DOT___135070_ = &TOP__wasmetal_core__DOT___135070_;
    TOP.__PVT__wasmetal_core__DOT___135071_ = &TOP__wasmetal_core__DOT___135071_;
    TOP.__PVT__wasmetal_core__DOT___135072_ = &TOP__wasmetal_core__DOT___135072_;
    TOP.__PVT__wasmetal_core__DOT___135073_ = &TOP__wasmetal_core__DOT___135073_;
    TOP.__PVT__wasmetal_core__DOT___135074_ = &TOP__wasmetal_core__DOT___135074_;
    TOP.__PVT__wasmetal_core__DOT___135075_ = &TOP__wasmetal_core__DOT___135075_;
    TOP.__PVT__wasmetal_core__DOT___135195_ = &TOP__wasmetal_core__DOT___135195_;
    TOP.__PVT__wasmetal_core__DOT___135196_ = &TOP__wasmetal_core__DOT___135196_;
    TOP.__PVT__wasmetal_core__DOT___135426_ = &TOP__wasmetal_core__DOT___135426_;
    TOP.__PVT__wasmetal_core__DOT__data_sizes__02ewords__02e0__02e0 = &TOP__wasmetal_core__DOT__data_sizes__02ewords__02e0__02e0;
    TOP.__PVT__wasmetal_core__DOT__element_sizes__02ewords__02e0__02e0 = &TOP__wasmetal_core__DOT__element_sizes__02ewords__02e0__02e0;
    TOP.__PVT__wasmetal_core__DOT__frames_memory__02e0__02e0 = &TOP__wasmetal_core__DOT__frames_memory__02e0__02e0;
    TOP.__PVT__wasmetal_core__DOT__frames_memory__02e0__02e1 = &TOP__wasmetal_core__DOT__frames_memory__02e0__02e1;
    TOP.__PVT__wasmetal_core__DOT__labels_memory__02e0__02e0 = &TOP__wasmetal_core__DOT__labels_memory__02e0__02e0;
    TOP.__PVT__wasmetal_core__DOT__labels_memory__02e0__02e1 = &TOP__wasmetal_core__DOT__labels_memory__02e0__02e1;
    TOP.__PVT__wasmetal_core__DOT__labels_memory__02e0__02e2 = &TOP__wasmetal_core__DOT__labels_memory__02e0__02e2;
    TOP.__PVT__wasmetal_core__DOT__labels_memory__02e0__02e3 = &TOP__wasmetal_core__DOT__labels_memory__02e0__02e3;
    TOP.__PVT__wasmetal_core__DOT__labels_memory__02e0__02e4 = &TOP__wasmetal_core__DOT__labels_memory__02e0__02e4;
    TOP.__PVT__wasmetal_core__DOT__labels_memory__02e0__02e5 = &TOP__wasmetal_core__DOT__labels_memory__02e0__02e5;
    TOP.__PVT__wasmetal_core__DOT__labels_memory__02e0__02e6 = &TOP__wasmetal_core__DOT__labels_memory__02e0__02e6;
    TOP.__PVT__wasmetal_core__DOT__labels_memory__02e0__02e7 = &TOP__wasmetal_core__DOT__labels_memory__02e0__02e7;
    TOP.__PVT__wasmetal_core__DOT__labels_memory__02e0__02e8 = &TOP__wasmetal_core__DOT__labels_memory__02e0__02e8;
    TOP.__PVT__wasmetal_core__DOT__memory_bounds__02ewords__02e0__02e0 = &TOP__wasmetal_core__DOT__memory_bounds__02ewords__02e0__02e0;
    TOP.__PVT__wasmetal_core__DOT__memory_sizes__02ewords__02e0__02e0 = &TOP__wasmetal_core__DOT__memory_sizes__02ewords__02e0__02e0;
    TOP.__PVT__wasmetal_core__DOT__memory_sizes__02ewords__02e1__02e0 = &TOP__wasmetal_core__DOT__memory_sizes__02ewords__02e1__02e0;
    TOP.__PVT__wasmetal_core__DOT__table_bounds__02ewords__02e0__02e0 = &TOP__wasmetal_core__DOT__table_bounds__02ewords__02e0__02e0;
    TOP.__PVT__wasmetal_core__DOT__table_sizes__02ewords__02e0__02e0 = &TOP__wasmetal_core__DOT__table_sizes__02ewords__02e0__02e0;
    TOP.__PVT__wasmetal_core__DOT__table_sizes__02ewords__02e1__02e0 = &TOP__wasmetal_core__DOT__table_sizes__02ewords__02e1__02e0;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e1 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e1;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e10 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e10;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e11 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e11;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e12 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e12;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e13 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e13;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e14 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e14;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e2 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e2;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e3 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e3;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e4 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e4;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e5 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e5;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e6 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e6;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e7 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e7;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e8 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e8;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e9 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e9;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e0 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e0;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e1 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e1;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e10 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e10;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e11 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e11;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e12 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e12;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e13 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e13;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e14 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e14;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e2 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e2;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e3 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e3;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e4 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e4;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e5 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e5;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e6 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e6;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e7 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e7;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e8 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e8;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e9 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e9;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e0 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e0;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e1 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e1;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e10 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e10;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e11 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e11;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e12 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e12;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e13 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e13;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e14 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e14;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e2 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e2;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e3 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e3;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e4 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e4;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e5 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e5;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e6 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e6;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e7 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e7;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e8 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e8;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e9 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e9;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e0 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e0;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e1 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e1;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e10 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e10;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e11 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e11;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e12 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e12;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e13 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e13;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e14 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e14;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e2 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e2;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e3 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e3;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e4 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e4;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e5 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e5;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e6 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e6;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e7 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e7;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e8 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e8;
    TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e9 = &TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e9;
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    TOP__wasmetal_core__DOT___134220_.__Vconfigure(true);
    TOP__wasmetal_core__DOT___134221_.__Vconfigure(true);
    TOP__wasmetal_core__DOT___134222_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___134223_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___134224_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___134225_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___134226_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___134227_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___134228_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___134229_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___134230_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___134231_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___134232_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___135064_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___135065_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___135066_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___135067_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___135068_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___135069_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___135070_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___135071_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___135072_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___135073_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___135074_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___135075_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___135195_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___135196_.__Vconfigure(false);
    TOP__wasmetal_core__DOT___135426_.__Vconfigure(false);
    TOP__wasmetal_core__DOT__data_sizes__02ewords__02e0__02e0.__Vconfigure(true);
    TOP__wasmetal_core__DOT__element_sizes__02ewords__02e0__02e0.__Vconfigure(false);
    TOP__wasmetal_core__DOT__frames_memory__02e0__02e0.__Vconfigure(false);
    TOP__wasmetal_core__DOT__frames_memory__02e0__02e1.__Vconfigure(false);
    TOP__wasmetal_core__DOT__labels_memory__02e0__02e0.__Vconfigure(true);
    TOP__wasmetal_core__DOT__labels_memory__02e0__02e1.__Vconfigure(false);
    TOP__wasmetal_core__DOT__labels_memory__02e0__02e2.__Vconfigure(false);
    TOP__wasmetal_core__DOT__labels_memory__02e0__02e3.__Vconfigure(false);
    TOP__wasmetal_core__DOT__labels_memory__02e0__02e4.__Vconfigure(false);
    TOP__wasmetal_core__DOT__labels_memory__02e0__02e5.__Vconfigure(false);
    TOP__wasmetal_core__DOT__labels_memory__02e0__02e6.__Vconfigure(false);
    TOP__wasmetal_core__DOT__labels_memory__02e0__02e7.__Vconfigure(false);
    TOP__wasmetal_core__DOT__labels_memory__02e0__02e8.__Vconfigure(false);
    TOP__wasmetal_core__DOT__memory_bounds__02ewords__02e0__02e0.__Vconfigure(false);
    TOP__wasmetal_core__DOT__memory_sizes__02ewords__02e0__02e0.__Vconfigure(false);
    TOP__wasmetal_core__DOT__memory_sizes__02ewords__02e1__02e0.__Vconfigure(false);
    TOP__wasmetal_core__DOT__table_bounds__02ewords__02e0__02e0.__Vconfigure(false);
    TOP__wasmetal_core__DOT__table_sizes__02ewords__02e0__02e0.__Vconfigure(false);
    TOP__wasmetal_core__DOT__table_sizes__02ewords__02e1__02e0.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0.__Vconfigure(true);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e1.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e10.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e11.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e12.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e13.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e14.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e2.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e3.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e4.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e5.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e6.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e7.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e8.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e9.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e0.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e1.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e10.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e11.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e12.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e13.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e14.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e2.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e3.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e4.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e5.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e6.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e7.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e8.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e9.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e0.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e1.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e10.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e11.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e12.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e13.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e14.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e2.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e3.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e4.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e5.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e6.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e7.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e8.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e9.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e0.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e1.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e10.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e11.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e12.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e13.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e14.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e2.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e3.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e4.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e5.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e6.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e7.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e8.__Vconfigure(false);
    TOP__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e9.__Vconfigure(false);
    // Setup scopes
    __Vscope_wasmetal_core__data_sizes__02ewords__02e0__02e0__memory.configure(this, name(), "wasmetal_core.data_sizes.words.0.0.memory", "memory", -12, VerilatedScope::SCOPE_OTHER);
    __Vscope_wasmetal_core__element_sizes__02ewords__02e0__02e0__memory.configure(this, name(), "wasmetal_core.element_sizes.words.0.0.memory", "memory", -12, VerilatedScope::SCOPE_OTHER);
    __Vscope_wasmetal_core__frames_memory__02e0__02e0__memory.configure(this, name(), "wasmetal_core.frames_memory.0.0.memory", "memory", -12, VerilatedScope::SCOPE_OTHER);
    __Vscope_wasmetal_core__frames_memory__02e0__02e1__memory.configure(this, name(), "wasmetal_core.frames_memory.0.1.memory", "memory", -12, VerilatedScope::SCOPE_OTHER);
    __Vscope_wasmetal_core__memory_bounds__02ewords__02e0__02e0__memory.configure(this, name(), "wasmetal_core.memory_bounds.words.0.0.memory", "memory", -12, VerilatedScope::SCOPE_OTHER);
    __Vscope_wasmetal_core__memory_sizes__02ewords__02e0__02e0__memory.configure(this, name(), "wasmetal_core.memory_sizes.words.0.0.memory", "memory", -12, VerilatedScope::SCOPE_OTHER);
    __Vscope_wasmetal_core__memory_sizes__02ewords__02e1__02e0__memory.configure(this, name(), "wasmetal_core.memory_sizes.words.1.0.memory", "memory", -12, VerilatedScope::SCOPE_OTHER);
    __Vscope_wasmetal_core__table_bounds__02ewords__02e0__02e0__memory.configure(this, name(), "wasmetal_core.table_bounds.words.0.0.memory", "memory", -12, VerilatedScope::SCOPE_OTHER);
    __Vscope_wasmetal_core__table_sizes__02ewords__02e0__02e0__memory.configure(this, name(), "wasmetal_core.table_sizes.words.0.0.memory", "memory", -12, VerilatedScope::SCOPE_OTHER);
    __Vscope_wasmetal_core__table_sizes__02ewords__02e1__02e0__memory.configure(this, name(), "wasmetal_core.table_sizes.words.1.0.memory", "memory", -12, VerilatedScope::SCOPE_OTHER);
}
