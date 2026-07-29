import pygame
from game_data import (
  Main_Font,
  BTN_BACKGROUND,
  PRIMARY_DARK,
  button_border_thickness,
)


class Button:
  def __init__(
    self,
    screen: pygame.Surface,
    text_input: str,
  ):
    self._screen = screen

    self.text_input = text_input
    self.text = Main_Font.render(text_input, True, "white")
    self.size = self.width, self.height = (
      self.text.width * 1.5 + button_border_thickness * 2,
      self.text.height * 1.5 + button_border_thickness * 2,
    )

  def render(
    self,
    pos: tuple[int, int],
  ):
    self.pos = self.x, self.y = pos

    self.text_rect = self.text.get_rect(
      center=(self.x + self.width / 2, self.y + self.height / 2 - 1)
    )

    pygame.draw.rect(
      self._screen,
      PRIMARY_DARK,
      (self.pos, self.size),
    )

    pygame.draw.rect(
      self._screen,
      BTN_BACKGROUND,
      (
        self.x + button_border_thickness,
        self.y + button_border_thickness,
        self.width - button_border_thickness*2,
        self.height - button_border_thickness*2,
      ),
    )

    self._screen.blit(self.text, self.text_rect)

  def on_click(self):
    pass
