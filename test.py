import ctypes
from memory import MemoryBlock
from number.long_int import LongInt
from number.short_int import ShortInt

number = ShortInt(0)

number.upper_nibble = 0b1111
number.lower_nibble = 0

def print_number(number):
    print("---")
    print(number.value)
    print("upper",number.upper_nibble)
    print("lower",number.lower_nibble)

    print(bin(number.value))
    print("upper", bin(number.upper_nibble))
    print("lower",bin(number.lower_nibble))

print_number(number)

number.swap_nibbles()

print_number(number)


pixels = (ctypes.c_ubyte * (16*16 * 3))()


print(len(pixels))