# From the Wasm specification to an FPGA

WasMetal is one processor design represented and checked at several levels. The microarchitecture, RTL and SystemVerilog are closely related descriptions of that design; they are not three different processors.

| Term | Meaning in WasMetal |
|---|---|
| **ISA** | The instruction set architecture: the operations and observable behavior defined by WebAssembly. It specifies what a program means. |
| **Microarchitecture** | Our choices for how to execute that ISA: a stack machine, banked storage, shared arithmetic units, serialized SIMD, control states and memory interfaces. |
| **RTL** | Register-transfer-level description: what state is stored and how logic computes the next state between clock edges. This is a way of describing hardware. |
| **SystemVerilog** | The language used to write that RTL. It can also describe test benches and constructs that are not synthesizable hardware. |
| **RTL simulation** | A program evaluates our RTL's behavior as clocks and inputs change. Verilator generates and compiles this model from the SystemVerilog. |
| **Synthesis** | Yosys transforms the RTL into hardware building blocks. Technology mapping selects blocks available in the target FPGA. |
| **Netlist** | The resulting list of hardware instances, their settings and their connections. The ECP5 netlist contains lookup tables, carry logic, flip-flops, RAM and multipliers. |
| **Netlist simulation** | Simulation of those interconnected blocks, using models of the FPGA primitives. We also use Verilator for this stage. |
| **Placement and routing** | Tools assign blocks to locations in a particular FPGA and select physical routing resources connecting them. |
| **Bitstream** | Configuration data that programs an existing FPGA's logic, memory modes and routing. It does not manufacture a new chip. |
| **Physical hardware testing** | Load that configuration into an actual board, send programs and check results under real clocks, power supplies and interfaces. |

The microarchitecture is embodied in the SystemVerilog RTL. There is no required separate compilation step called “compile the microarchitecture into RTL”; implementing the microarchitecture is the design work we do when writing that RTL.

RTL describes both registers and memory accesses. WasMetal's value stack maps to FPGA block RAM; the RTL describes the control logic that selects entries to read and write on clock edges.

```mermaid
flowchart TD
    ISA["WebAssembly ISA: required behavior"] --> ARCH["Microarchitecture: our hardware organization"]
    ARCH --> RTL["SystemVerilog RTL: implementation"]
    RTL -->|Verilator| RSIM["Executable RTL simulation"]
    RTL -->|Yosys synthesis and mapping| NET["ECP5 netlist: blocks and connections"]
    NET -->|Primitive models and Verilator| NSIM["Executable netlist simulation"]
    TESTS["Official Wasm core tests"] --> RSIM
    TESTS --> NSIM
    NET --> BOARD["Board interface, placement and routing"]
    BOARD --> BIT["FPGA bitstream"]
    BIT --> HW["Physical board testing"]
```

## The two simulation models

Verilator translates a hardware description into C++ and builds an executable simulation. That executable represents signals, registers, memories and their changes over simulated clock cycles. It runs on the development computer.

The surrounding C++ adapter supplies clocks, instructions, metadata and backing storage. Wasm instruction results come from the simulated processor. The Python runner keeps expected results separately and compares them with the outputs. A Wasm software interpreter does not substitute results for the execution engine.

For RTL simulation, Verilator receives the original SystemVerilog modules. For netlist simulation, it receives the synthesized circuit and models of its FPGA building blocks. These are two simulation executables with the same CPU interface, not two separately designed CPUs.

Both use the same software loading/validation boundary. `wasm-tools` validates modules; Python decodes binaries and prepares their execution images. A core test-corpus pass includes separately counted execution, validation and embedding assertions. It does not mean all those responsibilities moved into RTL.

## Why simulate after synthesis

An addition in RTL becomes a network of logic and carry cells. An RTL memory array must map to FPGA RAM with the right clock edges, addressing and write masks. Synthesis also restructures and optimizes logic.

The original RTL can simulate correctly while a tool translation, primitive configuration, RAM inference or simulation model has a bug. Netlist simulation checks the translated representation against the same external program expectations.

