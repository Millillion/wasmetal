# Prepared-program upload

The byte-level receiver in `soc/loader/wasmetal_image_loader.sv` and the encoder
in `tools/program_upload.py` implement the protocol below. CPU, writable-store
and UART integration is in progress. The current standalone bitstream still
boots its prepared ROM image; this component alone does not enable board upload.

The goal is to change a program without rebuilding the FPGA bitstream. The
host still prepares and validates Wasm. This is a transport for trusted prepared
images, not a Wasm binary validator, authentication mechanism or secure boot.

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
CPU and board integration is still in progress; the existing ROM bitstream does
not accept this protocol.

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
revokes permission and discards the attempt; UART integration will use framing
errors/break to trigger it. Transmit backpressure holds a reply indefinitely
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

These are component checks. They do not establish execution on a CPU, serial
timing tolerance, writable-memory mapping, routed timing or physical operation.
