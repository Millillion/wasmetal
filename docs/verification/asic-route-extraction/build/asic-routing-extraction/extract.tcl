read_liberty {/tmp/wasmetal-xc7-core/build/asic-physical-startup/cells.lib}
read_db {/tmp/wasmetal-xc7-core/build/asic-routing-extended/routed.odb}
read_sdc {/tmp/wasmetal-xc7-core/build/asic-routing-extended/routed.sdc}
set_propagated_clock [all_clocks]
define_process_corner -ext_model_index 0 X
extract_parasitics -ext_model_file {/tmp/wasmetal-xc7-core/.cache/sky130hd-extraction/rcx_patterns.rules}
write_spef {/tmp/wasmetal-xc7-core/build/asic-routing-extraction/routed.spef}
read_spef {/tmp/wasmetal-xc7-core/build/asic-routing-extraction/routed.spef}
puts "WASMETAL extracted setup slack"
report_worst_slack -max -digits 6
puts "WASMETAL extracted hold slack"
report_worst_slack -min -digits 6
report_tns -digits 6
check_setup -verbose
report_checks -path_delay min_max -group_path_count 10 -format full_clock_expanded -fields {slew capacitance fanout input_pin} -digits 6 > {/tmp/wasmetal-xc7-core/build/asic-routing-extraction/timing-paths.rpt}
report_check_types -violators -max_slew -max_capacitance -max_fanout -min_pulse_width -min_period -digits 6 > {/tmp/wasmetal-xc7-core/build/asic-routing-extraction/electrical.rpt}
check_antennas -report_file {/tmp/wasmetal-xc7-core/build/asic-routing-extraction/antennas.rpt}
write_db {/tmp/wasmetal-xc7-core/build/asic-routing-extraction/extracted.odb}
puts "FINISHED routed parasitic extraction and nominal timing diagnostics"
