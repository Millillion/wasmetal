#!/usr/bin/env python3
"""Build the complete UART/board RTL and reuse the host memory adapter."""
from pathlib import Path
import os
import subprocess
import build_identity

ROOT=Path(__file__).resolve().parent.parent


def main():
    subprocess.run(["python3",str(ROOT/"tools/generate_fpga_ports.py")],check=True)
    vendor=ROOT/"third_party/hardfloat/source"
    sources=[ROOT/"rtl/vendor.vlt"]+sorted((ROOT/"rtl").glob("*.sv"))+sorted(vendor.glob("*.v"))
    sources += [vendor/"RISCV/HardFloat_specialize.v"]+sorted((ROOT/"fpga").glob("*.sv"))
    args=[str(ROOT/".cache/tools/usr/bin/verilator"),"-Wall","-Wno-UNUSEDSIGNAL","--unroll-count","512",
          "--assert","-DWASMETAL_ASSERTIONS","--top-module","wasmetal_ulx3s","-I"+str(ROOT/"fpga"),
          "-I"+str(vendor),"-I"+str(vendor/"RISCV"),"--cc","--exe","--build","-j","4",
          "--Mdir",str(ROOT/"build/uart-model"),"-CFLAGS","-std=c++17 -O3 -Wall -Wextra -Werror -DWASMETAL_FPGA -DWASMETAL_UART_MODEL"]
    args+=list(map(str,sources))+[str(ROOT/"sim/main.cpp")]
    binary=ROOT/"build/uart-model/Vwasmetal_ulx3s"
    build_identity.begin(binary,"uart")
    subprocess.run(args,cwd=ROOT,env=dict(os.environ,VERILATOR_ROOT=str(ROOT/".cache/tools/usr/share/verilator")),check=True)
    build_identity.finish(binary)


if __name__=="__main__":
    main()
