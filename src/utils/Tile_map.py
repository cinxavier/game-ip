import json
import pygame
from src.personagens.Inimigo import Inimigo

tela = pygame.display.get_desktop_sizes()[0]
paredes: list[tuple[int, pygame.Rect]] = []
with open("data/tile_map.json", "r") as file:
  paredes = json.load(file)
  for parede in paredes:
    x, y, w, h = parede[1]
    x = tela[0] * x / 100
    w = tela[0] * w / 100
    y = tela[1] * y / 100
    h = tela[1] * h / 100
    parede[1] = pygame.Rect(x, y, w, h)


def init_inimigos():
  lista: list[Inimigo] = []
  with open("data/enemies_map.json", "r") as file:
    lista_dados_inimigos: list[
      tuple[
        list[str],
        list[int],
        list[int],
      ]
    ] = json.load(file)

    for dados_sprite, colisao_inimigo, campo_inimigo in lista_dados_inimigos:
      enemy_x, enemy_y, enemy_w, enemy_h = colisao_inimigo
      enemy_x = tela[0] * enemy_x / 100
      enemy_w = tela[0] * enemy_w / 100
      enemy_y = tela[1] * enemy_y / 100
      enemy_h = tela[1] * enemy_h / 100
      posicao = pygame.Rect(enemy_x, enemy_y, enemy_w, enemy_h)

      hitbox_x, hitbox_y, hitbox_w, hitbox_h = campo_inimigo
      hitbox_x = tela[0] * hitbox_x / 100
      hitbox_w = tela[0] * hitbox_w / 100
      hitbox_y = tela[1] * hitbox_y / 100
      hitbox_h = tela[1] * hitbox_h / 100
      campo_visao = pygame.Rect(hitbox_x, hitbox_y, hitbox_w, hitbox_h)

      inimigo = Inimigo(dados_sprite, posicao, campo_visao)
      lista.append(inimigo)
  return lista


lista_inimigos = init_inimigos()

with open("data/settings.json", "r") as file:
  imported_settings = json.load(file)
  x, y, w, h = imported_settings["spawnpoint"][1]
  x = tela[0] * x / 100
  w = tela[0] * w / 100
  y = tela[1] * y / 100
  h = tela[1] * h / 100
  imported_settings["spawnpoint"][1] = pygame.Rect(x, y, w, h)
spawnpoint = imported_settings["spawnpoint"]