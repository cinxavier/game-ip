import pygame
import Settings
from Settings import PALLET_COLORS, BORDER, DEFAULT_FONT, COLORS
from .sprites import Inimigo, NIVEIS, TIPOS, FRENTE

sprites: list[pygame.Surface] = []

for nivel in NIVEIS:
  for tipo in TIPOS:
    sprite = Inimigo(nivel, tipo).parado(FRENTE)[0]
    sprite = pygame.transform.scale(sprite, (120, 120))
    sprites.append([sprite, [nivel, tipo, FRENTE]])


class Pallet:
  def __init__(
    self,
    screen: pygame.Surface,
  ):
    self.screen = screen
    self.content_width, self.content_height = (50, 50)
    self.gap = 4
    self.width = (
      (len(PALLET_COLORS) + 1) * (self.content_width + self.gap)
      - self.gap
      + BORDER * 2
    )

    self.height = (
      self.content_height * 2
      + BORDER * 2
      + DEFAULT_FONT.get_height()
      + self.gap * 2
    )

    self.selected_color = 0
    self.selected_sprite = 0

  def update(self, x: int, y: int, curr_pensil: str):
    self.curr_pensil = curr_pensil
    if self.curr_pensil == "enemy":
      self.content_width, self.content_height = (120, 120)
      self.sprites_width = (
        (len(sprites) + 1) * (self.content_width + self.gap)
        - self.gap
        + BORDER * 2
      )
      self.width = self.sprites_width

    else:
      self.content_width, self.content_height = (50, 50)
      self.colors_width = (
        (len(PALLET_COLORS) + 1) * (self.content_width + self.gap)
        - self.gap
        + BORDER * 2
      )
      self.width = self.colors_width

    self.height = (
      self.content_height * 2
      + BORDER * 2
      + DEFAULT_FONT.get_height()
      + self.gap * 2
    )

    container = pygame.Rect(x, y, self.width, self.height)
    self.pallet = self.screen.subsurface(container)

  def render(self):

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

    if self.curr_pensil == "enemy":
      self.pallet.blit(
        sprites[self.selected_sprite][0],
        (self.pallet.width / 2 - self.content_width / 2, BORDER),
      )

    else:
      pygame.draw.rect(
        self.pallet,
        PALLET_COLORS[self.selected_color],
        (
          BORDER,
          BORDER,
          self.pallet.get_width() - BORDER * 2,
          self.content_height,
        ),
      )

    for idx, contents in enumerate(
      sprites if self.curr_pensil == "enemy" else PALLET_COLORS
    ):
      content = contents[0] if self.curr_pensil == "enemy" else contents
      pos_x = BORDER + (self.content_width + self.gap) * idx
      if self.curr_pensil == "enemy":
        self.pallet.blit(
          content, (pos_x, BORDER + self.content_height + self.gap)
        )
      else:
        pygame.draw.rect(
          self.pallet,
          content,
          (
            pos_x,
            BORDER + self.content_height + self.gap,
            self.content_width,
            self.content_height,
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
          pos_x + self.content_width / 2 - text.get_width() / 2,
          self.pallet.get_height() - text.get_height() - BORDER,
        ),
      )

    text = DEFAULT_FONT.render(
      f"{Settings.TILE_SIZE}",
      False,
      COLORS["fg"],
    )
    self.pallet.blit(
      text,
      (
        pos_x + self.content_width + self.gap,
        self.pallet.get_height() / 2 - text.get_height() / 2,
      ),
    )
