"""Drive a DUT cycle by cycle from a CSV file and check its outputs.

CSV format (one row = one clock cycle):
  - header row with signal names; columns named "cycle" or "comment" are ignored
  - columns listed in `outputs` are expected values, checked after the rising edge
  - all other columns are inputs, applied before the rising edge
  - values are integers (decimal, 0x.., 0b..); an empty cell or "x" means
    "keep previous value" for inputs and "don't care" for outputs
"""

import csv

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, ReadOnly, RisingEdge

IGNORED_COLUMNS = {"cycle", "comment"}


def _parse(cell):
    cell = cell.strip()
    if cell == "" or cell.lower() == "x":
        return None
    return int(cell, 0)


async def run_csv(dut, path, outputs, clk_name="clk", period_ns=2):
    clk = getattr(dut, clk_name)
    cocotb.start_soon(Clock(clk, period_ns, units="ns").start())

    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))

    errors = []
    for line, row in enumerate(rows, start=2):  # line 1 is the header
        cycle = row.get("cycle", line - 2)

        # apply inputs while the clock is low
        await FallingEdge(clk)
        for name, cell in row.items():
            if name in IGNORED_COLUMNS or name in outputs:
                continue
            value = _parse(cell)
            if value is not None:
                getattr(dut, name).value = value

        # sample outputs once the rising edge has settled
        await RisingEdge(clk)
        await ReadOnly()
        for name in outputs:
            expected = _parse(row.get(name, ""))
            if expected is None:
                continue
            got = getattr(dut, name).value
            if not got.is_resolvable or got.integer != expected:
                shown = got.integer if got.is_resolvable else got.binstr
                msg = f"cycle {cycle} (line {line}): {name} expected {expected}, got {shown}"
                dut._log.error(msg)
                errors.append(msg)

    assert not errors, f"{len(errors)} mismatch(es):\n" + "\n".join(errors)
