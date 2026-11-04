# WasMetal RTL

## Target and current status

The implementation target is **the complete WebAssembly Core 3.0 ISA**, pinned to
`WebAssembly/spec` commit `6057acdb1a213f85369c64454c078a15f11ac4b1` (2026-10-28).
The earlier i32-only roadmap proposal is superseded as a compatibility target.
All 259 official core test files pass with direct integral rounding and the
SIMD selector, with both zero and three memory wait states: 57,711
execution assertions, 4,677 loader-validation assertions, and 254 embedding
assertions, with zero failures, unsupported cases, or blocked commands. The
[recorded report](verification/core-3.0-current.json) identifies source and
simulator hashes and every suite's counts. This establishes passage of that
test corpus, not a proof of correctness for every possible program. The recorded
run uses three memory wait states and completes 306,351,688 simulated cycles.
FPGA deployment has a
separate [board build and verification process](FPGA.md). Unsupported behavior
fails verification.

The verified native configuration shares floating-point arithmetic, uses
8,192 value slots and includes the descriptor RAM changes, SIMD selector and
direct integral rounding. Both native configurations preserve every command's
cycle count from the preceding revision. The new mapped CPU passes four
focused floating-point suites; its complete mapped regression is running.

The preceding selector revision [passed the complete mapped corpus in CI](verification/ci-selector-complete.json),
including exact command-cycle agreement, packaged executable/input checks and
local/CI circuit agreement. That receipt remains bound to the preceding sources.
Routed reports identify earlier CPU revisions; simulation does not establish
current physical timing.

The official **core** tests cover the ISA and module semantics. Browser DOM and
JavaScript embedding API tests are not processor ISA tests. Proposals not merged
into this pinned specification are not silently added to the target.

## Execution boundary

`rtl/wasmetal_core.sv` is a clocked stack machine. Each value slot is 128 bits.
It owns the program counter, operand and control stacks, locals, calls, arithmetic,
runtime bounds checks, and traps. Integer division is iterative. Floating-point
operations use separately licensed Berkeley HardFloat arithmetic and Wasm-specific
SystemVerilog wrappers. No `real`, `shortreal`, DPI interpreter, or host floating-
point execution implements Wasm instructions.

Four interleaved value banks supply the four newest operands. Locals, copies and
results reuse those read ports, and `array.copy` fetches its fifth operand in a
separate state. Pending writes are forwarded immediately. Integer SIMD operations
reuse a lane datapath over sixteen output-byte cycles; SIMD floating-point
operations reuse the scalar floating-point units. Descriptor RAM uses validity
bits so reset does not require a flip-flop for every stored data bit.

Single-precision operands are widened exactly for a shared raw arithmetic unit.
Its unrounded result and sticky bit feed separate final-format rounders, avoiding
an intermediate rounding. Integer conversions and format-specific bit operations
retain their separate precision implementations. Differential verification against
the earlier separate units covers 1,734,368 cases; this is not a formal arithmetic
proof. See the [floating-point report](verification/floating-point.json).

Ceiling, floor, truncation and nearest-even now use
[direct IEEE-field rounding](ROUNDING.md), preserving signed zero and canonical
NaNs. Both precisions have all-input component and mapped equivalence proofs.
A separate integration proof compares every format-unit output, including
non-rounding operations and flags, against the frozen prior implementation.
This change adds no state or latency.

Floating-point SIMD operands use explicit 32-bit or 64-bit lane selection.
The narrow result is zero-extended, and every out-of-range lane returns zero.
This removes the general multiplication formerly used to calculate the shift
amount. An [all-input binary proof](verification/simd-fp-selection.json)
extracts the actual CPU selection and result-assembly block and compares it
with the original definition using multiplication and shifting. It includes all lane indices,
operand values, arities, modes and widths. An independent four-state oracle
also checks 12,288 patterns, including unknown selector and data bits, and
rejects optimistic handling of unknown controls. These checks preserve the
instruction interface and cycle behavior; they are not whole-CPU equivalence.

Values, descriptors, control labels and saved call frames use synchronous block
RAM. Rising edges commit state and writes; falling edges capture reads for the
next rising edge. A preparation state provides instruction operands and metadata
time to settle. Fetching the fifth `array.copy` operand also restores the normal
operand window before resuming that same instruction. Assertions independently
check consumed addresses and data against storage. Both half-cycle paths must meet
timing. Descriptor-size queries take a separate command cycle, and result reads
must be clocked; the host adapter completes both clock phases.

The RTL now contains scalar integer and floating-point instructions, vector and
relaxed-vector operations, structured control, direct/indirect/reference calls,
tail calls, bulk memory/table operations, typed references, GC object operations,
and exception allocation, matching, and unwinding. This inventory is not a
conformance claim: the full regression remains the acceptance gate.

GC objects and exceptions currently use a bounded, external heap with a bump
allocator. References carry object kind, canonical type, extent, and heap address.
There is no reclaiming garbage collector yet. Heap exhaustion is reported rather
than silently reusing live objects. The loading front end canonicalizes recursive
types and supplies a read-only subtype relation; runtime tests and dispatch use
that relation in the RTL.

`tools/wasm_image.py` reads validated standard Wasm binaries. It decodes immediates
and computes structured-control targets, preserving the Wasm opcode of each
instruction. Code fetch uses this expanded representation, not raw binary bytes.
This is a trusted software loading front end; a raw-bytecode fetch decoder is not
present. Loading requires a host and is not a self-contained boot implementation.

