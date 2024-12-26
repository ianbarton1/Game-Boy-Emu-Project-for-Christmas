from number.short_int import ShortInt

a = ShortInt()

a.write_bit(bit_number= 7, bit= True)

print(a.value)

print(a.get_bit(7))

a.write_bit(bit_number=7, bit=False)
print(a.get_bit(7))