# 7-series state primitive verification

The [flip-flop receipt](verification/xc7-flops.json) checks every flip-flop
type used by the complete programmable circuit: `FDRE`, `FDRE_1`, `FDSE` and
`FDCE`. The [archive](verification/xc7-flops/index.json) contains the actual
fixtures, independent oracle traces, logs and negative controls. Vendor files
are unmodified and pinned to the same Xilinx revision as the RAM/DSP models.

## Known inputs and startup

With initial states zero and one, all four types pass 35,328 settled
observations per model in Icarus, using both the Yosys and vendor libraries.
The Yosys models pass the same observations in Verilator. The regression
preloads each prior binary state through the real data/clock pins, then checks
every combination of old/new binary clock, reset/set/clear, enable and data.
It also applies reproducible random sequences. Data and controls settle before
active clock changes, with observations taken after the vendor's unit delays.

The tests check rising and falling clock edges, reset/set priority over enable,
asynchronous clear without a clock, disabled-state retention and initial
values. Vendor global reset is explicitly pulsed after time zero to establish
`INIT`; later global-reset behavior is outside this regression. Separate
unknown-startup checks reject replacing X with zero.

The base circuit contains 6 asynchronous-clear flip-flops, 6,677 ordinary
synchronous-reset flip-flops, 192 falling-edge flip-flops and 76 set flip-flops.
The locally recorded audit also covers the accelerated-UART circuit. Parameter
or port changes outside the tested configuration are rejected.

## Four-state scope

The library models have different semantics for unknown enables, controls and
data. They are not asserted to be four-state equivalent. Independent Python
state/event oracles check 43,520 Yosys observations and 34,304 vendor
observations, with the exact stimulus and scope retained per check.

For the synchronous flip-flops, both models exercise X/Z controls and data.
For `FDCE`, Yosys is checked with X/Z clear, enable and data. The vendor oracle
checks X/Z enable/data with clear held to binary values. A second Yosys run
uses that same restricted trace, allowing a direct comparison. Clock inputs
always remain binary; these tests do not model metastability or physical
setup/hold behavior.

## Vendor asynchronous-clear diagnostic

The pinned vendor `FDCE` has a separate, reproducible simulation edge case.
Changing `CLR` from Z to zero produces a zero-time X pulse on its internal
clear expression in the pinned Icarus simulator. With enable high and data
zero, the output can change from one to zero while the clock stays low.
An independent oracle based only on settled clear levels does not describe
that behavior.

The regression preserves and requires the
[minimal diagnostic](verification/xc7-flops/vendor-unknown-clear.sv) and its
[observed log](verification/xc7-flops/vendor-unknown-clear.log). This is
characterization of a simulation model, not a hardware timing prediction or
a general unknown-clear oracle. The vendor's full unknown-clear behavior is
explicitly marked unverified. The unused vendor expectation column in the
Yosys-only full-clear trace is X rather than a claimed prediction.

## Fault checks and reproduction

Eight semantic/parser controls reject the wrong clock edge, synchronous
replacement of asynchronous clear, enable-gated reset, wrong startup value,
zeroed unknown startup, and truncated/extra/malformed traces. Four inventory
controls per netlist reject unsupported inversion, unsupported initialization,
unknown parameters and changed port widths. The local two-netlist run rejects
all sixteen controls; CI checks the base netlist and its twelve controls.

```sh
python3 tools/check_xc7_flops.py --netlist build/xc7-system/mapped.json --netlist build/xc7-accelerated/mapped.json
```

Verilator generation/build uses one worker. The pinned tool aborted internally
after one parallel generation/build attempt; that attempt was not accepted as
a passing compilation. HDL warnings remain fatal except for the extracted
library's unnamed generate blocks, initial nonblocking-assignment convention,
filenames and unused signals.

These are independent simulation-oracle checks, not a sequential formal proof
or a substitute for complete-system tests, physical timing closure or testing
an FPGA.
