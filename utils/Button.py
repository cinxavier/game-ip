import pygame
from game_data import (
  Main_Font,
  primary_dark,
  secondary,
  button_border_thickness,
  primary_light,
)


class Button:
  def __init__(
    self,
    screen: pygame.Surface,
    size: tuple[int, int],
    pos: tuple[int, int],
    text_input: str,
  ):
    self.screen = screen
    self.size = self.width, self.height = size
    self.pos = self.x, self.y = pos

    self.text_input = text_input
    self.text = Main_Font.render(text_input, True, "white")
    self.text_rect = self.text.get_rect(
      center=(self.x + self.width / 2, self.y + self.height / 2 - 1 )
    )

    self.is_selected = False

  def render(self):
    if self.is_selected:
      pygame.draw.rect(
        self.screen,
        primary_light,
        (
          self.x - button_border_thickness * 1.5,
          self.y - button_border_thickness * 1.5,
          self.width + button_border_thickness * 3,
          self.height + button_border_thickness * 3,
        ),
      )

    self.border = pygame.draw.rect(
      self.screen,
      primary_dark,
      (
        self.x - button_border_thickness,
        self.y - button_border_thickness,
        self.width + button_border_thickness * 2,
        self.height + button_border_thickness * 2,
      ),
    )

    self.content = pygame.draw.rect(self.screen, secondary, (self.pos, self.size))

    self.screen.blit(self.text, self.text_rect)

  def on_hover(self):
    self.is_selected = True

  def on_release(self):
    self.is_selected = False

  def on_click(self, do_something):
    do_something()
