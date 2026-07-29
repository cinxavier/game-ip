import json
import pygame
from src.personagens.Inimigo import Inimigo

paredes: list[tuple[int, pygame.Rect]] = []
with open("data/tile_map.json", "r") as file:
  paredes = json.load(file)
  for parede in paredes:
    x, y, w, h = parede[1]
    parede[1] = pygame.Rect(x, y, w, h)

lista_inimigos: list[Inimigo] = []
with open("data/enemies_map.json", "r") as file:
  lista_dados_inimigos: list[
    tuple[
      list[str],
      list[int],
      list[int],
    ]
  ] = json.load(file)

  for dados_sprite, colisao_inimigo, campo_inimigo in lista_dados_inimigos:
    inimigo = Inimigo(dados_sprite, pygame.Rect(colisao_inimigo),pygame.Rect(campo_inimigo))
    lista_inimigos.append(inimigo)

with open("data/settings.json", "r") as file:
  imported_settings = json.load(file)
spawnpoint = imported_settings["spawnpoint"] or (2, (0, 0, 16, 16))
spawnpoint = (spawnpoint[0], pygame.Rect(spawnpoint[1]))
