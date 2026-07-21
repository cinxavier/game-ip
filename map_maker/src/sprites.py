import pygame
from pathlib import Path


def listar(path: str):
  frames: list[pygame.Surface] = []

  for idx, item in enumerate(Path(path).iterdir()):
    if item.is_file() and item.name[0].isdigit():
      frames.append(pygame.image.load(f"{path}/{idx + 1}.png"))
  return frames


ELETRICO = "Eletrico"
METAL = "Metal"
BORRACHA = "Borracha"
TIPOS = [
  ELETRICO,
  METAL,
  BORRACHA,
]

BOSS = "Boss"
SLIME = "Slime"
NIVEIS = [BOSS, SLIME]

FRENTE = "Frente"
COSTAS = "Costas"
DIREITA = "Direita"
ESQUERDA = "Esquerda"
DIRECOES = [
  FRENTE,
  COSTAS,
  DIREITA,
  ESQUERDA,
]

ANDANDO = "Andando"
ATAQUE = 'Ataque'
PARADO = "Parado"
MORTE = 'Morte'

ATACAR = "Atacar"
DEFENDER = "Defender"
USAR = "Usar"
ACOES = [
  ATACAR,
  DEFENDER,
  USAR,
]


class Inimigo:
  def __init__(self, nivel, elemento):
    self.nivel = nivel
    self.elemento = elemento

  def parado(self, direcao):
    return listar(
      f"assets/images/Inimigos/{self.nivel}/{self.elemento}/Parado/{direcao}"
    )

  def atacando(self):
    return listar(f"assets/images/Inimigos/{self.nivel}/{self.elemento}/Ataque")

  def morrendo(self):
    return listar(f"assets/images/Inimigos/{self.nivel}/{self.elemento}/Morte")


class Coletavel:
  def util(self):
    return listar("assets/images/Coletavel/Utilitario")

  def elemento(self):
    return listar("assets/images/Coletavel/Elemental")

  def forma(self):
    return listar("assets/images/Coletavel/Forma")


class Player:
  def andando(self, direcao):
    if direcao == DIREITA:
      sprites_esquerda = listar(f"assets/images/Player/Andando/{ESQUERDA}")
      sprites_direita = []
      for sprite in sprites_esquerda:
        sprites_direita.append(pygame.transform.flip(sprite, True, False))
      return sprites_direita

    return listar(f"assets/images/Player/Andando/{direcao}")

  def parado(self, direcao):
    return listar(f"assets/images/Player/Parado/{direcao}")

  def atacando(self):
    return listar("assets/images/Player/Atacando")
