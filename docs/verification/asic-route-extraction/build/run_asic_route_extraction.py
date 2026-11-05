"""Extract routed startup-block parasitics and report nominal timing diagnostics."""
from pathlib import Path
import json,sys,time
from copy import deepcopy
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from asic_physical_tools import provision
from check_asic_startup import execute
from prepare_standalone import digest
base=ROOT/'build/asic-routing-extraction';base.mkdir(exist_ok=True)
route=ROOT/'build/asic-routing-extended';source=ROOT/'build/asic-physical-startup'
rules=ROOT/'.cache/sky130hd-extraction/rcx_patterns.rules'
assert digest(rules)=='d5bd9b1077ceac9929416abca272a6d52e51cd9a575453a31d129817bb286476'
status=json.loads((route/'status.json').read_text());assert status['status']=='zero-router-markers' and status['inputs_unchanged']
assert (route/'drc.rpt').read_bytes()==b''
for name,sha in status['inputs'].items():assert digest(ROOT/name)==sha,name
for name,sha in status['artifacts'].items():assert digest(route/name)==sha,name
exe,env,tools=provision()
def reconcile(before,after):
 assert set(before)==set(after),'physical-tool report inventory changed'
 for key in before:
  if key!='inputs':assert before[key]==after[key],'physical tool/runtime identity changed: '+key
 # These imported Wasm functions are never executed by the OpenROAD launcher.
 # Their changes and both snapshots remain explicit; no other drift is allowed.
 allowed={'tools/run_spec.py','tools/spec_inputs.py','tools/check_spec_conversion.py'}
 changed={n:{'before':before['inputs'].get(n),'after':after['inputs'].get(n)}
          for n in set(before['inputs'])|set(after['inputs']) if before['inputs'].get(n)!=after['inputs'].get(n)}
 assert set(changed)<=allowed,'physical launcher or platform dependency changed: '+str(set(changed)-allowed)
 return changed
drift=reconcile(status['tools'],tools);controls=[]
for field in ('executable_sha256','loaded_libraries','package_trees','inputs'):
 bad=deepcopy(tools)
 if field=='executable_sha256':bad[field]='0'*64
 elif field=='loaded_libraries':bad[field][next(iter(bad[field]))]='0'*64
 elif field=='package_trees':bad[field][next(iter(bad[field]))]['sha256']='0'*64
 else:bad[field]['tools/asic_physical_tools.py']='0'*64
 try:reconcile(status['tools'],bad)
 except AssertionError as error:controls.append({'field':field,'rejected':True,'reason':str(error)})
 else:raise ValueError('physical input reconciliation accepted '+field)
paths=[route/'routed.odb',route/'routed.sdc',route/'routed.v',route/'status.json',source/'cells.lib',rules,Path(__file__).resolve()]
bound={str(p.relative_to(ROOT)):digest(p) for p in paths};bound.update(tools['inputs'])
script=f'''read_liberty {{{source}/cells.lib}}
read_db {{{route}/routed.odb}}
read_sdc {{{route}/routed.sdc}}
set_propagated_clock [all_clocks]
define_process_corner -ext_model_index 0 X
extract_parasitics -ext_model_file {{{rules}}}
write_spef {{{base}/routed.spef}}
read_spef {{{base}/routed.spef}}
puts "WASMETAL extracted setup slack"
report_worst_slack -max -digits 6
puts "WASMETAL extracted hold slack"
report_worst_slack -min -digits 6
report_tns -digits 6
check_setup -verbose
report_checks -path_delay min_max -group_path_count 10 -format full_clock_expanded -fields {{slew capacitance fanout input_pin}} -digits 6 > {{{base}/timing-paths.rpt}}
report_check_types -violators -max_slew -max_capacitance -max_fanout -min_pulse_width -min_period -digits 6 > {{{base}/electrical.rpt}}
check_antennas -report_file {{{base}/antennas.rpt}}
write_db {{{base}/extracted.odb}}
puts "FINISHED routed parasitic extraction and nominal timing diagnostics"
'''
script_path=base/'extract.tcl';script_path.write_text(script);bound[str(script_path.relative_to(ROOT))]=digest(script_path)
report={'status':'running','scope':'single-corner extracted startup-block diagnostics, not chip timing signoff',
        'inputs':bound,'tools':tools,'physical_timing_accepted':False,'physical_hardware_tested':False,
        'unexecuted_test_tool_snapshot_drift':drift,'physical_reconciliation_faults':controls}
out=base/'status.json';out.write_text(json.dumps(report,indent=2)+'\n');started=time.monotonic()
try:
 code=execute([str(exe),'-no_init','-no_settings','-exit','-threads','2',str(script_path)],base/'extract.log',timeout=600,env=env,accepted_failure=True)
 report.update(exit_code=code,status='diagnostic-completed' if code==0 else 'incomplete')
except Exception as error:
 report.update(status='incomplete',error=str(error))
finally:
 report.update(elapsed_seconds=time.monotonic()-started,inputs_unchanged=all(digest(ROOT/n)==s for n,s in bound.items()))
 if not report['inputs_unchanged']:report['status']='changed-inputs'
 report['artifacts']={p.name:digest(p) for p in base.iterdir() if p.is_file() and p!=out}
 out.write_text(json.dumps(report,indent=2)+'\n')
 print(report['status'],flush=True)
