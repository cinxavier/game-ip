import pygame
from Settings import DEFAULT_FONT, COLORS, BORDER


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
    text = DEFAULT_FONT.render(txt, False, COLORS["fg"])
    self.width, self.height = (
      text.width + BORDER * 2,
      text.height + BORDER * 2,
    )

    container = self.screen.subsurface((0, 0, self.width, self.height))
    pygame.draw.rect(container, COLORS["bg"], (0, 0, self.width, self.height))
    container.blit(text, (BORDER, BORDER))

  def toggle_show(self):
    self.show = not self.show
