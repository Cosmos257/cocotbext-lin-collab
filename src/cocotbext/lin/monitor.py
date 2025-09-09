import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb_coverage.coverage import CoverPoint, CoverCross

# Coverage points
@CoverPoint("top.prot.lin.current", xf=lambda t: t["current"], bins=["Idle","HeaderTx","ResponseTx"])
@CoverPoint("top.prot.lin.previous", xf=lambda t: t["previous"], bins=["Idle","HeaderTx","ResponseTx"])
@CoverCross("top.prot.lin.cross", items=["top.prot.lin.previous","top.prot.lin.current"])
def protocol_cover(t):
    pass

class LinMonitor:
    """Cocotb monitor for LIN protocol transitions with coverage."""
    def __init__(self, dut):
        self.dut = dut
        self.prev = "Idle"
        cocotb.start_soon(self._monitor())

    async def _monitor(self):
        # Wait for reset to deassert
        while int(self.dut.rstn.value) == 0:
            await RisingEdge(self.dut.sys_clk)

        while True:
            await RisingEdge(self.dut.comm_tx_done)
            protocol_cover({"previous": self.prev, "current": "HeaderTx"})
            self.prev = "HeaderTx"

            await RisingEdge(self.dut.resp_tx_done)
            protocol_cover({"previous": self.prev, "current": "ResponseTx"})
            self.prev = "ResponseTx"

            await FallingEdge(self.dut.resp_tx_done)
            protocol_cover({"previous": self.prev, "current": "Idle"})
            self.prev = "Idle"
