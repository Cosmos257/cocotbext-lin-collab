import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb_coverage.coverage import coverage_db

from cocotbext.lin.coverage.coverage import protocol_cover


class LinMonitor:
    def __init__(self, dut):
        self.dut = dut
        cocotb.start_soon(self._monitor())

    async def _monitor(self):
        """Monitor DUT signals for protocol state transitions and record coverage."""
        prev = "Idle"

        # Wait for reset to finish
        while int(self.dut.rstn.value) == 0:
            await RisingEdge(self.dut.sys_clk)

        while True:
            # HEADER phase
            await RisingEdge(self.dut.comm_tx_done)
            protocol_cover({"previous": prev, "current": "HeaderTx"})
            prev = "HeaderTx"

            # RESPONSE phase
            await RisingEdge(self.dut.resp_tx_done)
            protocol_cover({"previous": prev, "current": "ResponseTx"})
            prev = "ResponseTx"

            # Idle phase
            await FallingEdge(self.dut.resp_tx_done)
            protocol_cover({"previous": prev, "current": "Idle"})
            prev = "Idle"
