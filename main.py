"""
Main simulation script for the Game Of Life
"""

import render


def main():
    r = render.Renderer((1600, 1000), fullscreen=True)

    while True:
        render.check_input()
        r.clear_screen()
        r.update_screen()


if __name__ == "__main__":
    main()
