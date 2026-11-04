# Complete programmable 7-series CPU simulation

The complete `wasmetal_loadable` core-clock netlist now executes uploaded
programs in Verilator. This extends the component checks to the CPU, runtime
storage, upload protocol and result transmitter together. It excludes a board's
clock/reset circuitry, pin constraints, placement and physical timing.

## Recorded results

The [initial evidence bundle](verification/xc7-system-initial/index.json)
preserves these completed runs and the simulator identities:

| Configuration | Completed evidence |
| --- | --- |
| Native RTL, 81 clocks per UART bit, upload timeout 2,000,000 | All 35 programmable integration cases pass. |
| Xilinx mapped circuit, 4 clocks per bit, timeout 4,096, original LUT models | `answer` and `program-address-boundaries` pass. UART bytes, every recorded clock count, prepared image hashes and CPU results match the corresponding RTL cases exactly. Eight comparison faults are rejected. |
| Xilinx mapped circuit, 4 clocks per bit, proven faster LUT models | All 35 integration cases pass. Every complete case observation matches native RTL exactly, and all fifteen comparison faults are rejected. |
| Xilinx mapped circuit, 81 clocks per bit, proven faster LUT models | One complete upload/execution is running against the finished board-rate RTL reference. |

The original-library `answer` test takes 2,259,198 core clocks, including
upload and response. Its CPU invocation returns 42 in 53 CPU cycles. The
clock comparison includes commit and first-result timing, rather than only
checking the final answer.

The [complete campaign archive](verification/xc7-system-complete/index.json)
retains all six mapped partitions, their logs, the original native reference,
the original campaign driver/plan and the
[final comparison](verification/xc7-system-complete/reports/xc7-system-complete.json).
It includes reset/recovery scenarios, memory and program boundaries, and the
watchdog. All 48 shared model inputs agree. The comparison rechecked both
actual simulator executables and all recorded inputs before accepting the run.

These are **bounded programmable integration tests**, distinct from the
259-suite official Wasm corpus run against the host-backed RTL and ECP5
mapped models. They do not establish that the official corpus has run on
this Xilinx circuit, nor that a physical board works.

## Model construction and identity

`build_xc7_gate_sim.py` consumes the exact JSON circuit from the corrected
[system estimate](research/xc7-system-estimate.json). It checks RAM address
pins, DSP configurations, the primitive inventory and the six asynchronous
HardFloat reset consumers before exporting Verilog. Canonical library
declarations are reloaded before export so that primitive parameters and
port widths are preserved.

Simulation uses the checked [block-RAM models](XILINX-MEMORY.md), the
[explicit DSP carry connections](XILINX-DSP.md), and Yosys functional models
for the other primitives. These are untimed functional models. HDL warnings
remain fatal except for specific generated-library conventions; the shared
synchronous/asynchronous reset alias is reviewed and narrowly identified.
Compiler style exceptions apply only to generated C++, with the unused DSP
temporary exception limited to generated DSP translation units.

`estimate_xc7_accelerated.py` changes exactly two elaboration parameters:
`UART_TICKS=4` and `UPLOAD_TIMEOUT_CYCLES=4096`. All other synthesis commands
and parameters are preserved. The checker verifies unchanged storage capacity
and top-level ports. This is a separately synthesized circuit, not a claim
that the 81-clock UART was exercised at four clocks per bit.

`accelerate_xc7_sim.py` changes only the simulator's LUT expressions, using
the [proved lookup transformation](XILINX-LOGIC.md). The synthesized circuit
is unchanged. It requires proofs for all six LUT widths, the oracle checks,
all negative controls, and inclusion of the actual circuit's truth tables.
It also rechecks the original simulator, library modules and generated inputs.

Every comparison rechecks actual executable hashes and build inputs before
and after use. The older native builder parses nine unused modules for
alternate memories, instruction codecs and board wrappers. The comparison
records this explicit allowlist; all execution sources must match, and any
other missing or changed source is rejected. Six CI metadata tests exercise
coverage, identity, parameter, source and circuit-binding failures. They
are not counted as CPU execution tests.

The first board-rate attempt with original LUT models was deliberately
interrupted after the proven faster model became available. Its partial
report and interruption log remain in the bundle. It produced no complete
test result, and is neither a pass nor an observed CPU functional failure.
The replacement permits six hours of wall time for the single upload;
the hardware parameters and simulator cycle limits are unchanged.

## Reproduction

After bootstrapping the pinned tools, run the prerequisites in this order so
the recorded component identities refer to the current synthesis output:

```sh
python3 tools/check_xc7_memory_mapping.py
python3 tools/check_xc7_ram_models.py
python3 tools/estimate_xc7_system.py
python3 tools/check_xc7_dsp.py
python3 tools/build_xc7_native_sim.py --jobs 2
python3 tools/check_loadable.py --binary build/xc7-native-sim/obj/Vwasmetal_loadable --report reports/xc7-loadable-rtl.json
python3 tools/build_xc7_gate_sim.py --jobs 2
python3 tools/estimate_xc7_accelerated.py
python3 tools/build_xc7_gate_sim.py --jobs 2 --estimate reports/xc7-accelerated-estimate.json --netlist build/xc7-accelerated/mapped.json --directory build/xc7-accelerated-gate-sim
python3 tools/check_xc7_luts.py --netlist build/xc7-system/mapped.json --netlist build/xc7-accelerated/mapped.json
python3 tools/accelerate_xc7_sim.py --simulator build/xc7-accelerated-gate-sim/obj/Vwasmetal_loadable --directory build/xc7-accelerated-gate-fast --jobs 2
python3 tools/accelerate_xc7_sim.py --simulator build/xc7-gate-sim/obj/Vwasmetal_loadable --directory build/xc7-board-rate-gate-fast --jobs 2
python3 tools/check_xc7_board_rate.py
```

The original-library smoke comparison consumes a completed native reference
from `build_loadable_sim.py` and these two mapped cases:

```sh
python3 tools/check_loadable.py --binary build/xc7-accelerated-gate-sim/obj/Vwasmetal_loadable --case answer --case program-address-boundaries --no-recovery --report reports/xc7-accelerated-mapped-smoke.json
python3 tools/check_xc7_smoke.py
```

The full mapped campaign uses the six existing `loadable_ci.py` partitions,
with recovery scenarios in partition zero. `check_xc7_system.py` requires
every case exactly once and checks the complete observations against the RTL
reference. Its fifteen deliberate comparison faults must also be rejected
before a full-regression receipt can be written.

Build receipts describe an untested executable at build time. Test results
live in separate receipts; a successful run does not rewrite its build identity.
