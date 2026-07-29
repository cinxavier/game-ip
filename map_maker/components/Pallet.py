import pygame
import Settings
from Settings import PALLET_COLORS, BORDER, DEFAULT_FONT, COLORS, PENSILS
from .sprites import Inimigo, NIVEIS, TIPOS, FRENTE, DIRECOES

sprites: list[tuple[pygame.Surface, list[str]]] = []

for nivel in NIVEIS:
  for tipo in TIPOS:
    sprite = Inimigo(nivel, tipo).parado(FRENTE)[0]
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
      + BORDER * 2
    )

    self.height = (
      self.content_height * 2
      + BORDER * 2
      + DEFAULT_FONT.get_height()
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
      sprite_data = sprites[self.selected_sprite][1]
      sprite = Inimigo(sprite_data[0], sprite_data[1]).parado(
        DIRECOES[self.sprite_direction_idx]
      )[0]
      sprite = pygame.transform.scale(sprite, (120, 120))
      self.pallet.blit(
        sprite,
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

  def toggle_show(self):
    self.show = not self.show

  def change_sprite_direction(self):
    self.sprite_direction_idx += (
      1
      if self.sprite_direction_idx < len(DIRECOES) - 1
      else -(len(DIRECOES) - 1)
    )

  def get_sprite(self, only_data: bool = False):
    sprite = sprites[self.selected_sprite][1] + [
      DIRECOES[self.sprite_direction_idx]
    ]
    if only_data:
      return sprite
    return Inimigo(sprite[0], sprite[1]).parado(
      DIRECOES[self.sprite_direction_idx]
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
