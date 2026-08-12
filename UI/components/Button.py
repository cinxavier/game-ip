import pygame
from theme import sizes, colors, fonts


class Button:
  def __init__(
    self,
    screen: pygame.Surface,
    text_input: str,
  ):
    self._screen = screen

    self.text_input = text_input
    self.text = fonts.DEFAULT.render(text_input, True, "white")
    self.size = self.width, self.height = (
      self.text.width * 1.5 + sizes.BTN_BORDER * 2,
      self.text.height * 1.5 + sizes.BTN_BORDER * 2,
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
      colors.PRIMARY_DARK,
      (self.pos, self.size),
    )

    pygame.draw.rect(
      self._screen,
      colors.BTN_BG,
      (
        self.x + sizes.BTN_BORDER,
        self.y + sizes.BTN_BORDER,
        self.width - sizes.BTN_BORDER * 2,
        self.height - sizes.BTN_BORDER * 2,
      ),
    )

    self._screen.blit(self.text, self.text_rect)

  def on_click(self):
    pass
