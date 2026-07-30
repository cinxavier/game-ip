import pygame
from Settings import COLORS, DEFAULT_FONT
from game_data.colors import SECONDARY
import src.utils.sprites as sprites


class Inventory:
  def __init__(
    self,
    screen: pygame.Surface,
  ):
    self._screen = screen

    self.tile_size = 120
    self.gap = 5
    self.border = 10
    self.items = {
      sprites.Carta.FORMAS: {
        "quadrado": {"qnt": 1},
        "triangulo": {"qnt": 1},
        "circulo": {"qnt": 0},
      },
      sprites.Carta.ELEMENTAIS: {
        "eletricidade": {"qnt": 1},
        "metal": {"qnt": 0},
        "borracha": {"qnt": 0},
      },
      sprites.Carta.UTILITARIOS: {
        "cura": {"qnt": 2},
        "invisibilidade": {"qnt": 0},
        "bencao": {"qnt": 0},
      },
    }
    for line in self.items:
      for col in self.items[line]:
        img = sprites.Carta(line, col.capitalize()).item()
        img = pygame.transform.scale(img, (self.tile_size, self.tile_size))
        self.items[line][col]["img"] = img

    self.width = (
      self.tile_size * len(self.items)
      + self.gap * (len(self.items) - 1)
      + self.border * 2
    )
    self.bar_size = (self.width - self.border * 2, 25)
    self.height = self.width + (self.bar_size[1] + self.gap) * 3

    self.rect = pygame.Rect(0, 0, self.width, self.height)
    self.rect.centerx = screen.width / 2
    self.rect.centery = screen.height / 2

    self.is_open = False

    self.selected_col = 0
    self.selected_line = 0

  def events(self, event: pygame.Event):
    if event.type == pygame.KEYDOWN:
      match event.key:
        case pygame.K_d:
          self.selected_col += 1
        case pygame.K_a:
          self.selected_col -= 1
        case pygame.K_w:
          self.selected_line -= 1
        case pygame.K_s:
          self.selected_line += 1

  def update(self, hp: int, mp: int):
    self.hp = hp
    self.mp = mp
    if self.selected_line > len(self.items) - 1:
      self.selected_line = len(self.items) - 1
    elif self.selected_line < 0:
      self.selected_line = 0

    if (
      self.selected_col
      > len(self.items[list(self.items.keys())[self.selected_line]]) - 1
    ):
      self.selected_col = (
        len(self.items[list(self.items.keys())[self.selected_line]]) - 1
      )
    elif self.selected_col < 0:
      self.selected_col = 0

  def render(self):
    self.container = self._screen.subsurface(self.rect)
    pygame.draw.rect(
      self.container,
      COLORS["bg"],
      (0, 0, self.container.width, self.container.height),
    )

    pygame.draw.rect(
      self.container, (120, 0, 0), ((self.border, self.border), self.bar_size)
    )
    pygame.draw.rect(
      self.container,
      (200, 0, 0),
      (
        (self.border, self.border),
        (self.bar_size[0] * (self.hp / 100), self.bar_size[1]),
      ),
    )

    txt = DEFAULT_FONT.render(f"HP: {self.hp}", False, COLORS["fg"])
    self.container.blit(
      txt,
      (
        self.container.width / 2 - txt.width / 2,
        self.border + self.bar_size[1] / 2 - txt.height / 2,
      ),
    )
    pygame.draw.rect(
      self.container,
      (0, 0, 120),
      ((self.border, self.border + self.bar_size[1] + self.gap), self.bar_size),
    )
    pygame.draw.rect(
      self.container,
      (0, 0, 200),
      (
        (self.border, self.border + self.bar_size[1] + self.gap),
        (self.bar_size[0] * (self.mp / 100), self.bar_size[1]),
      ),
    )
    txt = DEFAULT_FONT.render(f"MP: {self.mp}", False, COLORS["fg"])
    self.container.blit(
      txt,
      (
        self.container.width / 2 - txt.width / 2,
        self.border
        + self.bar_size[1]
        + self.gap
        + self.bar_size[1] / 2
        - txt.height / 2,
      ),
    )

    for l_idx, line in enumerate(self.items):
      for c_idx, col in enumerate(self.items[line]):
        x = self.border + (self.tile_size + self.gap) * c_idx
        y = (
          self.border
          + (self.tile_size + self.gap) * l_idx
          + (self.bar_size[1] + self.gap) * 3
        )

        if l_idx == self.selected_line and c_idx == self.selected_col:
          pygame.draw.rect(
            self.container,
            SECONDARY,
            (
              x - self.border / 2,
              y - self.border / 2,
              self.tile_size + self.border / 2 * 2,
              self.tile_size + self.border / 2 * 2,
            ),
          )

        pygame.draw.rect(
          self.container,
          COLORS["bg"],
          (
            x,
            y,
            self.tile_size,
            self.tile_size,
          ),
        )
        if self.items[line][col]["qnt"] > 0:
          self.container.blit(self.items[line][col]["img"], (x, y))
          txt = DEFAULT_FONT.render(
            str(self.items[line][col]["qnt"]), False, COLORS["fg"]
          )
          self.container.blit(
            txt,
            (
              x + self.tile_size - txt.width,
              y + self.tile_size - txt.height,
            ),
          )
        else:
          txt = DEFAULT_FONT.render("?", False, COLORS["fg"])
          txt = pygame.transform.scale(
            txt, (self.tile_size, self.tile_size)
          )
          self.container.blit(txt, (x, y))
