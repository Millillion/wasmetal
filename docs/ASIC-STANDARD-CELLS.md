# Experimental ASIC standard-cell checks

WasMetal's startup controller, memory self-test and SRAM adapter now pass
functional checks after mapping to SKY130HD standard cells. Independent
upstream Verilog also verifies the actual cell models used by the simulations.
This is a bounded subsystem experiment. It does not select a fabrication
process for the final CPU or establish physical timing.

## Inputs and reproducibility

`tools/asic_cells.lock.json` pins the typical 1.8 V, 25 C Liberty library and
platform configuration from OpenROAD-flow-scripts, plus the upstream license
texts. Downloads must match their byte count, SHA256 and Git blob hash.
`tools/asic_cell_models.lock.json` separately pins the upstream SkyWater
functional Verilog and primitive definitions. Both locks use complete commit
identifiers.

The platform configuration excludes 36 cell types, including special
power-isolation cells. The mapping-library helper removes exactly those groups
from the 428-cell library and verifies that every retained cell and all
non-cell library data remain byte-identical. There are 392 retained cells.
The first private mapping experiment selected excluded isolation cells and was
rejected; its synthesis exit status alone was insufficient evidence.

The library inputs come from the
[pinned OpenROAD platform](https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/tree/d056a2b304182bf76ff10653531165b1dd9848d4/flow/platforms/sky130hd).
The independent functional definitions come from the
[pinned SkyWater cell repository](https://github.com/fossi-foundation/skywater-pdk-libs-sky130_fd_sc_hd/tree/9cb2d7cb8ed4619094263614039a61b6b2d22a88).
The archive retains the cell library's Apache 2.0 license, upstream source
copyright notices and the OpenROAD build/run scripts' BSD 3-Clause license.
These third-party notices do not change WasMetal's project license.

## Independent cell behavior

```sh
python3 tools/check_asic_startup.py
python3 tools/check_asic_cell_models.py --asic-report reports/asic-startup.json
python3 tests/asic_cell_source_test.py
```

The [published result](verification/asic-startup-cell-models.json) checks all
69 cell types selected across the six startup configurations. The report binds
the generated netlists and their actual functional model files by hash. Icarus
compares those Liberty-derived definitions against upstream Verilog gates and
enabled primitive tables. The check requires matching scalar port inventories
and rejects unsupported stateful cells. Omitting `--asic-report` instead checks
fresh Liberty-derived definitions; it does not bind a circuit simulation.

All 1,115 binary combinational input vectors pass. The positive-edge flip-flop
also passes all 32 combinations of a known previous output, previous binary
data/clock levels and following binary data/clock levels. Sixty-four additional
checks verify that seeding and pretransition data changes produce the expected
state. A clock edge establishes the initial output; no power-on value is assumed.

Wrong tie-high logic, an inverted AND output and a falling-edge flip-flop must
all fail simulation. Seven source-inventory fixtures check the valid inventory
and reject omitted cells, unbound types, duplicate files, missing primitive
includes, altered source hashes and a moving upstream branch reference. Every
active include must be part of the pinned file inventory. Primitive black-box
definitions are not used.

The [initial cell-only archive](verification/asic-cell-models/index.json)
retains its original 67-type result. The [complete startup archive](verification/asic-startup/index.json)
adds the actual circuit models, both additional upstream definitions, testbench,
fault variants and logs. The source-inventory gate initially rejected the final
configuration's additional cell type; its pinned definition was added and the
complete independent comparison was then rerun.

## Complete startup circuit campaign

The [summary](verification/asic-startup-summary.json) and
[detailed report](verification/asic-startup.json) cover six parameter settings:

| SRAM bytes | Read latency | Response timeout |
| ---: | ---: | ---: |
| 16 | 1 | 9 |
| 80 | 3 | 11 |
| 272 | 7 | 10 |
| 131,072 | 3 | 11 |
| 80 | 3 | 5 |
| 80 | 3 | 2 |

RTL and standard-cell simulations produce exactly matching observations and
trace hashes over 59,107,887 clocks per model. The 128 KiB case accounts for
50,513,199 clocks and maps to 3,712 cells, including 620 flip-flops. The same
independent C++ SRAM oracle drives both simulations. Startup completion,
expected startup failures, resets and subsequent CPU-side memory requests are
checked; this harness does not instantiate the Wasm CPU or a physical SRAM.

Each configuration also passes inductive RTL-to-cell equivalence with explicit
FSM encoding maps. A separate 12-cycle reset proof checks the comparison points;
another reset proof compares output pins without assuming matching internal
state. Initial register values are undefined. Structural checks reject generic
or excluded cells, missing inputs, undriven bits, multiple drivers, altered
clocks and initialized state. Netlist normalization must preserve every cell
pin connection, and the flattened bit-level graph must have no combinational
cycle.

Fourteen deliberate circuit faults exercise these checks, including a rewired
tie cell rejected by both simulation and the independent reset proof, and a
corrupted SRAM read rejected by the unchanged simulation oracle. The first
attempt reached matching observations in all six configurations but stopped
when a fault-test build exposed a vector-alias warning. After checking that the
mutated circuit had no bit-level cycle, the waiver was restricted to that
specific warning. The entire six-configuration campaign was rerun. Its initial
failure and the complete successful rerun are both retained in the archive.

CI has a dedicated job for all six mappings, proofs, paired simulations, fault
controls and independent checks of the actual cell definitions. Logs and
generated circuits are uploaded even when a job fails. The local pass described
here does not imply that a newly queued CI run has completed.

## Limits

These checks cover binary functional behavior with zero cell delays. They do
not establish equivalent X/Z behavior, metastability handling, setup/hold time,
power-pin behavior or analog correctness. A Liberty corner is not a timing
closure result. The complete CPU, SRAM macros, placement, routing, clock tree,
power delivery, design-rule checks and foundry signoff remain separate work.
