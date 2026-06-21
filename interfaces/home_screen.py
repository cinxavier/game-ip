import pygame
from utils.Button import Button
from game_data import Main_Font

btn_img = pygame.image.load("utils/btn.png")
btn_img = pygame.transform.scale(btn_img, (btn_img.width * 6, btn_img.height * 6))


def home(screen: pygame.Surface):
    PLAY_BTN = Main_Font.render("teste de texto", True, (200, 200, 200))
    btn = Button(screen, btn_img, (200, 200), "teste de btn")

    screen.fill((0, 0, 0))
    screen.blit(PLAY_BTN, (50, 50))
    btn.update()
