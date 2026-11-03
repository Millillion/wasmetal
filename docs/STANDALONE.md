# Standalone boot

This milestone adds a second FPGA system around the existing WasMetal execution
core. RTL integration is implemented and tested; mapped-system verification and
routing are in progress. The host-backed reference system and its conformance
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
result is 42.

```sh
python3 tools/build_standalone_sim.py
python3 tools/check_local_memory.py
python3 tools/check_standalone.py
python3 tools/build_standalone_sim.py --board
python3 tools/check_standalone.py --board
```

The [RTL report](verification/standalone-rtl.json) covers 29 cases. The
[board-clock report](verification/standalone-board-rtl.json) covers nine cases,
including power-on, reset during RAM clearing, execution and UART transmission,
and restart. The test driver only drives clock/reset and samples the serial pin;
it cannot supply instructions or backing memory. The
[memory report](verification/standalone-memory.json) compares 4,836 transactions
with an independent byte-array oracle, including invalid requests and reset
interruption. UART checksum and deliberately wrong-result controls must fail.

The comprehensive [self-test](../examples/standalone/selftest.wat) exercises all
six backing-memory kinds, initialization, direct/indirect/reference/tail calls,
bulk operations, GC, exceptions, floating point and SIMD. It returns twelve
results, beginning with 42. Other integration cases exercise Memory64, subtypes,
sixteen results, resource limits and corruption. This is bounded integration
coverage, not the full official Wasm corpus on local RAM.

## Clock and UART

The board divides its 25 MHz oscillator by 32 to obtain a 781.25 kHz free-running
system clock with equal phases. The UART sends 8 data bits, no parity and one
stop bit, at 81 clocks per bit: about 9645 baud, 0.47% above 9600 baud. A terminal
or serial decoder should use 9600 baud. Reset asserts asynchronously at the board
reset synchronizer and releases through two clocked stages; boot clears the
entire local RAM before replaying initialization.

The binary result frame contains `57 4d 01`, status, Wasm trap code, result count,
a four-byte invocation cycle count, each result as sixteen little-endian bytes,
and a two-byte little-endian CRC-16/CCITT (polynomial 0x1021, initial 0xffff).
CRC covers the version through the last result. Status is 0 for success, 1 for
an exported-function trap, 2 for an invalid image, 3 for watchdog expiry, or 4
for an initializer trap. Errors carry no results. The watchdog bounds each
invocation, including initializers; UART completes after the CPU stops.
