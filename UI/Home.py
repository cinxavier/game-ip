import pygame
from src.types.Base_Screen import ScreenBase
from .components.Button import Button
from theme import colors
from theme import sizes

from src.types.Type_Switch_Stand import Type_Switch_Stand


class StartButton(Button):
  def __init__(
    self, screen: pygame.Surface, text_input: str, game: Type_Switch_Stand
  ):
    super().__init__(screen, text_input)
    self.game = game

  def on_click(self):
    self.game.change_screen("game")


class ExitButton(StartButton):
  def on_click(self):
    self.game._running = False


class Home(ScreenBase):
  def __init__(self, game):
    super().__init__(game)
    self.selectables: list[Button] = [
      StartButton(self._screen, "Começar", game),
      ExitButton(self._screen, "Sair", game),
    ]

    btns_container = pygame.Rect(0, 0, 0, 0)
    for btn in self.selectables:
      btns_container.width += btn.width
    btns_container.width += sizes.BTN_BORDER * 4

    btns_container.height = btn.height
    btns_container.height += sizes.BTN_BORDER * 2

    btns_container.centerx = self._screen.width / 2
    btns_container.centery = self._screen.height / 2

    self.btns_container = self._screen.subsurface(btns_container)
    self.hovering_btn_idx = 0
    self.selected_btn = self.selectables[self.hovering_btn_idx]
    for btn in self.selectables:
      btn._screen = self.btns_container

  def update(self):
    if self.hovering_btn_idx >= len(self.selectables):
      self.hovering_btn_idx = len(self.selectables) - 1
    elif self.hovering_btn_idx < 0:
      self.hovering_btn_idx = 0

    self.selected_btn = self.selectables[self.hovering_btn_idx]

  def handle_events(self, events: list[pygame.Event]):
    for event in events:
      if event.type == pygame.KEYDOWN:
        match event.key:
          case pygame.K_ESCAPE:
            self.game._running = False
            break
          case pygame.K_d:
            self.hovering_btn_idx += 1

          case pygame.K_a:
            self.hovering_btn_idx -= 1

          case pygame.K_SPACE:
            self.selected_btn.on_click()

  def render(self):
    self._screen.fill(colors.BACKGROUND)

    last = sizes.BTN_BORDER
    for idx, btn in enumerate(self.selectables):
      if idx == self.hovering_btn_idx:
        pygame.draw.rect(
          self.btns_container,
          colors.SECONDARY,
          (
            last - sizes.BTN_BORDER,
            0,
            btn.width + sizes.BTN_BORDER * 2,
            btn.height + sizes.BTN_BORDER * 2,
          ),
        )
      btn.render((last, sizes.BTN_BORDER))
      last += btn.width + sizes.BTN_BORDER * 2
