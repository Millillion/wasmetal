# SDR SDRAM controller

`wasmetal_sdram_memory` is a separate 128-bit memory backend for an x16 SDR
SDRAM device. It is connected to the complete CPU in a separate RTL simulation;
it is not included in a board bitstream yet. It exercises a real external-memory command interface and
provides a path beyond the block RAM used by the existing ULX3S prototype.
The Genesys 2 board discussed in the purchase research uses DDR3; it needs a
DDR3 controller and PHY connected through the existing AXI path.

## Device and timing assumptions

The ULX3S schematic identifies an MT48LC16M16A2TG-6A option and several
alternatives. The default configuration follows the x16 geometry and timing
of the Micron 256 Mb part: four banks, 13 row bits and nine column bits,
providing 32 MiB. The actual part fitted to a purchased board must be checked.
Sources: [ULX3S SDRAM schematic](https://github.com/emard/ulx3s/blob/master/ram.sch)
and [Micron 256 Mb SDRAM datasheet, revision W](https://www.alliancememory.com/wp-content/uploads/Micron_256M_SDRAM_PartNo.MT48LC16M16A2.pdf).

The two device profiles use a 200 microsecond startup wait and the
commercial/industrial refresh requirement of 8,192 refreshes in 64 milliseconds.
The controller starts refresh early enough to finish an accepted transaction
before its deadline. The independent pin model checks the actual command gap,
including while requests remain asserted and during warm reset.

| Timing parameter, in memory clocks | 25 MHz profile | 100 MHz profile |
| --- | ---: | ---: |
| Startup wait | 5,000 | 20,000 |
| Maximum refresh interval | 195 | 781 |
| CAS latency | 2 | 3 |
| ACTIVATE to READ/WRITE, tRCD | 1 | 2 |
| PRECHARGE recovery, tRP | 1 | 2 |
| REFRESH recovery, tRFC | 2 | 6 |
| Minimum active row time, tRAS | 2 | 5 |
| Write recovery, tWR | 2 | 2 |
| ACTIVATE spacing, tRC | 2 | 6 |
| Mode register recovery, tMRD | 2 | 2 |

These values select cycle-based protocol constraints. They do not establish
that an FPGA implementation meets either clock frequency. A memory PHY,
forwarded clock, pin assignment and input/output timing analysis remain work.
The current read interface samples each word one clock after the device's
nominal output edge; changing that interface requires updating its latency
contract and tests.

## Request and reset contract

A request carries an aligned 16-byte address, 128 data bits, a direction and
16 byte enables. The caller holds `valid` and the request stable until `ready`.
A completed request cannot execute again until `valid` drops or `bus_reset`
releases the interface. A zero mask, misaligned address or request beyond
`RAM_BYTES` returns a fault without issuing a device access. Reads return all
16 bytes; the upstream bridge selects the requested bytes.

Each accepted access activates one bank, transfers an eight-word x16 burst
and explicitly precharges the bank. The controller keeps one request in
flight and waits for row and precharge timing before acknowledging it.
Address bits select byte, column, bank and row in that order. The bounded
128 KiB test profile retains the real device geometry while restricting the
permitted address range.

`reset` is a **cold power/clock initialization reset**. It initializes the
controller and runs the SDRAM startup sequence. `bus_reset` is a **warm
interface reset**: it suppresses the old response, finishes any accepted
pin operation, closes the bank and continues refresh. It does not roll back
an accepted write. Dropping `valid` also cancels the response while allowing
the operation to finish. The memory clock must continue running.

Neither reset clears the SDRAM array. The CPU memory bridge must perform its
normal initialization before a new program uses memory. The tests start
with nonzero contents and retain contents through warm resets.

Unknown request controls cannot authorize a simulated write. Unknown read
data remains unknown. These four-state simulation rules do not detect
analog metastability or physical memory errors.

## Verification

After `python3 tools/bootstrap.py`, run:

```sh
python3 tools/check_sdram.py --mapped
python3 tools/check_sdram_four_state.py
python3 tools/prove_sdram.py
```

The functional campaign compares the native controller and its ECP5-mapped
circuit against an independent pin-level SDRAM model and a byte-array oracle.
It covers every 16-bit write mask, randomized traffic, bank/column boundaries,
invalid addresses, held requests and resets throughout reads, writes and
refresh. Six configurations cover the two device timing profiles, a bounded
memory prefix, and artificial timing/geometry stress cases. The two models
must match stimulus hashes, observations and cycle counts. Corrupted data,
ignored masks, missing refresh, premature commands, wrong read latency and
read masking must each fail the appropriate independent check.

The mapped builder verifies the actual LUT models and checks the flattened
combinational graph for cycles. A deliberately cyclic circuit must fail that
check. Verilator 5.020 cannot split public port vectors, so the builder permits
only the `sdram_address` vector scheduling warning after the graph check;
other combinational-loop warnings remain fatal. This does not change the
mapped circuit.

The four-state campaign uses Icarus Verilog for X/Z inputs, reset and read data,
with three deliberately broken controllers. The formal campaign uses
induction with an initial cold reset followed by arbitrary binary requests,
read data and warm resets. Its assertions check request isolation, pin payload,
read capture, refresh deadlines and bounded controller activity. Seven
controller mutations must produce counterexamples before positive proofs run.
The formal model does not prove a DRAM array, electrical timing or a board PHY.

The [completed proof](verification/sdram-proof.json) covers all six
configurations. Intermediate assertions relate timers to controller phases,
captured requests to device payloads and partial reads to the completed word.
These assertions are proved along with the original properties. They are not
additional assumptions about the inputs. This permits induction to finish
without unrolling an entire transaction or the startup delay.

Reports in `reports/sdram-*.json` identify the exact sources, tools, profiles
and outcomes. A report is written only after its entire selected campaign
passes and its input identities remain unchanged. Completed results are
linked from the README; a running proof is not a completed result.

## Complete CPU integration

The integration builder replaces the block-RAM backend only in a private
simulation build. It uses a second, independent SystemVerilog SDRAM model
with nonzero initial contents, retained contents across application resets,
pin-command timing assertions and refresh coverage. The existing UART
uploader and independent program-result oracle remain in use.

The memory bridge stays in reset until the SDR controller reports that
initialization is complete. Application reset goes to the controller's warm
reset input. Both [the ordinary timing run](verification/sdram-system-25mhz-5000.json)
and [the delayed startup run](verification/sdram-system-100mhz-5000000.json)
pass all 35 programmable-system cases. The delayed run uses 5,000,000 startup
clocks so initialization actually overlaps a committed upload; normal serial
uploads otherwise hide this condition. The observed startup stalls total
12,178,089 clocks across the test processes. This is a test delay, not a new
board startup requirement.

```sh
python3 tools/check_sdram_system.py --timing 25mhz
python3 tools/check_sdram_system.py --timing 100mhz --startup-cycles 5000000
python3 tools/check_sdram_system.py --timing 25mhz --negative-control read-corruption
python3 tools/check_sdram_system.py --timing 100mhz --startup-cycles 5000000 --negative-control startup-bypass
```

The read-corruption case must fail the program-result oracle. The startup
bypass must trigger the independent assertion against premature memory
requests; its raw HDL diagnostic is captured directly. A generic process or
JSON parsing failure cannot stand in for either expected rejection.
CI repeats both complete campaigns and their negative controls.

The freestanding C CRC-32 workload also passes all five lengths through this
CPU and device model, checked against Python's independent CRC implementation.
Both the [25 MHz run](verification/sdram-c-25mhz.json) and
[100 MHz run with delayed startup](verification/sdram-c-100mhz-5000000.json)
perform 1,281 device reads and 42,246 writes. Their longest observed refresh
gaps are 173 and 756 clocks, within their respective 195- and 781-clock limits.
The delayed run records 13,873,015 startup-wait clocks across its five processes.
Each result checker also rejects an intentionally wrong CRC. These runs use
separate build and coverage directories so they preserve the 35-case evidence.

```sh
python3 tools/check_sdram_c_workload.py --timing 25mhz
python3 tools/check_sdram_c_workload.py --timing 100mhz --startup-cycles 5000000
```

Clang 18 and LLD 18 compile and link the workload; their exact identities, the
upload packets, simulator, source inputs and device observations are recorded.
CI repeats both configurations.

All four jobs in [CI run 41788486972](https://github.com/Millillion/wasmetal/actions/runs/41788486972)
passed. The [independent artifact comparison](verification/ci-sdram.json)
checks all nine downloaded reports against the local records: six native/mapped
profiles, six formal configurations, negative controls, both complete CPU
campaigns and both C campaigns. The UART observations, execution cycles and
device coverage match. Compiled Wasm and serialized C upload packets also
match; image-manifest identities are retained separately because those
manifests also identify their preparation executables.
The CI reports are archived under [verification/ci-sdram](verification/ci-sdram).

Those earlier system tests use one simulation clock and a behavioral device.
The separately clocked integration below adds digital clock-crossing verification.
The default board backend remains block RAM. Physical memory-clock generation,
clock-crossing constraints and a board PHY are still required; the 25 MHz and
100 MHz settings describe device-model timing constraints.

## Complete CPU with separate clocks

The private integration binding now connects the complete CPU through the
production `wasmetal_memory_cdc` and SDR controller to the behavioral device.
The memory clock has its own schedule, with edges both between and coincident
with CPU edges. Cold initialization occurs in the memory domain. Application
reset resets the crossing and asserts the SDR controller's warm reset, allowing
refresh and accepted pin operations to continue. A two-register startup
synchronizer and the CDC's online indication hold the CPU memory bridge until
both the device and transport are ready.

All 35 integration cases pass in each configuration:

| Configuration | Memory cycles per CPU cycle | Startup wait in memory clocks | Result |
| --- | ---: | ---: | --- |
| 25 MHz timing profile, faster memory clock | 11/3 | 5,000 | [35 passed](verification/sdram-async-faster-25mhz-5000.json) |
| 100 MHz timing profile, slower memory clock | 7/11 | 2,000,000 | [35 passed](verification/sdram-async-slower-100mhz-2000000.json) |

These clock ratios are digital stress configurations, not proposed physical
operating frequencies. The second run deliberately extends initialization
beyond program upload and records 3,981,937 CPU clocks of startup waiting across
the campaign. The device begins with nonzero contents and preserves its array
across application resets. The UART program-result oracle remains independent
of the controller and the device model.

Three deliberate integration faults are rejected: a
[controller on the wrong clock](verification/sdram-async-faster-25mhz-5000-wrong-clock.json)
violates the device monitor's timing checks;
[bypassed startup permission](verification/sdram-async-slower-100mhz-2000000-startup-bypass.json)
issues a request before device initialization; and
[corrupted reads](verification/sdram-async-faster-25mhz-5000-read-corruption.json)
fail the independent program-result check. Generic crashes or timeouts cannot
satisfy those expected rejections.

The [clock-driver check](verification/sdram-clock-driver.json) extracts the
actual C++ scheduler and records every clock transition presented to `eval()`.
Both schedules match independently enumerated event sequences exactly. Six
mutations covering premature CPU edges, omitted simultaneous edges and the
wrong memory period are rejected. Each full CPU run also checks its observed
edge counts and coincident edges against arithmetic formulas.

```sh
python3 tools/check_sdram_clock_driver.py
python3 tools/check_sdram_async_system.py --timing 25mhz --clocks faster
python3 tools/check_sdram_async_system.py --timing 100mhz --clocks slower --startup-cycles 2000000
python3 tools/check_sdram_async_system.py --timing 25mhz --clocks faster --negative-control wrong-clock
python3 tools/check_sdram_async_system.py --timing 25mhz --clocks faster --negative-control read-corruption
python3 tools/check_sdram_async_system.py --timing 100mhz --clocks slower --startup-cycles 2000000 --negative-control startup-bypass
```

CI is configured to repeat both complete campaigns, the scheduler check and
all three faults. [Archived observations](verification/sdram-async) preserve the
device, source-interface and clock counters. This verifies the assembled RTL
with digital clocks; metastability, a board PHY and physical I/O timing remain
outside this simulation.

## Integration work remaining

1. Add a board-specific PHY and clock/reset boundary with I/O timing
   constraints. Check the actual populated device and board revision.
2. Synthesize and route that complete system. Measure memory savings,
   performance and timing using the resulting implementation.
3. Exercise a physical board with memory tests and repeated application loads.

The existing programmable FPGA system continues to use block RAM. No working
external-memory board implementation follows from these component tests.
