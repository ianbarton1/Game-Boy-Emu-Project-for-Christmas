from time import sleep
from memory import MemoryBlock
from number.long_int import LongInt
from number.short_int import ShortInt
from rom import ROM

def get_immediate_address_value(cpu_obj)->ShortInt:
    '''
        This helper function will perform the following actions:
        
        1.) Read two bytes from the current program counter
        2.) increment the program counter by 2
        3.) Read the byte specified in the address read in the first step
    
    '''

    address = LongInt()

    address.low_byte = cpu_obj.bus.read(cpu_obj.program_counter)
    address.high_byte = cpu_obj.bus.read(cpu_obj.program_counter+ 1)

    cpu_obj.program_counter += 2

    return cpu_obj.bus.read(address.value)


def read_byte_from_address_from_register(cpu_obj, long_register:LongInt)->ShortInt:
    return cpu_obj.bus.read(long_register.value)


def read_byte_at_pc(cpu_obj)->ShortInt:
    '''
        Reads a single byte from the bus at the program counter,
        increment the program counter and returns the byte
    '''

    value = cpu_obj.bus.read(cpu_obj.program_counter)
    cpu_obj.program_counter += 1

    return value

class Bus():
    

    def __init__(self, rom:ROM):
        self.rom:ROM = rom
        self.ram:MemoryBlock = MemoryBlock()
        self.interrupt_enable_register:MemoryBlock = MemoryBlock(size = 1)
        self.io_register:MemoryBlock = MemoryBlock(size = 128)
        self.high_ram:MemoryBlock = MemoryBlock(size = 127)
        self.dummy_external_ram:MemoryBlock = MemoryBlock(size= 8192, read_only=True)

        self.vram:MemoryBlock = MemoryBlock(size = 24577)

        self.ro_block:MemoryBlock = MemoryBlock(size = 96, read_only=True)
        self.oam_memory:MemoryBlock = MemoryBlock(size = 100000)

        self.last_read_address:int = 0x0000


    def _resolve_address(self, address:int)->tuple[int, MemoryBlock]:
        if address >= 0x0 and address <= 0x7FFF:
            return 0x0000, self.rom
        elif address >= 0x4000 and address <= 0x9fff:
            # print("read/write vram")
            return 0x4000, self.vram
        elif address >= 0xA000 and address <= 0xBFFF:
            # print("read external ram")
            return 0xA000, self.dummy_external_ram
        elif address >= 0xC000 and address <= 0xDFFF:
            return 0xC000, self.ram
        elif address >= 0xE000 and address <= 0xFDFF:
            return 0xE000, self.ram
        elif address >= 0xFE00 and address <= 0xFE9F:
            return 0xFE00, self.oam_memory
        elif address >= 0xFEA0 and address <= 0xFEFF:
            # print("Not usable")
            return 0xFEA0, self.ro_block
        elif address >= 0xFF00 and address <= 0xFF7F:
            # print("I/O Register")
            return 0xFF00, self.io_register
        elif address >= 0xFF80 and address <= 0xFFFE:
            # print("High RAM (HRAM)")
            return 0xFF80, self.high_ram
        elif address == 0xFFFF:
            # print("Interrupt enable register (IE)")
            return 0xFFFF, self.interrupt_enable_register
        if address > 0xFFFF or address < 0x0000:
            print("Illegal address found :", hex(address))
            raise ValueError("Address is out of bounds")

    def write(self, address:int, value:int)->None:
        offset, memory_block = self._resolve_address(address)

        if not isinstance(value, int):
            raise TypeError('write function expected int, use init')
        memory_block.write(address - offset, value)

    def init_shortint(self, address:int, value:ShortInt):
        offset, memory_block = self._resolve_address(address)

        if not isinstance(value, ShortInt):
            raise TypeError('write function expected int, use init')
        memory_block.init_shortint(address - offset, value)


    def read(self, address:int) -> ShortInt:
        offset, memory_block = self._resolve_address(address)

        self.last_read_address = address
            
        return memory_block.read(address - offset)