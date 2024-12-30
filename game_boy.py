from bus import Bus
from cpu import CPU
from gpu import GPU
from memory import MemoryBlock
from rom import ROM


class GameBoy:
    bus:Bus = Bus()
    cpu:CPU = CPU(bus=bus)
    gpu:GPU = GPU(bus=bus)
    
    

    def __init__(self) -> None:
        self.ticks:int = 0




    def tick(self):
        self.ticks += 1

        self.cpu.tick()
        self.gpu.tick()

        # if self.cpu.last_tick_was_active or self.gpu.last_tick_was_active:
        #     print(self.cpu)
        #     print(self.gpu)
        
                    