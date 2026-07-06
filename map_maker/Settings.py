import pygame

pygame.init()

type rgb_type = tuple[int, int, int]
type pos_type = tuple[int, int]
type size_type = tuple[int, int]

SCREEN_COLORS = {
    "bg_color": (30, 30, 30, 0),
    "tile_color": (50, 50, 50, 0),
}

PALLET_COLORS = {  # cores presentes na paleta
    "red": (200, 0, 0, 9),
    "green": (0, 200, 0, 9),
    "blue": (0, 0, 200, 9),
    "black": (0, 0, 0, 9),
    "white": (200, 200, 200, 9),
}

# global props
BORDER = 0

# cnavas props
CANVAS_GAP = 0

TILE_SIZE = 16

SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_desktop_sizes()[0]
PROPORION_HW = SCREEN_HEIGHT / SCREEN_WIDTH

CANVAS_WIDTH = SCREEN_WIDTH
CANVAS_HEIGHT = CANVAS_WIDTH * PROPORION_HW
CANVAS_SIZE = (CANVAS_WIDTH, CANVAS_HEIGHT)

PALLET_WIDTH = 50
