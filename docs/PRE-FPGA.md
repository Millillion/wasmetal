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
- [ ] Integrate controller startup/calibration and physical clock-crossing
  constraints before issuing timed CPU memory requests.
- [ ] Add an external-memory controller with independently checked device
  commands, timing, refresh, masking and reset. Board-specific PHY timing and
  electrical behavior still require hardware.

## Program loading and useful operation

- [x] Define and verify prepared-image framing, bounds, profile identity,
  corruption detection, commit/abort behavior and reset recovery.
- [x] Connect the verified receiver to writable instruction and metadata
  memories, allowing program upload without rebuilding the FPGA bitstream.
- [x] Exercise interrupted uploads, repeated boots, multiple programs, malformed
  traffic and independent serial clock rates in simulation.
  Native checks pass; complete mapped integration and programmable routing are
  still in progress. See the [upload guide](PROGRAM-UPLOAD.md).
- [x] Add reproducible workloads and cycle/memory statistics so optimization
  follows measurements. Preserve the full Wasm instruction semantics.
  See the [CRC and scalar/SIMD baselines](BENCHMARKS.md).
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
  [macro contract](SRAM.md) is concrete; a real macro and CPU integration remain.
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
