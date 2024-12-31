import ctypes
from enum import Enum
from random import randint
import sys
from time import perf_counter
from bus import Bus
from number.short_int import ShortInt

import sdl2.ext as py_sdl
import sdl2 as py_sdl_native

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

    draw_counter:int = 0
    draw_frequency:int = 1
    tile_update:int = 60

    def __init__(self, bus:Bus, renderer:py_sdl.Renderer):
        self.last_tick_was_active:bool = True

        self.register_LY:ShortInt = bus.read(0xFF44)
        self.renderer = renderer
        self.bus:Bus = bus

        self.tile_textures:list[py_sdl_native.SDL_Texture] = [py_sdl_native.SDL_CreateTexture(self.renderer.renderer, py_sdl_native.SDL_PIXELFORMAT_RGB24, py_sdl_native.SDL_TEXTUREACCESS_STREAMING, 16, 16) for _ in range(400)]
        self.rectangles:py_sdl_native.SDL_Rect = []

        for tile_id in range(384):
            self.rectangles.append(py_sdl_native.SDL_Rect(400 + (tile_id % 16) * 16, 100 + ((tile_id // 16) * 16), 16, 16))
        
        self.update_tiles()

    def update_tiles(self):
        address_reads = 0
        for tile_id in range(384):
            pixels = (ctypes.c_ubyte * (16*16 * 3))()
            for line_idx in range(8):
                
                address = 0x8000 + (tile_id * 16) + (line_idx * 2)
                byte_1 = self.bus.read(address)
                byte_2 = self.bus.read(address+1)
                address_reads += 2
                
                

                for pixel_idx in range(8):
                    colour_index = (byte_2.get_bit(7 - pixel_idx) << 1) + byte_1.get_bit(7 - pixel_idx)
                    greyscale_value = int((3 - colour_index) / 3 * 85)

                    pixels[96 * line_idx + pixel_idx * 6 + 0] = greyscale_value
                    pixels[96 * line_idx + pixel_idx * 6 + 1] = greyscale_value
                    pixels[96 * line_idx + pixel_idx * 6 + 2] = greyscale_value
                    pixels[96 * line_idx + pixel_idx * 6 + 3] = greyscale_value
                    pixels[96 * line_idx + pixel_idx * 6 + 4] = greyscale_value
                    pixels[96 * line_idx + pixel_idx * 6 + 5] = greyscale_value

                    pixels[96 * line_idx + pixel_idx * 6 + 48] = greyscale_value
                    pixels[96 * line_idx + pixel_idx * 6 + 49] = greyscale_value
                    pixels[96 * line_idx + pixel_idx * 6 + 50] = greyscale_value
                    pixels[96 * line_idx + pixel_idx * 6 + 51] = greyscale_value
                    pixels[96 * line_idx + pixel_idx * 6 + 52] = greyscale_value
                    pixels[96 * line_idx + pixel_idx * 6 + 53] = greyscale_value

                
                

                # for pixel_idx in range(8):
                #     colour_index = (byte_2.get_bit(7 - pixel_idx) << 1) + byte_1.get_bit(7 - pixel_idx)
                #     greyscale_value = int((3 - colour_index) / 3 * 85)

                #     start_pixel_offset = line_idx * 96 + pixel_idx * 6

                #     for byte_index in range(3):
                #         for i in range(6):
                #             pixels[start_pixel_offset + i + byte_index * 4] = greyscale_value
                #             pixels[start_pixel_offset  + 48 + i + byte_index * 4] = greyscale_value

                #             print(start_pixel_offset + i + byte_index * 3,start_pixel_offset  + 48 + i + byte_index * 3)
                            
                    
            py_sdl_native.SDL_UpdateTexture(self.tile_textures[tile_id], None, pixels, 48)
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
                        self.renderer.clear()
                        
                        self.draw_counter += 1

                        

                        if self.draw_counter >= self.draw_frequency:

                            self.draw_counter = 0
                            self.renderer.fill((0, 0, 160*2, 144*2), py_sdl.Color(255,255,255,0))

                            #draw tilemap rendering?

                            start_time = perf_counter()
                            address_reads = 0

                            
                            for tile_id in range(384):
                                self.renderer.copy(self.tile_textures[tile_id].contents, None, self.rectangles[tile_id])


                            # for colour_index in range(4):
                            #     if len(coloured_rectangles[colour_index]) > 0:
                            #         self.renderer.draw_rect(coloured_rectangles[colour_index], colour_pallette[colour_index])

                        
                            self.update_tiles()
                            self.renderer.present()

                            end_time = perf_counter()
                            
                            print(f"Tilemap generation: {end_time - start_time}, address reads {address_reads}")
                            
                            



                        events = py_sdl.get_events()

                        for e in events:
                            if e.type == py_sdl_native.SDL_QUIT:
                                sys.exit()
                                
                            if e.type == py_sdl_native.SDL_KEYDOWN:
                                if e.key.keysym.sym == py_sdl_native.SDLK_ESCAPE:
                                    sys.exit()
                                    
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

        
        