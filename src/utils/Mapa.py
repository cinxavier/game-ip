import pygame
from Settings import ESCALA, PALLET_COLORS, COLORS
from utils.Tile_map import paredes, inimigos

screen = pygame.display.get_desktop_sizes()[0]


class Mapa:
  def __init__(self, tela: pygame.Surface):
    self.tela = tela
    self.mapa = pygame.image.load("assets/images/Mapa.png")
    self.mapa = pygame.transform.scale(self.mapa, (screen[0], screen[1]))
    self.show_hitboxes = False

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

    if self.show_hitboxes:
      for conteudo, tijolo in paredes:
        pygame.draw.rect(
          self.tela,
          PALLET_COLORS[conteudo],
          (
            tijolo.x * ESCALA,
            tijolo.y * ESCALA,
            tijolo.w * ESCALA,
            tijolo.h * ESCALA,
          ),
        )

    for sprite_inimigo, colisao, campo in inimigos:
      if self.show_hitboxes:
        pygame.draw.rect(
          self.tela,
          COLORS["enemy"],
          (
            campo.x * ESCALA,
            campo.y * ESCALA,
            campo.w * ESCALA,
            campo.h * ESCALA,
          ),
        )

      sprite = pygame.transform.scale_by(sprite_inimigo, ESCALA)
      self.tela.blit(
        sprite,
        (colisao.x * ESCALA, colisao.y * ESCALA),
      )

  def toggle_hitboxes(self):
    self.show_hitboxes = not self.show_hitboxes

  def get_mapa(self):
    return self.mapa
