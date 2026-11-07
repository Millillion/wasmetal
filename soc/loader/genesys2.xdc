# Genesys 2 (Rev. H) pins for wasmetal_loadable_genesys2, from Digilent's
# Genesys-2-Master.xdc at digilent-xdc c8644a9fe31cc803789643124545d56b3bef4600.
set_property -dict {PACKAGE_PIN AD12 IOSTANDARD LVDS} [get_ports sysclk_p]
set_property -dict {PACKAGE_PIN AD11 IOSTANDARD LVDS} [get_ports sysclk_n]
create_clock -name sysclk -period 5.000 [get_ports sysclk_p]

# The CPU clock is divider[7], a 200 MHz / 256 counter bit on a global buffer.
# Both of its edges clock the CPU's half-cycle RAM paths.
create_generated_clock -name core_clock -source [get_pins -hierarchical -filter {NAME =~ "divider_reg[7]/C"}] \
    -divide_by 256 [get_pins -hierarchical -filter {NAME =~ "divider_reg[7]/Q"}]

# CPU_RESET (active low) is synchronized to core_clock inside the design.
set_property -dict {PACKAGE_PIN R19 IOSTANDARD LVCMOS33} [get_ports cpu_resetn]
# uart_tx_in is the FPGA's receive input from the USB-UART bridge; it is
# synchronized by the UART receiver. uart_rx_out is the FPGA's transmit output.
set_property -dict {PACKAGE_PIN Y20 IOSTANDARD LVCMOS33} [get_ports uart_tx_in]
set_property -dict {PACKAGE_PIN Y23 IOSTANDARD LVCMOS33} [get_ports uart_rx_out]
set_property -dict {PACKAGE_PIN T28 IOSTANDARD LVCMOS33} [get_ports {led[0]}]
set_property -dict {PACKAGE_PIN V19 IOSTANDARD LVCMOS33} [get_ports {led[1]}]

# Asynchronous board signals: no timing relationship with either clock.
set_false_path -from [get_ports {cpu_resetn uart_tx_in}]
set_false_path -to [get_ports {uart_rx_out led[*]}]
