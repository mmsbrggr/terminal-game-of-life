from game import GameOfLife
from game import TerminalUI
import time


delay = 0.1
steps = 100000000
game = GameOfLife()
game.set_random(50)
ui = TerminalUI(game)

for _ in range(steps + 1):
    ui.update()
    game.step()
    time.sleep(delay)
