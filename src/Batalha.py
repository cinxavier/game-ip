import pygame
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
    for idx, sprite in enumerate(self.player_sprites):
      self.player_sprites[idx] = pygame.transform.smoothscale(
        sprite, (250, 250)
      )

  def handle_events(self, events):
    for event in events:
      if event.type == pygame.KEYDOWN:
        match event.key:
          case pygame.K_ESCAPE:
            self.game.change_screen("game")
            break

  def update(self):
    pass

  def render(self):
    self._screen.blit(self.campo, (0, 0))
    self._screen.blit(
      self.player_sprites[0],
      (300, self._screen.height / 2 - self.player_sprites[0].height / 1.5),
    )
