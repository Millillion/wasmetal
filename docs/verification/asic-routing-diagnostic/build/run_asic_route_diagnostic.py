from pathlib import Path
import json,re,sys,time
sys.path.insert(0,'tools')
from asic_physical_tools import provision,PDK
from check_asic_startup import execute
from prepare_standalone import ROOT,digest
base=ROOT/'build/asic-routing-diagnostic';base.mkdir(exist_ok=True)
source=ROOT/'build/asic-physical-startup';executable,env,tool=provision()
paths=[source/name for name in ('cells.lib','global-routed.odb','global-routed.sdc','global-routed.v','route.guide')]
paths += [PDK/'setRC.tcl',PDK/'fastroute.tcl',Path(__file__).resolve()]
bound={str(p.relative_to(ROOT)):digest(p) for p in paths}
script=f'''set source {{{source}}}
set trial {{{base}}}
set platform {{{PDK}}}
read_liberty [file join $source cells.lib]
read_db [file join $source global-routed.odb]
read_sdc [file join $source global-routed.sdc]
source [file join $platform setRC.tcl]
set ::env(MIN_ROUTING_LAYER) met1
set ::env(MAX_ROUTING_LAYER) met5
set ::env(MIN_CLK_ROUTING_LAYER) met3
source [file join $platform fastroute.tcl]
read_guides [file join $source route.guide]
detailed_route -output_drc [file join $trial drc.rpt] -output_maze [file join $trial maze.log] -output_guide_coverage [file join $trial guide-coverage.csv] -droute_end_iter 3 -or_seed 1
check_placement -verbose
check_power_grid -net VDD
check_power_grid -net VSS
write_db [file join $trial routed.odb]
write_def [file join $trial routed.def]
write_verilog [file join $trial routed.v]
write_sdc [file join $trial routed.sdc]
puts "FINISHED bounded detailed-routing diagnostic"
'''
path=base/'route.tcl';path.write_text(script);bound[str(path.relative_to(ROOT))]=digest(path)
report={'status':'running','inputs':bound,'tools':tool,'iteration_limit':3,'time_limit_seconds':2100,'routing_accepted':False,'physical_timing_accepted':False};out=base/'status.json';out.write_text(json.dumps(report,indent=2)+'\n');start=time.monotonic()
try:
 code=execute([str(executable),'-no_init','-no_settings','-exit','-threads','2',str(path)],base/'route.log',timeout=2100,env=env,accepted_failure=True)
 report['exit_code']=code;log=(base/'route.log').read_text();counts=[int(x) for x in re.findall(r'Number of violations = (\d+)',log)]
 report['completed_iteration_violations']=counts
 complete=code==0 and 'FINISHED bounded detailed-routing diagnostic' in log and all((base/name).exists() for name in ('routed.odb','routed.def','routed.v','routed.sdc','drc.rpt'))
 report['detailed_route_command_completed']=complete
 if complete:
  markers=len(re.findall(r'^violation type:',(base/'drc.rpt').read_text(),re.M));report['drc_report_markers']=markers
  if not counts or markers!=counts[-1]:report['status']='inconsistent-diagnostic'
  else:report['status']='violations-remain' if markers else 'zero-router-markers';report['routing_accepted']=not markers
 else:report['status']='incomplete'
except Exception as error:
 report['status']='incomplete';report['error']=str(error)
finally:
 report['elapsed_seconds']=time.monotonic()-start;report['inputs_unchanged']=all(digest(ROOT/name)==sha for name,sha in bound.items());report['artifacts']={p.name:digest(p) for p in base.iterdir() if p.is_file() and p!=out};out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('inputs','tools','artifacts')}),flush=True)
