from bus import Bus
from cpu import CPU
from memory import MemoryBlock
from rom import ROM


class GameBoy:
    bus:Bus = Bus()
    cpu:CPU = CPU(bus=bus)
    
    

    def __init__(self) -> None:
        self.ticks:int = 0


    def tick(self):
        self.ticks += 1
        self.cpu.tick()