import pygame
from src.personagens.Inimigo import Inimigo
from src.types.Base_Screen import ScreenBase
import src.utils.sprites as sprites


class Batalha(ScreenBase):
  def __init__(self, game):
    super().__init__(game)
    self.campo = pygame.image.load(
      "assets/images/Campos_Batalha/Campo_Metal.png"
    )
    self.campo = pygame.transform.smoothscale(self.campo, self._screen.size)

    self.player_sprites = sprites.Jogador().atacando()
    self.player_sprite: pygame.Surface = None

    for idx, sprite in enumerate(self.player_sprites):
      self.player_sprites[idx] = pygame.transform.smoothscale(
        sprite, (250, 250)
      )
    self.frame_player = 0

  def handle_events(self, events):
    for event in events:
      if event.type == pygame.KEYDOWN:
        match event.key:
          case pygame.K_ESCAPE:
            self.game.change_screen("game")
            break

  def update(self):
    self.frame_player += 0.2
    self.frame_enemy += 0.2

    if self.frame_player >= len(self.player_sprites):
      self.frame_player = 0
    if self.frame_enemy >= len(self.enemy_sprites):
      self.frame_enemy = 0

    self.player_sprite = self.player_sprites[int(self.frame_player)]
    self.enemy_sprite = self.enemy[int(self.frame_enemy)]

  def render(self):
    self._screen.blit(self.campo, (0, 0))
    self._screen.blit(
      self.player_sprite,
      (300, self._screen.height / 2 - self.player_sprites[0].height / 1.5),
    )
    self._screen.blit(
      self.enemy_sprite,
      (
        self._screen.width - 300 - self.enemy_sprite.width,
        self._screen.height / 2 - self.player_sprites[0].height / 1.5,
      ),
    )

  def set_enemy(self, inimigo: Inimigo):
    self.enemy_data = inimigo.dados_sprite
    self.enemy_sprites = sprites.Inimigo(
      self.enemy_data[0], self.enemy_data[1]
    ).atacando(self.enemy_data[2])
    for idx, sprite in enumerate(self.enemy_sprites):
      self.enemy_sprites[idx] = pygame.transform.smoothscale(sprite, (250, 250))
    self.enemy_sprite: pygame.Surface = self.enemy_sprites[0]

    self.frame_enemy = 0
