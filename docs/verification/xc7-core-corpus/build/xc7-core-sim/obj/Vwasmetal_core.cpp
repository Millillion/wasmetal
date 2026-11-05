#pragma GCC diagnostic ignored "-Wint-in-bool-context"
#pragma GCC diagnostic ignored "-Wbool-operation"
#pragma GCC diagnostic ignored "-Wbitwise-instead-of-logical"
// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vwasmetal_core__pch.h"

//============================================================
// Constructors

Vwasmetal_core::Vwasmetal_core(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vwasmetal_core__Syms(contextp(), _vcname__, this)}
    , clk{vlSymsp->TOP.clk}
    , reset{vlSymsp->TOP.reset}
    , cmd_valid{vlSymsp->TOP.cmd_valid}
    , cmd_kind{vlSymsp->TOP.cmd_kind}
    , busy{vlSymsp->TOP.busy}
    , done{vlSymsp->TOP.done}
    , trap{vlSymsp->TOP.trap}
    , insn_valid{vlSymsp->TOP.insn_valid}
    , function_valid{vlSymsp->TOP.function_valid}
    , type_matches{vlSymsp->TOP.type_matches}
    , mem_valid{vlSymsp->TOP.mem_valid}
    , mem_write{vlSymsp->TOP.mem_write}
    , mem_kind{vlSymsp->TOP.mem_kind}
    , mem_bytes{vlSymsp->TOP.mem_bytes}
    , mem_ready{vlSymsp->TOP.mem_ready}
    , mem_fault{vlSymsp->TOP.mem_fault}
    , cmd_index{vlSymsp->TOP.cmd_index}
    , cmd_data{vlSymsp->TOP.cmd_data}
    , result_count{vlSymsp->TOP.result_count}
    , result_index{vlSymsp->TOP.result_index}
    , result_data{vlSymsp->TOP.result_data}
    , pc{vlSymsp->TOP.pc}
    , insn_op{vlSymsp->TOP.insn_op}
    , insn_x{vlSymsp->TOP.insn_x}
    , insn_y{vlSymsp->TOP.insn_y}
    , insn_z{vlSymsp->TOP.insn_z}
    , insn_w{vlSymsp->TOP.insn_w}
    , insn_imm{vlSymsp->TOP.insn_imm}
    , function_index{vlSymsp->TOP.function_index}
    , function_entry{vlSymsp->TOP.function_entry}
    , function_params{vlSymsp->TOP.function_params}
    , function_locals{vlSymsp->TOP.function_locals}
    , function_results{vlSymsp->TOP.function_results}
    , function_type{vlSymsp->TOP.function_type}
    , type_actual{vlSymsp->TOP.type_actual}
    , type_expected{vlSymsp->TOP.type_expected}
    , mem_index{vlSymsp->TOP.mem_index}
    , mem_wdata{vlSymsp->TOP.mem_wdata}
    , mem_rdata{vlSymsp->TOP.mem_rdata}
    , cmd_aux{vlSymsp->TOP.cmd_aux}
    , mem_address{vlSymsp->TOP.mem_address}
    , __PVT__wasmetal_core__DOT___134220_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___134220_}
    , __PVT__wasmetal_core__DOT___134221_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___134221_}
    , __PVT__wasmetal_core__DOT___134222_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___134222_}
    , __PVT__wasmetal_core__DOT___134223_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___134223_}
    , __PVT__wasmetal_core__DOT___134224_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___134224_}
    , __PVT__wasmetal_core__DOT___134225_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___134225_}
    , __PVT__wasmetal_core__DOT___134226_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___134226_}
    , __PVT__wasmetal_core__DOT___134227_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___134227_}
    , __PVT__wasmetal_core__DOT___134228_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___134228_}
    , __PVT__wasmetal_core__DOT___134229_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___134229_}
    , __PVT__wasmetal_core__DOT___134230_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___134230_}
    , __PVT__wasmetal_core__DOT___134231_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___134231_}
    , __PVT__wasmetal_core__DOT___134232_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___134232_}
    , __PVT__wasmetal_core__DOT___135064_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___135064_}
    , __PVT__wasmetal_core__DOT___135065_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___135065_}
    , __PVT__wasmetal_core__DOT___135066_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___135066_}
    , __PVT__wasmetal_core__DOT___135067_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___135067_}
    , __PVT__wasmetal_core__DOT___135068_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___135068_}
    , __PVT__wasmetal_core__DOT___135069_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___135069_}
    , __PVT__wasmetal_core__DOT___135070_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___135070_}
    , __PVT__wasmetal_core__DOT___135071_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___135071_}
    , __PVT__wasmetal_core__DOT___135072_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___135072_}
    , __PVT__wasmetal_core__DOT___135073_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___135073_}
    , __PVT__wasmetal_core__DOT___135074_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___135074_}
    , __PVT__wasmetal_core__DOT___135075_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___135075_}
    , __PVT__wasmetal_core__DOT___135195_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___135195_}
    , __PVT__wasmetal_core__DOT___135196_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___135196_}
    , __PVT__wasmetal_core__DOT___135426_{vlSymsp->TOP.__PVT__wasmetal_core__DOT___135426_}
    , __PVT__wasmetal_core__DOT__data_sizes__02ewords__02e0__02e0{vlSymsp->TOP.__PVT__wasmetal_core__DOT__data_sizes__02ewords__02e0__02e0}
    , __PVT__wasmetal_core__DOT__element_sizes__02ewords__02e0__02e0{vlSymsp->TOP.__PVT__wasmetal_core__DOT__element_sizes__02ewords__02e0__02e0}
    , __PVT__wasmetal_core__DOT__frames_memory__02e0__02e0{vlSymsp->TOP.__PVT__wasmetal_core__DOT__frames_memory__02e0__02e0}
    , __PVT__wasmetal_core__DOT__frames_memory__02e0__02e1{vlSymsp->TOP.__PVT__wasmetal_core__DOT__frames_memory__02e0__02e1}
    , __PVT__wasmetal_core__DOT__labels_memory__02e0__02e0{vlSymsp->TOP.__PVT__wasmetal_core__DOT__labels_memory__02e0__02e0}
    , __PVT__wasmetal_core__DOT__labels_memory__02e0__02e1{vlSymsp->TOP.__PVT__wasmetal_core__DOT__labels_memory__02e0__02e1}
    , __PVT__wasmetal_core__DOT__labels_memory__02e0__02e2{vlSymsp->TOP.__PVT__wasmetal_core__DOT__labels_memory__02e0__02e2}
    , __PVT__wasmetal_core__DOT__labels_memory__02e0__02e3{vlSymsp->TOP.__PVT__wasmetal_core__DOT__labels_memory__02e0__02e3}
    , __PVT__wasmetal_core__DOT__labels_memory__02e0__02e4{vlSymsp->TOP.__PVT__wasmetal_core__DOT__labels_memory__02e0__02e4}
    , __PVT__wasmetal_core__DOT__labels_memory__02e0__02e5{vlSymsp->TOP.__PVT__wasmetal_core__DOT__labels_memory__02e0__02e5}
    , __PVT__wasmetal_core__DOT__labels_memory__02e0__02e6{vlSymsp->TOP.__PVT__wasmetal_core__DOT__labels_memory__02e0__02e6}
    , __PVT__wasmetal_core__DOT__labels_memory__02e0__02e7{vlSymsp->TOP.__PVT__wasmetal_core__DOT__labels_memory__02e0__02e7}
    , __PVT__wasmetal_core__DOT__labels_memory__02e0__02e8{vlSymsp->TOP.__PVT__wasmetal_core__DOT__labels_memory__02e0__02e8}
    , __PVT__wasmetal_core__DOT__memory_bounds__02ewords__02e0__02e0{vlSymsp->TOP.__PVT__wasmetal_core__DOT__memory_bounds__02ewords__02e0__02e0}
    , __PVT__wasmetal_core__DOT__memory_sizes__02ewords__02e0__02e0{vlSymsp->TOP.__PVT__wasmetal_core__DOT__memory_sizes__02ewords__02e0__02e0}
    , __PVT__wasmetal_core__DOT__memory_sizes__02ewords__02e1__02e0{vlSymsp->TOP.__PVT__wasmetal_core__DOT__memory_sizes__02ewords__02e1__02e0}
    , __PVT__wasmetal_core__DOT__table_bounds__02ewords__02e0__02e0{vlSymsp->TOP.__PVT__wasmetal_core__DOT__table_bounds__02ewords__02e0__02e0}
    , __PVT__wasmetal_core__DOT__table_sizes__02ewords__02e0__02e0{vlSymsp->TOP.__PVT__wasmetal_core__DOT__table_sizes__02ewords__02e0__02e0}
    , __PVT__wasmetal_core__DOT__table_sizes__02ewords__02e1__02e0{vlSymsp->TOP.__PVT__wasmetal_core__DOT__table_sizes__02ewords__02e1__02e0}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e1{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e1}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e10{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e10}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e11{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e11}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e12{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e12}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e13{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e13}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e14{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e14}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e2{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e2}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e3{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e3}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e4{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e4}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e5{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e5}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e6{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e6}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e7{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e7}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e8{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e8}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e9{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e9}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e0{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e0}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e1{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e1}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e10{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e10}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e11{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e11}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e12{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e12}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e13{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e13}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e14{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e14}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e2{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e2}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e3{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e3}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e4{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e4}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e5{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e5}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e6{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e6}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e7{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e7}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e8{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e8}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e9{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e9}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e0{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e0}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e1{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e1}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e10{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e10}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e11{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e11}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e12{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e12}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e13{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e13}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e14{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e14}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e2{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e2}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e3{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e3}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e4{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e4}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e5{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e5}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e6{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e6}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e7{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e7}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e8{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e8}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e9{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e9}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e0{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e0}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e1{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e1}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e10{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e10}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e11{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e11}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e12{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e12}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e13{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e13}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e14{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e14}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e2{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e2}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e3{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e3}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e4{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e4}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e5{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e5}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e6{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e6}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e7{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e7}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e8{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e8}
    , __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e9{vlSymsp->TOP.__PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e9}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vwasmetal_core::Vwasmetal_core(const char* _vcname__)
    : Vwasmetal_core(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vwasmetal_core::~Vwasmetal_core() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vwasmetal_core___024root___eval_debug_assertions(Vwasmetal_core___024root* vlSelf);
#endif  // VL_DEBUG
void Vwasmetal_core___024root___eval_static(Vwasmetal_core___024root* vlSelf);
void Vwasmetal_core___024root___eval_initial(Vwasmetal_core___024root* vlSelf);
void Vwasmetal_core___024root___eval_settle(Vwasmetal_core___024root* vlSelf);
void Vwasmetal_core___024root___eval(Vwasmetal_core___024root* vlSelf);

void Vwasmetal_core::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vwasmetal_core::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vwasmetal_core___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        vlSymsp->__Vm_didInit = true;
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vwasmetal_core___024root___eval_static(&(vlSymsp->TOP));
        Vwasmetal_core___024root___eval_initial(&(vlSymsp->TOP));
        Vwasmetal_core___024root___eval_settle(&(vlSymsp->TOP));
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vwasmetal_core___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vwasmetal_core::eventsPending() { return false; }

uint64_t Vwasmetal_core::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "%Error: No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* Vwasmetal_core::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vwasmetal_core___024root___eval_final(Vwasmetal_core___024root* vlSelf);

VL_ATTR_COLD void Vwasmetal_core::final() {
    Vwasmetal_core___024root___eval_final(&(vlSymsp->TOP));
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vwasmetal_core::hierName() const { return vlSymsp->name(); }
const char* Vwasmetal_core::modelName() const { return "Vwasmetal_core"; }
unsigned Vwasmetal_core::threads() const { return 1; }
void Vwasmetal_core::prepareClone() const { contextp()->prepareClone(); }
void Vwasmetal_core::atClone() const {
    contextp()->threadPoolpOnClone();
}

//============================================================
// Trace configuration

VL_ATTR_COLD void Vwasmetal_core::trace(VerilatedVcdC* tfp, int levels, int options) {
    vl_fatal(__FILE__, __LINE__, __FILE__,"'Vwasmetal_core::trace()' called on model that was Verilated without --trace option");
}
