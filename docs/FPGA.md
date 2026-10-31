# WasMetal FPGA bring-up

The reference board is a **ULX3S 85F**, with an ECP5 LFE5U-85F, CABGA381 package,
speed grade 6. Smaller ULX3S variants cannot use this bitstream. The pin assignments
come from the board project's [v2.0 constraints](https://github.com/emard/ulx3s/blob/6a92cec6b177191c5b0f80e260013a1f8ec147dd/doc/constraints/ulx3s_v20.lpf).

This is a host-backed bring-up system. The FPGA contains the clocked Wasm execution
engine, including integer, floating-point, SIMD, reference, GC and exception
instructions. A host loads validated modules and supplies the expanded instruction
image, function/type metadata and backing storage over UART. The host does not
calculate instruction results. This system has no autonomous boot, SDRAM
controller or operating system. A physical board has not been programmed or tested
in this workspace.

## Storage profiles

[`fpga/profile.json`](../fpga/profile.json) defines the FPGA's finite capacities.
They are advertised by the bitstream and checked by the host:

| Resource | FPGA | Full conformance simulator |
|---|---:|---:|
| 128-bit value slots, including locals | 128 | 16,384 |
| Control labels | 128 | 2,048 |
| Saved call frames | 64 | 512 |
| Descriptors per memory/table/segment class | 16 | 256 |
| External 128-bit heap slots | 1,048,576 | 1,048,576 |

The instruction set is the same in both profiles. Programs exceeding a profile's
resources cannot be assumed to run successfully. Full official-suite results use
the larger simulator profile; they are not a claim that every test fits the smaller
FPGA profile. Heap allocation is bounded and currently has no reclamation.

The host reserves zero-initialized backing storage up to each memory's configured
maximum. The core checks bounds and exposes additional pages on `memory.grow`.
The unused tail must remain private and zeroed until exposed. The supplied sparse
host adapter implements that contract.

## Reproducible build

On Ubuntu 24.04 x86-64:

```sh
python3 tools/bootstrap.py --fpga-tools
make lint
make fpga-smoke fpga-host
make fpga-bitstream
```

The optional FPGA tool download is large. Dependencies and upstream tests are
checksum-pinned in `tools/upstream.lock.json`; installation stays under `.cache`.
The build uses Yosys 0.33, nextpnr-ecp5 and Project Trellis. `tools/cad.py` launches
the pinned CAD-suite binaries without their configuration-writing wrapper scripts.

`make fpga-core` creates `build/core-ecp5.json` and its source manifest.
`tools/build_board.py` checks that manifest, integrates the UART wrapper, then
places and routes the board. Timing failures fail the command; there is no
`--timing-allow-fail` option. A successful build produces:

- `build/ulx3s/wasmetal.bit`: FPGA configuration.
- `build/ulx3s/timing.json` and `nextpnr.log`: timing and resource evidence.
- `build/ulx3s/manifest.json`: source, configuration and bitstream identities.

Rebuild the host adapter after changing RTL or the FPGA profile. The protocol
checks a port-schema identifier and a 128-bit RTL build fingerprint, and rejects
an incompatible bitstream. The official-suite runner also checks executable and
source hashes before and after a run.

## Functional verification

`make fpga-smoke` simulates the entire board wrapper and UART, including serial
bits, framing, CRCs, clock pulses and the real CPU. It exercises arithmetic,
unaligned memory, SIMD, floating-point division, GC objects and array copying,
exceptions, bounds traps and zero-filled memory growth. It verifies that corrupt
packets, invalid flags, capability queries and abandoned packets do not execute
instructions. An incomplete packet is discarded after a 100 ms receive timeout.

For an additional check of synthesis mapping:

```sh
python3 tools/build_gate_sim.py --core-netlist build/core-ecp5.json
python3 tools/run_spec.py --simulator build/gate-model/obj/Vwasmetal_core \
  --suite i32 --suite i64 --suite f32 --suite f64 --suite conversions \
  --report reports/mapped-arithmetic.json
```

This is functional simulation of the mapped FPGA cells, not a timing simulation.
It uses Yosys' LUT, carry, RAM and flip-flop models. The unregistered 18-by-18 DSP
multiplier model accepts only the configurations emitted by this flow; unexpected
primitive types, DSP modes or connections fail the build.

