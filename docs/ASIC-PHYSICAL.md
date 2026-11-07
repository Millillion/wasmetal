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

## Detailed routing and extraction

The functional result above covers binary behavior with zero cell delays
after placement, clock trees and global-routing repair. The separate detailed
route and extracted diagnostics below retain their own evidence and limitations.

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
database and retains its own results. It now [finishes with zero OpenROAD
routing-rule markers](verification/asic-route-extraction-summary.json) after
1,340 seconds. Completed iteration counts were 6,076, 4,021, 3,574, 1,493,
487, 225, 168, 97, 47, 47, 15, 3, 3 and 0. The final Verilog still has exactly
the same 4,183 functional cells and canonical pin connections as the verified
global-route circuit. No additional functional simulation is inferred from
that structural equality.

OpenRCX extracted 4,419 nets, 24,009 resistance segments, 24,009 ground
capacitances and 53,034 coupling capacitances. The extraction rules are pinned
to the same ORFS revision; its SKY130HD path resolves to the SKY130HS rules
file, and both that symlink identity and the resolved content are recorded.
At the SKY130HD TT, 1.8 V, 25 C cell corner with the trial's 100 ns clock and
block-interface constraints, setup slack is **+75.045525 ns** and hold slack
is **−0.008133 ns**. The selected slew, capacitance, fanout, pulse-width and
period report is empty. The antenna checker still reports **139 net and 148
pin violations**. Hold and antenna checks therefore remain open.

The [raw archive](verification/asic-route-extraction/index.json) preserves
73 artifacts, including the routed/extracted databases, SPEF, timing paths,
antenna reports, exact commands, source snapshots and licenses. All 47 bound
inputs were rechecked. The first extraction driver rejected a difference in
its broad Python-import snapshot caused by the new Wasm input code. The
revised check retains both snapshots and permits only those unexecuted test
functions to differ. Physical executable, package trees, resolved libraries,
launcher code and platform data match; four deliberate substitutions are
rejected. The initial rejection is retained too.

Zero router markers are separate from antenna checks, extracted timing and
signoff DRC/LVS. These results concern the startup/BIST/SRAM-adapter block;
they contain neither the full CPU nor a physical SRAM array. There is no
chip timing or fabrication-readiness claim.

## Hold, electrical and antenna repair

`tools/close_asic_startup_route.py` starts from that extracted route and runs
[`asic-startup-route-closure.tcl`](../tools/asic-startup-route-closure.tcl).
It repairs hold against the extracted parasitics, re-routes every signal and
clock net, and repairs slew and capacitance limits against the new global
routes. A second hold pass follows. It inserts antenna diodes before detailed
routing, then repeats diode repair and detailed routing against the actual
wires until the antenna checker is clean, up to five rounds.

The [completed closure](verification/asic-route-closure-summary.json) passes
every check the flow runs at the trial corner. It finishes with **zero router
markers**, **setup slack +75.049370 ns**, **hold slack +0.093747 ns**,
**no antenna violations** and an empty slew, capacitance, fanout,
pulse-width and period report. `check_setup` reports nothing, both supply nets
are fully connected, and placement is legal. The run took 2,656 seconds: the
first detailed route reached zero violations, and two post-route antenna
rounds reduced 21 antenna nets to 2, then to 0.

The netlist grows from 4,183 to 4,555 functional cells: 124 hold delay gates,
247 passive diodes (24 of them inserted after detailed routing), one
electrical buffer and eight upsized cells. The resizer's own summary messages
undercount the hold buffers. The archive counts edits by comparing the
netlists.

The [functional check](verification/asic-route-closure/reports/asic-route-closure-functional.json)
(`tools/check_asic_route_closure.py`) verifies the routed netlist itself.
Apart from diodes, its pin incidence is identical to the pre-detailed-route
netlist, and every diode is a passive input in both the pinned upstream and
Liberty-derived models. The routed circuit is acyclic. It passes inductive
equivalence over all 620 state points, a 12-cycle reset base and an
independent output-pin proof against the startup RTL. Its gate-level
simulation runs **50,513,199 clocks** with observations identical to RTL, and
all 98 active cell types match pinned upstream models. All twenty fault
controls are rejected: normalization, diode attachment, diode-model,
clock-tree, corrupted-SRAM and tie-cell faults.

Two earlier trials are kept for comparison. The first hold/antenna repair
reached +0.067417 ns hold slack. Its re-route detoured one weak driver's wire,
leaving one slew/capacitance violation and 15 antenna nets. A jumper-insertion
variant was interrupted during detailed routing and produced no result. The
[archive](verification/asic-route-closure/index.json) keeps 60 files: the
routed and extracted databases, SPEF, reports, logs, exact tool versions and
both trials' records.

These detailed-routing steps run locally, not in CI, because their baseline
route comes from archived diagnostic scripts. The router skips some LEF58
via-enclosure rules, so zero router markers is not signoff DRC.

## Remaining physical work

Process-corner timing closure, signoff DRC/LVS, power integrity, a real
SRAM macro and pad strategy, manufacturing test and the complete CPU remain
necessary. Timing so far uses one typical 1.8 V, 25 C library corner and the
trial 100 ns clock. No physical hardware has been tested.
