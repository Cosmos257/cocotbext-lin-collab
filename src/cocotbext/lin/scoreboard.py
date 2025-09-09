from .utils import build_expected_header, build_expected_response
from cocotb.triggers import RisingEdge, ReadOnly
import cocotb


class LinScoreboard:
    def __init__(self, dut):
        self.dut = dut

    async def check(self, transaction, i):
        cocotb.log.info(f"\n===== Transaction {i} =====")
        cocotb.log.info(f"[INPUT] PID = 0x{transaction.pid:02X}, "
                        f"Data = {[hex(x) for x in transaction.data_bytes]} "
                        f"(padded: {[hex(x) for x in (transaction.data_bytes + [0]*(8-len(transaction.data_bytes)))]})")

        # --- Header ---
        await RisingEdge(self.dut.comm_tx_done)
        await ReadOnly()
        actual_header = int(self.dut.frame_header_out.value)
        expected_header, _ = build_expected_header(transaction.pid)

        cocotb.log.info(f"[HEADER] Expected: 0x{expected_header:X}")
        cocotb.log.info(f"[HEADER] Actual:   0x{actual_header:X}")

        assert actual_header == expected_header, \
            f"[Header Mismatch] Tx {i}: {hex(actual_header)} != {hex(expected_header)}"

        # --- Response ---
        await RisingEdge(self.dut.resp_tx_done)
        await ReadOnly()
        actual_response = int(self.dut.response_out.value)
        expected_response, _ = build_expected_response(
            transaction.data_bytes + [0] * (8 - len(transaction.data_bytes))
        )

        cocotb.log.info(f"[RESPONSE] Expected: 0x{expected_response:X}")
        cocotb.log.info(f"[RESPONSE] Actual:   0x{actual_response:X}")

        assert actual_response == expected_response, \
            f"[Response Mismatch] Tx {i}: {hex(actual_response)} != {hex(expected_response)}"


