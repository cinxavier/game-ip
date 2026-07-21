import json
import pygame

info_paredes = []
with open("data/tile_map.json", "r") as file:
  info_paredes = json.load(file)

paredes: list[tuple[str,int, pygame.Rect]] = []
for tijolo in info_paredes:
  x, y, w, h = tijolo[2]
  paredes.append([tijolo[0], tijolo[1], pygame.Rect(x, y, w, h)])
with open("data/settings.json", "r") as file:
  imported_settings = json.load(file)
spawnpoint = imported_settings["spawnpoint"] or (2, (0, 0, 16, 16))
spawnpoint = (spawnpoint[1], pygame.Rect(spawnpoint[2]))
