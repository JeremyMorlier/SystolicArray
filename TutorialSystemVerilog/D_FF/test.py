import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def my_first_test4(dut):
    """Try accessing the design."""

    for cycle in range(10):
        dut.clk.value = 0
        await Timer(1, units="ns")
        dut.clk.value = 1
        await Timer(1, units="ns")

    dut._log.info("my_signal_1 is %s", dut.d.value)
    assert dut.d.value[0] == 0, "my_signal_2[0] is not 0!"

@cocotb.test()
async def my_second_test(dut):
    """Try accessing the design."""

    for cycle in range(100):
        dut.clk.value = 0
        await Timer(1, units="ns")
        dut.clk.value = 1
        await Timer(1, units="ns")

    dut._log.info("my_signal_1 is %s", dut.d.value)
    assert dut.d.value[0] == 0, "my_signal_2[0] is not 0!"