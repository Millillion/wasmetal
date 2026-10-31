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
.PHONY: sim lint test test-all synth
sim: build/obj/Vwasmetal_core
build/obj/Vwasmetal_core: $(RTL) sim/main.cpp Makefile
	$(VERILATOR) $(VFLAGS) --cc --exe --build -j 4 --Mdir build/obj -CFLAGS '-std=c++17 -O2 -Wall -Wextra -Werror' $(RTL) $(CURDIR)/sim/main.cpp
lint:
	$(VERILATOR) $(VFLAGS) --lint-only $(RTL)
test: sim
	python3 tools/run_spec.py --suite i32 --suite i64
test-all: sim
	python3 tools/run_spec.py
synth:
	python3 tools/synth.py