The control labels and call frames map to nine block RAMs. The `DP16KD` functional
model accepts only the generated 512-by-36 pseudo-dual-port configuration, with
rising-edge writes, falling-edge reads and nine-bit write enables. Its packing
follows pinned Yosys' mapping and its behavior follows the
[Lattice memory guide](https://www.latticesemi.com/-/media/LatticeSemi/Documents/ApplicationNotes/EH/FPGA-TN-02204-1-6-ECP5-and-ECP5-5G-Memory-Usage-Guide.ashx?document_id=50466).
`make test-ecp5-ram` compares mapped and inferred initialized storage in a four-state
simulator. The timing report must also cover the CPU's half-cycle RAM paths.

At execution-source revision `f4e578b`, this mapped CPU passed twenty-eight official
suites with three memory wait states: 11,559 execution assertions covering scalar
arithmetic, SIMD, GC, exceptions and structured control in the
[mapped-cell report](verification/ecp5-mapped.json). The
[whole-board UART report](verification/fpga-uart.json) records fourteen passing
execution and transport checks. Each report identifies its executable, sources
and capacity profile. The mapped results are a subset; the
[complete 259-suite report](verification/core-3.0-current.json) uses the larger
RTL simulation profile.

## Loading a physical board

First build successfully and inspect its manifest and timing report. With the
correct board connected, openFPGALoader can load volatile SRAM:

```sh
openFPGALoader -b ulx3s -d /dev/ttyUSB0 build/ulx3s/wasmetal.bit
```

Select the actual board's device path. This is the documented
[SRAM-loading command](https://trabucayre.github.io/openFPGALoader/guide/first-steps.html)
for the supported [ULX3S board profile](https://trabucayre.github.io/openFPGALoader/compatibility/board.html).
It does not program persistent flash. Loading is a manual hardware step and has
not been executed here.

Then select that board's serial port explicitly and run the same bring-up checks:

```sh
WASMETAL_SERIAL=/dev/serial/by-id/your-board \
  python3 tools/check_fpga.py --simulator build/wasmetal-fpga
```

The adapter uses exclusive access, raw 8N1 at 500,000 baud, no flow control and
bounded I/O waits. It does not discover or open a device without `WASMETAL_SERIAL`.
It does not retry a potentially executed instruction after a lost response.

The official runner can use that same executable with `--simulator`. UART
single-stepping is deliberately slow; the full corpus contains hundreds of
millions of clock cycles and is not a quick physical bring-up test.

## Clocking and transport

The 25 MHz board oscillator feeds a free-running divide-by-two flip-flop. A DCCA
routes its 12.5 MHz output to the UART and bridge. A second DCCA routes the manual
CPU clock onto a global clock network. Each accepted step holds new inputs stable
for 8 microseconds before the CPU edge, holds its pulse high for 2 microseconds,
then waits at least 4 microseconds before sampling outputs. An evaluation request
changes inputs and samples combinational outputs without a CPU edge.

The build checks all three clock constraints and separately audits both directions
of the held-bus crossing. It requires each cross-domain path to settle within a
conservative 1 microsecond budget, below the protocol's actual hold times. This
does not replace the same-clock timing checks or introduce timing waivers.

Requests contain `57 4d`, flags, sequence, 106 input bytes and a little-endian
CRC16-CCITT-FALSE. Responses contain `57 52`, status, sequence, 67 output bytes and
the same CRC. The CRC covers flags/status, sequence and payload. Flag 0 evaluates,
flag 1 steps, flag 2 reads capabilities; flag 3 is invalid. `fpga/ports.json`
defines packed bit positions; generated headers bind the C++ and RTL layouts.

The error LED indicates a bad or timed-out frame; the busy LED reflects CPU
execution. The board button resets the transport. The host explicitly clocks a
CPU reset during initialization.

## Next hardware stages

Physical-board testing is still required. A practical standalone machine also
needs buffered program loading, local memory and fetch controllers, larger operand
storage in block RAM or external RAM, autonomous clocking, and a boot interface. Those
changes need their own conformance runs and timing closure. An ASIC additionally
requires a process/PDK, memories, I/O and clock/reset integration, physical design,
signoff and fabrication; the FPGA bitstream is not an ASIC deliverable.
