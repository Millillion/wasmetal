# Crossing to an external-memory clock

`soc/external/wasmetal_memory_cdc.sv` transports one 128-bit physical memory
request between independent CPU and memory clocks. The assembled
`wasmetal_async_axi_memory.sv` connects it to the [AXI adapter](AXI.md).
These verified components are not yet connected to the CPU's active memory
path or a DDR controller. The standalone system still uses local block RAM.

## Transaction and reset contract

The source registers the entire 177-bit request: write/read, byte address,
byte mask and data. It toggles a request bit and holds the request registers.
Two destination-clock registers synchronize the toggle. The destination then
captures the stable bundle and holds its memory request until completion.
It registers the 129-bit response (fault and data), toggles the acknowledgment,
and holds that bundle. Two source-clock registers synchronize the acknowledgment
before the source captures the response. A fault returns known zero data.

`s_ready` pulses for one source cycle. The caller must release `s_valid` after
completion before another request can be accepted. Changing input fields after
capture does not change the pending request. Withdrawing `s_valid` while waiting
does not cancel an accepted request. The caller must drain the response or reset
the complete interface; a timeout alone cannot safely reuse it.

This is a full handshake, with one outstanding transaction and additional
latency for synchronization. It is not a multi-entry asynchronous FIFO.
The need to finish the handshake before starting another transfer also appears
in AMD's [bus-handshake CDC guidance](https://docs.amd.com/r/2021.1-English/ug1344-versal-architecture-libraries/XPM_CDC_HANDSHAKE).

A common reset asserts asynchronously in both domains. Each domain releases
its local reset after two clock edges. The destination registers an additional
"up" indication after leaving reset; that indication is synchronized back to
the source. `source_online`/`online` stays low until both domains have started.
Requests presented early wait without being issued. A stopped clock may delay
release indefinitely. A common reset still clears the link with both clocks
stopped.

The assembled wrapper exports `axi_reset`. The AXI adapter and the connected
subordinate must share that reset boundary and discard pending transfers
coherently. The adapter samples the stretched reset synchronously; the crossing
uses it asynchronously. A narrowly scoped Verilator `SYNCASYNCNET` waiver at
that wrapper port documents this intentional combination. Other lint warnings
remain enabled. Reset does not undo a write already accepted by external memory.

`online` describes this transport's reset sequence, **not DDR calibration**.
A future integration must keep the logical bridge in reset until the controller
can service transactions within its timeout, and must handle controller failure
or reset coherently. The bridge's startup memory clear must not run into a
controller that is still training or retaining an old transaction.

## Verification

Run `make cdc-test`; CI runs it with the memory and AXI checks.

- The [independent transport test](verification/cdc-mapped.json) passes 7,290
  transfers and 3,183,543 time steps in each model. Seven clock ratios/phases
  include either clock 32 times faster, equal frequencies with different phases,
  stopped clocks and 371 pauses during transfers. The 294 resets include startup
  and interrupted requests; the test requires observed coverage before capture,
  during backend work, while the response crosses and after source completion.
- The [assembled AXI test](verification/async-axi-mapped.json) repeats the full
  21,732-transaction AXI oracle test with each clock faster in turn: 43,464
  transactions per model. It exercises independent AW/W ordering, channel
  stalls, partial writes, response errors, overflow, held requests, late
  completion and reset interruption. Native and mapped clocks and results agree.
- The [structural audit](verification/cdc-structure.json) checks both generic
  and ECP5-mapped two-register chains, reset values, receiving clocks, attributes
  and first-stage fanout. It traces every generic register's data cone: only the
  three control synchronizers and the two registered payload bundles may cross
  clock domains. Mutations removing an attribute, exposing a first stage,
  bypassing a stage or injecting a raw source input are rejected.
- The same audit runs an Icarus four-state test with unknown startup state,
  stopped-clock reset and an unknown backend data value accompanying a fault.
  Omitting the request-toggle reset makes the negative control fail.
- [Unbounded induction](verification/cdc-proof.json) proves initialization and
  the RTL's source/destination stall-stability assertions. Yosys `clk2fflogic`
  models independent clock edges on a global formal time step; clocks may stop.
  Inputs are arbitrary binary values after an initial common reset, with later
  resets unrestricted. Reachable-state lemmas are proved jointly, not assumed.
  Missing payload reset and changing the pending payload both fail. This proof
  does not establish complete transfer equivalence, liveness or analog behavior.

## Required physical implementation

Digital simulation, these safety proofs and structural checks do not model
metastability, placement, analog reset behavior or routed wire delay. No
physical CDC signoff or FPGA test is claimed.

Both `ASYNC_REG="TRUE"` and the lower-case attribute are retained in the mapped
netlist. AMD documents the uppercase property for its
[synthesis tools](https://docs.amd.com/r/en-US/ug901-vivado-synthesis/ASYNC_REG).
Preserving an attribute is not evidence that a particular placer honors it.

The actual board implementation must constrain and inspect these paths:

1. Place the two registers of each synchronizer together and time the path from
   its first stage to its second stage at the receiving clock. Only the first
   stage may sample the asynchronous control; it must have no other consumers.
2. Bound every request-payload path to its destination capture register and every
   response-payload path to its source capture register. The control handshake
   provides settling time, but does not itself constrain those wires. A
   conservative integration budget is one receiving-clock period, reduced for
   clock-to-Q, setup and uncertainty. Validate the actual bound and exceptions
   with the selected implementation tools and operating conditions.
3. Avoid broad asynchronous-clock false paths that silently override the bundled
   payload delay limits. Check timing coverage and CDC reports on the implemented
   netlist, not just the RTL names.
4. Check reset pulse widths, asynchronous assertion, synchronous release,
   recovery/removal, controller reset interaction and synchronizer reliability
   for actual clock rates, voltage and temperature.

Those constraints must be tied to the selected controller, generated clocks and
synthesized hierarchy. They cannot be certified by this generic component test.
