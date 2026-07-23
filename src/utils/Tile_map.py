import json
import pygame
from .sprites import Inimigo

paredes: list[tuple[int, pygame.Rect]] = []
with open("data/tile_map.json", "r") as file:
  paredes = json.load(file)
  for parede in paredes:
    x, y, w, h = parede[1]
    parede[1] = pygame.Rect(x, y, w, h)

inimigos: list[tuple[pygame.Surface, pygame.Rect, pygame.Rect]] = []
with open("data/enemies_map.json", "r") as file:
  inimigos = json.load(file)
  for idx,(dados_sprite, colisao_inimigo, campo_inimigo) in enumerate(inimigos):
    sprite = Inimigo(dados_sprite[0], dados_sprite[1]).parado(dados_sprite[2])[0]

    inimigos[idx][1] = pygame.Rect(colisao_inimigo)
    sprite = pygame.transform.smoothscale(sprite, (colisao_inimigo[2], colisao_inimigo[3]))
    inimigos[idx][0] = sprite
    inimigos[idx][2] = pygame.Rect(campo_inimigo)

with open("data/settings.json", "r") as file:
  imported_settings = json.load(file)
spawnpoint = imported_settings["spawnpoint"] or (2, (0, 0, 16, 16))
spawnpoint = (spawnpoint[1], pygame.Rect(spawnpoint[2]))
