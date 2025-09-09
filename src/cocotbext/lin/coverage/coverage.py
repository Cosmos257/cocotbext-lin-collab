from cocotb_coverage.coverage import CoverPoint, CoverCross

PID_LOW_THRESHOLD = 21
PID_MEDIUM_THRESHOLD = 42
BYTE_LOW_THRESHOLD = 85
BYTE_MEDIUM_THRESHOLD = 170


@CoverPoint("top.prot.lin.current", xf=lambda t: t["current"], bins=["Idle","HeaderTx","ResponseTx"])
@CoverPoint("top.prot.lin.previous", xf=lambda t: t["previous"], bins=["Idle","HeaderTx","ResponseTx"])
@CoverCross("top.prot.lin.cross", items=["top.prot.lin.previous","top.prot.lin.current"])
def protocol_cover(t):
    pass

@CoverPoint("top.lin.pid", xf=lambda pid: "low" if pid < PID_LOW_THRESHOLD else ("medium" if pid < PID_MEDIUM_THRESHOLD  else "high"), bins=["low", "medium", "high"])
def cover_pid(pid):
    pass

@CoverPoint("top.lin.data_byte", xf=lambda b: "low" if b < BYTE_LOW_THRESHOLD else ("medium" if b < BYTE_MEDIUM_THRESHOLD  else "high"), bins=["low", "medium", "high"])
def cover_data_byte(b):
    pass

@CoverPoint("top.lin.data_len", xf=lambda length: length, bins=list(range(1, 9)))
def cover_data_len(length):
    pass

