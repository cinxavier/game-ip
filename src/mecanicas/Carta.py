import pygame
from src.utils import Sprites


class Carta:
  def __init__(self, tipo: str, elemento: str):
    sprites = Sprites.Carta(tipo, elemento)
    self.sprite = sprites.item()
    tamanho = 200
    self.sprite = pygame.transform.scale(self.sprite, (tamanho, tamanho*1.1))

  def update(self):
    pass

  def render(self, tela, pos: tuple[int, int]):
    tela.blit(self.sprite, pos)
