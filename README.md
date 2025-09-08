# lin COCOTB VIP for lin protocol
LIN VIP

# install
`pip3 install cocotbext_lin`

#Usage

```
from cocotbext.lin import LinBus,LinDriver,LinConfig

....
class Env:
   def __init__(self,dut):
	lin_bus = LinBus(from_prefix='...',dut=....)
	lin_config = LinConfig()
	lin_config.<key>=<value>
	lin_driver = linDriver(lin_bus, lin_config)
   async def xyz(self):
 	lin_driver.write(address,byteArray)
 	rv =lin_driver.read(address,numbytes)
	assert rv=byteArray, "Data mismatch at %X"%(address)

