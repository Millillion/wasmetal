# External memory adapter

`soc/external/wasmetal_axi_memory.sv` converts the
[128-bit physical memory interface](MEMORY.md) into AXI4 transactions. It is a
verified component; the standalone FPGA system still uses local block RAM.
It has not been connected to a DDR controller or tested on a board.

Each operation is one aligned sixteen-byte transfer with ID zero, length zero,
size four, incrementing burst type, byte write strobes and no exclusive access.
Cache, protection and quality-of-service attributes are zero. A configurable
base address translates the physical offset; overflow, misalignment and zero
masks fault before issuing a transaction.

Write address and write data handshake independently. Their VALID signals do
not wait for READY, and their payloads remain stable until accepted. A write
response is accepted after both transfers; a read response follows acceptance
of its address. These dependencies follow the
[Arm AXI4 specification, sections A3.2–A3.3](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/IHI0022H_amba_axi_protocol_spec.pdf).

There is one outstanding operation. Unexpected IDs, a missing final-read-beat
flag or a non-OKAY response return a fault with zero read data and prevent new
transactions until reset. Writes already accepted by a downstream system may
have changed memory; an error does not roll them back. Local address faults
do not poison the adapter.

## Verification

`make axi-test` runs the independent behavioral subordinate and byte-array
oracle, maps the adapter to ECP5 primitives, and repeats the same tests. The
[recorded run](verification/axi-mapped.json) passes 21,732 transactions in each
model with identical cycles and channel-order counts. It exercises address
before data, data before address and simultaneous acceptance; independent
stalls; masked writes; address overflow; response errors; interrupted transfers;
reset recovery; held requests and late completions. Deliberate read corruption
must fail the oracle in both models.

The [inductive safety proof](verification/axi-proof.json) covers request
stability, handshake dependencies, alignment and error isolation for three
base addresses. It allows arbitrary binary channel inputs after initial reset.
Mutations that make VALID depend on READY, accept a write response too early,
or omit a data-register reset must produce counterexamples. This proves the
listed safety properties, not complete data equivalence, eventual responses
from an unresponsive subordinate, or a complete third-party AXI compliance test.

## Integration requirements

All adapter signals currently share one clock. A different DDR-controller
clock needs a verified clock crossing. Connect reset coherently to the AXI
interface: resetting this master alone cannot cancel a transfer that another
component has already accepted.

The logical bridge owns the timeout. If its request is withdrawn after timeout,
this adapter keeps an outstanding AXI request valid until accepted. It cannot
invent completion or retract accepted work. Recovery must drain or coherently
reset the connected interface before reuse.

AMD's 7-series memory controller can expose an AXI4 interface and provides
startup/calibration status and a user-interface clock. Those are integration
boundaries, not evidence that this adapter already drives DDR.
[AMD UG586](https://www.xilinx.com/support/documents/ip_documentation/mig_7series/v4_1/ug586_7Series_MIS.pdf)
Our integration will hold WasMetal's memory initialization until the controller
is available, so the finite per-request timeout is not spent on DDR training.
The chosen board still needs its own controller configuration, pin and timing
constraints, device model and physical calibration checks.
