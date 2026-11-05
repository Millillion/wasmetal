# Experimental SKY130 SRAM bank wrapper

`soc/asic/wasmetal_sky130_sram.sv` connects the existing synchronous adapter to
the named OpenRAM `sky130_sram_2kbyte_1rw1r_32x512_8` macro interface. Four
512-word, 32-bit instances form an 8 KiB bank of 128-bit words. Larger arrays
use additional banks; each byte write enable reaches its corresponding lane.
The unused second read port is disabled. Only one transaction may be outstanding,
as enforced by `wasmetal_sram_memory`.

The wrapper is tested with the **unmodified upstream behavioral model**, pinned
to [VLSIDA revision 965df150](https://github.com/VLSIDA/sky130_sram_macros/tree/965df150c754fe2b3f93a0bd1f9883eb114279b2).
The [source lock](../tools/sky130_sram.lock.json) records its byte count, SHA256
and Git blob identity, plus its Apache 2.0 license. This is an experimental
integration boundary, not a selected production SRAM or fabrication process.

## Clock and reset behavior

The upstream model samples commands on rising edges and performs memory
operations on falling edges. It also invalidates its read output after later
rising edges, including idle edges. The wrapper exposes completed read data
at the following rising edge and retains a copy for adapters that respond
later. Without that retention, a three-cycle adapter would capture unknown data.

Reset blocks macro commands and clears the wrapper's control and held-data
registers. It does not clear the array. Unwritten memory remains unknown in
four-state simulation and must be initialized before normal use.

`RAM_BYTES` must be a positive multiple of 8 KiB; non-power-of-two bank counts
are supported. The generic adapter rejects accesses outside the configured
array. `WASMETAL_SKY130_SRAM_MODEL` enables model-only delay parameters in
simulation. The physical interface instantiation does not pass those parameters.
The upstream `DELAY` and `T_HOLD` values are explicitly arbitrary model settings;
they are not characterized access times or evidence of a silicon clock rate.

## Repeating the checks

```sh
python3 tools/bootstrap.py
python3 tools/check_sky130_sram.py
```

The [complete report](verification/sky130-sram.json) covers six simulator runs:

| Array | Adapter read latency | Model read delay | Nonzero write masks | Simulators |
| --- | --- | --- | --- | --- |
| 8 KiB | 1 cycle | 9 ns | 65,535 | Icarus and Verilator |
| 16 KiB | 3 cycles | 3 ns | 65,535 | Icarus and Verilator |
| 24 KiB | 2 cycles | 5 ns | 255 | Icarus |
| 128 KiB | 3 cycles | 3 ns | 255 | Icarus |

Every run uses a 20 ns clock and a 1 ns output-hold setting. The first row
leaves just 1 ns between the modeled read arrival and the sampling edge.
An independent byte-array oracle checks **563,734 transactions** in total:
initial writes, reads across all words and banks, partial writes, invalid
addresses and masks, exact response cycles, held requests and reset recovery.
The Icarus runs additionally require an unwritten read to remain unknown;
Verilator's two-state behavior cannot establish that property.

Five deliberately damaged wrappers must fail: lost read retention, incorrect
byte lanes, incorrect banking, capture on the wrong transaction edge and
inverted macro clocks. A sixth check delays the model's read beyond the capture
window and must also fail. None of these controls changes the upstream model.

The runner verifies installed Icarus and Verilator package members against
the checksum-pinned packages. It records source and executable identities and
checks its inputs again after execution. The shared tool directory can contain
other packages; this is not an audit of the complete host compiler/runtime.
The [archive](verification/sky130-sram/index.json) retains the source, vendor
license, observations, generated test inputs and tool payload inventories.
A dedicated CI job repeats the matrix and preserves evidence on failure.

## Remaining integration

The default FPGA memory and the complete CPU's existing SRAM simulations are
unchanged. This campaign connects the real transaction adapter to the bank
wrapper; it does not run the Wasm CPU or official corpus against this macro.
The CPU's other memories have different port and clock contracts, described
in the [ASIC audit](ASIC.md), and still need suitable implementations.

Physical use requires compatible Liberty, LEF/GDS, power connections, clock
and timing constraints, memory placement, testing and signoff. The current
startup block's physical-routing experiments do not contain these SRAM arrays.