The ECP5 simulator uses Yosys logic-cell models plus checked models for the emitted RAM and multiplier configurations. The [builder](../tools/build_gate_sim.py) rejects unknown primitive types or unsupported configurations and records exact inputs and executable hashes.

This is **functional** simulation. It checks values and clocked behavior, not analog electrical behavior or realistic routed wire delays. Static timing analysis separately checks whether signals can arrive before their required clock edges. Both rising and falling edges matter to WasMetal's RAM design.

Simulation speed is also different from hardware clock speed. A computer may take milliseconds to evaluate one cycle of the mapped circuit. The configured FPGA carries out its circuit's operations in parallel. A slow simulator does not establish a slow FPGA clock; the recorded timing constraints and physical measurements address that question.

## Why the previous reports said 259 and 40

The full original-RTL run completed all **259** pinned official core test files, with 57,711 execution assertions, 4,677 validation assertions and 254 embedding assertions. See the [recorded RTL run](verification/core-3.0-current.json).

The additional netlist regression selected **40** files and completed 17,379 execution assertions. Its report explicitly records `full_core_suite_passed: false`, because it is a subset. It uses the same core netlist as the default routed ULX3S bitstream. See the [recorded mapped run](verification/ecp5-abc9.json).

That record does not establish failures in the remaining files; it establishes that the full mapped regression was not completed. The mapped simulation evaluates a much more detailed circuit and can take substantially longer. The direct and reference tail-call suites alone account for over 210 million simulated cycles in the recorded RTL run; their official long-running cases must remain intact.

Expanded testing has now passed [249 official suites](verification/ecp5-expanded.json), with 48,604 execution assertions, 4,320 validation assertions, 254 embedding assertions and 3,038,303 cycles. Every per-suite count matches the original RTL run. Executable/source identity checks passed, and no failures, unsupported cases, conversion errors, blocked commands or runner errors were recorded.

The original slow full run was interrupted while faster simulator builds were checked. The full regression resumed on 2026-11-02. The [checkpoint](verification/mapped-regression-status.json) preserves 250 suites from completed prior reports. The current full run has completed 258 suites without reported errors; `return_call_ref.wast` remains. A final full result must identify all 259 suites, show zero errors and pass executable/source identity checks. No full mapped pass is claimed until that report exists.

## Running and observing the full mapped regression

For a freshly built model in the current workspace:

```sh
make fpga-core
python3 tools/build_gate_sim.py --core-netlist build/core-ecp5.json --fast-sim --fast-luts
python3 tools/run_spec.py \
  --simulator build/gate-model/obj/Vwasmetal_core \
  --wait-states 3 --jobs 4 --response-timeout 172800 \
  --schedule-from docs/verification/core-3.0-current.json \
  --progress-report reports/ecp5-full-20261102.progress.json \
  --report reports/ecp5-full-20261102.json
```

The optional `--fast-sim` builder flag uses Clang with `-O3 -march=native` for
the simulator executable. It changes neither the netlist nor the FPGA
bitstream. It requires Clang and targets the development computer's instruction
set, so rebuild the simulator when moving to a different host CPU. Compiler
identity and flags are recorded; a full build recompiles every object to avoid
silently reusing objects from different compiler settings. `--jobs` controls
compilation parallelism, and `--build-directory build/gate-fast` keeps an
experimental executable separate from an existing one.

`--fast-luts` expresses each lookup table as a direct lookup when its selectors
are known, retaining the original multiplexer expression whenever a selector is
X or Z. This changes the simulation representation of the primitive, not the
mapped circuit. Each build first proves binary equivalence for every possible
table and selector and runs four-state comparisons for the mapped table values.
A deliberately wrong primitive must fail the proof. See the
[primitive-check report](verification/ecp5-lut-model.json). These are local
primitive checks, separate from the inconclusive whole-CPU equivalence attempt.

Omitting `--suite` selects the entire official core tree. `--schedule-from` changes only execution order, using prior cycle counts to start long suites early. Each suite has its own simulator process and independent state.

