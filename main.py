import pygame
from interfaces.Home import Home
from src.Jogo import Jogo
from src.types.Type_Switch_Stand import Type_Switch_Stand

class Main(Type_Switch_Stand):
  def __init__(self):
    pygame.init()

    size = pygame.display.get_desktop_sizes()[0]
    self._screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    self._running = True

    self.screens = {"home": Home(self), "game": Jogo(self)}
    self.curr_screen = self.screens["home"]

  def cleanup(self):
    pygame.quit()

  def change_screen(self, new_screen_name: str):
    self.curr_screen = self.screens[new_screen_name]

  def run(self):
    while self._running:
      events = pygame.event.get()
      for event in events:
        if event.type == pygame.QUIT:
          self._running = False
          continue

      self.curr_screen.handle_events(events)

      self.curr_screen.update()
      self.curr_screen.render()
      pygame.display.flip()
    self.cleanup()


if __name__ == "__main__":
  Main().run()
