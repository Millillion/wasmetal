# Xilinx Unisim block-RAM reference models

These are unmodified files from [XilinxUnisimLibrary at
1c8e05fd1e9a79ceb8b996a0996674122eed086f](https://github.com/Xilinx/XilinxUnisimLibrary/tree/1c8e05fd1e9a79ceb8b996a0996674122eed086f).
The original [README](UPSTREAM_README.md) identifies the library as corresponding
to Vivado 2020.1. Its [Apache 2.0 license](LICENSE) and source copyright notices
are preserved. No WasMetal production logic is licensed or relicensed by these
simulation-only dependencies.

`RAMB18E1.v`, `RAMB36E1.v`, and `glbl.v` provide an independent, four-state
reference for testing the project's 7-series memory mapping. The installed
Yosys library supplies logic primitives, but its empty block-RAM shells must
not be used as functional RAM models.

[UPSTREAM.json](UPSTREAM.json) records upstream paths, the pinned revision,
Git blob identities and SHA-256 digests. The regression checks those identities
before and after simulation. Preserve the original bytes, including upstream
whitespace; place WasMetal adaptations in separate files.

Run `python3 tools/check_xc7_memory_mapping.py` from the repository root after
tool bootstrap. Primitive simulation does not establish FPGA timing, complete
CPU correctness or a working board port.
