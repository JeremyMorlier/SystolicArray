# Wrapper around OpenROAD-flow-scripts.
#   make                         full RTL-to-GDS flow (default VARIANT=array_with_mem)
#   make VARIANT=PE              run the plain array without memories
#   make synth|floorplan|place|cts|route|finish
#   make gui_final               open the final layout in the OpenROAD GUI
#   make clean_all               remove this variant's results
ORFS_FLOW ?= $(abspath ../../OpenROAD-flow-scripts/flow)
VARIANT   ?= array_with_mem
YOSYS_EXE ?= $(shell command -v yosys || echo $(HOME)/Toolchain/oss-cad-suite-linux-x64-20260929/oss-cad-suite/bin/yosys)
OPENROAD_EXE ?= $(shell command -v openroad)

ORFS_ARGS = -C $(ORFS_FLOW) \
            DESIGN_CONFIG=$(abspath config.mk) \
            WORK_HOME=$(abspath work) \
            VARIANT=$(VARIANT) \
            YOSYS_EXE=$(YOSYS_EXE) \
            OPENROAD_EXE=$(OPENROAD_EXE)

.DEFAULT_GOAL := all
all:
	$(MAKE) $(ORFS_ARGS)

%:
	$(MAKE) $(ORFS_ARGS) $@
