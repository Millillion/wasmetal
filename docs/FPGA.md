# WasMetal FPGA bring-up

The reference board is a **ULX3S 85F**, with an ECP5 LFE5U-85F, CABGA381 package,
speed grade 6. Smaller ULX3S variants cannot use this bitstream. The pin assignments
come from the board project's [v2.0 constraints](https://github.com/emard/ulx3s/blob/6a92cec6b177191c5b0f80e260013a1f8ec147dd/doc/constraints/ulx3s_v20.lpf).

For a new purchase, see the [board selection research](FPGA-SELECTION.md). Its
Genesys 2 recommendation and exploratory resource estimate do not establish a
supported Xilinx target; the reference build described here remains ULX3S 85F.

This is a host-backed bring-up system. The FPGA contains the clocked Wasm execution
engine, including integer, floating-point, SIMD, reference, GC and exception
instructions. A host loads validated modules and supplies the expanded instruction
image, function/type metadata and backing storage over UART. The host does not
calculate instruction results. This system has no autonomous boot, SDRAM
controller or operating system. A physical board has not been programmed or tested
in this workspace.

## Storage profiles

[`fpga/profile.json`](../fpga/profile.json) defines the FPGA's finite capacities.
They are advertised by the bitstream and checked by the host:

The FPGA and native conformance simulator now use the same capacities:

| Resource | Capacity |
|---|---:|
| 128-bit value slots, including locals | 8,192 |
| Control labels | 2,048 |
| Saved call frames | 512 |
| Descriptors per memory/table/segment class | 256 |
| External 128-bit heap slots | 1,048,576 |

Programs exceeding these finite resources cannot be assumed to run successfully.
The current committed RTL, including the 8,192-value profile and shared
floating-point arithmetic, passed the full official corpus with three memory
wait states; the report below identifies its exact source and simulator hashes.
The [standard-build routing record](verification/fpga-routing.json) contains a
completed, timing-verified bitstream for the same RTL: 58,892 of 83,640 logic
cells (70.4%), 98 of 208 block RAMs and 27 of 156 DSP blocks. The core meets its
1 MHz constraint with a reported maximum of 3.24 MHz, and the bridge meets
12.5 MHz. The bitstream survives unpacking and repacking with identical bytes.
ABC9 mapping and static placement are the default recipe. A fresh
`make fpga-bitstream` run reproduced the prototype bitstream byte for byte.
The rebuilt native simulator is also identical to the full-suite-tested binary.
The complete 259-suite mapped functional regression has also passed. An additional
formal comparison was inconclusive; see the verification details below.
Heap allocation is bounded and currently has no reclamation. Mapped-cell results
apply to their recorded netlist and capacity profile; a changed mapping requires
its own checks.

The host reserves zero-initialized backing storage up to each memory's configured
maximum. The core checks bounds and exposes additional pages on `memory.grow`.
The unused tail must remain private and zeroed until exposed. The supplied sparse
host adapter implements that contract.

## Reproducible build

On Ubuntu 24.04 x86-64:

```sh
python3 tools/bootstrap.py --fpga-tools
make lint
make fpga-smoke fpga-host
make fpga-bitstream
```

The optional FPGA tool download is large. Dependencies and upstream tests are
checksum-pinned in `tools/upstream.lock.json`; installation stays under `.cache`.
The build uses Yosys 0.33, nextpnr-ecp5 and Project Trellis. `tools/cad.py` launches
the pinned CAD-suite binaries without their configuration-writing wrapper scripts.

`make fpga-core` uses ABC9 with ECP5 LUT timing models and a 500 ns combinational
target, creating `build/core-ecp5.json` and its source manifest.
`tools/build_board.py` checks that manifest, integrates the UART wrapper, then
uses the static placer, saves `placed.json`, and routes that checkpoint with
router2. Each stage starts with seed 1 by default. Timing failures fail the command; there is no
`--timing-allow-fail` option. A successful build produces:

- `build/ulx3s/wasmetal.bit`: FPGA configuration.
- `build/ulx3s/timing.json`, `timing-audit.json` and `nextpnr.log`: timing and resource evidence.
- `build/ulx3s/placed.json` and `commands.json`: placement checkpoint and exact commands.
- `build/ulx3s/manifest.json`: source, configuration and bitstream identities.

