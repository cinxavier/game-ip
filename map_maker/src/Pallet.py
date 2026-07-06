import pygame
from map_maker.Settings import PALLET_COLORS, BORDER, PALLET_WIDTH


class Pallet:
  def __init__(self, pos_x: int, pos_y: int = BORDER):
    self.selected_color = 0
    PALLET_WIDTH
    self.ink_heigth = 50
    self.gap = 2

    self.pos_x = pos_x
    self.pos_y = pos_y

    self.width = PALLET_WIDTH + BORDER
    self.heigth = (self.ink_heigth + self.gap) * len(PALLET_COLORS)

  def draw_pallet(self, screen: pygame.Surface):
    pos_y = BORDER

    container_form = pygame.Rect(self.pos_x, pos_y, self.width, self.heigth)
    self.pallet = screen.subsurface(container_form)
    self.insert_colors()

  def insert_colors(self):
    ink_pos_y = 0
    for key in PALLET_COLORS:
      pygame.draw.rect(
        self.pallet,
        PALLET_COLORS[key],
        (0, ink_pos_y, self.width - self.gap, self.ink_heigth),
      )
      ink_pos_y += self.ink_heigth + self.gap

  def change_color(self):
    proportion_coef = self.ink_heigth + BORDER
    mouse_pos = pygame.mouse.get_pos()
    ink_idx = mouse_pos[1] // proportion_coef

    if mouse_pos[0] > self.pos_x and ink_idx < len(PALLET_COLORS):
      self.selected_color = ink_idx
