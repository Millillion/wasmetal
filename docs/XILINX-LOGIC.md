# Checking 7-series logic models

A lookup table, or LUT, stores a small Boolean truth table. Xilinx 7-series
logic mapping uses LUTs with one through six inputs. The original Yosys
simulation models select a truth-table bit through a tree of conditional
expressions. A private simulation copy can use a direct table lookup for known
selectors and retain the original expression whenever a selector contains X
or Z. This changes simulator work; it does not change the synthesized circuit.

The [recorded verification](verification/xc7-luts.json) establishes that identity
for every binary truth table and selector at all six widths. The proof moves
each model's `INIT` parameter into an unconstrained input, preserving its logic.
It therefore covers all 64 table bits of LUT6, rather than sampling a few
particular configurations. An inverted output at each width must fail its
proof.

An independent Python oracle enumerates all known addresses consistent with
each selector. It returns a known value, or Z, only when every possible entry
agrees; otherwise it returns X. Both the original and optimized model must
match that oracle. The local run includes every distinct table in both the
board-rate and accelerated-UART whole-system netlists, along with constant
tables and single X/Z table-bit patterns:

- Icarus and Verilator each pass 183,664 binary comparisons per model.
- Icarus passes 11,811,032 four-state comparisons per model, covering every
  selector combination for the selected tables.
- Eleven controls reject six inverted outputs, an unsafe lookup with unknown
  selectors, a corrupted oracle, and truncated, extra or malformed input.

The simulator inputs, compiler identity, generated fixtures, traces and logs
are hashed in the receipt. HDL warnings remain fatal except for generated
fixture filenames and deliberately unused signals. The [archived evidence](verification/xc7-luts)
includes the original proof logs, counterexamples, fixture sources and traces;
large text traces are compressed without changing their contents. Its index
records both original and archive hashes.

After the complete-system estimate:

```sh
python3 tools/check_xc7_luts.py
```

To also include the accelerated-UART mapping's distinct truth tables:

```sh
python3 tools/check_xc7_luts.py \
  --netlist build/xc7-system/mapped.json \
  --netlist build/xc7-accelerated/mapped.json
```

CI repeats the proofs and the current system mapping's table regression. The
table-specific comparison count can differ from the two-netlist local run.
These component checks do not establish complete CPU correctness, board timing
or physical hardware operation. The [RAM](XILINX-MEMORY.md) and
[DSP](XILINX-DSP.md) checks have their own scopes.
