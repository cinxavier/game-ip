import json
import pygame
from . import MM_Settings
from .MM_Settings import PALLET_COLORS
from theme import colors
from src.utils.Sprites import Inimigo

txt = pygame.font.Font("assets/fonts/main_font.ttf", 24)

class Canvas:
  def __init__(self, screen: pygame.Surface):
    self.enemies_map: list[tuple[list[str], pygame.Rect, pygame.Rect]] = []
    self.tile_map: list[tuple[int, pygame.Rect]] = []
    self.screen = screen

    # tamanho da tela, calculada pela relação dos tijolos bordas e gaps
    self.tiles_amount_x = self.screen.get_width() // MM_Settings.TILE_SIZE
    self.tiles_amount_y = self.screen.get_height() // MM_Settings.TILE_SIZE

    self.width = self.tiles_amount_x * MM_Settings.TILE_SIZE
    self.height = self.tiles_amount_y * MM_Settings.TILE_SIZE

    map = pygame.image.load("assets/images/Mapa.png")
    self.map = pygame.transform.smoothscale(
      map, (self.screen.get_width(), self.screen.get_height())
    )

    self.waiting_second_point = False
    self.first_rect_x = None
    self.first_rect_y = None
    self.temp_tile_idx = None
    self.spawnpoint: tuple[int, pygame.Rect] = None
    self.load_save()

  def save_map(self):
    with open("data/settings.json", "w") as data:
      spawnpoint_rect = self.spawnpoint[1]
      settings = {
        "PALLET_COLORS": PALLET_COLORS,
        "spawnpoint": [
          self.spawnpoint[0],
          [
            spawnpoint_rect.x,
            spawnpoint_rect.y,
            spawnpoint_rect.w,
            spawnpoint_rect.h,
          ],
        ],
      }
      json.dump(
        settings,
        data,
      )

    with open("data/tile_map.json", "w") as cache:
      backup = self.tile_map.copy()
      for tile in backup:
        x, y, w, h = tile[1].x, tile[1].y, tile[1].w, tile[1].h
        tile[1] = [x, y, w, h]
      json.dump(backup, cache)
    with open("data/enemies_map.json", "w") as cache:
      backup = self.enemies_map.copy()
      for tile in backup:
        enemy_x, enemy_y, enemy_w, enemy_h = (
          tile[1].x,
          tile[1].y,
          tile[1].w,
          tile[1].h,
        )
        hitbox_x, hitbox_y, hitbox_w, hitbox_h = (
          tile[2].x,
          tile[2].y,
          tile[2].w,
          tile[2].h,
        )
        tile[1] = [enemy_x, enemy_y, enemy_w, enemy_h]
        tile[2] = [hitbox_x, hitbox_y, hitbox_w, hitbox_h]
      json.dump(backup, cache)

  def load_save(self):
    try:
      with open("data/tile_map.json") as data:
        cache = json.load(data)
        for item in cache:
          item[1] = pygame.Rect(item[1])
        self.tile_map = cache

      with open("data/enemies_map.json") as data:
        cache = json.load(data)
        for item in cache:
          item[1] = pygame.Rect(item[1])
          item[2] = pygame.Rect(item[2])
        self.enemies_map = cache

      with open("data/settings.json") as data:
        settings = json.load(data)
        if settings["spawnpoint"]:
          spawnpoint_rect_data = settings["spawnpoint"][1]
          self.spawnpoint = [2, pygame.Rect(spawnpoint_rect_data)]
    except FileNotFoundError:
      print("Arquivo não encontrado")

  def get_tile_coords(self):
    mouse_pos = pygame.mouse.get_pos()
    tile_percent_x = mouse_pos[0] / self.width
    tile_pos_x = max(
      0,
      min(
        int(self.tiles_amount_x * tile_percent_x) * MM_Settings.TILE_SIZE,
        self.width - MM_Settings.TILE_SIZE,
      ),
    )

    tile_percent_y = mouse_pos[1] / self.height
    tile_pos_y = max(
      0,
      min(
        int(self.tiles_amount_y * tile_percent_y) * MM_Settings.TILE_SIZE,
        self.height - MM_Settings.TILE_SIZE,
      ),
    )

    return tile_pos_x, tile_pos_y

  def draw_tile(self, ink_idx: int):
    tile_x, tile_y = self.get_tile_coords()
    new_tile = [
      ink_idx,
      pygame.Rect(tile_x, tile_y, MM_Settings.TILE_SIZE, MM_Settings.TILE_SIZE),
    ]

    if new_tile not in self.tile_map:
      if ink_idx == 2:
        if self.spawnpoint is not None:
          for idx, tile in enumerate(self.tile_map):
            if tile[0] == 2:
              self.tile_map.pop(idx)
        self.spawnpoint = new_tile
      self.tile_map.append(new_tile)

  def draw_rect(self, ink_idx: int):
    if not self.waiting_second_point:
      if ink_idx == 2:
        return
      self.first_rect_x, self.first_rect_y = self.get_tile_coords()
      temp_tile = [
        ink_idx,
        pygame.Rect(
          [
            self.first_rect_x,
            self.first_rect_y,
            MM_Settings.TILE_SIZE,
            MM_Settings.TILE_SIZE,
          ]
        ),
      ]
      if temp_tile not in self.tile_map:
        self.temp_tile_idx = len(self.tile_map)
        self.tile_map.append(temp_tile)
        self.waiting_second_point = True

    else:
      second_rect_x, second_rect_y = self.get_tile_coords()
      if second_rect_x < self.first_rect_x:
        second_rect_x, self.first_rect_x = self.first_rect_x, second_rect_x
      if second_rect_y < self.first_rect_y:
        second_rect_y, self.first_rect_y = self.first_rect_y, second_rect_y

      tile_w = second_rect_x - self.first_rect_x + MM_Settings.TILE_SIZE
      tile_h = second_rect_y - self.first_rect_y + MM_Settings.TILE_SIZE

      new_rect = pygame.Rect(
        self.first_rect_x,
        self.first_rect_y,
        max(tile_w, MM_Settings.TILE_SIZE),
        max(tile_h, MM_Settings.TILE_SIZE),
      )

      if self.temp_tile_idx:
        self.tile_map[self.temp_tile_idx][1] = new_rect

      self.waiting_second_point = False
      self.temp_tile_idx = None
      self.first_rect_x = None
      self.first_rect_y = None

  def draw_enemy(self, sprite_data: list[str]):
    tile_x, tile_y = self.get_tile_coords()
    if not self.waiting_second_point:
      self.first_rect_x, self.first_rect_y = tile_x, tile_y

      enemy_position = [
        sprite_data,
        pygame.Rect(
          self.first_rect_x,
          self.first_rect_y,
          MM_Settings.TILE_SIZE,
          MM_Settings.TILE_SIZE,
        ),
        pygame.Rect(
          self.first_rect_x,
          self.first_rect_y,
          MM_Settings.TILE_SIZE,
          MM_Settings.TILE_SIZE,
        ),
      ]

      if enemy_position not in self.enemies_map:
        self.temp_tile_idx = len(self.enemies_map)
        self.enemies_map.append(enemy_position)
        self.waiting_second_point = True
    else:
      second_rect_x, second_rect_y = tile_x, tile_y
      if second_rect_x < self.first_rect_x:
        second_rect_x, self.first_rect_x = self.first_rect_x, second_rect_x
      if second_rect_y < self.first_rect_y:
        second_rect_y, self.first_rect_y = self.first_rect_y, second_rect_y

      tile_w = second_rect_x - self.first_rect_x + MM_Settings.TILE_SIZE
      tile_h = second_rect_y - self.first_rect_y + MM_Settings.TILE_SIZE

      dangerous_hitbox = pygame.Rect(
        self.first_rect_x,
        self.first_rect_y,
        max(tile_w, MM_Settings.TILE_SIZE),
        max(tile_h, MM_Settings.TILE_SIZE),
      )
      if self.temp_tile_idx is not None:
        self.enemies_map[self.temp_tile_idx][2] = dangerous_hitbox

      self.temp_tile_idx = None
      self.waiting_second_point = False
      self.first_rect_x = None
      self.first_rect_y = None

  def erase(self, pensil_type: str):
    tile_x, tile_y = pygame.mouse.get_pos()
    if pensil_type == "enemy":
      for idx, enemy in enumerate(self.enemies_map):
        if enemy[1].collidepoint(tile_x, tile_y):
          self.enemies_map.pop(idx)
    else:
      for idx, tile in enumerate(self.tile_map):
        if tile[1].collidepoint(tile_x, tile_y):
          if tile[0] == 2:
            self.spawnpoint = None
          self.tile_map.pop(idx)
          break

  def clean_all(self):
    self.tile_map = []
    self.spawnpoint = None

  def update_grid_tiles(self):
    self.tiles_amount_x = self.screen.get_width() // MM_Settings.TILE_SIZE
    self.tiles_amount_y = self.screen.get_height() // MM_Settings.TILE_SIZE

    self.width = self.tiles_amount_x * MM_Settings.TILE_SIZE
    self.height = self.tiles_amount_y * MM_Settings.TILE_SIZE

  def update(self):
    self.screen.blit(self.map, (0, 0))
    for tile_type, tile_data in self.tile_map:
      pygame.draw.rect(
        self.screen,
        PALLET_COLORS[tile_type],
        tile_data,
      )

    for enemy_data, rect, hitbox in self.enemies_map:
      sprite = Inimigo(enemy_data[0], enemy_data[1]).parado(enemy_data[2])[0]
      sprite = pygame.transform.scale(sprite, (rect[2], rect[3]))

      pygame.draw.rect(self.screen, colors.ENEMY_HOTBOX, hitbox)
      self.screen.blit(
        sprite,
        (
          rect[0],
          rect[1],
        ),
      )
