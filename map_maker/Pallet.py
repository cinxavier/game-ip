import pygame
from . import MM_Settings
from .MM_Settings import PALLET_COLORS, PENSILS
from theme import fonts, sizes, colors
from src.utils.Sprites import Inimigo
from src.utils import Sprites

sprites: list[tuple[pygame.Surface, list[str]]] = []

for nivel in Sprites.NIVEIS:
  for tipo in Sprites.ELEMENTOS:
    sprite = Inimigo(nivel, tipo).parado(Sprites.FRENTE)[0]
    sprite = pygame.transform.scale(sprite, (120, 120))
    sprites.append([sprite, [nivel, tipo]])


class Pallet:
  def __init__(self, screen: pygame.Surface):
    self.show = True

    self.screen = screen
    self.content_width, self.content_height = (50, 50)
    self.gap = 4
    self.width = (
      (len(PALLET_COLORS) + 1) * (self.content_width + self.gap)
      - self.gap
      + sizes.BORDER * 2
    )

    self.height = (
      self.content_height * 2
      + sizes.BORDER * 2
      + fonts.DEFAULT.get_height()
      + self.gap * 2
    )

    self.pensil_idx = 0
    self.curr_pensil = PENSILS[self.pensil_idx]
    self.selected_color = 0
    self.selected_sprite = 0
    self.sprite_direction_idx = 0

  def update(self, x: int, y: int):
    self.curr_pensil = PENSILS[self.pensil_idx]
    if self.curr_pensil == "enemy":
      self.content_width, self.content_height = (120, 120)
      self.sprites_width = (
        (len(sprites) + 1) * (self.content_width + self.gap)
        - self.gap
        + sizes.BORDER * 2
      )
      self.width = self.sprites_width

    else:
      self.content_width, self.content_height = (50, 50)
      self.colors_width = (
        (len(PALLET_COLORS) + 1) * (self.content_width + self.gap)
        - self.gap
        + sizes.BORDER * 2
      )
      self.width = self.colors_width

    self.height = (
      self.content_height * 2
      + sizes.BORDER * 2
      + fonts.DEFAULT.get_height()
      + self.gap * 2
    )

    container = pygame.Rect(x, y, self.width, self.height)
    self.pallet = self.screen.subsurface(container)

  def render(self):
    pygame.draw.rect(
      self.pallet,
      colors.BACKGROUND,
      (
        0,
        0,
        self.pallet.get_width(),
        self.pallet.get_height(),
      ),
    )

    if self.curr_pensil == "enemy":
      sprite = pygame.transform.scale(self.get_sprite(), (120, 120))
      self.pallet.blit(
        sprite,
        (self.pallet.width / 2 - self.content_width / 2, sizes.BORDER),
      )

    else:
      pygame.draw.rect(
        self.pallet,
        PALLET_COLORS[self.selected_color],
        (
          sizes.BORDER,
          sizes.BORDER,
          self.pallet.get_width() - sizes.BORDER * 2,
          self.content_height,
        ),
      )

    for idx, contents in enumerate(
      sprites if self.curr_pensil == "enemy" else PALLET_COLORS
    ):
      content = contents[0] if self.curr_pensil == "enemy" else contents
      pos_x = sizes.BORDER + (self.content_width + self.gap) * idx
      if self.curr_pensil == "enemy":
        self.pallet.blit(
          content, (pos_x, sizes.BORDER + self.content_height + self.gap)
        )
      else:
        pygame.draw.rect(
          self.pallet,
          content,
          (
            pos_x,
            sizes.BORDER + self.content_height + self.gap,
            self.content_width,
            self.content_height,
          ),
        )

      text = fonts.DEFAULT.render(
        str(idx + 1),
        False,
        colors.FOREGROUND,
      )

      self.pallet.blit(
        text,
        (
          pos_x + self.content_width / 2 - text.get_width() / 2,
          self.pallet.get_height() - text.get_height() - sizes.BORDER,
        ),
      )

    text = fonts.DEFAULT.render(
      f"{MM_Settings.TILE_SIZE}",
      False,
      colors.FOREGROUND,
    )
    self.pallet.blit(
      text,
      (
        pos_x + self.content_width + self.gap,
        self.pallet.get_height() / 2 - text.get_height() / 2,
      ),
    )

  def toggle_show(self):
    self.show = not self.show

  def change_sprite_direction(self):
    self.sprite_direction_idx += (
      1
      if self.sprite_direction_idx < len(Sprites.DIRECOES) - 1
      else -(len(Sprites.DIRECOES) - 1)
    )

  def get_sprite(self, only_data: bool = False):
    sprite = sprites[self.selected_sprite][1] + [
      Sprites.DIRECOES[self.sprite_direction_idx]
    ]
    if only_data:
      return sprite
    return Inimigo(sprite[0], sprite[1]).parado(
      Sprites.DIRECOES[self.sprite_direction_idx]
    )[0]

  def change_pensil(self):
    self.pensil_idx += (
      1 if self.pensil_idx < len(PENSILS) - 1 else -(len(PENSILS) - 1)
    )

  def change_pallet_ink(self, ink_idx: int):
    if self.curr_pensil == "enemy":
      self.selected_sprite = min(ink_idx, len(sprites) - 1)
    else:
      self.selected_color = min(ink_idx, len(PALLET_COLORS) - 1)
