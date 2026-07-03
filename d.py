import pygame

s = pygame.display.set_mode((800, 800))


while True:
    pygame.draw.rect(s, (0, 200, 100), (s.width / 2-50, s.height / 2 -50, 100, 100))
    pygame.display.update()