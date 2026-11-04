# Memory startup and CPU ownership

`soc/asic/wasmetal_memory_startup.sv` runs the destructive
[memory self-test](MEMORY-SELF-TEST.md) once after each shared reset. It grants
the CPU access only after the complete test succeeds. This is an optional
component; the default CPU and FPGA images do not instantiate it.

## Interface and sequencing

The controller connects a CPU request port and the test master to one physical
memory port. Both use held requests, a completion response and a low-valid
release cycle. Reset the controller and its memory backend together. The backend
must support aligned 128-bit accesses and the configured `RAM_BYTES` capacity.

1. Reset immediately suppresses memory requests and CPU responses. A clocked
   reset clears test status and rearms the automatic test.
2. After reset deasserts, the test owns the memory. The CPU may hold a request
   pending, but receives no acknowledgement or read data during testing.
3. A successful test finishes all `80 * (RAM_BYTES / 16)` accesses, leaves the
   array zeroed and completes a release cycle before `cpu_enabled` rises.
4. The CPU then owns the port until the next reset. Requests and responses pass
   through without an added clock cycle. Holding valid after a completion still
   requires the backend's ordinary release protocol.
5. Any test failure prevents the handoff. A timeout keeps the outstanding test
   request active until its late response or a shared reset; the CPU cannot
   mistake that response for its own transaction.

`test_busy`, `test_done`, `test_failed`, the completed-operation count and the
first-failure diagnostics expose the underlying test status. Failure remains
latched until reset. CPU transaction faults after a successful handoff pass
through normally and do not restart the test.

Every shared reset starts another destructive test. There is no warm-reset
retention mode or periodic background testing. The test covers the array on this
port; instruction and metadata memories elsewhere in the CPU are outside its
scope.

## Memory bridge integration

The existing memory bridge starts clearing memory immediately after reset and
has a short transaction timeout. Hold that bridge in reset while `cpu_enabled`
is false. Keep the startup controller and SRAM adapter on the original shared
reset, so they can run the test independently. Report `test_failed` to the boot
controller. After a successful test, release the bridge and let its normal
initialization and prepared-image loading proceed.

The optional controller is verified below. A separate complete-CPU test binding
with this reset sequencing is being evaluated; its execution results are not
part of the component reports.

## Verification

```sh
python3 tools/check_memory_startup.py --mapped
python3 tools/check_memory_startup_four_state.py
python3 tools/prove_memory_startup.py
```

The [component summary](verification/memory-startup-summary.json) records six
configurations with 16-byte, 80-byte, 272-byte and 128 KiB arrays and one-, three-
and seven-cycle SRAM reads. Two deliberately short response deadlines exercise
write and read timeouts. An independent C++ oracle checks every March command,
normal CPU transaction, byte enable and stored value at the actual SRAM adapter's
macro pins. The CPU request source is a transaction generator.

RTL and ECP5 functional mapping have identical observations and trace checksums
over 59,107,887 clocks per model. The checks observe 2,760 successful handoffs,
266 completed failure cases, 11,237 CPU responses and 720 expected CPU address or
mask faults. They also cover 5,614 resets, 408 stale SRAM read responses delivered
across reset, and 36,028 clocks with CPU valid held after completion. The small
arrays are reset at every clock of a complete startup/handoff sequence. SRAM
contents and pending read responses survive those resets.

Eight simulation fault controls must fail, including early or failed-test
handoff, repeated testing, leaked test responses, wrong CPU masks and read data,
retained ownership during reset, and a corrupt SRAM model. The
[four-state checks](verification/memory-startup-four-state.json) also reject three
faults and verify that X/Z read data blocks handoff while retaining the observed
bad value. This is simulation diagnosis, not electrical metastability detection.

Four configurations pass [unbounded safety proofs](verification/memory-startup-proof.json)
with the actual test master and its sequence-accounting invariants. They prove
complete-test handoff, ownership retention, request stability and response
isolation. The environment supplies an initial shared reset, arbitrary binary
memory responses, and CPU requests held stable until response or reset. Four
deliberately broken controllers must fail these proofs. No response fairness,
eventual completion or SRAM storage correctness is assumed or proved by these
protocol checks.

The [raw archive](verification/memory-startup/index.json) contains source snapshots,
mapped circuits, observations, proof scripts and fault diagnostics. The combined
startup controller, test master and SRAM adapter use 620 ECP5 registers and
1,751 LUT4s in the 128 KiB, three-cycle-read, eleven-cycle-timeout configuration;
this excludes the SRAM array and the CPU. These are functional mapped results,
not ASIC standard-cell area, timing signoff or physical-board validation.

The default builder still selects the identical
[47 RTL sources](verification/memory-startup-source-inventory.json), and the default
programmable system passes lint. CI runs the component simulation, four-state
checks and proofs in a dedicated memory-startup job.
