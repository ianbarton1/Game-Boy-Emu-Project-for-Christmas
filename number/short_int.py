class ShortInt:
    def __init__(self, value:int = 0) -> None:
        self._value = value
        self.write_viewer = None
        self.read_viewer = None
        self.write_token = None
        self.read_token = None

    def __repr__(self)->str:
        return hex(self._value)
    
    def add_write_viewer(self, viewer_fn:callable)->None:
        self.write_viewer = viewer_fn

    def clear_write_viewer(self)->None:
        self.write_viewer = None

    def clear_read_viewer(self)->None:
        self.read_viewer = None

    def add_read_viewer(self, viewer_fn:callable)->None:
        self.read_viewer = viewer_fn

    def add_write_token(self, write_token:int)->None:
        if self.write_viewer is not None:
            self.write_token = write_token
        
    def add_read_token(self, read_token:int)->None:
        if self.read_viewer is not None:
            self.read_token = read_token
    
    @property
    def value(self):
        if self.read_viewer is not None:
            if self.read_token is None:
                self.read_viewer()
            else:
                self.read_viewer(self.read_token)
        

        return self._value
    
    @value.getter
    def value(self):
        if self.read_viewer is not None:
            if self.read_token is None:
                self.read_viewer()
            else:
                self.read_viewer(self.read_token)

        return self._value
    
    @property
    def special_value(self):
        '''
            Viewerless property
        
        '''
        return self._value
    
    @special_value.setter
    def special_value(self, new_value:int):
        '''
            Sets the value without calling the viewer function
        '''
        self._value_setter(new_value=new_value)
    

    @property
    def upper_nibble(self)->int:
        return (self._value & 240) >> 4
    
    @property
    def lower_nibble(self)->int:
        return self._value & 15
    
    @upper_nibble.setter
    def upper_nibble(self, new_value:int)->None:
        '''
            Set a nibble must be between 0-15
        '''

        new_value = new_value & 15
        if new_value < 0:
            raise ValueError('negative nibble not allowed')
    
        self._value = (new_value << 4) + self.lower_nibble

    
    @lower_nibble.setter
    def lower_nibble(self, new_value:int)->None:
        '''
            Set a nibble must be between 0 - 15
        
        '''

        new_value = new_value & 15
        if new_value < 0:
            raise ValueError('negative nibble not allowed')
        
        self._value = (self.upper_nibble << 4) + new_value

    @value.setter
    def value(self, new_value:int):
        '''
            Unsigned value setter
        
        '''

        self._value_setter(new_value)

        if self.write_viewer is not None:
            if self.write_token is None:
                self.write_viewer()
            else:
                self.write_viewer(self.write_token)

    def _value_setter(self, new_value):
        if not isinstance(new_value, int):
            raise TypeError('value for shortint of invalid type, expected int')


        if new_value < 0:
            new_value += 256

        if new_value > 255:
            new_value -= 256

        new_value = new_value & 255
        
        self._value = new_value
    
    @property
    def signed_value(self)->int:
        if self.get_bit(bit_number=7):
            return -1 * ((self.value ^ 255) + 1)
        
        return self.value
    
    @signed_value.setter
    def signed_value(self, new_value)->None:
        '''
            convenience function to save a "signed" value back to to the shortint.
        '''

        if new_value < 0:
            self._value = -1 * ((new_value ^ 255) + 1)
        else:
            self._value = new_value
    
    def get_bit(self, bit_number:int)->bool:
        '''
            Gets a single bit from the ShortInt Value,
            This uses least significant bit as bit 0 convention.

            Thus for 8 bit value:
            Bit 7 is the top bit (Msb)
            Bit 0 is the bottom bit (Lsb)
        
        '''
        
        mask:int = 1 << bit_number
        
        return bool((self.special_value & mask) >> bit_number)
    

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

            self.special_value |= mask

            return
        
        #clear bit
        
        mask:int = 255 ^ (1 << bit_number)

        self.special_value &= mask

    def swap_nibbles(self):
        '''
            A simple utility to swap nibbles around using the XOR trick
        '''

        self.upper_nibble = self.lower_nibble ^ self.upper_nibble
        self.lower_nibble = self.upper_nibble ^ self.lower_nibble
        self.upper_nibble = self.lower_nibble ^ self.upper_nibble




    
