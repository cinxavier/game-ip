import pygame
from .Inventario import Inventory
from .Carta import Carta


class Disco_Batalha:
  def __init__(self, tela: pygame.Surface, inventario: Inventory):
    self._screen = tela
    self.inventario = inventario

    self.decks = self.inventario.get_items_list().copy()
    for deck in self.decks:
      for carta in deck:
        carta.update(200)

    self.curr_group = -1

  def events(self, evento: pygame.Event):
    if evento.type == pygame.KEYDOWN:
      match evento.key:
        case pygame.K_SPACE:
          self.curr_group += 1

  def update(self):
    if self.curr_group >= len(self.decks):
      self.curr_group = -1

  def render(self):
    carta_ex: Carta = self.decks[0][0]

    if self.curr_group < 0:
      diagonal = (carta_ex.height**2 + carta_ex.width**2) ** 0.5
      container = pygame.Rect(
        0,
        0,
        diagonal * len(self.inventario.get_items_list()),
        diagonal,
      )

      container.center = (
        self._screen.width / 2,
        self._screen.height - diagonal - 70,
      )

      container = self._screen.subsurface(container)

      pygame.draw.rect(container, "gray", ((0, 0), container.size))

      for deck_idx, deck in enumerate(self.decks):
        for idx, carta in enumerate(deck):
          sp = pygame.transform.rotate(carta.sprite, 45 - (45 * idx))
          container.blit(sp, (diagonal * deck_idx - diagonal * 0.1, 0))

    else:
      container = pygame.Rect(
        0,
        0,
        carta_ex.width * 0.75 * len(self.inventario.get_items_list()),
        carta_ex.height,
      )

      container.center = (
        self._screen.width / 2,
        self._screen.height - carta_ex.height - 70,
      )

      container = self._screen.subsurface(container)

      pygame.draw.rect(container, "gray", ((0, 0), container.size))
      for idx, carta in enumerate(self.decks[self.curr_group]):
        carta.render(
          container, (carta_ex.width * 0.75 * idx - carta_ex.width * 0.125, 0)
        )
