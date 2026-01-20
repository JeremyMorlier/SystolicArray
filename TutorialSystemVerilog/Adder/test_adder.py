import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test_adder(dut):
    """Try accessing the design."""

    dut.A.value = 10
    dut.B.value = 10
    dut.compute.value = 0
    for cycle in range(10):
        dut.clk.value = 0
        await Timer(1, units="ns")
        dut.clk.value = 1
        await Timer(1, units="ns")

    dut._log.info("X is %s", dut.X.value)
    assert dut.X.value == 0

    dut.compute.value = 1

    for cycle in range(10):
        dut.clk.value = 0
        await Timer(1, units="ns")
        dut.clk.value = 1
        await Timer(1, units="ns")

    dut._log.info("X is %s", dut.X.value)
    assert dut.X.value == 20