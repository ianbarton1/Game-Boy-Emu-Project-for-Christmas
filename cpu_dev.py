from bus import read_byte_at_pc
from cpu import CPU
from number.long_int import LongInt
from number.short_int import ShortInt

cpu_obj:CPU = CPU()

register = cpu_obj.bus.read(0xFF00 + read_byte_at_pc(cpu_obj))
