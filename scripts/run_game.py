from game import GameOfLife, TerminalUI, parse_cells
import numpy as np
import time
import random
import sys

DELAY = 0.1
STEPS = 100000000

if len(sys.argv) > 2:
    raise Exception("Usage: command [<cells-file-path>]")

game = game = GameOfLife()
if len(sys.argv) == 2:
    file_path = sys.argv[1]
    with open(file_path, "r") as file:
        game.set_pattern(parse_cells(file.read()))
else:
    random_size = random.randint(2, 90)
    random_pattern = np.random.rand(random_size, random_size) < 0.5
    game.set_pattern(random_pattern)

ui = TerminalUI(game)
for _ in range(STEPS + 1):
    ui.update()
    game.step()
    time.sleep(DELAY)
