# Checking 7-series DSP arithmetic

The complete programmable system maps to 29 DSP48E1 blocks. These are the FPGA's
dedicated arithmetic blocks, used for multiplication and for combining partial
products into wider results. Checking their behavior is a prerequisite for
trusting a simulation of the complete mapped CPU.

The [recorded regression](verification/xc7-dsp.json) covers every configuration
present in the corrected system netlist. It runs the same independent integer
oracle against four simulations: the unmodified Xilinx model in Icarus, the
original Yosys model in Icarus, and the model with explicit carry connections
in both Icarus and Verilator. All 87,040 vectors per
model pass. The original logs are preserved beside the receipt.

| A input | B input | OPMODE | Added value | Instances | Vectors per model |
|---|---|---:|---|---:|---:|
| Direct | Direct | 5 | Zero | 9 | 17,408 |
| Cascade | Direct | 85 | Signed PCIN shifted right 17 bits | 16 | 17,408 |
| Direct | Direct | 21 | PCIN | 1 | 17,408 |
| Direct | Cascade | 85 | Signed PCIN shifted right 17 bits | 1 | 17,408 |
| Direct | Direct | 53 | C | 2 | 17,408 |

All pipeline registers are disabled in this mapping. The oracle treats the
selected A operand as a signed 25-bit number and B as a signed 18-bit number,
adds the selected 48-bit operand, and retains the low 48 result bits. It also
checks the full A and B cascade outputs and the product cascade output. These
are all output types consumed by the current mapped system.

Each configuration gets 640 combinations of arithmetic boundaries, 384 walking
bit/complement cases across all data inputs, and 16,384 deterministic random
cases. Comparisons occur before, on and after clock edges while reset and
enable inputs toggle. These toggles must not introduce latency or gating into
the unregistered configurations.

The complete-system simulator uses three explicit bit connections for the
standard model's `int_carry_in[3:1] = int_carry_out[2:0]` assignment. These
represent the same wires, while allowing Verilator to schedule each carry
separately. `tools/xc7_dsp_model.py` requires an exact recognized source anchor
before producing this private simulation copy. The original library remains
the reference, and the candidate repeats the full arithmetic regression.

Six real simulated faults must fail: choosing the wrong A or B cascade source,
omitting the cascade shift, adding a carry, flipping a product bit, and losing
the product cascade output. Eight structural controls reject a new registered
mode, nonzero carry, variable or unsupported operation, unsupported A source,
extra parameter, missing DSP, and consumption of an unverified output type.
The configuration inventory is checked against the actual synthesized circuit;
future changes require review.

The reference source is the unmodified, Apache-licensed
[DSP48E1 model](https://github.com/Xilinx/XilinxUnisimLibrary/blob/1c8e05fd1e9a79ceb8b996a0996674122eed086f/verilog/src/unisims/DSP48E1.v).
Its Git blob identity and SHA-256 hash are pinned separately in
`third_party/xilinx-unisim/DSP48E1.UPSTREAM.json`. The original upstream notices
and license are preserved. The parent library's README identifies Vivado 2020.1.

After the complete-system estimate:

```sh
python3 tools/check_xc7_dsp.py
```

CI runs this check after synthesis and preserves the receipt, generated traces,
fixtures, binaries and original logs. The check is limited to known input data
and the unregistered configurations listed above. It does not establish
four-state DSP equivalence, timing, complete CPU correctness or physical-board
operation. See the separate [RAM checks](XILINX-MEMORY.md) for memory models.
