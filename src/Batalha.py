import pygame
from src.personagens.Inimigo import Inimigo
from src.personagens.Jogador import Jogador
from src.types.Base_Screen import ScreenBase
from src.utils import Sprites


class Batalha(ScreenBase):
  def __init__(self, game, player: Jogador):
    super().__init__(game)
    self.campo = pygame.image.load("assets/images/Campos_Batalha/Campo_Metal.png")
    self.campo = pygame.transform.smoothscale(self.campo, self._screen.size)

    self.player: Jogador = player
    self.player_sprites = {
      "ataque": Sprites.Jogador().atacando(),
      "parado": Sprites.Jogador().parado(Sprites.DIREITA),
    }
    self.player_animacao_atual = "parado"
    self.frame_player = 0

    for sprites in self.player_sprites:
      for idx, sprite in enumerate(self.player_sprites[sprites]):
        self.player_sprites[sprites][idx] = pygame.transform.scale(sprite, (110, 110))

    self.player_sprite_atual = self.player_sprites[self.player_animacao_atual][0]

  def handle_events(self, events):
    for event in events:
      if event.type == pygame.KEYDOWN:
        match event.key:
          case pygame.K_ESCAPE:
            self.game.change_screen("game")
            break
          case pygame.K_1:
            self.run_animation("player", "ataque")
          case pygame.K_2:
            self.run_animation("inimigo", "ataque")
        self.player.disco_de_batalha.events(event)
          
  def update(self):
    if self.inimigo:
      self.frame_player += 0.3
      self.frame_inimigo += 0.2 if self.inimigo_animacao_atual == "ataque" else 0.2

      if self.frame_player >= len(self.player_sprites[self.player_animacao_atual]):
        self.frame_player = 0
        if self.player_animacao_atual != "parado":
          self.run_animation("player", "parado")

      self.player_sprite_atual = self.player_sprites[self.player_animacao_atual][
        int(self.frame_player)
      ]

      if self.frame_inimigo >= len(self.inimigo_sprites[self.inimigo_animacao_atual]):
        self.frame_inimigo = 0
        if self.inimigo_animacao_atual != "parado":
          self.run_animation("inimigo", "parado")

      self.inimigo_sprite_atual = self.inimigo_sprites[self.inimigo_animacao_atual][
        int(self.frame_inimigo)
      ]
      self.player.update()
  def render(self):
    if self.inimigo:
      self._screen.blit(self.campo, (0, 0))

      self._screen.blit(
        self.player_sprite_atual,
        (300, self._screen.height / 2 - self.player_sprite_atual.height / 1.5),
      )
      self._screen.blit(
        self.inimigo_sprite_atual,
        (
          self._screen.width - 300 - self.inimigo_sprite_atual.width,
          self._screen.height / 2 - self.inimigo_sprite_atual.height / 1.5,
        ),
      )

      self.player.disco_de_batalha.render()

  def set_enemy(self, inimigo: Inimigo):
    self.inimigo: Inimigo = inimigo

    sprites_inimigo = Sprites.Inimigo(inimigo.dados_sprite[0], inimigo.dados_sprite[1])
    self.inimigo_sprites = {
      "parado": sprites_inimigo.parado(Sprites.ESQUERDA),
      "ataque": sprites_inimigo.atacando(),
    }

    for sprites in self.inimigo_sprites:
      for idx, sprite in enumerate(self.inimigo_sprites[sprites]):
        self.inimigo_sprites[sprites][idx] = pygame.transform.scale(sprite, (220, 220))

    self.frame_inimigo = 0
    self.inimigo_animacao_atual = "parado"
    self.inimigo_sprite_atual = self.inimigo_sprites[self.inimigo_animacao_atual][0]

  def run_animation(self, personagem: str, acao: str):
    if personagem == "inimigo":
      self.frame_inimigo = 0
      self.inimigo_animacao_atual = acao
    elif personagem == "player":
      self.frame_player = 0
      self.player_animacao_atual = acao
