# Host-backed Xilinx execution core

The execution core has now been synthesized independently for 7-series FPGAs
at the same capacity profile used by the official Wasm suite. Its identified
Verilator simulator passes an eight-suite smoke test. The complete 259-suite
regression is running; it has not passed the full corpus on this new circuit yet.

The [synthesis receipt](verification/xc7-core-estimate.json) and
[raw evidence](verification/xc7-core-initial/index.json) identify the circuit,
commands, source inputs and pinned synthesis tools. The structural checks pass
with 47,009 LUT1–LUT6 primitives, 5,265 flip-flops, 29 DSP48E1 blocks, 60 RAMB18E1
blocks and 19 RAMB36E1 blocks. The RAM total is equivalent to 49 36-Kbit blocks.
There are no distributed-RAM primitives in this core. Its 13 generic memories
contain 1,542,912 bits before technology mapping.

These are synthesis counts, not packed utilization, routed timing or a board
fit result. The top is `wasmetal_core`; the software harness provides the
existing memory/runtime services. The separate `wasmetal_loadable` circuit has
its own local storage, UART and program loader and passes the 35 integration
cases described in [system verification](XILINX-SYSTEM-SIMULATION.md).

## Capacity and mapping contract

The profile in `fpga/profile.json` specifies 8,192 value slots, 2,048 control
entries, 512 call entries, 256 memories and 1,048,576 heap slots. The bounded
board-system profile uses 1,024 heap slots. The host-backed heap-slot limit
does not mean that this core contains on-chip storage for that whole heap.

```sh
python3 tools/synth_xc7_core.py
```

The synthesis sequence uses the same corrected Xilinx RAM mapping as the
whole system. It checks the value-stack capacity before mapping, then checks
every top-level parameter, the complete external port contract, allowed cell
types and RAMB36E1 address-pin constants. Inputs are hashed before and after
synthesis. The new netlist SHA-256 is
`d1a75b8abd964755db4e63c6b8a0a5db3972971188dd58593ad8ec804247d120`.

## Verification setup

The LUT and flip-flop checkers now accept `--top wasmetal_core`. Their default
remains the complete programmable system. The DSP checker accepts an explicit
estimate/netlist pair and checks the distinct core inventory: ten direct
multipliers with `OPMODE=5` and one direct multiply/add cell with `OPMODE=53`.
The other three configuration counts match the whole system. All five modes
remain subject to the existing integer oracle and fault controls.

`spec_ci.py merge` and `pack` now require an explicit
`--mapped-backend mapped-xc7-functional` for Xilinx results. ECP5 remains the
default. The merger rejects missing, unreviewed or mixed backends and retains
its full command-ownership, executable-identity and exact native-cycle checks.
The updated 18-test fixture regression passes; those fixtures are metadata
checks rather than CPU execution evidence. Its log is in the initial archive.

## Simulator and initial execution

The [simulator report](verification/xc7-core-simulator.json) and its
[raw evidence archive](verification/xc7-core-simulator/index.json) preserve the
executable identities, component receipts, build logs, smoke results and nine
builder fault controls. The smoke run executes `i32`, `i64`, `f32`, `f64`,
`conversions`, `simd/simd_const`, `exceptions/throw_ref` and `gc/struct` with three
memory wait states. All 6,647 execution assertions and 355 validation assertions
pass. Its 7,326 script commands account for 132,959 canonical cycles; every
command agrees with the complete native reference.

The core's actual LUT tables pass 139,552 known-value and 9,188,056 four-state
observations per model, six symbolic binary LUT proofs and eleven fault
controls. All five DSP modes pass 87,040 arithmetic vectors per model, six
arithmetic faults and eight inventory faults. The core's flip-flop inventory,
carry chains and muxes pass the existing independent-oracle campaigns. The
unchanged fast RAM models reuse their verified source-bound proof. There is
no distributed RAM in this netlist. Component reports retain the documented
vendor/Yosys differences on X/Z values and the unverified vendor oracle for an
unknown asynchronous clear; this is not a claim of complete four-state vendor
equivalence.

To rebuild from a bootstrapped checkout:

```sh
make sim
python3 tools/check_xc7_memory_mapping.py
python3 tools/check_xc7_ram_models.py
python3 tools/synth_xc7_core.py
python3 tools/check_xc7_dsp.py --estimate reports/xc7-core-estimate.json --netlist build/xc7-core/mapped.json
python3 tools/check_xc7_luts.py --top wasmetal_core --netlist build/xc7-core/mapped.json --directory build/xc7-core-lut-check --report reports/xc7-core-luts.json
python3 tools/check_xc7_carry.py
python3 tools/check_xc7_muxes.py
python3 tools/check_xc7_flops.py --top wasmetal_core --netlist build/xc7-core/mapped.json
python3 tools/build_xc7_core_sim.py --jobs 2
```

The builder uses the unchanged official-suite C++ host through the existing
mapped-core adapter. It checks the exact circuit, capacities and primitive
evidence before generating a model. It binds the generated sources, compiler
identity, circuit and executable to the build manifest and rechecks inputs
when compilation finishes. The shared-reset warning exception is restricted
to the exact top-level reset signal after checking its six asynchronous
HardFloat consumers.

The ongoing full campaign uses sixteen disjoint command partitions, with
eight simulator workers. Its archived driver records commands and inputs,
cleans up worker process groups on failure, rechecks both executables and
requires exact command coverage and native cycle counts during final merging.
This core is an untimed host-backed simulation. Xilinx placement, routing,
timing, bitstream generation and physical-board testing remain unverified.
