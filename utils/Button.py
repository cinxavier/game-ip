import pygame
class Button:
    def __init__(self, image:pygame.Surface, pos: tuple[int, int], text_input):
        self.image = image
        self.pos = pos
        self.rect = self.image.get_rect()
        self.text_input = text_input
        self.text = ''

imag = pygame.image.load('')