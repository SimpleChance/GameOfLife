"""
GameEngine class file: Encapsulates GOL logic and data structures
"""
import numpy as np
from scipy.signal import convolve2d


class Engine(object):
    """
    Engine base class: contains numpy array representing cells in the environment and the dimensions of said environment
    """
    def __init__(self, grid_dimensions: tuple, ndims: int):
        self.ndims = ndims
        self.dimensions = grid_dimensions
        self.cells = np.zeros(shape=[self.dimensions[_] for _ in range(self.ndims)])

    def _update_cell_dtype(self, dtype: str):
        self.cells.astype(dtype, copy=False)


class Engine2D(Engine):
    def __init__(self, grid_dimensions: tuple[int, int] = (500, 500), ndims: int = 2):
        super().__init__(grid_dimensions, ndims)
        self.kernel = np.array([[1, 1, 1],
                                [1, 0, 1],
                                [1, 1, 1]])

    def gol_update_cells(self):
        # Scipy convolve2d to efficiently count neighbors based on a kernel
        neighbors_count = convolve2d(self.cells, self.kernel, mode='same', boundary='wrap')
        # Default GOL rules applied efficiently using Numpy arrays
        self.cells = (neighbors_count == 3) | ((self.cells == 1) & (neighbors_count == 2))
        self._update_cell_dtype('bool')
