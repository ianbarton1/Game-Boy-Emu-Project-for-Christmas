from number.short_int import ShortInt


class MemoryBlock:
    def __init__(self,  data_in:bytes|None = None ,read_only:bool = False) -> None:
        self._read_only = read_only

        self.data_block:list[ShortInt] = []

        if data_in is not None:
            for byte in data_in:
                self.data_block.append(ShortInt(value=byte))
        else:
            self.data_block = [ShortInt() for _ in range(65536)]

    def read(self, address:int)->ShortInt:
        return self.data_block[address]

    def write(self, address:int, value:ShortInt)->None:
        if self._read_only:
            return
        #TODO: protect the value from illegal writes
        self.data_block[address].value = value