import pygame
from game_data import Main_Font


class Button:
    def __init__(
        self,
        screen: pygame.Surface,
        image: pygame.Surface,
        pos: tuple[int, int],
        text_input: str,
    ):
        self.screen = screen
        self.image = image
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.text_input = text_input
        self.text = Main_Font.render(text_input, True, "white")
        self.text_rect = self.text.get_rect(center=self.pos)

    def update(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text, self.text_rect)

    def on_hover(self):
        self.text = Main_Font.render(self.text_input, True, "red")

    def on_release(self):
        self.text = Main_Font.render(self.text_input, True, "red")

    def on_click(self):
        print("clicado")