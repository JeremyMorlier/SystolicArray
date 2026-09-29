SIM ?= verilator 
TOPLEVEL_LANG ?= verilog
EXTRA_ARGS += --trace --trace-structs
VERILOG_SOURCES += pe.v 
VERILOG_SOURCES += pe_array.v
TOPLEVEL = array 
MODULE = test_array

# ---- Waveform dumping ----

# ---------------------------
include $(shell cocotb-config --makefiles)/Makefile.sim