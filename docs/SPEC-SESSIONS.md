# Official scripts on the programmable system

The host-backed conformance runs prove the CPU executes every pinned official
suite while the host supplies instructions and memory. That path does not
carry over to a board: single-stepping hundreds of millions of cycles over a
USB-UART would take days. A **session** instead runs a whole official script
on the programmable system itself.

## How a session is built

`tools/spec_session.py` runs each `.wast` script through the unchanged native
runner (`tools/run_spec.py`) and records its exact transcript: every loader
command and every response. `spectest` is itself a Wasm module in the same
store, so a script needs no host calls. The transcript becomes one prepared
image:

- loader setup (instructions, functions, types, descriptors, data/element
  segments, globals and memory bytes) is replayed by the boot sequencer, as in
  ordinary prepared images;
- every execution (`R`: initializers, start functions and every invocation of
  every assertion) becomes a **reported execution** (boot mode 4);
- every global read (`H`) and memory/table size query (`S`) becomes a
  **reported query** (boot mode 5).

The device reports each one as a separate UART frame and continues, including
after traps, which `assert_trap` expects. Session frames are kind 2 (result)
and kind 3 (end); each carries the boot-record index, so a dropped, repeated or
reordered frame is detected. The single-invocation frame (kind 1) is
unchanged.

The checker requires, in order, one frame per reporting record with exactly
the native status, trap code and 128-bit values. The native responses already
satisfy every official assertion, so a session that matches is the official
script executing on the device.

## Physical capacity

A memory's or table's physical maximum is set to the peak size the script
reached natively (its final size, since neither ever shrinks). Every growth
that succeeded natively stays within that size, and every growth that failed
natively still exceeds it, so behavior is identical with no wasted RAM.
Sessions upload in the [compact format](PROGRAM-UPLOAD.md#compact-uploads-version-2).

## Running

```sh
WASMETAL_PROFILE=soc/profiles/corpus.json python3 tools/build_loadable_sim.py
WASMETAL_PROFILE=soc/profiles/corpus.json python3 tools/spec_session.py \
  --binary build/loadable-sim-corpus/Vwasmetal_loadable --report reports/spec-sessions.json
```

`--native-only` stops after packing each session, which measures the storage
every suite needs without device simulation.
[`soc/profiles/corpus.json`](../soc/profiles/corpus.json) is a
simulation-sized profile with the native corpus's core capacities; a board
profile must fit its memories.

## Running sessions on a board

`spec_session.py` saves each suite's compact upload (`session.wmu`) and the
frames the device must report (`expected.json`) under
`build/spec-sessions/<profile>/<suite>/`. On the board machine, with the
matching bitstream loaded:

```sh
python3 tools/board_sessions.py --device /dev/serial/by-id/your-board \
  --sessions build/spec-sessions/genesys2 --report reports/board-sessions.json
```

It uploads each session, reads every frame until the end frame and requires
each to equal its expectation, writing results as suites complete. It needs
no simulator. Its [test](../tests/board_sessions_test.py) drives a fake board
on a pseudo-terminal: a passing session, a wrong value, a missing frame, an
error frame, a corrupted frame followed by a valid one, and a missing end
frame.

## Results so far

- The [packing measurement](verification/spec-sessions-packed.json) prepares
  all 259 suites as peak-sized sessions. Excluding the heap, 243 need at most
  1 MiB of local RAM, 249 at most 2 MiB and 255 at most 4 MiB; `memory_grow`,
  `memory64/memory_grow64`, `call` and `call_indirect` need 35-52 MiB.
- [`i32` passes on the device](verification/spec-session-i32.json): all 378
  reported executions equal the native responses, in 2,308,863 system clocks
  including upload, startup clear and UART reporting. This run used the small
  [`session-debug`](../soc/profiles/session-debug.json) profile (1 MiB RAM).
  A run with the 128 MiB `corpus` profile spent most of its time clearing RAM
  at startup and was stopped; the corpus run uses the 8 MiB
  [`session`](../soc/profiles/session.json) profile, with `corpus` reserved
  for the suites that need more.
- The complete on-device corpus run is in progress.
