from enum import Enum
from bus import Bus
from number.short_int import ShortInt

class GPUState(Enum):
    OAMSearch = 80
    PixelTransfer = 172
    HBlank = 204
    VBlank = 456


class GPU:
    clock_wait:int = 80
    state:GPUState = GPUState.OAMSearch
    prev_state:GPUState = GPUState.VBlank
    x_position:int = 0
    

    def __init__(self, bus:Bus):
        self.last_tick_was_active:bool = True

        self.register_LY:ShortInt = bus.read(0xFF44)

    def __repr__(self)->str:
        return f"{self.state}, LY:{hex(self.register_LY.value)}"
    
    def tick(self):
        '''Tick the GPU(PPU) one tick forward, this occurs at the same time as the CPU.'''

        #transition between different states (transitions always happen at clock_wait = 0)
        
        if self.clock_wait > 0:
            self.clock_wait -= 1
            self.last_tick_was_active = False
            return
        
        self.last_tick_was_active = True

        
        
        match self.state:
            case GPUState.OAMSearch:
                if self.clock_wait == 0:
                    self.state = GPUState.PixelTransfer
                
            case GPUState.PixelTransfer:

                if self.clock_wait == 0:
                    self.state = GPUState.HBlank
                    self.x_position = 0
                else:
                    self.x_position = 160 - self.clock_wait


            case GPUState.HBlank:
                if self.clock_wait == 0:
                    self.register_LY.value += 1

                    if self.register_LY.value == 144:
                        self.state = GPUState.VBlank
                    else:
                        self.state = GPUState.OAMSearch
                    
            case GPUState.VBlank:
                if self.clock_wait == 0:
                    self.register_LY.value += 1
                    self.prev_state = GPUState.OAMSearch
                    if self.register_LY.value == 153:
                        self.register_LY.value = 0
                        self.state = GPUState.OAMSearch

        if self.prev_state != self.state:
            self.clock_wait = self.state.value
            self.prev_state = self.state

        
        