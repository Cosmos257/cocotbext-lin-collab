import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly
from cocotb_coverage.coverage import CoverPoint, CoverCross

@CoverPoint("top.prot.lin.current",  xf=lambda t: t["current"],  bins=["Idle","HeaderTx","ResponseTx"])
@CoverPoint("top.prot.lin.previous", xf=lambda t: t["previous"], bins=["Idle","HeaderTx","ResponseTx"])
@CoverCross("top.prot.lin.cross", items=["top.prot.lin.previous","top.prot.lin.current"])
def protocol_cover(t): pass


async def protocol_monitor(dut):
    prev = "Idle"
    while int(dut.rstn.value) == 0:
        await RisingEdge(dut.sys_clk)

    while True:
        await RisingEdge(dut.comm_tx_done)
        protocol_cover({"previous": prev, "current": "HeaderTx"})
        prev = "HeaderTx"

        await RisingEdge(dut.resp_tx_done)
        protocol_cover({"previous": prev, "current": "ResponseTx"})
        prev = "ResponseTx"

        await FallingEdge(dut.resp_tx_done)
        protocol_cover({"previous": prev, "current": "Idle"})
        prev = "Idle"
