# Freestanding C on WasMetal

`crc32.c` is compiled by Clang to an ordinary Wasm module. The existing software
loader validates it and converts it to the prepared instruction, metadata and
initialization stores consumed by the hardware. The CPU executes those prepared
records; this does not add a raw Wasm binary parser to the RTL.

The program needs no imports, libc, operating system or allocator. It fills a
volatile 1,024-byte buffer with repeating bytes 0 through 255 and calculates
CRC-32. Volatile accesses retain the memory writes and reads in the generated
program. An oversized input returns `UINT32_MAX`.

Install `clang-18` and `lld-18`, then run:

```sh
make sim
python3 tools/build_loadable_sim.py
python3 tools/check_c_workload.py
```

The five inputs are 0, 1, 256, 1,024 and 1,025. Python's `zlib.crc32` supplies
independent expectations for the valid lengths. The linked module has one
64 KiB memory page and a 16 KiB stack reservation. The current Clang 18.1.3
output prepares into 228 instruction records, two functions and seven boot
records, allocating 81,936 bytes in the bounded backing pool.

For the mapped comparison, first build the complete programmable circuit:

```sh
make standalone-core loadable-mapped-build
python3 tools/check_c_workload.py --mapped
```

Both models execute uploads through their UART pins. The checker requires
identical packets, serial responses, result values and cycle counts for each
input. It saves partial progress and stops on a discrepancy. Compiler and linker
versions, executable hashes, commands and the resulting Wasm hash are recorded;
LLVM's major version is selected, but its package patch version is not pinned.
CI compiles once and uses that same Wasm file for both models.

The generated files are under `build/c-workload`, and reports are
`reports/c-workload-rtl.json` or `reports/c-workload-mapped.json`. After loading a
verified [programmable bitstream](../../docs/PROGRAM-UPLOAD.md) onto a board, the
1,024-byte workload can be uploaded with:

```sh
python3 tools/upload_program.py build/c-workload/image-1024 --device /dev/ttyUSB0
```

Its result is `0xb70b4c26`. No physical FPGA execution of this example has been
performed yet. Programs that need WASI, other imports, more memory or a larger
prepared image need additional runtime or capacity support.
