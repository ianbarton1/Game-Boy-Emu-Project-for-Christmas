class ShortInt:
    def __init__(self, value:int = 0) -> None:
        self.value = value

    def __repr__(self)->str:
        return hex(self.value)
    
    def get_bit(self, bit_number:int)->bool:
        '''
            Gets a single bit from the ShortInt Value,
            This uses least significant bit as bit 0 convention.

            Thus for 8 bit value:
            Bit 7 is the top bit (Msb)
            Bit 0 is the bottom bit (Lsb)
        
        '''
        
        mask:int = 1 << bit_number
        
        return bool((self.value & mask) >> bit_number)
    

    def write_bit(self, bit_number:int, bit:bool)->None:
        '''
            Sets a single bit as provided
            This uses least significant bit as bit 0 convention.

            Thus for 8 bit value:
            Bit 7 is the top bit (Msb)
            Bit 0 is the bottom bit (Lsb)
        
        '''

        if bit:
            #set bit
            mask:int = 1 << bit_number

            self.value |= mask

            return
        
        #clear bit
        
        mask:int = 255 ^ (1 << bit_number)

        self.value &= mask




    
