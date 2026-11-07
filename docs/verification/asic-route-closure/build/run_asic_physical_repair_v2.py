"""Second antenna repair with jumper/diode choices; results remain unsigned-off diagnostics."""
from pathlib import Path
import json,re,sys,time
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from asic_physical_tools import PDK,provision
from check_asic_startup import execute
from prepare_standalone import digest
base=ROOT/'build/asic-routing-repair-v2';base.mkdir(exist_ok=False)
source=ROOT/'build/asic-physical-startup';extraction=ROOT/'build/asic-routing-repair'
record=json.loads((extraction/'status.json').read_text());assert record['status']=='diagnostic-completed' and record['inputs_unchanged']
for name,sha in record['artifacts'].items():assert digest(extraction/name)==sha,name
exe,env,tools=provision();assert tools==record['tools'],'physical repair tool/runtime inputs changed'
rules=ROOT/'.cache/sky130hd-extraction/rcx_patterns.rules'
paths=[extraction/'extracted.odb',extraction/'routed.spef',ROOT/'build/asic-routing-repair/routed.sdc',
       source/'cells.lib',PDK/'setRC.tcl',PDK/'fastroute.tcl',rules,Path(__file__).resolve()]
bound={str(p.relative_to(ROOT)):digest(p) for p in paths};bound.update(tools['inputs'])
script=f'''read_liberty {{{source}/cells.lib}}
read_db {{{extraction}/extracted.odb}}
read_sdc {{{ROOT}/build/asic-routing-repair/routed.sdc}}
read_spef {{{extraction}/routed.spef}}
set_propagated_clock [all_clocks]
source {{{PDK}/setRC.tcl}}
set ::env(MIN_ROUTING_LAYER) met1
set ::env(MAX_ROUTING_LAYER) met5
set ::env(MIN_CLK_ROUTING_LAYER) met3
source {{{PDK}/fastroute.tcl}}
check_placement -verbose
# Re-route signal/clock wires after the intentional connectivity edits. Keep PDN.
if {{[llength [info commands odb::dbWire_destroy]] != 1}} {{ error "missing documented OpenDB wire destruction binding" }}
set removed 0
foreach net [[ord::get_db_block] getNets] {{
  if {{[$net isSpecial]}} {{ continue }}
  set wire [$net getWire]
  if {{$wire ne "NULL"}} {{ odb::dbWire_destroy $wire; incr removed }}
}}
puts "REMOVED prior signal routes $removed"
global_route -guide_file {{{base}/before-antenna.guide}} -congestion_report_file {{{base}/congestion.rpt}}
repair_antennas sky130_fd_sc_hd__diode_2 -iterations 5 -ratio_margin 50
check_placement -verbose
check_antennas -report_file {{{base}/global-antennas.rpt}}
write_guides {{{base}/repaired.guide}}
estimate_parasitics -global_routing
report_worst_slack -min -digits 6
write_db {{{base}/repaired-global.odb}}
write_verilog {{{base}/repaired-global.v}}
write_sdc {{{base}/repaired-global.sdc}}
detailed_route -output_drc {{{base}/drc.rpt}} -output_maze {{{base}/maze.log}} -output_guide_coverage {{{base}/guide-coverage.csv}} -droute_end_iter 20 -or_seed 1
check_placement -verbose
check_power_grid -net VDD
check_power_grid -net VSS
write_db {{{base}/routed.odb}}
write_verilog {{{base}/routed.v}}
write_def {{{base}/routed.def}}
write_sdc {{{base}/routed.sdc}}
define_process_corner -ext_model_index 0 X
extract_parasitics -ext_model_file {{{rules}}}
write_spef {{{base}/routed.spef}}
read_spef {{{base}/routed.spef}}
puts "WASMETAL repaired extracted setup slack"
report_worst_slack -max -digits 6
puts "WASMETAL repaired extracted hold slack"
report_worst_slack -min -digits 6
report_checks -path_delay min_max -group_path_count 10 -format full_clock_expanded -digits 6 > {{{base}/timing-paths.rpt}}
report_check_types -violators -max_slew -max_capacitance -max_fanout -min_pulse_width -min_period -digits 6 > {{{base}/electrical.rpt}}
check_setup -verbose
check_antennas -report_file {{{base}/antennas.rpt}}
write_db {{{base}/extracted.odb}}
puts "FINISHED physical repair diagnostic"
'''
script_path=base/'repair.tcl';script_path.write_text(script);bound[str(script_path.relative_to(ROOT))]=digest(script_path)
out=base/'status.json';report={'status':'running','inputs':bound,'tools':tools,'hold_repair_repeated':False,'antenna_margin_percent':50,
                            'physical_timing_accepted':False,'fabrication_ready':False,'physical_hardware_tested':False}
out.write_text(json.dumps(report,indent=2)+'\n');started=time.monotonic()
try:
 code=execute([str(exe),'-no_init','-no_settings','-exit','-threads','4',str(script_path)],base/'repair.log',timeout=4800,env=env,accepted_failure=True)
 log=(base/'repair.log').read_text();complete=code==0 and 'FINISHED physical repair diagnostic' in log
 report.update(exit_code=code,status='diagnostic-completed' if complete else 'incomplete',
               completed_iteration_violations=[int(x) for x in re.findall(r'Number of violations = (\d+)',log)])
 if complete:report['drc_report_markers']=len(re.findall(r'^violation type:',(base/'drc.rpt').read_text(),re.M))
except Exception as error:report.update(status='incomplete',error=str(error))
finally:
 report.update(elapsed_seconds=time.monotonic()-started,inputs_unchanged=all(digest(ROOT/name)==sha for name,sha in bound.items()))
 if not report['inputs_unchanged']:report['status']='changed-inputs'
 report['artifacts']={p.name:digest(p) for p in base.iterdir() if p.is_file() and p!=out}
 out.write_text(json.dumps(report,indent=2)+'\n');print(report['status'],flush=True)
