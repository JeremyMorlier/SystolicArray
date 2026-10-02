import random

import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test(dut):
    """Try accessing the design."""

    data_width = dut.DATA_WIDTH.value
    dut._log.info("DATA_WIDTH is %s", data_width)
    a = 1023
    b = 1023
    expected = a * b

    dut.A.value = a
    dut.B.value = b
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
    assert dut.X.value == expected


async def tick(dut, n=1):
    """Drive n clock cycles (simple manual clock)."""
    for _ in range(n):
        dut.clk.value = 0
        await Timer(1, units="ns")
        dut.clk.value = 1
        await Timer(1, units="ns")


def u(val, bits):
    """Unsigned wrap to 'bits' bits."""
    return val & ((1 << bits) - 1)


async def init_dut(dut):
    dut.compute.value = 0
    dut.A.value = 0
    dut.B.value = 0
    await tick(dut, 2)


def get_widths(dut):
    data_width = int(dut.DATA_WIDTH.value)
    out_bits = 2 * data_width + 2  # because X is [2*DATA_WIDTH+1:0]
    max_w = (1 << data_width) - 1
    max_out = (1 << out_bits) - 1
    return data_width, out_bits, max_w, max_out


async def apply_and_check(dut, a, b, out_bits, max_out, compute=1):
    # Capture previous X to verify hold when compute=0
    prev_x = int(dut.X.value)

    dut.A.value = a
    dut.B.value = b
    dut.compute.value = compute

    # One rising edge updates state if compute=1
    await tick(dut, 1)

    got = int(dut.X.value)

    if compute == 0:
        assert got == prev_x, f"X changed while compute=0: prev={prev_x} got={got}"
        return

    full = a * b
    expected = u(full, out_bits)

    # Detect if arithmetic overflow happened beyond output width
    overflow = full > max_out

    assert got == expected, (
        f"Mismatch: A={a} B={b} full={full} expected(masked)={expected} got={got}"
    )

    # Log overflow cases (not a failure—just evidence we hit them)
    if overflow:
        dut._log.info(f"Overflow case hit: A={a} B={b} full={full} masked={expected}")


@cocotb.test()
async def compute_hold_when_low(dut):
    _, out_bits, max_w, max_out = get_widths(dut)
    await init_dut(dut)

    await apply_and_check(dut, 5, 7, out_bits, max_out, compute=0)
    await apply_and_check(dut, max_w, max_w, out_bits, max_out, compute=0)


@cocotb.test()
async def edge_cases(dut):
    _, out_bits, max_w, max_out = get_widths(dut)
    await init_dut(dut)

    vectors = [
        (0, 0),
        (0, max_w),
        (max_w, 0),
        (1, 1),
        (max_w, 1),
        (1, max_w),
        (max_w, max_w),  # max product
    ]
    for a, b in vectors:
        await apply_and_check(dut, a, b, out_bits, max_out, compute=1)


@cocotb.test()
async def overflow_cases(dut):
    _, out_bits, max_w, max_out = get_widths(dut)
    await init_dut(dut)

    # Product is at most (2^W-1)^2 < 2^(2W). Adding C (up to 2^W-1)
    # can overflow into bit 2W (and beyond), which is why X is wider.
    # Make product near its max and add max C to force carry.
    await apply_and_check(dut, max_w, max_w, out_bits, max_out, compute=1)

    # Another overflow-ish pattern: big product + big C
    await apply_and_check(dut, max_w, max_w - 1, out_bits, max_out, compute=1)


@cocotb.test()
async def random_stress(dut):
    _, out_bits, max_w, max_out = get_widths(dut)
    await init_dut(dut)

    random.seed(0xC0C0)
    trials = 200

    def biased_rand():
        # Bias toward corners to hit edge cases often
        r = random.random()
        if r < 0.20:
            return 0
        if r < 0.40:
            return 1
        if r < 0.60:
            return max_w
        if r < 0.70:
            return max_w - 1
        return random.randint(0, max_w)

    for _ in range(trials):
        a = biased_rand()
        b = biased_rand()
        await apply_and_check(dut, a, b, out_bits, max_out, compute=1)


@cocotb.test()
async def compute_hold_after_update(dut):
    _, out_bits, max_w, max_out = get_widths(dut)
    await init_dut(dut)

    # Test that the PE holds its output when compute is low
    await apply_and_check(dut, 13, 17, out_bits, max_out, compute=1)
    await apply_and_check(dut, 0, 0, out_bits, max_out, compute=0)
    await apply_and_check(dut, max_w, max_w, out_bits, max_out, compute=0)
