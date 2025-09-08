class LinScoreboard:
    def __init__(self, dut, utils):
        self.dut = dut
        self.utils = utils

    async def check_header(self, pid):
        actual = int(self.dut.frame_header_out.value)
        expected, _ = self.utils.build_expected_header(pid)
        assert actual == expected, f"Header mismatch: {hex(actual)} != {hex(expected)}"

    async def check_response(self, data_bytes):
        actual = int(self.dut.response_out.value)
        expected, _ = self.utils.build_expected_response(data_bytes)
        assert actual == expected, f"Response mismatch: {hex(actual)} != {hex(expected)}"
