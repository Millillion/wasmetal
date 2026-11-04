# Direct integral floating-point rounding

The circuit in [rtl/wasmetal_fp_round.sv](../rtl/wasmetal_fp_round.sv)
implements binary32 and binary64 ceiling, floor, truncation and nearest-even
rounding directly in the IEEE encoding. Both FPU format units use it in place
of the former float-to-integer-to-float conversion path. The change is
combinational and preserves the interface and completion timing.

The last completed standalone timing report, from before the SIMD-selector
change, contains a 166.934 ns path from the falling-edge instruction RAM to a
rising-edge CPU register. It traverses the floating-point rounding conversion
logic. This motivated the change; it does not establish the critical path
or attainable frequency of a new CPU build. The
[trace analysis](verification/fp-round-timing-origin.json) identifies the
historical timing artifact and the contributing source locations.

## Circuit

The component has a two-bit mode: ceiling, floor, truncation, nearest-even.
NaNs return the same canonical NaN as the existing implementation. Infinities,
signed zero and values already large enough to be integral are handled
explicitly.

For magnitudes below one, the result is signed zero or signed one. In the
remaining range, an exponent-derived mask clears the fractional bits. The
discarded bits, sign and integer parity decide whether to add one. Exact halves
round to an even integer; a result of zero retains the input sign. The ordinary
branch's mask count is between 1 and the significand width minus one.

This removes a conversion to a signed 64-bit integer followed by a conversion
back to floating point. Conditional expressions retain uncertainty when a
control contains X/Z.

## Verification

Run:

```sh
python3 tools/bootstrap.py
python3 tools/check_fp_round.py
python3 tools/prove_fp_format.py
make test-fpu
```

The [recorded campaign](verification/fp-round-experiment.json) checks both
precisions:

- SAT proves equivalence for every binary input and all four modes against a
  frozen copy of the CPU's original format module. Its reconstructed source
  hash is checked before the proof. No floating-point values are excluded.
- Separate SAT proofs compare the actual ABC9 ECP5 mappings with the candidate
  RTL. Both mappings pass structural checks with no combinational cycles.
- An independent Python rational-arithmetic oracle supplies 73,728 binary
  vectors, spanning every exponent, both signs and all modes.
- Another 100,124 vectors exercise X/Z in data and control. For cases with up
  to two uncertain bits, the oracle enumerates every binary completion. Neither
  RTL nor the mapped circuit may assert a known bit that contradicts a possible
  result. Pessimistic unknowns are allowed. Whole-input unknown stress cases are
  included separately.
- Five deliberate defects per precision are rejected: rounding ties away,
  losing negative zero, inverting a mapped result bit, treating an unknown mode
  as false and treating an unknown NaN condition as false.

Every generated vector must be consumed. Reports bind the sources, tools,
circuits, oracle vectors, executables and proof diagnostics to their hashes.
CI repeats the complete component campaign and the integration proof.

The [complete format-interface proof](verification/fp-format-proof.json)
compares all 266 output bits for binary32 and all 426 for binary64 against the
frozen original format unit. Every input is symbolic, including all 64
operation encodings, signedness controls, integer inputs and arithmetic
results. This checks the new mode wiring and preservation of the other
operations. An incorrect mode offset must produce a real counterexample for
each precision. The [FPU campaign](verification/floating-point.json) also
passes 1,734,368 arithmetic and complete-unit comparisons, including conversions,
traps and reset interruption.

## Measured hardware cost

These are isolated ECP5 mappings, using the same synthesis tool and options.

| Precision | Original LUT4 | Direct LUT4 | Original CCU2C | Direct CCU2C |
|---|---:|---:|---:|---:|
| binary32 | 1,867 | 374 | 121 | 44 |
| binary64 | 3,150 | 739 | 139 | 63 |

The two instances total 1,113 LUT4 cells instead of 5,017. Neither uses block
RAM or DSPs. Whole-CPU resource sharing and mapping can change the savings.
The [whole-CPU synthesis comparison](verification/fp-round-synthesis.json)
measures the integrated effect, including global sharing and optimization:

| Configuration | Previous LUT4 | Direct-rounding LUT4 | Previous CCU2C | Direct-rounding CCU2C |
|---|---:|---:|---:|---:|
| Host-backed | 41,615 | 41,056 | 5,448 | 5,485 |
| Bounded | 41,800 | 41,401 | 5,458 | 5,501 |

Both retain 5,265 registers, 98 block-RAM primitives and 26 DSP primitives,
with unchanged capacities. These are synthesis primitive counts; physical
packing and routing must be measured separately.

The complete native corpus passes all 259 suites with
[zero](verification/core-rounding-native-zero.json) and
[three](verification/core-3.0-current.json) memory wait states. Both
[preserve every command cycle](verification/fp-round-native-comparison.json).
The new complete mapped CPU also passes [four focused scalar/SIMD suites](verification/fp-round-mapped-focused.json),
covering 5,352 execution assertions and 74 validation assertions. Its lookup
models pass [binary equivalence and 282,368 four-state checks](verification/fp-round-lut-model.json).
The complete mapped corpus, programmable-system comparisons and new physical
implementation are underway. No physical board has been tested.
