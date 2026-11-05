# Experimental ASIC physical preparation

WasMetal has a reproducible tool-input check for an experimental SKY130HD
physical flow. It verifies the inputs needed for placement, clock trees and
routing. It does not establish a completed physical implementation.

```sh
python3 tools/asic_physical_tools.py
```

The command targets Ubuntu 24.04 on x86-64. It keeps OpenROAD and two additional
runtime packages in the project's private cache. Other OpenROAD runtime
dependencies must already be available on the host; missing libraries cause a
failure. CI installs those prerequisites on its disposable runner. The local
verification did not install system packages.

The [lock](../tools/asic_physical.lock.json) pins OpenROAD
`26Q2-1164-g08f67ee5ec`, its Ubuntu package, the two extra runtime packages and
seven physical platform files. OpenROAD comes from the download service linked
by the [official installation documentation](https://openroad.readthedocs.io/en/latest/user/Build.html).
Its [source revision](https://github.com/Precision-Innovations/OpenROAD/tree/08f67ee5ecd14db5a42be8c610bbfd1ccf079299)
is recorded. The platform files use the same OpenROAD-flow-scripts revision as
the [standard-cell functional reference](ASIC-STANDARD-CELLS.md).

The checker verifies package sizes and SHA256 values, every extracted file and
symlink, the executable hash and reported version. It rejects extra files in
the private package directories and checks physical-source byte counts,
SHA256 values and Git blob identities. Fresh extraction is verified in a
temporary directory before becoming the active cache. Source and resolved
shared-library identities are checked again before a successful report.

The [local report](verification/asic-physical-tools.json) covers 11,632 package
files, seven physical platform inputs and 133 resolved shared libraries. The
[archive](verification/asic-physical-tools/index.json) retains the source locks,
physical inputs, license notices and verification logs. Binary packages are
identified by their hashes and download URLs; they are not redistributed in
the archive. A failed check removes the previous output report.

The OpenROAD package hash was pinned from its first HTTPS download. This is
neither a vendor-signature attestation nor proof that rebuilding its source
produces that binary. Host runtime libraries are fingerprinted, rather than
assumed identical across computers. The tool-input CI job is separate from
functional and physical circuit verification.

These platform inputs do not select the final CPU's fabrication process.
SRAM macros, pads, manufacturing test, full-chip verification and foundry
signoff remain further work.

## Startup functionality after physical changes

```sh
python3 tools/check_asic_startup.py
python3 tools/check_asic_cell_models.py --asic-report reports/asic-startup.json
python3 tools/check_asic_physical_startup.py
python3 tests/asic_cell_source_test.py --cell-lock tools/asic_physical_cell_models.lock.json
```

The [published summary](verification/asic-physical-startup-summary.json) and
[complete report](verification/asic-physical-startup.json) cover the startup
controller, memory self-test and SRAM adapter with 128 KiB, a three-cycle read
latency and an eleven-cycle response timeout. This subsystem contains neither
the Wasm CPU nor a physical SRAM array.

The flow verifies the preceding six-configuration startup report and its
inputs, binaries and observations. It re-emits the reference circuit from its
hash-bound JSON, imports both Verilog representations, and requires identical
cell types, parameters and complete pin connectivity. Wire aliases may differ;
a deliberately rewired reference must fail this comparison.

OpenROAD places the cells, builds the clock tree, repairs signal and hold
paths, and performs global routing with estimated parasitics. The initial
floorplan uses 35% utilization. The experimental clock constraint is 100 ns,
with explicit input/output delays, driver strength, output loads, clock
transition and uncertainty. These are experiment assumptions, not measured
performance or a closed chip timing specification.

The resulting circuit has 4,183 functional cells and 620 flip-flops. Its 1,070
physical tap cells have no digital connections; only those empty instances
are removed from the functional model. Every surviving cell pin and top port
must remain unchanged. Structural checks cover all cell inputs and drivers,
and the flattened bit-level graph must have no combinational cycle.

All 620 state-instance names are preserved. Every clock path must lead back to
the original primary clock through approved non-inverting clock buffers. The
observed paths contain two or three buffers. Nine faults exercise this audit,
including wrong clocks on each flip-flop strength, inversion, feedback,
multiple drivers, missing or wide clock pins, and changed state identities.
Clock wiring is checked explicitly before synchronous equivalence; that proof
alone is not evidence of a correct clock tree.

All 1,267 state/output comparison points pass one-step induction between the
encoded circuits, followed by an independent twelve-cycle reset base with
undefined initial state. A separate reset proof compares current RTL and the
modified circuit's output pins without assuming matching internal state. The
preceding RTL-to-standard-cell proofs provide the other part of the equivalence
chain. The unchanged C++ SRAM oracle then produces exactly matching observations
and trace hashes over **50,513,199 clocks**. Fifteen circuit fault controls pass,
including rejection of an observable wrong tie-cell connection and a corrupted
SRAM read.

The [independent cell report](verification/asic-physical-startup-cells.json)
binds the exact 98 functional cell definitions used by this simulator. All
1,035 combinational input vectors, 96 binary flip-flop transitions and 192
seed/hold checks pass against pinned upstream Verilog. Wrong clock polarity is
tested separately for each of the three flip-flop strengths; all five model
faults are rejected. The source-inventory fixtures pass for both the original
and expanded cell inventories.

CI runs this flow after the complete startup mapping campaign and preserves
circuits, proofs, physical databases and observations even on failure. The
[raw archive](verification/asic-physical-startup/index.json) retains the local
evidence and earlier incomplete attempts. A direct RTL/FSM-map comparison
crashed Yosys during construction; comparing every shared internal wire then
exceeded its 600-second limit. The accepted proof preserves every state Q and
output port as a comparison point, with a separate reset base. Its circuit
and simulation inputs are unchanged by that proof strategy.

## Routing and timing remain open

The accepted result above covers binary functionality with zero cell delays
after placement, clock trees and global-routing repair. It does not include
a completed detailed route or extracted timing.

The first detailed-routing trial stopped at its 1,200-second limit. Completed
iterations reported 6,132, 3,724 and 3,689 violations; the next iteration was
still running. No final routed database was produced. The logs and exact
scripts are retained, including earlier command-compatibility failures.
A [completed bounded diagnostic](verification/asic-routing-diagnostic-summary.json)
ran iterations zero through three in 1,133 seconds. Its completed iteration
counts were 6,076, 4,021, 3,574 and 1,493 violations. The final marker file
contains 1,080 shorts, 402 metal-spacing violations, nine cut-spacing
violations, one minimum-hole violation and one cut short. The route command
returned success despite these violations, so its exit status alone cannot
establish an acceptable layout.

The [archive](verification/asic-routing-diagnostic/index.json) retains the
routed database, DEF, Verilog, constraints, violation markers, input identities
and logs. The Verilog preserves all 4,183 functional cells and exact canonical
pin incidence relative to the verified global-route circuit. Only the 1,070
physical tap cells with no digital connections are removed for that comparison.
Logical netlist equality cannot establish physical connectivity while shorts
remain. No additional RTL simulation or timing pass is inferred from it.

A separate attempt now permits sixteen as the final routing iteration, with
four threads and an 80-minute limit. It starts from the same global-route
database and retains its own results. It has now finished. Its extracted
timing and antenna findings are being checked before publication; no accepted
physical implementation is claimed.

Global routing supplies coarse paths and estimated parasitics. Detailed routing,
extracted timing, setup/hold closure across appropriate process corners,
antenna checks, signoff DRC/LVS, power integrity and a real memory/pad strategy
remain necessary. No physical hardware has been tested.
