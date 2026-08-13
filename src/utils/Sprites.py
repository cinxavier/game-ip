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


ELETRICO = "Eletricidade"
METAL = "Metal"
BORRACHA = "Borracha"
ELEMENTOS = [
  ELETRICO,
  METAL,
  BORRACHA,
]

ANDANDO = "Andando"
ATAQUE = "Atacando"
PARADO = "Parado"
MORTE = "Morte"
ACOES = [
  ANDANDO,
  ATAQUE,
  PARADO,
]

FRENTE = "Frente"
COSTAS = "Costas"
DIREITA = "Direita"
ESQUERDA = "Esquerda"
DIRECOES = [
  FRENTE,
  DIREITA,
  COSTAS,
  ESQUERDA,
]

BOSS = "Boss"
SLIME = "Slime"
NIVEIS = [BOSS, SLIME]


class Inimigo:
  def __init__(self, nivel, elemento):
    self.nivel = nivel
    self.elemento = elemento

  def parado(self, direcao):
    return listar(
      f"assets/images/Inimigos/{self.nivel}/{self.elemento}/Parado", direcao
    )

  def atacando(self, direcao):
    return listar(
      f"assets/images/Inimigos/{self.nivel}/{self.elemento}/{ATAQUE}",
      direcao,
    )

  def morrendo(self):
    return listar(f"assets/images/Inimigos/{self.nivel}/{self.elemento}/Morte")


class Jogador:
  def __init__(self):
    self.sprites: dict[str, dict[str, list[pygame.Surface]]] = {}
    for acao in ACOES:
      self.sprites[acao] = {}
      for direcao in DIRECOES:
        if acao != ATAQUE:
          self.sprites[acao][direcao] = listar(
            f"assets/images/Player/{acao}", direcao
          )
        else:
          self.sprites[acao] = listar("assets/images/Player/Atacando")

  def andando(self, direcao):
    return self.sprites[ANDANDO][direcao]

  def parado(self, direcao):
    return self.sprites[PARADO][direcao]

  def atacando(self):
    return self.sprites[ATAQUE]


class Carta:
  BENCAO = "Bencao"
  CURA = "Cura"
  INVISIBILIDADE = "Invisibilidade"

  ELEMENTAIS = "Elementais"
  FORMAS = "Formas"
  UTILITARIOS = "Utilitarios"
  TIPOS_CARTAS = [
    ELEMENTAIS,
    FORMAS,
    UTILITARIOS,
  ]

  CIRCULO = "Circulo"
  QUADRADO = "Quadrado"
  TRIANGULO = "Triangulo"
  FORMAS_CARTAS = [
    CIRCULO,
    QUADRADO,
    TRIANGULO,
  ]

  def __init__(
    self,
    tipo_carta: str,
    carta: str,
  ):
    self.tipo_carta = tipo_carta
    self.carta = carta

  def coletavel(self):
    return listar(f"assets/images/Cartas/{self.tipo_carta}/Coletavel")

  def item(self):
    return pygame.image.load(
      f"assets/images/Cartas/{self.tipo_carta}/Itens/{self.carta}.png"
    )
