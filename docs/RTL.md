# WasMetal RTL

## Target and current status

The implementation target is **the complete WebAssembly Core 3.0 ISA**, pinned to
`WebAssembly/spec` commit `6057acdb1a213f85369c64454c078a15f11ac4b1` (2026-10-28).
The earlier i32-only roadmap proposal is superseded as a compatibility target.
Implementation is in progress. Neither full conformance nor FPGA readiness is
claimed. Unsupported instructions and script commands fail the verification run.

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

## Licensing

Project code uses the repository MIT license. The existing root copyright notice
has not been changed. `third_party/hardfloat/COPYING.txt` governs HardFloat; its
README records origin, archive checksum and the compatibility patch.
