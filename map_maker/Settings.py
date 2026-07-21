import pygame

pygame.init()

type rgb_type = tuple[int, int, int]
COLORS = {"bg": (30, 30, 30, 0), "fg": (200, 200, 200)}
PENSILS = ["tile", "rect", "enemy"]

PALLET_COLORS = [
  (0, 0, 0),
  (200, 0, 0),
  (0, 200, 0),
  (200, 200, 200),
  (0, 0, 200),
]

# global props
BORDER = 8

# cnavas props
TILE_SIZE = 24

SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_desktop_sizes()[0]
PROPORION_HW = SCREEN_HEIGHT / SCREEN_WIDTH

CANVAS_SIZE = CANVAS_WIDTH, CANVAS_HEIGHT = (
  SCREEN_WIDTH,
  SCREEN_WIDTH * PROPORION_HW,
)

DEFAULT_FONT = pygame.font.Font("assets/fonts/main_font.ttf", 40)
