"""Run the pinned, relocatable CAD tools headlessly without user config writes."""
import os
from pathlib import Path

SUITE = Path(__file__).resolve().parent.parent / ".cache/tools/oss-cad-suite"


def command(name):
    if name not in ("nextpnr-ecp5", "ecppack", "yosys", "yosys-abc"):
        raise ValueError(name)
    return [str(SUITE / "lib/ld-linux-x86-64.so.2"), "--inhibit-cache", "--inhibit-rpath", "",
            "--library-path", str(SUITE / "lib"), str(SUITE / "libexec" / name)]


def environment():
    return dict(os.environ, PYTHONHOME=str(SUITE), PYTHONNOUSERSITE="1", QT_QPA_PLATFORM="offscreen")
