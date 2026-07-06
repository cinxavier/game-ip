import pygame
import pygame.locals as pg_lc
from src.Canvas import Canvas
from Settings import CANVAS_HEIGHT, CANVAS_WIDTH

pygame.init()
pygame.display.set_caption("Map Maker")


fullscreen = True
screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT), pg_lc.FULLSCREEN if fullscreen else pg_lc.RESIZABLE)

canvas = Canvas(screen)
txt = pygame.font.Font("assets/fonts/main_font.ttf", 32)

running_game = True
while running_game:
    for event in pygame.event.get():
        if event.type == pg_lc.QUIT:
            canvas.save_map()
            running_game = False
            continue

        if event.type == pg_lc.KEYDOWN:
            if event.key == pg_lc.K_f:
                fullscreen = not fullscreen
                screen = (
                    pygame.display.set_mode((0, 0), pg_lc.FULLSCREEN)
                    if fullscreen
                    else pygame.display.set_mode(
                        (CANVAS_WIDTH, CANVAS_HEIGHT), pg_lc.RESIZABLE
                    )
                )
                canvas.redimentionize(screen)

            if event.key == pg_lc.K_l:
                canvas.toggle_lines()

            if event.key == pg_lc.K_ESCAPE:
                canvas.save_map()
                running_game = False
                continue

    if pygame.mouse.get_pressed()[0]:
        canvas.draw(0)

    if pygame.mouse.get_pressed()[1]:
        canvas.clean_all()

    if pygame.mouse.get_pressed()[2]:
        canvas.draw(-1)

    canvas.render_mouse_lines()
    pygame.display.update()

pygame.quit()
