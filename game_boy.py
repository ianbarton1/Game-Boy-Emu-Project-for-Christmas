from pprint import pprint
import sys
from time import perf_counter, perf_counter_ns
from bus import Bus
from cpu import CPU
from gpu import GPU
from joypad import Joypad
from memory import MemoryBlock
from rom import ROM


import sdl2.ext as py_sdl
import sdl2 as py_sdl_native

from timer import Timer

py_sdl.init()




class GameBoy:
    
    

    def __init__(self, rom_file:str, cpu_debug_print_counter:int|None = None, ) -> None:
        '''
            cpu_debug_print_counter when set, will starting printing information about the cpu after the internal instruction count
            exceeds the supplied value, if not set debug information will not be printed until an unimplemented instruction is
            encountered.

            Setting this to 0 will mean debug information is printed for every instruction (very slow)
        
        '''
        self.display:py_sdl.Window = py_sdl.Window(title=f"Game Boy Emulator {rom_file}", size=(1200,600))
        self.display.show()

        self.renderer:py_sdl.Renderer =py_sdl.Renderer(self.display, backend='direct3d')

        self.ticks:int = 0

        self.rom:ROM = ROM(rom_file=rom_file)

        self.bus:Bus = Bus(rom=self.rom)
        self.cpu:CPU = CPU(bus=self.bus)
        self.gpu:GPU = GPU(bus=self.bus, renderer=self.renderer)
        self.timer:Timer = Timer(bus=self.bus)
        self.joypad:Joypad = Joypad(bus=self.bus, show_keypresses=True, parent_gameboy = self)   
        
        self.print_debug_cpu_info:bool = cpu_debug_print_counter is not None
        self.debug_print_count = cpu_debug_print_counter

        self.this_second_start:float = perf_counter()
        self.this_second_end:float = 0

        self.running = True

        

        

    def play(self):
        while self.running:
            self.tick()

        self.renderer.destroy()
        self.display.close()

    def finish(self):
        self.running = False

        
    
    def tick(self):
        self.ticks += 1
        UPDATE_RATE = 4

        if not self.joypad.debug_pause:
            self.cpu.tick(tick_amount=UPDATE_RATE)

            if self.cpu.cpu_is_stopped:
                self.gpu.ppu_is_stopped = True


            self.gpu.tick(clock_increment=UPDATE_RATE)
            self.timer.tick(tick_rate=UPDATE_RATE)
        
        if self.joypad.debug_print:
            print(self.cpu)
            self.joypad.debug_print = False

        self.joypad.tick()

        if self.print_debug_cpu_info and self.cpu.instruction_count > self.debug_print_count and self.cpu.last_tick_was_active:
            print(self.cpu)
            # print(self.timer.divider_register.high_byte.value)

        if self.gpu.frames_rendered == 60:
            self.gpu.frames_rendered = 0
            self.this_second_end = perf_counter()
            print(f"60 frames rendered in {self.this_second_end - self.this_second_start}")
            self.this_second_start = self.this_second_end

        


        #check joypad
        
                    
        
                    