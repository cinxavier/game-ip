import pygame
from src.utils import Sprites


class Carta:
  def __init__(self, tipo: str, elemento: str):
    sprites = Sprites.Carta(tipo, elemento)
    self.sprite = sprites.item()
    self.proportion = self.sprite.width / self.sprite.height
    self.width, self.height = 150 * self.proportion, 150
    self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))

  def update(self, tamanho: int):
    self.width, self.height = tamanho * self.proportion, tamanho
    self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))

  def render(self, tela, pos: tuple[int, int]):
    tela.blit(self.sprite, pos)
