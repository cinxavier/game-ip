import json
import pygame

info_paredes = []
with open("data/tile_map.json", "r") as file:
  info_paredes = json.load(file)

paredes: list[tuple[int, pygame.Rect]] = []
for tijolo in info_paredes:
  x, y, w, h = tijolo[1]
  paredes.append([tijolo[0], pygame.Rect(x, y, w, h)])
