// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Primary model header
//
// This header should be included by all source files instantiating the design.
// The class here is then constructed to instantiate the design.
// See the Verilator manual for examples.

#ifndef VERILATED_VWASMETAL_CORE_H_
#define VERILATED_VWASMETAL_CORE_H_  // guard

#include "verilated.h"

class Vwasmetal_core__Syms;
class Vwasmetal_core___024root;
class Vwasmetal_core_DSP48E1__pi1;
class Vwasmetal_core_DSP48E1__pi2;
class Vwasmetal_core_RAMB18E1__pi6;
class Vwasmetal_core_RAMB36E1__pi4;
class Vwasmetal_core_RAMB36E1__pi5;


// This class is the main interface to the Verilated model
class alignas(VL_CACHE_LINE_BYTES) Vwasmetal_core VL_NOT_FINAL : public VerilatedModel {
  private:
    // Symbol table holding complete model state (owned by this class)
    Vwasmetal_core__Syms* const vlSymsp;

  public:

    // PORTS
    // The application code writes and reads these signals to
    // propagate new values into/out from the Verilated model.
    VL_IN8(&clk,0,0);
    VL_IN8(&reset,0,0);
    VL_IN8(&cmd_valid,0,0);
    VL_IN8(&cmd_kind,3,0);
    VL_OUT8(&busy,0,0);
    VL_OUT8(&done,0,0);
    VL_OUT8(&trap,7,0);
    VL_IN8(&insn_valid,0,0);
    VL_IN8(&function_valid,0,0);
    VL_IN8(&type_matches,0,0);
    VL_OUT8(&mem_valid,0,0);
    VL_OUT8(&mem_write,0,0);
    VL_OUT8(&mem_kind,2,0);
    VL_OUT8(&mem_bytes,4,0);
    VL_IN8(&mem_ready,0,0);
    VL_IN8(&mem_fault,0,0);
    VL_IN(&cmd_index,31,0);
    VL_INW(&cmd_data,127,0,4);
    VL_OUT(&result_count,31,0);
    VL_IN(&result_index,31,0);
    VL_OUTW(&result_data,127,0,4);
    VL_OUT(&pc,31,0);
    VL_IN(&insn_op,31,0);
    VL_IN(&insn_x,31,0);
    VL_IN(&insn_y,31,0);
    VL_IN(&insn_z,31,0);
    VL_IN(&insn_w,31,0);
    VL_INW(&insn_imm,127,0,4);
    VL_OUT(&function_index,31,0);
    VL_IN(&function_entry,31,0);
    VL_IN(&function_params,31,0);
    VL_IN(&function_locals,31,0);
    VL_IN(&function_results,31,0);
    VL_IN(&function_type,31,0);
    VL_OUT(&type_actual,31,0);
    VL_OUT(&type_expected,31,0);
    VL_OUT(&mem_index,31,0);
    VL_OUTW(&mem_wdata,127,0,4);
    VL_INW(&mem_rdata,127,0,4);
    VL_IN64(&cmd_aux,63,0);
    VL_OUT64(&mem_address,63,0);

