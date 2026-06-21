import pygame
# from game_data.fonts import Cambria


def home(screen: pygame.Surface):
    font = pygame.font.SysFont("Arial", 50)
    PLAY_BTN = font.render("teste de texto", True, (200, 200, 200))
    
    screen.fill((0, 0, 0))
    screen.blit(PLAY_BTN, (50, 50))