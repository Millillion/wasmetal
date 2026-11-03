# Programmable board acceptance

The acceptance runner is prepared for the first physical board. It has not
been run on an FPGA. Its host logic passes nine tests, including 50 complete
uploads through a pseudo-terminal with a software peer. The
[preparation receipt](verification/board-acceptance-preparation.json) verifies
that all 25 prepared upload packets match programs already executed by the
native RTL simulation.

## Prepare before connecting a board

```sh
make loadable-test
```

This creates `build/board-acceptance/plan.json`, the prepared images and a copy
of the completed native reference. CI retains them in the `loadable-acceptance`
artifact. To regenerate the plan from an existing current native report:

```sh
python3 tools/board_acceptance.py prepare
```

The plan preserves program order, including the type-subtyping replacement
that changes a previously true matrix bit to false. It covers arithmetic,
floating point, SIMD, memory64, unaligned accesses, references, tail calls,
exceptions, traps, capacity exhaustion, the watchdog and high store addresses.
It checks exact result values, status, trap and invocation cycle counts.
These 25 programs are bounded system checks, separate from the full official
host-backed Wasm corpus and the ten simulated protocol/reset recovery cases.

## Run after programming the board

Use the [programmable build](PROGRAM-UPLOAD.md) and the correct board's
[connection and volatile programming procedure](FPGA.md). The completed build
must provide both `wasmetal.bit` and its verified `manifest.json`.

```sh
python3 tools/board_acceptance.py run \
  --device /dev/ttyUSB0 \
  --hardware --board-label "ULX3S 85F, board serial or personal identifier" \
  --bitstream-manifest build/loadable-ulx3s/manifest.json \
  --report reports/board-acceptance-first-board.json
```

Choose the serial device explicitly. The default is two passes through all 25
programs, changing programs without rebuilding or reprogramming the FPGA.
At 9600 baud, allow approximately 50 minutes, mostly for image transfers.
`--repetitions 1` runs one pass; `--timeout` sets the deadline for each upload
and result, defaulting to 120 seconds.

Every transfer uses a fresh nonce and the normal checked ready/commit protocol.
The runner validates all prepared inputs before the first transfer and checks
them again at completion. It stops on the first discrepancy or connection
failure and saves completed cases, the failing observation when available,
and the active program in the report. Reports must be outside the prepared
plan and bitstream directories so progress cannot overwrite those inputs.

`--hardware` records the operator's statement that a physical board is being
tested; it requires a board label and bitstream manifest and rejects a
pseudo-terminal. Without it, a run is recorded as a serial transport test.
The manifest identifies the intended bitstream and verifies the local file.
It is not a readback or attestation of the FPGA's actual configuration.

## Physical checks still needed

Record cold power-on behavior and repeat the campaign after power cycling.
Check reset during upload, execution and result transmission, followed by a
fresh upload. Inspect clock, reset and UART behavior on the actual board,
including supply stability, cable reliability and sustained operation.
Keep the board identity, source revision, bitstream manifest and measurements
with the resulting report. Passing this campaign establishes those observed
board results; ASIC timing, memory-macro and manufacturing signoff remain
separate work.
