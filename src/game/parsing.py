from typing import Any
import numpy as np

def parse_cells(cells_string: str) -> np.ndarray[Any, np.dtype[np.bool]]:
    lines = cells_string.split("\n")
    lines = [l for l in lines if not l.startswith("!")]
    height = len(lines)
    width = max([len(l) for l in lines])
    result = np.zeros((height, width), dtype=np.bool)
    for row in range(height):
        row_data = _parse_cells_line(lines[row])
        result[row, 0 : row_data.size] = row_data
    return result

def _parse_cells_line(cells_line: str) -> np.ndarray[Any, np.dtype[np.bool]]:
    return np.asarray([c == "O" for c in cells_line], dtype=np.bool)