import pygame
import pygame.locals as pg_lc
from Settings import screen_colors
from src.Canvas import Canvas
import json

pygame.init()
pygame.display.set_caption("Map Maker")

canvas = Canvas()
running_game = True
while running_game:
  canvas.draw_grid()
  for event in pygame.event.get():
    if event.type == pg_lc.QUIT:
      with open("cache.json", "w") as cache:
        json.dump(canvas.drawings, cache, indent=2)

      running_game = False

  if pygame.mouse.get_pressed()[0]:
    try:
      canvas.draw(tuple(event.pos))
      canvas.change_color(tuple(event.pos))
    except AttributeError:
      pass

  if pygame.mouse.get_pressed()[2]:
    try:
      canvas.draw(tuple(event.pos), screen_colors["tile_color"])
    except AttributeError:
      pass

  pygame.display.update()

pygame.quit()
