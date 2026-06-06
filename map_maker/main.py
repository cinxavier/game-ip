import pygame
import pygame.locals as pg_lc
from Settings import screen_colors
from src.Canvas import Canvas
from src.Pallet import Pallet

pygame.init()
pygame.display.set_caption("Map Maker")

# janela que carrega a tela e a paleta


canvas = Canvas()
pallet = Pallet(canvas.size)

screen = pygame.display.set_mode((canvas.size + pallet.width, canvas.size))
screen.fill(screen_colors["bg_color"])

canvas.draw_grid(screen)
pallet.draw_pallet(screen)

running_game = True
while running_game:
  for event in pygame.event.get():
    if event.type == pg_lc.QUIT:
      canvas.save_drawing()
      running_game = False

    if event.type == pg_lc.KEYDOWN:
      if pygame.key.get_pressed()[pg_lc.K_p]:
        canvas.clean_all(screen)

  if pygame.mouse.get_pressed()[0]:
    canvas.draw(pallet.selected_color)
    pallet.change_color()

  if pygame.mouse.get_pressed()[1]:
    canvas.clean_all(screen)

  if pygame.mouse.get_pressed()[2]:
    canvas.draw(screen_colors["tile_color"])

  canvas.draw_grid(screen)
  pygame.display.update()

pygame.quit()
