import pygame
from pathlib import Path


def listar(path: str, direcao: str = ""):
  frames: list[pygame.Surface] = []

  direcao_real = direcao

  if direcao == ESQUERDA:
    direcao_real = DIREITA

  path = f"{path}/{direcao_real}" if direcao else path
  for idx, item in enumerate(Path(path).iterdir()):
    if item.is_file() and item.name[0].isdigit():
      img = pygame.image.load(f"{path}/{idx}.png")
      if direcao == ESQUERDA:
        img = pygame.transform.flip(img, True, False)
      frames.append(img)
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
ATAQUE = "Ataque"
PARADO = "Parado"
MORTE = "Morte"

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
      f"assets/images/Inimigos/{self.nivel}/{self.elemento}/Parado", direcao
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


class Jogador:
  def andando(self, direcao):
    return listar("assets/images/Player/Andando", direcao)

  def parado(self, direcao):
    return listar(f"assets/images/Player/Parado/{direcao}")

  def atacando(self):
    return listar("assets/images/Player/Atacando")
