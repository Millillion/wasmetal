set source {/tmp/wasmetal-xc7-core/build/asic-physical-startup}
set trial {/tmp/wasmetal-xc7-core/build/asic-routing-extended}
set platform {/tmp/wasmetal-xc7-core/.cache/sky130hd-physical}
read_liberty [file join $source cells.lib]
read_db [file join $source global-routed.odb]
read_sdc [file join $source global-routed.sdc]
source [file join $platform setRC.tcl]
set ::env(MIN_ROUTING_LAYER) met1
set ::env(MAX_ROUTING_LAYER) met5
set ::env(MIN_CLK_ROUTING_LAYER) met3
source [file join $platform fastroute.tcl]
read_guides [file join $source route.guide]
detailed_route -output_drc [file join $trial drc.rpt] -output_maze [file join $trial maze.log] -output_guide_coverage [file join $trial guide-coverage.csv] -droute_end_iter 16 -or_seed 1
check_placement -verbose
check_power_grid -net VDD
check_power_grid -net VSS
write_db [file join $trial routed.odb]
write_def [file join $trial routed.def]
write_verilog [file join $trial routed.v]
write_sdc [file join $trial routed.sdc]
puts "FINISHED bounded detailed-routing diagnostic"
