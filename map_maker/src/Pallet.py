import pygame
from Settings import (
  pallet_colors,
  border,
)


class Pallet:
  def __init__(self, pos_x: int, pos_y: int = border):
    self.selected_color = pallet_colors["red"]

    self.pallet_width = 80
    self.ink_heigth = 50
    self.pallet_gap = 2

    self.pos_x = pos_x
    self.pos_y = pos_y
    self.width = self.pallet_width + border
    self.heigth = (self.ink_heigth + self.pallet_gap) * len(pallet_colors)

  def draw_pallet(self, screen: pygame.Surface):
    pos_y = border

    container_form = pygame.Rect(self.pos_x, pos_y, self.width, self.heigth)
    self.pallet = screen.subsurface(container_form)
    self.insert_colors()

  def insert_colors(self):
    ink_pos_y = 0
    for key in pallet_colors:
      pygame.draw.rect(
        self.pallet,
        pallet_colors[key],
        (0, ink_pos_y, self.width - self.pallet_gap, self.ink_heigth),
      )
      ink_pos_y += self.ink_heigth + border

  def change_color(self):
    proportion_coef = self.ink_heigth + border
    mouse_pos = pygame.mouse.get_pos()
    ink_idx = mouse_pos[1] // proportion_coef
    inks_names = list(pallet_colors.keys())

    if mouse_pos[0] > self.pos_x and ink_idx < len(pallet_colors):
      self.selected_color = pallet_colors[inks_names[ink_idx]]
