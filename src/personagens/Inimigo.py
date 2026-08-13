import pygame
from src.utils import Sprites
from src.Settings import ESCALA
from ..types.Personagem import Personagem


class Inimigo(Personagem):
  def __init__(
    self,
    dados_sprite: list[str],
    retang: pygame.Rect,
    colisao: pygame.Rect,
  ):
    self.retang = retang
    self.colisao = colisao
    self.largura, self.altura = self.retang.w, self.retang.h
    self.dados_sprite = dados_sprite
    self.sprites = Sprites.Inimigo(dados_sprite[0], dados_sprite[1]).parado(
      dados_sprite[2]
    )

    self.frame = 0
    self.prox_frame = 0.5
    self.sprite_atual = self.sprites[self.frame]

  def eventos(self):
    return super().eventos()

  def update(self):
    self.colisao.x = self.retang.x
    self.colisao.y = self.retang.y
    
    if self.frame >= len(self.sprites) - 1:
      self.frame = 0

    self.frame += self.prox_frame

    self.sprite_atual = self.sprites[int(self.frame)]
    self.sprite_atual = pygame.transform.smoothscale(
      self.sprite_atual, (self.largura * ESCALA, self.altura * ESCALA)
    )

  def render(self, tela: pygame.Surface):
    self.sprite_atual = pygame.transform.scale_by(self.sprite_atual, 3)
    tela.blit(
      self.sprite_atual,
      (
        (
          self.retang.x
          - self.sprite_atual.width / ESCALA / 2
          + self.retang.w / 2
        )
        * ESCALA,
        (
          self.retang.y
          - self.sprite_atual.height / ESCALA / 2
          + self.retang.height / 2
        )
        * ESCALA,
      ),
    )
