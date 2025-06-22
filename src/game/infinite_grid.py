from typing import Any, Callable
import numpy as np
from scipy.signal import convolve2d

class InfiniteGrid:
    
    # The border columns will always be kept empty
    _grid: np.ndarray[Any, np.dtype[np.bool]]
    _min_size : int

    def __init__(self, min_size: int = 9):
        if min_size <= 0:
            raise ValueError("Minimum size must be a positive odd integer.")
        if min_size % 2 != 1:
            raise ValueError("Size must must an odd integer.")
        self._min_size = min_size
        self._grid = np.ndarray((min_size, min_size), dtype=np.bool)
        self.empty()

    def empty(self):
        self._grid[:, :] = False

    def set(self, x : int, y : int, value: bool=True):
        self._ensure_coordinate_exists(x)
        self._ensure_coordinate_exists(y)
        size, _ = self._grid.shape
        origin = int(size / 2)
        self._grid[origin - y, origin + x] = value
        self._ensure_padding()

    def set_array(self, array : np.ndarray[Any, np.dtype[np.bool]]):
        if len(array.shape) != 2:
            raise ValueError("Array must be 2D")
        required_size = max(array.shape[0], array.shape[1], self._min_size)
        if required_size % 2 == 0:
            required_size += 1
        self._grid = np.zeros((required_size, required_size), dtype=np.bool)
        origin = int(required_size / 2)
        insert_from_y = origin - int(array.shape[0]  / 2)
        insert_from_x = origin - int(array.shape[1]  / 2)
        self._grid[insert_from_y : insert_from_y + array.shape[0], insert_from_x : insert_from_x + array.shape[1]] = array
        self._ensure_padding()

    def _ensure_coordinate_exists(self, coordinate : int):
        required_size = 2 * abs(coordinate) + 1
        grid_size, _ = self._grid.shape
        if required_size <= self._grid.shape[0]:
            return
        padding = int((required_size - grid_size) / 2)
        self._grid = np.pad(self._grid, padding, mode="constant", constant_values=False)

    def apply_window_function(self, func: Callable[[np.ndarray], bool]):
        new_grid = np.zeros_like(self._grid, dtype=np.bool)
        kernel = np.ones((3,3), dtype=np.uint8)
        convolved_array = convolve2d(self._grid.astype(np.uint8), kernel, mode="same", boundary="fill", fillvalue=0)
        neighbor_mask = convolved_array > 0
        row_indices, col_indices = np.nonzero(neighbor_mask)

        for row, col in zip(row_indices, col_indices):
            window =  self._grid[row - 1 : row + 2, col - 1 : col + 2]
            new_grid[row, col] = func(window)
        self._grid = new_grid
        self._ensure_padding()

    def _ensure_padding(self):
        if not self._border_has_elements():
            return
        self._grid = np.pad(self._grid, 2, mode="constant", constant_values=False)

    def _border_has_elements(self) -> np.bool:
        size, _ = self._grid.shape
        return self._grid[0:2, :].any() or self._grid[:, 0:2].any() or self._grid[size-2:size, :].any() or self._grid[:, size-2:size].any()
    
    def get_effective_size(self) -> int:
        return self._grid.shape[0]
    
    def get_grid_view(self, view_size: int):
        if view_size <= 0:
            raise ValueError("View size must be positive")

        grid_size, _ = self._grid.shape
        result = None
        if grid_size < view_size:
            result = np.zeros((view_size, view_size), dtype=np.bool)
            view_origin = int(view_size / 2)
            insert_from = view_origin - int(grid_size  / 2)
            insert_to = view_origin + int(grid_size / 2) + 1
            result[insert_from : insert_to, insert_from : insert_to] = self._grid
            result.flags.writeable = False
            return result

        if grid_size > view_size:
            grid_origin = int(grid_size / 2)
            cut_from = grid_origin - int((view_size) / 2)
            cut_to = grid_origin + int(view_size / 2) + 1
            result = self._grid[cut_from : cut_to, cut_from : cut_to]
            result.flags.writeable = False
            return result
        
        result = self._grid.view()
        result.flags.writeable = False
        return result
