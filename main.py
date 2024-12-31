from cpu import CPU

from game_boy import GameBoy
from time import perf_counter



game_boy:GameBoy = GameBoy(cpu_debug_print_counter= None)
print(perf_counter())



running:bool = True

while running:
    game_boy.tick()

    # events = py_sdl.get_events()

    # for e in events:
    #     if e.type == py_sdl_native.SDL_QUIT:
    #         running = False
    #         break
    #     if e.type == py_sdl_native.SDL_KEYDOWN:
    #         if e.key.keysym.sym == py_sdl_native.SDLK_ESCAPE:
    #             running = False   
    #             break
    
    
    
    