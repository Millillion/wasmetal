# Integral floating-point rounding experiment

The candidate in
[experiments/rounding/wasmetal_fp_round.sv](../experiments/rounding/wasmetal_fp_round.sv)
implements binary32 and binary64 ceiling, floor, truncation and nearest-even
rounding directly in the IEEE encoding. It is an isolated component; the
default CPU still uses its existing HardFloat integer-conversion path.

The last completed standalone timing report, from before the SIMD-selector
change, contains a 166.934 ns path from the falling-edge instruction RAM to a
rising-edge CPU register. It traverses the floating-point rounding conversion
logic. This motivates the experiment; it does not establish the critical path
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
CI repeats the complete component campaign.

## Measured hardware cost

These are isolated ECP5 mappings, using the same synthesis tool and options.

| Precision | Original LUT4 | Candidate LUT4 | Original CCU2C | Candidate CCU2C |
|---|---:|---:|---:|---:|
| binary32 | 1,867 | 374 | 121 | 44 |
| binary64 | 3,150 | 739 | 139 | 63 |

The two instances total 1,113 LUT4 cells instead of 5,017. Neither uses block
RAM or DSPs. Whole-CPU resource sharing and mapping can change the savings.
No new CPU frequency, routed implementation or physical-board result is
claimed by this component experiment.

Integration must preserve the FPU's interfaces and completion timing, repeat
the complete CPU regressions, and measure the resulting full circuit and
physical implementation.
