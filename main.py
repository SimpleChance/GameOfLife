"""
Main simulation script for the Game Of Life
"""

import render
import game_engine


def main():
    engine2d = game_engine.Engine2D()
    r = render.Renderer((1000, 600), engine2d.dimensions, fullscreen=False)

    for i in range(125, 375):
        for j in range(125, 375):
            engine2d.cells[i][j] = True

    while True:
        render.check_input()

        engine2d.gol_update_cells()

        r.clear_screen()
        r.draw_cells_2d(engine2d.cells, engine2d.dimensions)
        r.update_screen()


if __name__ == "__main__":
    main()
