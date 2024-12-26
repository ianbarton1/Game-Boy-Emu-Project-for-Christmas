from number.long_int import LongInt
from number.short_int import ShortInt

a = ShortInt()
b = LongInt()

b.signed_value = -32000

for _ in range(200):
    
    # print(a, a.value, a.signed_value)
    # a.signed_value -= 1

    print(b, b.value, b.signed_value, b.high_byte, b.low_byte)
    b.signed_value -= 1

