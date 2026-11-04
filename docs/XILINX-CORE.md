# Host-backed Xilinx execution core

The execution core has now been synthesized independently for 7-series FPGAs
at the same capacity profile used by the official Wasm suite. Its complete
instruction-level regression is being prepared; it has not passed the official
corpus on this new circuit yet.

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

The mapped simulator and official-suite execution are the next steps. No
Xilinx conformance completion, physical board result or ASIC readiness follows
from this synthesis checkpoint.
