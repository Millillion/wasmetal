# Standalone boot

This milestone adds a second FPGA system around the existing WasMetal execution
core. Work is in progress. The host-backed reference system and its conformance
reports remain separate from verification of this integration.

The first standalone system boots a prepared image from block RAM, supplies all
instruction, function, type and backing-memory interfaces locally, and reports
the invocation's results or trap over UART. The computer prepares the image;
it does not supply instructions, memory transactions or execution results while
the FPGA runs. No physical board is required to develop or simulate this system.

## Image and memory contract

The preparation tool validates a module with the pinned `wasm-tools`, uses the
existing loader to preserve Wasm instruction identities and resolve metadata,
and records initialization for replay on the device. Initializer expressions
and the optional Wasm start function execute on RTL during preparation and are
replayed on RTL during boot. The exported function itself runs on the device.
Imports, on-device binary validation, dynamic program upload, external RAM and
reclaiming garbage collection are outside this first milestone.

The [profile](../soc/profile.json) bounds every image and storage structure.
An image that exceeds a bound must be rejected, not truncated. Linear memories
and tables receive explicit physical growth limits. The heap limit is passed
to the execution core. Resource exhaustion during execution can still trap.

The local memory controller serves all six core memory kinds: linear bytes,
globals, tables, data segments, element segments and heap values. It checks
full addresses, access widths, region limits and segment write protection
before writing any byte of a transaction. Tables, globals, elements and heap
slots contain 128-bit values; byte memory supports unaligned 1–16-byte accesses.
Reset clears mutable storage before replaying the image, including after a
reset in the middle of a transaction.

Instruction and function ROMs use synchronous falling-edge reads, consistent
with the core's existing half-cycle RAM contract. Type matching uses a bounded
subtype matrix. The CPU, memory controller, boot sequencer and UART share one
free-running clock. The board wrapper must constrain both clock edges.

Boot records contain a mode (bits 231:228), command kind (227:224), index
(223:192), auxiliary value (191:128) and data (127:0). Mode 1 issues a core
configuration or initializer invocation; mode 2 initializes 1–16 bytes of RAM
at the index address; mode 3 invokes the exported function; mode 0 terminates
the image. The boot controller must detect malformed records, traps and
watchdog expiry, and emit a bounded result rather than silently hanging.

## Verification gates

- Validate and bound prepared images; preserve source and artifact hashes.
- Test local memory boundaries, unaligned accesses, read-only segments,
  invalid indices, handshake behavior and reset interruption.
- Boot real Wasm programs through the complete RTL system and decode UART
  output, including calls, branches, linear memory, globals, tables, SIMD,
  floating point, GC, initialization, traps, restart and watchdog behavior.
- Compare suitable programs with the existing native execution model.
- Simulate the synthesized system and check the actual board clock/reset path.
- Route the standalone FPGA target, enforce timing and RAM limits, and verify
  the bitstream's unpack/repack round trip.

These checks do not substitute for the existing complete official core corpus,
or for eventual testing of a physical FPGA board.

## Preparing an image

```sh
make sim
python3 tests/standalone_image_test.py
python3 tools/prepare_standalone.py examples/standalone/answer.wat
```

The output directory is `build/standalone-image`. It contains a validated Wasm
binary, the recorded initialization, five padded hexadecimal ROM files, and a
manifest with storage bounds and hashes. `--export` chooses the function;
repeat `--arg` to supply numeric or SIMD arguments as unsigned raw bits.
Preparation does not invoke that exported function. The example's expected
result is 42; standalone execution is still being implemented and verified.
