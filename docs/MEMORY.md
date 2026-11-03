# Memory transaction boundary

The new `soc/memory` components separate Wasm address checking from physical
storage. Integration into the standalone system is in progress. The interface
is a small synchronous request/completion protocol, not AXI or Wishbone.

## Logical requests

The bridge accepts the core's six memory kinds and preserves their existing
meaning: linear bytes, globals, tables, passive data, passive elements and heap
values. Value spaces use sixteen-byte slots. A synchronous region lookup supplies
a 32-bit physical base and a 32-bit byte length in the cycle after capture.

All bounds are checked before the first physical request. Address arithmetic
uses 69 bits so scaling a 64-bit slot index and adding a width cannot wrap into
valid memory. Invalid indices, widths, segment writes and physical overruns
return a fault without issuing any memory transaction. They do not poison the
backend; a subsequent valid request can succeed.

## Physical requests

All signals use one clock; requests and completions are sampled on its rising
edge. `bus_valid` holds the request until `bus_ready`, including address, write
direction, mask and data. `bus_fault` is meaningful only with completion.
There is one outstanding request and a release cycle between requests.

- `bus_address` is a 32-bit byte address aligned to sixteen bytes.
- `bus_wdata` and `bus_rdata` are 128-bit little-endian words.
- `bus_mask[n]` selects byte `n` for writes. Reads may fetch the entire word;
  the bridge returns only requested bytes and zeroes all other result bytes.
- One logical request of 1–16 bytes becomes one or two aligned physical
  requests. Adjacent bytes must survive a masked write unchanged.

An independent byte-array oracle checks translation, byte enables, contents and
the exact number of physical requests under randomized response latency.
The byte-lane aligner also has a separate exhaustive symbolic equivalence
check against byte-indexed reference expressions.

`make memory-test` also proves the bridge's address alignment, physical bounds,
nonzero byte masks, request stability through stalls, beat geometry and poisoned
state isolation by temporal induction. The proof assumes an initial reset and
allows arbitrary binary requests, region descriptors and backend responses
afterward, including subsequent resets. It covers both the small test instance
and the production parameters, including the 1,024-cycle timeout. This is an
unbounded safety proof for these properties, not a proof of complete memory
data equivalence or eventual completion. Corrupted-address and missing-reset
negative controls must produce counterexamples.

## Reset and faults

Reset discards any in-flight response and clears the complete backing pool
through full-word writes before asserting `initialized`. Backends must reset
their request state too. Physical RAM contents need not be initialized by the
FPGA configuration or reset by a large reset tree.

A backend error or timeout while clearing asserts `initialization_failed` and
prevents execution until reset. A backend error or timeout during a logical
request returns a fault and poisons the interface. Further logical requests
fault without issuing new bus requests, so a late completion cannot be confused
with a new transaction. The timeout is per physical request and defaults to
1,024 clock cycles.

A bounds fault never partially writes memory. A physical backend failure on the
second beat can follow a completed first beat: this is a hardware failure, not
an architectural bounds check. There is no rollback of an acknowledged write.
Reset and full reinitialization are required to recover from the poisoned state.

## Replaceable storage

`wasmetal_bram` implements masked storage using explicit banks of up to 2,048
words. Its opposite-edge RAM ports fit the existing checked ECP5 primitive
model. Reset clears its protocol state, not its stored bytes; the bridge owns
zero initialization. A backend response is held for a full clock cycle, and
holding `valid` after completion cannot execute the request twice.

An external-memory controller or ASIC SRAM adapter can implement the same
physical interface with a different internal memory latency and clocking scheme.
It must preserve byte masking, ordering, fault and reset contracts. An external
controller/device model and an actual process-compatible SRAM implementation
are separate deliverables; this interface alone does not establish either.
