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
    tile_update:int = 1

    ppu_is_stopped:bool = False

    def update_tile_state(self, tile_index:int):
        # print(f"TILE {tile_index} marked as needing update")
        self.tile_needs_update[tile_index] = True

    def __init__(self, bus:Bus, renderer:py_sdl.Renderer):
        self.last_tick_was_active:bool = True

        TILEMAP_X:int = 600
        TILEMAP_Y:int = 0

        self.register_LY:ShortInt = bus.read(0xFF44)
        self.lcd_control_register:ShortInt = bus.read(0xFF40)
        self.lcd_status_register:ShortInt = bus.read(0xFF41)
        self.ie_register:ShortInt = bus.read(0xFF0F)

        self.renderer = renderer
        self.bus:Bus = bus

        for address in range(0x8000, 0x9800, 0x1):
            self.bus.read(address).add_write_viewer(self.update_tile_state)
            self.bus.read(address).add_write_token((address - 0x8000) // 16)

        self.tile_textures:list[py_sdl_native.SDL_Texture] = [py_sdl_native.SDL_CreateTexture(self.renderer.renderer, py_sdl_native.SDL_PIXELFORMAT_RGB24, py_sdl_native.SDL_TEXTUREACCESS_STREAMING, 16, 16) for _ in range(400)]
        self.tile_needs_update:list[bool] = [False for _ in range(400)]
        
        self.rectangles:py_sdl_native.SDL_Rect = []

        self.clock_update_rate = 4

        self.frames_rendered:int = 0

        for tile_id in range(384):
            
            self.rectangles.append(py_sdl_native.SDL_Rect(TILEMAP_X + (tile_id % 16) * 16, TILEMAP_Y + ((tile_id // 16) * 16), 16, 16))
        
        self.update_tiles()

    def update_tiles(self):
        address_reads = 0
        for tile_id in range(384):
            if not self.tile_needs_update[tile_id]:
                continue

            self.tile_needs_update[tile_id] = False
            pixels = (ctypes.c_ubyte * (16*16 * 3))()
            for line_idx in range(8):
                
                address = 0x8000 + (tile_id * 16) + (line_idx * 2)
                byte_1 = self.bus.read(address)
                byte_2 = self.bus.read(address+1)
                address_reads += 2
                
                for pixel_idx in range(8):
                    colour_index = (byte_2.get_bit(7 - pixel_idx) << 1) + byte_1.get_bit(7 - pixel_idx)
                    greyscale_value = int((3 - colour_index) / 3 * 255)

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
    
    def tick(self, clock_increment:int = 1):
        '''Tick the GPU(PPU) one tick forward, this occurs at the same time as the CPU.'''

        #transition between different states (transitions always happen at clock_wait = 0)
        if self.ppu_is_stopped:
            return


        if self.clock_wait > 0:
            
            self.clock_wait -= clock_increment
            self.last_tick_was_active = False
            return
        
        self.last_tick_was_active = True

        
        
        match self.state:
            case GPUState.OAMSearch:
                self.lcd_status_register.write_bit(bit_number=0, bit=False)
                self.lcd_status_register.write_bit(bit_number=1, bit=False)
                
                if self.clock_wait == 0:
                    self.state = GPUState.PixelTransfer
                    
                
            case GPUState.PixelTransfer:

                if self.clock_wait == 0:
                    self.state = GPUState.HBlank
                    if self.lcd_status_register.get_bit(bit_number=3):
                            self.trigger_stat_interrupt()
                    self.x_position = 0
                else:
                    self.x_position = 160 - self.clock_wait


            case GPUState.HBlank:
                if self.clock_wait == 0:
                    self.register_LY.value += 1

                    if self.register_LY.value == 144:
                        self.renderer.clear()
                        self.renderer.fill((0, 0, 160*2, 144*2), py_sdl.Color(255,255,255,0))
                        self.draw_counter += 1
                        
                        if self.draw_counter >= self.tile_update:
                            self.draw_counter = 0
                            self.update_tiles()

                        self.draw_tilemap()
                        self.draw_background()
                        self.draw_sprites()
                        
                        
                        self.renderer.present() 
                        

                        
                                    
                        self.state = GPUState.VBlank
                        
                        
                        if self.lcd_status_register.get_bit(bit_number=4):
                            self.trigger_stat_interrupt()
                        #trigger v-blank interrupt?
                        self.ie_register.write_bit(bit_number=0, bit=True)

                        # print("GPU", id(self.bus.read(0xFF0F)),id(self.bus.read(0xFFFF)))
                        # print(f"V-blank {self.bus.read(0xFF0F).get_bit(bit_number=0)} {self.bus.read(0xFFFF).get_bit(bit_number=0)}")
                    else:
                        self.state = GPUState.OAMSearch
                        if self.lcd_status_register.get_bit(bit_number=5):
                            self.trigger_stat_interrupt()
                    
            case GPUState.VBlank:
                if self.clock_wait == 0:
                    self.register_LY.value += 1
                    self.prev_state = GPUState.OAMSearch
                    if self.register_LY.value == 153:
                        self.register_LY.value = 0
                        self.state = GPUState.OAMSearch

                        self.frames_rendered += 1

                        if self.lcd_status_register.get_bit(bit_number=5):
                            self.trigger_stat_interrupt()

        if self.prev_state != self.state:
            match self.state:
                case GPUState.HBlank:
                    self.lcd_status_register.write_bit(bit_number=0, bit=False)
                    self.lcd_status_register.write_bit(bit_number=1, bit=False)
                case GPUState.VBlank:
                    self.lcd_status_register.write_bit(bit_number=0, bit=True)
                    self.lcd_status_register.write_bit(bit_number=1, bit=False)
                case GPUState.OAMSearch:
                    self.lcd_status_register.write_bit(bit_number=0, bit=False)
                    self.lcd_status_register.write_bit(bit_number=1, bit=True)
                case GPUState.PixelTransfer:
                    self.lcd_status_register.write_bit(bit_number=0, bit=True)
                    self.lcd_status_register.write_bit(bit_number=1, bit=True)



            self.clock_wait = self.state.value
            self.prev_state = self.state

    def draw_tilemap(self):
        
            

        #draw tilemap rendering?

        start_time = perf_counter()
        address_reads = 0

                        
        for tile_id in range(384):
            self.renderer.copy(self.tile_textures[tile_id].contents, None, self.rectangles[tile_id])


                        # for colour_index in range(4):
                        #     if len(coloured_rectangles[colour_index]) > 0:
                        #         self.renderer.draw_rect(coloured_rectangles[colour_index], colour_pallette[colour_index])                        
        end_time = perf_counter()
                        
                        # print(f"Tilemap generation: {end_time - start_time}, address reads {address_reads}")

        # print(self.bus.read(0xFF45), self.lcd_status_register.get_bit(bit_number=6),self.lcd_status_register.get_bit(bit_number=5),self.lcd_status_register.get_bit(bit_number=4),self.lcd_status_register.get_bit(bit_number=3))
                            
        

    def draw_background(self):
        background_map = (0x9C00,0xA000) if self.lcd_control_register.get_bit(bit_number=3) else (0x9800, 0x9C00)
        use_normal_tile_addressing = self.lcd_control_register.get_bit(bit_number=4)

        background_window_layer_enabled = self.lcd_control_register.get_bit(bit_number=0)

        if background_window_layer_enabled:
            for tile_index, tile_address in enumerate(range(background_map[0], background_map[1], 0x1)):
                if use_normal_tile_addressing:
                    tile_id = self.bus.read(tile_address).value
                else:
                    tile_id = 256 + self.bus.read(tile_address).signed_value
                                    
                self.renderer.copy(self.tile_textures[tile_id].contents, None, py_sdl_native.SDL_Rect((tile_index % 32) * 16, ((tile_index // 32) * 16), 16, 16))

    def draw_sprites(self):
        sprites_enabled = self.lcd_control_register.get_bit(bit_number=1)
        # print("SPRITES_ENABLED", sprites_enabled)
        if sprites_enabled:
            for sprite_index, sprite_address in enumerate(range(0xFE00,0xFEA0,0x4)):
                y_position = self.bus.read(sprite_address).value - 16
                x_position = self.bus.read(sprite_address + 1).value - 8
                tile_id = self.bus.read(sprite_address+ 2).value
                sprite_flags = self.bus.read(sprite_address + 3).value

                # print(tile_id,x_position, y_position)

                '''Bit 7    OBJ-to-BG Priority
                                    0 = Sprite is always rendered above background
                                    1 = Background colors 1-3 overlay sprite, sprite is still rendered above color 0
                                    Bit 6    Y-Flip
                                            If set to 1 the sprite is flipped vertically, otherwise rendered as normal
                                    Bit 5    X-Flip
                                            If set to 1 the sprite is flipped horizontally, otherwise rendered as normal
                                    Bit 4    Palette Number
                                            If set to 0, the OBP0 register is used as the palette, otherwise OBP1
                                    Bit 3-0  CGB-Only flags'''
                                    # print(sprite_index, hex(sprite_address), x_position, y_position, tile_id)
                self.renderer.copy(self.tile_textures[tile_id].contents,None,py_sdl_native.SDL_Rect(x_position * 2, y_position * 2, 16, 16))
                
    
    def trigger_stat_interrupt(self):
        '''
            Request an LCD STAT interrupt
        '''
        print("STAT Interrupt")
        self.ie_register.write_bit(bit_number=1, bit= True)
        
        