from concurrent.futures import ThreadPoolExecutor,as_completed
import json
from pathlib import Path
import subprocess
import sys
import time
root=Path.cwd();sys.path.insert(0,str(root/'tools'))
from loadable_ci import GROUPS,RECOVERY,check_plan
from standalone_support import verify_simulator,parameters
from prepare_standalone import digest
from program_upload import profile_tag
check_plan()
binary=root/'build/xc7-accelerated-gate-fast/obj/Vwasmetal_loadable'
identity=verify_simulator(binary)
reference_path=root/'reports/loadable-rtl.json';reference=json.loads(reference_path.read_text())
native=root/'build/loadable-sim/Vwasmetal_loadable'
assert verify_simulator(native)==reference['model'] and reference['status']=='passed'
for key in ('profile','profile_tag','uart_ticks','clock_scale','upload_timeout'):assert identity[key]==reference['model'][key],key
expected=parameters(identity['profile']);expected.update(PROFILE_TAG=f"128'h{int.from_bytes(profile_tag(identity['profile']),'little'):032x}",UART_TICKS=identity['uart_ticks'],UPLOAD_TIMEOUT_CYCLES=identity['upload_timeout'])
assert identity['parameters']==expected
out=root/'reports/xc7-system-shards';out.mkdir(exist_ok=True)
logs=root/'build/xc7-system-tests';logs.mkdir(exist_ok=True)
started=time.monotonic();done=[]
commands=[]
for n,group in enumerate(GROUPS):
 command=[sys.executable,'tools/check_loadable.py','--binary',str(binary),'--report',str(out/f'loadable-mapped-{n}.json')]
 for name in group:command+=['--case',name]
 if n:command+=['--no-recovery']
 commands.append(command)
inputs={str(p.relative_to(root)):digest(p) for p in [Path(__file__).resolve(),root/'tools/loadable_ci.py',reference_path,Path(str(binary)+'.build.json')]}
plan={'status':'running','model':identity,'reference_sha256':digest(reference_path),'commands':commands,'inputs':inputs,'completed_groups':done}
path=logs/'plan.json'
def save(status):
 plan.update(status=status,elapsed_seconds=time.monotonic()-started);path.write_text(json.dumps(plan,indent=2)+'\n')
def run(n):
 with (logs/f'{n}.log').open('w') as log:subprocess.run(commands[n],cwd=root,stdout=log,stderr=subprocess.STDOUT,check=True)
 return n
save('running')
try:
 with ThreadPoolExecutor(max_workers=4) as pool:
  futures=[pool.submit(run,n) for n in range(len(GROUPS))]
  for future in as_completed(futures):
   n=future.result();done.append(n);save('running');print('PASS group',n,flush=True)
 assert verify_simulator(binary)==identity
 assert verify_simulator(native)==reference['model']
 for name,value in inputs.items():assert digest(root/name)==value,name
 save('workers_completed_awaiting_aggregation')
except BaseException:
 save('failed');raise
