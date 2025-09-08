class LinBus:
    def __init__(self, dut):
        self.clk = dut.sys_clk
        self.rstn = dut.rstn
        self.pid = dut.pid
        self.data = dut.data
        self.comm_tx_done = dut.comm_tx_done
        self.resp_tx_done = dut.resp_tx_done
        self.frame_header_out = dut.frame_header_out
        self.response_out = dut.response_out
