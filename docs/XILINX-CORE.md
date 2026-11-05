# Host-backed Xilinx execution core

The execution core has now been synthesized independently for 7-series FPGAs
at the same capacity profile used by the official Wasm suite. Its identified
Verilator simulator now passes the complete 259-suite regression locally,
with exact native RTL results and command cycle counts. FPGA placement,
routing and physical-board operation remain unverified.

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

## Complete official corpus

The [completed campaign](verification/xc7-core-corpus-summary.json) uses sixteen
disjoint command partitions and eight simulator workers. It finished in
19,799 seconds. All 259 suites pass: 57,711 RTL execution assertions, 4,677
front-end validation assertions and 254 embedding assertions. Every one of
the 65,353 script commands agrees with native RTL. The 306,351,688 canonical
cycles exclude the duplicate setup replay needed by partitioned workers.

The [reconciliation check](verification/xc7-core-reconciliation.json) rechecks
both executable identities and 452 exact execution dependencies. All 28
deliberate identity and coverage defects are rejected. Changes to unrelated
ASIC tools during the campaign produced different broad workspace hashes;
the original hashes remain recorded, and no single workspace hash is invented.
The [archive](verification/xc7-core-corpus/index.json) includes all original
partition reports, logs, the native reference, both aggregate reports, model
manifests, generated sources and the supervising driver. Its 460 frozen
campaign inputs were checked again before publication.

The original conversion cache verified each WAST source and converter version
stamp, but did not hash every generated JSON and module payload before execution.
An [independent post-run replay](verification/spec-conversion.json) now verifies
the installed converter against its checksum-pinned release archive, regenerates
all 259 scripts into a separate directory and checks every command, expected
value and all 7,216 generated payloads against the unchanged cache. All thirteen
deliberate corruptions are rejected. Only the informational absolute source
directory prefix may differ; the pinned revision and suite suffix must match.
Both text and binary representations of invalid modules are included.
This establishes current input consistency; it does not retroactively create
a before-execution input attestation. The archived conversion inputs and
fresh JSON/logs are in `xc7-core-corpus/conversion-inputs.tar.gz`, with an
entry-by-entry SHA-256 manifest beside it. The standalone replay tool audits
an existing legacy `build/spec` cache, such as the cache preserved in that
archive. New runner versions use the isolated inputs described below:

```sh
python3 tools/check_spec_conversion.py
```

The supervising driver records commands and inputs, cleans up worker process
groups on failure, rechecks both executables and requires exact command
coverage and native cycle counts during final merging.
This core is an untimed host-backed simulation. Xilinx placement, routing,
timing, bitstream generation and physical-board testing remain unverified.

## Fresh inputs for new runs

`run_spec.py` now generates each script afresh in a unique directory for its
process. It verifies the installed `wasm-tools` bytes against the pinned release
archive and verifies every WAST against the pinned specification archive.
It never reuses another process's conversion cache. Repeated use within the
same process requires the original generated hashes to match.

Before and after each script executes, the runner checks the exact JSON,
every referenced text/binary payload, its source and its conversion-command
receipt. It checks the converter, complete official source inventory and all
generated inputs again before accepting the final report. The shared
`spectest` fixture must also match a fresh trusted conversion. Original
source-directory prefixes are retained in raw hashes; only the informational
prefix is normalized for comparisons between workers.

The CI planner and merger independently generate their own inputs and compare
each native and mapped suite's semantic JSON, source and payload identities.
Missing before/after checks or changed input identities prevent a complete
pass. Merged reports preserve every partition's input evidence. Separate CI
artifacts retain native, ECP5-worker and Xilinx-worker input directories without
changing the existing report artifact paths.

The [three-model regression](verification/spec-input-integrity.json) passes
eight suites per model: 6,647 RTL execution assertions, 355 validation
assertions and 132,959 canonical cycles each. Complete observations agree
with the prior native reference. Fifteen integrity tests include real pinned
conversions, stale-cache isolation, payload changes before/during execution,
binary representations of invalid modules and converter substitution. The
nineteen CI fixture tests include 24 native/mapped evidence corruptions.
Existing timeout, partition and reconciliation fixtures also pass.
The [archive](verification/spec-input-integrity/index.json) retains the three
reports, code, test logs and 2,093 actual input files. The complete native
corpus is being rerun with this stronger evidence; complete mapped reruns
with these new records have not yet passed.

## CI deployment

The workflow now builds this core independently of the bounded programmable
system. It waits for the full native reference, reruns the used primitive
checks, compiles one portable simulator and packages its executable and all
additional inputs. Sixteen workers restore that same package and run the
complete ownership plan. `Complete Xilinx mapped corpus` requires every
worker and exact command-by-command agreement with the native reference.
Failures retain partial results and build diagnostics. This new CI pipeline
has not completed on GitHub yet.

The [deployment preflight](verification/xc7-core-ci-preflight.json) restores the
package into another directory containing the required repository inputs and
pinned upstream tools/sources. The restored model verifies its identity,
passes the actual command-partition/setup-replay fixture and repeats all eight
smoke suites with identical observations. Packaging rejects the wrong FPGA
family. Actionlint 1.7.12 reports no workflow findings. These are local
deployment checks, separate from the completed local corpus and the pending
complete CI result.

`check_spec_reconciliation.py` now accepts the same explicit
`--mapped-backend mapped-xc7-functional` selection. It protects direct and
transitive inputs before removing stale output files. Five fixtures exercise
that protection, including actual command-line failures with preserved
canaries. The full-result reconciliation now passes against the completed
sixteen-partition campaign, including its 28 identity and coverage controls.
