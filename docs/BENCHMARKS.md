# Reproducible workload measurements

`tools/benchmark_standalone.py` prepares the committed Wasm workloads, runs each
twice across reset through the standalone RTL's UART, and checks the answers
against Python arithmetic or `zlib.crc32`. It also checks the prepared program
against the host-backed execution model. The [measurement record](verification/benchmarks.json)
includes source, executable, image and profile fingerprints.

```sh
make sim standalone-sim
python3 tools/benchmark_standalone.py
```

| Workload | Useful work | Invocation cycles |
| --- | ---: | ---: |
| CRC-32, empty input | 0 bytes | 36 |
| CRC-32 | 256 bytes | 80,651 |
| CRC-32 | 1,024 bytes | 321,817 |
| Scalar integer dot product | 64 multiply-accumulates | 3,126 |
| Scalar integer dot product | 1,024 multiply-accumulates | 49,596 |
| SIMD integer dot product | 64 multiply-accumulates | 1,454 |
| SIMD integer dot product | 1,024 multiply-accumulates | 21,524 |

These are simulated core invocation cycles. They exclude program preparation,
serial upload, backing-memory clearing, boot records and result transmission.
They are not host simulator speed measurements or physical-board measurements.
The dot-product comparison uses the same two input vectors and arithmetic;
the SIMD implementation processes four elements per loop iteration. Its larger
case uses about 2.30 times fewer invocation cycles. This is a workload result,
not a general SIMD speedup guarantee.

The CRC implementation uses the direct bit-at-a-time algorithm. The dot
products use wrapping 32-bit integer arithmetic. All workloads fit the current
bounded local-memory profile; they do not exercise external DDR or reclaiming
garbage collection. The report also records instruction/boot counts, allocated
backing memory and complete UART observations.

Use these baselines to evaluate a specific change to instruction latency,
memory access, SIMD sequencing or generated code. Preserve the answer and
report both execution cycles and memory cost. An algorithm change, a different
input size and a microarchitecture change should be identified separately.
