# WasMetal

A project to build a bare metal physical implementation of WebAssembly. That's right, a WebAssembly CPU. Inspired in part by [this amazing talk](https://www.destroyallsoftware.com/talks/the-birth-and-death-of-javascript).

WasMetal is being revived under [Millillion](https://github.com/Millillion) in 2026. It implements WebAssembly Core 3.0 instructions in a clocked SystemVerilog stack machine, with a software loading and validation front end.

Completed work lives on `main`. Temporary development branches are integrated into `main` and pushed before a task is finished; the README is reviewed with every commit. Main-branch verification runs finish before queued code changes are tested, so frequent commits do not cancel active regressions. Newer pushes can replace an older pending run.

## Current status

The CPU now implements integral floating-point rounding directly in the IEEE
encoding. All 259 official suites pass [without memory stalls](docs/verification/core-rounding-native-zero.json)
and [with three wait states](docs/verification/core-3.0-current.json), with
[every command cycle unchanged](docs/verification/fp-round-native-comparison.json).
The component proofs, complete format-interface proofs, 1,734,368 FPU
comparisons and all 35 programmable RTL cases pass.
[Fresh CPU synthesis](docs/verification/fp-round-synthesis.json) saves 399 LUT4
cells in the bounded profile and 559 in the host-backed profile, with unchanged
memory, register and DSP counts. The new mapped CPU passes
[5,352 execution assertions in four scalar/SIMD floating-point suites](docs/verification/fp-round-mapped-focused.json).
All five [compiled-C cases](docs/verification/c-workload-mapped.json) also pass
on the new RTL and mapped programmable system, with exact UART and cycle agreement.
Its [35-case programmable comparison](docs/verification/loadable-mapped.json)
also passes, with identical UART bytes, execution results and clock counts,
and all seven comparison fault controls rejected. The complete official
host-backed mapped corpus now [passes all 259 suites](docs/verification/core-rounding-mapped.json),
with all 65,353 commands and their cycle counts matching native RTL.
The [reconciliation check](docs/verification/core-rounding-reconciliation.json)
rechecks both executable identities and 288 execution/verification inputs,
preserves the differing workspace fingerprints caused by ongoing tool work,
and rejects all 26 deliberate identity and coverage defects. Original partition
reports and logs are [archived](docs/verification/core-rounding-mapped).
The complete system also passes a new
[four-state boot and upload campaign](docs/verification/loadable-four-state.json)
at production capacities. All 1,492,992 bits in the five writable program stores
and backing RAM begin unknown. Two uploaded programs, an interrupted upload,
warm-reset memory clearing and ROM boot pass, with exact native UART results
and invocation cycle counts. Both deliberate mutations are rejected;
CI is configured to require this check for programmable-system completion.
The [CPU logic-mapping comparison](docs/DESIGN-FLOW.md#comparing-complete-cpu-logic-cones)
now [passes all 28,506 original boundary bits](docs/verification/core-mapping-cones.json)
for the host-backed core profile. The original engine proves 27,098 bits;
classic CEC proves the remaining 1,408. Every cone retains its original logic
and inputs, with no additional internal logic assumptions. The completed
receipt and all saved solver results were rechecked. Both inverted-output
controls fail as required. This compares two technology mappings around
matching registers, RAM and DSP blocks; their internals, physical timing and
the common RTL synthesis front end are outside the proof. The two
[driver](docs/verification/core-mapping-driver.json)
[fixtures](docs/verification/core-classic-driver.json) also reject 17 and 15
checkpoint/input defects, respectively; CI repeats those fixtures.
Fresh proofs pass for the programmable
[board wrapper](docs/verification/loadable-mapping-proof.json) and
[simulation wrapper](docs/verification/loadable-simulation-mapping-proof.json),
covering 15,976 and 15,892 boundary bits respectively. Both reject an inverted
output; their CPU and stored-state outputs are shared arbitrary inputs, so
these are wrapper proofs. The new board design has placed; routing remains incomplete.
The [placement analysis](docs/PLACEMENT.md) records 61,344 logic cells and
identifies a reset net driving 4,783 pins across most of the device. The isolated
[reset-distribution experiment](docs/verification/reset-replication.json) preserves
the circuit's logic with 31 extra LUTs, limits each copy to 150 sinks and rejects
five deliberate defects. Its completed placement has a
[7.1% lower placer wire-length cost](docs/verification/reset-placement-comparison.json),
with unchanged register, RAM and DSP counts. Its router2 trial was
[retired incomplete](docs/verification/reset-replication-router2-retired.json)
after five worsening iterations; its best result still had 23,415 conflicting
wires. Saved placement settings initially overrode the command-line router
choice. The [corrected trial](docs/verification/reset-router1-preflight.json)
changes only that setting, checks every other placement value and confirms
router1 in its log. It [reached its two-hour limit without completing](docs/verification/reset-replication-router1-timeout.json);
all inputs were rechecked afterward, and no routed design or bitstream was
produced. Both router trials remain incomplete. CI repeats
[13 corruption controls](docs/verification/routing-placement-driver.json).
A real
[timeout control](docs/verification/reset-routing-timeout.json) verifies that
an interrupted attempt retains an incomplete receipt and emits no bitstream.
The physical benefit remains unproven. The baseline route was
[retired after worsening congestion](docs/verification/rounding-routing-retirement.json).
Other whole-system integration and routed-bitstream records below retain their
earlier source identities until their replacements are verified. **No physical board
has been tested.**

The preceding SIMD-selector revision [passed the entire mapped corpus in CI](docs/verification/ci-selector-complete.json),
all 35 programmable mapped cases and all five compiled C cases. Its
[all-input selector proof](docs/verification/simd-fp-selection.json) and
[measured synthesis savings](docs/verification/simd-selector-synthesis.json)
remain documented. Two older programmable routing trials were
[retired with unresolved, increasing congestion](docs/verification/selector-routing-retirement.json).
Their iteration records are preserved; neither produced a completed bitstream.
A standalone board build [hit its three-hour CI limit](https://github.com/Millillion/wasmetal/actions/runs/41770401814/job/126379123153)
during physical implementation, which also skipped dependent system checks.
CI now separates mapped simulation from standalone placement/routing so those
functional checks can finish independently. Both remain required.

- **Standalone boot:** prepared images execute using local instruction, function, type and backing memory, with autonomous initialization and UART results. [29 RTL cases](docs/verification/standalone-rtl.json) and [nine board-clock cases](docs/verification/standalone-board-rtl.json) passed. The [complete synthesized system](docs/verification/standalone-mapped.json) matches every UART byte and completion clock across four boot/reset scenarios. The production memory controller passes [4,837 oracle-checked transactions in both models](docs/verification/standalone-memory-mapped.json), with separately checked [four-state RAM models](docs/verification/standalone-ram-model.json). The [routed ULX3S bitstream](docs/verification/standalone-routing.json) uses 63,656/83,640 logic cells and 171/208 block RAMs, meets its 781.25 kHz clock and passes unpack/repack verification. These are bounded integration tests, separate from the full host-backed corpus below. **No physical board has been tested.** See the [standalone guide](docs/STANDALONE.md).
- **Conformance:** the direct-rounding RTL passes all 259 pinned official suites with zero and three memory wait states: 57,711 RTL execution assertions, 4,677 validation assertions and 254 embedding assertions in each run, with zero failures or unsupported cases. The [stalled result](docs/verification/core-3.0-current.json) identifies the sources, simulator and capacities and completes 306,351,688 cycles. [Both runs preserve every command cycle](docs/verification/fp-round-native-comparison.json) from the preceding revision. New CI verification remains to finish.
- **Floating point:** arithmetic shares one raw datapath and rounds directly to either precision. [1,734,368 additional comparisons](docs/verification/floating-point.json) cover arithmetic, conversions, traps and reset interruption, with separate negative controls.
- **Storage:** the native and FPGA defaults both use 8,192 value slots, 2,048 labels, 512 call frames, 256 descriptors per class and 1,048,576 external heap slots. Generated host and FPGA interface headers advertise the matching capacities and build identity. These remain finite resource limits.
- **Mapped conformance:** the current direct-rounding CPU passes **all 259 pinned official suites** locally on the ABC9 ECP5 mapping with three memory wait states. The [full result](docs/verification/core-rounding-mapped.json) records 57,711 execution assertions, 4,677 validation assertions and 254 embedding assertions, with zero failures or unsupported cases. Every suite's counts and every command's canonical cycle count match native RTL. All sixteen partitions and the final coverage check passed; [executable and dependency reconciliation](docs/verification/core-rounding-reconciliation.json) verifies the differing workspace snapshots without changing any original report. The preceding SIMD-selector revision also [passed in CI](docs/verification/ci-selector-complete.json), with identical local/CI netlists after relocating workspace paths. Optional `--fast-sim --fast-luts` builds preserve the circuit; the lookup models pass [binary equivalence and 287,232 four-state checks](docs/verification/ecp5-lut-model.json). See the [verification flow](docs/DESIGN-FLOW.md). Whole-circuit formal equivalence remains [inconclusive](docs/verification/mapping-equivalence.json).
- **FPGA:** the preceding configuration passed fourteen whole-board UART checks in simulation; see the [interface report](docs/verification/fpga-uart.json). The [last verified host-backed bitstream](docs/verification/fpga-routing.json), before the selector change, uses 58,892 of 83,640 logic cells (70.4%), with the core meeting 1 MHz at a reported 3.24 MHz maximum. Its rebuild reproduced the bitstream exactly and passed its unpack/repack check. **No physical board has been tested.**

See the [RTL architecture](docs/RTL.md) and [FPGA guide](docs/FPGA.md) for the execution boundary and reproducible verification commands. The host-backed conformance system supplies the instruction image, metadata and backing memory from the computer. The standalone prototype supplies these locally for bounded prepared images. Programmable prepared-image loading passes RTL and mapped integration checks; its FPGA routing remains incomplete. External RAM and reclaiming garbage collection remain future work.

For an explanation of the ISA, microarchitecture, SystemVerilog RTL, the two simulation models, synthesis and the FPGA bitstream, read [From the Wasm specification to an FPGA](docs/DESIGN-FLOW.md).

The [FPGA purchase research](docs/FPGA-SELECTION.md) compares development boards,
tools, community support and US home-use compliance. Genesys 2 remains the
technical recommendation, conditional on supplier clarification of its
regulatory basis for home R&D; ZCU104 is the leading alternative with an Arm
host. The corrected [complete-system Xilinx estimate](docs/research/xc7-system-estimate.json)
counts 50,964 logic LUT primitives, 6,951 flip-flops, 29 DSPs and 96 equivalent
36-Kbit RAM blocks, before board clock/reset and DDR integration. Logic LUTs
occupy about 25.0% of Genesys 2's LUT-site capacity, excluding distributed RAM.

New [vendor-model memory checks](docs/XILINX-MEMORY.md) exposed a real 72-bit
RAM mapping defect in pinned Yosys 0.33. An isolated correction passes 26,028
operations per model across five RAM configurations; all six negative controls,
including the original faulty mapping, are rejected. CI now runs this check
before the resource estimate. A separate address-pin audit also passes and
rejects 18 structural mutations. The corrected complete-system synthesis passes
structural checks and checks all 340 unused address-pin constants across its
28 RAMB36E1 cells. Earlier estimates remain historical size evidence with a known
functional mapping defect. The new [fast RAM models](docs/verification/xc7-ram-models.json)
pass those same 26,028 operations in both Icarus and Verilator, plus 25,414
four-state operations compared with generic RTL and the unmodified vendor
models. All 14 additional controls reject faulty configurations, erased unknown
data, collisions and incomplete test input. CI repeats these component checks.
The [DSP arithmetic checks](docs/XILINX-DSP.md) cover all 29 mapped multiplier
blocks: 87,040 vectors per model across five configurations agree with an
independent signed-integer oracle, using both original Xilinx and Yosys models.
Six arithmetic faults and eight unreviewed configuration/output changes are
rejected. CI now runs this check after synthesis.
An explicit-bit form of the DSP carry bus also passes the same oracle in both
Icarus and Verilator; it removes an artificial scheduling loop when compiling
the complete mapped circuit.
The [LUT model checks](docs/XILINX-LOGIC.md) prove the lookup optimization for
every binary truth table and selector at widths one through six. Independent
oracle regressions pass 183,664 known-input cases per model in Icarus and
Verilator, plus 11,811,032 four-state cases per model in Icarus. All eleven
fault controls are rejected. CI repeats the proofs and the mapped-table
regression; the proven models also support the complete-system runs below.
The [carry-chain checks](docs/XILINX-LOGIC.md#carry-chains) prove binary
equivalence with Xilinx, pass every binary input and 11,264 C++-driven input
transitions, and reject eleven faults. Each model also passes its independent
oracle for all 1,048,576 four-state input combinations. Their X/Z behavior
differs on 415,001 combinations; this is explicitly recorded, and no
four-state vendor-equivalence claim is made. CI repeats these checks.
The remaining mux/inverter logic now has binary equivalence proofs and
complete four-state tables. All four used flip-flop types pass independent
startup and state-transition checks in Icarus and Verilator. Their
[unknown-state limits and vendor reset diagnostic](docs/XILINX-STATE.md)
are explicit; CI repeats the component checks.
The [distributed-RAM model](docs/XILINX-LUTRAM.md) also passes a binary proof
of its 256 state bits and four outputs, with checked initial state and an
explicit write-enable specialization. Independent binary/four-state memory
oracles and twenty local fault controls pass for the configuration used by
all 22 mapped instances. CI repeats the checks for both UART profiles.
The [complete Xilinx CPU simulation](docs/XILINX-SYSTEM-SIMULATION.md) now
passes all **35 programmable integration cases** with accelerated UART timing,
matching the native RTL's complete case observations, UART bytes and clock
counts exactly. All fifteen comparison faults are rejected. Two smoke cases
also pass with the original LUT models. The native reference at 81 clocks per
UART bit passes all 35 cases. A [mapped upload at that unchanged timing](docs/verification/xc7-board-rate.json)
also passes: 45,114,201 core clocks, exact UART/commit/result timing agreement,
and the expected result of 42 in 53 execution cycles. All six comparison faults
are rejected. Xilinx placement and timing remain unverified.
CI is now configured to build the native reference and accelerated Xilinx
circuit, run all 35 cases through a supervised four-worker campaign, and
require the full comparison. The new complete CI job has not finished on
GitHub yet; the published passing campaign is local evidence.
A separate [host-backed Xilinx core](docs/XILINX-CORE.md) now passes synthesis
and structural checks at the official-suite capacities: 47,009 logic LUT
primitives, 5,265 flip-flops, 29 DSPs and 49 equivalent 36-Kbit RAM blocks.
Its [identified simulator and eight-suite smoke test](docs/verification/xc7-core-simulator.json)
pass 6,647 execution assertions and 355 validation assertions. All 132,959
canonical cycles match native RTL, command by command. Nine deliberately
corrupted build inputs are rejected before model generation. The complete
259-suite Xilinx campaign is running; it has not passed yet. The family-specific
report guards pass 18 metadata fixture tests. CI now includes a separate
Xilinx core build, sixteen official-corpus workers and a complete-coverage
gate. Its [local deployment checks](docs/verification/xc7-core-ci-preflight.json)
restore the package in another directory and pass the same eight suites and
the actual command-partition fixture. Five output-protection fixtures pass.
The new full Xilinx CI pipeline has not finished yet.
ULX3S 85F remains the implemented board target, with routing
still incomplete; no board has been purchased or physically tested by this work.
The latest archived [standalone routing attempt](docs/verification/ci-standalone-routing-41846026922.json)
was cancelled after about three hours. Its best 1,705 conflicting wires grew
to 25,771 before cancellation; no routed timing or bitstream result follows.
A separate two-hour trial now uses nextpnr's alternative congestion weights on
the verified programmable placement. Its [preflight checks](docs/verification/routing-alternate.json)
pass, including native settings import/export, 21 rejected defects and an
actual timeout control. The routing outcome is pending.

## GUI Microarchitecture Simulator

The [historical demo](https://wasm-metal-demo.netlify.com) uses the original hosting address; its availability has not been verified for the revival.

```bash
git clone https://github.com/Millillion/wasmetal.git
cd wasmetal
npm install
npm start
```

Go to [http://localhost:5000](http://localhost:5000) in your web browser.

## Work before the FPGA arrives

The [active engineering sequence](docs/PRE-FPGA.md) covers wider memory,
program upload, external-memory verification and ASIC preparation. The new
[memory interface](docs/MEMORY.md) has passed
[13,327 independently checked transactions](docs/verification/memory-bridge.json)
under stalls and faults. Its byte-lane alignment has an
[exhaustive symbolic proof](docs/verification/memory-lanes-proof.json), and its
[bus safety invariants](docs/verification/memory-bridge-proof.json) have an
unbounded induction proof for the tested small and production configurations.
The 128 KiB masked RAM backend passes
[36,432 transactions](docs/verification/masked-bram-mapped.json) in both RTL and
mapped simulation with identical cycle counts. Run these checks with
`make memory-test`; CI runs them in a dedicated job.
The wider memory is integrated into the standalone RTL and mapped model.
[Measured execution cycles](docs/verification/standalone-performance.json) drop
from 73 to 39 for unaligned SIMD and from 73 to 31 for struct allocation/cast;
arithmetic-only examples retain their cycle counts. The 128 KiB startup clear
takes 32,768 core cycles, down from 131,072. The complete system passes mapped comparison and routing at the same clock.
The current standalone uses about 4,000 more logic cells than the earlier
byte-wide prototype, with block-RAM use unchanged.

The [external-memory AXI4 adapter](docs/AXI.md) separately passes
[21,732 transactions in RTL and mapped simulation](docs/verification/axi-mapped.json)
and an [inductive protocol safety proof](docs/verification/axi-proof.json).
Run `make axi-test`. The [clock-crossing link](docs/CDC.md) passes
[7,290 transfers across seven clock configurations](docs/verification/cdc-mapped.json),
including stopped clocks and 294 resets. Its
[initialization and stall safety proof](docs/verification/cdc-proof.json) is
unbounded; its [structural and four-state checks](docs/verification/cdc-structure.json)
also pass. The assembled asynchronous AXI path passes
[43,464 transactions in each model](docs/verification/async-axi-mapped.json),
with faster and slower memory clocks. Run `make cdc-test`.
The new [complete-CPU AXI integration test](docs/AXI.md#complete-cpu-integration)
connects these components to the active memory path in a separate simulation,
using a behavioral RAM slave. All 35 system cases pass with the AXI clock at
[one-half](docs/verification/axi-system-1-1.json) and
[one-sixth](docs/verification/axi-system-3-5.json) the CPU frequency, with
different response delays, independent channel stalls and retained memory
across resets. [Corrupted reads](docs/verification/axi-system-1-1-negative.json)
fail the independent result oracle. Both configurations and that negative
control [also pass in CI](docs/verification/ci-axi-system.json), with downloaded
observations and bus counters matching the local runs. The default FPGA system
still uses block RAM; DDR controller
integration, physical clock-crossing constraints and controller startup remain.

A separate [SDR SDRAM backend](docs/SDRAM.md) now implements startup, refresh,
masked eight-word bursts and warm reset without interrupting accepted device
operations. Its six-profile native/mapped campaign and expanded formal proofs
are separate from the complete CPU tests. The
[component campaign](docs/verification/sdram-mapped.json) passes 836,574
requests and 774 warm resets in each model, with matching observations and
cycles, all 65,536 write masks per profile and six rejected fault injections
per model/profile. Another [366 four-state checks](docs/verification/sdram-four-state.json)
pass with three rejected controller mutations. An
[unbounded protocol safety proof](docs/verification/sdram-proof.json) now passes
all six configurations and rejects seven controller mutations. The complete
CPU also passes all 35 integration cases through a behavioral SDRAM device
with [25 MHz timing](docs/verification/sdram-system-25mhz-5000.json) and
[100 MHz timing plus a long startup delay](docs/verification/sdram-system-100mhz-5000000.json).
The latter holds off memory requests for 12,178,089 startup cycles across the
campaign. [Corrupted reads](docs/verification/sdram-system-25mhz-5000-read-corruption.json)
and [bypassed startup gating](docs/verification/sdram-system-100mhz-5000000-startup-bypass.json)
are rejected independently. Compiled C also passes all five CRC-32 cases with
[25 MHz timing](docs/verification/sdram-c-25mhz.json) and
[100 MHz timing and delayed startup](docs/verification/sdram-c-100mhz-5000000.json),
each exercising 1,281 SDRAM reads and 42,246 writes. A dedicated workflow repeats
the component, formal, complete-CPU and compiled C checks. Those four earlier jobs
[passed in CI](docs/verification/ci-sdram.json); the downloaded device observations,
UART results and cycle counts match the local campaigns. These are simulation timing profiles, not
measured FPGA clock rates. The board PHY and physical implementation remain;
Genesys 2 requires DDR3. The default FPGA memory backend remains block RAM.

The [separately clocked SDRAM integration](docs/SDRAM.md#complete-cpu-with-separate-clocks)
now passes all 35 cases with memory clocks
[faster](docs/verification/sdram-async-faster-25mhz-5000.json) and
[slower](docs/verification/sdram-async-slower-100mhz-2000000.json) than the CPU.
The delayed-startup run records 3,981,937 CPU clocks of startup waiting.
Wrong clock binding, bypassed startup permission and corrupted reads are
rejected. The [clock scheduler](docs/verification/sdram-clock-driver.json)
matches independent event sequences and rejects six mutations. CI is configured
to repeat these campaigns. These checks exercise the assembled RTL and a
behavioral SDRAM device; physical clock generation, CDC constraints and the
board PHY remain.

The [CDC/SDRAM reset campaign](docs/verification/cdc-sdram-mapped.json) adds
1,260 resets and 4,704 completed transactions per model, with identical RTL and
mapped observations. It interrupts reads and writes at 15 observed points
across seven clock schedules and two timing profiles. Checks cover cancellation
before acceptance, every burst beat, immediate replacement requests, retained
masked-write data and refresh during reset. Corrupt reads, ignored masks,
missing refresh and incorrect cold-reset wiring are rejected. See the
[reset contract and campaign](docs/SDRAM.md#reset-across-the-clock-crossing).

The [prepared-image upload protocol](docs/PROGRAM-UPLOAD.md) now has an RTL
receiver and Python encoder. The production layout test checks
[80,537 store writes in each model](docs/verification/image-loader-mapped.json),
plus a complete Python-encoded image. Uploads with a bad checksum or incomplete
payload cannot authorize execution; [four-state tests](docs/verification/image-loader-four-state.json)
also reject an unknown payload. An [unbounded safety proof](docs/verification/image-loader-proof.json)
checks store bounds, initialization and the conditions for execution permission.
Run `make image-loader-test`.
The [host uploader](tools/upload_program.py) handles the ready/commit exchange,
serial deadlines and execution results, including replies arriving together.
Its serial-device tests pass. The programmable system now connects UART loading
to writable instruction and metadata stores and the complete CPU.
[All 35 native integration checks](docs/verification/loadable-rtl.json) and
[all 35 checks on the preceding ABC9 mapped circuit](docs/verification/loadable-mapped.json) pass,
including program replacement, rejection, timeout, UART break, rate variation
and reset recovery. [Two complete board-clock uploads](docs/verification/loadable-board-rtl.json)
and [three board-clock sender rates](docs/verification/loadable-board-rates.json)
also pass, including the expected 9600-baud setting. A
[mapped I/O audit](docs/verification/loadable-io.json) checks the UART/reset
synchronizers and free-running clock, with eight rejected circuit mutations.
Core-level integration uses a faster test UART; board tests retain the actual
divider and serial timing. Every mapped UART byte, result and clock count
matches RTL in that completed comparison. The preceding ABC9 wrapper mapping
[reduces placement from 66,251 to 62,958 logic cells](docs/verification/loadable-synthesis.json),
out of 83,640, with the same CPU circuit, all storage capacities and 192/208
block RAMs. It explicitly preserves the audited reset synchronizer. With
identical stored state and CPU outputs, an
[independent binary-equivalence proof](docs/verification/loadable-mapping-proof.json)
passes for 15,976 boundary bits and rejects a deliberately inverted output.
The [accelerated simulation mapping](docs/verification/loadable-simulation-mapping-proof.json)
passes for 15,892 boundary bits. Both proofs have been rerun for the current
direct-rounding build; CI requires both comparisons before the programmable execution
shards, independently of the long physical-routing job.
The [completed CI run at b79b0db](docs/verification/ci-programmable.json)
passed the complete 259-suite corpus in both native configurations and the
mapped core, plus all six programmable integration shards and five compiled C
cases. An independent check of the downloaded artifacts confirms
[all 35 programmable cases match RTL](docs/verification/ci-programmable-mapped.json),
including UART bytes and cycle counts. The workflow as a whole did **not** pass:
programmable routing hit its 350-minute job limit, and the final integration
gate failed. CI now writes separate JSON reports for the board and accelerated
mapping proofs; previously the later invocation replaced the earlier report,
although both proof logs were retained.
Programmable FPGA routing remains unresolved. The current
[routing experiment snapshot](docs/verification/loadable-routing-status.json)
records ABC9 placement/routing strategies and an isolated deeper-RAM experiment,
with unchanged capacities. All four recorded trials were stopped after
prolonged unresolved congestion. Earlier attempts are retained in Git history.
The new [instruction codec](soc/loader/wasmetal_instruction_encode.sv)
has an [all-input binary proof](docs/verification/instruction-codec-proof.json):
it stores suitable 288-bit expanded rows in 194 bits, retains the full 32-bit
opcode and flags any row that would lose information. Four operand layouts
cover different combinations of indices and wide immediates without relying
on opcode-specific assumptions. Run `python3 tools/prove_instruction_codec.py`;
CI also requires the proof and its corrupted-opcode negative control.
The [complete corpus audit](docs/verification/instruction-codec-corpus.json)
passes all 259 official suites with the RTL codec interposed on the host-backed
CPU's instruction inputs. It also checks every loaded row, including unreachable
instructions: 81,201 rows and 501 distinct opcode values, with every assertion
count and command cycle count matching the native reference. This does not test
local instruction RAM. The portable builder reproduces the validated HDL and
adapter sources byte for byte; its rebuilt simulator passes a separate smoke
check. A dedicated CI job now repeats the complete comparison and preserves
per-process coverage. Reproduce it with
`python3 tools/build_instruction_codec_sim.py`, then
`python3 tools/check_instruction_corpus.py --reference reports/core-stalled.json`
using a complete native report from the same source revision.
The [isolated local-memory experiment](docs/research/instruction-storage-experiment.json)
reduces block RAM from 192 to 187 but increases placed logic from 62,958 to
63,769 cells. Its routing trial was stopped after persistent congestion; it
produced no routed circuit or bitstream. All 35 native integration checks,
five compiled C cases in both models, wide-offset SIMD cases and explicit
unencodable-row rejection/recovery checks pass.
[All 35 mapped integration cases](docs/verification/storage-experiment-loadable-mapped.json)
also pass with identical UART bytes, results and clocks. The patch and evidence are
preserved, but the production image store remains 288 bits wide.
No programmable bitstream has
passed routing and timing checks yet. Routing and mapped
execution have separate CI jobs, and both must pass the final integration check.
The programmable CI build exposed a command error: the board-clock check was
given the core-clock simulator. `make loadable-test` now selects the board
simulator explicitly. The complete target now passes locally: all 35 core-clock
cases, both board-clock uploads, all three sender rates, the nine host tests
and acceptance-campaign preparation.
The original ROM system has been reverified,
including its mapped comparisons and fresh routing/bitstream checks.

The [board acceptance runner](docs/BOARD-ACCEPTANCE.md) prepares 25 programs
whose upload packets match the native simulation reference, then checks results
and execution cycles over serial with repeatable program replacement and
partial failure reports. Its nine host tests pass, including 50 uploads through
a pseudo-terminal. The physical-board campaign remains to be run.

A [freestanding C example](examples/c/README.md) now compiles through Clang to
Wasm and uploads through the same prepared-image path. All five CRC-32 cases
[pass in both RTL and mapped simulation](docs/verification/c-workload-mapped.json),
on the preceding ABC9 wrapper. They match independent
Python results with identical UART output and cycle counts.
The compiler-generated workload is also a required CI integration job.

The [integral floating-point rounding circuit](docs/ROUNDING.md) now replaces
two conversions with direct IEEE-field operations in both FPU formats. Its
[component checks](docs/verification/fp-round-experiment.json) prove both
precisions for every binary input, prove the actual ECP5 mappings, and pass
173,852 independent oracle vectors in both models, including 100,124 X/Z
cases. Ten deliberate defects are rejected. The isolated mappings use 1,113
LUT4 cells instead of 5,017. The [integration proof](docs/verification/fp-format-proof.json)
also covers every format-unit output for every binary input and all 64
operation encodings; it rejects incorrect mode wiring in both precisions.
Both complete native CPU runs and all 35 programmable RTL cases pass.
The complete mapped checks and physical implementation are underway;
new physical timing measurements remain to be established.

[Reproducible workloads](docs/BENCHMARKS.md) now measure CRC-32 and scalar/SIMD
integer dot products, with independently calculated results and repeated resets.
For 1,024 multiply-accumulates, SIMD takes 21,524 invocation cycles versus
49,596 for scalar code. These are [simulation measurements](docs/verification/benchmarks.json),
excluding upload, initialization and UART output; no physical performance is claimed.

The [ASIC preparation audit](docs/ASIC.md) retains 82 logical memories containing
3,035,968 bits and identifies the memory-port, clock-edge and boot requirements
for a silicon implementation. This is technology-neutral elaboration; it is
not standard-cell mapping, SRAM-macro integration or physical signoff.
The [programmable audit](docs/verification/asic-loadable-audit.json) additionally
checks all five writable program stores: 444,416 bits with no preset contents,
loaded before execution. That system retains the same memory capacity and
uses 7,125 generic register bits; it still needs real SRAM macros and physical
clock, reset and test implementations.
The programmable audit has also been repeated for direct rounding, with all
memory and register counts preserved. The ROM audit retains its selector-revision
record. A failed audit removes
its previous output report, preventing stale success from appearing current.
The separate [synchronous SRAM adapter](docs/SRAM.md) now passes
[719,924 transactions per model](docs/verification/sram-mapped.json), including
every byte mask, five capacity/latency configurations and 90 resets. Its
[unbounded protocol proof](docs/verification/sram-proof.json) and
[four-state checks](docs/verification/sram-four-state.json) also pass. It defines
a concrete interface for a future macro wrapper; it is not connected to the
default FPGA memory path and does not supply a foundry SRAM or physical timing
signoff. A separate complete-CPU simulation binds this adapter to a behavioral
SRAM with nonzero initial contents. All 35 system cases pass at
[one-cycle](docs/verification/asic-sram-system-1.json) and
[three-cycle](docs/verification/asic-sram-system-3.json) read latencies; deliberately
corrupted reads fail the independent result check. This full-system SRAM test
also runs in CI.

## RTL Microarchitecture Simulator

The clocked SystemVerilog core runs in Verilator. The test harness converts the
pinned official Wasm core test suite and compares its expectations with RTL
execution results and traps. Unsupported cases fail the run.

Pushes containing only documentation or recorded verification outputs do not
start a new hardware workflow, so publishing evidence does not cancel running
source verification. The performance-reference fixtures in
`docs/verification/standalone-ci/` remain CI inputs and still trigger checks.
Code, build-tool and workflow changes also trigger CI; pull requests and manual
runs remain unfiltered.

CI runs the complete suite with zero and three memory wait states, then checks
the serial FPGA interface. The workflow now also synthesizes the ECP5 CPU and
runs the complete official corpus against its Verilator circuit model across
16 CI jobs. Each official command is assigned to exactly one partition;
required module setup is repeated and recorded separately. A final check
compares every suite's counts and command cycles with the original RTL run.
The [complete CI run](https://github.com/Millillion/wasmetal/actions/runs/41470404770)
passed all sixteen partitions and the final coverage and native-agreement check.
Partition/replay accounting is additionally checked on both actual simulator
executables using a short synthetic script with globals, tables, calls and a trap. A
[complete native rehearsal of all 16 partitions](docs/verification/ci-partitions.json)
matches the intact run for all 65,353 commands, every command's cycle count and
every suite's assertion totals. The mapped acceptance check also rejects native
simulator reports, even when their results match.

Separate standalone CI jobs verify the local-memory and UART integration,
compare the mapped circuit with board RTL, and place/route the complete
autonomous system. The final standalone check requires both functional
verification and physical implementation to pass. It retains `standalone-verification`
and `standalone-fpga` artifacts for 30 days. The first
[clean CI job passed](https://github.com/Millillion/wasmetal/actions/runs/41572176563/job/125707382260),
reproducing every local case's UART bytes and completion clocks and the exact
FPGA bitstream from that earlier build. The [CI receipt](docs/verification/standalone-ci.json)
preserves the downloaded reports, artifact hashes and source checks.
Its mapped integration checks use
the comprehensive prepared self-test; they do not run all official suites on
the standalone system's bounded local RAM.

JSON results are retained for 30 days as `verification-reports`,
`mapped-results-*` and `mapped-complete` artifacts. Partial reports remain
available after failures and cannot establish a full pass. See the
[CI verification details](docs/DESIGN-FLOW.md#what-ci-runs).

```sh
python3 tools/bootstrap.py
make lint
make test-fpu
make test-all
```

See [docs/RTL.md](docs/RTL.md). The WebAssembly specification and its official
tests define the compatibility target.

## Loading Microarchitecture Implementation to FPGA

A host-backed ULX3S 85F reference system includes a UART loader/step interface,
board constraints, synthesis, placement/routing and bitstream build tools. The
whole serial interface and CPU are tested together in simulation. The standard
build has completed routing and timing closure, and produces the verified
bitstream at `build/ulx3s/wasmetal.bit`. See the [FPGA guide](docs/FPGA.md) for the build flow
and the remaining physical-board checks.

For autonomous execution, `make standalone-bitstream` instead builds
`build/standalone-ulx3s/wasmetal.bit`, including the prepared self-test image.
`make standalone-mapped-test` runs its complete verification flow. The
[standalone guide](docs/STANDALONE.md) describes image limits and UART decoding.

## Hardware roadmap

- [x] Implement Core 3.0 instruction execution in clocked SystemVerilog.
- [x] Pass the complete official core suite in RTL simulation.
- [x] Verify a host-backed FPGA board interface in simulation.
- [x] Complete FPGA placement, routing and timing closure for the host-backed reference system.
- [ ] Load and verify the design on a physical ULX3S 85F.
- [x] Simulate local instruction/data memory and autonomous prepared-image execution.
- [x] Simulate the complete standalone mapped circuit and complete FPGA routing and timing checks.
- [ ] Verify autonomous execution on a physical FPGA.
- [ ] Add buffered program loading and external memory.
- [ ] Select an ASIC process and integrate suitable memories, I/O, clocks, reset and manufacturing test support.
- [ ] Complete physical design and signoff, fabricate a prototype, then package and test the silicon.

The standalone prototype boots a prepared image from local FPGA memory and
reports results over UART without host instruction or memory service. Image
preparation and validation run on the development computer. RTL simulation,
mapped simulation and standalone routing have passed; physical-board checks
remain. See the [standalone guide](docs/STANDALONE.md).

## Why is this a good idea?

* [Maybe it's not](https://twitter.com/lastmjs/status/928682791511789568), but who cares
* The world is moving to WebAssembly
* Some of the biggest and potentially most world-changing projects are implementing their virtual machines as WebAssembly virtual machines (DFINITY, Ethereum)
* The bytecode is being designed as a compilation target for low-level languages first
* The bytecode is meant to execute at near-native speeds on a variety of underlying ISAs
* Java processors already offer potential benefits, even being compilation targets for a high-level language
* Cutting out the translation from WebAssembly to the underlying ISAs could provide efficiency benefits
* We could get rid of WebAssembly virtual machines entirely, and replace them with WebAssembly physical machines
* If [all SIM cards are Java processors](https://twitter.com/hedgeberg/status/935380806549286912), imagine what WebAssembly processors could do. I'm betting that WebAssembly is a better bytecode than Java bytecode for what Java bytecode is doing with microcontrollers, so WebAssembly could take over all spaces that Java processors currently have

## Prior art

* https://en.wikipedia.org/wiki/Jazelle
* https://stackoverflow.com/questions/1153076/does-android-castrate-the-arms-jazelle-technology
* https://en.wikipedia.org/wiki/Lisp_machine
* https://en.wikipedia.org/wiki/Java_processor
* https://en.wikipedia.org/wiki/High-level_language_computer_architecture
