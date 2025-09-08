from cocotb_coverage.coverage import CoverPoint, CoverCross

@CoverPoint("top.prot.lin.current", xf=lambda t: t["current"], bins=["Idle","HeaderTx","ResponseTx"])
@CoverPoint("top.prot.lin.previous", xf=lambda t: t["previous"], bins=["Idle","HeaderTx","ResponseTx"])
@CoverCross("top.prot.lin.cross", items=["top.prot.lin.previous","top.prot.lin.current"])
def protocol_cover(t):
    pass

@CoverPoint("top.lin.pid", xf=lambda pid: "low" if pid < 21 else ("medium" if pid < 42 else "high"), bins=["low", "medium", "high"])
def cover_pid(pid):
    pass

@CoverPoint("top.lin.data_byte", xf=lambda b: "low" if b < 85 else ("medium" if b < 170 else "high"), bins=["low", "medium", "high"])
def cover_data_byte(b):
    pass

@CoverPoint("top.lin.data_len", xf=lambda length: length, bins=list(range(1, 9)))
def cover_data_len(length):
    pass
