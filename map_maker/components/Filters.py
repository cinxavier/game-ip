import pygame
import Settings
from .Canvas import Canvas


class Filters:
  def __init__(self, screen: pygame.Surface, canvas: Canvas):
    self.screen = screen
    self.canvas = canvas

    self.show_lines = False
    self.show_grid = False

  def toggle_lines(self):
    self.show_lines = not self.show_lines

  def render_mouse_lines(self):
    mouse_pos = pygame.mouse.get_pos()
    if self.show_lines:
      pygame.draw.line(
        self.screen,
        "white",
        (mouse_pos[0], 0),
        (mouse_pos[0], self.screen.height),
      )
      pygame.draw.line(
        self.screen,
        "white",
        (0, mouse_pos[1]),
        (self.screen.width, mouse_pos[1]),
      )

  def toggle_grid(self):
    self.show_grid = not self.show_grid

  def render_grid(self):
    if self.show_grid:
      for x in range(self.canvas.tiles_amount_x):
        pygame.draw.line(
          self.screen,
          (0, 160, 80),
          (x * Settings.TILE_SIZE, 0),
          (x * Settings.TILE_SIZE, self.screen.width),
        )
      for y in range(self.canvas.tiles_amount_y):
        pygame.draw.line(
          self.screen,
          (0, 160, 120),
          (0, y * Settings.TILE_SIZE),
          (self.screen.width, y * Settings.TILE_SIZE),
        )

  