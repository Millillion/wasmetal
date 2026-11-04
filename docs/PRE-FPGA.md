# Work before a physical FPGA

This is the active engineering sequence toward a useful standalone WasMetal
system and, later, an ASIC. A passed simulation, a routed FPGA design, a measured
board result and foundry signoff are separate kinds of evidence.

## Memory and performance

- [x] Introduce a bounded 128-bit memory transaction interface with byte enables,
  explicit completion/fault handling and a timeout that prevents reuse after a
  lost response.
- [x] Verify region translation, unaligned transfers, read-only segments, all
  logical memory kinds, stalls, faults and reset against an independent oracle.
- [x] Integrate a wider local block-RAM backend, measure boot and execution
  cycles, and repeat standalone RTL, mapped-circuit and routing checks.
- [x] Add an independently verified AXI4 adapter for a future board-specific
  memory controller, including separate channel stalls and error recovery.
- [x] Verify a separate memory clock, common reset and stopped-clock recovery;
  test the assembled clock-crossing and AXI path in RTL and mapped simulation.
- [x] Connect the complete CPU to that AXI path in simulation. All 35 system
  cases pass with two slower memory clocks, response delays, separate channel
  stalls, nonzero initial RAM and retained contents across reset. Deliberately
  corrupted reads fail the independent result check. See the
  [complete-CPU AXI checks](AXI.md#complete-cpu-integration).
- [ ] Integrate controller startup/calibration and physical clock-crossing
  constraints before issuing timed CPU memory requests.
- [x] Add a separate SDR SDRAM controller with independently checked device
  commands, timing, refresh, masking and reset. Its [six-profile campaign](SDRAM.md)
  passes 836,574 requests and 774 warm resets per model in native and mapped
  simulation, plus four-state checks. Unbounded protocol safety proofs pass
  all six configurations with seven rejected controller mutations.
- [x] Connect the SDR controller to the complete CPU in a separate simulation.
  All 35 system cases pass in two timing configurations, including startup
  that extends beyond program commit. Corrupted reads and deliberately
  bypassed startup gating fail independent checks.
- [x] Run the complete CPU through the CDC and SDR controller with separately
  scheduled clocks. All 35 cases pass with faster and slower memory clocks,
  including delayed initialization. Wrong clock binding, startup bypass and
  corrupted reads are rejected. The clock scheduler passes an independent
  event-sequence check with six rejected mutations. See [SDRAM integration](SDRAM.md#complete-cpu-with-separate-clocks).
- [ ] Implement and verify the board PHY, then route the complete external
  memory system. Physical timing and electrical behavior still require
  hardware. Genesys 2 requires a separate DDR3 controller/PHY.

## Program loading and useful operation

- [x] Define and verify prepared-image framing, bounds, profile identity,
  corruption detection, commit/abort behavior and reset recovery.
- [x] Connect the verified receiver to writable instruction and metadata
  memories, allowing program upload without rebuilding the FPGA bitstream.
- [x] Exercise interrupted uploads, repeated boots, multiple programs, malformed
  traffic and independent serial clock rates in simulation.
  All 35 native and mapped checks pass with identical UART output and clocks.
  See the [upload guide](PROGRAM-UPLOAD.md).
- [ ] Complete programmable FPGA routing, timing verification and bitstream
  round-trip checks. The current ULX3S placement uses 192 of 208 block RAMs;
  the direct-rounding baseline places 61,344 logic cells. An equivalent
  reset-distribution experiment adds 31 LUTs and reduces the placer wire-length
  cost by 7.1%, with unchanged capacities. Both wrapper comparisons and native
  integration checks pass; the new complete mapped comparisons are running.
  [Routing remains incomplete](PLACEMENT.md).
- [x] Measure the complete programmable system on a larger FPGA family without
  reducing configured capacities. The [7-series estimate](research/xc7-system-estimate.json)
  passes structural checks with 52,437 logic LUT primitives and 96 equivalent
  36-Kbit RAM blocks. Xilinx functional verification and physical implementation
  remain separate work; no board selection or working port follows from this
  measurement alone.
- [x] Add reproducible workloads and cycle/memory statistics so optimization
  follows measurements. Preserve the full Wasm instruction semantics.
  See the [CRC and scalar/SIMD baselines](BENCHMARKS.md).
- [x] Compile a freestanding C program to Wasm and execute its uploads in both
  complete-system models, comparing independent results, UART bytes and cycles.
  See the [compiled CRC-32 example](../examples/c/README.md).
- [x] Prepare a reproducible physical-board acceptance campaign with exact
  simulation references, repeated program replacement and partial failure
  reports. The [host tooling](BOARD-ACCEPTANCE.md) is tested; the physical run
  still requires a board.
- [ ] Define the host-call/runtime boundary for applications that need I/O;
  arbitrary Wasm binary validation and garbage collection are additional work.

## ASIC preparation

- [x] Inventory inferred memories, clock edges, reset assumptions and FPGA
  primitives. Identify the memory and clock/reset boundaries needing replacement.
- [x] Produce technology-neutral elaboration evidence without
  silently converting large SRAMs to flip-flops or claiming an FPGA bitstream
  is an ASIC implementation.
- [x] Define and independently verify a synchronous backing-SRAM adapter with
  byte masks, configurable read latency and reset/release behavior. The
  [macro contract](SRAM.md) is concrete; integration with a real macro remains.
- [x] Connect that adapter to the complete CPU in simulation and run all 35
  system cases at two read latencies, starting SRAM with nonzero contents and
  preserving memory across reset. Reject deliberately corrupted read data.
  This uses a behavioral macro; the default FPGA backend remains block RAM.
- [ ] Define implementation timing constraints against selected clocks,
  interfaces, macros, standard cells and operating corners.
- [ ] Define SRAM/ROM macro contracts, power-on reset, debug/test access,
  manufacturing-test requirements and physical-design acceptance checks.
- [ ] Select a real process, compatible macros, I/O and packaging, then perform
  process-specific synthesis, physical design, timing/power and physical signoff.
  These choices require actual PDK/IP and fabrication information; no tapeout
  readiness follows from a generic model or an educational process library.

## Verification throughout

Keep the complete pinned official corpus on the execution core, independently
verify new interfaces and primitives, and test the assembled system end to end.
Preserve hashes, commands, bounded capacities and negative controls in reports.
Do not treat integration samples as the entire official corpus on local RAM.
Commit completed increments to `main`, with the README reflecting measured
results and the remaining hardware checks.
