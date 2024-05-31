"""
Render class and methods for GOL. Encapsulates all Pygame logic and objects
"""

import sys
import numpy as np
import pygame as pg


def check_input():
    """
    check_input: Gathers all Pygame input and checks for various input combinations. - Contains program exit logic
    :return: void
    """
    if not pg.get_init():
        pg.init()

    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()


def _initialize(tmp_dims, fullscreen):
    """
    Helper function for the initialization of a pygame window
    :param tmp_dims: tuple[int, int]
    :param fullscreen: bool
    :return: tuple[tuple[int, int], bool] (fullscreen can be set to the Pygame flag pygame.FULLSCREEN
    """
    if not (pg.get_init() and pg.display.get_init()):
        pg.init()
        pg.display.init()
    if fullscreen:
        tmp_dims = pg.display.get_desktop_sizes()[0]
        fullscreen = pg.FULLSCREEN
    return tmp_dims, fullscreen


class Renderer(object):
    """
    Renderer class: contains various methods for screen-drawing and updates, as well Pygame objects like Screen and Clock
    """
    def __init__(self, window_dimensions: tuple[int, int], grid_dimensions: tuple[int ,int], max_fps: int = 60, fullscreen: bool = False):
        """
        Initializes Pygame and generates a window based on the given parameters
        :param window_dimensions: tuple[int, int] - The dimensions of the generated window
        :param max_fps: int - The maximum frame rate for the simulation
        :param fullscreen: bool - Temporary value for fullscreen logic
        """

        self.window_dimensions = window_dimensions
        self.max_fps = max_fps
        tmp_dims, self.fullscreen = _initialize(window_dimensions, fullscreen)

        self.screen = pg.display.set_mode(tmp_dims, flags=self.fullscreen)
        self.clock = pg.time.Clock()

        self.colors = {
            'White': (255, 255, 255), 'Gray': (127, 127, 127), 'Black': (0, 0, 0),
            'Red': (255, 0, 0), 'Green': (0, 255, 255), 'Blue': (0, 0, 255),
        }

        self.background_color = self.colors['White']
        self.alive_cell_color = self.colors['Black']
        self.dead_cell_color = self.colors['Gray']

        self.grid_surface: pg.Surface
        self.grid_dimensions = grid_dimensions
        self.grid_scale = (1, 1)
        self.grid_display_dimensions = (self.grid_dimensions[0] * self.grid_scale[0],
                                        self.grid_dimensions[1] * self.grid_scale[1])
        self.cell_size = 5  # Default cell size is set to 5x5 pixels
        self.grid_position = (0, 0)  # Default position to center of window
        self.grid_surface_init = False  # Keeps track of if the current grid surface has been set

    def _update_grid2d_surface(self, dimensions: tuple[int, int]):
        self.grid_dimensions = dimensions
        self.grid_display_dimensions = (self.grid_dimensions[0] * self.grid_scale[0],
                                        self.grid_dimensions[1] * self.grid_scale[1])
        self.grid_surface = pg.Surface(self.grid_display_dimensions)
        self.grid_surface_init = True

    def update_grid2d_scale(self, new_scale: tuple[int, int]):
        self.grid_scale = new_scale

    def update_grid2d_position(self, new_position: tuple[int, int]):
        self.grid_position = new_position

    def update_max_fps(self, new_fps: int):
        self.max_fps = new_fps

    def update_window_dimensions(self, new_dimensions: tuple[int, int]):
        self.window_dimensions = new_dimensions

    def toggle_fullscreen(self):
        if self.fullscreen == pg.FULLSCREEN:
            self.fullscreen = False
            tmp_dims = self.window_dimensions
        else:
            self.fullscreen = pg.FULLSCREEN
            tmp_dims = pg.display.get_desktop_sizes()[0]
        self.screen = pg.display.set_mode(tmp_dims, flags=self.fullscreen)

    def clear_screen(self):
        """
        Fills the current screen with the background color
        :return: void
        """
        self.screen.fill(pg.Color(self.background_color))

    def update_screen(self):
        """
        Updates the current screen and ticks at max_fps
        :return: void
        """
        pg.display.flip()
        self.clock.tick(self.max_fps)

    def draw_cells_2d(self, cells: list, dimensions: tuple[int, int]):
        if not self.grid_surface_init:
            self._update_grid2d_surface(dimensions)

        alive_mask = np.zeros((self.grid_dimensions[0], self.grid_dimensions[1], 3), dtype=np.uint8)
        alive_mask[cells == 1] = self.alive_cell_color
        pg.surfarray.blit_array(self.grid_surface, alive_mask)

        self.screen.blit(self.grid_surface, self.grid_position)
