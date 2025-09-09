import cocotb
from cocotb.triggers import Timer, RisingEdge, ReadOnly
from cocotb_coverage.coverage import coverage_db
import os

from cocotbext.lin.bus import LinBus
from cocotbext.lin.driver import LinDriver
from cocotbext.lin.monitor import LinMonitor
from cocotbext.lin.scoreboard import LinScoreboard
from cocotbext.lin.config import random_pid, random_data

# Import coverage functions
from cocotbext.lin.coverage.coverage import cover_pid, cover_data_byte, cover_data_len


@cocotb.test()
async def lin_top_test(dut):
    # Reset DUT
    dut.rstn.value = 1
    await Timer(1, "ns")
    dut.rstn.value = 0
    await Timer(1, "ns")
    await RisingEdge(dut.sys_clk)
    dut.rstn.value = 1

    # Start monitor and scoreboard
    LinMonitor(dut)  # this handles protocol_cover internally
    driver = LinDriver(dut)
    scoreboard = LinScoreboard(dut)

    # Run CRV transactions
    for i in range(30):
        pid = random_pid()
        length, data_bytes = random_data()
        txn = LinBus(pid, data_bytes)

        # --- Coverage calls for values ---
        cover_pid(pid)
        cover_data_len(length)
        for b in data_bytes:
            cover_data_byte(b)

        # Drive and check
        await driver.send(txn)
        await scoreboard.check(txn, i+1)
        await Timer(50, "ns")

    # --- Coverage reporting ---
    coverage_db.report_coverage(cocotb.log.info, bins=True)
    coverage_file = os.path.join(os.getenv("RESULT_PATH", "./"), "coverage.xml")
    coverage_db.export_to_xml(filename=coverage_file)

