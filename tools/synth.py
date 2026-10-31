#!/usr/bin/env python3
"""Synthesis elaboration/consistency gate; does not claim FPGA fit or timing."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fpga", action="store_true", help="also map the configured FPGA core to ECP5 primitives")
    parser.add_argument("--fast-share", action="store_true", help="use bounded-control resource-sharing analysis")
    parser.add_argument("--no-share", action="store_true", help="retain parallel arithmetic resources")
    mapping=parser.add_mutually_exclusive_group()
    mapping.add_argument("--lut4",action="store_true",help="map directly to four-input LUTs")
    mapping.add_argument("--abc9",action="store_true",help="use ECP5 LUT timing models with a 500 ns combinational target")
    parser.add_argument("--value-depth", type=int)
    parser.add_argument("--output-name")
    parser.add_argument("--top",default="wasmetal_core")
    args = parser.parse_args()
    name = args.output_name or ("core-ecp5" if args.fpga else "core-generic")
    if not name.replace("-", "").replace("_", "").isalnum() or not args.top.replace("_", "").isalnum() or (args.value_depth is not None and args.value_depth < 1):
        parser.error("invalid output name or value capacity")
    (ROOT / "build").mkdir(exist_ok=True)
    vendor = ROOT / "third_party/hardfloat/source"
    sources = sorted(vendor.glob("*.v")) + [vendor / "RISCV/HardFloat_specialize.v"] + sorted((ROOT / "rtl").glob("*.sv"))
    profile=json.loads((ROOT/"fpga/profile.json").read_text())
    if args.value_depth is not None: profile["VALUE_DEPTH"]=args.value_depth
    script = "read_verilog -sv -Ithird_party/hardfloat/source -Ithird_party/hardfloat/source/RISCV "
    script += " ".join(str(p.relative_to(ROOT)) for p in sources) + "\n"
    if args.fpga:
        if args.top=="wasmetal_core":
            script += "chparam "+" ".join(f"-set {key} {value}" for key,value in profile.items())+" wasmetal_core\n"
        if args.fast_share or args.no_share or args.lut4 or args.abc9:
            # Pinned Yosys 0.33 ECP5 flow with its documented fast sharing heuristic.
            script += """synth_ecp5 -top wasmetal_core -run begin:begin
proc
flatten
tribuf -logic
deminout
opt_expr
opt_clean
check
opt -nodffe -nosdff
fsm
opt
wreduce
peepopt
opt_clean
share -fast
techmap -map +/cmp2lut.v -D LUT_WIDTH=4
opt_expr
opt_clean
techmap -map +/mul2dsp.v -map +/ecp5/dsp_map.v -D DSP_A_MAXWIDTH=18 -D DSP_B_MAXWIDTH=18 -D DSP_A_MINWIDTH=2 -D DSP_B_MINWIDTH=2 -D DSP_NAME=$__MUL18X18
chtype -set $mul t:$__soft_mul
alumacc
opt
memory -nomap
opt_clean
"""
            # Yosys -run uses an exclusive end label. Keep check/autoname out
            # of the timed mapping path, but include primitive-cell mapping.
            if args.lut4 or args.abc9:
                mapper="abc9 -D 500000 -W 300" if args.abc9 else "abc -dress -lut 4"
                script += "synth_ecp5 -top wasmetal_core -run map_ram:map_luts\ntechmap -map +/ecp5/latches_map.v\n"+mapper+"\nclean\nsynth_ecp5 -top wasmetal_core -run map_cells:check\n"
            else:
                script += "synth_ecp5 -top wasmetal_core -run map_ram:check\n"
            script += f"hierarchy -check\nblackbox =A:whitebox\ncheck -assert\nstat\nwrite_json build/{name}.json\n"
            if args.no_share:
                script = script.replace("share -fast\n", "")
        else:
            script += f"synth_ecp5 -top wasmetal_core\ncheck -assert\nstat\nwrite_json build/{name}.json\n"
    else:
        script += "hierarchy -check -top wasmetal_core\nproc\nopt\nmemory_collect\ncheck -assert\nstat\n"
        script += f"write_json build/{name}.json\n"
    path = ROOT / f"build/{name}.ys"
    script=script.replace("-top wasmetal_core","-top "+args.top)
    path.write_text(script)
    inputs=sources+sorted(vendor.rglob("*.vi"))+[ROOT/"tools/synth.py",ROOT/"tools/upstream.lock.json"]
    if args.fpga: inputs.append(ROOT/"fpga/profile.json")
    manifest={"top":args.top,"arguments":vars(args),"inputs":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
              "script_sha256":hashlib.sha256(path.read_bytes()).hexdigest()}
    yosys = ROOT / ".cache/tools/usr/bin/yosys"
    log = ROOT / f"build/{name}.log"
    with log.open("w") as stream:
        result = subprocess.run([str(yosys), "-Q", "-T", "-s", str(path)], cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
    print(log.read_text()[-6000:])
    if result.returncode==0:
        for source_name,digest in manifest["inputs"].items():
            if hashlib.sha256((ROOT/source_name).read_bytes()).hexdigest()!=digest:
                raise RuntimeError("synthesis input changed during build: "+source_name)
        output=ROOT/f"build/{name}.json"
        manifest["netlist_sha256"]=hashlib.sha256(output.read_bytes()).hexdigest()
        (ROOT/f"build/{name}.manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
