#!/usr/bin/env python3
"""Fetch checksum-pinned tools and tests into .cache without a system install."""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import tarfile
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache"
LOCK = json.loads((ROOT / "tools/upstream.lock.json").read_text())
PACKAGES = {
    "verilator_5.020-1_amd64.deb": ("verilator=5.020-1", "bb74ca8c32c73eb903ee91da64c8b58cfbe095c229967a95782108afb67bb3ca"),
    "yosys_0.33-5build2_amd64.deb": ("yosys=0.33-5build2", "94247f2157ec6ce63c6638326e419975d911ace5356b3dc276d1d8b36659efbd"),
    "yosys-abc_0.33-5build2_amd64.deb": ("yosys-abc=0.33-5build2", "916ba59b6ca6dd1b6b927c7364357c2801ccb85db7eb3ca858ac9a856270fa44"),
    "iverilog_12.0-2build2_amd64.deb": ("iverilog=12.0-2build2", "f19394cee05ad526e0eb3873bc6c17a5828f56df17fbe2db40cb66513a2d4667"),
}


def verify(path, digest):
    if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        raise RuntimeError(f"checksum mismatch: {path}")


def archive(entry, path, destination):
    if not path.exists():
        temp = path.with_suffix(path.suffix + ".partial")
        urllib.request.urlretrieve(entry["url"], temp)
        verify(temp, entry["sha256"])
        temp.rename(path)
    verify(path, entry["sha256"])
    with tarfile.open(path) as tar:
        tar.extractall(destination, filter="data")


def main():
    if platform.system() != "Linux" or platform.machine() != "x86_64":
        raise SystemExit("Pinned binary bootstrap currently supports Ubuntu 24.04 x86-64; see docs/RTL.md")
    for directory in ("packages", "tools", "upstream"):
        (CACHE / directory).mkdir(parents=True, exist_ok=True)
    archive(LOCK["spec"], CACHE / "upstream/spec.tar.gz", CACHE / "upstream")
    archive(LOCK["wasm_tools"], CACHE / "packages/wasm-tools.tar.gz", CACHE / "tools")
    for filename, (package, digest) in PACKAGES.items():
        path = CACHE / "packages" / filename
        if not path.exists():
            subprocess.run(["apt-get", "download", package], cwd=CACHE / "packages", check=True)
        verify(path, digest)
        subprocess.run(["dpkg-deb", "-x", str(path), str(CACHE / "tools")], check=True)
    executable = CACHE / "tools/usr/share/verilator/bin/verilator_bin"
    if not executable.exists():
        executable.symlink_to("../../../bin/verilator_bin")
    print("Verified pinned test sources, wasm-tools, Verilator, Yosys and Icarus in .cache")


if __name__ == "__main__":
    main()
