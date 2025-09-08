import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, ReadOnly
import random
from cocotb_coverage.coverage import coverage_db

from cocotbext.lin.driver import LinDriver
from cocotbext.lin.monitor import LinMonitor
from cocotbext.lin.scoreboard import LinScoreboard
import cocotbext.lin.utils as utils

from cocotbext.lin.coverage import cover_pid, cover_data_byte, cover_data_len, protocol_cover


@cocotb.test()
async def lin_top_test(dut):
    # Reset
    dut.rstn.value = 1
    await Timer(1, "ns")
    dut.rstn.value = 0
    await Timer(1, "ns")
    await RisingEdge(dut.sys_clk)
    dut.rstn.value = 1

    # Clock
    cocotb.start_soon(Clock(dut.sys_clk, 10, "ns").start())

    # Init VIP
    driver = LinDriver(dut, dut.sys_clk)
    scoreboard = LinScoreboard(dut, utils)
    monitor = LinMonitor(dut, callback=protocol_cover)
    cocotb.start_soon(monitor.run())

    for i in range(20):
        pid = random.randint(0, 0x3F)
        data_len = random.randint(1, 8)
        data_bytes = [random.randint(0, 0xFF) for _ in range(data_len)]

        cover_pid(pid)
        cover_data_len(data_len)
        for b in data_bytes:
            cover_data_byte(b)

        padded = await driver.send(pid, data_bytes)

        await RisingEdge(dut.comm_tx_done)
        await ReadOnly()
        await scoreboard.check_header(pid)

        await RisingEdge(dut.resp_tx_done)
        await ReadOnly()
        await scoreboard.check_response(padded)

        await Timer(50, "ns")

    coverage_db.report_coverage(cocotb.log.info, bins=True)
    coverage_db.export_to_xml("coverage.xml")
