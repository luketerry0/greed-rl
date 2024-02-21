# stores a static script in a txt file, to be read by RL agents

import math
import random

WIDTH = 55
HEIGHT = 15

game_board = [[math.floor(random.random() * 9) + 1 for x in range(WIDTH)] for y in range(HEIGHT)]

f = open("static_board.txt", "w")
for row in game_board:
    for element in row:
        f.write(str(element))
    f.write("\n")
f.close()