import pygame
from .Inventario import Inventory
from .Carta import Carta
from theme.sizes import BORDER
from theme.colors import SECONDARY_DARK
from src.utils import Sprites


class Disco_Batalha:
  ACTIONS_GROUP = -1
  FORMS_GROUP = 0
  ELEMENTS_GROUP = 1
  ITEMS_GROUP = 2

  def __init__(self, tela: pygame.Surface, inventario: Inventory):
    self._screen = tela
    self.inventario = inventario

    self.decks = self.inventario.get_items_list().copy()
    self.action_cards = []
    for card in Sprites.Carta.ACOES_CARTAS:
      new_card = Carta(Sprites.Carta.ACOES, card)
      new_card.update(inventario.tile_size * 0.9)
      self.action_cards.append(new_card)
    self.curr_group = self.ACTIONS_GROUP
    self.cursor_idx = 0

  def events(self, evento: pygame.Event):
    if evento.type == pygame.KEYDOWN:
      match evento.key:
        case pygame.K_SPACE:
          if self.curr_group < self.ACTIONS_GROUP:
            self.curr_group = self.cursor_idx
            self.cursor_idx = 0
        case pygame.K_RIGHT | pygame.K_d:
          self.cursor_idx += 1
        case pygame.K_LEFT | pygame.K_a:
          self.cursor_idx -= 1

  def update(self):
    if self.curr_group >= len(self.decks):
      self.curr_group = -1

    if self.cursor_idx >= len(self.decks):
      self.cursor_idx = 0
    elif self.cursor_idx < 0:
      self.cursor_idx = len(self.decks) - 1

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
        if self.cursor_idx == deck_idx:
          pygame.draw.rect(
            container,
            SECONDARY_DARK,
            (
              BORDER - 5 + (BORDER + deck_w) * deck_idx,
              BORDER - 5,
              deck_w + 5 * 2,
              deck_h + 5 * 2,
            ),
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
        if self.cursor_idx == carta_idx:
          pygame.draw.rect(
            container,
            SECONDARY_DARK,
            (
              BORDER - 5 + (BORDER + carta.width) * carta_idx,
              BORDER - 5,
              carta.width + 5 * 2,
              carta.height + 5 * 2,
            ),
          )
        carta.render(
          container,
          (
            (carta_ex.width + BORDER) * carta_idx + BORDER,
            (container.height - carta.sprite.height) / 2,
          ),
        )
