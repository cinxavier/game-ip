import pygame
from .Base_Screen import ScreenBase
from utils import Button
from game_data import background


class Home(ScreenBase):
  def __init__(self, game):
    super().__init__(game)

    start_btn_size = start_btn_width, start_btn_height = (90, 40)
    self.start_btn = Button(
      game._screen,
      start_btn_size,
      (
        game._screen.width / 2 - start_btn_width - 20,
        game._screen.height - start_btn_height - 50,
      ),
      "Começar",
    )

    config_btn_size = config_btn_width, config_btn_height = (110, 40)
    self.config_btn = Button(
      game._screen,
      config_btn_size,
      (
        game._screen.width / 2 + 20,
        game._screen.height - config_btn_height - 50,
      ),
      "Configurar",
    )

    self.selectables = [self.start_btn, self.config_btn]
    self.selected_btn = self.selectables[self.hovering_btn_idx]
    self.selected_btn.on_hover()

  def handle_events(self, events):
    for event in events:
      if event.type == pygame.QUIT:
        self.game._running = False
        continue

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.game._running = False
          continue

        if event.key == pygame.K_d:
          self.selected_btn.on_release()
          self.surf("n")
          self.selected_btn.on_hover()

        if event.key == pygame.K_a:
          self.selected_btn.on_release()
          self.surf("p")
          self.selected_btn.on_hover()

  def render(self, screen: pygame.Surface):
    screen.fill(background)
    self.start_btn.render()
    self.config_btn.render()
    pygame.draw.line(
      screen, (200, 200, 200), (screen.width / 2, 0), (screen.width / 2, screen.height)
    )
