import json
import pygame
from Settings import screen_colors, pallet_colors, canvas_settings, pallet_settings


class Canvas:
  def __init__(self):
    self.drawings: list = []  # matrix da tela
    self.pallet_colors = pallet_colors
    self.ink_heigth = pallet_settings["ink_heigth"]  # altura do bloco de tinta
    self.selected_color = self.pallet_colors["red"]["rgb"]

    self.border = canvas_settings["border"]
    self.gap = canvas_settings["gap"]  # espaço entre tijolos da tela
    self.tile_size = canvas_settings["tile_size"]  # tamanho dos tijolos da tela
    self.tiles_amount = canvas_settings["tiles_amount"]  # numero de tijolos² na tela

    # tamanho da tela, calculada pela relação dos tijolos bordas e gaps
    self.canvas_size = (
      self.tile_size * self.tiles_amount
      + self.border * 2
      + self.gap * (self.tiles_amount - 1)
    )
    # janela que carrega a tela e a paleta
    self.screen = pygame.display.set_mode((self.canvas_size * 1.2, self.canvas_size))
    self.screen.fill(screen_colors["bg_color"])

    self.create_grid()
    self.draw_pallet()
    self.insert_colors()

  def create_grid(self):  # cria a matriz da tela
    with open("cache.json") as data:
      cache = json.load(data)
      if len(cache) > 0:
        self.drawings = cache
        return

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

  def draw_grid(self):  # desenha a tela
    for line in self.drawings:
      for slot in line:
        pygame.draw.rect(self.screen, slot[0], slot[1])  # tile

  # desenha na tela com cores especificas ou cores selecionadas da paleta
  def draw(self, matrix_coords, color=None):
    # o coeficiente de proporção entre um tijolo e outro em relação a matrix
    # se o coeficiente é 2, e o cursor estiver em uma posição entre 1 e 2.9, o indice é 0
    # caso o cursor esteja entre 3 e 4.9, o indice é 1
    proportion_coef = self.canvas_size / self.tiles_amount
    col = int(matrix_coords[0] / proportion_coef)
    line = int(matrix_coords[1] / proportion_coef)

    # caso o mouse esteja nas delimitações da tela e selecione um tijolo registrado
    if col <= self.tiles_amount - 1 and line <= self.tiles_amount - 1:
      slot = self.drawings[line][col]
      if matrix_coords:  # se as coordenadas forem dadas
        # desenha nesse tijolo especifico com a cor selecionada
        self.drawings[line][col] = (color or self.selected_color,) + (tuple(slot[1]),)

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