The timing audit checks all three constrained clocks, both held-bus crossings,
and the reported core critical path against its full-cycle or half-cycle budget.
The build unpacks and repacks the bitstream and requires identical bytes before
publishing `wasmetal.bit`; a failed rebuild removes stale final output.

Rebuild the host adapter after changing RTL or the FPGA profile. The protocol
checks a port-schema identifier and a 128-bit RTL build fingerprint, and rejects
an incompatible bitstream. The official-suite runner also checks executable and
source hashes before and after a run.

## Functional verification

`make fpga-smoke` simulates the entire board wrapper and UART, including serial
bits, framing, CRCs, clock pulses and the real CPU. It exercises arithmetic,
unaligned memory, SIMD, floating-point division, GC objects and array copying,
exceptions, bounds traps and zero-filled memory growth. It verifies that corrupt
packets, invalid flags, capability queries and abandoned packets do not execute
instructions. An incomplete packet is discarded after a 100 ms receive timeout.

For an additional check of synthesis mapping:

```sh
python3 tools/build_gate_sim.py --core-netlist build/core-ecp5.json
python3 tools/run_spec.py --simulator build/gate-model/obj/Vwasmetal_core \
  --suite i32 --suite i64 --suite f32 --suite f64 --suite conversions \
  --report reports/mapped-arithmetic.json
```

This is functional simulation of the mapped FPGA cells, not a timing simulation.
It uses Yosys' LUT, dedicated `PFUMX`/`L6MUX21` multiplexer, carry and flip-flop models,
plus the checked block-RAM model described below. The unregistered 18-by-18 DSP
multiplier model accepts only the configurations emitted by this flow; unexpected
primitive types, DSP modes or connections fail the build.

