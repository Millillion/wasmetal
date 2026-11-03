# Prepared-program upload

The receiver in `soc/loader/wasmetal_image_loader.sv`, writable program stores
and execution system are connected in `soc/loader/wasmetal_loadable.sv`.
`tools/upload_program.py` sends a prepared image through the board's UART,
then reads its execution result. The separate original standalone bitstream
continues to boot a fixed ROM image.

The goal is to change a program without rebuilding the FPGA bitstream. The
host still prepares and validates Wasm. This is a transport for trusted prepared
images, not a Wasm binary validator, authentication mechanism or secure boot.

## Building and using the programmable system

All 35 local RTL/mapped integration cases pass, but the programmable ULX3S
bitstream has not yet completed routing and timing verification. The
[routing snapshot](verification/loadable-routing-status.json) records the
remaining congestion and attempted placements. The commands below describe
the build and subsequent board workflow; a verified programmable bitstream
is still required before physical acceptance testing.

```sh
python3 tools/bootstrap.py --fpga-tools
make loadable-bitstream
make sim
python3 tools/prepare_standalone.py examples/standalone/selftest.wat --output build/program-image
```

A successful build writes `build/loadable-ulx3s/wasmetal.bit`. It contains the complete
CPU and writable storage, with no prepared program embedded. Follow the board
connection and volatile-SRAM loading procedure in the [FPGA guide](FPGA.md),
using this bitstream path. Once it is running on the correct board:

```sh
python3 tools/upload_program.py build/program-image --device /dev/ttyUSB0
```

For repeated checks of 25 programs against their simulated results and cycle
counts, use the [board acceptance runner](BOARD-ACCEPTANCE.md).

No physical board has been programmed or tested by this work. The existing
ULX3S clock divider and 9600-baud connection are retained. The busy LED stays on
while waiting for an image, receiving it, clearing backing RAM and executing;
it turns off after a complete result is transmitted. An execution failure lights
the error LED. Upload rejection is reported through the serial reply.

The CPU stays in reset while the loader writes the instruction, function,
type, region and boot stores. A successful commit releases execution; boot then
clears the backing pool and applies the uploaded initialization records. The
same FPGA configuration can accept another program after completion. Reset
revokes execution permission and requires another upload.

The full padded image is about 55.6 kB and takes roughly 58 seconds over a
9600-baud 8N1 link, before execution. The uploader's default overall timeout is
120 seconds; `--timeout` can change it. This first implementation prioritizes a
checked boot path. Transfer compression, faster serial rates and external RAM
are future improvements. Profile limits and the no-import requirement in the
[standalone guide](STANDALONE.md) also apply here.

## Image and handshake

All integer fields and words are little-endian. Send the 33-byte header first,
wait for the matching `ready` reply, then send the payload and its four-byte CRC.
An upload attempt has a fresh random 64-bit nonce; replies echo it so an old
response cannot be mistaken for the current attempt.

| Header field | Bytes |
| --- | ---: |
| ASCII `WMLD` | 4 |
| Protocol version, currently 1 | 1 |
| Nonce | 8 |
| Hardware profile tag | 16 |
| Payload byte count | 4 |

The tag is the first 16 bytes of SHA-256 over
`b'WasMetal prepared image upload v1\0'` followed by the hardware profile encoded
as sorted-key, compact JSON. It binds core capacities, store dimensions and
the other profile settings. The RTL receives the corresponding little-endian
128-bit parameter. An unconfigured zero parameter rejects every header.

The payload contains every row, including zero padding, in this order:

| Section | Row width | Current rows | Current bytes |
| --- | ---: | ---: | ---: |
| Instructions | 288 bits | 1,024 | 36,864 |
| Functions | 160 bits | 128 | 2,560 |
| Type relationships | `type_depth` bits | 64 | 512 |
| Memory regions | 64 bits | 96 | 768 |
| Boot records | 232 bits | 512 | 14,848 |

The current total is **55,552 bytes**, or 1,824 store writes. Type rows are
padded to whole bytes. A full layout prevents remnants of a previous larger
program from surviving in an unused row. The encoder checks file fingerprints,
row counts and word widths before producing a packet.

CRC-32/IEEE covers the version, nonce, profile, length and complete payload,
excluding the four magic bytes. It uses reflected polynomial `0xedb88320`,
initial state `0xffffffff` and final complement, matching Python `zlib.crc32`.
The checksum trailer is four bytes, little-endian.

For inspection or offline transport preparation:

```sh
python3 tools/program_upload.py build/standalone-image --output build/selftest.wmu
```

The output file contains header, payload and checksum. **Do not send it as one
uninterrupted stream:** the receiver waits for the ready reply to be transmitted
before it accepts payload bytes.

`tools/upload_program.py` implements this handshake on a POSIX serial device at
9600 baud, then decodes the execution result. It checks the echoed nonce and
committed checksum, preserves a result arriving with the acknowledgment, imposes
an overall deadline and restores terminal settings. Its pseudo-terminal tests
exercise fragmented, corrupt and stale replies, rejection, timeout and cleanup.
The existing ROM bitstream does not accept this protocol; use the programmable
bitstream above.

## Reply and recovery

A reply is 20 bytes: ASCII `WMLR`, version (1 byte), status (1 byte), nonce
(8 bytes), image checksum (4 bytes), and CRC-16/CCITT-FALSE (2 bytes). The reply
CRC covers version through image checksum, starting at `0xffff` with polynomial
`0x1021`. The image checksum is zero except for `committed` and `checksum` replies.
The decoder checks framing, version, status, reserved values and CRC.

| Status | Meaning |
| ---: | --- |
| 0 | Ready to receive the payload |
| 1 | Complete image checksum accepted |
| 2 | Unsupported version |
| 3 | Wrong or unconfigured hardware profile |
| 4 | Wrong payload length |
| 5 | Payload checksum mismatch |
| 6 | Inter-byte timeout |
| 7 | Aborted |

