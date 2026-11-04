import sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/"tools"))
from check_memory_startup_system import owned_run
latency=sys.argv[1]
with Path(f"build/startup-reference-{latency}.log").open("w") as log:
    result=owned_run([sys.executable,"tools/check_sram_system.py","--latency",latency],log,3600)
result.check_returncode()
print("PASS fresh SRAM reference",latency)
