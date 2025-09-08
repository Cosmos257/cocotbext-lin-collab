from cocotb.triggers import RisingEdge, FallingEdge


class LinMonitor:
    def __init__(self, dut, callback=None):
        self.dut = dut
        self.callback = callback
        self.prev = "Idle"

    async def run(self):
        while int(self.dut.rstn.value) == 0:
            await RisingEdge(self.dut.sys_clk)
        while True:
            # Header
            await RisingEdge(self.dut.comm_tx_done)
            self._notify("HeaderTx")

            # Response
            await RisingEdge(self.dut.resp_tx_done)
            self._notify("ResponseTx")

            # Back to Idle
            await FallingEdge(self.dut.resp_tx_done)
            self._notify("Idle")

    def _notify(self, state):
        if self.callback:
            txn = {"previous": self.prev, "current": state}
            self.callback(txn)
        self.prev = state
