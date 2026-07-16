import json
import pygame
import Settings
from Settings import PALLET_COLORS, PENSILS

txt = pygame.font.Font("assets/fonts/main_font.ttf", 24)


class Canvas:
  def __init__(self, screen: pygame.Surface):

    self.tile_map: list[tuple[int, pygame.Rect]] = []  # matrix da tela
    self.screen = screen

    # tamanho da tela, calculada pela relação dos tijolos bordas e gaps
    self.tiles_amount_x = self.screen.get_width() // Settings.TILE_SIZE
    self.tiles_amount_y = self.screen.get_height() // Settings.TILE_SIZE

    self.canvas_width = self.tiles_amount_x * Settings.TILE_SIZE
    self.canvas_height = self.tiles_amount_y * Settings.TILE_SIZE

    map = pygame.image.load("map_maker/src/Mapa.png")
    self.map = pygame.transform.scale(
      map, (self.screen.get_width(), self.screen.get_height())
    )

    self.show_lines = False
    self.show_grid = False
    self.waiting_rect_width = False
    self.first_rect_x = None
    self.first_rect_y = None
    self.pensil_idx = 0

    self.load_save()

  def save_map(self):
    with open("data/settings.json", "w") as data:
      settings = {
        "original_resolution": list(self.screen.get_size()),
        "tile_size": Settings.TILE_SIZE,
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

          for color_idx, tile_data in self.tile_map:
            rect = pygame.Rect(tile_data)

            if (
              rect.x in screen_w_range and rect.x + rect.width in screen_w_range
            ) and (
              rect.y in screen_h_range
              and rect.y + rect.height in screen_h_range
            ):
              pygame.draw.rect(self.screen, PALLET_COLORS[color_idx], rect)

    except FileNotFoundError:
      print("Arquivo não encontrado")

  def toggle_lines(self):
    self.show_lines = not self.show_lines

  def render_mouse_lines(self):
    mouse_pos = pygame.mouse.get_pos()
    if self.show_lines:
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
          (x * Settings.TILE_SIZE, 0),
          (x * Settings.TILE_SIZE, self.screen.width),
        )
      for y in range(self.tiles_amount_y):
        pygame.draw.line(
          self.screen,
          (0, 160, 120),
          (0, y * Settings.TILE_SIZE),
          (self.screen.width, y * Settings.TILE_SIZE),
        )

  def get_tile_coords(self):
    mouse_pos = pygame.mouse.get_pos()
    tile_percent_x = mouse_pos[0] / self.canvas_width
    tile_pos_x = max(
      0,
      min(
        int(self.tiles_amount_x * tile_percent_x) * Settings.TILE_SIZE,
        self.canvas_width - Settings.TILE_SIZE,
      ),
    )

    tile_percent_y = mouse_pos[1] / self.canvas_height
    tile_pos_y = max(
      0,
      min(
        int(self.tiles_amount_y * tile_percent_y) * Settings.TILE_SIZE,
        self.canvas_height - Settings.TILE_SIZE,
      ),
    )

    return tile_pos_x, tile_pos_y

  def draw(self, color_idx: int = None):
    match PENSILS[self.pensil_idx]:
      case "tile":
        tile_x, tile_y = self.get_tile_coords()
        new_tile = [
          color_idx,
          [tile_x, tile_y, Settings.TILE_SIZE, Settings.TILE_SIZE],
        ]
        if new_tile not in self.tile_map:
          self.tile_map.append(new_tile)

      case "rect":
        if not self.waiting_rect_width:
          self.first_rect_x, self.first_rect_y = self.get_tile_coords()
          temp_tile = [
            color_idx,
            [
              self.first_rect_x,
              self.first_rect_y,
              Settings.TILE_SIZE,
              Settings.TILE_SIZE,
            ],
          ]
          if temp_tile not in self.tile_map:
            self.tile_map.append(temp_tile)
          self.waiting_rect_width = True

        else:
          second_rect_x, second_rect_y = self.get_tile_coords()
          if second_rect_x < self.first_rect_x:
            second_rect_x, self.first_rect_x = self.first_rect_x, second_rect_x
          if second_rect_y < self.first_rect_y:
            second_rect_y, self.first_rect_y = self.first_rect_y, second_rect_y

          tile_w = second_rect_x - self.first_rect_x + Settings.TILE_SIZE
          tile_h = second_rect_y - self.first_rect_y + Settings.TILE_SIZE

          new_tile = [
            color_idx,
            [
              self.first_rect_x,
              self.first_rect_y,
              max(tile_w, Settings.TILE_SIZE),
              max(tile_h, Settings.TILE_SIZE),
            ],
          ]
          if new_tile not in self.tile_map:
            self.tile_map.append(new_tile)

          temp_tile = [
            color_idx,
            [
              self.first_rect_x,
              self.first_rect_y,
              Settings.TILE_SIZE,
              Settings.TILE_SIZE,
            ],
          ]
          if temp_tile in self.tile_map:
            self.tile_map.pop(self.tile_map.index(temp_tile))

          self.waiting_rect_width = False
          self.first_rect_x = None
          self.first_rect_y = None

  def erase(self):
    tile_x, tile_y = self.get_tile_coords()
    for tile in self.tile_map:
      if tile[1][0] == tile_x and tile[1][1] == tile_y:
        self.tile_map.pop(self.tile_map.index(tile))

  def clean_all(self):
    self.tile_map = []

  def update_grid_tiles(self):
    self.tiles_amount_x = self.screen.get_width() // Settings.TILE_SIZE
    self.tiles_amount_y = self.screen.get_height() // Settings.TILE_SIZE

    self.canvas_width = self.tiles_amount_x * Settings.TILE_SIZE
    self.canvas_height = self.tiles_amount_y * Settings.TILE_SIZE

  def update(self):
    self.screen.blit(self.map, (0, 0))
    for color_idx, tile_data in self.tile_map:
      pygame.draw.rect(
        self.screen,
        PALLET_COLORS[color_idx],
        tile_data,
      )