Values, control labels, call frames and descriptor data use synchronous block
RAM, with rising-edge writes and falling-edge reads. The checked `DP16KD` model
accepts the generated 512-by-36 pseudo-dual-port and 2048-by-9 dual-port modes.
Its packing follows pinned Yosys' mapping and its behavior follows the
[Lattice memory guide](https://www.latticesemi.com/-/media/LatticeSemi/Documents/ApplicationNotes/EH/FPGA-TN-02204-1-6-ECP5-and-ECP5-5G-Memory-Usage-Guide.ashx?document_id=50466).
`make test-ecp5-ram` compares mapped and inferred initialized storage in a four-state
simulator, including both read edges, banking and partial writes. The timing
report must also cover the CPU's half-cycle RAM paths.

At execution-source revision `bf3ce24`, the four-input-LUT mapped CPU passed forty
official suites with three memory wait states: 17,379 execution assertions over
1,912,810 cycles covering scalar arithmetic, SIMD, GC, exceptions, control,
calls, locals and memory/table sizes in the
[mapped-cell report](verification/ecp5-mapped.json). The
default ABC9 mapping first passed the same forty suites with identical assertion
counts and cycle counts; see its [initial mapped-cell report](verification/ecp5-abc9.json).
The tested netlist is byte-identical to the standard bitstream build’s core. The
[whole-board UART report](verification/fpga-uart.json) records fourteen passing
execution and transport checks. Each report identifies its executable, sources
and capacity profile. These initial mapped reports are subsets; the
[complete native 259-suite report](verification/core-3.0-current.json) records the original RTL simulation with the same capacities as the FPGA profile.

The unchanged default ABC9 netlist now passes the [complete 259-suite mapped
regression](verification/ecp5-full.json): 57,711 execution assertions, 4,677
validation assertions and 254 embedding assertions over 306,351,688 cycles,
with three memory wait states. All final source/executable identity checks passed,
and every per-suite count exactly matches the native RTL result. There were no
failures, unsupported cases, conversion errors, blocked commands or runner errors.
The local run completed in 8 hours 14 minutes with four workers. The
[completed checkpoint](verification/mapped-regression-status.json) preserves the
final report identity and historical evidence.

CI runs the full official corpus against the original RTL, with and without
memory stalls. It also builds the synthesized CPU and distributes the complete
corpus across 16 CI jobs. All sixteen jobs and the final coverage and native
agreement check [passed](https://github.com/Millillion/wasmetal/actions/runs/41470404770).
The [full CI report](verification/ci-mapped-complete.json) and
[verification record](verification/ci-complete.json) preserve the results and
their source/model identities. The
[design-flow explanation](DESIGN-FLOW.md#what-ci-runs) describes partition safety,
the shared executable, report artifacts and the final acceptance check.

An additional [whole-mapping equivalence attempt](verification/mapping-equivalence.json)
was inconclusive. The bounded solver timed out. A second model used 929 internal
cut points with an acyclic dependency graph, but allowed independent internal
values that violated their signal definitions. Its counterexample produced no
differing outputs when replayed on the original circuits. This is not a formal
proof of either the complete CPU or equivalence of the two mappings. The two
reference netlists are reproducible with the current synthesis tools, and both
pass the forty-suite mapped regression described above.

## Loading a physical board

First build successfully and inspect its manifest and timing report. With the
correct board connected, openFPGALoader can load volatile SRAM:

```sh
openFPGALoader -b ulx3s -d /dev/ttyUSB0 build/ulx3s/wasmetal.bit
```

Select the actual board's device path. This is the documented
[SRAM-loading command](https://trabucayre.github.io/openFPGALoader/guide/first-steps.html)
for the supported [ULX3S board profile](https://trabucayre.github.io/openFPGALoader/compatibility/board.html).
It does not program persistent flash. Loading is a manual hardware step and has
not been executed here.

Then select that board's serial port explicitly and run the same bring-up checks:

```sh
WASMETAL_SERIAL=/dev/serial/by-id/your-board \
  python3 tools/check_fpga.py --simulator build/wasmetal-fpga
```

The adapter uses exclusive access, raw 8N1 at 500,000 baud, no flow control and
bounded I/O waits. It does not discover or open a device without `WASMETAL_SERIAL`.
It does not retry a potentially executed instruction after a lost response.

The official runner can use that same executable with `--simulator`. UART
single-stepping is deliberately slow; the full corpus contains hundreds of
millions of clock cycles and is not a quick physical bring-up test.

## Clocking and transport

The 25 MHz board oscillator feeds a free-running divide-by-two flip-flop. A DCCA
routes its 12.5 MHz output to the UART and bridge. A second DCCA routes the manual
CPU clock onto a global clock network. Each accepted step holds new inputs stable
for 8 microseconds before the CPU edge, holds its pulse high for 2 microseconds,
then waits at least 4 microseconds before returning outputs. The core clock and
inputs remain held during transmission, so the bridge reads the stable output bus
directly; simulation assertions check this condition. An evaluation request
changes inputs and samples combinational outputs without a CPU edge.

The build checks all three clock constraints and separately audits both directions
of the held-bus crossing. It requires each cross-domain path to settle within a
conservative 1 microsecond budget, below the protocol's actual hold times. This
does not replace the same-clock timing checks or introduce timing waivers.

Requests contain `57 4d`, flags, sequence, 106 input bytes and a little-endian
CRC16-CCITT-FALSE. Responses contain `57 52`, status, sequence, 67 output bytes and
the same CRC. The CRC covers flags/status, sequence and payload. Flag 0 evaluates,
flag 1 steps, flag 2 reads capabilities; flag 3 is invalid. `fpga/ports.json`
defines packed bit positions; generated headers bind the C++ and RTL layouts.

The error LED indicates a bad or timed-out frame; the busy LED reflects CPU
execution. The board button resets the transport. The host explicitly clocks a
CPU reset during initialization.

## Next hardware stages

Physical-board testing is still required. A separate
[standalone prototype](STANDALONE.md) now implements local memory and fetch
controllers, autonomous clocking, prepared-image boot and UART results. Its
RTL and board-clock integration tests pass. Mapped-system verification and
standalone routing are in progress; buffered program loading and external memory
remain future work.

The development computer prepares and validates the image; loading and
validating arbitrary Wasm binaries on the device is additional work. External
memory can follow, using controller and memory-device models during development.
Vendor-specific memory IP may require a vendor-supported simulator instead of
Verilator.

The physical board is needed to confirm electrical interfaces, memory
calibration where applicable, power-on behavior and measured performance.
An ASIC additionally requires a process/PDK, memories, I/O and clock/reset
integration, physical design, signoff and fabrication; the FPGA bitstream is not
an ASIC deliverable.
