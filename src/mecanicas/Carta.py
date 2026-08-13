import pygame
from src.utils import Sprites


class Carta:
  def __init__(self, tipo: str, elemento: str):
    sprites = Sprites.Carta(tipo, elemento)
    self.sprite = sprites.item()
    tamanho = 270
    self.sprite = pygame.transform.scale(self.sprite, (tamanho, tamanho))

  def update(self):
    pass

  def render(self, tela, pos: tuple[int, int]):
    tela.blit(self.sprite, pos)
