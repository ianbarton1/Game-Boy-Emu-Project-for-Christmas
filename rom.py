from memory import MemoryBlock
from number.short_int import ShortInt


class ROM:
    def __init__(self, rom_file:str) -> None:
        with open(rom_file, mode="rb") as rom_file_handle:
            rom_bytes:bytes = rom_file_handle.read()


        self.memory_block:MemoryBlock = MemoryBlock(read_only= True, data_in = rom_bytes)

    def read(self,address)->ShortInt:
        return self.memory_block.read(address)

    def write(self, address)->None:
        self.memory_block.write(address)
