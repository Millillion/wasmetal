# Non-project Vivado build of the programmable WasMetal system for Genesys 2.
# Run through tools/genesys2_vivado.py, which writes the manifest read here:
#   vivado -mode batch -source tools/vivado/genesys2.tcl -tclargs build/genesys2
set out [file normalize [lindex $argv 0]]
source [file join $out manifest.tcl]
set_param general.maxThreads 4
foreach path $wasmetal_sources { read_verilog -sv $path }
read_xdc $wasmetal_constraints
synth_design -top wasmetal_loadable_genesys2 -part $wasmetal_part \
    -include_dirs $wasmetal_include_dirs -verilog_define SYNTHESIS \
    -generic PROFILE_TAG=$wasmetal_profile_tag
report_utilization -file [file join $out synth-utilization.rpt]
write_checkpoint -force [file join $out synth.dcp]
opt_design
place_design
phys_opt_design
route_design
report_utilization -file [file join $out utilization.rpt]
report_timing_summary -max_paths 20 -report_unconstrained -file [file join $out timing-summary.rpt]
report_clocks -file [file join $out clocks.rpt]
report_clock_interaction -file [file join $out clock-interaction.rpt]
report_methodology -file [file join $out methodology.rpt]
report_drc -file [file join $out drc.rpt]
check_timing -verbose -file [file join $out check-timing.rpt]
write_checkpoint -force [file join $out routed.dcp]
write_bitstream -force [file join $out wasmetal.bit]
puts "WASMETAL Vivado build finished"
