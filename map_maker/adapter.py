import pygame
import json

pygame.init()
width,height = pygame.display.get_desktop_sizes()[0]

with open("data/settings.json", "r") as file:
  settings = json.load(file)
with open("data/original.json", "r") as file:
  cache = json.load(file)

prorporcao_h = ((width  * 100) / settings["original_resolution"][0]) / 100
prorporcao_v = ((height * 100) / settings["original_resolution"][1]) / 100
new_cache = []
for slot in cache:
  rect = slot[1]
  new_cache.append(
    [
      slot[0],
      [
        rect[0] * prorporcao_h,
        rect[1] * prorporcao_v,
        rect[2] * prorporcao_h,
        rect[3] * prorporcao_v,
      ],
    ]
  )

with open("data/cache.json", "w") as file:
  json.dump(new_cache, file)
