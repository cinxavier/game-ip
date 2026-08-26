import pygame
from .Inventario import Inventory
from .Carta import Carta
from theme.sizes import BORDER


class Disco_Batalha:
  def __init__(self, tela: pygame.Surface, inventario: Inventory):
    self._screen = tela
    self.inventario = inventario

    self.decks = self.inventario.get_items_list().copy()
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
      deck_w = carta_ex.width + carta_ex.width * 0.2 * 2
      deck_h = carta_ex.height
      container = pygame.Rect(
        0,
        0,
        deck_w * (len(self.inventario.get_items_list())) + BORDER * 4,
        deck_h + BORDER * 2,
      )

      container.center = (
        self._screen.width / 2,
        self._screen.height - deck_w - 70,
      )

      container = self._screen.subsurface(container)

      pygame.draw.rect(container, "gray", ((0, 0), container.size))

      for deck_idx, deck in enumerate(self.decks):
        pygame.draw.rect(
          container,
          "green",
          ((BORDER + (deck_w + BORDER) * deck_idx, BORDER), (deck_w, deck_h)),
        )

        for carta_idx, carta in enumerate(deck):
          container.blit(
            carta.sprite,
            (
              BORDER
              + (deck_w + BORDER) * deck_idx
              + (deck_w - carta.sprite.width) / 2
              - carta_ex.width * 0.2
              + carta_ex.width * 0.2 * carta_idx,
              (container.height - deck_h) / 2,
            ),
          )

    else:
      container = pygame.Rect(
        0,
        0,
        (carta_ex.width + BORDER) * len(self.inventario.get_items_list()) + BORDER,
        carta_ex.height + BORDER * 2,
      )

      container.center = (
        self._screen.width / 2,
        self._screen.height - carta_ex.height - 70,
      )

      container = self._screen.subsurface(container)

      pygame.draw.rect(container, "gray", ((0, 0), container.size))
      for carta_idx, carta in enumerate(self.decks[self.curr_group]):
        carta.render(
          container,
          (
            (carta_ex.width + BORDER) * carta_idx + BORDER,
            (container.height - carta.sprite.height) / 2,
          ),
        )
