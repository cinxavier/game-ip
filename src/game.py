import os
import sys

import pygame

if __package__ is None and __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from game_data import primary, secondary
from interfaces.home_screen import home


class Game:
    def __init__(self):
        self._running = True
        self._screen = None
        self.size = self.width, self.height = 800, 600
        self.curr_screen = 0

        self.on_init()

    def on_init(self):
        pygame.init()
        self._screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self._running = True

    def on_event(self, event: pygame.Event):
        if event.type == pygame.QUIT:
            self._running = False

        if pygame.key.get_pressed()[pygame.K_e]:
            self.curr_screen = 1
        elif pygame.key.get_pressed()[pygame.K_d]:
            self.curr_screen = 0

    def loop(self):
        pass


    def render(self):
        match self.curr_screen: 
            case 0:
                self._screen.fill(primary)
                pygame.draw.rect(self._screen, secondary, (10, 10, 120, 60))
            case 1:
                home(self._screen)

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
