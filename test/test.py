import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, ReadOnly

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # A=0, B=0 → S=0, C=0
    dut.ui_in[0].value = 0
    dut.ui_in[1].value = 0
    await ClockCycles(dut.clk, 1)
    await ReadOnly()
    assert dut.uo_out[0].value == 0
    assert dut.uo_out[1].value == 0

    # A=0, B=1 → S=1, C=0
    dut.ui_in[0].value = 0
    dut.ui_in[1].value = 1
    await ClockCycles(dut.clk, 1)
    await ReadOnly()
    assert dut.uo_out[0].value == 1
    assert dut.uo_out[1].value == 0

    # A=1, B=0 → S=1, C=0
    dut.ui_in[0].value = 1
    dut.ui_in[1].value = 0
    await ClockCycles(dut.clk, 1)
    await ReadOnly()
    assert dut.uo_out[0].value == 1
    assert dut.uo_out[1].value == 0

    # A=1, B=1 → S=0, C=1
    dut.ui_in[0].value = 1
    dut.ui_in[1].value = 1
    await ClockCycles(dut.clk, 1)
    await ReadOnly()
    assert dut.uo_out[0].value == 0
    assert dut.uo_out[1].value == 1
