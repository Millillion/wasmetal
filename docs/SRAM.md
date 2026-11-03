# Synchronous SRAM macro boundary

`soc/asic/wasmetal_sram_memory.sv` adapts the existing 128-bit physical memory
transaction interface to a synchronous SRAM port. It is verified separately
and is not connected to the CPU's active memory path. No foundry macro, PDK,
standard-cell mapping or silicon timing is supplied by this component.

## Macro contract

The macro and adapter share one clock. The macro samples a command on a rising
edge when `sram_enable` is high. `sram_write` selects a write; otherwise the
command is a read. Each accepted legal transaction issues exactly one command.

| Signal | Meaning |
| --- | --- |
| `sram_address` | Word index; one word is 16 bytes |
| `sram_wdata`, `sram_rdata` | 128-bit little-endian write and read values |
| `sram_byte_enable[n]` | Active-high enable for write-data bits `8*n +: 8`; ignored on reads |
| `sram_enable` | One-cycle command enable, suppressed while reset is asserted |
| `sram_write` | Write direction, asserted only with command enable |

A read issued at edge N must produce data stable before edge
N + `READ_LATENCY`. The adapter samples that data on the latter edge. For
latency 1, a synchronous SRAM may change its output after the issue edge and
must meet setup at the following edge. A multi-cycle implementation must
complete its read pipeline even though command enable was only one cycle.
Polarity changes, banking, write-mask conversion and any additional registers
belong in a macro-specific wrapper that preserves this contract.

`RAM_BYTES` must be a positive multiple of 16. The default is 128 KiB with
8,192 words. `ADDRESS_WIDTH` must equal the derived word-address width. A
non-power-of-two size is allowed: unused addresses remain inaccessible even
when the address bus could represent them.

The adapter captures the bus request, issues the SRAM command on the next
edge, and returns a one-cycle completion. Writes complete after issue; reads
complete after the configured read latency. It rejects zero masks, unaligned
addresses, out-of-range words and 32-bit address overflow without enabling the
macro. Holding the bus request high after completion cannot repeat a write.

## Reset and initialization

Reset clears controller state and cancels pending responses. It does not clear
the SRAM or undo a write that already reached the macro. The upstream
[memory bridge](MEMORY.md) owns backing-store initialization and must reset
alongside the adapter. A macro's delayed old read data may still arrive after
reset; the adapter waits for the new transaction's proper capture edge.

Uninitialized SRAM data is not converted into a fabricated zero. Four-state
simulation preserves unknown read data. The system must finish initialization
before using those locations. Error correction, power-state sequencing,
memory-test access and detection of electrical or macro failures need their
own implementations.

## Verification

```sh
python3 tools/check_sram.py --mapped
python3 tools/prove_sram.py
python3 tools/check_sram_four_state.py
```

The [independent byte-memory tests](verification/sram-mapped.json) pass
719,924 transactions in each of RTL and functional ECP5-mapped simulation,
with identical observations and 6,815,791 clock cycles per model. They cover
128 KiB at read latencies 1, 2 and 3; 80 bytes at latency 8; and a single
16-byte word. Every configuration tests all 65,536 byte masks, address bounds,
data preservation and held requests. Ninety resets interrupt different
transaction phases, including reads still in the macro model's pipeline.
Corrupted read data and ignored write masks must fail the independent oracle.

The [unbounded induction proof](verification/sram-proof.json) covers all five
configurations under arbitrary binary requests, read data and subsequent
resets after an initial reset. It proves command bounds and payload, exact
response timing, request-release behavior and defined controller state.
Wrong masks, early capture, duplicate commands and missing reset assignments
are rejected by negative controls. This proves the adapter's properties, not
the SRAM array's stored-data behavior or physical timing.

The [four-state checks](verification/sram-four-state.json) independently verify
reset isolation, unknown-read propagation, subsequent known reads and fault
responses. Mutants that erase unknown data or remove reset isolation fail.
The ECP5 mapping is an extra logic implementation check; it is not an ASIC
implementation of the SRAM.
