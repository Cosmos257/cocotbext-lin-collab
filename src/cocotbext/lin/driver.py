import cocotb
from cocotb.triggers import RisingEdge

class LinDriver:
    def __init__(self, dut):
        self.dut = dut

    async def send(self, transaction):
        padded = transaction.data_bytes + [0] * (8 - len(transaction.data_bytes))
        self.dut.pid.value = transaction.pid
        self.dut.data.value = int.from_bytes(bytes(padded), "little")
        await RisingEdge(self.dut.sys_clk)


