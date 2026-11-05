set trial [file join [pwd] build asic-startup-physical]
set platform [file join [pwd] .cache sky130hd-physical]
read_lef [file join $platform lef sky130_fd_sc_hd.tlef]
read_lef [file join $platform lef sky130_fd_sc_hd_merged.lef]
read_liberty [file join $trial cells.lib]
read_verilog [file join $trial mapped.v]
link_design wasmetal_startup_sram
create_clock -name core_clk -period 100 [get_ports clk]
set nonclock [remove_from_collection [all_inputs] [get_ports clk]]
set_input_delay -clock core_clk -max 10 $nonclock
set_input_delay -clock core_clk -min 2 $nonclock
set_output_delay -clock core_clk -max 10 [all_outputs]
set_output_delay -clock core_clk -min 2 [all_outputs]
set_driving_cell -lib_cell sky130_fd_sc_hd__buf_4 -pin X $nonclock
set_load 0.005 [all_outputs]
set_clock_transition 0.5 [get_clocks core_clk]
set_clock_uncertainty 0.5 [get_clocks core_clk]
report_units
initialize_floorplan -utilization 35 -aspect_ratio 1 -core_space 10 -site unithd
source [file join $platform make_tracks.tcl]
source [file join $platform setRC.tcl]
repair_tie_fanout sky130_fd_sc_hd__conb_1/LO -max_fanout 1
repair_tie_fanout sky130_fd_sc_hd__conb_1/HI -max_fanout 1
set ::env(TAP_CELL_NAME) sky130_fd_sc_hd__tapvpwrvgnd_1
source [file join $platform tapcell.tcl]
source [file join $platform pdn.tcl]
pdngen
place_pins -hor_layers met3 -ver_layers met2 -random_seed 1
global_placement -density 0.55
detailed_placement
check_placement -verbose
estimate_parasitics -placement
check_setup -verbose
report_checks -path_delay min_max -group_path_count 5
report_check_types -violators -max_slew -max_capacitance -max_fanout
write_db [file join $trial placed.odb]
write_def [file join $trial placed.def]
write_verilog [file join $trial placed.v]
write_sdc [file join $trial constraints.sdc]
puts "PASS experimental startup floorplan and placement"
