# Checking 7-series memory mapping

WasMetal's pinned Yosys 0.33 library contains a real data-routing defect in its
72-bit simple dual-port block-RAM mapping. A small synthesized memory loses
written data bits when simulated with Xilinx's original RAMB36E1 model.
The generic RTL passes the same independent trace. The corrected mapping also
passes it. This finding concerns the exploratory Xilinx flow; ECP5 uses its own
technology library and synthesis recipe.

## The correction

RAMB36E1 has separate data and parity-data pins. A mapper can use both kinds of
pins for ordinary stored bits; these bits are not necessarily an error-checking
code. In 72-bit mode the pinned mapping mistakenly connects the upper four
parity-data inputs to the lower four bits:

```verilog
.DIPBDIP(PORT_W_WIDTH == 71 ? DIP[7:4] : DIP[3:0])
```

The width check must be `72`. This is also the condition in the checked
[upstream Yosys mapping](https://github.com/YosysHQ/yosys/blob/24471b847a1c90b6b7a0e0535f15ea48b477d5b4/techlibs/xilinx/brams_xc6v_map.v).
Structural synthesis checks do not detect the wrong connection, which is why
resource estimates alone could not establish functional correctness.

`tools/xc7_memory_mapping.py` verifies five pinned mapping-library hashes and
creates a private overlay with that parity correction. Its commands preserve the
other xc7 memory-mapping options from
[Yosys 0.33](https://github.com/YosysHQ/yosys/blob/yosys-0.33/techlibs/xilinx/synth_xilinx.cc).
The installed tools and libraries are unchanged. The system estimator uses the
overlay and records its input and output hashes. A changed library requires
review instead of silently applying a text substitution to unfamiliar code.

The overlay also follows the RAMB36E1 address-pin guidance in
[AMD UG473, pages 30 and 38](https://docs.amd.com/api/khub/documents/9gZGbqBxtlKXxBfkBt~lAg/content).
Non-cascaded RAM uses a 16-bit address connection with unused pins held high.
The old SDP expression produced 17 bits, losing its intended high constant
when connected to the 16-bit primitive port. Functional simulation ignores
that unused bit, so successful data comparisons did not catch the discrepancy.
The new expressions preserve active address bits and drive the unused pins
high. A separate structural audit checks exact port widths and constants;
18 deliberate pin/configuration mutations must be rejected. Cascaded RAM and
unsupported port widths require review. This check complements simulation.

## Independent verification

[The recorded regression](verification/xc7-memory-mapping.json) runs the same
26,028 operations against generic RTL and technology-mapped netlists. Icarus
simulates the block RAM using the unmodified, Apache-licensed
[Xilinx Unisim sources](../third_party/xilinx-unisim/README.md), whose original
Git blob identities and SHA-256 hashes are checked before and after the run.
The preserved upstream README identifies that library with Vivado 2020.1.

| Logical width and depth | Physical primitive | Mode | Operations per model |
|---|---|---|---:|
| 9 bits × 2,048 words | RAMB18E1 | True dual port | 8,268 |
| 18 bits × 2,048 words | RAMB36E1 | True dual port | 8,308 |
| 36 bits × 1,024 words | RAMB36E1 | True dual port | 4,308 |
| 36 bits × 512 words | RAMB18E1 | Simple dual port | 2,260 |
| 72 bits × 512 words | RAMB36E1 | Simple dual port | 2,884 |

The independent Python oracle supplies expected values. The test reads every
initialized address, exercises walking bits and their complements, applies
every combination of nine-bit write-lane masks, writes and rereads every
address, checks disabled reads and writes, and checks enabled and disabled
output resets. It compares outputs before, after and between active edges.
Resetting the output must preserve stored data. Unexpected X values fail the
four-state comparisons; unexpected simulator diagnostics also fail the run.

Six negative controls must fail: the actual uncorrected mapper, ignored write
enable, ignored lane mask, ignored read enable, ignored output reset and an
aliased read-address bit. The original defect is reproduced by real synthesis
and the vendor model, without modifying the reference model or its result.
The address-pin audit passes alongside all of those data checks, and all 18
of its structural negative controls are rejected.

After tool bootstrap:

```sh
python3 tools/check_xc7_memory_mapping.py
python3 tools/estimate_xc7_system.py
```

The regression writes `reports/xc7-memory-mapping.json` and preserves generated
HDL, netlists, expected traces and logs under `build/xc7-memory-mapping/`.
Concurrent runs in that directory are rejected. CI runs the memory regression
before the system estimate and retains both sets of artifacts.

## Scope

This is component verification for the five memory geometries used by the
exploratory system mapping. Read and write clock edges are separated by at
least 10 ns in this test. It does not establish collision behavior, clock
apertures, physical timing, DSP correctness or complete Xilinx CPU correctness.
The Yosys library's empty block-RAM shells are excluded from simulation.

Earlier uncorrected Xilinx resource estimates remain historical size
measurements, not deployable or functionally verified netlists. The corrected
[complete-system synthesis](research/xc7-system-estimate.json) passes its
structural check and verifies 340 address-pin constants across all 28 RAMB36E1
cells. It contains 50,964 logic LUT primitives, 6,951 flip-flops, 29 DSPs,
136 RAMB18E1 and 28 RAMB36E1 cells, plus 22 RAM64M distributed-memory cells.
Complete Xilinx system simulation,
board clock/reset and memory integration, implementation timing and physical
board tests remain required before claiming a working 7-series port.
