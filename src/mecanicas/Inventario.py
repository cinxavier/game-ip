import pygame
from Settings import COLORS, DEFAULT_FONT
from game_data.colors import SECONDARY
import src.utils.sprites as sprites


class Inventory:
  def __init__(self, screen: pygame.Surface):
    self._screen = screen
        
    self.tile_size = 120
    self.gap = 5
    self.border = 10
    self.items = {
      sprites.Carta.FORMAS: {
        "circulo": {"qnt": 0},
        "quadrado": {"qnt": 1},
        "triangulo": {"qnt": 0},
      },
      sprites.Carta.ELEMENTAIS: {
        "metal": {"qnt": 0},
        "eletricidade": {"qnt": 1},
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
    self.height = self.width

    self.rect = pygame.Rect(0, 0, self.width, self.height)
    self.rect.centerx = screen.width / 2
    self.rect.centery = screen.height / 2

    self.is_open = True

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

  def update(self):
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
    for l_idx, line in enumerate(self.items):
      for c_idx, col in enumerate(self.items[line]):
        x = self.border + (self.tile_size + self.gap) * c_idx
        y = self.border + (self.tile_size + self.gap) * l_idx

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
          COLORS["fg"],
          (
            x,
            y,
            self.tile_size,
            self.tile_size,
          ),
        )

        self.container.blit(self.items[line][col]["img"], (x, y))
        txt = DEFAULT_FONT.render(str(self.items[line][col]['qnt']), False, False)
        self.container.blit(
          txt,
          (
            x + self.tile_size - txt.width,
            y + self.tile_size - txt.height,
          ),
        )
