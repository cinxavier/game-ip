import pygame
from Settings import ESCALA, PALLET_COLORS, COLORS
import src.utils.Tile_map as Tile_map

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
      for conteudo, tijolo in Tile_map.paredes:
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

    for inimigo in Tile_map.lista_inimigos:
      if self.show_hitboxes:
        pygame.draw.rect(
          self.tela,
          COLORS["enemy"],
          (
            inimigo.colisao.x * ESCALA,
            inimigo.colisao.y * ESCALA,
            inimigo.colisao.w * ESCALA,
            inimigo.colisao.h * ESCALA,
          ),
        )
      inimigo.update()
      inimigo.render(self.tela)

  def toggle_hitboxes(self):
    self.show_hitboxes = not self.show_hitboxes

  def get_mapa(self):
    return self.mapa
