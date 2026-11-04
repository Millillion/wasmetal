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

[Archived inputs, scripts and logs](verification/memory-bist/index.json) also
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
