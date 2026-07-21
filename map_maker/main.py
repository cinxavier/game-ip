import pygame
from src.Canvas import Canvas
from src.Pallet import Pallet, sprites
from src.Filters import Filters
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
filters = Filters(screen, canvas)
pallet = Pallet(screen)

txt = pygame.font.Font("assets/fonts/main_font.ttf", 32)

show_pallet = False
running_game = True
while running_game:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      canvas.save_map()
      running_game = False
      continue

    if event.type == pygame.KEYDOWN:
      if show_pallet:
        if event.key in range(49, 59):
          if PENSILS[canvas.pensil_idx] == "enemy":
            pallet.selected_sprite = min(
              int(pygame.key.name(event.key)) - 1, len(sprites) - 1
            )
          else:
            pallet.selected_color = min(
              int(pygame.key.name(event.key)) - 1, len(PALLET_COLORS) - 1
            )

      match event.key:
        case pygame.K_l:
          filters.toggle_lines()
        case pygame.K_g:
          filters.toggle_grid()
        case pygame.K_ESCAPE:
          canvas.save_map()
          running_game = False
          continue
        case pygame.K_p:
          show_pallet = not show_pallet
        case pygame.K_c:
          canvas.pensil_idx += (
            1 if canvas.pensil_idx < len(PENSILS) - 1 else -(len(PENSILS) - 1)
          )

    if event.type == pygame.MOUSEWHEEL:
      if event.y > 0:
        Settings.TILE_SIZE += 1
      else:
        if Settings.TILE_SIZE > 1:
          Settings.TILE_SIZE -= 1
      canvas.update_grid_tiles()

    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        if PENSILS[canvas.pensil_idx] == "rect":
          canvas.draw(pallet.selected_color)
        elif PENSILS[canvas.pensil_idx] == "enemy":
          canvas.draw(sprites[pallet.selected_sprite][1])

  if pygame.key.get_pressed()[pygame.K_UP]:
    Settings.TILE_SIZE += 1
    canvas.update_grid_tiles()
  if pygame.key.get_pressed()[pygame.K_DOWN] and Settings.TILE_SIZE > 1:
    Settings.TILE_SIZE -= 1
    canvas.update_grid_tiles()
  if PENSILS[canvas.pensil_idx] == "tile":
    if pygame.mouse.get_pressed()[0]:
      canvas.draw(pallet.selected_color)

  if pygame.mouse.get_pressed()[1]:
    canvas.clean_all()
  elif pygame.mouse.get_pressed()[2]:
    canvas.erase()

  canvas.update()

  if filters.show_lines:
    filters.render_mouse_lines()
  if filters.show_grid:
    filters.render_grid()

  if show_pallet:
    pallet.update(
      screen.get_width() / 2 - pallet.width / 2,
      screen.get_height() - pallet.height - 200,
      PENSILS[canvas.pensil_idx],
    )
    pallet.render()

  pensil_mode = DEFAULT_FONT.render(
    str(
      PENSILS[canvas.pensil_idx]
      + ("*" if canvas.waiting_rect_second_point else "")
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
