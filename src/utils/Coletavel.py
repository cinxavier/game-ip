import pygame
import utils.sprites as sprite


class Coletavel:
  def __init__(self, tipo: str, pos: tuple[int, int]):
    self.pos = self.x, self.y = pos
    self.tamanho = self.largura, self.altura = (40, 40)
    self.ret = pygame.Rect(self.x, self.y, self.largura, self.altura)

    sprites_coletaveis = sprite.Coletavel()
    if tipo == "util":
      self.sprites = sprites_coletaveis.util()
    elif tipo == "forma":
      self.sprites = sprites_coletaveis.forma()
    elif tipo == "elemento":
      self.sprites = sprites_coletaveis.elemento()

    self.frame = 0
    self.imagem = self.sprites[0]

  def update(self):
    self.frame += self.next_frame

    if self.frame > len(self.sprites) - 1:
      self.frame = 0

    self.imagem = self.sprites[int(self.frame)]
    self.imagem = pygame.transform.scale(self.imagem, self.tamanho)

  def render(self, tela):
    tela.blit(self.imagem, (self.x, self.y))
