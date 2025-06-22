from game import GameOfLife
from game import TerminalUI
import numpy as np
import time
import random


DELAY = 0.1
STEPS = 100000000

game = game = GameOfLife()
random_size = random.randint(2, 90)
random_pattern = np.random.rand(random_size, random_size) < 0.5
game.set_pattern(random_pattern)

ui = TerminalUI(game)
for _ in range(STEPS + 1):
    ui.update()
    game.step()
    time.sleep(DELAY)
