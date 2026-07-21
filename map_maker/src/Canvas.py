import json
import pygame
import Settings
from Settings import PALLET_COLORS, PENSILS
from .sprites import Inimigo
from .Pallet import sprite

txt = pygame.font.Font("assets/fonts/main_font.ttf", 24)


class Canvas:
  def __init__(self, screen: pygame.Surface):
    self.tile_map: list[tuple[int, pygame.Rect]] = []  # matrix da tela
    self.screen = screen

    # tamanho da tela, calculada pela relação dos tijolos bordas e gaps
    self.tiles_amount_x = self.screen.get_width() // Settings.TILE_SIZE
    self.tiles_amount_y = self.screen.get_height() // Settings.TILE_SIZE

    self.width = self.tiles_amount_x * Settings.TILE_SIZE
    self.height = self.tiles_amount_y * Settings.TILE_SIZE

    map = pygame.image.load("assets/images/Mapa.png")
    self.map = pygame.transform.scale(
      map, (self.screen.get_width(), self.screen.get_height())
    )

    self.waiting_rect_second_point = False
    self.first_rect_x = None
    self.first_rect_y = None
    self.pensil_idx = 0
    self.spawnpoint = None
    self.load_save()

  def save_map(self):
    with open("data/settings.json", "w") as data:
      settings = {"PALLET_COLORS": PALLET_COLORS, "spawnpoint": self.spawnpoint}
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

        self.tile_map = cache

        for idx, (tile_type, _, tile_data) in enumerate(self.tile_map):
          if tile_type == "rect":
            rect = pygame.Rect(tile_data)
            self.tile_map[idx][2] = rect

      with open("data/settings.json") as data:
        settings = json.load(data)
        if settings["spawnpoint"]:
          self.spawnpoint = settings["spawnpoint"]
    except FileNotFoundError:
      print("Arquivo não encontrado")

  def get_tile_coords(self):
    mouse_pos = pygame.mouse.get_pos()
    tile_percent_x = mouse_pos[0] / self.width
    tile_pos_x = max(
      0,
      min(
        int(self.tiles_amount_x * tile_percent_x) * Settings.TILE_SIZE,
        self.width - Settings.TILE_SIZE,
      ),
    )

    tile_percent_y = mouse_pos[1] / self.height
    tile_pos_y = max(
      0,
      min(
        int(self.tiles_amount_y * tile_percent_y) * Settings.TILE_SIZE,
        self.height - Settings.TILE_SIZE,
      ),
    )

    return tile_pos_x, tile_pos_y

  def draw(self, content: int | list[str] = None):
    match PENSILS[self.pensil_idx]:
      case "tile":
        tile_x, tile_y = self.get_tile_coords()
        new_tile = [
          "rect",
          content,
          [tile_x, tile_y, Settings.TILE_SIZE, Settings.TILE_SIZE],
        ]

        if new_tile not in self.tile_map:
          if content == 2:
            if self.spawnpoint:
              for tile in self.tile_map:
                if tile[0] == 2:
                  self.tile_map.pop(self.tile_map.index(tile))
              self.spawnpoint = None
            self.spawnpoint = new_tile

          self.tile_map.append(new_tile)

      case "rect":
        if not self.waiting_rect_second_point:
          if content == 2:
            return
          self.first_rect_x, self.first_rect_y = self.get_tile_coords()
          temp_tile = [
            "rect",
            content,
            [
              self.first_rect_x,
              self.first_rect_y,
              Settings.TILE_SIZE,
              Settings.TILE_SIZE,
            ],
          ]
          if temp_tile not in self.tile_map:
            self.tile_map.append(temp_tile)
          self.waiting_rect_second_point = True

        else:
          second_rect_x, second_rect_y = self.get_tile_coords()
          if second_rect_x < self.first_rect_x:
            second_rect_x, self.first_rect_x = self.first_rect_x, second_rect_x
          if second_rect_y < self.first_rect_y:
            second_rect_y, self.first_rect_y = self.first_rect_y, second_rect_y

          tile_w = second_rect_x - self.first_rect_x + Settings.TILE_SIZE
          tile_h = second_rect_y - self.first_rect_y + Settings.TILE_SIZE

          new_tile = [
            "rect",
            content,
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
            content,
            [
              self.first_rect_x,
              self.first_rect_y,
              Settings.TILE_SIZE,
              Settings.TILE_SIZE,
            ],
          ]
          if temp_tile in self.tile_map:
            self.tile_map.pop(self.tile_map.index(temp_tile))

          self.waiting_rect_second_point = False
          self.first_rect_x = None
          self.first_rect_y = None

      case "enemy":
        tile_x, tile_y = self.get_tile_coords()
        tile_x -= sprite.width / 2
        tile_y -= sprite.height / 2

        new_line = [
          "enemy",
          content,
          [tile_x, tile_y, sprite.width, sprite.height],
        ]
        if new_line not in self.tile_map:
          self.tile_map.append(new_line)

  def erase(self):
    tile_x, tile_y = self.get_tile_coords()
    for tile in self.tile_map:
      if tile[0] == "rect":
        if tile[2][0] == tile_x and tile[2][1] == tile_y:
          if tile[1] == 2:
            self.spawnpoint = None
          self.tile_map.pop(self.tile_map.index(tile))

  def clean_all(self):
    self.tile_map = []
    self.spawnpoint = None

  def update_grid_tiles(self):
    self.tiles_amount_x = self.screen.get_width() // Settings.TILE_SIZE
    self.tiles_amount_y = self.screen.get_height() // Settings.TILE_SIZE

    self.width = self.tiles_amount_x * Settings.TILE_SIZE
    self.height = self.tiles_amount_y * Settings.TILE_SIZE

  def update(self):
    self.screen.blit(self.map, (0, 0))
    for tile_type, content, tile_data in self.tile_map:
      match tile_type:
        case "rect":
          pygame.draw.rect(
            self.screen,
            PALLET_COLORS[content],
            tile_data,
          )
        case "enemy":
          self.screen.blit(
            Inimigo(content[0], content[1]).parado(content[2])[0],
            tile_data,
          )
