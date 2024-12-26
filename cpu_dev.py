from cpu import CPU
from number.long_int import LongInt
from number.short_int import ShortInt

cpu_obj:CPU = CPU()

cpu_obj.bus.read(cpu_obj.register_BC.value)

