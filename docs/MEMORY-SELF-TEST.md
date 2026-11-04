# Destructive memory self-test

`soc/asic/wasmetal_memory_bist.sv` is a separate test master for the existing
128-bit physical memory transaction interface. It is intended for startup or
maintenance while another controller grants it exclusive access to memory.
It is not wired into the default CPU or FPGA image, and it does not supply
arbitration, scan insertion, a foundry SRAM model or manufacturing qualification.

## Algorithm and contents

The master makes eight complete March C- passes. Each pass writes a background
across memory, performs ascending read/write sweeps with complementary values,
repeats the read/write sweeps in descending order, then reads the background
again. The underlying sequence follows the
[March C- definition documented by Microchip](https://onlinedocs.microchip.com/oxy/GUID-1BC922B5-0BDE-4D42-AC92-68359BB22BEC-en-US-1/GUID-81A68B22-3BC9-479D-A63A-DAD6B44A852F.html).

Seven backgrounds alternate groups of 1, 2, 4, 8, 16, 32 and 64 bits within
each 128-bit word. Every pair of data-bit positions differs in at least one
of those backgrounds. The last pass uses zero, leaving the array zeroed on a
successful run. There are 80 completed memory transactions per word, or
655,360 transactions for the default 128 KiB capacity.

This test destroys previous contents. Its fault-injection campaign establishes
detection of the explicit models in the verification report. It does not
establish coverage of all physical defects, linked faults, retention failures,
electrical disturbances or process-specific SRAM behavior.

## Control and memory contract

| Signal or parameter | Contract |
| --- | --- |
| `RAM_BYTES` | Positive multiple of 16; default 131,072. A non-power-of-two number of words is supported. |
| `RESPONSE_TIMEOUT` | Number of request clock edges without completion before recording timeout; default 1,024. |
| `start` | Begin a test while idle. Requests while busy are ignored. Hold low for at least one clock after completion before issuing another start. |
| `busy` | Owns the memory path, including the response-release cycle. |
| `done` | Sticky completion status, cleared by reset or a newly accepted start. |
| `failed`, `error_code` | Sticky first failure: 1 is read mismatch, 2 is a memory fault response, 3 is timeout. |
| `error_address` | Byte address of the first failed transaction. |
| `expected_data`, `observed_data` | Expected and returned values at the first failure. Timeout records zero for the absent observation. |
| `completed_operations` | Number of actual completed transactions, including a failed response. |

The memory request uses the same `valid`, `write`, byte `address`, 16-bit byte
`mask`, 128-bit `wdata`, completion `ready`, `fault` and `rdata` convention as
the [SRAM adapter](SRAM.md). Every request uses an aligned address and all byte
enables. The master holds the entire request stable until completion, then
holds `valid` low for a release edge before issuing another request. It records
a fault response before considering a simultaneous read-data mismatch.

On timeout, `failed` becomes true but the pending request remains active and
`busy` remains true. A late response is drained before `done` becomes true;
it cannot overwrite the original timeout evidence. If the response never
arrives, reset this master and its memory controller together before releasing
ownership. Reset cancels controller activity; it does not undo writes that
have already reached memory or restore previous contents.

## Verification

```sh
python3 tools/check_memory_bist.py --mapped
python3 tools/check_memory_bist_four_state.py
python3 tools/prove_memory_bist.py
```

The C++ checker generates the March sequence from a declarative list of
operations and compares every request, address, byte mask and write value.
An independent memory model supplies responses and injected faults. The test
covers all data bits in one-word and five-word arrays, every data-bit pair
with wired-AND and wired-OR faults, selected address aliases, dropped byte
writes and six inter-word transition/coupling models. It also exercises the
full 128 KiB capacity, variable response delays, held starts, resets throughout
the sequence, read/write timeouts and fault-response priority. RTL and mapped
executables must produce identical observations and cycle counts.

Six deliberately broken implementations must fail that independent checker.
The four-state campaign starts memory with unknown contents, checks X/Z read
diagnostics, resets an outstanding request and verifies recovery. Its two
mutants remove unknown-data diagnosis or request isolation during reset.
Detecting X/Z in simulation is not a physical metastability detector.

The formal checker uses an independent mathematical position within the March
sequence to prove progress accounting and request bounds. It also checks
request stability and preservation of the first error under arbitrary binary
responses, start inputs and subsequent resets. It assumes an initial reset
and does not assume that memory eventually responds. Consequently its safety
proof does not claim eventual completion for an unresponsive memory or prove
the SRAM array's storage behavior. Its separate fault controls must also pass
before the proof report is accepted.

## Recorded results

The [RTL and ECP5 mapped campaign](verification/memory-bist-mapped.json) passed
55,137 campaigns per model with identical observations: 7,326,876 requests,
33,625,771 clocks, 58,506 resets and 51,759 completed fault detections. Twelve
timeout scenarios include late responses and requests that remain pending
until a shared reset. The independent sequence checker rejects six broken
implementations. These counts describe the specific injected models and do
not establish manufacturing fault coverage.

The [four-state campaign](verification/memory-bist-four-state.json) passes and
rejects two mutants. The [unbounded safety campaign](verification/memory-bist-proof.json)
passes for 80-byte, 16-byte and 128 KiB arrays, plus a one-clock response
deadline; it rejects four deliberate proof faults. The positive proofs keep
responses unconstrained after the initial reset.

[The original baseline archive](verification/memory-bist/index.json) also
retain the early descending-sweep control experiments. A 12-step trace did
not reach that late fault, and an unconstrained 32-step attempt timed out.
A separate 32-step trace with immediate healthy responses exposed the fault.
The regular proof gate uses an early reversed-sweep fault for bounded runtime;
the independent simulation also rejects the descending-sweep mutation. These
fault controls remain separate from the four unbounded positive proofs.

The default CPU builder excludes this separate master. Its
[47-source inventory](verification/memory-bist-source-inventory.json) matches
the previously verified programmable system byte for byte, and default CPU
lint passes. An unused-source synthesis experiment is retained in the archive:
parsing the extra module changed downstream mapping to 50,991 LUTs. That
experiment was discarded; its circuit has no functional-verification claim.
The default Xilinx estimator remains unchanged.

## SRAM adapter integration

`tests/asic/wasmetal_bist_sram.sv` connects the master directly to the actual
SRAM adapter. Its C++ harness observes only the macro pins and public test
status. It generates the full expected March command sequence independently,
checks every address, write value and byte enable, and models the stored bytes
and synchronous read latency separately from both controllers.

```sh
python3 tools/check_bist_sram.py --mapped
```

The six configurations cover 16 bytes, 80 bytes, 272 bytes and 128 KiB, with
one-, three- and seven-cycle reads. They include the smallest successful
response deadline and deliberate deadlines that expire on reads or writes.
Timeout cases must drain the actual macro access and retain the first error.
For the two smallest healthy configurations, the test injects corruption at
every read position and applies a shared reset at every clock of a complete
healthy sequence. Memory contents and outstanding macro reads survive reset;
unused read cycles carry changing garbage to expose incorrect capture timing.

Three deliberately broken bindings change read latency, omit the adapter's
reset or drop a byte enable. A fourth control corrupts the macro's read data.
The integration gate accepts its report only after all configurations agree
between RTL and mapped simulation and all four controls are rejected. This
verification binding has no CPU arbitration or boot-control logic, and does
not substitute for a foundry macro model or physical timing signoff.

The [completed integration report](verification/bist-sram-mapped.json) records
2,848 campaigns, 7,329,277 macro commands and 40,301,847 clocks per model, with
identical RTL/mapped observations. It includes 5,440 resets, 266 expected error
detections and 400 old read responses delivered after a shared reset. All four
controls are rejected. The [original integration archive](verification/bist-sram/index.json)
retains the baseline runs and the earlier ambiguous fault-edit setup that the gate rejected.
The complete integration campaign runs in CI alongside the component checks.

## Counter sizing

The current master stores only the counter bits needed for `80 * WORDS`
completed operations. It still reports a 64-bit zero-extended count. A 64-bit
constant computes the bound before `$clog2`, avoiding 32-bit arithmetic overflow
at large capacities. This saves logic without changing the transaction sequence,
latency or diagnostic interface.

The [before/after comparison](verification/memory-bist-counter-sizing.json)
checks every component and SRAM integration configuration against the immutable
baseline reports. All observations, trace checksums and cycle counts match;
the independent C++ oracles are unchanged. RTL, ECP5 mapping, four-state checks
and all four unbounded safety proofs pass again, along with their fault controls.

| Master capacity | Counter bits | ECP5 registers, before → after | LUT4s, before → after |
| --- | ---: | ---: | ---: |
| 16 bytes | 7 | 345 → 288 | 1,227 → 1,172 |
| 80 bytes | 9 | 350 → 295 | 1,244 → 1,187 |
| 128 KiB | 20 | 375 → 331 | 1,295 → 1,247 |

These are resources for the separate test master, not the CPU or SRAM array.
The combined master/adapter also saves 44 registers and 44 LUT4s at 128 KiB.

```sh
python3 tools/check_memory_bist_widths.py
```

The [capacity-boundary gate](verification/memory-bist-widths.json) checks seven
elaborated capacities, including both sides of the 32-bit count boundary and
the largest positive signed 32-bit, 16-byte-aligned `RAM_BYTES` value. It checks
the actual internal width and output zero extension, then uses a three-step SAT
check seeded at the last successful read to prove the final count and completion
status. This is a seeded boundary check, not a proof that the seed is reachable
or a complete sweep of a large SRAM. Deliberately truncating the capacity
arithmetic or removing a counter bit must fail the check. CI requires this gate.

The [current archive](verification/memory-bist-counter-sized/index.json) retains
the new reports, source snapshots, mapped circuits, proof scripts and logs,
including three rejected early boundary-check setups. The original archives
remain unchanged so the resource and behavior comparison can be repeated.
