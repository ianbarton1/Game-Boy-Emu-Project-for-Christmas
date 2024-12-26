from number.short_int import ShortInt


class LongInt:
    def __init__(self, value = 0) -> None:
        

        self.high_byte = ShortInt((value >> 8) & 255)
        self.low_byte = ShortInt(value & 255)

    def _convert_signed_unsigned(self, value:int)->int:
        '''
            Converts an unsigned integer to the equivalent signed integer and vise-versa
        '''
        return -1 * ((value ^ 65535) + 1)

    @property
    def value(self)->int:
        return (self.high_byte.value << 8) + self.low_byte.value
    
    @value.setter
    def value(self, new_value:int):
        '''
            Unsigned value of this long int
        
        '''
        if new_value < 0:
            new_value += 65536 

        self.high_byte.value = (new_value >> 8) & 255
        self.low_byte.value = (new_value & 255)

    @property
    def signed_value(self):
        if self.high_byte.get_bit(bit_number=7):
            return self._convert_signed_unsigned(self.value)
        
        return self.value

    @signed_value.setter
    def signed_value(self, new_value:int):
        if new_value < 0:
            new_value = self._convert_signed_unsigned(new_value)
        
        self.value = new_value

    def __repr__(self)->str:
        return hex(self.value)