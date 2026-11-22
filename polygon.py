import sys

try:
    import pygame
    from pygame.locals import *
except ImportError:
    pygame = None

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


def polygon(surface=None, color=GREEN, points=((146, 0), (236, 277), (56, 277))):
    """
    Draw a polygon onto a surface or return validated polygon points.

    Supported Boundary Contract:
      Preconditions:
        - Line 9: `WHITE = (255, 255, 255)` background color anchor.
        - Line 10: `GREEN = (0, 255, 0)` drawing color anchor.
        - Boundary: len(points) >= 3 defines the smallest supported polygon domain (triangle).
                    len(points) < 3 is explicitly unsupported and raises ValueError.
      Returns:
        - Pygame Rect if surface is provided and pygame is available, otherwise returns validated points.
      Exceptions:
        - Raises ValueError if len(points) < 3.
    """
    if len(points) < 3:
        raise ValueError("A polygon requires at least 3 points")
    if surface is not None and pygame is not None:
        return pygame.draw.polygon(surface, color, points)
    return points


def main():
    if pygame is None:
        print("pygame is required to run the GUI demo")
        return
    pygame.init()
    window = pygame.display.set_mode((400, 300), 0, 32)
    pygame.display.set_caption("Shape")
    window.fill(WHITE)
    polygon(window, GREEN, ((146, 0), (236, 277), (56, 277)))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


if __name__ == "__main__":
    main()
