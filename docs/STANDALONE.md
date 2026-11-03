# Standalone boot

This milestone adds a second FPGA system around the existing WasMetal execution
core. RTL and mapped-system integration tests pass, and the complete system
routes for ULX3S 85F with checked timing and a verified bitstream round trip.
No physical board has been tested. The host-backed reference system and its
conformance reports remain separate from verification of this integration.

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

The current profile has 128 KiB of shared backing RAM, 1,024 instructions,
128 functions, 64 types, 512 boot records and at most 16 returned values.
Each linear memory is limited to one 64 KiB page, each table to 128 entries,
and the heap to 1,024 sixteen-byte slots. These allocations share the 128 KiB
pool with globals and passive segments; their individual maxima are not all
simultaneously available. Programs that need more storage require a new profile
and sufficient FPGA resources or external memory.

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

The [production memory-controller report](verification/standalone-memory-mapped.json)
checks 4,837 transactions against the independent oracle in both RTL and mapped
simulation, using the full 128 KiB RAM and regions crossing physical RAM banks.
The [RAM-model checks](verification/standalone-ram-model.json) cover every address
in all five additional configurations, both ROM clock edges, read-before-write
behavior, unknown addresses, and deliberate model corruption. Unsupported modes
fail model generation. The existing execution core's checked RAM models remain
unchanged.

The [complete-system mapped report](verification/standalone-mapped.json) compares
the self-test's UART bytes and exact completion clocks with board RTL for
power-on and restart, external reset, reset during execution and reset during
UART transmission. The mapped model includes the CPU, local memory, boot
sequencer, divided clock, reset and UART. It uses the complete pre-routing
mapped netlist, not a delay-annotated post-routing simulation. Placement/routing
timing analysis is a separate gate; these checks are not whole-circuit formal
equivalence or electrical testing.

## Reproducing the FPGA build

```sh
python3 tools/bootstrap.py --fpga-tools
make standalone-test
make standalone-bitstream
```

The default image is `examples/standalone/selftest.wat`. To build a different
bounded image, use `make standalone-bitstream STANDALONE_IMAGE=path/to/program.wat`.
For non-default exports or arguments, prepare the image explicitly, run
`make standalone-core`, then `python3 tools/build_standalone_board.py`.
Do not run `make standalone-bitstream` afterward unless intending to replace
that image with `STANDALONE_IMAGE`.

The [routing receipt](verification/standalone-routing.json) records 59,657 of
83,640 logic cells, 171 of 208 block RAMs and 27 of 156 multipliers. The core
meets the configured 0.78125 MHz clock; the timing tool reports a 3.04 MHz
maximum. Its critical falling-to-rising path is 164.36 ns against a 640 ns
budget. These are tool estimates, not measured board performance.

The bitstream is `build/standalone-ulx3s/wasmetal.bit`. Its neighboring manifest
records the source, image, netlist, timing and bitstream hashes. Build acceptance
requires both clocks and half-cycle paths to meet timing, resource limits to
hold, and unpacking/repacking to reproduce the bitstream exactly. The unchanged
mapped CPU is restored after separately synthesizing the wrapper, so synthesis
cannot replace instruction execution with a constant result for the example.

```sh
make standalone-mapped-test
```

This runs the native checks, prepares the self-test, synthesizes the CPU, routes
the board, checks production memory in both models, checks RAM models, builds
the full mapped simulator, and compares board RTL and mapped behavior. CI runs
the same target in its **Standalone FPGA system** job. Reports and the verified
bitstream/image are retained as artifacts for 30 days; local reports are under
`reports/standalone*.json`. The older host-backed target and all 259 official
conformance suites remain separate. New pushes cancel superseded runs of the
same workflow/ref.

The [first clean CI job](https://github.com/Millillion/wasmetal/actions/runs/41572176563/job/125707382260)
passed on source commit `4e8e696ff7d568e43d04e77c4a6088409ad8dfa0`.
The [CI receipt](verification/standalone-ci.json) preserves its reports and
artifact archive hashes. Independent checks after download confirmed all 63
referenced tracked source hashes, identical UART bytes and completion clocks
for every local/CI case, identical prepared images, accepted timing, and a
bitstream identical byte for byte to the local build. This records the
standalone job's success; the separate full-core workflow has its own results.

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

When a physical board is available, the [volatile SRAM loading procedure](FPGA.md#loading-a-physical-board)
uses the standalone bitstream instead of the host-backed one:

```sh
openFPGALoader -b ulx3s -d /dev/ttyUSB0 build/standalone-ulx3s/wasmetal.bit
```

This hardware step has not been executed here. On a POSIX host, start the reader
and then reset the programmed board:

```sh
python3 tools/read_standalone.py --device /dev/ttyUSB0
```

Choose the actual board serial device. The reader temporarily configures
9600-baud 8N1, verifies frame length/status/CRC, prints raw result bits in decimal
and hexadecimal, and restores terminal settings on exit. Floating-point and
SIMD values are not converted to decimal floats or lane arrays. It tolerates a truncated old
frame and times out after 30 seconds by default. `--hex` decodes a captured frame
without a serial device. The reader is tested with pipes and a pseudo-terminal;
physical UART connectivity still needs board testing.
