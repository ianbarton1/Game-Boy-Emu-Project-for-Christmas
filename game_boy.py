from dataclasses import dataclass
from enum import Enum
from pprint import pprint
import sys
from time import perf_counter, perf_counter_ns
from bus import Bus
from cpu import CPU
from gpu import GPU
from joypad import Joypad
from memory import MemoryBlock
from number.long_int import LongInt
from number.short_int import ShortInt
from rom import ROM

from time import sleep

import sdl2.ext as py_sdl
import sdl2 as py_sdl_native

from timer import Timer

from tqdm import tqdm

py_sdl.init()

@dataclass
class DebugString:
    text:str
    rect_coordinates:tuple[int]

class PreRenderedValueType(Enum):
    LONGINT = 16
    SHORTINT = 8
    FLAG = 1

@dataclass
class PreRenderedFontDefiniton:
    label:str
    value_type:PreRenderedValueType



class GameBoy:
    
    

    def __init__(self, rom_file:str, cpu_debug_print_counter:int|None = None, display_debug:bool = False) -> None:
        '''
            cpu_debug_print_counter when set, will starting printing information about the cpu after the internal instruction count
            exceeds the supplied value, if not set debug information will not be printed until an unimplemented instruction is
            encountered.

            Setting this to 0 will mean debug information is printed for every instruction (very slow)
        
        '''
        self.display:py_sdl.Window = py_sdl.Window(title=f"Game Boy Emulator {rom_file}", size=(1400,600))
        self.display.show()

        self.renderer:py_sdl.Renderer =py_sdl.Renderer(self.display, backend='opengl')

        self.ticks:int = 0

        self.rom:ROM = ROM(rom_file=rom_file)

        self.bus:Bus = Bus(rom=self.rom)
        self.cpu:CPU = CPU(bus=self.bus)
        self.gpu:GPU = GPU(bus=self.bus, renderer=self.renderer, debug_print_fn= self.draw_debug_info_fn)
        self.timer:Timer = Timer(bus=self.bus)
        self.joypad:Joypad = Joypad(bus=self.bus, show_keypresses=True, parent_gameboy = self)   
        
        self.print_debug_cpu_info:bool = cpu_debug_print_counter is not None
        self.debug_print_count = cpu_debug_print_counter

        self.this_second_start:float = perf_counter()
        self.this_second_end:float = 0

        self.debug_font = py_sdl.FontTTF('AnonymousPro-Regular.ttf', size=200, color=(255,255,255))

        self.running = True

        self.frame_pacing:float = 1 / 60

        self.this_frame_measurement_start:float = perf_counter()
        self.this_frame_measurement_end:float = 0
        self.frames_counted:int = 0

        self.text_surface = None
        self.draw_debug_info = display_debug              

    def render_label(self, label:str, value)->py_sdl_native.SDL_Texture:
        if isinstance(value, bool):
            temp_surface =self.debug_font.render_text(f"{label}{str(int(value))}")
            temp_texture = py_sdl_native.SDL_CreateTextureFromSurface(self.renderer.renderer, temp_surface)
        elif isinstance(value,LongInt):
            temp_surface = self.debug_font.render_text(f"{label}{hex(value.value)[2:].rjust(4,'0').upper()}")
            temp_texture = py_sdl_native.SDL_CreateTextureFromSurface(self.renderer.renderer, temp_surface)
        elif isinstance(value, ShortInt):
            temp_surface = self.debug_font.render_text(f"{label}{hex(value.value)[2:].rjust(2,'0').upper()}")
            temp_texture =  py_sdl_native.SDL_CreateTextureFromSurface(self.renderer.renderer, temp_surface)
        
        py_sdl_native.SDL_FreeSurface(temp_surface)
        return temp_texture
                        
    def draw_debug_info_fn(self):
        '''
            Display information about the current emulation on the screen 
        
        '''
        if not self.draw_debug_info:
            return
        DEBUG_X = 800
        DEBUG_Y = 0
        STRING_SIZE_X = 200
        STRING_SIZE_Y = 30
        PADDING = 5

        # if self.text_surface is None:

        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *0 + PADDING, DEBUG_Y + STRING_SIZE_Y * 0 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,'AF= ', self.cpu.register_AF)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *0 + PADDING, DEBUG_Y + STRING_SIZE_Y * 1 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"BC= ", self.cpu.register_BC)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *0 + PADDING, DEBUG_Y + STRING_SIZE_Y * 2 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"DE= ", self.cpu.register_DE)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *0 + PADDING, DEBUG_Y + STRING_SIZE_Y * 3 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"HL= ", self.cpu.register_HL)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *0 + PADDING, DEBUG_Y + STRING_SIZE_Y * 4 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"SP= ", self.cpu.register_SP)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *0 + PADDING, DEBUG_Y + STRING_SIZE_Y * 5 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"PC= ", self.cpu.register_PC)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *0 + PADDING, DEBUG_Y + STRING_SIZE_Y * 6 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"IME= ", self.cpu.ime_flag)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *0 + PADDING, DEBUG_Y + STRING_SIZE_Y * 7 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"IMA= ", True)

        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *1 + PADDING * 2, DEBUG_Y + STRING_SIZE_Y * 0 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"LCDC= ", self.gpu.lcd_control_register)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *1 + PADDING * 2, DEBUG_Y + STRING_SIZE_Y * 1 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"STAT= ", self.gpu.lcd_status_register)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *1 + PADDING * 2, DEBUG_Y + STRING_SIZE_Y * 2 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"LY= ", self.gpu.register_LY)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *1 + PADDING * 2, DEBUG_Y + STRING_SIZE_Y * 3 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"IE= ", self.cpu.interrupt_enable)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *1 + PADDING * 2, DEBUG_Y + STRING_SIZE_Y * 4 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"IF= ", self.cpu.interrupt_flag)




    def _draw_variable_on_screen(self, x_pos, y_pos, string_size_x, string_size_y,label:str, variable:bool|ShortInt|LongInt):
        temp_texture:py_sdl_native.SDL_Texture = self.render_label(label, value=variable)
    
        self.renderer.copy(temp_texture.contents,None, py_sdl_native.SDL_Rect(x_pos, y_pos, string_size_x, string_size_y))

        py_sdl_native.SDL_DestroyTexture(temp_texture)

        # self.renderer.copy()





        

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

        
        
        #speed limiting (where speed is above 100%)
        if self.gpu.frames_rendered == 1:
            
            self.gpu.frames_rendered = 0
            self.this_second_end = perf_counter()

            actual_frame_time = self.this_second_end - self.this_second_start

            current_draw_time = perf_counter() - self.this_second_start
            delay_period = max(0,self.frame_pacing - (current_draw_time))

            while delay_period >= 1/150:
                current_draw_time = perf_counter() - self.this_second_start
                delay_period = max(0,self.frame_pacing - (current_draw_time))

                sleep(delay_period)

            frame_draw_time = perf_counter() - self.this_second_start

            # print(f"This frame: {frame_draw_time}, Delay: {delay_period}, Total: {round(frame_draw_time + delay_period,4)}, Actual: {perf_counter() - self.this_second_end}")
            
            self.this_second_start = perf_counter()
            self.frames_counted += 1

        if self.frames_counted == 60:
            self.frames_counted = 0
            self.this_frame_measurement_end = perf_counter()
            print(f"60 frames rendered in {self.this_frame_measurement_end - self.this_frame_measurement_start}")
            self.this_frame_measurement_start = self.this_frame_measurement_end
            
        
                    