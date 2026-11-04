# 7-series distributed RAM verification

The [RAM64M receipt](verification/xc7-lutram.json) covers the configuration used
by all 22 distributed-RAM instances in each complete-system netlist. The
[evidence archive](verification/xc7-lutram/index.json) preserves proofs, original
oracle traces, simulation logs and negative controls. The original Xilinx file
is pinned and unmodified.

## Binary state proof

All **260 equivalence points** pass: 256 memory-state bits and four read-output
bits. Both lowered models are checked to contain exactly four 64-bit banks,
with identical all-zero initial values and complete coverage of every state
bit. Induction proves the state transition, and combinational checks prove the
read outputs. A wrong write-address bit fails the proof; a wrong initial bit
fails the initial-state audit.

The proof has an explicit **binary write-enable** assumption. The vendor
expression `(WE === 1'bz) || WE` becomes `WE` for the proof only. Its original
expression is exhaustively checked in Icarus for all four states, including
agreement with `WE` at zero and one. The checker verifies that this one
specialization and the module rename are the only behavioral-source changes.
It does not assert an unrestricted four-state equivalence. The original vendor
file, including its Z-enable behavior, is used for the independent simulations.

Vendor unit delays are ignored by this untimed proof. This is a proof of a
binary primitive model, not placed/routed circuit timing or silicon behavior.

## Independent memory oracles

Two binary initialization patterns pass **74,368 observations per model**:
the Yosys and vendor models in Icarus, and the Yosys model in Verilator. A
separate four-state run passes **143,744 observations per library** in Icarus.
The Python oracle maintains four separate banks for each model, rather than
copying the implementation's packed-vector expressions.

Coverage includes all 64 write addresses and data combinations, disabled
writes, data changes without a clock edge, nonuniform bank contents, every
address pairing between read ports, and reproducible random operations. The
four-state run checks unknown initialization/data, every six-bit X/Z read
address on every port, and unknown write-address semantics. Outputs are
compared directly, preserving Z.

The vendor writes when `WE` is Z; Yosys does not. Their oracles therefore track
separate memory states, and the receipt records the resulting differences.
Both models ignore writes with an unknown selected bit index in these
simulations. That result is **not** a physical guarantee about an FPGA with an
indeterminate address. Clock inputs remain binary and observations wait for
the vendor's unit delays to settle.

## Fault controls and reproduction

Twelve proof/oracle/parser controls reject incorrect enable specialization,
wrong initial state, aliased write/read addresses, ignored enables, transparent
writes, exchanged data banks, zeroed unknown state/data, and broken trace
framing. Four inventory controls per netlist reject unsupported clock
inversion, nonzero initialization, unknown parameters and changed address
widths. The local two-netlist run rejects all twenty controls; CI now checks
both netlists with those same controls.

```sh
python3 tools/check_xc7_lutram.py --netlist build/xc7-system/mapped.json --netlist build/xc7-accelerated/mapped.json
```

These checks complement the [block RAM](XILINX-MEMORY.md),
[flip-flop](XILINX-STATE.md), [logic](XILINX-LOGIC.md),
[DSP](XILINX-DSP.md) and [complete-system](XILINX-SYSTEM-SIMULATION.md)
verification. Physical placement, timing closure and FPGA testing remain
separate requirements.
