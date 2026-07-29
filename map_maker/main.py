import pygame
from components.Canvas import Canvas
from components.Pallet import Pallet
from components.Help_Box import Help
from components.Filters import Filters
import Settings
from Settings import (
  CANVAS_HEIGHT,
  CANVAS_WIDTH,
  DEFAULT_FONT,
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
helper = Help(screen)

txt = pygame.font.Font("assets/fonts/main_font.ttf", 32)

running_game = True
while running_game:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      canvas.save_map()
      running_game = False
      continue

    if event.type == pygame.KEYDOWN:
      if pallet.show:
        if event.key in range(49, 59):
          pallet.change_pallet_ink(event.key - 49)
          canvas.waiting_second_point = False

      match event.key:
        case pygame.K_F1:
          helper.toggle_show()
        case pygame.K_l:
          filters.toggle_lines()
        case pygame.K_g:
          filters.toggle_grid()
        case pygame.K_ESCAPE:
          canvas.save_map()
          running_game = False
          continue
        case pygame.K_p:
          pallet.toggle_show()
        case pygame.K_c:
          pallet.change_pensil()
        case pygame.K_r:
          if event.mod == pygame.KMOD_NONE:
            if pallet.curr_pensil == "enemy":
              pallet.change_sprite_direction()

          elif pygame.KMOD_LSHIFT:
            canvas.map = pygame.transform.smoothscale(
              canvas.map, (screen.get_width(), screen.get_height())
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
        if pallet.curr_pensil == "rect":
          canvas.draw_rect(pallet.selected_color)
        elif pallet.curr_pensil == "enemy":
          canvas.draw_enemy(pallet.get_sprite(True))

  if pallet.curr_pensil == "tile":
    if pygame.mouse.get_pressed()[0]:
      canvas.draw_tile(pallet.selected_color)

  if pygame.mouse.get_pressed()[1]:
    canvas.clean_all()
  elif pygame.mouse.get_pressed()[2]:
    canvas.erase(pallet.curr_pensil)

  canvas.update()

  if filters.show_lines:
    filters.render_mouse_lines()
  if filters.show_grid:
    if pygame.key.get_pressed()[pygame.K_UP]:
      Settings.TILE_SIZE += 1
      canvas.update_grid_tiles()
    if pygame.key.get_pressed()[pygame.K_DOWN] and Settings.TILE_SIZE > 1:
      Settings.TILE_SIZE -= 1
    canvas.update_grid_tiles()

    filters.render_grid()

  if pallet.show:
    pallet.update(screen.get_width() / 2 - pallet.width / 2, 100)
    pallet.render()

  if pallet.curr_pensil == "enemy":
    sprite_demo = pallet.get_sprite()
    sprite_demo = pygame.transform.scale(
      sprite_demo, (Settings.TILE_SIZE, Settings.TILE_SIZE)
    )
    screen.blit(sprite_demo, canvas.get_tile_coords())
  else:
    pensil_mode = DEFAULT_FONT.render(
      str(
        pallet.curr_pensil + ("*" if canvas.waiting_second_point else "")
      ).capitalize(),
      False,
      COLORS["fg"],
      COLORS["bg"],
    )
    screen.blit(
      pensil_mode, (pygame.mouse.get_pos()[0] + 20, pygame.mouse.get_pos()[1])
    )
  if helper.show:
    helper.render()
  pygame.display.update()

pygame.quit()
