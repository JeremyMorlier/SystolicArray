SIM ?= verilator
TOPLEVEL_LANG ?= verilog

BUILD_DIR := build

# Put all simulator-generated files in build/
SIM_BUILD := $(BUILD_DIR)

# Put cocotb results in build/
COCOTB_RESULTS_FILE := $(BUILD_DIR)/results.xml

EXTRA_ARGS += --trace --trace-structs

VERILOG_SOURCES += pe.v
# VERILOG_SOURCES += pe_array.v

TOPLEVEL = pe
MODULE = test_pe

include $(shell cocotb-config --makefiles)/Makefile.sim