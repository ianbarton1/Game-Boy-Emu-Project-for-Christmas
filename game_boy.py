from bus import Bus
from cpu import CPU
from gpu import GPU
from memory import MemoryBlock
from rom import ROM


class GameBoy:
    bus:Bus = Bus()
    cpu:CPU = CPU(bus=bus)
    gpu:GPU = GPU(bus=bus)
    
    

    def __init__(self, cpu_debug_print_counter:int|None = None) -> None:
        '''
            cpu_debug_print_counter when set, will starting printing information about the cpu after the internal instruction count
            exceeds the supplied value, if not set debug information will not be printed until an unimplemented instruction is
            encountered.

            Setting this to 0 will mean debug information is printed for every instruction (very slow)
        
        '''
        self.ticks:int = 0

        
        self.print_debug_cpu_info:bool = cpu_debug_print_counter is not None
        self.debug_print_count = cpu_debug_print_counter




    def tick(self):
        self.ticks += 1

        self.cpu.tick()
        self.gpu.tick()


        if self.print_debug_cpu_info and self.cpu.instruction_count > self.debug_print_count and self.cpu.last_tick_was_active:
            print(self.cpu)

        # if self.cpu.last_tick_was_active or self.gpu.last_tick_was_active:
        #     print(self.cpu)
        #     print(self.gpu)
        
                    