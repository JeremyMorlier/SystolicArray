# Makefile
SIM ?= verilator
TOPLEVEL_LANG ?= verilog
VERILOG_SOURCES += d_ff.v 
TOPLEVEL = d_ff 
MODULE = test 
include $(shell cocotb-config --makefiles)/Makefile.sim

# adder:
# # defaults
# SIM ?= verilator
# TOPLEVEL_LANG ?= verilog

# VERILOG_SOURCES += $(PWD)/../adder.v
# # use VHDL_SOURCES for VHDL files

# # TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
# TOPLEVEL = adder

# # MODULE is the basename of the Python test file
# MODULE = test_adder

# # include cocotb's make rules to take care of the simulator setup
# include $(shell cocotb-config --makefiles)/Makefile.sim