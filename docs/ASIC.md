# ASIC preparation

The [generic elaboration audit](verification/asic-audit.json) inventories the
standalone SoC before any FPGA technology mapping. It retains 82 logical
memories containing 3,035,968 bits, plus 6,177 bits in generic clocked register
cells. These are logical storage counts, not silicon area estimates.

The audit applies the actual standalone capacity profile, checks that the
backing pool and value stack each retain exactly 1,048,576 bits, rejects
unexplained clocks and latches, and requires all cells to remain generic Yosys
cells. Its source, image, script, tool and netlist hashes are recorded. The
prepared self-test image supplies the ROM contents for this particular audit.

```sh
make sim
python3 tools/prepare_standalone.py examples/standalone/selftest.wat
python3 tools/audit_asic.py
```

The output is `reports/asic-audit.json`; the generic netlist and synthesis log
are in `build/asic-audit`. This flow does not perform standard-cell mapping,
SRAM-macro mapping, static timing analysis, placement, routing or signoff.

The programmable system has a separate audit:

```sh
python3 tools/audit_asic.py --loadable
```

It does not read a prepared ROM image. The
[programmable audit](verification/asic-loadable-audit.json) retains the same
82 logical memories and 3,035,968 memory bits, plus 7,125 generic register bits.
All five program stores are writable, have their expected dimensions and
contain no known initial bits: 444,416 bits are supplied through the serial
loader before execution. No initialized registers remain in this SoC either.
This removes the fixed-program ROM assumption for this implementation; SRAM
macro mapping and clock/reset implementation still require real technology IP.

## Memory boundaries that need real implementations

| Storage | Logical organization | Contract to preserve |
| --- | --- | --- |
| Values and locals | Four 2,048 × 128-bit banks | Concurrent bank reads, pending-write forwarding and out-of-range masking |
| Control labels | 2,048 × 161 bits | Existing read/write ordering and capacity checks |
| Call frames | 512 × 128 bits | Existing read/write ordering and capacity checks |
| Six descriptor stores | 256 rows, 64 or 65 bits per row | Two stores need two read ports; all accept writes |
| Backing pool | 128 KiB, currently 64 banks of 2,048 × 8 bits | Masked writes through the [physical memory interface](MEMORY.md) |
| Program and metadata | Instruction, function, boot, region and type memories | Contents must exist before execution; type matching currently reads asynchronously |

Most memory reads use the falling edge while writes and CPU state use the
rising edge. Both phases are part of the timing contract. A replacement macro
must match that behavior, or the surrounding control must be changed and
verified with its new latency. A macro with different read latency cannot
simply replace an inferred array.

The memory-size and table-size descriptor stores have two read ports. They need
a compatible macro or a verified implementation such as replicated storage
with broadcast writes. The asynchronous type matrix and small decoder ROM
also need explicit implementation decisions. The audit identifies eight
memories requiring review for multiple read ports, initial contents or
asynchronous reads; every other memory still needs a compatible macro.

The wide backing-memory boundary already supports variable response latency.
An ASIC SRAM adapter can therefore replace the FPGA-specific banking without
changing the logical Wasm address checks. The core's internal stack and control
memories have separate timing contracts and are not covered by that flexibility.
The separately verified [synchronous SRAM adapter](SRAM.md) now implements that
transaction boundary with explicit byte masks and fixed read latency. A
separate complete-CPU simulation binds it into the memory path with a
behavioral SRAM; all 35 integration cases pass at each of two read latencies.
A compatible real
macro wrapper remains necessary; this does not replace the other logical
memories listed above or change the default FPGA backend.

For programmable storage, the generic audit also reports an asynchronous region
array feeding a separately retained enabled read register. A macro integration
must preserve that complete read boundary; the raw array's port description
alone does not describe its architectural latency. Instructions, functions and
boot records retain falling-edge reads and rising-edge writes. The region
read is disabled during upload, preventing simultaneous read/write access in
the FPGA's same-edge RAM mode; that exclusion is separately proved against the
mapped circuit. The type matrix remains an asynchronous lookup.

## Reset, boot and test access

The audited SoC takes a clock and synchronous reset as inputs. It excludes the
FPGA oscillator divider, clock buffer, initialized reset synchronizer and pads.
An ASIC needs a real power-on-reset and clock/reset implementation, including
reset release, test-mode behavior and any required clock-domain crossings.

No initialized register nets remain in this generic SoC. That does not make
its initialized ROM contents appear automatically in silicon. A fixed program
needs an actual ROM implementation; a programmable product needs a loader and
writable storage, with execution held until a complete image is available.
Mutable backing storage is explicitly cleared by transactions during boot.

Before a manufacturing implementation, add and verify the intended debug,
scan and memory-test access. Decide how test mode controls clocks, resets,
memory ports and I/O, and how failures can be observed. A simulation harness
and a UART result packet are not substitutes for manufacturing-test coverage.

A separate [destructive memory-test master](MEMORY-SELF-TEST.md) now implements
eight March C- passes through the physical memory transaction boundary. Its
[composed SRAM check](verification/bist-sram-mapped.json) now verifies both
controllers together at the macro pins, including delayed reads across reset. It
checks seven separating bit backgrounds and a final zero background, records
the first error and retains ownership of a timed-out request until completion
or joint reset. Its independent fault-injection tests cover RTL and a functional
FPGA mapping. Integrating exclusive test access, selecting process-specific
fault models and establishing manufacturing coverage remain separate work;
the component is not connected to the default CPU image.

## Gates before fabrication

1. Select a process, supported tools, standard cells, memory macros, I/O cells,
   package and operating conditions. Resolve their licenses and availability.
2. Implement the memory, clock/reset, boot and debug/test boundaries. Re-run
   functional tests and equivalence checks with the selected macro models.
3. Constrain every clock, clock edge, external interface and operating corner.
   Resolve reset recovery/removal, clock crossings and timing exceptions with
   explicit justification. Set performance and power targets from measurements.
4. Perform process-specific synthesis, floorplanning, power distribution,
   placement, clock-tree construction and routing. Close timing across corners
   and analyze power, voltage drop, electromigration and signal integrity.
5. Complete foundry-required physical verification, including DRC, LVS and
   antenna checks; validate test coverage, pad/package connections and the
   production test plan. Review the final fabrication database and reports.

All of these stages can be advanced before FPGA testing when the necessary
process and IP information is available. FPGA bring-up remains useful evidence
about the assembled system; it does not replace these ASIC checks.
