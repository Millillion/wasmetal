from pathlib import Path
import sys,re,json
sys.path.insert(0,'tools')
from check_asic_startup import yosys
from prepare_standalone import digest
p=Path('build/asic-startup-post-physical').resolve();before=Path('build/asic-startup/131072-3-11/mapped.v').resolve()
assert digest(before)==digest(Path('build/asic-startup-physical/mapped.v'))
assert json.loads((p/'clock-audit.json').read_text())['status']=='passed'
names=sorted(re.findall(r'sky130_fd_sc_hd__dfxtp_1\s+(\S+)\s*\(',before.read_text()));assert len(names)==620
selectors=' '.join('wasmetal_startup_sram/w:'+name+'.Q' for name in names)
setup=''
for label,circuit in [('gold',before),('gate',p/'functional.v')]:
 setup+=f'read_verilog {p}/equivalence-cells.v {circuit}\nprep -top wasmetal_startup_sram -flatten\nopt\nsplitnets\n'
 setup+=f'select -assert-count 620 {selectors}\nselect -set state_points {selectors}\nrename -hide wasmetal_startup_sram/w:* @state_points %d\nselect *\n'
 setup+=f'rename wasmetal_startup_sram {label}\ndesign -stash {label}\n'
setup+='design -copy-from gold -as gold gold\ndesign -copy-from gate -as gate gate\n'
script=setup+f'equiv_make gold gate equiv\nhierarchy -top equiv\nwrite_rtlil {p}/state-equiv.il\nequiv_simple -undef -short\nequiv_induct -undef -seq 12\nequiv_status -assert\n'
_,log=yosys(script,p,'state-equivalence');assert 'Equivalence successfully proven!' in log.read_text()
script=f'read_rtlil {p}/state-equiv.il\nequiv_miter -assert -undef reset_points\nhierarchy -top reset_points\nflatten\nopt_clean\nsat -seq 12 -set-at 1 reset 1 -set-def-inputs -set-init-undef -enable_undef -prove-skip 1 -prove-asserts -verify\n'
_,log=yosys(script,p,'state-reset-points');assert 'SAT proof finished - no model found: SUCCESS!' in log.read_text()
print('PASS exact pre/post physical circuit equivalence at all output pins and 620 state points, including independent 12-cycle reset base')
