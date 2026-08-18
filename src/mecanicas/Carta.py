import pygame
from src.utils import Sprites


class Carta:
  def __init__(self, tipo: str, elemento: str):
    sprites = Sprites.Carta(tipo, elemento)
    self.sprite = sprites.item()
    self.width, self.height = 270, 270
    self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))

  def update(self, tamanho: int):
    self.width, self.height = tamanho, tamanho
    self.sprite = pygame.transform.scale(self.sprite, (tamanho, tamanho))

  def render(self, tela, pos: tuple[int, int]):
    tela.blit(self.sprite, pos)
