import os
import sys
from .game_of_life import GameOfLife

FG_LIGHT = "\033[37m"
FG_DARK = "\033[90m"
BG_LIGHT = "\033[47m"
BG_DARK = "\033[100m"
CELL_CHAR = "\u2584"
RESET_COLOR = "\033[0m"

class TerminalUI:
    _game: GameOfLife
    _size: int

    def __init__(self, game: GameOfLife):
        self._game = game
        terminal_size = os.get_terminal_size()
        self._size = 2 * min(terminal_size.lines, terminal_size.columns) - 5
        self._clear_screen()

    def update(self):
        # Put pointer at top of screen
        sys.stdout.write("\033[H")
        sys.stdout.flush()
        # Print game
        sys.stdout.write(self._get_game_string())
        sys.stdout.flush()

    def _clear_screen(self):
        sys.stdout.write("\033[H\033[2J")
        sys.stdout.flush()

    def _get_game_string(self) -> str:
        result = ""
        view = self._game.get_grid_view(self._size)
        for row in range(0, self._size, 2):
            for col in range(self._size):
                top_color = BG_LIGHT if view[row, col] else BG_DARK
                bottom_color = FG_LIGHT if row + 1 < self._size and view[row + 1, col] else FG_DARK
                result += f"{top_color}{bottom_color}{CELL_CHAR}"
            result += f"{RESET_COLOR}\n"
        result += f"Size: {self._game.get_size()}\n"
        return result