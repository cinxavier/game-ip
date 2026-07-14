import json
import pygame
from Settings import (
  PALLET_COLORS,
  TILE_SIZE,
)

txt = pygame.font.Font("assets/fonts/main_font.ttf", 24)


class Canvas:
  def __init__(self, screen: pygame.Surface):

    self.tile_map: list[tuple[int, pygame.Rect]] = []  # matrix da tela
    self.colors = tuple(PALLET_COLORS.keys())

    self.screen = screen

    # tamanho da tela, calculada pela relação dos tijolos bordas e gaps
    self.tiles_amount_x = self.screen.get_width() // TILE_SIZE
    self.tiles_amount_y = self.screen.get_height() // TILE_SIZE

    self.canvas_width = self.tiles_amount_x * TILE_SIZE
    self.canvas_height = self.tiles_amount_y * TILE_SIZE

    self.last_width = self.canvas_width
    self.last_height = self.canvas_height

    map = pygame.image.load("map_maker/src/Mapa.png")
    self.map = pygame.transform.scale(
      map, (self.screen.get_width(), self.screen.get_height())
    )

    self.show_lines = False
    self.show_grid = False

    self.load_save()
    self.update()

  def save_map(self):
    with open("data/settings.json", "w") as data:
      settings = {
        "original_resolution": list(self.screen.get_size()),
        "tile_size": TILE_SIZE,
        "tiles_amount": [self.tiles_amount_x, self.tiles_amount_y],
        "PALLET_COLORS": PALLET_COLORS,
      }
      json.dump(
        settings,
        data,
      )

    with open("data/tile_map.json", "w") as cache:
      json.dump(self.tile_map, cache)

  def load_save(self):
    try:
      with open("data/tile_map.json") as data:
        cache = json.load(data)

        if len(cache) > 0:
          self.tile_map = cache
          self.last_len = len(self.tile_map)
          screen_w_range = range(self.screen.get_width())
          screen_h_range = range(self.screen.get_height())

          for slot in self.tile_map:
            rect = pygame.Rect(slot[1])

            if (
              rect.x in screen_w_range and rect.x + rect.width in screen_w_range
            ) and (
              rect.y in screen_h_range
              and rect.y + rect.height in screen_h_range
            ):
              pygame.draw.rect(
                self.screen, PALLET_COLORS[self.colors[slot[0]]], rect
              )

    except FileNotFoundError:
      print("Arquivo não encontrado")

  def toggle_lines(self):
    self.show_lines = not self.show_lines

  def render_mouse_lines(self):
    mouse_pos = pygame.mouse.get_pos()
    if self.show_lines:
      self.update()
      pygame.draw.line(
        self.screen,
        "white",
        (mouse_pos[0], 0),
        (mouse_pos[0], self.screen.height),
      )
      pygame.draw.line(
        self.screen,
        "white",
        (0, mouse_pos[1]),
        (self.screen.width, mouse_pos[1]),
      )

  def toggle_grid(self):
    self.show_grid = not self.show_grid

  def render_grid(self):
    if self.show_grid:
      for x in range(self.tiles_amount_x):
        pygame.draw.line(
          self.screen,
          (0, 160, 80),
          (x * TILE_SIZE, 0),
          (x * TILE_SIZE, self.screen.width),
        )
      for y in range(self.tiles_amount_y):
        pygame.draw.line(
          self.screen,
          (0, 160, 80),
          (0, y * TILE_SIZE),
          (self.screen.width, y * TILE_SIZE),
        )

  def get_tile_coords(self):
    mouse_pos = pygame.mouse.get_pos()
    tile_percent_x = mouse_pos[0] / self.canvas_width
    tile_pos_x = max(
      0,
      min(
        int(self.tiles_amount_x * tile_percent_x) * TILE_SIZE,
        self.canvas_width - TILE_SIZE,
      ),
    )

    tile_percent_y = mouse_pos[1] / self.canvas_height
    tile_pos_y = max(
      0,
      min(
        int(self.tiles_amount_y * tile_percent_y) * TILE_SIZE,
        self.canvas_height - TILE_SIZE,
      ),
    )

    return tile_pos_x, tile_pos_y

  def draw(self, color_idx: int = None):
    tile_x, tile_y = self.get_tile_coords()
    new_tile = [color_idx, [tile_x, tile_y, TILE_SIZE, TILE_SIZE]]
    if new_tile not in self.tile_map:
      self.tile_map.append(new_tile)
    self.update()

  def erase(self):
    tile_x, tile_y = self.get_tile_coords()
    for tile in self.tile_map:
      if tile[1][0] == tile_x and tile[1][1] == tile_y:
        self.tile_map.pop(self.tile_map.index(tile))
    self.update()

  def clean_all(self):
    self.tile_map = []
    self.update()

  def update(self):
    self.screen.blit(self.map, (0, 0))

    for slot in self.tile_map:
      if slot[0] >= 0:
        pygame.draw.rect(
          self.screen,
          PALLET_COLORS[self.colors[slot[0]]],
          slot[1],
        )

  def redimentionize(self, screen: pygame.Surface):
    self.screen = screen

    self.tiles_amount_x = self.screen.get_width() // TILE_SIZE
    self.tiles_amount_y = self.screen.get_height() // TILE_SIZE

    self.last_width = self.canvas_width
    self.last_height = self.canvas_height

    self.canvas_width = self.tiles_amount_x * TILE_SIZE
    self.canvas_height = self.tiles_amount_y * TILE_SIZE

    self.map = pygame.transform.scale(
      self.map, (self.canvas_width, self.canvas_height)
    )

    # scale_x = self.canvas_width / self.last_width
    # print(scale_x)

    # for tile_idx, tile in enumerate(self.tile_map):
    #     new_data = tile
    #     for idx in range(len(tile[1])):
    #         new_data[1][idx] *= scale_x
    #     self.tile_map[tile_idx] = new_data
    self.update()
