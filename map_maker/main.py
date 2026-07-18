import pygame
from src.Canvas import Canvas
from src.Pallet import Pallet
import Settings
from Settings import (
  CANVAS_HEIGHT,
  CANVAS_WIDTH,
  PALLET_COLORS,
  DEFAULT_FONT,
  PENSILS,
  COLORS,
)

pygame.init()
pygame.display.set_caption("Map Maker")


fullscreen = True
screen = pygame.display.set_mode(
  (CANVAS_WIDTH, CANVAS_HEIGHT),
  pygame.FULLSCREEN if fullscreen else pygame.RESIZABLE,
)

canvas = Canvas(screen)
pallet = Pallet(screen)
show_pallet = False
txt = pygame.font.Font("assets/fonts/main_font.ttf", 32)

running_game = True
while running_game:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      canvas.save_map()
      running_game = False
      continue

    if event.type == pygame.KEYDOWN:
      if show_pallet:
        if event.key in range(49, 49 + len(PALLET_COLORS)):
          pallet.selected_color = int(pygame.key.name(event.key)) - 1

      match event.key:
        case pygame.K_l:
          canvas.toggle_lines()
        case pygame.K_g:
          canvas.toggle_grid()
        case pygame.K_ESCAPE:
          canvas.save_map()
          running_game = False
          continue
        case pygame.K_p:
          show_pallet = not show_pallet
        case pygame.K_c:
          canvas.pensil_idx = 1 if canvas.pensil_idx == 0 else 0

    if event.type == pygame.MOUSEWHEEL:
      if event.y > 0:
        Settings.TILE_SIZE += 1
      else:
        if Settings.TILE_SIZE > 1:
          Settings.TILE_SIZE -= 1
      canvas.update_grid_tiles()

    if PENSILS[canvas.pensil_idx] == "rect":
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          canvas.draw(pallet.selected_color)

  if pygame.key.get_pressed()[pygame.K_UP]:
    Settings.TILE_SIZE += 1
    canvas.update_grid_tiles()
  if pygame.key.get_pressed()[pygame.K_DOWN] and Settings.TILE_SIZE > 1:
    Settings.TILE_SIZE -= 1
    canvas.update_grid_tiles()
  if PENSILS[canvas.pensil_idx] != "rect":
    if pygame.mouse.get_pressed()[0]:
      canvas.draw(pallet.selected_color)

  if pygame.mouse.get_pressed()[1]:
    canvas.clean_all()

  elif pygame.mouse.get_pressed()[2]:
    canvas.erase()

  canvas.update()
  canvas.render_mouse_lines()
  canvas.render_grid()

  if show_pallet:
    pallet.render(
      screen.get_width() / 2 - pallet.width / 2, screen.get_height() - 200
    )

  pensil_mode = DEFAULT_FONT.render(
    str(
      PENSILS[canvas.pensil_idx] + ("*" if canvas.waiting_rect_width else "")
    ).capitalize(),
    False,
    COLORS["fg"],
    COLORS["bg"],
  )
  screen.blit(
    pensil_mode, (pygame.mouse.get_pos()[0] + 20, pygame.mouse.get_pos()[1])
  )
  pygame.display.update()

pygame.quit()
