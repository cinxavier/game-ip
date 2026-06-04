import pygame
import pygame.locals as pg_lc
from interfaces import RGB, grid_style

pygame.init()
bg_color: RGB = (30, 30, 30)
pygame.display.set_caption("Map Maker")


class Canvas:
  def __init__(self):
    self.color: RGB = (15, 15, 15)

    self.border = 5
    self.gap = 1
    self.tile_size = 16
    self.tiles_amount = 32

    self.screen_size = (
      self.tile_size * self.tiles_amount
      + self.border * 2
      + self.gap * (self.tiles_amount - 1)
    )
    self.screen = pygame.display.set_mode((self.screen_size * 1.2, self.screen_size))
    self.screen.fill(bg_color)
    self.drawings: list[grid_style] = []

    self.set_grid()
    self.set_pallet()


  def set_grid(self):
    for line in range(self.tiles_amount):
      self.drawings.append([])
      for col in range(self.tiles_amount):
        pos_x = (
          self.border + (self.gap + self.tile_size if col > 0 else self.tile_size) * col
        )
        pos_y = (
          self.border
          + (self.gap + self.tile_size if line > 0 else self.tile_size) * line
        )
        pos_size = (
          pos_x,
          pos_y,
          self.tile_size,  # size x
          self.tile_size,  # size y
        )

        grid = (self.color, pos_size)
        self.drawings[line].append(grid)
    self.selected_grid = self.drawings[0][0]

  def draw_grid(self):
    for line in self.drawings:
      for slot in line:
        pygame.draw.rect(self.screen, slot[0], slot[1])  # tile

  def draw(self, matrix_coords, color=(255, 0, 0)):
    proportion_coef = self.screen_size / self.tiles_amount
    col = int(matrix_coords[0] / proportion_coef)
    line = int(matrix_coords[1] / proportion_coef)

    if col <= self.tiles_amount - 1 and line <= self.tiles_amount - 1:
      slot = self.drawings[line][col]

      if matrix_coords:
        self.drawings[line][col] = (color,) + (tuple(slot[1]),)

  def set_pallet(self):
    self.pallet_pos_x = self.screen_size
    self.pallet_pos_y = self.border
    pygame.draw.rect(
      self.screen,
      (255, 255, 255),
      (self.pallet_pos_x, self.pallet_pos_y, self.screen_size * 0.1, 40),
    )


canvas = Canvas()

running_game = True
while running_game:
  canvas.draw_grid()
  for event in pygame.event.get():
    if event.type == pg_lc.QUIT:
      running_game = False

  if pygame.mouse.get_pressed()[0]:
    try:
      canvas.draw(tuple(event.pos))
    except AttributeError:
      pass
  elif pygame.mouse.get_pressed()[2]:
    try:
      canvas.draw(tuple(event.pos), canvas.color)
    except AttributeError:
      pass

  pygame.display.update()

pygame.quit()
