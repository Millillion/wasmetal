#!/usr/bin/env python3
"""Synthesis elaboration/consistency gate; does not claim FPGA fit or timing."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fpga", action="store_true", help="also map a reduced-capacity core to ECP5 primitives")
    args = parser.parse_args()
    (ROOT / "build").mkdir(exist_ok=True)
    vendor = ROOT / "third_party/hardfloat/source"
    sources = sorted(vendor.glob("*.v")) + [vendor / "RISCV/HardFloat_specialize.v"] + sorted((ROOT / "rtl").glob("*.sv"))
    script = "read_verilog -sv -Ithird_party/hardfloat/source -Ithird_party/hardfloat/source/RISCV "
    script += " ".join(str(p.relative_to(ROOT)) for p in sources) + "\n"
    if args.fpga:
        script += "chparam -set VALUE_DEPTH 256 -set CONTROL_DEPTH 128 -set CALL_DEPTH 64 -set MEMORY_COUNT 16 wasmetal_core\n"
        script += "synth_ecp5 -top wasmetal_core -json build/core-ecp5.json\ncheck -assert\nstat\n"
    else:
        script += "hierarchy -check -top wasmetal_core\nproc\nopt\nmemory_collect\ncheck -assert\nstat\n"
        script += "write_json build/core-generic.json\n"
    path = ROOT / "build/synth.ys"
    path.write_text(script)
    yosys = ROOT / ".cache/tools/usr/bin/yosys"
    log = ROOT / ("build/synth-ecp5.log" if args.fpga else "build/synth.log")
    with log.open("w") as stream:
        result = subprocess.run([str(yosys), "-Q", "-T", "-s", str(path)], cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
    print(log.read_text()[-6000:])
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
