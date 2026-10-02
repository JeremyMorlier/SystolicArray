# OpenROAD-flow-scripts design config for the systolic PE array.
# Select the RTL variant with VARIANT=PE (plain array) or VARIANT=array_with_mem.
BACKEND_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
VARIANT     ?= array_with_mem

export DESIGN_NICKNAME = pe_array
export DESIGN_NAME     = array
export PLATFORM       ?= sky130hd
export FLOW_VARIANT    = $(VARIANT)

export VERILOG_FILES = $(BACKEND_DIR)../$(VARIANT)/pe.v \
                       $(BACKEND_DIR)../$(VARIANT)/pe_array.v
export SDC_FILE      = $(BACKEND_DIR)constraint.sdc

# RTL uses SystemVerilog (logic, unpacked array ports) -> use the slang frontend
export SYNTH_HDL_FRONTEND = slang
export VERILOG_TOP_PARAMS = NUM_PES 4 DATA_WIDTH 10

export CORE_UTILIZATION = 40
export PLACE_DENSITY    = 0.60
export TNS_END_PERCENT  = 100
