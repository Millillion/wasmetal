#!/usr/bin/env python3
"""Bind an executable to its inputs; reject edits during compilation or reuse."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent


def inputs(profile):
    directories=["rtl","sim","third_party/hardfloat"]
    if profile!="native": directories.append("fpga")
    paths={p for d in directories for p in (ROOT/d).rglob("*")
           if p.is_file() and p.suffix in (".sv",".svh",".v",".vi",".vlt",".cpp",".hpp",".json")}
    paths.update([ROOT/"Makefile",ROOT/"tools/upstream.lock.json",ROOT/"tools/generate_fpga_ports.py",ROOT/"tools/build_identity.py"])
    if profile=="uart": paths.add(ROOT/"tools/build_fpga_sim.py")
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}


def begin(binary,profile):
    binary.parent.mkdir(parents=True,exist_ok=True)
    Path(str(binary)+".inputs.json").write_text(json.dumps({"profile":profile,"inputs":inputs(profile)},indent=2)+"\n")


def finish(binary):
    snapshot=json.loads(Path(str(binary)+".inputs.json").read_text())
    if snapshot["inputs"]!=inputs(snapshot["profile"]):
        raise RuntimeError("build inputs changed during compilation; rebuild")
    snapshot["binary_sha256"]=hashlib.sha256(binary.read_bytes()).hexdigest()
    Path(str(binary)+".build.json").write_text(json.dumps(snapshot,indent=2)+"\n")


def verify(binary):
    path=Path(str(binary)+".build.json")
    if not path.exists():
        raise RuntimeError(f"missing build identity for {binary}; rebuild with make sim, fpga-sim, or fpga-host")
    snapshot=json.loads(path.read_text())
    if snapshot["inputs"]!=inputs(snapshot["profile"]):
        raise RuntimeError("simulator build is stale; rebuild before running the suite")
    if snapshot["binary_sha256"]!=hashlib.sha256(binary.read_bytes()).hexdigest():
        raise RuntimeError("simulator binary does not match its build identity")
    return snapshot


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("action",choices=["begin","finish","verify"])
    parser.add_argument("binary",type=Path)
    parser.add_argument("--profile",choices=["native","uart","physical"],default="native")
    args=parser.parse_args()
    if args.action=="begin": begin(args.binary,args.profile)
    elif args.action=="finish": finish(args.binary)
    else: verify(args.binary)


if __name__=="__main__": main()
