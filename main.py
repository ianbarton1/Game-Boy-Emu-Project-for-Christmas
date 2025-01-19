from cpu import CPU

from game_boy import GameBoy
from time import perf_counter


blargg_test_list = [
    # 'roms/tests/blargg/01-special.gb', #hang fail
    # 'roms/tests/blargg/02-interrupts.gb', #test 2 fail
    # R'roms/tests/blargg/03-op sp,hl.gb' #crash fail
    # R"roms/tests/blargg/04-op r,imm.gb", #hang fail
    # R"roms/tests/blargg/05-op rp.gb", #hang fail
    # R"roms/tests/blargg/06-ld r,r.gb", # test 6 fail
    # R"roms/tests/blargg/07-jr,jp,call,ret,rst.gb", #test 7 crash
    # R"roms/tests/blargg/08-misc instrs.", #test 8 hangs
    # R"roms/tests/blargg/09-op r,r.gb", #test 9 hangs
    # R"roms/tests/blargg/10-bit ops.gb", #test 10 hangs
    # R"roms/tests/blargg/11-op a,(hl).gb" #test 11 unimplemented instruction
    # R"roms/games/tetris.gb",
    R"roms/games/drmario.gb"
]

for rom_file in blargg_test_list:
    game_boy:GameBoy = GameBoy(cpu_debug_print_counter= None, rom_file = rom_file, display_debug= True)
    print(perf_counter())
    game_boy.joypad.debug_pause = True
    game_boy.play()




    
    
    
    