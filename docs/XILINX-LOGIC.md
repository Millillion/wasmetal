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

## Carry chains

The [CARRY4 regression](verification/xc7-carry.json) compares the Yosys model
with the [unmodified Xilinx source](https://github.com/Xilinx/XilinxUnisimLibrary/blob/1c8e05fd1e9a79ceb8b996a0996674122eed086f/verilog/src/unisims/CARRY4.v).
The vendor file's Git blob, SHA-256 identity and original notices are retained.
A SAT proof establishes equivalence for every binary input. Both models also
pass an independent Python oracle for all 1,024 binary combinations. Verilator
checks the Yosys model with the same split-carry scheduling configuration used
by the complete system.

A separate C++ test drives the primitive's actual top-level input ports,
checking all 1,024 complete words and every intermediate value while updating
each bit individually: 11,264 observations. Eleven controls reject inversions
of each of the eight outputs, an incorrect carry-input merge in Icarus and
the C++ simulation, and that same arithmetic error in the formal proof.

Four-state equivalence does **not** hold between these two library models.
For example, Xilinx models a pull-down when `CI` or `CYINIT` is Z; Yosys does
not. Yosys uses conditional selection, while Xilinx uses gates whose unknown
propagation differs. Each model instead passes its own independently computed
oracle for every one of the 1,048,576 combinations of 0, 1, X and Z at its ten
inputs. Outputs differ between the models on 415,001 combinations. The receipt
records examples; this difference is not counted as a successful equivalence
check. The complete Verilator system simulations use two-state behavior.

The [evidence archive](verification/xc7-carry) also retains a development
diagnostic: a timed SystemVerilog fixture that assigned input bits in a loop
produced stale outputs under pinned Verilator 5.020. The final timed fixture
assigns the complete word, and the independent C++ port driver passes both
whole-word and individual-bit updates. The failing diagnostic is not counted
as a passed check. Unknown values are compared directly; even XOR with zero
would incorrectly turn Z into X in a test wrapper.

```sh
python3 tools/check_xc7_carry.py
```

CI repeats the proof, simulation oracles and negative controls. These remain
untimed component checks, without a physical timing or silicon claim. The
Yosys library notice is preserved with both logic evidence archives.

## Muxes and inverters

The [mux/inverter receipt](verification/xc7-muxes.json) and
[evidence archive](verification/xc7-muxes/index.json) cover `MUXF7`, `MUXF8`
and `INV` against their unmodified, pinned Xilinx sources. All three binary
equivalence proofs pass. Independent truth-table checks cover every binary
input in Icarus and Verilator, and every four-state input in Icarus: 18 binary
and 132 four-state observations per library model.

For an X or Z selector, the vendor mux's procedural `if` chooses input zero.
Yosys conditionally merges the two inputs. Each mux differs on 18 of its 64
four-state combinations; both pass their separate Python oracles. The inverter
agrees for all four input states. Deliberately pretending that the muxes are
four-state equivalent is rejected. Eleven controls also cover incorrect input
wiring, flipped outputs and truncated, extra or malformed trace data.

```sh
python3 tools/check_xc7_muxes.py
```

CI runs these checks. See [state primitives](XILINX-STATE.md) for the distinct
clocked-model verification scope.
