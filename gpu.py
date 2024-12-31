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
    draw_frequency:int = 30

    py_sdl_native.SDL_Texture()

    tile_textures:list[py_sdl_native.SDL_Texture] = [py_sdl_native.SDL_CreateTexture() for _ in range(400)]
    
    

    def __init__(self, bus:Bus, renderer:py_sdl.Renderer):
        self.last_tick_was_active:bool = True

        self.register_LY:ShortInt = bus.read(0xFF44)
        self.renderer = renderer
        self.bus:Bus = bus

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

                        rectangles = []

                        # coloured_rectangles = [[],[],[],[]]
                        # colour_pallette = [
                        #                     py_sdl_native.SDL_Colour(255,255,255,0),
                        #                     py_sdl_native.SDL_Colour(170,170,170,0),
                        #                     py_sdl_native.SDL_Colour(85,85,85,0),
                        #                     py_sdl_native.SDL_Colour(0,0,0,0)
                        #                 ]

                        if self.draw_counter >= self.draw_frequency:

                            self.draw_counter = 0
                            self.renderer.fill((0, 0, 160*2, 144*2), py_sdl.Color(255,255,255,0))

                            #draw tilemap rendering?

                            start_time = perf_counter()
                            address_reads = 0

                            for tile_id in range(384):

                                rectangles.append(py_sdl_native.SDL_Rect(400 + (tile_id % 16) * 16, 100 + line_idx * 2 + ((tile_id // 16) * 16), 16, 16))
                                for line_idx in range(8):

                                    address = 0x8000 + (tile_id * 16) + (line_idx * 2)
                                    byte_1 = self.bus.read(address)
                                    byte_2 = self.bus.read(address+1)
                                    address_reads += 2
                                    

                                    # for pixel_idx in range(8):
                                    #     colour_index = (byte_2.get_bit(7 - pixel_idx) << 1) + byte_1.get_bit(7 - pixel_idx)
                                    #     # self.renderer.fill((400 + (tile_id % 16) * 16 + pixel_idx * 2, 100 + line_idx * 2 + ((tile_id // 16) * 16), 2, 2), py_sdl.Color(colour_value,colour_value,colour_value,0))
                                    #     coloured_rectangles[colour_index].append(py_sdl_native.SDL_Rect(400 + (tile_id % 16) * 16 + pixel_idx * 2, 100 + line_idx * 2 + ((tile_id // 16) * 16), 2, 2))


                            # for colour_index in range(4):
                            #     if len(coloured_rectangles[colour_index]) > 0:
                            #         self.renderer.draw_rect(coloured_rectangles[colour_index], colour_pallette[colour_index])



                            end_time = perf_counter()

                            print(f"Tilemap generation: {end_time - start_time}, address reads {address_reads}")
                            self.renderer.present()



                        # events = py_sdl.get_events()

                        # for e in events:
                        #     if e.type == py_sdl_native.SDL_QUIT:
                        #         sys.exit()
                                
                        #     if e.type == py_sdl_native.SDL_KEYDOWN:
                        #         if e.key.keysym.sym == py_sdl_native.SDLK_ESCAPE:
                        #             sys.exit()
                                    
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

        
        