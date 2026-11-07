read_liberty {/tmp/wasmetal-xc7-core/build/asic-physical-startup/cells.lib}
read_db {/tmp/wasmetal-xc7-core/build/asic-routing-extraction/extracted.odb}
read_sdc {/tmp/wasmetal-xc7-core/build/asic-routing-extended/routed.sdc}
read_spef {/tmp/wasmetal-xc7-core/build/asic-routing-extraction/routed.spef}
set_propagated_clock [all_clocks]
source {/tmp/wasmetal-xc7-core/.cache/sky130hd-physical/setRC.tcl}
set ::env(MIN_ROUTING_LAYER) met1
set ::env(MAX_ROUTING_LAYER) met5
set ::env(MIN_CLK_ROUTING_LAYER) met3
source {/tmp/wasmetal-xc7-core/.cache/sky130hd-physical/fastroute.tcl}
repair_timing -hold -hold_margin 0.1 -max_buffer_percent 10 -verbose
detailed_placement -incremental
check_placement -verbose
# Re-route signal/clock wires after the intentional connectivity edits. Keep PDN.
if {[llength [info commands odb::dbWire_destroy]] != 1} { error "missing documented OpenDB wire destruction binding" }
set removed 0
foreach net [[ord::get_db_block] getNets] {
  if {[$net isSpecial]} { continue }
  set wire [$net getWire]
  if {$wire ne "NULL"} { odb::dbWire_destroy $wire; incr removed }
}
puts "REMOVED prior signal routes $removed"
global_route -guide_file {/tmp/wasmetal-xc7-core/build/asic-routing-repair/before-antenna.guide} -congestion_report_file {/tmp/wasmetal-xc7-core/build/asic-routing-repair/congestion.rpt}
repair_antennas sky130_fd_sc_hd__diode_2 -iterations 5 -ratio_margin 10 -diode_only
check_placement -verbose
check_antennas -report_file {/tmp/wasmetal-xc7-core/build/asic-routing-repair/global-antennas.rpt}
write_guides {/tmp/wasmetal-xc7-core/build/asic-routing-repair/repaired.guide}
estimate_parasitics -global_routing
report_worst_slack -min -digits 6
write_db {/tmp/wasmetal-xc7-core/build/asic-routing-repair/repaired-global.odb}
write_verilog {/tmp/wasmetal-xc7-core/build/asic-routing-repair/repaired-global.v}
write_sdc {/tmp/wasmetal-xc7-core/build/asic-routing-repair/repaired-global.sdc}
detailed_route -output_drc {/tmp/wasmetal-xc7-core/build/asic-routing-repair/drc.rpt} -output_maze {/tmp/wasmetal-xc7-core/build/asic-routing-repair/maze.log} -output_guide_coverage {/tmp/wasmetal-xc7-core/build/asic-routing-repair/guide-coverage.csv} -droute_end_iter 20 -or_seed 1
check_placement -verbose
check_power_grid -net VDD
check_power_grid -net VSS
write_db {/tmp/wasmetal-xc7-core/build/asic-routing-repair/routed.odb}
write_verilog {/tmp/wasmetal-xc7-core/build/asic-routing-repair/routed.v}
write_def {/tmp/wasmetal-xc7-core/build/asic-routing-repair/routed.def}
write_sdc {/tmp/wasmetal-xc7-core/build/asic-routing-repair/routed.sdc}
define_process_corner -ext_model_index 0 X
extract_parasitics -ext_model_file {/tmp/wasmetal-xc7-core/.cache/sky130hd-extraction/rcx_patterns.rules}
write_spef {/tmp/wasmetal-xc7-core/build/asic-routing-repair/routed.spef}
read_spef {/tmp/wasmetal-xc7-core/build/asic-routing-repair/routed.spef}
puts "WASMETAL repaired extracted setup slack"
report_worst_slack -max -digits 6
puts "WASMETAL repaired extracted hold slack"
report_worst_slack -min -digits 6
report_checks -path_delay min_max -group_path_count 10 -format full_clock_expanded -digits 6 > {/tmp/wasmetal-xc7-core/build/asic-routing-repair/timing-paths.rpt}
report_check_types -violators -max_slew -max_capacitance -max_fanout -min_pulse_width -min_period -digits 6 > {/tmp/wasmetal-xc7-core/build/asic-routing-repair/electrical.rpt}
check_setup -verbose
check_antennas -report_file {/tmp/wasmetal-xc7-core/build/asic-routing-repair/antennas.rpt}
write_db {/tmp/wasmetal-xc7-core/build/asic-routing-repair/extracted.odb}
puts "FINISHED physical repair diagnostic"
