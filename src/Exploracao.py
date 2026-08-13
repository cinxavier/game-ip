import pygame
from src.personagens.Jogador import Jogador
import src.utils.Tile_map as Tile_Map
from src.utils.Tile_map import paredes, init_inimigos
from src.utils.Mapa import Mapa
from src.Settings import ESCALA
from src.types.Base_Screen import ScreenBase
from src.types.Type_Switch_Stand import Type_Switch_Stand


class Exploracao(ScreenBase):
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

    for inimigo in Tile_Map.lista_inimigos:
      inimigo.retang.x -= self.player.camera_x
      inimigo.retang.y -= self.player.camera_y

    self.tempo = pygame.Clock()

  def update(self):
    self.tempo.tick(24)
    self.player.update()
    for idx, inimigo in enumerate(Tile_Map.lista_inimigos):
      if inimigo.colisao.colliderect(self.player.rect):
        self.game.change_screen("battle")
        self.game.curr_screen.set_enemy(self.player, inimigo)

        Tile_Map.lista_inimigos.pop(idx)
        break

  def render(self):
    self.mapa.render((self.player.camera_x, self.player.camera_y))
    self.player.render()

  def handle_events(self, eventos):
    for evento in eventos:
      if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_ESCAPE:
          self.game.change_screen("home")
          break

        match evento.key:
          case pygame.K_c:
            self.player.mostrar_colisao = not self.player.mostrar_colisao
            self.mapa.toggle_hitboxes()
          case pygame.K_e:
            self.player.inventario.is_open = not self.player.inventario.is_open
          case pygame.K_r:
            Tile_Map.lista_inimigos = init_inimigos()
            for inimigo in Tile_Map.lista_inimigos:
              inimigo.retang.x -= self.player.camera_x
              inimigo.retang.y -= self.player.camera_y

      if self.player.inventario.is_open:
        self.player.inventario.events(evento)
    self.player.eventos()
