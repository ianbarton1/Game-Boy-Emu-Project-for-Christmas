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

WINDOW_SIZE_X:int = 1400
WINDOW_SIZE_Y:int = 600

class GameBoy:
    
    

    def __init__(self, rom_file:str, cpu_debug_print_counter:int|None = None, display_debug:bool = False) -> None:
        '''
            cpu_debug_print_counter when set, will starting printing information about the cpu after the internal instruction count
            exceeds the supplied value, if not set debug information will not be printed until an unimplemented instruction is
            encountered.

            Setting this to 0 will mean debug information is printed for every instruction (very slow)
        
        '''
        

        self.display:py_sdl.Window = py_sdl.Window(title=f"Game Boy Emulator {rom_file}", size=(WINDOW_SIZE_X,WINDOW_SIZE_Y))
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

        self.debug_font = py_sdl.FontTTF('AnonymousPro-Regular.ttf', size=100, color=(255,255,255))
        self.active_font = py_sdl.FontTTF('AnonymousPro-Regular.ttf', size=100, color=(64,255,64))

        self.running = True

        self.frame_pacing:float = 1 / 60

        self.this_frame_measurement_start:float = perf_counter()
        self.this_frame_measurement_end:float = 0
        self.frames_counted:int = 0
        self.frame_rate:int = 0

        self.text_surface = None
        self.draw_debug_info = display_debug              

    def render_label(self, label:str, value, font:py_sdl.FontTTF)->py_sdl_native.SDL_Texture:
        if isinstance(value, bool):
            temp_surface =font.render_text(f"{label}{str(int(value))}")
        elif isinstance(value,LongInt):
            temp_surface = font.render_text(f"{label}{hex(value.value)[2:].rjust(4,'0').upper()}")
        elif isinstance(value, ShortInt):
            temp_surface = font.render_text(f"{label}{hex(value.value)[2:].rjust(2,'0').upper()}")
        elif isinstance(value, int):
            temp_surface = font.render_text(f"{label}{str(value).rjust(3,'0').upper()}")
        elif isinstance(value,str):
            temp_surface = font.render_text(f"{label}{value}")
            
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

        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *0 + PADDING, DEBUG_Y + STRING_SIZE_Y * 0 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,'AF= ', self.cpu.register_AF, font=self.debug_font)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *0 + PADDING, DEBUG_Y + STRING_SIZE_Y * 1 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"BC= ", self.cpu.register_BC, font=self.debug_font)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *0 + PADDING, DEBUG_Y + STRING_SIZE_Y * 2 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"DE= ", self.cpu.register_DE, font=self.debug_font)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *0 + PADDING, DEBUG_Y + STRING_SIZE_Y * 3 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"HL= ", self.cpu.register_HL, font=self.debug_font)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *0 + PADDING, DEBUG_Y + STRING_SIZE_Y * 4 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"SP= ", self.cpu.register_SP, font=self.debug_font)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *0 + PADDING, DEBUG_Y + STRING_SIZE_Y * 5 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"PC= ", LongInt(self.cpu.last_fetch_pc), font=self.debug_font)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *0 + PADDING, DEBUG_Y + STRING_SIZE_Y * 6 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"IME= ", self.cpu.ime_flag, font=self.debug_font)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *0 + PADDING, DEBUG_Y + STRING_SIZE_Y * 7 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"IMA= ", True, font=self.debug_font)

        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *1 + PADDING * 2, DEBUG_Y + STRING_SIZE_Y * 0 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"LCDC= ", self.gpu.lcd_control_register, font=self.debug_font)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *1 + PADDING * 2, DEBUG_Y + STRING_SIZE_Y * 1 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"STAT= ", self.gpu.lcd_status_register, font=self.debug_font)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *1 + PADDING * 2, DEBUG_Y + STRING_SIZE_Y * 2 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"LY= ", self.gpu.register_LY, font=self.debug_font)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *1 + PADDING * 2, DEBUG_Y + STRING_SIZE_Y * 3 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"IE= ", self.cpu.interrupt_enable, font=self.debug_font)
        self._draw_variable_on_screen(DEBUG_X + STRING_SIZE_X *1 + PADDING * 2, DEBUG_Y + STRING_SIZE_Y * 4 + PADDING, STRING_SIZE_X, STRING_SIZE_Y,"IF= ", self.cpu.interrupt_flag, font=self.debug_font)

        self._draw_variable_on_screen(WINDOW_SIZE_X-60,0,string_size_x=60,string_size_y=40,label="", variable=self.frame_rate, font=self.debug_font)

        active_address = max(self.cpu.last_fetch_pc - 10, -1)

        decoded_instruction_count =  0

        while active_address <= self.cpu.last_fetch_pc + 40 and decoded_instruction_count <= 10:
            active_address += 1
            if active_address not in self.cpu.instruction_list:
                continue
            
            instruction_bytes = ""
            for byte in self.cpu.instruction_list[active_address][1]:
                instruction_bytes += hex(byte)[2:].rjust(2,"0").upper()+" "

            instruction_text = f"{hex(active_address)}:{instruction_bytes}:"+self.cpu.instruction_list[active_address][0]
            
            self._draw_variable_on_screen(DEBUG_X,DEBUG_Y + STRING_SIZE_Y*(8+ decoded_instruction_count) + PADDING,len(instruction_text)*10,STRING_SIZE_Y,"",instruction_text, font=self.debug_font if active_address != self.cpu.last_fetch_pc else self.active_font)

            decoded_instruction_count += 1
            
            


    def _draw_variable_on_screen(self, x_pos, y_pos, string_size_x, string_size_y,label:str, variable:bool|ShortInt|LongInt, font:py_sdl.FontTTF):
        temp_texture:py_sdl_native.SDL_Texture = self.render_label(label, value=variable, font=font)
    
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
        elif self.joypad.step_instruction:
            print("Stepped to next instruction")
            self.joypad.step_instruction = False

            current_instruction = self.cpu.last_fetch_pc
            ticks_added = 0

            while self.cpu.last_fetch_pc == current_instruction and not self.cpu.cpu_is_halted and not self.cpu.cpu_is_stopped:
                ticks_added +- 1
                self.cpu.tick(tick_amount=1)
            
            self.gpu.frames_rendered = 0
            while self.gpu.frames_rendered == 0:
                self.gpu.tick()
            self.gpu.frames_rendered = 0
        
            for _ in range(ticks_added):

                self.timer.tick()
            
            print(hex(current_instruction), hex(self.cpu.last_fetch_pc))
        
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

            self.frame_rate = round(60 / (self.this_frame_measurement_end - self.this_frame_measurement_start))
            self.this_frame_measurement_start = self.this_frame_measurement_end
            
        
                    