Recognizing the complete `WMLD` prefix invalidates the previous image. The CPU
must remain in reset whenever `image_valid` is low. Each assembled word produces
one `word_valid` pulse and must be accepted by its selected store on that clock
edge; this interface has no write backpressure. Partial words are not written.
Execution permission is granted only after the full payload and checksum pass
and the transmitter accepts the last committed-reply byte. That is a local
transmit handshake, not confirmation that a remote host received the reply.

This provides atomic authorization to execute a complete image. It does not
preserve or roll back to the previous program: a failed attempt leaves the CPU
reset until a new successful upload. Reset also revokes execution permission,
even if the store contents remain physically present.

The default inter-byte timeout is 2,000,000 receiver clocks. At 781.25 kHz that
is 2.56 seconds. Header, payload and checksum timeouts discard the attempt.
Partial magic prefixes also expire. A dedicated `abort_load` input immediately
revokes permission and discards the attempt; UART framing errors/break trigger
it in the assembled system. Transmit backpressure holds a reply indefinitely
without granting permission early. Unexpected bytes during reply transmission
are ignored; the host must observe the two-phase handshake.

## Verification

Run `make image-loader-test`. CI preserves the reports and logs.

- [Native and mapped tests](verification/image-loader-mapped.json) cover a
  404-byte small layout and the full 55,552-byte layout. Each configuration
  commits 27 complete images across repeated uploads and checks 159 replies and
  24 resets. Production tests compare 80,537 store writes against an independent
  byte oracle over 4,439,611 cycles. Both models agree exactly.
- A production-layout packet from the Python encoder also passes both models,
  checking 1,824 writes. Python's `zlib` and `binascii` implementations provide
  independent checksum checks; C++ checks standard known CRC vectors as well.
- Mutated replies and store data must fail the respective independent oracles.
  Cases cover bad versions/profiles/lengths/CRCs, pauses, held replies, timeout
  in each receive phase, every first-word byte interruption, section boundaries,
  explicit abort and reset before commit acknowledgment.
- [Four-state RTL tests](verification/image-loader-four-state.json) start with
  unknown registers, upload a complete valid image, then inject an unknown
  payload byte and require rejection. Removing permission reset or the checksum
  gate makes a negative control fail.
- [Unbounded induction](verification/image-loader-proof.json) proves store
  bounds, defined registers after reset, exclusion of writes to an executable
  image, and authorization requiring the complete word count and matching
  received/accumulated checksum. Both small and production capacities pass;
  production uses the actual 2,000,000-clock timeout. After initial reset, bytes,
  strobes, aborts, transmit backpressure and later resets are arbitrary binary
  inputs. Reachable-state lemmas are proved jointly. Missing word reset and
  premature execution permission make negative controls fail. This is not
  complete CRC/data equivalence or CPU-level correctness.

These component checks are supplemented by the complete-system integration
flow:

```sh
make loadable-test
make loadable-mapped-test
```

The integration runner uses UART pins, reset and public completion signals.
It uploads 25 programs into the same running simulator, including high
instruction/function/boot addresses, every segment slot and type-matrix bits
that must change from true to false on replacement. Ten additional cases cover
rejection, interrupted transfers, reset, timeout, UART break, recovery and
independent serial periods of 98% and 102% of nominal. The board-clock tests
retain the actual divider and UART timing; core-level integration accelerates
UART to four clocks per bit and the receive timeout to 4,096 clocks.
The [board-rate checks](verification/loadable-board-rates.json) pass at 98%,
100.5% and 102% of the board's nominal bit period. The middle setting closely
matches a 9600-baud sender against the board's approximately 9645-baud UART.

The [mapped I/O audit](verification/loadable-io.json) checks both stages of the
UART and reset synchronizers, their clocks and reset polarity, exclusive
first-stage fanout and the permanently enabled core-clock buffer. Seven
deliberately broken circuits are rejected. This checks digital structure;
it does not establish analog metastability reliability or physical placement.

Mapped verification uses six independently assigned groups. The final merge
requires all 35 integration cases, the same circuit and simulator identities, and exact
agreement with native UART bytes, execution results and clock counts. Type
replacement cases remain together in one simulator. Missing or duplicated
groups, native-model substitution, changed simulator binaries and incorrect
results/clocks are rejected. The [completed comparison](verification/loadable-mapped.json)
passes all 35 cases and seven negative controls, preserving both simulator
identities and checker source hashes in the merged receipt.
These are bounded integration cases, separate from the 259-suite official
host-backed corpus.
CI builds the mapped simulator independently of board routing so routing
congestion cannot postpone execution testing. The final integration job
requires native tests, every mapped group, the compiled C workload and board
routing to succeed. The programmable bitstream has not yet completed routing;
passing the mapped execution campaign does not establish physical routability.

The new [RAM-model checks](verification/loadable-ram.json) cover all 1,024
addresses and four write masks in 18-bit mode, and all 512 addresses and 16
masks in 36-bit mode. They test initialization, opposite and same clock edges,
read enables, unknown addresses, read-before-write and collision behavior.
An independent combinational proof on the actual mapped region memories
excludes simultaneous reads and writes. Mutated read data, ignored masks and
disabled read protection must fail. This is functional primitive verification;
physical setup/hold timing and electrical behavior still require their own
checks. See Lattice's [ECP5 memory guide](https://www.latticesemi.com/-/media/LatticeSemi/Documents/ApplicationNotes/EH/FPGA-TN-02204-1-6-ECP5-and-ECP5-5G-Memory-Usage-Guide.ashx?document_id=50466)
for the primitive behavior and collision restrictions.
