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
    self.player_sprites: dict[str, list[pygame.Surface]] = {
      "ataque": Sprites.Jogador().atacando(),
      "parado": Sprites.Jogador().parado(Sprites.DIREITA),
    }
    self.player_animacao_atual = "parado"
    self.frame_player = 0

    for sprites in self.player_sprites:
      for idx, sprite in enumerate(self.player_sprites[sprites]):
        self.player_sprites[sprites][idx] = pygame.transform.scale(sprite, (110, 110))

    self.player_sprite_atual: pygame.Surface = self.player_sprites[
      self.player_animacao_atual
    ][0]

  def handle_events(self, events):
    for event in events:
      if event.type == pygame.KEYDOWN:
        match event.key:
          case pygame.K_ESCAPE:
            if self.player.disco_de_batalha.curr_group >= 0:
              self.player.disco_de_batalha.curr_group = -1
              self.player.disco_de_batalha.cursor_idx = 0
            else:
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

  def render_player(self):
    player_pos = (
      300,
      self._screen.height / 2 - self.player_sprite_atual.height / 1.5,
    )
    self._screen.blit(self.player_sprite_atual, player_pos)
    player_hp_w = self.player_sprites["parado"][0].width
    player_hp_h = 20
    player_hp_x = player_pos[0]
    player_hp_y = player_pos[1] - player_hp_h - 5

    pygame.draw.rect(
      self._screen, "red", (player_hp_x, player_hp_y, player_hp_w, player_hp_h)
    )
    pygame.draw.rect(
      self._screen,
      "green",
      (player_hp_x, player_hp_y, player_hp_w * (self.player.hp / 100), player_hp_h),
    )
    font = pygame.font.Font("assets/fonts/main_font.ttf", 25)
    player_hp_text = font.render(f"{self.player.hp}/100", False, "black")
    self._screen.blit(
      player_hp_text,
      (
        player_hp_x + (player_hp_w - player_hp_text.width) / 2,
        player_hp_y + (player_hp_h - player_hp_text.height) / 2,
      ),
    )

  def render_enemy(self):
    enemy_pos = (
      self._screen.width - 300 - self.inimigo_sprite_atual.width,
      self._screen.height / 2 - self.inimigo_sprite_atual.height / 1.5,
    )
    enemy_hp_w = self.inimigo_sprites["parado"][0].width
    enemy_hp_h = 20
    enemy_hp_x = enemy_pos[0]
    enemy_hp_y = enemy_pos[1] - enemy_hp_h - 5

    pygame.draw.rect(
      self._screen, "red", (enemy_hp_x, enemy_hp_y, enemy_hp_w, enemy_hp_h)
    )
    pygame.draw.rect(
      self._screen,
      "green",
      (enemy_hp_x, enemy_hp_y, enemy_hp_w * (self.inimigo.hp / 100), enemy_hp_h),
    )

    font = pygame.font.Font("assets/fonts/main_font.ttf", 25)
    enemy_hp_text = font.render(f"{self.inimigo.hp}/100", False, "black")
    self._screen.blit(
      enemy_hp_text,
      (
        enemy_hp_x + (enemy_hp_w - enemy_hp_text.width) / 2,
        enemy_hp_y + (enemy_hp_h - enemy_hp_text.height) / 2,
      ),
    )

    self._screen.blit(self.inimigo_sprite_atual, enemy_pos)

  def render(self):
    if self.inimigo:
      self._screen.blit(self.campo, (0, 0))

      self.render_player()
      self.render_enemy()

      self.player.disco_de_batalha.render()

  def set_enemy(self, inimigo: Inimigo):
    self.inimigo: Inimigo = inimigo

    sprites_inimigo = Sprites.Inimigo(inimigo.dados_sprite[0], inimigo.dados_sprite[1])
    self.inimigo_sprites: dict[str, list[pygame.Surface]] = {
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
