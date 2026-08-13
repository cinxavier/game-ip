import pygame
from src.personagens.Inimigo import Inimigo
from src.personagens.Jogador import Jogador
from src.types.Base_Screen import ScreenBase
from src.utils import Sprites


class Batalha(ScreenBase):
  def __init__(self, game):
    super().__init__(game)
    self.campo = pygame.image.load(
      "assets/images/Campos_Batalha/Campo_Metal.png"
    )
    self.campo = pygame.transform.smoothscale(self.campo, self._screen.size)

    self.player_sprites_ataque = Sprites.Jogador().atacando()
    self.frame_player = 0

    for idx, sprite in enumerate(self.player_sprites_ataque):
      self.player_sprites_ataque[idx] = pygame.transform.scale(
        sprite, (250, 250)
      )

    self.player_sprite_atual = self.player_sprites_ataque[0]

  def handle_events(self, events):
    for event in events:
      if event.type == pygame.KEYDOWN:
        match event.key:
          case pygame.K_ESCAPE:
            self.game.change_screen("game")
            break

  def update(self):
    if self.inimigo:
      # self.frame_player += 0.7
      # self.frame_inimigo += 0.7

      if self.frame_player >= len(self.player_sprites_ataque):
        self.frame_player = 0
      self.player_sprite_atual = self.player_sprites_ataque[
        int(self.frame_player)
      ]

      if self.frame_inimigo >= len(self.inimigo_sprites_ataque):
        self.frame_inimigo = 0

      self.inimigo_sprite_atual = self.inimigo_sprites_ataque[
        int(self.frame_inimigo)
      ]

  def render(self):
    self._screen.blit(self.campo, (0, 0))

    self._screen.blit(
      self.player_sprite_atual,
      (300, self._screen.height / 2 - self.player_sprite_atual.height / 1.5),
    )
    if self.inimigo:
      self._screen.blit(
        self.inimigo_sprite_atual,
        (
          self._screen.width - 300 - self.inimigo_sprite_atual.width,
          self._screen.height / 2 - self.inimigo_sprite_atual.height / 1.5,
        ),
      )

  def set_enemy(self, player: Jogador, inimigo: Inimigo):
    self.player: Jogador = player

    self.inimigo: Inimigo = inimigo
    self.inimigo_sprites_ataque = Sprites.Inimigo(
      inimigo.dados_sprite[0], inimigo.dados_sprite[1]
    ).atacando(Sprites.ESQUERDA)
    self.frame_inimigo = 0

    for idx, sprite in enumerate(self.inimigo_sprites_ataque):
      self.inimigo_sprites_ataque[idx] = pygame.transform.scale(
        sprite, (250, 250)
      )
    self.inimigo_sprite_atual = self.inimigo_sprites_ataque[
      int(self.frame_inimigo)
    ]
