import json
import pygame
from Settings import (
  screen_colors,
  pallet_colors,
  canvas_gap,
  canvas_tile_size,
  canvas_tiles_amount,
  border,
  rgb_type,
)


class Canvas:
  def __init__(self):
    self.drawings: list = []  # matrix da tela
    self.selected_color = pallet_colors["red"]

    self.border = border
    self.gap = canvas_gap  # espaço entre tijolos da tela
    self.tile_size = canvas_tile_size  # tamanho dos tijolos da tela
    self.tiles_amount = canvas_tiles_amount  # numero de tijolos² na tela

    # tamanho da tela, calculada pela relação dos tijolos bordas e gaps
    self.size = (
      self.tile_size * self.tiles_amount
      + self.border * 2
      + self.gap * (self.tiles_amount - 1)
    )
    if not self.load_save():
      self.create_grid()

  def save_drawing(self):
    with open("cache.json", "w") as cache:
      json.dump(self.drawings, cache, indent=2)

  def load_save(self):
    with open("cache.json") as data:
      cache = json.load(data)
      if len(cache) > 0:
        self.drawings = cache
        return True
      return False

  def create_grid(self):  # cria a matriz da tela
    for line in range(self.tiles_amount):
      self.drawings.append([])
      for col in range(self.tiles_amount):
        pos_x = (
          self.border + (self.gap + self.tile_size if col > 0 else self.tile_size) * col
        )
        pos_y = (
          self.border
          + (self.gap + self.tile_size if line > 0 else self.tile_size) * line
        )
        pos_size = (
          pos_x,
          pos_y,
          self.tile_size,  # size x
          self.tile_size,  # size y
        )

        grid = (screen_colors["tile_color"], pos_size)
        self.drawings[line].append(grid)

  def draw_grid(self, screen: pygame.Surface):
    canvas_container = pygame.Rect((0, 0, self.size, self.size))
    self.canvas = screen.subsurface(canvas_container)

    for line in self.drawings:
      for slot in line:
        pygame.draw.rect(self.canvas, slot[0], slot[1])

  # desenha na tela com cores especificas ou cores selecionadas da paleta
  def draw(self, color: rgb_type = None):
    # o coeficiente de proporção entre um tijolo e outro em relação a matrix
    # se o coeficiente é 2, e o cursor estiver em uma posição entre 1 e 2.9, o indice é 0
    # caso o cursor esteja entre 3 e 4.9, o indice é 1
    mouse_pos = pygame.mouse.get_pos()
    proportion_coef = self.size / self.tiles_amount
    col = int(mouse_pos[0] / proportion_coef)
    line = int(mouse_pos[1] / proportion_coef)

    # caso o mouse esteja nas delimitações da tela e selecione um tijolo registrado
    x_in_range = 0 <= col <= self.tiles_amount - 1
    y_in_range = 0 <= line <= self.tiles_amount - 1
    if x_in_range and y_in_range:
      slot = self.drawings[line][col]
      # desenha nesse tijolo especifico com a cor selecionada
      self.drawings[line][col] = (color or self.selected_color,) + (tuple(slot[1]),)

  def clean_all(self, screen: pygame.Surface):
    self.drawings = []
    self.create_grid()
    self.draw_grid(screen)
