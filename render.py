"""
Render class and methods for Game of Life. Encapsulates all Pygame logic and objects
"""

import sys
import pygame as pg


def check_input():
    """
    check_input: Gathers all Pygame input and checks for various inputs. - Contains program exit logic
    :return: void
    """
    if not pg.get_init():
        pg.init()
        pg.display.init()

    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()


class Renderer(object):
    """
    Renderer class: contains various methods for screen-drawing and updates, as well Pygame objects like Screen and Clock
    """
    def __init__(self, window_dimensions: tuple[int, int], max_fps: int = 60, fullscreen: bool = False):
        """
        Initializes Pygame and generates a window based on the given parameters
        :param window_dimensions: tuple[int, int] - The dimensions of the generated window
        :param max_fps: int - The maximum frame rate for the simulation
        :param fullscreen: bool - Temporary value for fullscreen logic
        """
        pg.init()
        pg.display.init()
        if fullscreen:
            window_dimensions = pg.display.get_desktop_sizes()[0]
            fullscreen = pg.FULLSCREEN

        self.window_dimensions = window_dimensions
        self.max_fps = max_fps

        self.screen = pg.display.set_mode(window_dimensions, flags=fullscreen)
        self.clock = pg.time.Clock()

        self.background_color = pg.Color("white")

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
