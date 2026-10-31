SHELL := /bin/bash
LOCAL_TOOLS := $(CURDIR)/.cache/tools
VERILATOR ?= $(if $(wildcard $(LOCAL_TOOLS)/usr/bin/verilator),$(LOCAL_TOOLS)/usr/bin/verilator,verilator)
ifneq ($(wildcard $(LOCAL_TOOLS)/usr/share/verilator),)
export VERILATOR_ROOT := $(LOCAL_TOOLS)/usr/share/verilator
endif
HARDFLOAT := $(wildcard third_party/hardfloat/source/*.v) third_party/hardfloat/source/RISCV/HardFloat_specialize.v
RTL := rtl/vendor.vlt $(wildcard rtl/*.sv) $(HARDFLOAT)
# Unused port bits and arithmetic carry bits are intentional; all width,
# latch, multiple-driver, and combinational-loop warnings remain fatal.
VFLAGS := -Wall -Wno-UNUSEDSIGNAL --unroll-count 512 --assert -DWASMETAL_ASSERTIONS --top-module wasmetal_core -Ithird_party/hardfloat/source -Ithird_party/hardfloat/source/RISCV
.PHONY: sim lint test test-all test-divider test-simd test-popcount test-values test-descriptors prove-masks synth fpga-sim fpga-smoke fpga-host fpga-core fpga-bitstream
sim: build/obj/Vwasmetal_core
sim/core_config.hpp: $(RTL) $(wildcard third_party/hardfloat/source/*.vi) $(wildcard third_party/hardfloat/source/RISCV/*.vi) $(wildcard fpga/*.sv) fpga/ports.json fpga/profile.json tools/generate_fpga_ports.py
	python3 tools/generate_fpga_ports.py
build/obj/Vwasmetal_core: $(RTL) $(wildcard third_party/hardfloat/source/*.vi) $(wildcard third_party/hardfloat/source/RISCV/*.vi) $(wildcard sim/*.hpp) sim/main.cpp sim/core_config.hpp Makefile tools/build_identity.py tools/upstream.lock.json
	python3 tools/build_identity.py begin $@ --profile native
	$(VERILATOR) $(VFLAGS) --cc --exe --build -j 4 --Mdir build/obj -MAKEFLAGS 'OPT_FAST=-O3' -CFLAGS '-std=c++17 -O3 -Wall -Wextra -Werror' $(RTL) $(CURDIR)/sim/main.cpp
	python3 tools/build_identity.py finish $@
lint:
	$(VERILATOR) $(VFLAGS) --lint-only $(RTL)
test: sim
	python3 tools/run_spec.py --suite i32 --suite i64
test-all: sim
	python3 tools/run_spec.py
test-divider:
	mkdir -p build/unit
	$(LOCAL_TOOLS)/usr/bin/iverilog -B$(LOCAL_TOOLS)/usr/lib/x86_64-linux-gnu/ivl -g2012 -s divider_tb -o build/unit/divider.vvp rtl/wasmetal_divider.sv tests/rtl/divider_tb.sv
	$(LOCAL_TOOLS)/usr/bin/vvp build/unit/divider.vvp
prove-masks:
	python3 tools/prove_masks.py
test-simd:
	mkdir -p build/unit
	$(LOCAL_TOOLS)/usr/bin/iverilog -B$(LOCAL_TOOLS)/usr/lib/x86_64-linux-gnu/ivl -g2012 -s simd_serial_tb -o build/unit/simd.vvp rtl/wasmetal_popcount.sv rtl/wasmetal_simd_decode.sv rtl/wasmetal_simd_lanes.sv rtl/wasmetal_simd_int.sv rtl/wasmetal_simd_serial.sv tests/rtl/simd_serial_tb.sv
	timeout 60s $(LOCAL_TOOLS)/usr/bin/vvp build/unit/simd.vvp
test-popcount:
	python3 tools/check_popcount.py
test-values:
	mkdir -p build/unit
	$(LOCAL_TOOLS)/usr/bin/iverilog -B$(LOCAL_TOOLS)/usr/lib/x86_64-linux-gnu/ivl -g2012 -s values_tb -o build/unit/values.vvp rtl/wasmetal_values.sv tests/rtl/values_tb.sv
	$(LOCAL_TOOLS)/usr/bin/vvp build/unit/values.vvp
test-descriptors:
	mkdir -p build/unit
	$(LOCAL_TOOLS)/usr/bin/iverilog -B$(LOCAL_TOOLS)/usr/lib/x86_64-linux-gnu/ivl -g2012 -s descriptors_tb -o build/unit/descriptors.vvp rtl/wasmetal_descriptors.sv tests/rtl/descriptors_tb.sv
	$(LOCAL_TOOLS)/usr/bin/vvp build/unit/descriptors.vvp
fpga-sim:
	python3 tools/build_fpga_sim.py
fpga-smoke: fpga-sim
	python3 tools/check_fpga.py
fpga-host: sim/core_config.hpp
	python3 tools/build_identity.py begin build/wasmetal-fpga --profile physical
	g++ -std=c++17 -O2 -Wall -Wextra -Werror -DWASMETAL_FPGA sim/main.cpp -o build/wasmetal-fpga
	python3 tools/build_identity.py finish build/wasmetal-fpga
fpga-core:
	python3 tools/synth.py --fpga --fast-share --lut4 --output-name core-ecp5
fpga-bitstream: fpga-core
	python3 tools/build_board.py --core-netlist build/core-ecp5.json
synth:
	python3 tools/synth.py
