import random
from cocotb.triggers import RisingEdge


class LinDriver:
    def __init__(self, dut, clock):
        self.dut = dut
        self.clock = clock

    async def send(self, pid, data_bytes):
        # Pad to 8 bytes
        padded_data = data_bytes + [0] * (8 - len(data_bytes))
        self.dut.pid.value = pid
        self.dut.data.value = int.from_bytes(bytes(padded_data), "little")
        await RisingEdge(self.clock)
        return padded_data


