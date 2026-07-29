import pygame
from src.personagens.Jogador import Jogador
from src.utils.Tile_map import paredes, lista_inimigos
from src.utils.Mapa import Mapa
from Settings import ESCALA
from interfaces.Base_Screen import ScreenBase
from src.types.Type_Switch_Stand import Type_Switch_Stand

class Jogo(ScreenBase):
  def __init__(self, game: Type_Switch_Stand):
    super().__init__(game)

    self.mapa = Mapa(self._screen)
    self.player = Jogador(self._screen, self.mapa.get_mapa())

    self.player.camera_x = (
      self.player.camera_x
      - self.mapa.get_mapa().width / ESCALA / 2
      + self.player.rect.w
    )
    self.player.camera_y = (
      self.player.camera_y
      - self.mapa.get_mapa().height / ESCALA / 2
      + self.player.rect.h
    )
    self.player.update()

    for tijolo in paredes:
      tijolo[1].x -= self.player.camera_x
      tijolo[1].y -= self.player.camera_y

    for inimigo in lista_inimigos:
      inimigo.retang.x -= self.player.camera_x
      inimigo.retang.y -= self.player.camera_y

    self.tempo = pygame.Clock()

  def update(self):
    self.tempo.tick(24)
    self.player.update()

  def render(self):
    self.mapa.render((self.player.camera_x, self.player.camera_y))
    self.player.render()

  def handle_events(self, eventos):
    for evento in eventos:
      if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_ESCAPE:
          self.game.change_screen("home" '')
          break

        match evento.key:
          case pygame.K_c:
            self.player.mostrar_colisao = not self.player.mostrar_colisao
            self.mapa.toggle_hitboxes()
      self.player.inventario.events(evento)
    self.player.eventos()
