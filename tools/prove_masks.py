#!/usr/bin/env python3
"""Exhaustive symbolic equivalence of the optimized HardFloat mask helpers."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent


def main():
    # Every specialization in WasMetal's elaborated f32/f64 arithmetic, plus
    # boundary cases including a threshold equal to 2**input_width.
    cases = {("lowMaskHiLo", 3, 7, 0), ("lowMaskHiLo", 4, 14, 0),
             ("lowMaskLoHi", 9, 105, 130), ("lowMaskLoHi", 12, 972, 1026)}
    for width in range(1, 5):
        for lo in range(1 << width):
            for hi in range(lo+1, (1 << width)+1):
                cases.add(("lowMaskHiLo", width, hi, lo))
                cases.add(("lowMaskLoHi", width, lo, hi))
    lines = ["module mask_equivalence(input [11:0] x);"]
    for index, (kind, width, top, bottom) in enumerate(sorted(cases)):
        n = abs(top-bottom)
        lines.extend([
            f"wire [{n-1}:0] actual_{index}, expected_{index};",
            f"{kind} #({width},{top},{bottom}) a{index}(x[{width-1}:0],actual_{index});",
            f"{kind}_reference #({width},{top},{bottom}) b{index}(x[{width-1}:0],expected_{index});",
            f"always @* assert(actual_{index} == expected_{index});",
        ])
    lines.append("endmodule")
    directory = ROOT / "build/proofs"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "mask_equivalence.sv").write_text("\n".join(lines)+"\n")
    script = """read_verilog -formal -sv third_party/hardfloat/source/HardFloat_primitives.v tests/rtl/hardfloat_mask_reference.v build/proofs/mask_equivalence.sv
prep -top mask_equivalence -flatten
sat -prove-asserts -verify
"""
    (directory / "masks.ys").write_text(script)
    with (directory / "masks.log").open("w") as output:
        subprocess.run([str(ROOT / ".cache/tools/usr/bin/yosys"), "-Q", "-T", "-s", str(directory / "masks.ys")],
                       cwd=ROOT, stdout=output, stderr=subprocess.STDOUT, check=True)
    print(f"Proved {len(cases)} mask specializations equivalent for every possible binary input.")


if __name__ == "__main__":
    main()
