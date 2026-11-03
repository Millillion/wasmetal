# WasMetal

A project to build a bare metal physical implementation of WebAssembly. That's right, a WebAssembly CPU. Inspired in part by [this amazing talk](https://www.destroyallsoftware.com/talks/the-birth-and-death-of-javascript).

WasMetal is being revived under [Millillion](https://github.com/Millillion) in 2026. It implements WebAssembly Core 3.0 instructions in a clocked SystemVerilog stack machine, with a software loading and validation front end.

Completed work lives on `main`. Temporary development branches are integrated into `main` and pushed before a task is finished; the README is reviewed with every commit.

## Current status

- **Standalone boot:** prepared images execute using local instruction, function, type and backing memory, with autonomous initialization and UART results. [29 RTL cases](docs/verification/standalone-rtl.json) and [nine board-clock cases](docs/verification/standalone-board-rtl.json) passed. The [complete synthesized system](docs/verification/standalone-mapped.json) matches every UART byte and completion clock across four boot/reset scenarios. The production memory controller passes [4,837 oracle-checked transactions in both models](docs/verification/standalone-memory-mapped.json), with separately checked [four-state RAM models](docs/verification/standalone-ram-model.json). The [routed ULX3S bitstream](docs/verification/standalone-routing.json) uses 59,657/83,640 logic cells and 171/208 block RAMs, meets its 781.25 kHz clock and passes unpack/repack verification. These are bounded integration tests, separate from the full host-backed corpus below. **No physical board has been tested.** See the [standalone guide](docs/STANDALONE.md).
- **Conformance:** the current committed RTL passes all 259 pinned official suites with three memory wait states: 57,711 RTL execution assertions, 4,677 validation assertions and 254 embedding assertions, with zero failures or unsupported cases. The [recorded result](docs/verification/core-3.0-current.json) identifies the exact sources, simulator and capacities; this run completed 306,351,688 simulated cycles. [CI also passed](https://github.com/Millillion/wasmetal/actions/runs/41470404770) the complete corpus both with and without memory stalls, arithmetic and boundary checks, and the UART simulation.
- **Floating point:** arithmetic shares one raw datapath and rounds directly to either precision. [1,734,368 additional comparisons](docs/verification/floating-point.json) cover arithmetic, conversions, traps and reset interruption, with separate negative controls.
- **Storage:** the native and FPGA defaults both use 8,192 value slots, 2,048 labels, 512 call frames, 256 descriptors per class and 1,048,576 external heap slots. Generated host and FPGA interface headers advertise the matching capacities and build identity. These remain finite resource limits.
- **Mapped circuit:** CI passes **all 259 pinned official suites** on the default ABC9 ECP5 mapping with three memory wait states. The [full CI report](docs/verification/ci-mapped-complete.json) records 57,711 execution assertions, 4,677 validation assertions and 254 embedding assertions, with zero failures or unsupported cases. Every suite's counts and every command's canonical cycle count match native RTL. All sixteen partitions and the final coverage check passed; the [verification record](docs/verification/ci-complete.json) preserves source, model and report identities and an independent aggregation check. The [earlier local run](docs/verification/ecp5-full.json) also passed the intact corpus in 8 hours 14 minutes; its netlist is the standard bitstream build's core. Optional `--fast-sim --fast-luts` builds preserve the circuit; the lookup models pass [binary equivalence and 287,232 four-state checks](docs/verification/ecp5-lut-model.json). See the [verification flow](docs/DESIGN-FLOW.md). Whole-circuit formal equivalence remains [inconclusive](docs/verification/mapping-equivalence.json).
- **FPGA:** the committed configuration passed fourteen whole-board UART checks in simulation; see the [interface report](docs/verification/fpga-uart.json). The [standard build](docs/verification/fpga-routing.json) produces a routed, timing-verified ULX3S 85F bitstream: 58,892 of 83,640 logic cells (70.4%), with the core meeting 1 MHz at a reported 3.24 MHz maximum. A fresh build reproduced the bitstream exactly and passed its unpack/repack check. **No physical board has been tested.**

See the [RTL architecture](docs/RTL.md) and [FPGA guide](docs/FPGA.md) for the execution boundary and reproducible verification commands. The host-backed conformance system supplies the instruction image, metadata and backing memory from the computer. The standalone prototype supplies these locally for bounded prepared images. External RAM, dynamic program loading and reclaiming garbage collection remain future work.

For an explanation of the ISA, microarchitecture, SystemVerilog RTL, the two simulation models, synthesis and the FPGA bitstream, read [From the Wasm specification to an FPGA](docs/DESIGN-FLOW.md).

The [FPGA purchase research](docs/FPGA-SELECTION.md) compares development boards, current tool licensing, community support and US home-use compliance. It recommends Genesys 2 as the next technical platform, conditional on supplier clarification of its regulatory basis for home R&D; ZCU104 is the leading alternative with an onboard Arm host. A [core-only Xilinx synthesis estimate](docs/research/xc7-resource-estimate.json) uses 47,801 LUT primitives, about 23.5% of Genesys 2's LUT capacity, and passes structural checks. This estimate has no Xilinx functional, placement or timing validation. ULX3S 85F remains the only routed board target; no board has been purchased or physically tested by this work.

## GUI Microarchitecture Simulator

The [historical demo](https://wasm-metal-demo.netlify.com) uses the original hosting address; its availability has not been verified for the revival.

```bash
git clone https://github.com/Millillion/wasmetal.git
cd wasmetal
npm install
npm start
```

Go to [http://localhost:5000](http://localhost:5000) in your web browser.

## RTL Microarchitecture Simulator

The clocked SystemVerilog core runs in Verilator. The test harness converts the
pinned official Wasm core test suite and compares its expectations with RTL
execution results and traps. Unsupported cases fail the run.

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

A separate standalone CI job runs the local-memory and UART integration tests,
builds and routes the complete autonomous system, checks its RAM models, and
compares the mapped circuit with board RTL. It retains `standalone-verification`
and `standalone-fpga` artifacts for 30 days. Its mapped integration checks use
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
