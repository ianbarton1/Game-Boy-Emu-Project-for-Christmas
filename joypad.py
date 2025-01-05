import sys
import sdl2.ext as py_sdl
import sdl2 as py_sdl_native

from bus import Bus

class Joypad:
    def __init__(self,bus:Bus, parent_gameboy, show_keypresses:bool = False, ):
        self.bus = bus
        self.keyboard_poll_frequency:int = 600
        self.keyboard_poll_timer:int = 0

        self.debug_pause:bool = False
        self.debug_print:bool = False

        self.joypad_register = self.bus.read(0xFF00)
        self.joypad_register.add_read_viewer(self.print_joypad_read)
        self.interrupt_register = self.bus.read(0xFF0F)

        self.last_key_state = {'up': False,
                               'down': False,
                               'right': False,
                               'left': False,
                               'a':False,
                               'b': False,
                               'select': False,
                               'start': False
                            }

        self.print_keypresses = show_keypresses
        self.parent_gameboy = parent_gameboy

    def print_joypad_read(self):
        self.update_register()
    
    def update_register(self):
        self.joypad_register.write_bit(bit_number=0, bit=True)
        self.joypad_register.write_bit(bit_number=1, bit=True)
        self.joypad_register.write_bit(bit_number=2, bit=True)
        self.joypad_register.write_bit(bit_number=3, bit=True)

        buttons_mode = not self.joypad_register.get_bit(bit_number=5)
        d_pad_mode = not self.joypad_register.get_bit(bit_number=4)

        for key, key_pressed in self.last_key_state.items():

            if buttons_mode and not d_pad_mode:
                match key:
                    case 'start':
                        self.joypad_register.write_bit(bit_number=3, bit=not key_pressed)
                    case 'a':
                        self.joypad_register.write_bit(bit_number=0, bit=not key_pressed)
                    case 'b':
                        self.joypad_register.write_bit(bit_number=1, bit=not key_pressed)
                    case 'select':
                        self.joypad_register.write_bit(bit_number=2, bit = not key_pressed)
            elif d_pad_mode and not buttons_mode:
                match key:
                    case 'down':
                        self.joypad_register.write_bit(bit_number=3, bit=not key_pressed)
                    case 'right':
                        self.joypad_register.write_bit(bit_number=0, bit=not key_pressed)
                    case 'left':
                        self.joypad_register.write_bit(bit_number=1, bit=not key_pressed)
                    case 'up':
                        self.joypad_register.write_bit(bit_number=2, bit = not key_pressed)
                



    def tick(self):
        self.keyboard_poll_timer += 1
        if self.keyboard_poll_timer >= self.keyboard_poll_frequency:
            self.keyboard_poll_timer = 0
            

            self.check_key_presses()

    def check_key_presses(self):
        events = py_sdl.get_events()

        for e in events:
            if e.type == py_sdl_native.SDL_KEYDOWN:
                for key in self.last_key_state.keys():
                    self.last_key_state[key] = False

            if e.type == py_sdl_native.SDL_QUIT:
                self.parent_gameboy.finish()
            
            

            if e.type == py_sdl_native.SDL_KEYDOWN:

                # print("Joypad Interrupt Requested")
                self.interrupt_register.write_bit(bit_number=4, bit=True)
                if e.key.keysym.sym == py_sdl_native.SDLK_ESCAPE:
                    self.parent_gameboy.finish()
                
                
                if e.key.keysym.sym == py_sdl_native.SDLK_RETURN:
                    self.last_key_state['start'] = True
                    if self.print_keypresses:
                        print('Joypad: START')
                if e.key.keysym.sym == py_sdl_native.SDLK_z:
                    self.last_key_state['a'] = True
                    if self.print_keypresses:
                        print('Joypad: A')
                if e.key.keysym.sym == py_sdl_native.SDLK_x:
                    self.last_key_state['b'] = True
                    if self.print_keypresses:
                        print('Joypad: B')
                        
                    #TODO: select
                
                if e.key.keysym.sym == py_sdl_native.SDLK_LEFT:
                    self.last_key_state['left'] = True
                    if self.print_keypresses:
                        print('Joypad: LEFT')
                if e.key.keysym.sym == py_sdl_native.SDLK_UP:
                    self.last_key_state['up'] = True
                    if self.print_keypresses:
                        print('Joypad: UP')
                if e.key.keysym.sym == py_sdl_native.SDLK_RIGHT:
                    self.last_key_state['right'] = True
                    if self.print_keypresses:
                        print('Joypad: RIGHT')
                if e.key.keysym.sym == py_sdl_native.SDLK_DOWN:
                    self.last_key_state['down'] = True
                    if self.print_keypresses:
                        print('Joypad: DOWN')

                if e.key.keysym.sym == py_sdl_native.SDLK_p:
                    self.debug_pause ^= True
                    match self.debug_pause:
                        case True:
                            print("Emulation was paused. Press d to print current emulation state")
                        case False:
                            print("Emulation was restarted.")

                if e.key.keysym.sym == py_sdl_native.SDLK_d and self.debug_pause:
                    self.debug_print = True