from number.short_int import ShortInt


class LongInt:
    def __init__(self, value = 0) -> None:
        

        self.high_byte = ShortInt((value >> 8) & 255)
        self.low_byte = ShortInt(value & 255)

    @property
    def value(self)->int:
        return (self.high_byte.value << 8) + self.low_byte.value
    
    @value.setter
    def value(self, new_value:int):
        self.high_byte.value = (new_value >> 8) & 255
        self.low_byte.value = (new_value & 255)

    def __repr__(self)->str:
        return hex(self.value)