    // CELLS
    // Public to allow access to /* verilator public */ items.
    // Otherwise the application code can consider these internals.
    Vwasmetal_core_DSP48E1__pi1* const __PVT__wasmetal_core__DOT___134220_;
    Vwasmetal_core_DSP48E1__pi2* const __PVT__wasmetal_core__DOT___134221_;
    Vwasmetal_core_DSP48E1__pi1* const __PVT__wasmetal_core__DOT___134222_;
    Vwasmetal_core_DSP48E1__pi2* const __PVT__wasmetal_core__DOT___134223_;
    Vwasmetal_core_DSP48E1__pi2* const __PVT__wasmetal_core__DOT___134224_;
    Vwasmetal_core_DSP48E1__pi1* const __PVT__wasmetal_core__DOT___134225_;
    Vwasmetal_core_DSP48E1__pi2* const __PVT__wasmetal_core__DOT___134226_;
    Vwasmetal_core_DSP48E1__pi2* const __PVT__wasmetal_core__DOT___134227_;
    Vwasmetal_core_DSP48E1__pi1* const __PVT__wasmetal_core__DOT___134228_;
    Vwasmetal_core_DSP48E1__pi2* const __PVT__wasmetal_core__DOT___134229_;
    Vwasmetal_core_DSP48E1__pi1* const __PVT__wasmetal_core__DOT___134230_;
    Vwasmetal_core_DSP48E1__pi2* const __PVT__wasmetal_core__DOT___134231_;
    Vwasmetal_core_DSP48E1__pi1* const __PVT__wasmetal_core__DOT___134232_;
    Vwasmetal_core_DSP48E1__pi2* const __PVT__wasmetal_core__DOT___135064_;
    Vwasmetal_core_DSP48E1__pi1* const __PVT__wasmetal_core__DOT___135065_;
    Vwasmetal_core_DSP48E1__pi2* const __PVT__wasmetal_core__DOT___135066_;
    Vwasmetal_core_DSP48E1__pi2* const __PVT__wasmetal_core__DOT___135067_;
    Vwasmetal_core_DSP48E1__pi2* const __PVT__wasmetal_core__DOT___135068_;
    Vwasmetal_core_DSP48E1__pi1* const __PVT__wasmetal_core__DOT___135069_;
    Vwasmetal_core_DSP48E1__pi2* const __PVT__wasmetal_core__DOT___135070_;
    Vwasmetal_core_DSP48E1__pi2* const __PVT__wasmetal_core__DOT___135071_;
    Vwasmetal_core_DSP48E1__pi2* const __PVT__wasmetal_core__DOT___135072_;
    Vwasmetal_core_DSP48E1__pi1* const __PVT__wasmetal_core__DOT___135073_;
    Vwasmetal_core_DSP48E1__pi2* const __PVT__wasmetal_core__DOT___135074_;
    Vwasmetal_core_DSP48E1__pi2* const __PVT__wasmetal_core__DOT___135075_;
    Vwasmetal_core_DSP48E1__pi1* const __PVT__wasmetal_core__DOT___135195_;
    Vwasmetal_core_DSP48E1__pi1* const __PVT__wasmetal_core__DOT___135196_;
    Vwasmetal_core_DSP48E1__pi1* const __PVT__wasmetal_core__DOT___135426_;
    Vwasmetal_core_RAMB36E1__pi4* const __PVT__wasmetal_core__DOT__data_sizes__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB36E1__pi4* const __PVT__wasmetal_core__DOT__element_sizes__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB36E1__pi4* const __PVT__wasmetal_core__DOT__frames_memory__02e0__02e0;
    Vwasmetal_core_RAMB36E1__pi4* const __PVT__wasmetal_core__DOT__frames_memory__02e0__02e1;
    Vwasmetal_core_RAMB36E1__pi5* const __PVT__wasmetal_core__DOT__labels_memory__02e0__02e0;
    Vwasmetal_core_RAMB36E1__pi5* const __PVT__wasmetal_core__DOT__labels_memory__02e0__02e1;
    Vwasmetal_core_RAMB36E1__pi5* const __PVT__wasmetal_core__DOT__labels_memory__02e0__02e2;
    Vwasmetal_core_RAMB36E1__pi5* const __PVT__wasmetal_core__DOT__labels_memory__02e0__02e3;
    Vwasmetal_core_RAMB36E1__pi5* const __PVT__wasmetal_core__DOT__labels_memory__02e0__02e4;
    Vwasmetal_core_RAMB36E1__pi5* const __PVT__wasmetal_core__DOT__labels_memory__02e0__02e5;
    Vwasmetal_core_RAMB36E1__pi5* const __PVT__wasmetal_core__DOT__labels_memory__02e0__02e6;
    Vwasmetal_core_RAMB36E1__pi5* const __PVT__wasmetal_core__DOT__labels_memory__02e0__02e7;
    Vwasmetal_core_RAMB36E1__pi5* const __PVT__wasmetal_core__DOT__labels_memory__02e0__02e8;
    Vwasmetal_core_RAMB36E1__pi4* const __PVT__wasmetal_core__DOT__memory_bounds__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB36E1__pi4* const __PVT__wasmetal_core__DOT__memory_sizes__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB36E1__pi4* const __PVT__wasmetal_core__DOT__memory_sizes__02ewords__02e1__02e0;
    Vwasmetal_core_RAMB36E1__pi4* const __PVT__wasmetal_core__DOT__table_bounds__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB36E1__pi4* const __PVT__wasmetal_core__DOT__table_sizes__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB36E1__pi4* const __PVT__wasmetal_core__DOT__table_sizes__02ewords__02e1__02e0;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e1;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e10;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e11;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e12;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e13;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e14;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e2;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e3;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e4;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e5;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e6;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e7;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e8;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b0__05d__02ewords__02e0__02e9;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e1;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e10;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e11;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e12;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e13;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e14;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e2;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e3;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e4;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e5;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e6;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e7;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e8;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b1__05d__02ewords__02e0__02e9;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e1;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e10;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e11;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e12;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e13;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e14;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e2;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e3;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e4;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e5;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e6;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e7;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e8;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b2__05d__02ewords__02e0__02e9;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e0;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e1;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e10;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e11;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e12;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e13;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e14;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e2;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e3;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e4;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e5;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e6;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e7;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e8;
    Vwasmetal_core_RAMB18E1__pi6* const __PVT__wasmetal_core__DOT__value_file__02ebanks__05b3__05d__02ewords__02e0__02e9;

    // Root instance pointer to allow access to model internals,
    // including inlined /* verilator public_flat_* */ items.
    Vwasmetal_core___024root* const rootp;

    // CONSTRUCTORS
    /// Construct the model; called by application code
    /// If contextp is null, then the model will use the default global context
    /// If name is "", then makes a wrapper with a
    /// single model invisible with respect to DPI scope names.
    explicit Vwasmetal_core(VerilatedContext* contextp, const char* name = "TOP");
    explicit Vwasmetal_core(const char* name = "TOP");
    /// Destroy the model; called (often implicitly) by application code
    virtual ~Vwasmetal_core();
  private:
    VL_UNCOPYABLE(Vwasmetal_core);  ///< Copying not allowed

  public:
    // API METHODS
    /// Evaluate the model.  Application must call when inputs change.
    void eval() { eval_step(); }
    /// Evaluate when calling multiple units/models per time step.
    void eval_step();
    /// Evaluate at end of a timestep for tracing, when using eval_step().
    /// Application must call after all eval() and before time changes.
    void eval_end_step() {}
    /// Simulation complete, run final blocks.  Application must call on completion.
    void final();
    /// Are there scheduled events to handle?
    bool eventsPending();
    /// Returns time at next time slot. Aborts if !eventsPending()
    uint64_t nextTimeSlot();
    /// Trace signals in the model; called by application code
    void trace(VerilatedVcdC* tfp, int levels, int options = 0);
    /// Retrieve name of this model instance (as passed to constructor).
    const char* name() const;

    // Abstract methods from VerilatedModel
    const char* hierName() const override final;
    const char* modelName() const override final;
    unsigned threads() const override final;
    /// Prepare for cloning the model at the process level (e.g. fork in Linux)
    /// Release necessary resources. Called before cloning.
    void prepareClone() const;
    /// Re-init after cloning the model at the process level (e.g. fork in Linux)
    /// Re-allocate necessary resources. Called after cloning.
    void atClone() const;
};

#endif  // guard
