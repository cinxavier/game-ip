import pygame
from theme import fonts, sizes, colors


class Help:
  def __init__(self, screen: pygame.Surface):
    self.screen = screen
    self.show = False

  def render(self):
    txt = """save & quit = ESC
toggle grid = G
toggle mouse lines = L
change pensil mode = C
toggle pallet = P
draw = LEFT CLICK
erase = RIGHT CLICK

**CAREFULL**
clear all = MIDDLE CLICK

*only when grid shown:
change tile size = ROLL UP/DOWN
OR KEY UP/DOWN"""
    text = fonts.DEFAULT.render(txt, False, colors.FOREGROUND)
    self.width, self.height = (
      text.width + sizes.BORDER * 2,
      text.height + sizes.BORDER * 2,
    )

    container = self.screen.subsurface((0, 0, self.width, self.height))
    pygame.draw.rect(container, colors.BACKGROUND, (0, 0, self.width, self.height))
    container.blit(text, (sizes.BORDER, sizes.BORDER))

  def toggle_show(self):
    self.show = not self.show
