import pygame
from src.types.Type_Switch_Stand import Type_Switch_Stand


class ScreenBase:
  def __init__(self, game: Type_Switch_Stand):
    self.game = game
    self._screen: pygame.Surface = self.game._screen
    self._running: bool = self.game._running

  def handle_events(self, events: list[pygame.event.Event]):
    pass

  def update(self):
    pass

  def render(self):
    pass
