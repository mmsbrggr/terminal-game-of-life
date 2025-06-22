import numpy as np
import random
from .infinite_grid import InfiniteGrid

def _cell_lives(window: np.ndarray) -> bool:
    is_alive = window[1, 1]
    num_alive_cells = window.sum()
    if is_alive:
        return 3 <= num_alive_cells <= 4
    return num_alive_cells == 3


class GameOfLife:

    _grid: InfiniteGrid

    def __init__(self):
        self._grid = InfiniteGrid()

    def set_glider(self) -> None:
        self._grid.set(-1, 0)
        self._grid.set(0, 0)
        self._grid.set(1, 0)
        self._grid.set(1, 1)
        self._grid.set(0, 2)

    def set_random(self, size: int) -> None:
        min_coordinate = -int(size/2)
        for x in range(min_coordinate, min_coordinate + size):
            for y in range(min_coordinate, min_coordinate + size):
                if random.choice([True, False]):
                    self._grid.set(x, y)

    def step(self) -> None:
        self._grid.apply_window_function(_cell_lives)

    def get_grid_view(self, view_size: int):
        return self._grid.get_grid_view(view_size)
    
    def get_size(self) -> int:
        return self._grid.get_effective_size()
