SIM ?= verilator 
TOPLEVEL_LANG ?= verilog
EXTRA_ARGS += --trace --trace-structs
VERILOG_SOURCES += pe.v 
TOPLEVEL = pe 
MODULE = test_pe

# ---- Waveform dumping ----

# ---------------------------
include $(shell cocotb-config --makefiles)/Makefile.sim