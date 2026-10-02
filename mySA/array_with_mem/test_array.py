import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test(dut):
    """First test to check the basic functionnalioty of the PE array."""

    data_width = dut.DATA_WIDTH.value
    dut._log.info("DATA_WIDTH is %s", data_width)
    a = 1
    b = [1, 2, 3, 4]

    first = a * b[0]
    second = b[1] * first
    third = b[2] * second
    fourth = b[3] * third
    expected = fourth

    dut.compute.value = 0
    dut.init.value = 0

    # Load RAM A and RAM B at address 0
    b_word = 0
    for i in range(len(b)):
        b_word |= b[i] << (i * data_width)

    a_word = a
    # for i in range(len(a)):
    #     a_word |= a[i] << (i * data_width)
    dut.we_a.value = 1
    dut.addr_a.value = 0
    dut.din_a.value = a_word
    dut.we_b.value = 1
    dut.addr_b.value = 0
    dut.din_b.value = b_word
    dut.clk.value = 0
    await Timer(1, units="ns")
    dut.clk.value = 1
    await Timer(1, units="ns")
    dut.we_a.value = 0
    dut.we_b.value = 0

    for cycle in range(10):
        dut.clk.value = 0
        await Timer(1, units="ns")
        dut.clk.value = 1
        await Timer(1, units="ns")
        dut.init.value = 1
        dut.clk.value = 0
        await Timer(1, units="ns")
        dut.init.value = 0
        dut.clk.value = 1
        await Timer(1, units="ns")
        dut.compute.value = 1
        dut.clk.value = 0
        await Timer(1, units="ns")
        dut.clk.value = 1
        await Timer(1, units="ns")
        dut.clk.value = 0
        await Timer(1, units="ns")
        dut.clk.value = 1
        await Timer(1, units="ns")
        dut.clk.value = 0
        await Timer(1, units="ns")
        dut.clk.value = 1
        await Timer(1, units="ns")
        dut.clk.value = 0
        await Timer(1, units="ns")
        dut.clk.value = 1
        await Timer(1, units="ns")

    dut._log.info("X is %s %s", dut.array_output.value, expected)
    assert dut.array_output.value == expected
