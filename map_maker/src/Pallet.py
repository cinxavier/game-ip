import pygame


class Pallet:
  def __init__(self):
    self.pallet_colors = {
      "black": {"rgb": (0, 0, 0)},
      "red": {"rgb": (200, 0, 0)},
      "green": {"rgb": (0, 200, 0)},
      "blue": {"rgb": (0, 0, 200)},
      "white": {"rgb": (200, 200, 200)},
    }
    self.ink_heigth = 50
    self.selected_color = self.pallet_colors["red"]["rgb"]

  def draw_pallet(self):
    pallet_pos_x = self.canvas_size
    pallet_pos_y = self.border
    self.pallet_width = self.canvas_size * 0.2 - self.border
    self.pallet_heigth = self.canvas_size - self.border * 2

    container_form = pygame.Rect(
      pallet_pos_x, pallet_pos_y, self.pallet_width, self.pallet_heigth
    )

    self.pallet = self.screen.subsurface(container_form)
    self.pallet.fill((25, 25, 25))

  def insert_colors(self):
    pos_y = 0

    for key in self.pallet_colors:
      self.pallet_colors[key]["ink"] = pygame.draw.rect(
        self.pallet,
        self.pallet_colors[key]["rgb"],
        (0, pos_y, self.pallet_width - self.gap, self.ink_heigth),
      )
      pos_y += self.ink_heigth + self.border

  def change_color(self, mouse_pos):
    proportion_coef = self.ink_heigth + self.border
    ink_idx = mouse_pos[1] // proportion_coef
    inks_names = list(self.pallet_colors.keys())
    if mouse_pos[0] > self.canvas_size and ink_idx < len(self.pallet_colors):
      self.selected_color = self.pallet_colors[inks_names[ink_idx]]["rgb"]
