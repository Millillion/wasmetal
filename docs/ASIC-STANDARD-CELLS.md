# Experimental ASIC standard-cell checks

WasMetal now has pinned SKY130HD library inputs and a separate check of the
binary behavior of the cell models. This establishes a reference for ASIC
synthesis experiments. It does not select a fabrication process for the final
CPU or provide a physical implementation.

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
python3 tools/check_asic_cell_models.py
python3 tests/asic_cell_source_test.py
```

The [published result](verification/asic-cell-models.json) checks 67 cell types
selected during the startup-controller synthesis experiments. Yosys derives one
set of functional definitions from Liberty. Icarus compares those definitions
against upstream Verilog gates and enabled primitive tables. The check requires
matching scalar port inventories and rejects unsupported stateful cells.

All 1,067 binary combinational input vectors pass. The positive-edge flip-flop
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

The [raw archive](verification/asic-cell-models/index.json) includes the pinned
inputs, upstream sources, generated models, testbench, fault variants and logs.
CI runs the model comparison and source-inventory fixtures. A separate startup
circuit campaign is still running; this report does not claim that campaign
has passed.

## Limits

These checks cover binary functional behavior with zero cell delays. They do
not establish equivalent X/Z behavior, metastability handling, setup/hold time,
power-pin behavior or analog correctness. A Liberty corner is not a timing
closure result. The complete CPU, SRAM macros, placement, routing, clock tree,
power delivery, design-rule checks and foundry signoff remain separate work.
