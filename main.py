from cpu import CPU

from game_boy import GameBoy
from time import perf_counter


game_boy:GameBoy = GameBoy()
print(perf_counter())
while True:
    game_boy.tick()