# lin_top_test.py

import cocotb
from cocotb.triggers import Timer
from cocotb_coverage.coverage import coverage_db
import os

from bus import LinTransaction
from driver import LinDriver
from monitor import protocol_monitor
from scoreboard import LinScoreboard
from config import random_pid, random_data


@cocotb.test()
async def lin_top_test(dut):
    dut.rstn.value = 1
    await Timer(1, "ns")
    dut.rstn.value = 0
    await Timer(1, "ns")
    dut.rstn.value = 1

    cocotb.start_soon(protocol_monitor(dut))
    driver = LinDriver(dut)
    scoreboard = LinScoreboard(dut)

    for i in range(30):
        pid = random_pid()
        length, data_bytes = random_data()
        txn = LinTransaction(pid, data_bytes)

        await driver.send(txn)
        await scoreboard.check(txn, i+1)
        await Timer(50, "ns")

    coverage_db.report_coverage(cocotb.log.info, bins=True)
    coverage_file = os.path.join(os.getenv("RESULT_PATH", "./"), "coverage.xml")
    coverage_db.export_to_xml(filename=coverage_file)
