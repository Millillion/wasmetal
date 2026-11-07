# Genesys 2 board port

This port prepares the programmable (UART-loadable) system for the Digilent
Genesys 2 (Kintex-7 XC7K325T-2FFG900C), the board recommended in the
[FPGA selection research](FPGA-SELECTION.md). **No Genesys 2 has been tested,
and the Vivado flow below has not been run in this repository.**

## What the port changes

[`wasmetal_loadable_genesys2`](../soc/loader/wasmetal_loadable_genesys2.sv)
wraps the same `wasmetal_loadable` system as the ULX3S top. The 200 MHz
differential system clock passes through an `IBUFDS` and an 8-bit counter, and
counter bit 7 drives a `BUFG`. 200 MHz / 256 is exactly the ULX3S system's
781.25 kHz CPU clock, so the CPU, UART divider (81 clocks per bit, about 9,645
baud) and upload timeout are unchanged from the verified ULX3S design. The
active-low CPU_RESET button uses the same two-stage reset synchronizer. LD0
lights while a program loads or runs, and LD1 reports an error.

[`genesys2.xdc`](../soc/loader/genesys2.xdc) takes its pins from Digilent's
Genesys 2 Rev. H master constraints: the system clock on AD12/AD11 (LVDS),
CPU_RESET on R19, the USB-UART's FPGA receive input on Y20 and transmit output
on Y23, and LD0/LD1 on T28/V19. It constrains the 200 MHz input clock and the
divided CPU clock as a generated clock, so both CPU clock edges are timed. The
asynchronous button, UART and LED signals are false paths; the design
synchronizes the inputs.

## Simulation through the board pins

```sh
python3 tools/build_loadable_sim.py --genesys2
python3 tools/check_loadable.py --board --binary build/loadable-genesys2-sim/Vwasmetal_loadable_genesys2 \
  --no-recovery --report reports/loadable-genesys2-rtl.json
```

The harness drives the differential clock, reset button and UART pins with
256 board clocks per CPU clock and real serial timing. It runs the same two
board-clock uploads as the ULX3S board check. [Both pass](verification/loadable-genesys2-rtl.json)
with the ULX3S results and cycle counts: `answer` returns 42 in 53 execution
cycles and `selftest` all twelve values in 2,005.

## Profiles

The bitstream above uses the default ULX3S-sized profile. For official-suite
sessions on the board, [`soc/profiles/genesys2.json`](../soc/profiles/genesys2.json)
sizes the stores for Genesys 2 block RAM: 1 MiB local RAM, 4,096
instructions, 8,192 boot records and 128 regions per kind. Measured with
peak-sized memories, 233 of the 259 official suites fit it; 17 of the rest
need more than 1 MiB of RAM and wait for DDR3. Build with
`WASMETAL_PROFILE=soc/profiles/genesys2.json`. A resource estimate for this
profile has not been made yet.

## Building with Vivado

Genesys 2 is covered by AMD's free Vivado Basic license. From the repository
root, with the pinned tools installed (`python3 tools/bootstrap.py`):

```sh
python3 tools/genesys2_vivado.py prepare
vivado -mode batch -log build/genesys2/vivado.log -journal build/genesys2/vivado.jou \
  -source tools/vivado/genesys2.tcl -tclargs build/genesys2
python3 tools/genesys2_vivado.py check
```

`prepare` records the exact sources, profile tag and constraint hashes.
[`genesys2.tcl`](../tools/vivado/genesys2.tcl) runs synthesis, placement,
physical optimization and routing, then writes timing, clock, methodology,
DRC and utilization reports and the bitstream. `check` accepts the build only
if no input changed since `prepare`, every timing constraint is met (setup and
hold), both clocks exist, `check_timing` finds no unclocked or unconstrained
endpoints, DRC has no errors and the bitstream exists. It writes
`reports/genesys2-vivado.json`. A first Vivado run may reveal language or
inference differences from Yosys; fix those before trusting the result.

## Before connecting the board

Run Digilent's board diagnostics first. Then program the bitstream over JTAG,
connect to the USB-UART at 9,600 baud (the bridge tolerates the design's
0.5% rate difference), and run the [board acceptance campaign](BOARD-ACCEPTANCE.md)
against that serial port. Simulation, a timing-clean Vivado build and a
physical board run are separate milestones.
