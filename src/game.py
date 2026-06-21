import os
import sys

import pygame

if __package__ is None and __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from game_data.colors import primary
from interfaces.home_screen import home


class Game:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 600, 400
        self.screen = 0

        self.on_init()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self._running = True

    def on_event(self, event: pygame.Event):
        if event.type == pygame.QUIT:
            self._running = False

        if pygame.key.get_pressed() == pygame.K_e:
            self.screen = 1
        elif pygame.key.get_pressed() == pygame.K_d:
            self.screen = 0
        print(pygame.key.get_pressed() == pygame.K_e)

    def loop(self):
        pass

    def render(self):
        self._display_surf.fill(primary)
        match self.screen:
            case 0:
                pygame.draw.rect(self._display_surf, (255, 0, 0), (50, 50, 50, 50))
            case 1:
                pygame.draw.rect(self._display_surf, (0, 255, 0), (50, 50, 50, 50))

        pygame.display.update()

    def cleanup(self):
        pygame.quit()

    def run(self):
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)

            self.loop()
            self.render()

        self.cleanup()


game = Game()
game.run()
