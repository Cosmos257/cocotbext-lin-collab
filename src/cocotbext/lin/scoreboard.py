from utils import build_expected_header, build_expected_response
from cocotb.triggers import RisingEdge, ReadOnly

class LinScoreboard:
    def __init__(self, dut):
        self.dut = dut

    async def check(self, transaction, i):
        # Header
        await RisingEdge(self.dut.comm_tx_done)
        await ReadOnly()
        actual_header = int(self.dut.frame_header_out.value)
        expected_header, _ = build_expected_header(transaction.pid)
        assert actual_header == expected_header, \
            f"[Header Mismatch] Tx {i}: {hex(actual_header)} != {hex(expected_header)}"

        # Response
        await RisingEdge(self.dut.resp_tx_done)
        await ReadOnly()
        actual_response = int(self.dut.response_out.value)
        expected_response, _ = build_expected_response(transaction.data_bytes + [0] * (8 - len(transaction.data_bytes)))
        assert actual_response == expected_response, \
            f"[Response Mismatch] Tx {i}: {hex(actual_response)} != {hex(expected_response)}"
