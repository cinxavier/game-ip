import pygame
import pygame.locals as pg_lc
from src.Canvas import Canvas
from src.Pallet import Pallet
from Settings import CANVAS_HEIGHT, CANVAS_WIDTH

pygame.init()
pygame.display.set_caption("Map Maker")


fullscreen = True
screen = pygame.display.set_mode(
  (CANVAS_WIDTH, CANVAS_HEIGHT),
  pg_lc.FULLSCREEN if fullscreen else pg_lc.RESIZABLE,
)

canvas = Canvas(screen)
pallet = Pallet(screen)
txt = pygame.font.Font("assets/fonts/main_font.ttf", 32)

running_game = True
while running_game:
  for event in pygame.event.get():
    if event.type == pg_lc.QUIT:
      canvas.save_map()
      running_game = False
      continue

    if event.type == pg_lc.KEYDOWN:
      match event.key:
        case pg_lc.K_l:
          canvas.toggle_lines()
          break
        case pg_lc.K_g:
          canvas.toggle_grid()
          break
        case pg_lc.K_ESCAPE:
            canvas.save_map()
            running_game = False
            continue
        case pg_lc.K_p:
            
            break

  if pygame.mouse.get_pressed()[0]:
    canvas.draw(0)

  if pygame.mouse.get_pressed()[1]:
    canvas.clean_all()

  if pygame.mouse.get_pressed()[2]:
    canvas.erase()

  canvas.update()
  canvas.render_mouse_lines()
  canvas.render_grid()
  pygame.display.update()

pygame.quit()