`--response-timeout` sets the wall-clock deadline for a simulator response. The separate simulated-cycle budget is unchanged. Wall timeouts, cycle timeouts and unsupported instructions remain failures; they cannot satisfy an expected Wasm exhaustion assertion.

CI includes regression checks for timeout classification and for recompiling simulator objects when compiler flags change.

The progress file is replaced atomically when a suite finishes. It is a partial observation, never evidence of a full pass. The final report is authoritative and follows the end-of-run identity checks. `--verbose` additionally logs the script location before each command, identifying long invocations while they run.

An independent expanded run used the Clang-compiled executable under
`build/abc9-check/root/build/gate-speed`, preserving the verified model's build
environment. Its netlist is byte-identical to `build/core-ecp5.json`, and its RTL
and host-adapter inputs match the current project. The current runner was copied
into that snapshot before launch. It passed the same 249 suites using the
original primitive expressions, with every per-suite count identical to the
optimized lookup model; see the [independent report](verification/ecp5-compiler-only.json).
Local launch details for the interrupted full run
remain in `reports/ecp5-full-launch.json`. Historical synthesis/routing scripts
in the snapshot are not used to execute the simulation.

The equivalent lookup model under
`build/abc9-check/root/build/gate-lookup-clang` completed all 249 selected suites.
Its final report is committed as `docs/verification/ecp5-expanded.json`.
The production builder also completed a fresh `--fast-sim --fast-luts` executable
under `build/gate-fast-lut`. It passes the existing engine boundary and negative
checks, including wrong results, wrong traps, resource exhaustion and timeout
classification; see the [engine report](verification/ecp5-production-engine.json).
It also passed the original [40 official suites](verification/ecp5-production.json)
with exactly the same assertions and cycles as both the native RTL and the
historical mapped run. These overlapping runs do not add distinct suite coverage.
The separate [`call_indirect` run](verification/ecp5-call-indirect.json) also
passed, adding 134 execution assertions, 35 validation assertions and 3,269,242
cycles with exact agreement against the original RTL.

## Resumed full regression

The current mapped coverage is **250/259 distinct suite files**, comprising 48,738 execution assertions over 6,307,545 cycles. After the owner explicitly resumed work on 2026-11-02, a fresh full 259-suite run started on the production-built simulator. Four workers start the longest suites first. The previous results remain valid; the new run must finish and pass its identity checks before it establishes a full mapped pass.

The [partial snapshot](verification/ecp5-full-progress.json) now contains **258 completed suites**, 57,676 execution assertions, 4,664 validation assertions, 254 embedding assertions and 186,314,508 cycles. Every completed suite has exactly the native RTL counts and no reported errors. Only `return_call_ref.wast` remains. A live executable/source identity check passed at the checkpoint; the final end-of-run identity check is still required.

The final reference-tail-call suite accounts for 120,037,180 cycles in the native report, so the file count alone does not measure remaining runtime. The checkpoint combines disjoint final reports; overlapping independent and fresh-builder checks are counted only once. The full mapped regression remains unfinished.

The active command is:

```sh
python3 tools/run_spec.py --simulator build/gate-fast-lut/obj/Vwasmetal_core --wait-states 3 --jobs 4 --response-timeout 172800 --schedule-from docs/verification/core-3.0-current.json --verbose --progress-report reports/ecp5-full-20261102.progress.json --report reports/ecp5-full-20261102.json
```

If that build directory is unavailable, use the fresh-build instructions above. The runner checks source and executable identities before execution. The previous pause cancelled CI runs 41270306771 and 41269745152 and skipped CI for the checkpoint commit. CI run 41393251485 passed for the resume commit. The active local log is `reports/ecp5-full-20261102.log`.

## After a full netlist pass

A full netlist pass would establish that the synthesized functional model passes the same official corpus as the RTL model. It would not establish a mathematical proof for every possible program, a transistor-level simulation or a physical-board result.

WasMetal has a routed ULX3S bitstream with recorded timing checks. Physical programming, board bring-up and on-board tests remain separate milestones. An ASIC is another implementation target: synthesis and physical design use a chip process's cell and memory libraries, followed by manufacturing, packaging and silicon testing.
