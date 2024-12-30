from number.short_int import ShortInt


class MemoryBlock:
    def __init__(self,  data_in:bytes|None = None ,read_only:bool = False, size = 65536) -> None:
        self._read_only = read_only

        self.data_block:list[ShortInt] = []

        if data_in is not None:
            for byte in data_in:
                self.data_block.append(ShortInt(value=byte))
        else:
            self.data_block = [ShortInt() for _ in range(size)]

    def read(self, address:int)->ShortInt:
        return self.data_block[address]

    def write(self, address:int, value:int)->None:
        if self._read_only:
            return
        #TODO: protect the value from illegal writes

        if not isinstance(value, int):
            raise TypeError('write expected int for value argument, init_shortint')

        self.data_block[address].value = value

    def init_shortint(self, address:int, value:ShortInt):
        if self._read_only:
            return
        #TODO: protect the value from illegal writes

        if not isinstance(value, ShortInt):
            raise TypeError('write expected Shortint for value argument, init_shortint')

        self.data_block[address] = value