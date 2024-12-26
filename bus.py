from memory import MemoryBlock
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


def read_byte_at_pc(cpu_obj)->ShortInt:
    '''
        Reads a single byte from the bus at the program counter,
        increment the program counter and returns the byte
    '''

    value = cpu_obj.bus.read(cpu_obj.program_counter)
    cpu_obj.program_counter += 1

    return value

class Bus():
    rom:ROM = ROM(rom_file="drmario.gb")
    ram:MemoryBlock = MemoryBlock()


    def _resolve_address(self, address:int)->tuple[int, MemoryBlock]:
        if address >= 0x0 and address <= 0x7FFF:
            return 0x0000, self.rom
        elif address >= 0x4000 and address <= 0x9fff:
            print("read vram")
            return 0x4000, None
        elif address >= 0xA000 and address <= 0xBFFF:
            print("read external ram")
            return 0xA000, None
        elif address >= 0xC000 and address <= 0xDFFF:
            return 0xC000, self.ram
        elif address >= 0xE000 and address <= 0xFDFF:
            return 0xE000, self.ram
        elif address >= 0xFE00 and address <= 0xFE9F:
            print("OAM not implemented")
            return 0xFE00, None
        elif address >= 0xFEA0 and address <= 0xFEFF:
            print("Not usable")
            return 0xFEA0, None
        elif address >= 0xFF00 and address <= 0xFF7F:
            print("I/O Register")
            return 0xFF00, None
        elif address >= 0xFF80 and address <= 0xFFFE:
            print("High RAM (HRAM)")
            return 0xFF80, None
        elif address == 0xFFFF:
            print("Interrupt enable register (IE)")
            return 0xFFFF, None

    def write(self, address:int, value:ShortInt)->None:
        offset, memory_block = self._resolve_address(address)
        print(hex(address), hex(offset))
        memory_block.write(address - offset, value)


    def read(self, address:int) -> ShortInt:
        offset, memory_block = self._resolve_address(address)
            
        return memory_block.read(address - offset)