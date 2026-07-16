import pygame
from Settings import ESCALA, PALLET_COLORS
from utils.Tile_map import paredes


class Mapa:
  def __init__(self, tela: pygame.Surface):
    self.tela = tela
    self.mapa = pygame.image.load("assets/images/Mapa.png")
    self.mapa = pygame.transform.scale(
      self.mapa, (self.tela.get_width(), self.tela.get_height())
    )

  def render(self, camera_pos: tuple[int, int]):
    camera_x, camera_y = camera_pos
    area_parcial = self.mapa.subsurface(
      (
        min(
          camera_x,
          self.mapa.get_width() - int(self.tela.get_width() / ESCALA),
        ),
        min(
          camera_y,
          self.mapa.get_height() - int(self.tela.get_height() / ESCALA),
        ),
        int(self.tela.get_width() / ESCALA),
        int(self.tela.get_height() / ESCALA),
      )
    )
    area_parcial = pygame.transform.smoothscale(area_parcial, self.tela.size)
    self.tela.blit(area_parcial, (0, 0))

    for cor_idx, tijolo in paredes:
      pygame.draw.rect(
        self.tela,
        PALLET_COLORS[cor_idx],
        (
          tijolo.x * ESCALA,
          tijolo.y * ESCALA,
          tijolo.w * ESCALA,
          tijolo.h * ESCALA,
        ),
      )

  def get_mapa(self):
    return self.mapa