The loader relocates function, global, memory and table indices. Initializer
expressions are emitted as functions and executed through the RTL. Data/element
segment placement and module linking are embedding/instantiation work. The
external `wasm-tools validate` command performs module validation. Validation
assertions are reported separately and are never described as RTL execution tests.

Memory configuration reserves and zero-initializes the **entire configured backing
capacity** at instantiation, before installing active data segments. `memory.grow`
then exposes a larger prefix of that storage after the RTL checks the maximum;
there is no operating-system allocation during the instruction. The reserved tail
must remain inaccessible to every other master. An FPGA memory adapter must honor
this initialization/isolation contract; arbitrary uninitialized DRAM is not valid
backing storage. The simulator uses sparse zero-initialized storage for this contract.

`sim/main.cpp` supplies clocks, read-only instruction/function descriptors, and
backing memory. It has no Wasm instruction interpreter. Expected results stay in
the Python test runner and are not sent to the simulator. Memory wait states can
be inserted to test transaction handling. Unrecognized memory protocols fail.

## Verification

Run `python3 tools/bootstrap.py` to fetch checksum-pinned dependencies on Ubuntu
24.04 x86-64, then:

```sh
make lint
make sim
make test
make test-all
make test-divider
make test-fpu
make test-simd test-popcount test-values test-descriptors
make test-ecp5-ram test-core-four-state
make prove-masks
python3 tools/prove_descriptors.py
python3 tools/check_simd_fp_selection.py
python3 tools/check_engine.py
python3 tools/run_spec.py --suite i32 --suite i64 --wait-states 3
```

`make test` is a fast scalar-integer regression. **It is not the completion gate.**
`make test-all` selects every `.wast` file recursively under the pinned upstream
`test/core` tree. It returns nonzero for failed/unsupported cases, converter
failures, or cases blocked by a simulator failure. Its JSON report records the
selected baseline, counts, and failures. Reports and downloaded tests are ignored
build artifacts; upstream test files are never edited to make them pass.
Reports also identify the source and simulator binary by SHA-256. Suite files run
in independent simulator processes, with four workers by default. The cycle
budget includes the official million-tail-call tests; timeouts never count as
expected Wasm exhaustion. Loader validation and embedding assertions have
separate counters from execution assertions.

The simulator is built with runtime assertions for stack bounds, stable stalled
memory requests and stable SIMD operands. Independent checks cover 4,041 divider
cases, 6,761 serial-versus-parallel SIMD cases, 77,888 popcount vectors and 25,097
banked-stack reads. A four-state Icarus test checks 40,000 descriptor reads,
including reset, forwarding and invalid indices. Yosys proves 372 optimized
HardFloat mask specializations equivalent for every binary input. Unbounded
induction checks descriptor reset elision and forwarding against fully reset
reference storage at capacities 1, 13, 16 and 256; the 13-entry case also checks
multi-bit words. The clock model explicitly includes both edges. These proofs are local properties, not a formal proof of the
entire CPU.

Four-state ECP5 block-RAM tests compare inferred storage with the restricted
primitive model over 10,512 wide-memory transactions and 14,096 deep-memory
transactions. They cover initialization, separate nine-bit write enables, bank
selection, both read edges and read-before-write. Eleven deliberately unsupported
configurations verify the model's rejection checks. A separate four-state CPU
bench checks eight execution, initialization and reset cases with non-power-of-two
storage capacities. Immediate-assertion diagnostics fail its runner even when
Icarus itself exits successfully.

The old parallel integer-SIMD implementation remains an independent structural
oracle and is not instantiated in the CPU. Expected Wasm results remain outside
both implementations. `tools/check_engine.py` deliberately supplies wrong expected
values/traps, checks signed zero and NaN/reference matching, fills the value stack
exactly, checks tail-frame reuse and bounded five-operand array copying, and confirms that a timeout cannot pass an
exhaustion assertion.

The present RTL uses finite parameterized value/control/call storage. Exhaustion
has a distinct result. Capacity limits, simulator timeouts, tool limitations and
unimplemented behavior must remain visible in reports. A passing subset cannot
set `full_core_suite_passed` to true.

## FPGA completion requirements

Simulation is one gate. A deployable FPGA system additionally needs synthesis,
resource fit, memory inference checks, a memory/controller integration, a board
wrapper and clock/reset constraints, placement/routing timing closure, a load
interface, and hardware bring-up tests. These are not established by compiling
SystemVerilog with Verilator. The current external memory/descriptor interfaces
make that integration explicit.

The full UART wrapper has passed simulation, including fourteen execution and
transport checks. Functional simulation of the production mapped ECP5 CPU passes
all 259 official suites with three memory wait states, both locally and in CI.
The [full CI report](verification/ci-mapped-complete.json) records the same
57,711 execution assertions and 306,351,688 canonical cycles as native RTL under
that memory profile, with every command's cycle count matching. The
[earlier local report](verification/ecp5-full.json) also covers the intact corpus;
both supersede the earlier subset results. See the
[CI verification flow](DESIGN-FLOW.md#what-ci-runs) for complete coverage and
repeated-setup accounting.

The host adapter also supports an
explicit physical serial device. The native and FPGA defaults have matching
storage capacities; see [FPGA.md](FPGA.md) for those limits and
physical bring-up instructions. There is no claim of physical-board testing.

## Licensing

Project code uses the repository MIT license. The existing root copyright notice
has not been changed. `third_party/hardfloat/COPYING.txt` governs HardFloat; its
README records origin, archive checksum and the compatibility patch.
