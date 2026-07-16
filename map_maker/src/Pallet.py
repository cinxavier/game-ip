import pygame
import Settings
from Settings import PALLET_COLORS, BORDER, DEFAULT_FONT, COLORS


class Pallet:
  def __init__(self, screen: pygame.Surface):
    self.screen = screen
    self.selected_color = 0
    self.ink_size = self.ink_width, self.ink_height = (80, 50)
    self.gap = 4
    self.width = (
      (len(PALLET_COLORS) + 1) * (self.ink_width + self.gap)
      - self.gap
      + BORDER * 2
    )
    self.height = (
      self.ink_height * 2
      + BORDER * 2
      + DEFAULT_FONT.get_height()
      + self.gap * 2
    )

  def render(self, x: int, y: int):
    container = pygame.Rect(x, y, self.width, self.height)
    self.pallet = self.screen.subsurface(container)

    pygame.draw.rect(
      self.pallet,
      COLORS["bg"],
      (
        0,
        0,
        self.pallet.get_width(),
        self.pallet.get_height(),
      ),
    )

    pygame.draw.rect(
      self.pallet,
      PALLET_COLORS[self.selected_color],
      (
        BORDER,
        BORDER,
        self.pallet.get_width() - BORDER * 2,
        self.ink_height,
      ),
    )

    for idx, ink in enumerate(PALLET_COLORS):
      pos_x = BORDER + (self.ink_width + self.gap) * idx
      pygame.draw.rect(
        self.pallet,
        ink,
        (
          pos_x,
          BORDER + self.ink_height + self.gap,
          self.ink_width,
          self.ink_height,
        ),
      )

      text = DEFAULT_FONT.render(
        str(idx + 1),
        False,
        COLORS["fg"],
      )

      self.pallet.blit(
        text,
        (
          pos_x + self.ink_width / 2 - text.get_width() / 2,
          self.pallet.get_height() - text.get_height() - BORDER,
        ),
      )
    text = DEFAULT_FONT.render(
      str(Settings.TILE_SIZE),
      False,
      COLORS["fg"],
    )

    self.pallet.blit(
      text,
      (
        pos_x + self.ink_width + self.gap,
        self.pallet.get_height() / 2 - text.get_height() / 2,
      ),
    )